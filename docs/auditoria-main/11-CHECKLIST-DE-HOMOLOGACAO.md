# Checklist de homologação

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Critérios e evidências exigidas

APROVADO LOCAL é restrito aos testes desta auditoria. HISTÓRICO não é execução atual; PENDENTE não conta como aprovado. Nenhum item autoriza deploy.

| Responsável | Critério objetivo | Evidência exigida | Status |
| --- | --- | --- | --- |
| Backend | main e origin/main coincidem com commit auditado | git fetch/rev-parse e preservação de hashes | APROVADO LOCAL |
| Backend | 100% das rotas inventariadas; docs habilitadas | 76 operações +4 docs; OpenAPI vivo; TestClient docs | APROVADO LOCAL |
| Backend/QA | JWT ausente/inválido/expirado e escopo externo rejeitados | testes de segurança + preservação de recursos | APROVADO LOCAL |
| QA | Suíte local sem falha e skips identificados | 745 pass,12 skip; log | APROVADO LOCAL com limite PostgreSQL |
| Infra/QA | Migration completa e corrida entre conexões reais | Novo DB com identidade/token;12 verdes; repetir concorrência | HISTÓRICO aprovado; reexecução atual PENDENTE |
| Infra | Confirmar migrations do ambiente de homologação | Inspeção autorizada do catálogo/heads; sem assumir Supabase | PENDENTE; não consultado |
| Backend/Infra | Sensores/mapping provisionados com contexto refrigerado | IDs/vínculos/unidades/field mapping sem chaves publicadas | PENDENTE manual; fixtures validadas |
| Frontend | Token/401/403/409/422 tratados e listas vazias distintas de erro | Teste navegador/UI por perfil e transportadora | PENDENTE; contrato disponível |
| Frontend | Não confundir subtotal com total; null não vira zero | Tela PARCIAL/SEM_ESTIMATIVA/maturação desconhecida | PENDENTE UI; backend validado |
| Frontend | Exaustão sempre SIMULADA; não dispara timer/comando físico | Tela usa ações permitidas e GET depois da transição | PENDENTE UI; backend validado |
| QA | Fluxo ponta a ponta em fixtures locais | test_fluxo_integrado_ponta_a_ponta_etapa8 | APROVADO LOCAL |
| QA | Swagger manual completo com banco isolado | Requests/IDs/estados/rows por etapa do guia | PENDENTE; não confundir TestClient com navegador |
| Backend/QA | Erros do Swagger refletem comportamento | Resolver P-01/P-04 com revisão de contrato | PENDENTE |
| Infra/Frontend | Origem CORS da integração aprovada | Preflight e navegador no domínio pretendido | PENDENTE |
| Equipe científica | Representatividade/calibração e validade cultivar | Protocolo experimental e evidência independente | PENDENTE; não requisito provado por testes unitários |
| Equipe | Nenhum código/segredo alterado e nenhum commit/push | git diff/index; somente docs novas; scan seguro | APROVADO LOCAL |
