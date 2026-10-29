"""Pure operational environmental rules; no q(T), ethylene volume or gas detection."""
from collections import defaultdict
from datetime import datetime
from decimal import Decimal,DecimalException,localcontext,Context,ROUND_HALF_EVEN
from app.modules.monitoramento.cobertura_iot import cobertura_temporal
from app.modules.monitoramento.etileno import converter_temperatura
from app.modules.monitoramento.analises_adapter import serializar

VERSAO='chicosense-preventivo-1.0.0'
LIMITACOES=[
    'Prioridade operacional; sem criterios validados de dano fisiologico.',
    'Amostras nao comprovam ausencia de variacao entre medicoes; sensor pode medir ar, nao polpa.',
    'Duracao usa dois extremos fora da mesma faixa/lado e retencao operacional entre amostras; sem preencher lacunas.',
    'Ausencia de alerta nao comprova seguranca ou ausencia de etileno.',
    'Intervencao depende de avaliacao humana; alerta ambiental nao recomenda automaticamente exaustao.',
]


def avaliar_ambiente(snapshot):
    with localcontext(Context(prec=50,rounding=ROUND_HALF_EVEN)):
        return serializar(_avaliar(snapshot))


def _avaliar(s):
    config=s['configuracao']; achados=[]
    def adicionar(regra,mensagem,evidencia,nivel=None):
        achados.append(dict(regra=regra,mensagem=mensagem,evidencia=evidencia,
            nivel=nivel or (config['prioridade'] if config else 'INFORMATIVO')))
    resultado=dict(versao_avaliador=VERSAO,classificacao_risco_etileno='NAO_AVALIADO',
        limitacoes=list(LIMITACOES),achados=achados,canais=[])
    if not config or s['sessao']['maturacao'] not in config['maturacoes_aplicaveis'] or s['sessao']['ambiente']!=config['ambiente']:
        resultado['status']='CONFIGURACAO_INSUFICIENTE'
        adicionar('CONFIGURACAO_AMBIENTAL_AUSENTE','Configuracao operacional ausente ou inaplicavel; condicoes ambientais nao avaliadas.',
            dict(maturacao=s['sessao']['maturacao'],ambiente=s['sessao']['ambiente']),'INFORMATIVO')
        return resultado
    if s['sessao']['maturacao'] in ('MISTA','DESCONHECIDA'):
        resultado['limitacoes'].append('Maturacao mista/desconhecida; aplicacao explicitamente operacional, sem presumir fruta verde ou madura.')
    a=datetime.fromisoformat(s['inicio']); b=datetime.fromisoformat(s['fim']); g=Decimal(config['intervalo_maximo_s'])
    falhas=[]; insuficientes=[]; prolongadas=[]
    for tipo,minimo,maximo in [('TEMPERATURA',config['temperatura_min_c'],config['temperatura_max_c']),
                                ('UMIDADE',config['umidade_min_percentual'],config['umidade_max_percentual'])]:
        grupos=defaultdict(list); desconhecido=False; barreiras=set(); incidentes=[]
        for o in s['ocorrencias']:
            if o['tipo'] not in (None,tipo): continue
            if o['codigo']=='CONFLITO_ORIGEM':
                affected=o['detalhes'].get('instantes_afetados',[]); relevante=not affected
                if not affected: desconhecido=True
                for raw in affected:
                    try: t=datetime.fromisoformat(raw.replace('Z','+00:00'))
                    except (ValueError,TypeError): desconhecido=True; relevante=True; continue
                    if t.tzinfo is None: desconhecido=True; relevante=True; continue
                    if a<=t<=b: barreiras.add(t); relevante=True
                if relevante: incidentes.append(o['id'])
            elif o['codigo'] in ('TIMESTAMP_INVALIDO','FEED_INVALIDO','ENTRY_ID_INVALIDO','FALHA_INTEGRIDADE','FALHA_PERSISTENCIA','HORARIO_FUTURO'):
                relevante=False
                if o['medida_em'] is None: desconhecido=True; relevante=True
                else:
                    t=datetime.fromisoformat(o['medida_em'])
                    if a<=t<=b: barreiras.add(t); relevante=True
                if relevante: incidentes.append(o['id'])
        invalidos=[]
        for row in s['leituras']:
            if row['tipo']!=tipo: continue
            t=datetime.fromisoformat(row['medida_em']); valor=None
            try:
                if row['estado']!='VALIDA': raise ValueError('Marcador invalido')
                if tipo=='TEMPERATURA':
                    valor=converter_temperatura(row['valor'],row['unidade'])
                    if valor<Decimal('-273.15'): raise ValueError('Temperatura abaixo do zero absoluto')
                else:
                    if row['unidade']!='%': raise ValueError('Unidade invalida')
                    valor=Decimal(row['valor'])
                    if not valor.is_finite() or not 0<=valor<=100: raise ValueError('Umidade invalida')
            except (ValueError,TypeError,DecimalException):
                valor=None; invalidos.append(row['id'])
            grupos[t].append((valor,row['id']))
        for t in barreiras: grupos[t]
        pontos=[]; anormais=[]
        lo=Decimal(minimo); hi=Decimal(maximo)
        for t,items in sorted(grupos.items()):
            valores={v for v,_ in items}; valido=bool(items) and None not in valores and len(valores)==1 and t not in barreiras
            valor=next(iter(valores)) if valido else None
            pontos.append((t,valido,valor))
            if valido and (valor<lo or valor>hi):
                anormais.append(dict(medida_em=t,valor=valor,registros=sorted(i for _,i in items),lado='ABAIXO' if valor<lo else 'ACIMA'))
        cobertura=cobertura_temporal(a,b,[(t,ok) for t,ok,_ in pontos],g)
        if desconhecido: cobertura['percentual_cobertura']=None
        canal=dict(tipo=tipo,unidade='C' if tipo=='TEMPERATURA' else '%',**cobertura,metadados_temporais_inconclusivos=desconhecido)
        resultado['canais'].append(canal)
        if anormais:
            adicionar('TEMPERATURA_FORA_DA_FAIXA' if tipo=='TEMPERATURA' else 'UMIDADE_FORA_DA_FAIXA',
                'Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.',
                dict(tipo=tipo,minimo=lo,maximo=hi,pontos=anormais,unidade=canal['unidade']))
        if cobertura['percentual_cobertura'] is None or cobertura['percentual_cobertura']<Decimal(config['cobertura_min_percentual']):
            insuficientes.append(dict(tipo=tipo,percentual=cobertura['percentual_cobertura'],
                minimo_percentual=config['cobertura_min_percentual'],duracao_coberta_s=cobertura['duracao_coberta_s'],
                duracao_nao_coberta_s=cobertura['duracao_nao_coberta_s']))
        gaps=[i for i in cobertura['intervalos'] if i['motivo'] in ('LACUNA_EXCESSIVA','PONTO_INVALIDO_OU_CONFLITANTE')]
        if gaps or invalidos or incidentes or desconhecido:
            falhas.append(dict(tipo=tipo,lacunas=gaps,registros_invalidos=sorted(invalidos),ocorrencias=sorted(incidentes),
                horario_inconclusivo=desconhecido))
        # No duration inferred from an isolated outlier or an out-of-range/in-range pair.
        sequencias=[]; corrente=None
        for p,q in zip(pontos,pontos[1:]):
            t,ok,v=p; u,ok2,w=q
            lado=lambda x: 'ABAIXO' if x<lo else ('ACIMA' if x>hi else None)
            delta=u-t; segundos=Decimal(delta.days*86400+delta.seconds)+Decimal(delta.microseconds)/1000000
            l=lado(v) if ok else None; l2=lado(w) if ok2 else None
            if ok and ok2 and l is not None and l==l2 and 0<segundos<=g:
                if corrente and corrente['fim']==t and corrente['lado']==l:
                    corrente['fim']=u; corrente['duracao_s']+=segundos
                else:
                    corrente=dict(tipo=tipo,inicio=t,fim=u,duracao_s=segundos,lado=l); sequencias.append(corrente)
            else: corrente=None
        limite=config['exposicao_continua_s']
        if limite is not None and not desconhecido:
            prolongadas.extend(x|dict(limite_s=limite) for x in sequencias if x['duracao_s']>=Decimal(limite))
    if prolongadas:
        adicionar('EXPOSICAO_AMBIENTAL_PROLONGADA','Persistencia entre amostras concordantes segundo regra operacional; duracao nao e limiar de dano.',dict(sequencias=prolongadas))
    if insuficientes:
        adicionar('COBERTURA_INSUFICIENTE','Dados ausentes ou cobertura abaixo do minimo operacional; resultado ambiental inconclusivo.',dict(canais=insuficientes))
    tentativas=[dict(id=r['id'],estado=r['estado']) for r in s['tentativas'] if r['estado'] in ('FALHA','PARCIAL','INTERROMPIDA')]
    if falhas or tentativas:
        adicionar('FALHA_MONITORAMENTO','Evidencia de falha, interrupcao ou inconsistencia na aquisicao; verificar monitoramento.',dict(canais=falhas,tentativas=tentativas))
    resultado['status']='INCONCLUSIVO' if insuficientes else 'AVALIADO'
    return resultado
