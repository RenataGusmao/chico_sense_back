# Contrato de integração frontend-backend

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Estratégia comum

Autenticar por JSON `/auth/login`, manter token apenas na sessão do cliente conforme decisão de segurança da equipe e enviar Authorization Bearer. A API não define armazenamento browser e não fornece cookie httpOnly/refresh/logout. Não colocar JWT em URL/log/analytics; reautenticar em 401. Em 403 mostrar indisponibilidade por permissão, sem trocar empresa_id para contornar o servidor. Escopo da empresa é validado pelos vínculos armazenados. Limpar dados exibidos ao trocar identidade.

422 pode retornar `detail` lista de `{type,loc,msg}`; domínio retorna string. 409 exige consultar estado/chave/revisão antes de reenviar; 503 exige feedback sem assumir falha definitiva do commit e retry idempotente. Não persistir mensagens de erro brutas com possíveis dados pessoais. Não existe envelope universal de listagem: listas simples legadas e envelopes novos convivem.

Sugestões de telas/atualização abaixo são trabalho futuro de UI. Nenhuma tela frontend foi criada ou validada nesta auditoria. Perfil, entrada, saída, campos obrigatórios/opcionais e erros de cada ação estão vinculados ao catálogo integral; as matrizes não exigem interpretação do código Python.

| Tela sugerida | Contrato/condições |
| --- | --- |
| Login | Obter JWT; expires_in em segundos; sem refresh; expiração exige novo login. |
| Dashboard geral | Não existe agregador/dashboard nem websocket; compor apenas recursos disponíveis no escopo e sinalizar listas parciais. |
| Transportadoras | ADMIN cria/edita e vincula usuários. Outros consultam empresas permitidas; PRODUTOR/CLIENTE são tipos, não transportadoras. |
| Usuários e perfis | Administração ADMIN; /auth/me para identidade corrente; não exibir hashes. |
| Produtos | Catálogo global; somente ADMIN escreve; parâmetro de produto não é configuração ambiental de sessão. |
| Frota e motoristas | Gestor/Admin escreve; transportar empresa_id não autoriza acesso. Tela também usa motoristas. |
| Cargas | Criação aninhada na viagem; declaração de monitoramento separada, não inferir massa de quantidade/caixas. |
| Viagens | Frota/motorista da mesma empresa; estados e horários reais coerentes. |
| Sessões | Histórico por carga/viagem; não existe listagem global de todas as sessões. Sensor precisa ser provisionado fora da UI atual. |
| Histórico IoT | Fixar revisão/janela; não preencher null com zero; distinguir medida_em/recebida_em/processada_em e estado da coleta. |
| Análises científicas | Mostrar faixa potencial µL, cobertura, motivos/limitações; PARCIAL só subtotal, total null; risco NAO_AVALIADO. |
| Configurações ambientais | Criar versão por sessão; perfis elevados; limites operacionais justificados, sem sugestão científica automática. |
| Avaliações preventivas | Exibir status e achados; AVALIADO não significa seguro; análise contextual opcional. |
| Central de alertas | Consulta por sessão; não há central global; nível operacional não equivale a dano fisiológico. |
| Detalhes/decisões | Exibir evidências e histórico; nota OBSERVAR não altera estado; decisões exigem justificativa/chave. |
| Intervenções simuladas | Solicitar/autorizar/iniciar/encerrar são ações distintas. acoes_permitidas auxilia UI, servidor revalida. Sem timer que conclui execução. |
| Histórico operacional | Históricos por recurso/sessão; não existe exportação/auditoria global HTTP. Preservar snapshots e hashes para consulta, não recomputar na tela. |


## Login

Obter JWT; expires_in em segundos; sem refresh; expiração exige novo login.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-007 | /api/v1/auth/login | POST | Público | LoginRequest | TokenResponse | IMPLEMENTADA; evidência HTTP 9 capturas |


### Campos de LoginRequest

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| email | True | string / email | {   "format": "email" } |
| senha | True | string / password | {   "maxLength": 128,   "minLength": 1,   "format": "password",   "writeOnly": true } |


## Dashboard geral

Não existe agregador/dashboard nem websocket; compor apenas recursos disponíveis no escopo e sinalizar listas parciais.

Status: tela sugerida; endpoint dedicado NÃO IMPLEMENTADO. Não simular resposta ou inventar contadores globais.

## Transportadoras

