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

As entidades de dominio existentes sao preservadas. A etapa de autenticacao
acrescenta o indice unico de identidade de email na migration
`20261005_0004_auth_email`, derivada de `20261002_0003`.

## Autenticacao, usuarios e empresas

Arquitetura: Route -> Service -> Repository -> Model -> Database.
Reutilizamos Usuario.senha_hash, Perfil, Empresa e EmpresaUsuario; nao ha
empresa unica obrigatoria no usuario. Perfis sao registros configuraveis.
O setup inicial cria ADMIN, GESTOR, OPERADOR e CONSULTA.

Senhas usam Argon2id via pwdlib, com minimo de 12 caracteres na criacao.
Hashes e senhas nunca compoem schemas de resposta. Erros de validacao omitem
os valores de entrada para evitar devolver senhas em respostas 422.
JWT usa HS256, subject UUID, issuer/audience chicosense-api e expiracao
controlada por ACCESS_TOKEN_EXPIRE_MINUTES (30 por padrao). Configure no
.env uma SECRET_KEY aleatoria com pelo menos 32 bytes; o placeholder nao
permite emitir ou validar tokens. Nao versione a chave.

Tokens nao sao persistidos e nao ha blacklist/logout no servidor.
Desativar o usuario bloqueia imediatamente novas requisicoes autenticadas.
Perfis e vinculos sao consultados no banco a cada requisicao; alterar senha
nao revoga tokens ja emitidos, que permanecem validos ate expirarem.

### Preparacao local

```powershell
python -m pip install -r requirements.txt
python -m pytest
alembic upgrade head
python scripts/setup_admin.py --nome "Administrador" --email "admin@exemplo.com"
python -m uvicorn app.main:app --reload
```

Execute migration e setup manualmente contra o banco desejado.
O setup solicita senha com getpass somente se precisar criar o administrador.
Executar novamente reutiliza usuario e perfis sem trocar senha. Um email
existente que nao seja de administrador ativo causa erro, sem promover o usuario.
O script nao recebe senha pela linha de comando nem imprime senha/hash.

A migration nao altera registros; emails ja existentes que sejam duplicados
ignorando caixa/espacos impedem a criacao do indice e exigem revisao manual.
Migrations 0001, 0002 e 0003 nao foram modificadas. Uma migration 0004 na
branch de monitoramento pode resultar em dois heads no merge futuro:
revisar ambas e criar uma migration de merge Alembic naquele momento,
sem reescrever migrations ja aplicadas.

### Endpoints

- POST /api/v1/auth/login: JSON com email e senha; devolve access_token,
  token_type e expires_in.
- GET /api/v1/auth/me: usuario atual, perfil e empresas ativas com vinculo ativo.
- GET /api/v1/perfis: perfis disponiveis (ADMIN).
- POST/GET /api/v1/usuarios e GET/PATCH /api/v1/usuarios/{usuario_id}: ADMIN.
- POST/PATCH /api/v1/empresas e /api/v1/empresas/{empresa_id}: ADMIN.
- GET /api/v1/empresas: todas para ADMIN; apenas vinculadas para demais usuarios.
- GET /api/v1/empresas/{empresa_id}: ADMIN ou usuario vinculado.
- POST /api/v1/empresas/{empresa_id}/usuarios/{usuario_id}: ADMIN; reutiliza vinculo.
- GET /api/v1/empresas/{empresa_id}/usuarios: ADMIN ou GESTOR vinculado.

POST de usuario recebe nome, email, senha, perfil_id e opcionalmente ativo.
PATCH aceita somente campos declarados e permite desativacao com ativo=false.
Empresa recebe nome, tipo (PRODUTOR/TRANSPORTADORA/CLIENTE), documento opcional
e ativo. Nao ha exclusao fisica. Listagens aceitam offset e limit (maximo 100).
OPERADOR e CONSULTA possuem acesso de leitura ao proprio contexto de empresa;
permissoes operacionais detalhadas ficam para etapas futuras.

Exemplo de corpo de login, com valores ilustrativos:

```json
{"email": "admin@exemplo.com", "senha": "<senha-definida-no-setup>"}
```

Nas chamadas protegidas, envie o header:

```text
Authorization: Bearer <access_token-retornado-pelo-login>
```

No /docs, use Authorize com o token retornado pelo login JSON.
Nao existe cadastro publico: o primeiro administrador vem do script.

### Testes de autenticacao

```powershell
python -m pytest tests/test_auth_usuarios_empresas.py -v
python -m pytest
```

Os novos testes usam SQLite em memoria, dependency override e JWT de teste.
Nao acessam Supabase ou ThingSpeak. A validacao da migration em PostgreSQL
deve ser realizada manualmente em ambiente de desenvolvimento antes do uso.
