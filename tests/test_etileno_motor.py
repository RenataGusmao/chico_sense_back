"""Acceptance examples E01-E12 and failure policies from the scientific specification."""
from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal, localcontext
from itertools import permutations
from pathlib import Path
import subprocess
import sys

import pytest

from app.modules.monitoramento.etileno import (
    EntradaEstimativa, EstagioMaturacao, LeituraTemperatura, ModoCalculo,
    Motivo, StatusCalculo, converter_massa, converter_temperatura, estimar_etileno,
)

D = Decimal
START = datetime(2026, 10, 1, tzinfo=timezone.utc)


def reading(seconds, temperature, **changes):
    return LeituraTemperatura(
        START + timedelta(seconds=seconds), temperature,
        changes.pop('sensor_id', 'temp-1'), changes.pop('sessao_id', 'demo'), **changes,
    )


def request(points=((0, 13), (3600, 13), (7200, 13)), end=7200, **changes):
    base = EntradaEstimativa(
        massa='1000', inicio=START, fim=START+timedelta(seconds=end),
        sensor_id='temp-1', sessao_id='demo',
        leituras=tuple(reading(t, value) for t, value in points), intervalo_maximo_s=3600,
    )
    return replace(base, **changes)


def assert_partition(result):
    assert sum((i.duracao_s for i in result.intervalos), D(0)) == result.duracao_janela_s
    assert result.duracao_coberta_s + result.duracao_nao_coberta_s == result.duracao_janela_s
    assert result.intervalos[0].inicio == result.inicio
    assert result.intervalos[-1].fim == result.fim
    assert all(a.fim == b.inicio for a,b in zip(result.intervalos,result.intervalos[1:]))
    assert all(i.duracao_s > 0 for i in result.intervalos)


@pytest.mark.parametrize('points,end,mass,expected', [
    (((0,13),(3600,13),(7200,13)),7200,'1000',('400','2000')),  # E01
    (((0,13),(3600,20),(7200,20)),7200,'1000',('700','9000')),  # E02
    (((0,10),(900,13),(3600,13)),3600,'500',('87.5','437.5')),  # E03
])
def test_documented_complete_examples(points,end,mass,expected):
    result=estimar_etileno(request(points,end,massa=mass))
    assert result.status_calculo == StatusCalculo.COMPLETO_NO_MODELO
    assert (result.volume_janela_min_ul,result.volume_janela_max_ul) == tuple(map(D,expected))
    assert result.volume_coberto_min_ul == result.volume_janela_min_ul
    assert result.percentual_cobertura == 100
    assert result.duracao_nao_coberta_s == 0
    assert_partition(result)


def test_e04_long_gap_is_excluded_in_full():
    result=estimar_etileno(request(((0,13),(3600,13),(10800,13)),10800))
    assert result.status_calculo == StatusCalculo.PARCIAL
    assert result.volume_coberto_min_ul == 200
    assert result.volume_coberto_max_ul == 1000
    assert result.volume_janela_min_ul is result.volume_janela_max_ul is None
    assert result.duracao_coberta_s == 3600
    assert result.duracao_nao_coberta_s == 7200
    assert result.intervalos[-1].motivos == (Motivo.LACUNA_EXCESSIVA,)
    assert_partition(result)


@pytest.mark.parametrize('points',[(),((3600,13),),((0,13),),((7200,13),)])
def test_e05_empty_or_single_reading_never_returns_zero(points):
    result=estimar_etileno(request(points))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert result.volume_coberto_min_ul is result.volume_coberto_max_ul is None
    assert result.volume_janela_min_ul is result.volume_janela_max_ul is None
    assert result.duracao_coberta_s == 0
    assert result.percentual_cobertura == 0
    assert_partition(result)


