# ChicoSense — Monitoramento Preventivo de Etileno da Manga Tommy Atkins

Backend acadêmico para acompanhar cargas refrigeradas, registrar temperatura e
umidade e apoiar decisões humanas durante o transporte da manga Tommy Atkins.
O sistema estima **produção potencial de etileno** a partir de referências gerais
de manga. Não mede etileno diretamente, não estima concentração real de gás e
não comprova experimentalmente eficácia de exaustão ou conservação da fruta.

## Problema, objetivo e escopo

Temperatura, tempo de exposição, lacunas de aquisição e condições da carga precisam
ser rastreáveis durante o transporte. O ChicoSense reúne logística, histórico IoT,
estimativas reproduzíveis, avaliação ambiental e auditoria das decisões.

A cultivar é declarada explicitamente como MANGA_TOMMY_ATKINS. Essa declaração não
certifica identidade botânica e as taxas bibliográficas não são calibração da
cultivar. O catálogo logístico continua genérico; os cálculos novos usam o perfil
específico declarado para a carga, sem inventar massa/maturação para dados legados.

## Arquitetura e tecnologias

Python, FastAPI 0.115, Pydantic 2, SQLAlchemy 2, PostgreSQL, psycopg 3, Alembic,
PyJWT, pwdlib/Argon2, HTTPX e pytest. Versões reproduzíveis em [requirements.txt](requirements.txt).

```text
Rotas HTTP → serviços de aplicação/autorização → repositories → SQLAlchemy/PostgreSQL
                  ↓
         motor científico puro (Decimal)
                  ↓
         snapshots, hashes e auditoria
```

- app/modules/auth, empresas, produtos e logistica: identidade, escopo e operações.
- app/modules/integracoes/thingspeak: cliente/mapper e integração externa.
- app/modules/monitoramento: sessões, histórico, análises, condições e intervenção.
- app/modules/monitoramento/etileno: cálculo puro, sem banco, HTTP ou relógio global.
- app/models, app/repositories, alembic e tests: persistência, evolução e validação.

## Autenticação e permissões

POST /api/v1/auth/login recebe email/senha em JSON e retorna access_token,
token_type=bearer e expires_in. GET /api/v1/auth/me informa perfil e vínculos.
Nas operações privadas: Authorization: Bearer <token-retornado-pelo-login>.
Não há cadastro público, refresh ou logout implementados.

| Operação | ADMIN | GESTOR | OPERADOR | CONSULTA |
|---|---|---|---|---|
| Ler catálogo de produtos/parâmetros | Sim | Sim | Sim | Sim |
| Alterar catálogo global | Sim | Não | Não | Não |
| Ler logística/monitoramento | Todos os escopos | Próprio escopo | Próprio escopo | Próprio escopo |
| Escrever veículos/motoristas | Sim | Próprio escopo | Não | Não |
| Escrever viagens/cargas/caixas e sessões | Sim | Próprio escopo | Próprio escopo | Não |
| Sincronizar sessão ativa e analisar/avaliar | Sim | Próprio escopo | Próprio escopo | Não |
| Configurar ambiente/complementar sessão encerrada | Sim | Próprio escopo, com requisitos explícitos | Não | Não |
| Consultar/sincronizar canal global ThingSpeak | Sim | Não | Não | Não |
| Autorizar/recusar/iniciar intervenção virtual | Sim | Próprio escopo | Não | Não |

OPERADOR pode solicitar intervenção e encerrar a própria; cancelamento próprio é
permitido enquanto SOLICITADA. Ações administrativas adicionais e estados estão
nos [contratos](docs/chicosense/contratos-api.md). Usuário ativo, perfil e vínculo
empresarial são verificados no backend. IDs enviados pelo cliente não concedem
acesso. Listagens são filtradas em SQL antes da paginação. Empresa inativa bloqueia
escrita; ADMIN possui a recuperação administrativa documentada de intervenção.

JWT ausente/inválido/expirado: 401; perfil/vínculo insuficiente: 403; recurso
inexistente: 404; conflito de estado/idempotência: 409; entrada inválida: 422.
A política existente usa 403 genérico para fora de escopo, sem retornar o recurso.
Não há DELETE físico dos registros logísticos ou históricos.

## Logística, cargas e sessões

Cadastre empresas, produto, veículo/motorista da transportadora e viagem. Crie a
carga vinculada à viagem/produto/produtor. Viagem deve estar EM_ANDAMENTO e carga
EM_TRANSITO para abrir sessão de transporte. As transições são explícitas; não há
propagação automática de status aos filhos.

