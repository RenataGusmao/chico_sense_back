# Estado atual da main

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Nota de publicação após a correção de CORS

Esta documentação preserva a auditoria do commit `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`; suas contagens, resultados e evidências são históricos desse código. A publicação documental parte da main `795f4b160325b863702e7ac793b381d777473d4a`, que já recebeu a correção de CORS pelo PR #4, commit `37887483cc7f12ce64e3974d31923978ec130f57`.

A pendência **P-11 foi corrigida no código**: `CORS_ALLOWED_ORIGINS` permite uma lista JSON de origens explícitas, somada às duas origens locais. Consulte o [README atual](../../README.md) e os [testes CORS](../../tests/test_cors.py). A configuração da variável no Render e a validação do login no navegador continuam sendo passos operacionais separados; esta publicação não os executa nem comprova sua realização.

A validação da correção registrou **765 aprovados, 12 skips PostgreSQL e um warning conhecido**, com 20 casos CORS acrescentados aos 757 casos anteriores (777 casos totais). Não se trata de reexecução da qualificação PostgreSQL. Não foram atualizados artificialmente os logs, hashes, schemas ou resultados originais da auditoria para fazê-los parecer uma nova execução. As referências a CORS limitado a localhost nos demais documentos descrevem o commit auditado, não a configuração atualizável da main após o PR #4.


## Identificação e preservação

Repositório `C:\Users\Lenovo\Downloads\Gerenciador de Tarefas\chico_sense_back`; origin https://github.com/RenataGusmao/chico_sense_back.git. Branch main, commit `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5` (merge PR #3). `git fetch origin` executado; origin/main coincide com HEAD. Não houve checkout, merge, rebase, commit, staging, push, deploy ou migration.

`git status --short` inicialmente falhou por acesso ao diretório no sandbox. Após liberar a travessia, retornou vazio; índice limpo. Comparação adicional dos arquivos rastreados contra HEAD (normalizando CRLF) não encontrou alteração. Ao final somente docs/auditoria-main é novo/não rastreado; código preexistente preservado. A auditoria usa código efetivamente integrado na main, não a branch feature.


| Métrica | Quantidade / evidência |
| --- | --- |
| Grupos de routers incluídos | 13 |
| Operações HTTP OpenAPI | 76 |
| Caminhos OpenAPI | 50 |
| Schemas | 84 |
| Rotas de documentação fora do schema | 4 |
| Tabelas ORM | 34 |
| Colunas ORM | 411 |
| Migrations | 10 |
| Funções estáticas de teste | 411 |
| Casos de teste coletados | 757 |
| Resultado atual | {'passed': 745, 'skipped': 12} |


## Estado por funcionalidade

A classificação é limitada ao comportamento computacional e ao ambiente descrito; não significa validação biológica, hardware ou produção.

| Módulo/funcionalidade | Status | Evidência/limite |
| --- | --- | --- |
| Autenticação/usuários/empresas | IMPLEMENTADA E VALIDADA | JWT real e testes HTTP locais; sem refresh/logout |
| Produtos/logística | IMPLEMENTADA E VALIDADA | 27 rotas protegidas; teste de isolamento |
| ThingSpeak | IMPLEMENTADA E VALIDADA | Cliente/mapping/mock e redaction; provedor real NÃO VERIFICÁVEL NO AMBIENTE |
| Declaração e sessões | IMPLEMENTADA E VALIDADA | Criação/finalização, snapshots e constraints locais |
| Histórico IoT | IMPLEMENTADA E VALIDADA | Dedup/revisões/qualidade em testes; aquisição física não verificada |
| Potencial de etileno | IMPLEMENTADA E VALIDADA | Motor e persistência computacional; validade cultivar NÃO VERIFICÁVEL NO AMBIENTE |
| Configurações/preventivo/alertas | IMPLEMENTADA E VALIDADA | Regras operacionais e decisões; não limiares de dano |
| Intervenções simuladas | IMPLEMENTADA E VALIDADA | Estado virtual e ações humanas; hardware NÃO IMPLEMENTADO |
| PostgreSQL real/concorrência | IMPLEMENTADA, MAS NÃO VALIDADA | Nesta execução: 12 skips; qualificação histórica documentada separadamente |
| Swagger/OpenAPI | PARCIALMENTE IMPLEMENTADA | Rotas habilitadas, schemas presentes; erros/exemplos/objetos abertos incompletos |
| Dashboard global / refresh / readiness | NÃO IMPLEMENTADA | Ausentes no registro real de rotas |
| Sensores/dispositivos via HTTP | NÃO IMPLEMENTADA | Models/scripts presentes, CRUD HTTP ausente |
| Planejamentos históricos | DOCUMENTADA, MAS AUSENTE DO CÓDIGO | Possibilidades futuras de ciência/hardware não são implementação; não há escore fisiológico ou exaustão física |


## Evidências e proveniência

Registro de rotas/símbolos/metadata exportado em processo com destino SQLite em memória e segredo artificial, sem abrir conexão. OpenAPI gerado ao vivo da aplicação foi comparado ao snapshot versionado; idêntico. Asserções de HTTP vêm da execução local, não de ambiente publicado. Nenhum banco remoto foi inspecionado.

[Snapshot OpenAPI](openapi.json), [inventário de fontes](evidencias/source-inventory.json), [resultado individual dos testes](evidencias/test-results.json), [validação documental](evidencias/document-validation.json).

## Git ao entregar

`git status --short`: `?? docs/auditoria-main/`. `git diff --name-status` e `git diff --cached --name-status`: vazios. HEAD e origin/main permanecem no commit auditado. As permissões adicionais do sandbox foram necessárias apenas para leitura/travessia, fetch e escrita dos novos artefatos; nenhum arquivo preexistente foi sobrescrito.

As categorias de implementação são temporais: PostgreSQL tem validação histórica real integrada e não foi revalidado agora; “IMPLEMENTADA, MAS NÃO VALIDADA” nessa linha diz respeito à execução atual, não apaga as evidências anteriores. Os campos científicos “maturação desconhecida” e “risco não avaliado” são resultados explícitos, não funcionalidades faltantes.