ADMIN cria/edita e vincula usuários. Outros consultam empresas permitidas; PRODUTOR/CLIENTE são tipos, não transportadoras.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-014 | /api/v1/empresas | POST | ADMIN | EmpresaCreate | EmpresaResponse | IMPLEMENTADA; evidência HTTP 16 capturas |
| API-015 | /api/v1/empresas | GET | Usuário ativo autenticado | Path/query; sem body | lista de EmpresaResponse | IMPLEMENTADA; evidência HTTP 3 capturas |
| API-016 | /api/v1/empresas/{empresa_id} | GET | Usuário ativo autenticado | Path/query; sem body | EmpresaResponse | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-017 | /api/v1/empresas/{empresa_id} | PATCH | ADMIN | EmpresaUpdate | EmpresaResponse | IMPLEMENTADA; evidência HTTP 12 capturas |
| API-018 | /api/v1/empresas/{empresa_id}/usuarios/{usuario_id} | POST | ADMIN | Path/query; sem body | VinculoResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-019 | /api/v1/empresas/{empresa_id}/usuarios | GET | ADMIN/GESTOR | Path/query; sem body | lista de UsuarioResponse | IMPLEMENTADA; evidência HTTP 2 capturas |


### Campos de EmpresaCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | True | string | {   "maxLength": 180,   "minLength": 1 } |
| tipo | True | TipoEmpresa | {} |
| documento | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40,       "minLength": 1     },     {       "type": "null"     }   ] } |
| ativo | False | boolean | {   "default": true } |


### Campos de EmpresaUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 180,       "minLength": 1     },     {       "type": "null"     }   ] } |
| tipo | False | TipoEmpresa ou null | {   "anyOf": [     {       "$ref": "#/components/schemas/TipoEmpresa"     },     {       "type": "null"     }   ] } |
| documento | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40,       "minLength": 1     },     {       "type": "null"     }   ] } |
| ativo | False | boolean ou null | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ] } |


## Usuários e perfis

Administração ADMIN; /auth/me para identidade corrente; não exibir hashes.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-010 | /api/v1/usuarios | POST | ADMIN | UsuarioCreate | UsuarioResponse | IMPLEMENTADA; evidência HTTP 4 capturas |
| API-011 | /api/v1/usuarios | GET | ADMIN | Path/query; sem body | lista de UsuarioResponse | IMPLEMENTADA; evidência HTTP 4 capturas |
| API-012 | /api/v1/usuarios/{usuario_id} | GET | ADMIN | Path/query; sem body | UsuarioResponse | IMPLEMENTADA; evidência HTTP 2 capturas |
| API-013 | /api/v1/usuarios/{usuario_id} | PATCH | ADMIN | UsuarioUpdate | UsuarioResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-018 | /api/v1/empresas/{empresa_id}/usuarios/{usuario_id} | POST | ADMIN | Path/query; sem body | VinculoResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-019 | /api/v1/empresas/{empresa_id}/usuarios | GET | ADMIN/GESTOR | Path/query; sem body | lista de UsuarioResponse | IMPLEMENTADA; evidência HTTP 2 capturas |


### Campos de UsuarioCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | True | string | {   "maxLength": 150,   "minLength": 1 } |
| email | True | string / email | {   "maxLength": 255,   "format": "email" } |
| senha | True | string / password | {   "maxLength": 128,   "minLength": 12,   "format": "password",   "writeOnly": true } |
| perfil_id | True | string / uuid | {   "format": "uuid" } |
| ativo | False | boolean | {   "default": true } |


### Campos de UsuarioUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 150,       "minLength": 1     },     {       "type": "null"     }   ] } |
| email | False | string / email ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255,       "format": "email"     },     {       "type": "null"     }   ] } |
| senha | False | string / password ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 128,       "minLength": 12,       "format": "password",       "writeOnly": true     },     {       "type": "null"     }   ] } |
| perfil_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| ativo | False | boolean ou null | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ] } |


## Produtos

Catálogo global; somente ADMIN escreve; parâmetro de produto não é configuração ambiental de sessão.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-020 | /api/v1/produtos | POST | ADMIN | ProdutoCreate | ProdutoResponse | IMPLEMENTADA; evidência HTTP 72 capturas |
| API-021 | /api/v1/produtos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de ProdutoResponse | IMPLEMENTADA; evidência HTTP 12 capturas |
| API-022 | /api/v1/produtos/{produto_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ProdutoResponse | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-023 | /api/v1/produtos/{produto_id} | PATCH | ADMIN | ProdutoUpdate | ProdutoResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-024 | /api/v1/produtos/{produto_id}/parametros | POST | ADMIN | ParametroCreate | ParametroResponse | IMPLEMENTADA; evidência HTTP 14 capturas |
| API-025 | /api/v1/produtos/{produto_id}/parametros | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de ParametroResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-026 | /api/v1/produtos/{produto_id}/parametros/{parametro_id} | PATCH | ADMIN | ParametroUpdate | ParametroResponse | IMPLEMENTADA; evidência HTTP 9 capturas |


### Campos de ParametroCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome_parametro | True | string | {   "maxLength": 120,   "minLength": 1 } |
| unidade | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 30     },     {       "type": "null"     }   ] } |
| valor_minimo | False | number ou string ou null | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| valor_maximo | False | number ou string ou null | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| observacao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de ParametroUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome_parametro | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120,       "minLength": 1     },     {       "type": "null"     }   ] } |
| unidade | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 30     },     {       "type": "null"     }   ] } |
| valor_minimo | False | number ou string ou null | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| valor_maximo | False | number ou string ou null | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| observacao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de ProdutoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | True | string | {   "maxLength": 120,   "minLength": 1 } |
| descricao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |
| ativo | False | boolean | {   "default": true } |