O perfil adicional declara massa líquida kg, cultivar, lote e maturação; não converte
quantidade de caixas em massa. A sessão congela perfil e origem dos sensores,
registrando início efetivo, fim, autor e motivo. ATIVA → ENCERRADA ou CANCELADA;
terminais não reabrem. Carga/sensores não participam de sessões ativas conflitantes.
Sensores/dispositivos precisam existir e ter tipo, unidade e vínculo compatíveis;
não há CRUD HTTP de sensores nesta versão. [Detalhes das sessões](app/modules/monitoramento/README.md).

## ThingSpeak e histórico ambiental

O cliente consulta campos fieldN conforme mapeamento explícito de sensor, tipo,
contexto e unidade; não presume que field1 seja temperatura. Chaves privadas ficam
no servidor e são removidas de respostas/logs. As quatro rotas globais ThingSpeak
são exclusivas de ADMIN, pois o canal global não tem propriedade empresarial
persistida. Elas não substituem o fluxo empresarial por sessão.

A aquisição por sessão é explícita, versionada e idempotente. Conserva horários de
medição/recebimento/processamento, origem, revisões, leituras inválidas e conflitos.
Deduplica por origem/canal/entry/campo. Leituras fora de ordem são ordenadas sem
alterar os registros originais. Complemento de sessão encerrada exige GESTOR/ADMIN,
flag e justificativa. Sessão cancelada não recebe nova aquisição.
[Política do histórico](app/modules/monitoramento/HISTORICO_IOT.md).

## Modelo matemático e limitações científicas

```text
V_min/max = Σ [q_min/max(T_i) × massa_kg × duração_h]
```

q é expresso em µL/(kg·h), duração em horas e volume potencial em µL. As referências
gerais UC Davis para manga são 10, 13, 15 e 20 °C. [Fundamentação e exemplos](docs/chicosense/modelo-cientifico.md).

- MODO_RESTRITO: usa somente temperaturas coincidentes com os quatro pontos.
- MODO_EXPLORATORIO: interpolação linear de taxas entre pontos, de 10 a 20 °C.
- Não há extrapolação, arredondamento para pontos nem fator por maturação.
- Cada intervalo exige dois extremos utilizáveis e duração até G explicitamente
  informado; usa a temperatura inicial. Não há extensão de bordas ou imputação.
- Lacunas, conflitos e temperatura fora do domínio impedem contribuição; ausência
  de dados nunca se transforma em produção zero. Subtotal parcial não é total da janela.
- Maturação desconhecida/mista não é corrigida. Atmosfera, ventilação, absorção,
  volume do compartimento e temperatura da polpa não são modelados.

Essas taxas não foram experimentalmente validadas para Tommy Atkins. Volume potencial
não é concentração em ppm, dano, amadurecimento ou eficácia de ventilação. O risco de
etileno é **NAO_AVALIADO**, sem limiar arbitrário baixo/médio/alto.
[Contrato do motor](app/modules/monitoramento/etileno/README.md).

As análises persistem parâmetros, revisão/corte de aquisição, snapshots, hashes e
versão do modelo. Consultar uma análise não recalcula nem incorpora leituras novas.

## Avaliação ambiental e decisões humanas

Configurações versionadas fornecem faixas ambientais, duração e requisitos de
cobertura com justificativa OPERACIONAL/EXPERIMENTAL. A avaliação ambiental é
separada do volume potencial de etileno. Dados insuficientes produzem resultado
inconclusivo, sem inferir segurança. Alertas têm evidências e trilha de decisões
CRIAR/RECONHECER/RESOLVER/DESCARTAR/OBSERVAR; não se resolvem automaticamente.

## Exaustor exclusivamente virtual

SOLICITADA → AUTORIZADA/RECUSADA; início e finalização exigem ações humanas
permitidas. Um veículo admite no máximo uma execução virtual ativa, inclusive
entre sessões distintas. Histórico registra justificativa, usuário e duração.
Não há comando a equipamento, scheduler de desligamento ou alteração dos resultados
científicos. Uma simulação concluída não comprova remoção de gás ou benefício à fruta.

## Principais endpoints

Prefixo funcional: /api/v1. API informa versão 0.1.0; as etapas não criaram outro prefixo.

| Finalidade | Método e caminho |
|---|---|
| Login / identidade | POST /api/v1/auth/login; GET /api/v1/auth/me |
| Produtos | GET/POST /api/v1/produtos |
| Viagens / cargas | GET/POST /api/v1/viagens; GET/POST /api/v1/viagens/{viagem_id}/cargas |
| Consultar carga / viagem | GET /api/v1/cargas/{carga_id}; GET /api/v1/viagens/{viagem_id} |
| Perfil da carga | PUT/GET /api/v1/cargas/{carga_id}/monitoramento |
| Abrir sessão | POST /api/v1/cargas/{carga_id}/monitoramentos |
| Encerrar/cancelar | POST /api/v1/monitoramentos/{sessao_id}/encerrar ou /cancelar |
| Aquisição / histórico | POST /api/v1/monitoramentos/{sessao_id}/sincronizacoes; GET /leituras e /qualidade no mesmo prefixo de sessão |
| Análises | POST/GET /api/v1/monitoramentos/{sessao_id}/analises-etileno |
| Configuração ambiental | POST/GET /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais |
| Avaliação / alertas | POST/GET /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas; GET /alertas no mesmo prefixo |
| Decisão | POST /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes |
| Intervenção | POST/GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas |
| Ação da intervenção | POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes |

