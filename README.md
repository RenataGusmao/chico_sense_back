# ChicoSense API

Backend do projeto acadêmico ChicoSense, uma plataforma de monitoramento inteligente para a cadeia logística de uvas e mangas do Vale do São Francisco.

Esta base integra autenticacao, usuarios, empresas, logistica operacional e a
integracao ThingSpeak existente. Autorizacao das rotas logisticas permanece
pendente; monitoramento, alertas e IA nao fazem parte desta integracao.

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

As entidades existentes sao reutilizadas pela camada operacional.

## Logistica operacional

Autenticacao e logistica coexistem nesta branch. Endpoints operacionais ainda
nao possuem autorizacao. A integracao de get_current_user, perfis e escopo de
empresa permanece pendente; nao publique estes endpoints para uso externo
antes dessa protecao.

Arquitetura: Route -> Service -> Repository -> Model -> Database.
Os repositories de logistica ficam juntos em app/repositories/logistica.py;
um helper compartilha somente busca, filtros, paginacao e persistencia.
Cada entidade possui service e schemas especificos, com regras no service.

Modelagem:
- Produto: nome persistido, descricao e ativo. Nao ha enum ou seed de frutas.
- ParametroProduto: nome_parametro, unidade, valor_minimo/valor_maximo e
  observacao. Limites sao opcionais, sem valores cientificos padrao.
  Quando ambos informados, minimo deve ser menor ou igual ao maximo.
  Esses parametros sao referencias do produto, nao regras por sensor.
- Veiculo: empresa_id, identificador, placa, modelo, descricao e ativo.
- Motorista: empresa_id, nome, documento opcional, telefone e ativo.
- Viagem: transportadora_id e vinculos obrigatorios com veiculo/motorista.
  saida_em representa inicio previsto; previsao_chegada_em e chegada_em
  representam fim previsto/real. inicio_real registra o inicio efetivo.
  Observacoes sao opcionais. Datas de entrada exigem timezone.
- Carga: viagem_id, produto_id, produtor_id e cliente_id opcional.
  Mantem identificacao e quantidade_caixas existentes; acrescenta quantidade,
  unidade, origem_produto e observacoes. Quantidade e unidade sao fornecidas juntas.
- Caixa: carga_id, identificacao, codigo_externo, peso opcional e observacoes.

Empresas de veiculos/motoristas/viagens devem ser transportadoras.
Veiculo e motorista da viagem devem pertencer a mesma transportadora.
Produtor/cliente da carga devem ter os tipos correspondentes.
Novos registros exigem empresas ativas; viagens iniciadas exigem veiculo
e motorista ativos. Produtos inativos nao recebem novas cargas.

Nao ha DELETE fisico nem alteracao dos pais de cargas/caixas/parametros.
Veiculos e motoristas nao mudam de empresa por PATCH. Veiculo e motorista
da viagem podem mudar apenas enquanto ela esta planejada.
Unicidade: veiculo por empresa+identificador; carga por viagem+identificacao;
caixa por carga+identificacao; parametro por produto+nome_parametro.
Restricoes existentes de nome de produto, placa e documento sao preservadas.
Duplicidades devolvem HTTP 409; referencias inexistentes, 404; regras invalidas, 422.

### Endpoints

```text
POST/GET  /api/v1/produtos
GET/PATCH /api/v1/produtos/{produto_id}
POST/GET  /api/v1/produtos/{produto_id}/parametros
PATCH     /api/v1/produtos/{produto_id}/parametros/{parametro_id}
POST/GET  /api/v1/veiculos
GET/PATCH /api/v1/veiculos/{veiculo_id}
POST/GET  /api/v1/motoristas
GET/PATCH /api/v1/motoristas/{motorista_id}
POST/GET  /api/v1/viagens
GET/PATCH /api/v1/viagens/{viagem_id}
POST/GET  /api/v1/viagens/{viagem_id}/cargas
GET/PATCH /api/v1/cargas/{carga_id}
POST/GET  /api/v1/cargas/{carga_id}/caixas
GET/PATCH /api/v1/caixas/{caixa_id}
```