### Campos de ProdutoUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120,       "minLength": 1     },     {       "type": "null"     }   ] } |
| descricao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |
| ativo | False | boolean ou null | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ] } |


## Frota e motoristas

Gestor/Admin escreve; transportar empresa_id não autoriza acesso. Tela também usa motoristas.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-027 | /api/v1/veiculos | POST | ADMIN/GESTOR | VeiculoCreate | VeiculoResponse | IMPLEMENTADA; evidência HTTP 72 capturas |
| API-028 | /api/v1/veiculos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de VeiculoResponse | IMPLEMENTADA; evidência HTTP 16 capturas |
| API-029 | /api/v1/veiculos/{veiculo_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | VeiculoResponse | IMPLEMENTADA; evidência HTTP 18 capturas |
| API-030 | /api/v1/veiculos/{veiculo_id} | PATCH | ADMIN/GESTOR | VeiculoUpdate | VeiculoResponse | IMPLEMENTADA; evidência HTTP 14 capturas |
| API-031 | /api/v1/motoristas | POST | ADMIN/GESTOR | MotoristaCreate | MotoristaResponse | IMPLEMENTADA; evidência HTTP 71 capturas |
| API-032 | /api/v1/motoristas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de MotoristaResponse | IMPLEMENTADA; evidência HTTP 16 capturas |
| API-033 | /api/v1/motoristas/{motorista_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | MotoristaResponse | IMPLEMENTADA; evidência HTTP 18 capturas |
| API-034 | /api/v1/motoristas/{motorista_id} | PATCH | ADMIN/GESTOR | MotoristaUpdate | MotoristaResponse | IMPLEMENTADA; evidência HTTP 7 capturas |


### Campos de MotoristaCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| empresa_id | True | string / uuid | {   "format": "uuid" } |
| nome | True | string | {   "maxLength": 150,   "minLength": 1 } |
| documento | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40,       "minLength": 1     },     {       "type": "null"     }   ] } |
| telefone | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40     },     {       "type": "null"     }   ] } |
| ativo | False | boolean | {   "default": true } |


### Campos de MotoristaUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| nome | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 150,       "minLength": 1     },     {       "type": "null"     }   ] } |
| documento | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40,       "minLength": 1     },     {       "type": "null"     }   ] } |
| telefone | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 40     },     {       "type": "null"     }   ] } |
| ativo | False | boolean ou null | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ] } |


### Campos de VeiculoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| empresa_id | True | string / uuid | {   "format": "uuid" } |
| identificador | True | string | {   "maxLength": 80,   "minLength": 1 } |
| placa | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 20,       "minLength": 1     },     {       "type": "null"     }   ] } |
| modelo | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120     },     {       "type": "null"     }   ] } |
| descricao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |
| ativo | False | boolean | {   "default": true } |


### Campos de VeiculoUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| identificador | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 80,       "minLength": 1     },     {       "type": "null"     }   ] } |
| placa | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 20,       "minLength": 1     },     {       "type": "null"     }   ] } |
| modelo | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120     },     {       "type": "null"     }   ] } |
| descricao | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |
| ativo | False | boolean ou null | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ] } |


## Cargas