def test_e06_out_of_domain_blocks_both_adjacent_intervals():
    result=estimar_etileno(request(((0,13),(3600,13),(7200,25),(10800,13)),10800))
    assert result.status_calculo == StatusCalculo.PARCIAL
    assert result.volume_coberto_min_ul == 200
    assert result.volume_coberto_max_ul == 1000
    assert result.duracao_nao_coberta_s == 7200
    assert all(Motivo.FORA_DO_DOMINIO in i.motivos for i in result.intervalos[1:])
    assert_partition(result)


@pytest.mark.parametrize('maturity',list(EstagioMaturacao)+[None])
def test_e07_maturity_does_not_invent_corrections(maturity):
    result=estimar_etileno(request(maturacao=maturity))
    assert result.volume_janela_min_ul == 400
    assert result.volume_janela_max_ul == 2000
    assert result.classificacao_risco_etileno == 'NAO_AVALIADO'
    assert result.motivo_risco == 'SEM_LIMIAR_VALIDADO'
    assert 'NAO_VALIDADA' in result.aplicabilidade
    if maturity in (None,EstagioMaturacao.DESCONHECIDA):
        assert any('desconhecida' in text for text in result.limitacoes)
    if maturity == EstagioMaturacao.MISTA:
        assert any('mista' in text for text in result.limitacoes)


@pytest.mark.parametrize('mass',[None,0,-1,'NaN','Infinity',True,False,'10 caixas',D('-Infinity')])
def test_e08_invalid_mass_is_unavailable(mass):
    result=estimar_etileno(request(massa=mass))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert Motivo.MASSA_INVALIDA in result.motivos
    assert result.volume_coberto_min_ul is result.volume_janela_max_ul is None
    assert result.duracao_coberta_s is result.percentual_cobertura is None


def test_e09_interpolation_requires_exploratory_mode():
    args=request(((0,12),(3600,12)),3600)
    restricted=estimar_etileno(args)
    assert restricted.modo == ModoCalculo.MODO_RESTRITO
    assert restricted.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert restricted.motivos == (Motivo.SEM_TAXA_NO_MODO,)
    assert restricted.volume_coberto_min_ul is None
    result=estimar_etileno(replace(args,modo=ModoCalculo.MODO_EXPLORATORIO))
    assert result.volume_janela_min_ul == D('166.666667')
    assert result.volume_janela_max_ul == D('833.333333')
    assert result.interpolacao_utilizada
    assert 'exploratoria' in result.metodologia
    assert any('hipotese matematica' in s for s in result.limitacoes)


def test_e10_source_duplicates_and_input_permutations():
    points=tuple(reading(t,temp,identificador_externo=str(t)) for t,temp in ((0,13),(3600,20),(7200,20)))
    baseline=estimar_etileno(request(leituras=points))
    for reordered in permutations(points):
        result=estimar_etileno(request(leituras=reordered+(points[1],)))
        assert result.volume_janela_min_ul == 700
        assert result.volume_janela_max_ul == 9000
        assert result.intervalos == baseline.intervalos
        assert result.duplicatas_descartadas == 1
        assert len(result.observacoes) == 3


def test_e10_conflicting_temperature_is_a_barrier():
    points=(reading(0,13),reading(3600,20),reading(3600,15),reading(7200,20))
    result=estimar_etileno(request(leituras=points))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert result.volume_coberto_min_ul is None
    assert all(i.motivos[0] == Motivo.CONFLITO_OBSERVACAO for i in result.intervalos)
    assert_partition(result)


def test_e11_borders_are_not_extrapolated():
    result=estimar_etileno(request(((1800,13),(5400,13))))
    assert result.percentual_cobertura == 50
    assert result.volume_coberto_min_ul == 200
    assert result.volume_coberto_max_ul == 1000
    assert result.volume_janela_min_ul is None
    assert len(result.intervalos) == 3
    assert_partition(result)


@pytest.mark.parametrize('seconds,expected',[(3600,StatusCalculo.COMPLETO_NO_MODELO),(3601,StatusCalculo.SEM_ESTIMATIVA)])
def test_gap_boundary_is_exact(seconds,expected):
    result=estimar_etileno(request(((0,13),(seconds,13)),seconds))
    assert result.status_calculo == expected
    assert_partition(result)