Inventário completo (76 operações/84 schemas), parâmetros e exemplos:
[Contratos do frontend](docs/chicosense/contratos-api.md),
[OpenAPI](docs/chicosense/openapi.json), [entradas hipotéticas](docs/chicosense/exemplos-frontend.json).
Raiz, /health e login são públicos. /docs, /redoc e /openapi.json também são públicos.

## Configuração e execução local

Na raiz do repositório, Windows/PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# Em ambiente novo, crie .env a partir de .env.example, sem sobrescrever outro .env.
# Defina DATABASE_URL local e SECRET_KEY próprio com pelo menos 32 caracteres.
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Revise o destino efetivo antes de iniciar: servidor HTTP local não garante banco
local. Não use credenciais de produção para demonstração. .env.example contém
somente placeholders; substitua SECRET_KEY inseguro antes de usar autenticação.
Não versionar .env, senha de setup, token JWT, chave de canal ou DSN real.

Variáveis: APP_NAME, APP_ENV, DEBUG, DATABASE_URL, SECRET_KEY,
ACCESS_TOKEN_EXPIRE_MINUTES e THINGSPEAK_BASE_URL/CHANNEL_ID/READ_API_KEY/
TIMEOUT_SECONDS/FIELD_MAPPING_JSON (estas últimas com o prefixo THINGSPEAK_).
Use DEBUG=false fora do desenvolvimento. READ_API_KEY é opcional para canal público;
mapeamento JSON deve referenciar sensores realmente provisionados.

Após preparar o banco local e aplicar migrations explicitamente autorizadas, crie
os perfis/primeiro ADMIN pelo script, com senha solicitada interativamente:

```powershell
python scripts/setup_admin.py --nome "Administrador local" --email "admin@example.com"
```

Não há seed automático ao iniciar a API. Não executar setup ou migrations contra
uma conexão remota por assumir que ela seja de teste.

## Migrations e testes

```powershell
python -m alembic heads
python -m alembic history
# Apenas em banco local novo/de desenvolvimento confirmado:
python -m alembic upgrade head
python -B -m pytest -q -rs -p no:cacheprovider
```

Head única: **20261028_0010_exaustao_virtual**, encadeada à base 20260930_0001.
Não alterar revisões históricas já aplicadas. Alembic autogenerate pode propor uma
recriação redundante do índice funcional de e-mail por trim/TRIM(BOTH FROM);
revise manualmente. O teste de catálogo confirma equivalência e unicidade sem
aplicar essa recriação. [Procedimento PostgreSQL seguro](tests/POSTGRESQL.md).

## Qualificação PostgreSQL real

PostgreSQL portátil 17.11: **757 aprovados, zero falhas/skips**, um warning conhecido;
12 casos reais, três repetições de nove testes concorrentes e 50 corridas na
qualificação final. Banco novo por rodada; conexões/PIDs independentes; catálogo,
upgrade/downgrade/upgrade, rollback, idempotência e auditoria verificados.
[Resumo reproduzível e limites](docs/chicosense/validacao.md).

Sem as três variáveis explícitas de teste PostgreSQL, a execução padrão resulta
em **745 aprovados +12 skips opcionais**. Isso não repete a qualificação real nem
é evidência nova de PostgreSQL. Não apontar essas variáveis ao banco da aplicação:
a trava exige loopback, marcador e identidade comprovada, além de schema vazio.
O warning conhecido é a depreciação BlockingPortal em Starlette/TestClient.

## Demonstração e integração futura

A [demonstração automatizada](docs/chicosense/demonstracao.md) usa JWT real, motor
real, SQLite descartável e HTTP ThingSpeak mockado; não requer sensores ou conta real.
O frontend deve tratar 401/403/404/409/422, mostrar cobertura/limitações e preservar
chaves de idempotência em retries. Acesso visual não substitui autorização no backend.
CORS de desenvolvimento permite localhost:5173 e 127.0.0.1:5173 (HTTP).

Não há frontend nesta entrega, dashboard agregador, refresh JWT, CRUD de sensores
ou identidade de máquina. Provisionamento de sensores/mapping, calibração, validade
específica para a cultivar, concentração real e atuação física são trabalhos futuros.
Nenhum resultado autoriza conservação garantida ou eficácia da exaustão. Publicação,
credenciais de ambiente, migrations remotas e envio Git dependem de autorização própria.