Criação aninhada na viagem; declaração de monitoramento separada, não inferir massa de quantidade/caixas.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-039 | /api/v1/viagens/{viagem_id}/cargas | POST | ADMIN/GESTOR/OPERADOR | CargaCreate | CargaResponse | IMPLEMENTADA; evidência HTTP 74 capturas |
| API-040 | /api/v1/viagens/{viagem_id}/cargas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de CargaResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-041 | /api/v1/cargas/{carga_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | CargaResponse | IMPLEMENTADA; evidência HTTP 29 capturas |
| API-042 | /api/v1/cargas/{carga_id} | PATCH | ADMIN/GESTOR/OPERADOR | CargaUpdate | CargaResponse | IMPLEMENTADA; evidência HTTP 16 capturas |
| API-043 | /api/v1/cargas/{carga_id}/caixas | POST | ADMIN/GESTOR/OPERADOR | CaixaCreate | CaixaResponse | IMPLEMENTADA; evidência HTTP 70 capturas |
| API-044 | /api/v1/cargas/{carga_id}/caixas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de CaixaResponse | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-047 | /api/v1/cargas/{carga_id}/monitoramento | PUT | ADMIN/GESTOR/OPERADOR | CargaMonitoramentoPut | CargaMonitoramentoResponse | IMPLEMENTADA; evidência HTTP 354 capturas |
| API-048 | /api/v1/cargas/{carga_id}/monitoramento | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | CargaMonitoramentoResponse | IMPLEMENTADA; evidência HTTP 4 capturas |
| API-049 | /api/v1/cargas/{carga_id}/monitoramentos | POST | ADMIN/GESTOR/OPERADOR | SessaoCreate | SessaoResponse-Output, SessaoResponse-Input | IMPLEMENTADA; evidência HTTP 333 capturas |
| API-050 | /api/v1/cargas/{carga_id}/monitoramentos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 6 capturas |


### Campos de CaixaCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| identificacao | True | string | {   "maxLength": 120,   "minLength": 1 } |
| codigo_externo | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120     },     {       "type": "null"     }   ] } |
| peso | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de CargaCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| produto_id | True | string / uuid | {   "format": "uuid" } |
| produtor_id | True | string / uuid | {   "format": "uuid" } |
| cliente_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| identificacao | True | string | {   "maxLength": 120,   "minLength": 1 } |
| quantidade_caixas | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "maximum": 2147483647.0,       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| quantidade | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| unidade | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 30,       "minLength": 1     },     {       "type": "null"     }   ] } |
| origem_produto | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de CargaMonitoramentoPut

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| produto_identificado | True | string | {   "enum": [     "MANGA_TOMMY_ATKINS"   ],   "const": "MANGA_TOMMY_ATKINS" } |
| massa_kg | True | number ou string | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| maturacao | False | MaturacaoCarga | {   "default": "DESCONHECIDA" } |
| lote_codigo | True | string | {   "maxLength": 120,   "minLength": 1 } |
| lote_hipotetico | True | boolean | {} |
| rastreabilidade | True | string | {   "maxLength": 2000,   "minLength": 1 } |


### Campos de CargaUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| identificacao | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 120,       "minLength": 1     },     {       "type": "null"     }   ] } |
| quantidade_caixas | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "maximum": 2147483647.0,       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| quantidade | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| unidade | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 30,       "minLength": 1     },     {       "type": "null"     }   ] } |
| origem_produto | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |
| status | False | StatusCarga ou null | {   "anyOf": [     {       "$ref": "#/components/schemas/StatusCarga"     },     {       "type": "null"     }   ] } |


### Campos de SessaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| inicio | True | string / date-time | {   "format": "date-time" } |
| sensor_temperatura_id | True | string / uuid | {   "format": "uuid" } |
| sensor_umidade_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| ambiente_aquisicao | True | string | {   "enum": [     "LABORATORIO",     "TRANSPORTE_REFRIGERADO"   ] } |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 2000     },     {       "type": "null"     }   ] } |


## Viagens

Frota/motorista da mesma empresa; estados e horários reais coerentes.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-035 | /api/v1/viagens | POST | ADMIN/GESTOR/OPERADOR | ViagemCreate | ViagemResponse | IMPLEMENTADA; evidência HTTP 73 capturas |
| API-036 | /api/v1/viagens | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de ViagemResponse | IMPLEMENTADA; evidência HTTP 21 capturas |
| API-037 | /api/v1/viagens/{viagem_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ViagemResponse | IMPLEMENTADA; evidência HTTP 25 capturas |
| API-038 | /api/v1/viagens/{viagem_id} | PATCH | ADMIN/GESTOR/OPERADOR | ViagemUpdate | ViagemResponse | IMPLEMENTADA; evidência HTTP 22 capturas |
| API-039 | /api/v1/viagens/{viagem_id}/cargas | POST | ADMIN/GESTOR/OPERADOR | CargaCreate | CargaResponse | IMPLEMENTADA; evidência HTTP 74 capturas |
| API-040 | /api/v1/viagens/{viagem_id}/cargas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de CargaResponse | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-051 | /api/v1/viagens/{viagem_id}/monitoramentos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 5 capturas |


### Campos de CargaCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| produto_id | True | string / uuid | {   "format": "uuid" } |
| produtor_id | True | string / uuid | {   "format": "uuid" } |
| cliente_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| identificacao | True | string | {   "maxLength": 120,   "minLength": 1 } |
| quantidade_caixas | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "maximum": 2147483647.0,       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| quantidade | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| unidade | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 30,       "minLength": 1     },     {       "type": "null"     }   ] } |
| origem_produto | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de ViagemCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| transportadora_id | True | string / uuid | {   "format": "uuid" } |
| veiculo_id | True | string / uuid | {   "format": "uuid" } |
| motorista_id | True | string / uuid | {   "format": "uuid" } |
| origem | True | string | {   "maxLength": 255,   "minLength": 1 } |
| destino | True | string | {   "maxLength": 255,   "minLength": 1 } |
| saida_em | True | string / date-time | {   "format": "date-time" } |
| previsao_chegada_em | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


