from sqlalchemy import inspect

import app.models
from app.core.database import Base
from app.models.iot import Medicao, Sensor
from app.models.logistica import Carga, Viagem
from app.models.usuario import Usuario


def test_models_are_importable() -> None:
    assert app.models.Usuario is Usuario
    assert app.models.Viagem is Viagem
    assert app.models.Medicao is Medicao


def test_main_tables_exist_in_metadata() -> None:
    expected_tables = {
        "perfis",
        "usuarios",
        "empresas",
        "empresas_usuarios",
        "produtos",
        "parametros_produto",
        "veiculos",
        "motoristas",
        "viagens",
        "cargas",
        "caixas",
        "dispositivos",
        "sensores",
        "medicoes",
        "alertas",
        "ocorrencias",
        "recomendacoes_ia",
        "dados_externos",
        "leituras_externas",
    }

    assert expected_tables.issubset(set(Base.metadata.tables.keys()))


def test_medicoes_indexes_are_declared() -> None:
    index_names = {index.name for index in Base.metadata.tables["medicoes"].indexes}

    assert "ix_medicoes_medida_em" in index_names
    assert "ix_medicoes_sensor_id" in index_names
    assert "ix_medicoes_viagem_id" in index_names
    assert "ix_medicoes_carga_id" in index_names
    assert "ix_medicoes_caixa_id" in index_names
    assert "ix_medicoes_sensor_medida_em" in index_names


def test_core_relationships_are_mapped() -> None:
    viagem_relationships = inspect(Viagem).relationships
    carga_relationships = inspect(Carga).relationships
    sensor_relationships = inspect(Sensor).relationships
    medicao_relationships = inspect(Medicao).relationships

    assert "cargas" in viagem_relationships
    assert "caixas" in carga_relationships
    assert "medicoes" in sensor_relationships
    assert "sensor" in medicao_relationships
    assert "viagem" in medicao_relationships
    assert "carga" in medicao_relationships
    assert "caixa" in medicao_relationships