def test_e12_engine_has_no_humidity_or_fan_input():
    # E01 executes with no humidity, alert, fan, DB or web input.
    result=estimar_etileno(request())
    assert result.volume_janela_min_ul == 400
    assert result.volume_janela_max_ul == 2000
    assert result.classificacao_risco_etileno == 'NAO_AVALIADO'


@pytest.mark.parametrize('mode',list(ModoCalculo))
@pytest.mark.parametrize('temperature,expected',[(10,('100','500')),(13,('200','1000')),(15,('300','4000')),(20,('500','8000'))])
def test_reference_points_are_identical_in_both_modes(mode,temperature,expected):
    result=estimar_etileno(request(((0,temperature),(3600,temperature)),3600,modo=mode))
    assert (result.volume_janela_min_ul,result.volume_janela_max_ul) == tuple(map(D,expected))
    assert not result.interpolacao_utilizada


@pytest.mark.parametrize('mode',list(ModoCalculo))
@pytest.mark.parametrize('temperature',['9.999','20.001',25,-10])
def test_no_extrapolation(mode,temperature):
    result=estimar_etileno(request(((0,temperature),(3600,temperature)),3600,modo=mode))
    assert result.volume_coberto_min_ul is None
    assert Motivo.FORA_DO_DOMINIO in result.motivos


@pytest.mark.parametrize('gap',[None,0,-1,True,'NaN','Infinity','bad'])
def test_gap_is_required_and_validated(gap):
    result=estimar_etileno(request(intervalo_maximo_s=gap))
    expected=StatusCalculo.CONFIGURACAO_INCOMPLETA if gap is None else StatusCalculo.ENTRADA_INVALIDA
    assert result.status_calculo == expected
    assert result.volume_coberto_min_ul is result.duracao_coberta_s is None


@pytest.mark.parametrize('value',[None,'bad','NaN','Infinity',True])
def test_invalid_temperature_is_preserved_without_bridging(value):
    result=estimar_etileno(request(((0,13),(1800,value),(3600,13)),3600))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert len(result.observacoes) == 3
    assert len(result.intervalos) == 2
    assert Motivo.TEMPERATURA_INVALIDA in result.motivos
    assert result.volume_coberto_min_ul is None
    assert_partition(result)


@pytest.mark.parametrize('value,unit,expected',[('500000','g','500'),('0.5','t','500'),('500','kg','500')])
def test_explicit_mass_conversions(value,unit,expected):
    assert converter_massa(value,unit) == D(expected)
    result=estimar_etileno(request(massa=value,unidade_massa=unit))
    assert result.massa_kg == D(expected)
    assert result.volume_janela_min_ul == 200


@pytest.mark.parametrize('value,unit',[('55.4','F'),('55.4','°F'),('286.15','K'),('13','C'),('13','°C')])
def test_explicit_temperature_conversions(value,unit):
    assert converter_temperatura(value,unit) == 13
    result=estimar_etileno(request(leituras=(reading(0,value,unidade=unit),reading(7200,value,unidade=unit)),intervalo_maximo_s=7200))
    assert result.volume_janela_min_ul == 400


def test_fahrenheit_conversion_does_not_snap_to_point():
    result=estimar_etileno(request(leituras=(reading(0,55,unidade='F'),reading(7200,55,unidade='F')),intervalo_maximo_s=7200))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert Motivo.SEM_TAXA_NO_MODO in result.motivos


@pytest.mark.parametrize('unit',['caixas','lb',''])
def test_unknown_mass_units_are_not_guessed(unit):
    result=estimar_etileno(request(unidade_massa=unit))
    assert result.massa_kg is None
    assert result.motivos == (Motivo.UNIDADE_MASSA_INVALIDA,)
    with pytest.raises(ValueError):
        converter_massa(1,unit)


