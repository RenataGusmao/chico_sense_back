"""Read queries for versioned acquisition, without implicit associations."""
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.historico_iot import FonteSessaoIoT, SincronizacaoIoT, RegistroSessaoIoT, OcorrenciaIoT
from app.models.iot import Medicao
from app.models.integracoes import LeituraExterna


class HistoricoIoTRepository:
    def __init__(self, db: Session):
        self.db=db

    def fontes(self, sessao_id: UUID):
        return list(self.db.scalars(select(FonteSessaoIoT).where(FonteSessaoIoT.sessao_id==sessao_id).order_by(FonteSessaoIoT.tipo)))

    def ultima_revisao(self, sessao_id: UUID):
        return self.db.scalar(select(func.max(SincronizacaoIoT.revisao)).where(SincronizacaoIoT.sessao_id==sessao_id)) or 0

    def registro(self, fonte_id: UUID, entry_id: int):
        return self.db.scalar(select(RegistroSessaoIoT).where(RegistroSessaoIoT.fonte_id==fonte_id,RegistroSessaoIoT.entry_id==entry_id))

    def externa(self, fonte: FonteSessaoIoT, entry_id: int):
        return self.db.scalar(select(LeituraExterna).where(
            LeituraExterna.origem==fonte.origem,LeituraExterna.channel_id==fonte.channel_id,
            LeituraExterna.field_name==fonte.field_name,LeituraExterna.entry_id==entry_id))

    def registros(self, sessao_id: UUID, revisao: int, inicio, fim, tipo=None):
        query=select(RegistroSessaoIoT,FonteSessaoIoT,SincronizacaoIoT.revisao).join(
            FonteSessaoIoT,RegistroSessaoIoT.fonte_id==FonteSessaoIoT.id).join(
            SincronizacaoIoT,RegistroSessaoIoT.sincronizacao_id==SincronizacaoIoT.id).where(
            RegistroSessaoIoT.sessao_id==sessao_id,SincronizacaoIoT.revisao<=revisao,
            SincronizacaoIoT.estado!="EM_EXECUCAO",RegistroSessaoIoT.medida_em>=inicio,RegistroSessaoIoT.medida_em<=fim)
        if tipo:
            query=query.where(FonteSessaoIoT.tipo==tipo)
        return query.order_by(RegistroSessaoIoT.medida_em,RegistroSessaoIoT.id)

    def ocorrencias(self, sessao_id: UUID, revisao: int):
        return list(self.db.scalars(select(OcorrenciaIoT).join(SincronizacaoIoT).where(
            SincronizacaoIoT.sessao_id==sessao_id,SincronizacaoIoT.revisao<=revisao,
            SincronizacaoIoT.estado!="EM_EXECUCAO").order_by(SincronizacaoIoT.revisao,OcorrenciaIoT.id)))

    def locais(self, fonte: FonteSessaoIoT, inicio, fim):
        return list(self.db.execute(select(Medicao,LeituraExterna).join(LeituraExterna,LeituraExterna.medicao_id==Medicao.id).where(
            Medicao.sensor_id==fonte.sensor_id,Medicao.medida_em>=inicio,Medicao.medida_em<=fim,
            LeituraExterna.origem==fonte.origem,LeituraExterna.channel_id==fonte.channel_id,
            LeituraExterna.field_name==fonte.field_name).order_by(Medicao.medida_em,LeituraExterna.entry_id)))
