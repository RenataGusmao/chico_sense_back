"""Authorized sensor options and ADMIN provisioning. Never provisions ThingSpeak."""
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import AwareDatetime, Field, model_validator
from sqlalchemy import and_, exists, func, or_, select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_database_session
from app.models.iot import Dispositivo, Sensor
from app.models.enums import ContextoMedicao, StatusDispositivo, StatusSensor, StatusViagem, StatusCarga, TipoSensor
from app.models.sessoes_monitoramento import SessaoMonitoramento
from app.models.usuario import Usuario
from app.modules.monitoramento.service import MonitoramentoService, utc
from app.schemas.operacional import Input


class SensorPublico(Input):
    id: UUID
    identificador: str
    tipo: TipoSensor
    contexto: ContextoMedicao
    unidade: str
    dispositivo_id: UUID


class CatalogoResponse(Input):
    carga_id: UUID
    viagem_id: UUID
    ambiente: Literal['LABORATORIO', 'TRANSPORTE_REFRIGERADO']
    inicio_consultado: datetime
    total: int
    limit: int
    offset: int
    sensores: list[SensorPublico]
    disponibilidade_revalidada_ao_iniciar: Literal[True] = True


class SensorCadastro(Input):
    identificador: str = Field(min_length=1, max_length=120)
    tipo: TipoSensor
    contexto: ContextoMedicao
    unidade: str = Field(min_length=1, max_length=30)

    @model_validator(mode='after')
    def unidade_compativel(self):
        allowed = ('C', '°C', 'F', '°F', 'K') if self.tipo == TipoSensor.TEMPERATURA else ('%', '%RH')
        if self.unidade not in allowed: raise ValueError('Unidade incompativel com o tipo de sensor.')
        return self


class DispositivoCadastro(Input):
    identificador_dispositivo: str = Field(min_length=1, max_length=120)
    descricao: str | None = Field(default=None, max_length=255)
    sensores: list[SensorCadastro] = Field(min_length=1, max_length=2)

    @model_validator(mode='after')
    def distintos(self):
        if len({s.tipo for s in self.sensores}) != len(self.sensores) or len({s.identificador for s in self.sensores}) != len(self.sensores):
            raise ValueError('Informe no maximo um sensor de cada tipo, com identificadores distintos.')
        return self


def publico(sensor):
    return dict(id=sensor.id, identificador=sensor.identificador, tipo=sensor.tipo,
                contexto=sensor.contexto, unidade=sensor.unidade, dispositivo_id=sensor.dispositivo_id)


class CatalogoService(MonitoramentoService):
    def contexto_operacional(self, carga_id):
        carga, viagem = self.carga(carga_id)
        self.autorizar_viagem(viagem, escrita=True)
        return carga, viagem

    def listar(self, carga_id, ambiente, inicio, tipo, limit, offset):
        carga, viagem = self.contexto_operacional(carga_id)
        instant = utc(inicio) if inicio else datetime.now(timezone.utc)
        if instant > datetime.now(timezone.utc) or (viagem.inicio_real and instant < utc(viagem.inicio_real)):
            raise HTTPException(422, 'Inicio de consulta deve respeitar a viagem e nao estar no futuro.')
        links = [(Dispositivo.carga_id, carga.id), (Dispositivo.viagem_id, viagem.id), (Dispositivo.veiculo_id, viagem.veiculo_id)]
        compatible = and_(*(or_(column.is_(None), column == value) for column, value in links))
        bound = or_(*(column.is_not(None) for column, _ in links))
        if self.escopo.admin and ambiente == 'LABORATORIO': bound = True
        occupied = exists(select(SessaoMonitoramento.id).where(
            or_(SessaoMonitoramento.carga_id == carga.id, SessaoMonitoramento.sensor_temperatura_id == Sensor.id,
                SessaoMonitoramento.sensor_umidade_id == Sensor.id),
            or_(SessaoMonitoramento.fim.is_(None), SessaoMonitoramento.fim > instant)))
        units = or_(and_(Sensor.tipo == TipoSensor.TEMPERATURA, Sensor.unidade.in_(['C', '°C', 'F', '°F', 'K'])),
                    and_(Sensor.tipo == TipoSensor.UMIDADE, Sensor.unidade.in_(['%', '%RH'])))
        query = select(Sensor).join(Dispositivo, Dispositivo.id == Sensor.dispositivo_id).where(
            compatible, bound, units, ~occupied, Sensor.status == StatusSensor.ATIVO,
            Dispositivo.status == StatusDispositivo.ATIVO)
        if ambiente == 'TRANSPORTE_REFRIGERADO': query = query.where(Sensor.contexto != ContextoMedicao.PROTOTIPO)
        if tipo: query = query.where(Sensor.tipo == tipo)
        if viagem.status != StatusViagem.EM_ANDAMENTO or carga.status != StatusCarga.EM_TRANSITO:
            query = query.where(False)
        total = self.db.scalar(select(func.count()).select_from(query.subquery()))
        rows = self.db.scalars(query.order_by(Sensor.identificador, Sensor.id).limit(limit).offset(offset))
        return dict(carga_id=carga.id, viagem_id=viagem.id, ambiente=ambiente, inicio_consultado=instant,
                    total=total, limit=limit, offset=offset, sensores=[publico(row) for row in rows])

    def cadastrar(self, carga_id, data):
        if not self.escopo.admin: raise HTTPException(403, 'Cadastro de dispositivos exige ADMIN.')
        with self.transacao():
            carga, viagem = self.carga(carga_id, escrita=True)
            if carga.status in (StatusCarga.ENTREGUE, StatusCarga.CANCELADA) or viagem.status in (StatusViagem.CONCLUIDA, StatusViagem.CANCELADA):
                raise HTTPException(409, 'Contexto encerrado nao recebe novo dispositivo.')
            device = Dispositivo(identificador=data.identificador_dispositivo, descricao=data.descricao,
                carga_id=carga.id, viagem_id=viagem.id, veiculo_id=viagem.veiculo_id, status=StatusDispositivo.ATIVO)
            self.db.add(device); self.db.flush()
            sensors = [Sensor(dispositivo_id=device.id, status=StatusSensor.ATIVO, **item.model_dump()) for item in data.sensores]
            self.db.add_all(sensors); self.db.flush()
            response = [publico(sensor) for sensor in sensors]
        return response


router = APIRouter(prefix='/api/v1/cargas', tags=['Catalogo de sensores'])


@router.get('/{carga_id}/sensores-disponiveis', response_model=CatalogoResponse)
def catalogo(carga_id: UUID, ambiente: Literal['LABORATORIO', 'TRANSPORTE_REFRIGERADO'], inicio: AwareDatetime | None = None,
             tipo: Literal['TEMPERATURA', 'UMIDADE'] | None = None,
             limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
             db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    return CatalogoService(db, user).listar(carga_id, ambiente, inicio, tipo, limit, offset)


@router.post('/{carga_id}/sensores', response_model=list[SensorPublico], status_code=201)
def cadastrar(carga_id: UUID, data: DispositivoCadastro,
              db: Session = Depends(get_database_session), user: Usuario = Depends(get_current_user)):
    return CatalogoService(db, user).cadastrar(carga_id, data)
