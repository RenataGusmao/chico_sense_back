# ChicoSense API

Backend do projeto acadêmico ChicoSense, uma plataforma de monitoramento inteligente para a cadeia logística de uvas e mangas do Vale do São Francisco.

Esta etapa contém somente a fundação arquitetural da API. Funcionalidades de negócio, modelos das entidades, autenticação completa, alertas, IoT e IA serão adicionados posteriormente.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy 2
- PostgreSQL
- Pydantic Settings
- Alembic
- Pytest

## Configuração

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo de ambiente local:

```bash
copy .env.example .env
```

Depois, ajuste o `DATABASE_URL` e o `SECRET_KEY` no `.env` com valores locais.

## Executando a API

```bash
uvicorn app.main:app --reload
```

Endpoints iniciais:

- `GET /`
- `GET /health`
- `GET /docs`

## Integração ThingSpeak

A integração com ThingSpeak usa a REST API para consultar feeds de um canal, normalizar os campos `fieldN` e converter cada leitura para uma estrutura interna do ChicoSense.

Configure no `.env`:

```bash
THINGSPEAK_BASE_URL=https://api.thingspeak.com
THINGSPEAK_CHANNEL_ID=
THINGSPEAK_READ_API_KEY=
THINGSPEAK_TIMEOUT_SECONDS=10
THINGSPEAK_FIELD_MAPPING_JSON={}
```

`THINGSPEAK_READ_API_KEY` deve ser preenchida somente para canais privados. A chave nunca é retornada pelos endpoints.

O mapeamento de fields é configurável. O código não assume que `field1` seja temperatura ou que `field2` seja umidade. Exemplo estrutural:

```json
{
  "field1": {
    "sensor_id": "00000000-0000-0000-0000-000000000000",
    "tipo": "TEMPERATURA",
    "contexto": "AMBIENTE",
    "unidade": "C"
  }
}
```

Endpoints de validação:

- `GET /api/v1/integracoes/thingspeak/status`
- `GET /api/v1/integracoes/thingspeak/feeds`
- `GET /api/v1/integracoes/thingspeak/ultima-leitura`
- `POST /api/v1/integracoes/thingspeak/sincronizar`

Os endpoints de feeds consultam o ThingSpeak quando `THINGSPEAK_CHANNEL_ID` está configurado.

### Sincronização manual

O endpoint `POST /api/v1/integracoes/thingspeak/sincronizar` busca feeds do ThingSpeak, aplica o mapeamento configurável, valida cada leitura e cria registros em `medicoes`.

Cada medição importada recebe um registro correspondente em `leituras_externas`, que preserva:

- origem;
- channel_id;
- entry_id;
- field_name;
- medicao_id.

A tabela `leituras_externas` possui uma constraint única para `origem + channel_id + entry_id + field_name`, impedindo que a mesma leitura externa gere medições duplicadas.

Exemplo:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/integracoes/thingspeak/sincronizar?results=100"
```

Resposta esperada:

```json
{
  "feeds_recebidos": 10,
  "fields_processados": 30,
  "medicoes_criadas": 26,
  "duplicados": 2,
  "ignorados": 2,
  "erros": []
}
```

Para persistir uma medição, o field configurado precisa informar `sensor_id`, `contexto` e `unidade`. O `sensor_id` deve existir no banco. O vínculo com `viagem_id` e `carga_id` pode vir do próprio mapeamento ou do dispositivo associado ao sensor. Sensores inexistentes, valores nulos, strings vazias e valores não numéricos são ignorados sem cancelar o lote inteiro.

### Protótipo ThingSpeak real

O protótipo atual usa o canal ThingSpeak `3493148` com:

- `field1`: Temperatura Atual;
- `field2`: Umidade;
- `field3`: Temperatura Máxima;
- `field4`: Temperatura Mínima;
- `field5`: Temperatura Média.

Nesta fase, somente `field1` e `field2` entram em `medicoes`, porque representam leituras diretas dos sensores internos do protótipo. `field3`, `field4` e `field5` são estatísticas derivadas do canal e ficam fora da persistência de medições.

O protótipo representa leitura de sala/laboratório, não uma viagem real. Por isso usa o contexto `PROTOTIPO` e não cria vínculos com viagem, carga, caixa, produtor ou transportadora.

Antes de sincronizar, aplique as migrations e execute o setup idempotente:

```bash
alembic upgrade head
python scripts/setup_prototipo.py
```

O script cria ou reutiliza:

- dispositivo `sensor-prototipo-sala`;
- sensor de temperatura do protótipo;
- sensor de umidade do protótipo.

Ao final, ele imprime o JSON pronto para `THINGSPEAK_FIELD_MAPPING_JSON`. Depois configure manualmente no `.env`:

```bash
THINGSPEAK_CHANNEL_ID=3493148
THINGSPEAK_READ_API_KEY=<chave real>
THINGSPEAK_FIELD_MAPPING_JSON=<json gerado pelo script>
```

Validação manual:

```bash
uvicorn app.main:app --reload
curl http://127.0.0.1:8000/api/v1/integracoes/thingspeak/status
curl http://127.0.0.1:8000/api/v1/integracoes/thingspeak/ultima-leitura
curl http://127.0.0.1:8000/api/v1/integracoes/thingspeak/feeds
curl -X POST "http://127.0.0.1:8000/api/v1/integracoes/thingspeak/sincronizar?results=10"
```

## Testes

```bash
pytest
```

## Alembic

O Alembic está preparado para usar a `Base` declarativa de `app.core.database`.

Quando houver modelos de banco em etapas futuras:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
alembic upgrade head
```

Nenhuma tabela de negócio foi criada nesta etapa.