def test_unknown_temperature_units_create_an_invalid_marker():
    points=(reading(0,13),reading(1800,13,unidade='unknown'),reading(3600,13))
    result=estimar_etileno(request(leituras=points,end=3600))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert Motivo.UNIDADE_TEMPERATURA_INVALIDA in result.motivos


@pytest.mark.parametrize('changes,reason',[
    ({'inicio':START.replace(tzinfo=None)},Motivo.JANELA_INVALIDA),
    ({'fim':START},Motivo.JANELA_INVALIDA),
    ({'fim':START-timedelta(seconds=1)},Motivo.JANELA_INVALIDA),
    ({'modo':'unknown'},Motivo.MODO_INVALIDO),
    ({'maturacao':'IMATURA'},Motivo.MATURACAO_INVALIDA),
    ({'sensor_id':''},Motivo.IDENTIDADE_INVALIDA),
    ({'corte_aquisicao':START.replace(tzinfo=None)},Motivo.HORARIO_INVALIDO),
])
def test_invalid_request_metadata(changes,reason):
    result=estimar_etileno(request(**changes))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert reason in result.motivos
    assert result.volume_coberto_min_ul is None


def test_explicit_none_mode_is_not_a_silent_default():
    result=estimar_etileno(request(modo=None))
    assert result.status_calculo == StatusCalculo.CONFIGURACAO_INCOMPLETA
    assert Motivo.MODO_AUSENTE in result.motivos


def test_invalid_input_precedes_incomplete_configuration():
    result=estimar_etileno(request(massa=0,intervalo_maximo_s=None))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert Motivo.MASSA_INVALIDA in result.motivos
    assert Motivo.INTERVALO_MAXIMO_AUSENTE in result.motivos


def test_invalid_timestamp_cannot_be_silently_dropped():
    points=(reading(0,13),replace(reading(3600,13),medida_em=START.replace(tzinfo=None)),reading(7200,13))
    result=estimar_etileno(request(leituras=points))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert result.motivos == (Motivo.HORARIO_INVALIDO,)


def test_future_reading_against_explicit_cutoff_invalidates_analysis():
    result=estimar_etileno(request(corte_aquisicao=START+timedelta(seconds=3600)))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert result.motivos == (Motivo.HORARIO_FUTURO,)


def test_source_id_with_different_timestamps_invalidates_identity():
    points=(reading(0,13,identificador_externo='same'),reading(7200,13,identificador_externo='same'))
    result=estimar_etileno(request(leituras=points))
    assert result.status_calculo == StatusCalculo.ENTRADA_INVALIDA
    assert result.motivos == (Motivo.IDENTIDADE_CONTRADITORIA,)


def test_source_id_payload_conflict_at_same_time_is_a_barrier():
    points=(reading(0,13),reading(3600,13,identificador_externo='same'),
            reading(3600,15,identificador_externo='same'),reading(7200,13))
    result=estimar_etileno(request(leituras=points))
    assert result.status_calculo == StatusCalculo.SEM_ESTIMATIVA
    assert result.motivos == (Motivo.CONFLITO_OBSERVACAO,)


def test_distinct_ids_with_equal_normalized_temperature_are_one_point():
    points=(reading(0,13,identificador_externo='a'),reading(0,'55.4',unidade='F',identificador_externo='b'),reading(3600,13))
    result=estimar_etileno(request(leituras=points,end=3600))
    assert result.volume_janela_min_ul == 200
    assert len(result.observacoes) == 2
    assert len(result.observacoes[0].originais) == 2


def test_invalid_and_valid_same_timestamp_are_conflicting():
    result=estimar_etileno(request(leituras=(reading(0,13),reading(0,None),reading(3600,13)),end=3600))
    assert result.intervalos[0].motivos[0] == Motivo.CONFLITO_OBSERVACAO
    assert result.volume_coberto_min_ul is None