### Campos de ViagemUpdate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| veiculo_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| motorista_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| origem | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255,       "minLength": 1     },     {       "type": "null"     }   ] } |
| destino | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 255,       "minLength": 1     },     {       "type": "null"     }   ] } |
| saida_em | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| previsao_chegada_em | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| inicio_real | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| chegada_em | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| status | False | StatusViagem ou null | {   "anyOf": [     {       "$ref": "#/components/schemas/StatusViagem"     },     {       "type": "null"     }   ] } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string"     },     {       "type": "null"     }   ] } |


## Sessões

Histórico por carga/viagem; não existe listagem global de todas as sessões. Sensor precisa ser provisionado fora da UI atual.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-049 | /api/v1/cargas/{carga_id}/monitoramentos | POST | ADMIN/GESTOR/OPERADOR | SessaoCreate | SessaoResponse-Output, SessaoResponse-Input | IMPLEMENTADA; evidência HTTP 333 capturas |
| API-050 | /api/v1/cargas/{carga_id}/monitoramentos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-051 | /api/v1/viagens/{viagem_id}/monitoramentos | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | lista de SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-052 | /api/v1/monitoramentos/{sessao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-053 | /api/v1/monitoramentos/{sessao_id}/encerrar | POST | ADMIN/GESTOR/OPERADOR | SessaoFinalizar | SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 99 capturas |
| API-054 | /api/v1/monitoramentos/{sessao_id}/cancelar | POST | ADMIN/GESTOR/OPERADOR | SessaoFinalizar | SessaoResponse-Output | IMPLEMENTADA; evidência HTTP 11 capturas |
| API-055 | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | POST | ADMIN/GESTOR/OPERADOR | SincronizacaoCreate | SincronizacaoResponse, SincronizacaoResponse | IMPLEMENTADA; evidência HTTP 189 capturas |
| API-056 | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | EstadoSincronizacaoResponse | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-057 | /api/v1/monitoramentos/{sessao_id}/leituras | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | HistoricoResponse | IMPLEMENTADA; evidência HTTP 40 capturas |
| API-058 | /api/v1/monitoramentos/{sessao_id}/qualidade | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | QualidadeResponse | IMPLEMENTADA; evidência HTTP 19 capturas |
| API-059 | /api/v1/monitoramentos/{sessao_id}/analises-etileno | POST | ADMIN/GESTOR/OPERADOR | AnaliseCreate | AnaliseResponse | IMPLEMENTADA; evidência HTTP 82 capturas |
| API-060 | /api/v1/monitoramentos/{sessao_id}/analises-etileno | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AnaliseLista | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-061 | /api/v1/monitoramentos/{sessao_id}/analises-etileno/{analise_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AnaliseResponse | IMPLEMENTADA; evidência HTTP 17 capturas |
| API-062 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | POST | ADMIN/GESTOR | ConfiguracaoCreate | ConfiguracaoResponse | IMPLEMENTADA; evidência HTTP 80 capturas |
| API-063 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaConfiguracoes | IMPLEMENTADA; evidência HTTP 4 capturas |
| API-064 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | POST | ADMIN/GESTOR/OPERADOR | AvaliacaoCreate | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 86 capturas |
| API-065 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAvaliacoes | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-066 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-067 | /api/v1/monitoramentos/{sessao_id}/alertas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAlertas | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-068 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AlertaResponse | IMPLEMENTADA; evidência HTTP 29 capturas |
| API-069 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | POST | ADMIN/GESTOR/OPERADOR | DecisaoCreate | DecisaoResponse | IMPLEMENTADA; evidência HTTP 22 capturas |
| API-070 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaDecisoes | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-071 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/evidencias | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaEvidencias | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-072 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | POST | ADMIN/GESTOR/OPERADOR | IntervencaoCreate | IntervencaoResponse | IMPLEMENTADA; evidência HTTP 95 capturas |
| API-073 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaIntervencoes | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-074 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | IntervencaoResponse | IMPLEMENTADA; evidência HTTP 46 capturas |
| API-075 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | POST | Por ação: ADMIN/GESTOR; OPERADOR somente cancela SOLICITADA própria ou encerra execução própria | AcaoCreate | AcaoResponse | IMPLEMENTADA; evidência HTTP 125 capturas |
| API-076 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAcoes | IMPLEMENTADA; evidência HTTP 13 capturas |


### Campos de AcaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "AUTORIZAR",     "RECUSAR",     "INICIAR",     "ENCERRAR",     "CANCELAR",     "REGISTRAR_FALHA"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


### Campos de AnaliseCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| modo | False | ModoCalculo | {   "default": "MODO_RESTRITO" } |
| intervalo_maximo_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ],   "description": "G operacional explicito. Ausencia persiste CONFIGURACAO_INCOMPLETA, sem volumes." } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| corte_aquisicao | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "description": "Obrigatorio para sessao ativa; inclui apenas revisoes consolidadas ate este instante. Nunca futuro." } |
| revisao_aquisicao | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "minimum": 0.0     },     {       "type": "null"     }   ],   "description": "Revisao consolidada; 0 representa ausencia de aquisicao. Omissao fixa a ultima elegivel no corte." } |


