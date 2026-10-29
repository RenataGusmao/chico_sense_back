"""Temporal acquisition coverage only: no q(T), volumes, imputation or risk."""
from datetime import datetime
from decimal import Decimal, localcontext, Context, ROUND_HALF_EVEN


def cobertura_temporal(inicio: datetime, fim: datetime, pontos: list[tuple[datetime, bool]], maximo_s: Decimal) -> dict:
    with localcontext(Context(prec=50, rounding=ROUND_HALF_EVEN)):
        def segundos(a, b):
            delta=b-a
            return Decimal(delta.days*86400+delta.seconds)+Decimal(delta.microseconds)/1000000
        total=segundos(inicio,fim)
        intervalos=[]
        def adicionar(a,b,motivo):
            if b>a:
                intervalos.append(dict(inicio=a,fim=b,duracao_s=segundos(a,b),motivo=motivo))
        if not pontos:
            adicionar(inicio,fim,"SEM_LEITURAS")
        else:
            adicionar(inicio,pontos[0][0],"BORDA_SEM_LEITURA")
            for a,b in zip(pontos,pontos[1:]):
                motivo="PONTO_INVALIDO_OU_CONFLITANTE" if not a[1] or not b[1] else (
                    "LACUNA_EXCESSIVA" if segundos(a[0],b[0])>maximo_s else None)
                adicionar(a[0],b[0],motivo)
            adicionar(pontos[-1][0],fim,"BORDA_SEM_LEITURA")
        coberto=sum((i['duracao_s'] for i in intervalos if i['motivo'] is None),Decimal(0))
        return dict(duracao_janela_s=total,duracao_coberta_s=coberto,
                    duracao_nao_coberta_s=total-coberto,
                    percentual_cobertura=coberto*100/total if total>0 else None,
                    intervalos=intervalos)