def test_multiple_exclusion_causes_do_not_double_count_time():
    result=estimar_etileno(request(((0,25),(7200,25)),7200))
    assert result.intervalos[0].motivos == (Motivo.FORA_DO_DOMINIO,Motivo.LACUNA_EXCESSIVA)
    assert result.duracao_nao_coberta_s == 7200
    assert_partition(result)


def test_sensor_session_and_window_are_selected_before_integration():
    points=(reading(-1,25),reading(0,13),reading(1800,25,sensor_id='other'),
            reading(1800,25,sessao_id='other'),reading(3600,13),reading(3601,25))
    result=estimar_etileno(request(leituras=points,end=3600))
    assert result.volume_janela_min_ul == 200
    assert len(result.observacoes) == 2


def test_timezone_offsets_represent_elapsed_absolute_time():
    local=timezone(timedelta(hours=-3))
    points=(replace(reading(0,13),medida_em=START.astimezone(local)),reading(3600,13))
    result=estimar_etileno(request(leituras=points,end=3600))
    assert result.duracao_coberta_s == 3600
    assert result.volume_janela_min_ul == 200
    assert result.observacoes[0].originais[0].medida_em.utcoffset() == timedelta(hours=-3)


def test_fractional_seconds_are_not_truncated():
    result=estimar_etileno(request(((0,13),(0.5,13)),0.5))
    assert result.duracao_coberta_s == D('0.5')
    assert result.volume_janela_min_ul == D('0.027778')
    assert result.volume_janela_max_ul == D('0.138889')


def test_only_final_sum_is_rounded():
    result=estimar_etileno(request(tuple((i,13) for i in range(11)),10,massa='0.001',intervalo_maximo_s=1))
    assert result.volume_janela_min_ul == D('0.000001')
    assert result.volume_janela_max_ul == D('0.000003')
    assert all(i.volume_min_ul > 0 for i in result.intervalos)


def test_positive_below_display_resolution_is_explicit():
    result=estimar_etileno(request(((0,13),(1,13)),1,massa='0.0000001'))
    assert result.status_calculo == StatusCalculo.COMPLETO_NO_MODELO
    assert result.volume_janela_min_ul == 0
    assert Motivo.RESOLUCAO_APRESENTACAO in result.motivos
    assert result.intervalos[0].volume_min_ul > 0


def test_global_decimal_context_does_not_change_results():
    args=request(((0,12),(3600,12)),3600,modo=ModoCalculo.MODO_EXPLORATORIO)
    baseline=estimar_etileno(args)
    with localcontext() as ctx:
        ctx.prec=6
        ctx.rounding='ROUND_DOWN'
        actual=estimar_etileno(args)
    assert actual == baseline


def test_inputs_results_and_reference_parameters_are_immutable():
    original=[reading(0,13),reading(3600,13)]
    args=request(end=3600,leituras=original)
    original.clear()
    result=estimar_etileno(args)
    assert result.volume_janela_min_ul == 200
    with pytest.raises(FrozenInstanceError):
        result.massa_kg=D(1)
    with pytest.raises(FrozenInstanceError):
        result.tabela_referencia[0].temperatura_c=D(99)
    assert result.entrada == args
    assert result.fonte.endswith('/produce-facts-sheets/mango')
    assert result.unidade_volume == 'µL'
    assert result.versao_modelo == 'chicosense-etileno-1.0.0'


def test_import_is_independent_of_framework_database_and_network():
    root=str(Path(__file__).resolve().parents[1])
    script=(f'import sys; sys.path.insert(0,{root!r}); '
            'from app.modules.monitoramento.etileno import estimar_etileno; '
            'assert not any(x in sys.modules for x in '
            '("fastapi","sqlalchemy","httpx","app.core.config","app.core.database"))')
    completed=subprocess.run([sys.executable,'-B','-I','-c',script],cwd=root,capture_output=True,text=True)
    assert completed.returncode == 0, completed.stderr
