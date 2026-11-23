# Índice geral — auditoria técnica ChicoSense

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Nota de publicação após a correção de CORS

Esta documentação preserva a auditoria do commit `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`; suas contagens, resultados e evidências são históricos desse código. A publicação documental parte da main `795f4b160325b863702e7ac793b381d777473d4a`, que já recebeu a correção de CORS pelo PR #4, commit `37887483cc7f12ce64e3974d31923978ec130f57`.

A pendência **P-11 foi corrigida no código**: `CORS_ALLOWED_ORIGINS` permite uma lista JSON de origens explícitas, somada às duas origens locais. Consulte o [README atual](../../README.md) e os [testes CORS](../../tests/test_cors.py). A configuração da variável no Render e a validação do login no navegador continuam sendo passos operacionais separados; esta publicação não os executa nem comprova sua realização.

A validação da correção registrou **765 aprovados, 12 skips PostgreSQL e um warning conhecido**, com 20 casos CORS acrescentados aos 757 casos anteriores (777 casos totais). Não se trata de reexecução da qualificação PostgreSQL. Não foram atualizados artificialmente os logs, hashes, schemas ou resultados originais da auditoria para fazê-los parecer uma nova execução. As referências a CORS limitado a localhost nos demais documentos descrevem o commit auditado, não a configuração atualizável da main após o PR #4.


## Uso da documentação

Comece pelo estado auditado e pelas pendências; use o guia local antes de fazer qualquer operação Swagger. O catálogo e o dicionário de dados são completos para este commit. O frontend pode consultar o contrato por tela sem inferir comportamento a partir de nomes de tabelas. QA pode usar node IDs e capturas de HTTP como evidência reproduzível. A qualificação histórica e a execução atual são explicitamente separadas.

| Documento | Objetivo |
| --- | --- |
| [01-ESTADO-ATUAL-DA-MAIN.md](01-ESTADO-ATUAL-DA-MAIN.md) | Branch/commit, inventário e status de cada módulo |
| [02-ARQUITETURA-TECNICA.md](02-ARQUITETURA-TECNICA.md) | Camadas, arquivos, dependências e diagramas |
| [03-REQUISITOS-E-REGRAS-DE-NEGOCIO.md](03-REQUISITOS-E-REGRAS-DE-NEGOCIO.md) | Requisitos/RN com código, condições, testes e rejeições |
| [04-CATALOGO-COMPLETO-DA-API.md](04-CATALOGO-COMPLETO-DA-API.md) | 76 operações, handlers, JWT/perfis, payloads, respostas, erros e 84 schemas |
| [05-GUIA-SWAGGER-PASSO-A-PASSO.md](05-GUIA-SWAGGER-PASSO-A-PASSO.md) | Sequência operacional, dados/IDs, pré-requisitos, falhas e evidências |
| [06-BANCO-DE-DADOS.md](06-BANCO-DE-DADOS.md) | 34 tabelas, 411 campos, FKs/CHECKs/índices/enums, ORM e dez migrations |
| [07-CONTRATO-DE-INTEGRACAO-FRONTEND.md](07-CONTRATO-DE-INTEGRACAO-FRONTEND.md) | Telas sugeridas, ações, campos, permissões e lacunas |
| [08-PLANO-DE-TESTES-E-VALIDACAO.md](08-PLANO-DE-TESTES-E-VALIDACAO.md) | 757 casos coletados: resultados e rastreabilidade |
| [09-PENDENCIAS-E-INCONSISTENCIAS.md](09-PENDENCIAS-E-INCONSISTENCIAS.md) | Problemas classificados e critérios de resolução |
| [10-FLUXOS-OPERACIONAIS.md](10-FLUXOS-OPERACIONAIS.md) | Dependências, bifurcações, estados e recuperação |
| [11-CHECKLIST-DE-HOMOLOGACAO.md](11-CHECKLIST-DE-HOMOLOGACAO.md) | Critérios objetivos com responsáveis e evidências |
| [12-GUIA-DE-EXECUCAO-LOCAL.md](12-GUIA-DE-EXECUCAO-LOCAL.md) | Configuração segura, execução isolada e troubleshooting |


