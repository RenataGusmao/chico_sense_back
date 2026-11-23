# Pendências e inconsistências

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Nota de publicação após a correção de CORS

Esta documentação preserva a auditoria do commit `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`; suas contagens, resultados e evidências são históricos desse código. A publicação documental parte da main `795f4b160325b863702e7ac793b381d777473d4a`, que já recebeu a correção de CORS pelo PR #4, commit `37887483cc7f12ce64e3974d31923978ec130f57`.

A pendência **P-11 foi corrigida no código**: `CORS_ALLOWED_ORIGINS` permite uma lista JSON de origens explícitas, somada às duas origens locais. Consulte o [README atual](../../README.md) e os [testes CORS](../../tests/test_cors.py). A configuração da variável no Render e a validação do login no navegador continuam sendo passos operacionais separados; esta publicação não os executa nem comprova sua realização.

A validação da correção registrou **765 aprovados, 12 skips PostgreSQL e um warning conhecido**, com 20 casos CORS acrescentados aos 757 casos anteriores (777 casos totais). Não se trata de reexecução da qualificação PostgreSQL. Não foram atualizados artificialmente os logs, hashes, schemas ou resultados originais da auditoria para fazê-los parecer uma nova execução. As referências a CORS limitado a localhost nos demais documentos descrevem o commit auditado, não a configuração atualizável da main após o PR #4.


## Resultado e critérios de severidade

Nenhum problema CRÍTICO foi demonstrado no escopo auditado. Isso não equivale a pentest, inspeção de segredos de produção ou autorização para publicar. ALTO indica bloqueio relevante de integração/alegação ou validação; MÉDIO divergência operacional/contrato; BAIXO dívida localizada. Não foram alteradas regras ou corrigidos problemas.

## P-01 · MÉDIO · Swagger incompleto para erros legados

| Campo | Descrição |
| --- | --- |
| Evidência | Login e /auth/me não declaram todos os 401/503; rotas de usuários/empresas não declaram toda autorização. Handler 422 remove input/ctx e coincide com loc/msg/type declarados; essa sanitização não é uma divergência de schema. |
| Arquivos/módulos | app/modules/auth/routes.py; app/api/routes/usuarios.py; app/modules/empresas/routes.py; app/main.py |
| Impacto | Clientes gerados/UI podem interpretar rejeições de forma incompleta. |
| Responsável sugerido | Backend |
| Recomendação | Documentar respostas de domínio em tarefa futura; teste contrato versus respostas. |
| Critério de resolução | Cada erro comprovado aparece corretamente no OpenAPI. |


## P-02 · ALTO · Provisionamento de sensores/mapping fora do HTTP

| Campo | Descrição |
| --- | --- |
| Evidência | Nenhum router registrado oferece CRUD de Sensor/Dispositivo ou gestão do mapping; setup_prototipo usa PROTOTIPO, rejeitado em TRANSPORTE_REFRIGERADO. |
| Arquivos/módulos | app/api/routes/__init__.py; scripts/setup_prototipo.py; app/modules/monitoramento/service.py:sensores |
| Impacto | Fluxo Swagger completo depende de seed externo identificado; integração frontend não pode cadastrar tudo. |
| Responsável sugerido | Backend/Infraestrutura |
| Recomendação | Definir e homologar procedimento local de provisionamento e ownership, sem contornar guardas. |
| Critério de resolução | Equipe reproduz sessão refrigerada com sensores válidos e fonte autorizada. |


## P-03 · MÉDIO · Sem readiness do banco

| Campo | Descrição |
| --- | --- |
| Evidência | /health retorna valores estáticos de configuração; não consulta DB e não há /ready. |
| Arquivos/módulos | app/api/routes/health.py |
| Impacto | Health 200 pode coexistir com banco indisponível. |
| Responsável sugerido | Infraestrutura/Backend |
| Recomendação | Definir readiness para operação futura e verificar conectividade no checklist. |
| Critério de resolução | Readiness distingue processo de dependências sem expor detalhes sensíveis. |


## P-04 · MÉDIO · Contratos de snapshots/evidências parcialmente abertos

| Campo | Descrição |
| --- | --- |
| Evidência | AvaliacaoResponse.resultado/entrada_snapshot e ListaEvidencias.evidencias usam dict; JSON Schema não determina todos os campos. |
| Arquivos/módulos | app/modules/monitoramento/preventivo_schemas.py; analises_schemas.py |
| Impacto | Frontend precisa deste guia e amostras; geração de tipos incompleta. |
| Responsável sugerido | Backend/Frontend |
| Recomendação | Versionar e detalhar contratos dos objetos abertos antes de consumidores rígidos. |
| Critério de resolução | Contrato tipado e exemplos positivos/negativos aprovados pela integração. |


## P-05 · MÉDIO · Faltam agregadores e listagem global para telas propostas

| Campo | Descrição |
| --- | --- |
| Evidência | Somente listas por sessão/carga/viagem; sem dashboard, central global ou WebSocket. |
| Arquivos/módulos | app/api/routes/__init__.py; openapi.json |
| Impacto | Frontend não pode presumir contadores globais nem central completa. |
| Responsável sugerido | Frontend/Backend |
| Recomendação | Definir escopo das telas usando contratos presentes; qualquer nova API em tarefa separada. |
| Critério de resolução | Tela não exibe agregado incompleto como total global. |


## P-06 · MÉDIO · Sessão de autenticação sem refresh/logout

