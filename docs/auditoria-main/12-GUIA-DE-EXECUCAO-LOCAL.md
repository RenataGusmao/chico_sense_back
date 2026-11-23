# Guia de execução local

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Pré-requisitos e limites

Windows x64 foi o ambiente observado; Python 3.13.7 com venv e pins de requirements.txt. PostgreSQL é o banco de produção previsto. SQLite é usado por fixtures de testes, não substituto homologado de migrations PostgreSQL. Não executar `alembic upgrade head` contra o `.env` de origem. Leia `tests/POSTGRESQL.md` antes de disponibilizar banco descartável. Não utilizar Supabase para testes.

### Dependências

Na raiz de uma cópia local de desenvolvimento, criar venv com `python -m venv .venv` e instalar `python -m pip install -r requirements.txt`. Estes comandos são instruções de reprodução, não instalações feitas pela auditoria. Não há runtime global novo necessário para os testes locais já executados. APIs exigem SECRET_KEY não placeholder com pelo menos 32 bytes. Não colocar a chave no Git nem nos exemplos de login.

## Configuração

| Variável | Função / padrão de código | Cuidado |
|---|---|---|
| APP_NAME | chicosense-api | Nome no health/OpenAPI |
| APP_ENV | development | Não implementa isolamento sozinho |
| DEBUG | false | Não expor debug em homologação |
| DATABASE_URL | DSN SQLAlchemy configurável | Confirmar host/porta/DB/proprietário; jamais copiar destino privado para testes |
| SECRET_KEY | placeholder bloqueado pela autenticação | Gerar segredo próprio fora do repositório; mínimo32 bytes |
| ACCESS_TOKEN_EXPIRE_MINUTES |30, positivo| expires_in da resposta é em segundos |
| THINGSPEAK_BASE_URL | https://api.thingspeak.com | Cliente valida URL; sem userinfo/query/fragment |
| THINGSPEAK_CHANNEL_ID | ausente | Canal numérico configurado no servidor |
| THINGSPEAK_READ_API_KEY | ausente | Somente servidor, não frontend/log |
| THINGSPEAK_TIMEOUT_SECONDS |10| Timeout HTTP |
| THINGSPEAK_FIELD_MAPPING_JSON |{}| Campos→sensores/contexto/unidades; não concede ownership |

`Settings` lê `.env` automaticamente: sobrescrever somente DATABASE_URL não impede leitura das demais configurações. Prepare uma cópia isolada ou forneça todas as configurações necessárias no processo; nunca reutilize credenciais privadas na demonstração. Não imprima o resultado de Settings nem DSN completo.

## Execução de testes segura

Os testes usam fixtures/overrides; este roteiro garante destino inofensivo no processo. Execute os comandos em um shell dedicado, descartável, para não alterar a configuração de outros trabalhos:

```powershell
$env:DATABASE_URL = 'sqlite+pysqlite:///:memory:'
$env:SECRET_KEY = 'fixture-local-exclusiva-nao-usar-em-producao-2026'
$env:THINGSPEAK_CHANNEL_ID = ''
$env:THINGSPEAK_READ_API_KEY = ''
$env:THINGSPEAK_FIELD_MAPPING_JSON = '{}'
python -B -m pytest tests -q -rs -p no:cacheprovider
```

Não exporte opt-ins PostgreSQL sem ambiente aprovado/identificado. Ausência completa gera12 skips; configuração parcial falha. Nenhum dos comandos acima inicializa schema no banco da aplicação. Guardas não autorizam reaproveitar DB existente.

## API manual e Swagger

Para uso manual, **não use SQLite em memória como servidor da aplicação**: o processo não cria tabelas e migrations usam PostgreSQL. Disponibilize cluster local novo com loopback, porta e credenciais dedicadas. Confirme separadamente identidade do cluster/diretório, DB e proprietário antes de DDL. O procedimento do repositório cria banco inicialmente vazio e o harness de teste controla migrations; não execute simultaneamente a API manual contra o mesmo banco da suíte. Prepare outro banco local descartável para demonstração, com autorização e seed explícitos.

Depois de confirmar destino isolado e aplicar a cadeia de migrations nesse banco de demonstração, `python scripts/setup_admin.py --nome "Admin local" --email "admin@example.com"` solicita senha sem echo e cria/reutiliza ADMIN/perfis. O script usa SessionLocal configurada; não executá-lo antes de confirmar o destino. Não promove usuário existente de outro perfil. Sensores/logística para transporte exigem seed próprio, pois não há CRUD de sensor. `setup_prototipo.py` é apenas protótipo e não atende por si só o fluxo refrigerado.

Com banco/seed próprios verificados:

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Acessar http://127.0.0.1:8000/docs, /redoc, /openapi.json e /health. Não foi iniciado servidor persistente nesta auditoria; documentação foi validada com TestClient. Follow o guia Swagger para as operações. API local não prova DB local.

## PostgreSQL real opcional

Seguir integralmente [tests/POSTGRESQL.md](../../tests/POSTGRESQL.md) e [scripts/pg_test_safety.py](../../scripts/pg_test_safety.py). Exige CHICOSENSE_TEST_DATABASE_URL, CHICOSENSE_TEST_DISPOSABLE_TOKEN e CHICOSENSE_TEST_SYSTEM_IDENTIFIER, só no processo. Driver postgresql+psycopg, loopback literal, porta explícita≥1024, usuário dedicado e banco com token; marcador/proprietário/identidade/schema vazio e advisory lock conferidos antes de escrever. Não há fallback para DATABASE_URL. Não usar pytest-xdist. Novo banco por rodada, preservar logs e parar servidor controladamente. Nenhuma credencial/cluster desta auditoria foi criado.

## Problemas comuns

| Sintoma | Verificação |
|---|---|
|503 no login| Chave placeholder/curta; não desligar autenticação |
|401| Token ausente/expirado, assinatura/claims inválidos ou usuário inativo |
|403| Perfil/vínculo/empresa; ThingSpeak global só ADMIN |
|422 ao criar sessão| Fuso, massa, sensor/protótipo/unidade; ver schema e motivo |
|409 ao iniciar| Sessão/fonte em uso, estado logístico ou chave divergente |
|200 sincronização com FALHA| Conferir estado/resumo/ocorrências, mapping e provedor; HTTP não garante coleta |
|SEM_ESTIMATIVA ou PARCIAL| Dados/gaps/domínio; null não é zero e subtotal não é total |
|CONFIGURACAO_INSUFICIENTE| Configuração precisa existir no corte e corresponder a ambiente/maturação |
|Veículo ocupado| Consultar execução anterior e realizar parada humana autorizada |
|Erro de tabela não existe| Banco/seed/migrations não preparados; não apontar para produção como solução |
|12 skips PostgreSQL| Opt-ins ausentes; pendência, não aprovação |
|Falha de guardas PostgreSQL| Parar procedimento afetado; não contornar identidade/schema vazio |
|Bloqueio CORS| Origem atual só5173; configuração futura requer revisão, sem enfraquecer JWT |