### Campos de AvaliacaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| configuracao_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| corte_aquisicao | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| revisao | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| analise_etileno_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |


### Campos de ConfiguracaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| temperatura_min_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| temperatura_max_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| umidade_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| umidade_max_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| intervalo_maximo_s | True | number ou string | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| cobertura_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| exposicao_continua_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| maturacoes_aplicaveis | True | lista de EstagioMaturacao | {   "items": {     "$ref": "#/components/schemas/EstagioMaturacao"   },   "maxItems": 5,   "minItems": 1 } |
| ambiente | True | string | {   "enum": [     "TRANSPORTE_REFRIGERADO",     "LABORATORIO"   ] } |
| fundamento | True | string | {   "enum": [     "OPERACIONAL",     "EXPERIMENTAL"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 10 } |
| referencias | False | lista de string | {   "items": {     "type": "string"   },   "maxItems": 10 } |
| prioridade | False | string | {   "enum": [     "INFORMATIVO",     "ATENCAO"   ],   "default": "ATENCAO" } |


### Campos de DecisaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "RECONHECER",     "OBSERVAR",     "RESOLVER",     "DESCARTAR"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


### Campos de IntervencaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |
| duracao_planejada_s | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 86400.0,       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ],   "description": "Duracao de demonstracao, ate 24h; sem eficacia cientifica ou encerramento automatico." } |
| alerta_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| avaliacao_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| analise_etileno_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |


### Campos de SessaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| inicio | True | string / date-time | {   "format": "date-time" } |
| sensor_temperatura_id | True | string / uuid | {   "format": "uuid" } |
| sensor_umidade_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| ambiente_aquisicao | True | string | {   "enum": [     "LABORATORIO",     "TRANSPORTE_REFRIGERADO"   ] } |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| observacoes | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 2000     },     {       "type": "null"     }   ] } |


### Campos de SessaoFinalizar

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| fim | True | string / date-time | {   "format": "date-time" } |
| motivo | True | string | {   "maxLength": 2000,   "minLength": 1 } |


### Campos de SincronizacaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| origem_dados | False | string | {   "enum": [     "THINGSPEAK",     "BANCO"   ],   "default": "THINGSPEAK" } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| complementar_encerrada | False | boolean | {   "default": false } |
| justificativa | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 2000,       "minLength": 1     },     {       "type": "null"     }   ] } |
| limite_atraso_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| max_requisicoes | False | integer | {   "maximum": 32.0,   "minimum": 1.0,   "default": 16 } |


## Histórico IoT

Fixar revisão/janela; não preencher null com zero; distinguir medida_em/recebida_em/processada_em e estado da coleta.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-057 | /api/v1/monitoramentos/{sessao_id}/leituras | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | HistoricoResponse | IMPLEMENTADA; evidência HTTP 40 capturas |


## Análises científicas

Mostrar faixa potencial µL, cobertura, motivos/limitações; PARCIAL só subtotal, total null; risco NAO_AVALIADO.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-059 | /api/v1/monitoramentos/{sessao_id}/analises-etileno | POST | ADMIN/GESTOR/OPERADOR | AnaliseCreate | AnaliseResponse | IMPLEMENTADA; evidência HTTP 82 capturas |
| API-060 | /api/v1/monitoramentos/{sessao_id}/analises-etileno | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AnaliseLista | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-061 | /api/v1/monitoramentos/{sessao_id}/analises-etileno/{analise_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AnaliseResponse | IMPLEMENTADA; evidência HTTP 17 capturas |


### Campos de AnaliseCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| modo | False | ModoCalculo | {   "default": "MODO_RESTRITO" } |
| intervalo_maximo_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ],   "description": "G operacional explicito. Ausencia persiste CONFIGURACAO_INCOMPLETA, sem volumes." } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| corte_aquisicao | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "description": "Obrigatorio para sessao ativa; inclui apenas revisoes consolidadas ate este instante. Nunca futuro." } |
| revisao_aquisicao | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "minimum": 0.0     },     {       "type": "null"     }   ],   "description": "Revisao consolidada; 0 representa ausencia de aquisicao. Omissao fixa a ultima elegivel no corte." } |


## Configurações ambientais

Criar versão por sessão; perfis elevados; limites operacionais justificados, sem sugestão científica automática.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-062 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | POST | ADMIN/GESTOR | ConfiguracaoCreate | ConfiguracaoResponse | IMPLEMENTADA; evidência HTTP 80 capturas |
| API-063 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaConfiguracoes | IMPLEMENTADA; evidência HTTP 4 capturas |