| Campo | Descrição |
| --- | --- |
| Evidência | Somente login e me; JWT expira e usuário ativo é consultado; não há revogação individual. |
| Arquivos/módulos | app/modules/auth/routes.py; app/core/security.py |
| Impacto | UI deve reautenticar; estratégia de armazenamento precisa de decisão própria. |
| Responsável sugerido | Frontend/Backend |
| Recomendação | Documentar UX de expiração e ameaça de armazenamento; não inventar endpoints. |
| Critério de resolução | 401 tratado, dados limpos ao trocar usuário, segredo não vai a logs/URLs. |


## P-07 · MÉDIO · Reexecução PostgreSQL pendente nesta auditoria

| Campo | Descrição |
| --- | --- |
| Evidência | 12 testes skipped porque opt-ins estão ausentes; qualificação histórica permanece documentação, não execução atual. |
| Arquivos/módulos | tests/POSTGRESQL.md; tests/test_postgresql_real.py; docs/chicosense/validacao.md |
| Impacto | Não comprova catálogo/locks no ambiente publicado ou após mudanças de infraestrutura. |
| Responsável sugerido | Testes/Infraestrutura |
| Recomendação | Reexecutar em novo banco descartável com identidade/guardas; depois repetir concorrência. |
| Critério de resolução | 12 aprovados e repetição concorrente, sem skips nem acesso remoto. |


## P-08 · BAIXO · Autogenerate textual no índice normalizado

| Campo | Descrição |
| --- | --- |
| Evidência | Alembic pode propor recriação equivalente trim(email)/TRIM(BOTH FROM email); comparação estrita descrita no teste. |
| Arquivos/módulos | tests/test_postgresql_real.py; app/models/usuario.py |
| Impacto | Aplicação cega de autogenerate gera DDL desnecessário. |
| Responsável sugerido | Backend |
| Recomendação | Revisar autogenerate e equivalência antes de aceitar migration. |
| Critério de resolução | Nenhuma recriação redundante aplicada; diferenças reais continuam falhando. |


## P-09 · MÉDIO · Documentos científicos preservam linguagem de etapa anterior

| Campo | Descrição |
| --- | --- |
| Evidência | modelo-cientifico.md contém implementação futura e referência aos 151 testes do diagnóstico; fonte de conhecimento científico, não fotografia atual. |
| Arquivos/módulos | docs/chicosense/modelo-cientifico.md |
| Impacto | Leitor pode confundir especificação histórica com status atual. |
| Responsável sugerido | Backend/Testes |
| Recomendação | Usar auditoria atual como índice temporal; marcar contexto histórico em revisão documental futura. |
| Critério de resolução | Contagens/status têm data e escopo explícitos. |


## P-10 · ALTO · Validade biológica e integração física não verificadas

| Campo | Descrição |
| --- | --- |
| Evidência | Taxas gerais de manga; ausência de validação cultivar, calibração/representatividade e sensor de etileno. Exaustão é virtual. |
| Arquivos/módulos | app/modules/monitoramento/etileno/parametros.py; exaustao_service.py |
| Impacto | Bloqueia alegações de concentração, dano, eficácia ou segurança fisiológica; não bloqueia demonstrador computacional rotulado. |
| Responsável sugerido | Testes/Backend |
| Recomendação | Planejar validação experimental separada e manter rótulos/limitações no frontend. |
| Critério de resolução | Nenhuma UI/documento confunde potencial com gás medido ou eficácia física. |


## P-11 · MÉDIO · CORS limitado ao desenvolvimento

| Campo | Descrição |
| --- | --- |
| Evidência | allow_origins contém apenas localhost e 127.0.0.1:5173. |
| Arquivos/módulos | app/main.py |
| Impacto | Frontend em outro domínio/porta não está habilitado pelo contrato atual. |
| Responsável sugerido | Infraestrutura/Frontend |
| Recomendação | Definir origem de homologação em tarefa autorizada; manter JWT/escopo. |
| Critério de resolução | Preflight/navegador na origem pretendida aprovados, sem abrir * indiscriminadamente. |


## P-12 · BAIXO · Warning de TestClient

| Campo | Descrição |
| --- | --- |
| Evidência | Depreciação BlockingPortal de Starlette/TestClient observada no log da suíte. |
| Arquivos/módulos | requirements.txt; evidencias/pytest.log |
| Impacto | Dívida de compatibilidade de dependências, sem falha observada. |
| Responsável sugerido | Testes/Backend |
| Recomendação | Avaliar atualização coordenada com regressão completa em tarefa futura. |
| Critério de resolução | Warning resolvido ou aceito com versão e evidência. |


## Revisão transversal

Código×README: módulos/limitações gerais coerentes com a main; não foi observada promessa de hardware ativo. Código×OpenAPI: snapshot anterior comparado ao vivo, sem diff; incompletudes P-01/P-04 são do próprio contrato. Código×testes: suíte local aprovada, mas PostgreSQL e hardware são limites distintos. Models×migrations: cadeia estática presente, comparação PostgreSQL histórica com exceção textual restrita P-08. Requisitos×implementação: dashboard, sensores via HTTP, refresh/logout, readiness e gás físico explicitamente ausentes. Backend×frontend: não presumir telas prontas ou APIs agregadas.

Política de existência/escopo não é homogênea: logística pode buscar recurso antes de autorizar (404 inexistente,403 externo); EmpresaService.authorize verifica vínculo antes de buscar para não ADMIN. Não uniformizar comportamento no cliente nem prometer ocultação de existência por 404 em todas as rotas. Evidências: LogisticaAccess.resource e EmpresaService.authorize, testes de isolamento.