## Artefatos seguros

- [openapi.json](openapi.json): schema obtido da aplicação auditada.
- [evidencias/routes.json](evidencias/routes.json): rotas e grafo de dependências.
- [evidencias/tables.json](evidencias/tables.json): metadata integral ORM.
- [evidencias/source-inventory.json](evidencias/source-inventory.json): funções/imports/migrations/testes e hashes, sem configuração privada.
- [evidencias/test-results.json](evidencias/test-results.json): resultado individual de cada caso.
- [evidencias/pytest.log](evidencias/pytest.log): saída completa da execução.
- [evidencias/document-validation.json](evidencias/document-validation.json): verificações de completude/links/preservação.

Fontes anteriores preservadas: [README](../../README.md), [contratos anteriores](../chicosense/contratos-api.md), [modelo científico](../chicosense/modelo-cientifico.md), [qualificação PostgreSQL histórica](../chicosense/validacao.md), [guardas PostgreSQL](../../tests/POSTGRESQL.md). Em divergência temporal, use comportamento do commit auditado e registre a diferença; uma possibilidade descrita em planejamento não é funcionalidade implementada.

## Relatório de conclusão e próximos passos

**Identificação:** main `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`, origin/main idêntica após fetch, auditoria em23/11/2026. Branch preservada; índice limpo; somente esta pasta de documentação nova. Origem oficial confirmada pelo remote Git. Não houve publicação ou alteração de implementação.

**Inventário:**13 grupos de routers registrados,76 operações de API em50 caminhos,84 schemas,4 rotas adicionais de documentação,34 tabelas ORM/411colunas,10 migrations,411 funções estáticas de testes que parametrizam757 casos. `app/modules` possui8 pacotes de primeiro nível: auth, empresas, integracoes, inteligencia, iot, logistica, monitoramento e produtos; inteligencia/iot são namespaces sem routers próprios. A contagem de grupos de routers não equivale à contagem de pacotes de domínio.

**Validação de23/11/2026:**745 aprovados,0 falhas,12 skips PostgreSQL;357,91s. Dois warnings: BlockingPortal (dependência já conhecida) e PytestAssertRewriteWarning de anyio causado pelo import antecipado no plugin externo da auditoria. Nenhum representa falha de aplicação. Não houve nova corrida PostgreSQL;757 aprovados/50 corridas é a qualificação histórica registrada em29/10/2026. As rotas /docs, /redoc, /openapi.json e /docs/oauth2-redirect responderam200 via TestClient. Não houve teste manual de navegador ou aquisição física.

**Documentação:** os13 Markdown listados acima foram efetivamente criados neste diretório, junto ao OpenAPI vivo e seis artefatos de evidência. Exemplos de sucesso das76 operações passaram pelos modelos Pydantic reais; links locais conferidos; nenhuma mudança em arquivo rastreado preexistente; scan em memória não encontrou valores secretos configurados nos artefatos. A validação documental está em evidencias/document-validation.json.

**Pendências:** nenhum CRÍTICO demonstrado no escopo; maiores limites são provisionamento de sensores/mapping fora do HTTP, reexecução PostgreSQL nesta auditoria e ausência de validação experimental específica. Swagger não enumera todos os erros; objetos de resultado/evidência abertos limitam geração de tipos. Dashboard/central global, refresh/logout, readiness e atuação física não existem. Isso não autoriza tratá-los como concluídos.

**Ações seguintes por equipe:** backend deve revisar P-01/P-02/P-04 e os contratos abertos; QA deve homologar Swagger manualmente e reexecutar PostgreSQL em outro banco vazio com identidade/guardas; frontend já pode implementar login, logística, sessões e consultas/ações por sessão usando este contrato, mantendo null/limitações/risco NAO_AVALIADO e rótulo SIMULADA. Agregadores, sensores via HTTP e refresh dependem de decisão de escopo e implementação futura. Infraestrutura deve prover seed isolado e origem CORS de homologação; qualquer inspeção remota, migration ou publicação exige tarefa separada.