### Campos de ConfiguracaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| temperatura_min_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| temperatura_max_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| umidade_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| umidade_max_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| intervalo_maximo_s | True | number ou string | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| cobertura_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| exposicao_continua_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| maturacoes_aplicaveis | True | lista de EstagioMaturacao | {   "items": {     "$ref": "#/components/schemas/EstagioMaturacao"   },   "maxItems": 5,   "minItems": 1 } |
| ambiente | True | string | {   "enum": [     "TRANSPORTE_REFRIGERADO",     "LABORATORIO"   ] } |
| fundamento | True | string | {   "enum": [     "OPERACIONAL",     "EXPERIMENTAL"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 10 } |
| referencias | False | lista de string | {   "items": {     "type": "string"   },   "maxItems": 10 } |
| prioridade | False | string | {   "enum": [     "INFORMATIVO",     "ATENCAO"   ],   "default": "ATENCAO" } |


## Avaliações preventivas

Exibir status e achados; AVALIADO não significa seguro; análise contextual opcional.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-064 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | POST | ADMIN/GESTOR/OPERADOR | AvaliacaoCreate | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 86 capturas |
| API-065 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAvaliacoes | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-066 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 8 capturas |


### Campos de AvaliacaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| configuracao_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| corte_aquisicao | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| revisao | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| analise_etileno_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |


## Central de alertas

Consulta por sessão; não há central global; nível operacional não equivale a dano fisiológico.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-067 | /api/v1/monitoramentos/{sessao_id}/alertas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAlertas | IMPLEMENTADA; evidência HTTP 7 capturas |
| API-068 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AlertaResponse | IMPLEMENTADA; evidência HTTP 29 capturas |
| API-069 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | POST | ADMIN/GESTOR/OPERADOR | DecisaoCreate | DecisaoResponse | IMPLEMENTADA; evidência HTTP 22 capturas |
| API-070 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaDecisoes | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-071 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/evidencias | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaEvidencias | IMPLEMENTADA; evidência HTTP 8 capturas |


### Campos de DecisaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "RECONHECER",     "OBSERVAR",     "RESOLVER",     "DESCARTAR"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


## Detalhes/decisões

Exibir evidências e histórico; nota OBSERVAR não altera estado; decisões exigem justificativa/chave.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-069 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | POST | ADMIN/GESTOR/OPERADOR | DecisaoCreate | DecisaoResponse | IMPLEMENTADA; evidência HTTP 22 capturas |
| API-070 | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaDecisoes | IMPLEMENTADA; evidência HTTP 6 capturas |


### Campos de DecisaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "RECONHECER",     "OBSERVAR",     "RESOLVER",     "DESCARTAR"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


## Intervenções simuladas

Solicitar/autorizar/iniciar/encerrar são ações distintas. acoes_permitidas auxilia UI, servidor revalida. Sem timer que conclui execução.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-072 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | POST | ADMIN/GESTOR/OPERADOR | IntervencaoCreate | IntervencaoResponse | IMPLEMENTADA; evidência HTTP 95 capturas |
| API-073 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaIntervencoes | IMPLEMENTADA; evidência HTTP 6 capturas |
| API-074 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | IntervencaoResponse | IMPLEMENTADA; evidência HTTP 46 capturas |
| API-075 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | POST | Por ação: ADMIN/GESTOR; OPERADOR somente cancela SOLICITADA própria ou encerra execução própria | AcaoCreate | AcaoResponse | IMPLEMENTADA; evidência HTTP 125 capturas |
| API-076 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAcoes | IMPLEMENTADA; evidência HTTP 13 capturas |


### Campos de AcaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "AUTORIZAR",     "RECUSAR",     "INICIAR",     "ENCERRAR",     "CANCELAR",     "REGISTRAR_FALHA"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


### Campos de IntervencaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |
| duracao_planejada_s | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 86400.0,       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ],   "description": "Duracao de demonstracao, ate 24h; sem eficacia cientifica ou encerramento automatico." } |
| alerta_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| avaliacao_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| analise_etileno_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |


## Histórico operacional

Históricos por recurso/sessão; não existe exportação/auditoria global HTTP. Preservar snapshots e hashes para consulta, não recomputar na tela.

Atualização sugerida: recarregar GET após mutação confirmada; polling manual ou periódico moderado para sincronização/intervenção em execução (não há push/event stream). Sem registros: renderizar estado vazio com filtros/escopo e ação de criação apenas quando permitida. Erro de autorização não é lista vazia. Desabilitar mutação para CONSULTA, contexto terminal/incompatível ou ação ausente em `acoes_permitidas`; backend permanece autoridade.