Todas as listagens aceitam limit (1 a 100, padrao 50) e offset (>=0).
Produtos filtram por ativo; veiculos e motoristas por empresa_id e ativo.
Viagens filtram por empresa_id (transportadora), status, veiculo_id e
motorista_id. Cargas da viagem filtram por produto_id e status.
PATCH usa somente os campos fornecidos; null e aceito apenas nos campos
opcionais. Campos desconhecidos e tentativas de alterar pais sao rejeitados.

### Status

- Viagem: PLANEJADA -> EM_ANDAMENTO -> CONCLUIDA;
  PLANEJADA -> CANCELADA.
- Carga: PLANEJADA -> EM_TRANSITO -> ENTREGUE;
  PLANEJADA -> CANCELADA.
- Caixa: REGISTRADA -> EM_TRANSITO -> ENTREGUE;
  REGISTRADA ou EM_TRANSITO -> AVARIADA.

O status e alterado no PATCH da entidade. Repetir o mesmo status e permitido.
Iniciar/concluir viagem preenche inicio_real/chegada_em com UTC se nao
foram informados. Chegada nao pode anteceder inicio real.
Registros legados sem inicio_real podem receber observacoes; ao concluir
uma viagem legada em andamento, informe seu inicio_real efetivo.
Carga entra em transito somente com viagem em andamento; caixa entra em
transito somente com carga em transito. Nao ha propagacao automatica de
status para filhos: aplique transicoes explicitamente. Entrega exige o pai
em transito/andamento ou entregue/concluido. Registros encerrados preservam
sua estrutura, permitindo observacoes. Nao e permitido reabrir registros.

### Fluxo

Cadastre empresas pelos mecanismos existentes. Cadastre um produto e,
opcionalmente, referencias fornecidas por uma fonte validada. Crie veiculo
e motorista da transportadora, depois viagem planejada com seus UUIDs.
Crie carga com produto/produtor e caixas dentro da carga. Inicie viagem,
coloque carga e caixas em transito e registre entrega/conclusao.

Empresa -> Veiculo/Motorista -> Viagem -> Carga -> Produto
e Carga -> Caixa -> Sensor/Medicao.

ThingSpeak, setup_prototipo e Medicao nao foram alterados.
Medicao.viagem_id/carga_id/caixa_id continuam opcionais para PROTOTIPO.

### Migration e validacao

Migration logistica: 20261007_0005_logistica, baseada em 20261005_0004_auth_email.
Acrescenta apenas campos operacionais e unicidade por escopo; nao remove
dados nem cria seed. Registros antigos recebem ativo=true para veiculos
e motoristas; demais campos adicionados sao opcionais.
Duplicidades preexistentes impedem a aplicacao das restricoes e exigem
revisao manual. Migrations 0001/0002/0003 permanecem intactas.
A migration auth ja aplicada foi preservada integralmente. Somente a
migration logistica, ainda nao aplicada no Supabase, foi sequenciada como
0005. Sua logica de upgrade/downgrade permanece identica. Ha um unico head:

```text
20260930_0001 -> 20261002_0002 -> 20261002_0003
             -> 20261005_0004_auth_email -> 20261007_0005_logistica
```

```powershell
python -m pip install -r requirements.txt
python -m pytest tests
alembic heads
alembic history
git diff --check
```

Nesta etapa de integracao, valide somente codigo, testes e grafo.
Nao aplique migrations no Supabase nem execute setup_admin ou seeds.
A aplicacao da migration 0005 fica para uma etapa posterior a revisao.
Para iniciar a API localmente:

```powershell
python -m uvicorn app.main:app --reload
```

Os testes operacionais usam SQLite em memoria com foreign keys habilitadas
e substituem a sessao da API. Nao acessam ThingSpeak ou Supabase.
As migrations devem ser validadas em PostgreSQL de desenvolvimento.