| ID / ação | Endpoint | Método | Perfil | Dados enviados / obrigatoriedade | Dados recebidos / estados | Status API |
| --- | --- | --- | --- | --- | --- | --- |
| API-003 | /api/v1/integracoes/thingspeak/status | GET | ADMIN | Path/query; sem body | ThingSpeakStatusResponse | IMPLEMENTADA; evidência HTTP 18 capturas |
| API-004 | /api/v1/integracoes/thingspeak/feeds | GET | ADMIN | Path/query; sem body | ThingSpeakMappingResult | IMPLEMENTADA; evidência HTTP 29 capturas |
| API-005 | /api/v1/integracoes/thingspeak/ultima-leitura | GET | ADMIN | Path/query; sem body | ThingSpeakFeed ou null | IMPLEMENTADA; evidência HTTP 18 capturas |
| API-006 | /api/v1/integracoes/thingspeak/sincronizar | POST | ADMIN | Path/query; sem body | ThingSpeakSyncSummary | IMPLEMENTADA; evidência HTTP 20 capturas |
| API-055 | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | POST | ADMIN/GESTOR/OPERADOR | SincronizacaoCreate | SincronizacaoResponse, SincronizacaoResponse | IMPLEMENTADA; evidência HTTP 189 capturas |
| API-056 | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | EstadoSincronizacaoResponse | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-062 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | POST | ADMIN/GESTOR | ConfiguracaoCreate | ConfiguracaoResponse | IMPLEMENTADA; evidência HTTP 80 capturas |
| API-063 | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaConfiguracoes | IMPLEMENTADA; evidência HTTP 4 capturas |
| API-064 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | POST | ADMIN/GESTOR/OPERADOR | AvaliacaoCreate | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 86 capturas |
| API-065 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAvaliacoes | IMPLEMENTADA; evidência HTTP 5 capturas |
| API-066 | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id} | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | AvaliacaoResponse | IMPLEMENTADA; evidência HTTP 8 capturas |
| API-075 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | POST | Por ação: ADMIN/GESTOR; OPERADOR somente cancela SOLICITADA própria ou encerra execução própria | AcaoCreate | AcaoResponse | IMPLEMENTADA; evidência HTTP 125 capturas |
| API-076 | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | GET | ADMIN/GESTOR/OPERADOR/CONSULTA | Path/query; sem body | ListaAcoes | IMPLEMENTADA; evidência HTTP 13 capturas |


### Campos de AcaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| acao | True | string | {   "enum": [     "AUTORIZAR",     "RECUSAR",     "INICIAR",     "ENCERRAR",     "CANCELAR",     "REGISTRAR_FALHA"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 1 } |


### Campos de AvaliacaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| configuracao_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| corte_aquisicao | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| revisao | False | integer ou null | {   "anyOf": [     {       "type": "integer",       "minimum": 0.0     },     {       "type": "null"     }   ] } |
| analise_etileno_id | False | string / uuid ou null | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ] } |


### Campos de ConfiguracaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| temperatura_min_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| temperatura_max_c | True | number ou string | {   "anyOf": [     {       "type": "number"     },     {       "type": "string"     }   ] } |
| umidade_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| umidade_max_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "minimum": 0.0     },     {       "type": "string"     }   ] } |
| intervalo_maximo_s | True | number ou string | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| cobertura_min_percentual | True | number ou string | {   "anyOf": [     {       "type": "number",       "maximum": 100.0,       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ] } |
| exposicao_continua_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| maturacoes_aplicaveis | True | lista de EstagioMaturacao | {   "items": {     "$ref": "#/components/schemas/EstagioMaturacao"   },   "maxItems": 5,   "minItems": 1 } |
| ambiente | True | string | {   "enum": [     "TRANSPORTE_REFRIGERADO",     "LABORATORIO"   ] } |
| fundamento | True | string | {   "enum": [     "OPERACIONAL",     "EXPERIMENTAL"   ] } |
| justificativa | True | string | {   "maxLength": 4000,   "minLength": 10 } |
| referencias | False | lista de string | {   "items": {     "type": "string"   },   "maxItems": 10 } |
| prioridade | False | string | {   "enum": [     "INFORMATIVO",     "ATENCAO"   ],   "default": "ATENCAO" } |


### Campos de SincronizacaoCreate

| Campo | Obrigatório | Contrato | Restrições/default |
| --- | --- | --- | --- |
| chave_idempotencia | True | string / uuid | {   "format": "uuid" } |
| origem_dados | False | string | {   "enum": [     "THINGSPEAK",     "BANCO"   ],   "default": "THINGSPEAK" } |
| inicio | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| fim | False | string / date-time ou null | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ] } |
| complementar_encerrada | False | boolean | {   "default": false } |
| justificativa | False | string ou null | {   "anyOf": [     {       "type": "string",       "maxLength": 2000,       "minLength": 1     },     {       "type": "null"     }   ] } |
| limite_atraso_s | False | number ou string ou null | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     },     {       "type": "null"     }   ] } |
| max_requisicoes | False | integer | {   "maximum": 32.0,   "minimum": 1.0,   "default": 16 } |


## Lacunas de integração

Sem CRUD HTTP de sensores/mapping, sem dashboard/agregador, sem listagem global de sessões/alertas, sem refresh/logout, sem protocolo de hardware, sem endpoint de readiness. CORS atual apenas desenvolvimento porta 5173. Snapshot OpenAPI é contrato da main auditada, não garantia de configuração do ambiente publicado. Não usar endpoints globais ThingSpeak com usuário operacional.
