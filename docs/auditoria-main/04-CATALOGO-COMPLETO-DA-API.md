# Catálogo completo da API

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Fontes e convenções

Inventário extraído de `app.routes` e `app.openapi()` em processo isolado sem conexão com banco. 76 operações OpenAPI, 50 caminhos, 84 schemas. As quatro rotas adicionais de documentação estão ao final. Autenticação não substitui autorização.

Os exemplos HTTP abaixo são capturas de testes locais desta auditoria, com credenciais removidas. IDs existem somente nas fixtures descartáveis; substituir pelos IDs da própria execução. `VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA` é marcador editorial de remoção de credencial, não valor utilizável para autenticar. Nenhum exemplo é resposta de produção. Uma captura comprova somente aquele cenário. Schemas e fontes vinculadas completam o contrato; campos abertos `dict` não são contratos rígidos.


| ID | Método | Endpoint | Módulo | Autenticação | Perfil | Finalidade | Evidência |
| --- | --- | --- | --- | --- | --- | --- | --- |
| API-001 | GET | / | root | Público | Público | Read Root | [app/api/routes/root.py:8](../../app/api/routes/root.py#L8) |
| API-002 | GET | /health | health | Público | Público | Health Check | [app/api/routes/health.py:8](../../app/api/routes/health.py#L8) |
| API-003 | GET | /api/v1/integracoes/thingspeak/status | integracoes,thingspeak | JWT Bearer | ADMIN | Diagnostico administrativo privado da integracao global | [app/modules/integracoes/thingspeak/routes.py:33](../../app/modules/integracoes/thingspeak/routes.py#L33) |
| API-004 | GET | /api/v1/integracoes/thingspeak/feeds | integracoes,thingspeak | JWT Bearer | ADMIN | Consultar leituras do canal global como ADMIN | [app/modules/integracoes/thingspeak/routes.py:39](../../app/modules/integracoes/thingspeak/routes.py#L39) |
| API-005 | GET | /api/v1/integracoes/thingspeak/ultima-leitura | integracoes,thingspeak | JWT Bearer | ADMIN | Consultar ultimo feed do canal global como ADMIN | [app/modules/integracoes/thingspeak/routes.py:49](../../app/modules/integracoes/thingspeak/routes.py#L49) |
| API-006 | POST | /api/v1/integracoes/thingspeak/sincronizar | integracoes,thingspeak | JWT Bearer | ADMIN | Sincronizacao manual administrativa do canal global | [app/modules/integracoes/thingspeak/routes.py:59](../../app/modules/integracoes/thingspeak/routes.py#L59) |
| API-007 | POST | /api/v1/auth/login | Auth | Público | Público | Login | [app/modules/auth/routes.py:12](../../app/modules/auth/routes.py#L12) |
| API-008 | GET | /api/v1/auth/me | Auth | JWT Bearer | Qualquer usuário ativo autenticado | Me | [app/modules/auth/routes.py:17](../../app/modules/auth/routes.py#L17) |
| API-009 | GET | /api/v1/perfis | Usuarios | JWT Bearer | ADMIN | Profiles | [app/api/routes/usuarios.py:13](../../app/api/routes/usuarios.py#L13) |
| API-010 | POST | /api/v1/usuarios | Usuarios | JWT Bearer | ADMIN | Create | [app/api/routes/usuarios.py:18](../../app/api/routes/usuarios.py#L18) |
| API-011 | GET | /api/v1/usuarios | Usuarios | JWT Bearer | ADMIN | Users | [app/api/routes/usuarios.py:23](../../app/api/routes/usuarios.py#L23) |
| API-012 | GET | /api/v1/usuarios/{usuario_id} | Usuarios | JWT Bearer | ADMIN | Detail | [app/api/routes/usuarios.py:28](../../app/api/routes/usuarios.py#L28) |
| API-013 | PATCH | /api/v1/usuarios/{usuario_id} | Usuarios | JWT Bearer | ADMIN | Update | [app/api/routes/usuarios.py:33](../../app/api/routes/usuarios.py#L33) |
| API-014 | POST | /api/v1/empresas | Empresas | JWT Bearer | ADMIN | Create | [app/modules/empresas/routes.py:16](../../app/modules/empresas/routes.py#L16) |
| API-015 | GET | /api/v1/empresas | Empresas | JWT Bearer | Usuário ativo autenticado | Companies | [app/modules/empresas/routes.py:21](../../app/modules/empresas/routes.py#L21) |
| API-016 | GET | /api/v1/empresas/{empresa_id} | Empresas | JWT Bearer | Usuário ativo autenticado | Detail | [app/modules/empresas/routes.py:26](../../app/modules/empresas/routes.py#L26) |
| API-017 | PATCH | /api/v1/empresas/{empresa_id} | Empresas | JWT Bearer | ADMIN | Update | [app/modules/empresas/routes.py:31](../../app/modules/empresas/routes.py#L31) |
| API-018 | POST | /api/v1/empresas/{empresa_id}/usuarios/{usuario_id} | Empresas | JWT Bearer | ADMIN | Link | [app/modules/empresas/routes.py:36](../../app/modules/empresas/routes.py#L36) |
| API-019 | GET | /api/v1/empresas/{empresa_id}/usuarios | Empresas | JWT Bearer | ADMIN/GESTOR | Users | [app/modules/empresas/routes.py:41](../../app/modules/empresas/routes.py#L41) |
| API-020 | POST | /api/v1/produtos | Produtos | JWT Bearer | ADMIN | Create | [app/modules/produtos/routes.py:18](../../app/modules/produtos/routes.py#L18) |
| API-021 | GET | /api/v1/produtos | Produtos | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Products | [app/modules/produtos/routes.py:23](../../app/modules/produtos/routes.py#L23) |
| API-022 | GET | /api/v1/produtos/{produto_id} | Produtos | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get | [app/modules/produtos/routes.py:29](../../app/modules/produtos/routes.py#L29) |
| API-023 | PATCH | /api/v1/produtos/{produto_id} | Produtos | JWT Bearer | ADMIN | Update | [app/modules/produtos/routes.py:34](../../app/modules/produtos/routes.py#L34) |
| API-024 | POST | /api/v1/produtos/{produto_id}/parametros | Produtos | JWT Bearer | ADMIN | Create Parameter | [app/modules/produtos/routes.py:39](../../app/modules/produtos/routes.py#L39) |
| API-025 | GET | /api/v1/produtos/{produto_id}/parametros | Produtos | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Parameters | [app/modules/produtos/routes.py:44](../../app/modules/produtos/routes.py#L44) |
| API-026 | PATCH | /api/v1/produtos/{produto_id}/parametros/{parametro_id} | Produtos | JWT Bearer | ADMIN | Update Parameter | [app/modules/produtos/routes.py:50](../../app/modules/produtos/routes.py#L50) |
| API-027 | POST | /api/v1/veiculos | Logistica | JWT Bearer | ADMIN/GESTOR | Create Veiculos | [app/modules/logistica/routes.py:24](../../app/modules/logistica/routes.py#L24) |
| API-028 | GET | /api/v1/veiculos | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | List Veiculos | [app/modules/logistica/routes.py:29](../../app/modules/logistica/routes.py#L29) |
| API-029 | GET | /api/v1/veiculos/{veiculo_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get Veiculos | [app/modules/logistica/routes.py:39](../../app/modules/logistica/routes.py#L39) |
| API-030 | PATCH | /api/v1/veiculos/{veiculo_id} | Logistica | JWT Bearer | ADMIN/GESTOR | Update Veiculos | [app/modules/logistica/routes.py:44](../../app/modules/logistica/routes.py#L44) |
| API-031 | POST | /api/v1/motoristas | Logistica | JWT Bearer | ADMIN/GESTOR | Create Motoristas | [app/modules/logistica/routes.py:49](../../app/modules/logistica/routes.py#L49) |
| API-032 | GET | /api/v1/motoristas | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | List Motoristas | [app/modules/logistica/routes.py:54](../../app/modules/logistica/routes.py#L54) |
| API-033 | GET | /api/v1/motoristas/{motorista_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get Motoristas | [app/modules/logistica/routes.py:64](../../app/modules/logistica/routes.py#L64) |
| API-034 | PATCH | /api/v1/motoristas/{motorista_id} | Logistica | JWT Bearer | ADMIN/GESTOR | Update Motoristas | [app/modules/logistica/routes.py:69](../../app/modules/logistica/routes.py#L69) |
| API-035 | POST | /api/v1/viagens | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Create Viagens | [app/modules/logistica/routes.py:74](../../app/modules/logistica/routes.py#L74) |
| API-036 | GET | /api/v1/viagens | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | List Viagens | [app/modules/logistica/routes.py:79](../../app/modules/logistica/routes.py#L79) |
| API-037 | GET | /api/v1/viagens/{viagem_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get Viagens | [app/modules/logistica/routes.py:91](../../app/modules/logistica/routes.py#L91) |
| API-038 | PATCH | /api/v1/viagens/{viagem_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Update Viagens | [app/modules/logistica/routes.py:96](../../app/modules/logistica/routes.py#L96) |
| API-039 | POST | /api/v1/viagens/{viagem_id}/cargas | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Create Carga | [app/modules/logistica/routes.py:101](../../app/modules/logistica/routes.py#L101) |
| API-040 | GET | /api/v1/viagens/{viagem_id}/cargas | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | List Cargas | [app/modules/logistica/routes.py:106](../../app/modules/logistica/routes.py#L106) |
| API-041 | GET | /api/v1/cargas/{carga_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get Carga | [app/modules/logistica/routes.py:113](../../app/modules/logistica/routes.py#L113) |
| API-042 | PATCH | /api/v1/cargas/{carga_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Update Carga | [app/modules/logistica/routes.py:118](../../app/modules/logistica/routes.py#L118) |
| API-043 | POST | /api/v1/cargas/{carga_id}/caixas | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Create Caixa | [app/modules/logistica/routes.py:123](../../app/modules/logistica/routes.py#L123) |
| API-044 | GET | /api/v1/cargas/{carga_id}/caixas | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | List Caixas | [app/modules/logistica/routes.py:128](../../app/modules/logistica/routes.py#L128) |
| API-045 | GET | /api/v1/caixas/{caixa_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Get Caixa | [app/modules/logistica/routes.py:134](../../app/modules/logistica/routes.py#L134) |
| API-046 | PATCH | /api/v1/caixas/{caixa_id} | Logistica | JWT Bearer | ADMIN/GESTOR/OPERADOR | Update Caixa | [app/modules/logistica/routes.py:139](../../app/modules/logistica/routes.py#L139) |
| API-047 | PUT | /api/v1/cargas/{carga_id}/monitoramento | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR | Declarar ou substituir os dados adicionais da carga | [app/modules/monitoramento/routes.py:28](../../app/modules/monitoramento/routes.py#L28) |
| API-048 | GET | /api/v1/cargas/{carga_id}/monitoramento | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar os dados adicionais de monitoramento | [app/modules/monitoramento/routes.py:39](../../app/modules/monitoramento/routes.py#L39) |
| API-049 | POST | /api/v1/cargas/{carga_id}/monitoramentos | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR | Iniciar uma sessao com janela efetiva explicita | [app/modules/monitoramento/routes.py:45](../../app/modules/monitoramento/routes.py#L45) |
| API-050 | GET | /api/v1/cargas/{carga_id}/monitoramentos | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar sessoes da carga com paginacao | [app/modules/monitoramento/routes.py:60](../../app/modules/monitoramento/routes.py#L60) |
| API-051 | GET | /api/v1/viagens/{viagem_id}/monitoramentos | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar sessoes da viagem com paginacao | [app/modules/monitoramento/routes.py:67](../../app/modules/monitoramento/routes.py#L67) |
| API-052 | GET | /api/v1/monitoramentos/{sessao_id} | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar a sessao e seu snapshot de rastreabilidade | [app/modules/monitoramento/routes.py:74](../../app/modules/monitoramento/routes.py#L74) |
| API-053 | POST | /api/v1/monitoramentos/{sessao_id}/encerrar | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR | Encerrar uma sessao ativa, com horario e motivo | [app/modules/monitoramento/routes.py:80](../../app/modules/monitoramento/routes.py#L80) |
| API-054 | POST | /api/v1/monitoramentos/{sessao_id}/cancelar | Monitoramento ambiental | JWT Bearer | ADMIN/GESTOR/OPERADOR | Cancelar uma sessao ativa, sem apagar sua janela historica | [app/modules/monitoramento/routes.py:87](../../app/modules/monitoramento/routes.py#L87) |
| API-055 | POST | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | Historico IoT | JWT Bearer | ADMIN/GESTOR/OPERADOR | Sincronizar explicitamente o historico de uma sessao | [app/modules/monitoramento/historico_routes.py:32](../../app/modules/monitoramento/historico_routes.py#L32) |
| API-056 | GET | /api/v1/monitoramentos/{sessao_id}/sincronizacoes | Historico IoT | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar estado e tentativas de sincronizacao | [app/modules/monitoramento/historico_routes.py:48](../../app/modules/monitoramento/historico_routes.py#L48) |
| API-057 | GET | /api/v1/monitoramentos/{sessao_id}/leituras | Historico IoT | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar leituras e marcadores invalidos em ordem cronologica | [app/modules/monitoramento/historico_routes.py:54](../../app/modules/monitoramento/historico_routes.py#L54) |
| API-058 | GET | /api/v1/monitoramentos/{sessao_id}/qualidade | Historico IoT | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar lacunas e cobertura temporal, sem estimativa de etileno | [app/modules/monitoramento/historico_routes.py:67](../../app/modules/monitoramento/historico_routes.py#L67) |
| API-059 | POST | /api/v1/monitoramentos/{sessao_id}/analises-etileno | Analises de etileno | JWT Bearer | ADMIN/GESTOR/OPERADOR | Calcular e persistir producao potencial com o motor cientifico existente | [app/modules/monitoramento/analises_routes.py:18](../../app/modules/monitoramento/analises_routes.py#L18) |
| API-060 | GET | /api/v1/monitoramentos/{sessao_id}/analises-etileno | Analises de etileno | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar analises preservadas da sessao | [app/modules/monitoramento/analises_routes.py:31](../../app/modules/monitoramento/analises_routes.py#L31) |
| API-061 | GET | /api/v1/monitoramentos/{sessao_id}/analises-etileno/{analise_id} | Analises de etileno | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar resultado e entradas fixados, sem recalcular | [app/modules/monitoramento/analises_routes.py:36](../../app/modules/monitoramento/analises_routes.py#L36) |
| API-062 | POST | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR | Registrar versao imutavel de parametros operacionais | [app/modules/monitoramento/preventivo_routes.py:20](../../app/modules/monitoramento/preventivo_routes.py#L20) |
| API-063 | GET | /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar versoes da configuracao operacional | [app/modules/monitoramento/preventivo_routes.py:26](../../app/modules/monitoramento/preventivo_routes.py#L26) |
| API-064 | POST | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR | Avaliar dados ambientais e registrar alertas explicaveis | [app/modules/monitoramento/preventivo_routes.py:31](../../app/modules/monitoramento/preventivo_routes.py#L31) |
| API-065 | GET | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar avaliacoes imutaveis | [app/modules/monitoramento/preventivo_routes.py:42](../../app/modules/monitoramento/preventivo_routes.py#L42) |
| API-066 | GET | /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id} | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar snapshot e resultado sem reavaliar | [app/modules/monitoramento/preventivo_routes.py:47](../../app/modules/monitoramento/preventivo_routes.py#L47) |
| API-067 | GET | /api/v1/monitoramentos/{sessao_id}/alertas | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar alertas operacionais da sessao | [app/modules/monitoramento/preventivo_routes.py:52](../../app/modules/monitoramento/preventivo_routes.py#L52) |
| API-068 | GET | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id} | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar alerta ambiental | [app/modules/monitoramento/preventivo_routes.py:58](../../app/modules/monitoramento/preventivo_routes.py#L58) |
| API-069 | POST | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR | Reconhecer, observar, resolver ou descartar com justificativa | [app/modules/monitoramento/preventivo_routes.py:63](../../app/modules/monitoramento/preventivo_routes.py#L63) |
| API-070 | GET | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar historico auditavel de decisoes | [app/modules/monitoramento/preventivo_routes.py:73](../../app/modules/monitoramento/preventivo_routes.py#L73) |
| API-071 | GET | /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/evidencias | Monitoramento preventivo | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar evidencias e avaliacoes que sustentam o alerta | [app/modules/monitoramento/preventivo_routes.py:78](../../app/modules/monitoramento/preventivo_routes.py#L78) |
| API-072 | POST | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | Exaustao exclusivamente simulada | JWT Bearer | ADMIN/GESTOR/OPERADOR | Solicitar intervencao virtual com justificativa humana | [app/modules/monitoramento/exaustao_routes.py:19](../../app/modules/monitoramento/exaustao_routes.py#L19) |
| API-073 | GET | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas | Exaustao exclusivamente simulada | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Listar intervencoes da sessao | [app/modules/monitoramento/exaustao_routes.py:29](../../app/modules/monitoramento/exaustao_routes.py#L29) |
| API-074 | GET | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id} | Exaustao exclusivamente simulada | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar estado logico e permissoes atuais | [app/modules/monitoramento/exaustao_routes.py:34](../../app/modules/monitoramento/exaustao_routes.py#L34) |
| API-075 | POST | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | Exaustao exclusivamente simulada | JWT Bearer | Por ação: ADMIN/GESTOR; OPERADOR somente cancela SOLICITADA própria ou encerra execução própria | Registrar decisao humana ou transicao virtual | [app/modules/monitoramento/exaustao_routes.py:43](../../app/modules/monitoramento/exaustao_routes.py#L43) |
| API-076 | GET | /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes | Exaustao exclusivamente simulada | JWT Bearer | ADMIN/GESTOR/OPERADOR/CONSULTA | Consultar trilha ordenada de decisoes e transicoes | [app/modules/monitoramento/exaustao_routes.py:53](../../app/modules/monitoramento/exaustao_routes.py#L53) |


## API-001 — GET /

Read Root

- Router/handler: [app/api/routes/root.py:8](../../app/api/routes/root.py#L8) · `read_root` · operationId `read_root__get`.
- Perfil: Público.
- Escopo: Não se aplica.
- Headers: sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | object; Successful Response |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "running",
    }

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_health.py](../../tests/test_health.py) `test_root`.

Caminho concreto da fixture: `GET /`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "service": "chicosense-api",
  "status": "running"
}
```

Cenário negativo a verificar: parâmetros/body inválidos quando declarados → 422; em operação privada, JWT ausente/inválido → 401. Isso é uma recomendação de teste, não uma captura desta operação.

Matriz de respostas observadas: 200.

Testes HTTP que atingiram esta rota:
[tests/test_health.py](../../tests/test_health.py) `test_root`

## API-002 — GET /health

Health Check

- Router/handler: [app/api/routes/health.py:8](../../app/api/routes/health.py#L8) · `health_check` · operationId `health_check_health_get`.
- Perfil: Público.
- Escopo: Não se aplica.
- Headers: sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | object; Successful Response |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_health.py](../../tests/test_health.py) `test_health_check`.

Caminho concreto da fixture: `GET /health`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "status": "ok",
  "service": "chicosense-api"
}
```

Cenário negativo a verificar: parâmetros/body inválidos quando declarados → 422; em operação privada, JWT ausente/inválido → 401. Isso é uma recomendação de teste, não uma captura desta operação.

Matriz de respostas observadas: 200.

Testes HTTP que atingiram esta rota:
[tests/test_health.py](../../tests/test_health.py) `test_health_check`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`

## API-003 — GET /api/v1/integracoes/thingspeak/status

Diagnostico administrativo privado da integracao global

- Router/handler: [app/modules/integracoes/thingspeak/routes.py:33](../../app/modules/integracoes/thingspeak/routes.py#L33) · `get_status` · operationId `get_status_api_v1_integracoes_thingspeak_status_get`.
- Perfil: ADMIN.
- Escopo: Canal global configurado no servidor; sem propriedade empresarial persistida.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ThingSpeakStatusResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN. |
| 503 | ; Configuracao insegura/invalida ou indisponibilidade da integracao. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "http_service",
    "module": "app.modules.integracoes.thingspeak.routes",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/status',response_model=ThingSpeakStatusResponse,
    summary='Diagnostico administrativo privado da integracao global')
def get_status(service:ThingSpeakService=Depends(http_service)):
    return safe_response(service.get_status(),service)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`.

Caminho concreto da fixture: `GET /api/v1/integracoes/thingspeak/status`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "configured": true,
  "base_url": "https://api.thingspeak.com",
  "channel_id": "12345",
  "message": "ThingSpeak channel configured."
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 503.

Testes HTTP que atingiram esta rota:
[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[expired]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[inactive]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_configuration_parse_failure_never_exposes_values`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[CONSULTA]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[GESTOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OPERADOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OUTRO]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_missing_channel_remains_private_diagnostic_and_queries_fail_generically`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_private_global_endpoints_preserve_shared_http_log_protection`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[file:///etc/example]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com#FAKE_TOKEN]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com:invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com?api_key=FAKE]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://user:FAKE_PASSWORD@example.invalid]`

## API-004 — GET /api/v1/integracoes/thingspeak/feeds

Consultar leituras do canal global como ADMIN

Nao e uma consulta por transportadora. Para operacao no escopo empresarial, usar historico por sessao.

- Router/handler: [app/modules/integracoes/thingspeak/routes.py:39](../../app/modules/integracoes/thingspeak/routes.py#L39) · `get_feeds` · operationId `get_feeds_api_v1_integracoes_thingspeak_feeds_get`.
- Perfil: ADMIN.
- Escopo: Canal global configurado no servidor; sem propriedade empresarial persistida.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | results | False | {   "anyOf": [     {       "type": "integer",       "maximum": 8000,       "minimum": 1     },     {       "type": "null"     }   ],   "default": 10,   "title": "Results" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ThingSpeakMappingResult; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN. |
| 503 | ; Configuracao insegura/invalida ou indisponibilidade da integracao. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "http_service",
    "module": "app.modules.integracoes.thingspeak.routes",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/feeds',response_model=ThingSpeakMappingResult,
    summary='Consultar leituras do canal global como ADMIN')
async def get_feeds(results:int|None=Query(default=10,ge=1,le=8000),service:ThingSpeakService=Depends(http_service)):
    """Nao e uma consulta por transportadora. Para operacao no escopo empresarial, usar historico por sessao."""
    try:
        return safe_response(await service.get_mapped_feeds(results=results),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`.

Caminho concreto da fixture: `GET /api/v1/integracoes/thingspeak/feeds`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "channel_id": "12345",
  "feeds_processados": 1,
  "leituras_normalizadas": [
    {
      "source": "thingspeak",
      "channel_id": "12345",
      "entry_id": 12,
      "field_name": "field4",
      "created_at": "2026-11-23T10:54:05.435676Z",
      "sensor_id": "e74191b3-f28d-4119-bb50-9ac9503f48c7",
      "tipo": "TEMPERATURA",
      "contexto": "AMBIENTE",
      "valor": "13",
      "unidade": "C",
      "viagem_id": null,
      "carga_id": null,
      "caixa_id": null,
      "valor_original": "13",
      "ignorada": false,
      "motivo_ignorada": null
    },
    {
      "source": "thingspeak",
      "channel_id": "12345",
      "entry_id": 12,
      "field_name": "field7",
      "created_at": "2026-11-23T10:54:05.435676Z",
      "sensor_id": "d590105d-7f56-413c-bcba-d36438f90db5",
      "tipo": "UMIDADE",
      "contexto": "AMBIENTE",
      "valor": "92",
      "unidade": "%",
      "viagem_id": null,
      "carga_id": null,
      "caixa_id": null,
      "valor_original": "92",
      "ignorada": false,
      "motivo_ignorada": null
    }
  ],
  "ignorados": 0
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 400, 401, 403, 429, 500, 502, 503, 504.

Testes HTTP que atingiram esta rota:
[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[expired]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[inactive]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_configured_channel_cannot_inject_path_or_parameters[0]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_configured_channel_cannot_inject_path_or_parameters[12345/../other]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_configured_channel_cannot_inject_path_or_parameters[12345?api_key=FAKE]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_configured_channel_cannot_inject_path_or_parameters[abc]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[CONSULTA]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[GESTOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OPERADOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OUTRO]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_known_secret_in_original_field_is_sanitized_on_copy`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_missing_channel_remains_private_diagnostic_and_queries_fail_generically`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_private_global_endpoints_preserve_shared_http_log_protection`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[file:///etc/example]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com#FAKE_TOKEN]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com:invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com?api_key=FAKE]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://user:FAKE_PASSWORD@example.invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc0-400]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc1-503]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc2-504]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc3-429]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc4-502]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_upstream_error_messages_are_not_echoed[exc5-500]`

## API-005 — GET /api/v1/integracoes/thingspeak/ultima-leitura

Consultar ultimo feed do canal global como ADMIN

Campos raw adicionais nao documentados sao omitidos por seguranca; servicos internos preservam o original.

- Router/handler: [app/modules/integracoes/thingspeak/routes.py:49](../../app/modules/integracoes/thingspeak/routes.py#L49) · `get_latest_feed` · operationId `get_latest_feed_api_v1_integracoes_thingspeak_ultima_leitura_get`.
- Perfil: ADMIN.
- Escopo: Canal global configurado no servidor; sem propriedade empresarial persistida.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ThingSpeakFeed ou null; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN. |
| 503 | ; Configuracao insegura/invalida ou indisponibilidade da integracao. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "http_service",
    "module": "app.modules.integracoes.thingspeak.routes",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/ultima-leitura',response_model=ThingSpeakFeed|None,
    summary='Consultar ultimo feed do canal global como ADMIN')
async def get_latest_feed(service:ThingSpeakService=Depends(http_service)):
    """Campos raw adicionais nao documentados sao omitidos por seguranca; servicos internos preservam o original."""
    try:
        return safe_latest(await service.get_latest_feed(),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`.

Caminho concreto da fixture: `GET /api/v1/integracoes/thingspeak/ultima-leitura`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "created_at": "2026-11-23T10:54:05.435676Z",
  "entry_id": 12,
  "fields": {
    "field4": "13",
    "field7": "92"
  },
  "raw": {
    "entry_id": 12,
    "created_at": "2026-11-23T10:54:05.435676+00:00",
    "field4": "13",
    "field7": "92"
  }
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 400, 401, 403, 503.

Testes HTTP que atingiram esta rota:
[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_last_reading_still_returns_null_when_no_feed`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_queries_preserve_dtos_and_sanitize_last_feed_without_mutation`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[expired]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[inactive]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[CONSULTA]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[GESTOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OPERADOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OUTRO]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_missing_channel_remains_private_diagnostic_and_queries_fail_generically`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_private_global_endpoints_preserve_shared_http_log_protection`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[file:///etc/example]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com#FAKE_TOKEN]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com:invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com?api_key=FAKE]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://user:FAKE_PASSWORD@example.invalid]`

## API-006 — POST /api/v1/integracoes/thingspeak/sincronizar

Sincronizacao manual administrativa do canal global

Escrita global apenas por ADMIN; nao concede associacao a sessoes nem dispensa os controles do historico IoT.

- Router/handler: [app/modules/integracoes/thingspeak/routes.py:59](../../app/modules/integracoes/thingspeak/routes.py#L59) · `sincronizar_feeds` · operationId `sincronizar_feeds_api_v1_integracoes_thingspeak_sincronizar_post`.
- Perfil: ADMIN.
- Escopo: Canal global configurado no servidor; sem propriedade empresarial persistida.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | results | False | {   "anyOf": [     {       "type": "integer",       "maximum": 8000,       "minimum": 1     },     {       "type": "null"     }   ],   "default": 100,   "title": "Results" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ThingSpeakSyncSummary; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN. |
| 503 | ; Configuracao insegura/invalida ou indisponibilidade da integracao. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  },
  {
    "call": "http_service",
    "module": "app.modules.integracoes.thingspeak.routes",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/sincronizar',response_model=ThingSpeakSyncSummary,
    summary='Sincronizacao manual administrativa do canal global')
async def sincronizar_feeds(results:int|None=Query(default=100,ge=1,le=8000),
    db:Session=Depends(get_database_session),service:ThingSpeakService=Depends(http_service)):
    """Escrita global apenas por ADMIN; nao concede associacao a sessoes nem dispensa os controles do historico IoT."""
    try:
        return safe_response(await service.sincronizar_feeds(db=db,results=results),service)
    except ThingSpeakError as exc:
        _raise_http_error(exc)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(503,'ThingSpeak synchronization persistence failed.') from None

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_sync_uses_real_deduplication_and_internal_services_need_no_http_token`.

Caminho concreto da fixture: `POST /api/v1/integracoes/thingspeak/sincronizar`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "feeds_recebidos": 1,
  "fields_processados": 2,
  "medicoes_criadas": 2,
  "duplicados": 0,
  "ignorados": 0,
  "erros": []
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 400, 401, 403, 503.

Testes HTTP que atingiram esta rota:
[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_admin_sync_uses_real_deduplication_and_internal_services_need_no_http_token`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[expired]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[inactive]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_all_global_operations_require_valid_active_jwt_before_factory[missing]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[CONSULTA]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[GESTOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OPERADOR]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_global_channel_denies_non_admin_even_if_sensor_belongs_to_user[OUTRO]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_missing_channel_remains_private_diagnostic_and_queries_fail_generically`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_private_global_endpoints_preserve_shared_http_log_protection`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_sync_persistence_failure_rolls_back_without_connection_details`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[file:///etc/example]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com#FAKE_TOKEN]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com:invalid]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://api.thingspeak.com?api_key=FAKE]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_unsafe_base_url_rejected_without_network_or_value_in_response[https://user:FAKE_PASSWORD@example.invalid]`<br>[tests/test_thingspeak_sync.py](../../tests/test_thingspeak_sync.py) `test_sync_endpoint_returns_summary_and_does_not_expose_api_key`

## API-007 — POST /api/v1/auth/login

Login

- Router/handler: [app/modules/auth/routes.py:12](../../app/modules/auth/routes.py#L12) · `login` · operationId `login_api_v1_auth_login_post`.
- Perfil: Público.
- Escopo: Não se aplica.
- Headers: `Content-Type: application/json`.
- Body: obrigatório; application/json: LoginRequest.
- Efeito: Lê usuário/hash e emite JWT; não persiste sessão de login.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | TokenResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_database_session)):
    return AuthService(db).login(data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_valid_login`.

Caminho concreto da fixture: `POST /api/v1/auth/login`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "email": "ADMIN@EXAMPLE.COM",
  "senha": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA"
}
```

Resposta capturada:

```json
{
  "access_token": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA",
  "token_type": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA",
  "expires_in": 1800
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_login[missing@example.com-test-only-password-123]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_login`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_login[admin@example.com-wrong]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_login[missing@example.com-test-only-password-123]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_placeholder_key_rejected`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_valid_login`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_validation_errors_and_cors_do_not_expose_request_secrets`

## API-008 — GET /api/v1/auth/me

Me

- Router/handler: [app/modules/auth/routes.py:17](../../app/modules/auth/routes.py#L17) · `me` · operationId `me_api_v1_auth_me_get`.
- Perfil: Qualquer usuário ativo autenticado.
- Escopo: Descreve somente a identidade do JWT; não exige papel específico.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CurrentUserResponse; Successful Response |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "get_current_user",
    "module": "app.api.deps",
    "children": [
      {
        "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
        "module": "fastapi.security.http",
        "children": []
      },
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/me", response_model=CurrentUserResponse)
def me(user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return AuthService(db).describe(user)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`.

Caminho concreto da fixture: `GET /api/v1/auth/me`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "cd25c23b-894b-4fc2-9044-e344c61eec7f",
  "nome": "Leitor",
  "email": "reader@example.com",
  "perfil_id": "79678237-b569-4f03-8999-c4ae78447f66",
  "ativo": true,
  "created_at": "2026-11-23T14:55:06",
  "updated_at": "2026-11-23T14:55:06",
  "perfil": "CONSULTA",
  "empresas": [
    {
      "id": "17f9b705-7302-4e0e-9c25-0f23194356ab",
      "nome": "Empresa teste",
      "tipo": "TRANSPORTADORA",
      "documento": null,
      "ativo": true,
      "created_at": "2026-11-23T14:55:06",
      "updated_at": "2026-11-23T14:55:06"
    },
    {
      "id": "ebcdbebf-94d4-447c-bf19-f5987da64d88",
      "nome": "Empresa teste",
      "tipo": "PRODUTOR",
      "documento": null,
      "ativo": true,
      "created_at": "2026-11-23T14:55:06",
      "updated_at": "2026-11-23T14:55:06"
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_login`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_login`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_membership`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[algorithm]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[audience]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[expired]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[missing]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[subject]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[tampered]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_jwt[type]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_without_token`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## API-009 — GET /api/v1/perfis

Profiles

- Router/handler: [app/api/routes/usuarios.py:13](../../app/api/routes/usuarios.py#L13) · `profiles` · operationId `profiles_api_v1_perfis_get`.
- Perfil: ADMIN.
- Escopo: Catálogo administrativo global.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de PerfilResponse; Successful Response |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/perfis", response_model=list[PerfilResponse])
def profiles(db: Session = Depends(get_database_session)):
    return UsuarioService(db).profiles_list()

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`.

Caminho concreto da fixture: `GET /api/v1/perfis`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "8ee366de-9bfd-402c-b429-5af1e02c1d02",
    "nome": "ADMIN",
    "descricao": null
  },
  {
    "id": "400f653a-b221-43a3-b0ad-adabda7ffb13",
    "nome": "CONSULTA",
    "descricao": null
  },
  {
    "id": "5aa845c2-ecec-4e73-a663-9aa56fc8ce34",
    "nome": "GESTOR",
    "descricao": null
  },
  {
    "id": "676522eb-bfec-4716-a970-04533668c8b9",
    "nome": "OPERADOR",
    "descricao": null
  }
]
```

Cenário negativo a verificar: parâmetros/body inválidos quando declarados → 422; em operação privada, JWT ausente/inválido → 401. Isso é uma recomendação de teste, não uma captura desta operação.

Matriz de respostas observadas: 200.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`

## API-010 — POST /api/v1/usuarios

Create

- Router/handler: [app/api/routes/usuarios.py:18](../../app/api/routes/usuarios.py#L18) · `create` · operationId `create_api_v1_usuarios_post`.
- Perfil: ADMIN.
- Escopo: Administração global de usuários.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: UsuarioCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | UsuarioResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def create(data: UsuarioCreate, db: Session = Depends(get_database_session)):
    return UsuarioService(db).create(data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_create_user`.

Caminho concreto da fixture: `POST /api/v1/usuarios`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome": "Gestor",
  "email": " GESTOR@EXAMPLE.COM ",
  "senha": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA",
  "perfil_id": "ebc97e30-5f8f-4c66-b65d-3d88cdd39c9b"
}
```

Resposta capturada:

```json
{
  "id": "7206dc9d-b26b-4d6a-803c-b3cf5af2bf6c",
  "nome": "Gestor",
  "email": "gestor@example.com",
  "perfil_id": "ebc97e30-5f8f-4c66-b65d-3d88cdd39c9b",
  "ativo": true,
  "created_at": "2026-11-23T14:54:57",
  "updated_at": "2026-11-23T14:54:57"
}
```

Cenário negativo comprovado: HTTP 409, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_email_unique`.

```json
{
  "detail": "Email ja cadastrado."
}
```

Matriz de respostas observadas: 201, 404, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_create_user`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_email_unique`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_missing_profile`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_validation_does_not_expose_password`

## API-011 — GET /api/v1/usuarios

Users

- Router/handler: [app/api/routes/usuarios.py:23](../../app/api/routes/usuarios.py#L23) · `users` · operationId `users_api_v1_usuarios_get`.
- Perfil: ADMIN.
- Escopo: Administração global de usuários.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de UsuarioResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/usuarios", response_model=list[UsuarioResponse])
def users(offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_database_session)):
    return UsuarioService(db).list(offset, limit)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`.

Caminho concreto da fixture: `GET /api/v1/usuarios`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "68645a85-7655-4b7b-8c68-9c216277f3d0",
    "nome": "Admin",
    "email": "admin@example.com",
    "perfil_id": "8ee366de-9bfd-402c-b429-5af1e02c1d02",
    "ativo": true,
    "created_at": "2026-11-23T14:55:10",
    "updated_at": "2026-11-23T14:55:10"
  }
]
```

Cenário negativo comprovado: HTTP 403, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[GESTOR]`.

```json
{
  "detail": "Perfil sem permissao."
}
```

Matriz de respostas observadas: 200, 403.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[CONSULTA]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[GESTOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[OPERADOR]`

## API-012 — GET /api/v1/usuarios/{usuario_id}

Detail

- Router/handler: [app/api/routes/usuarios.py:28](../../app/api/routes/usuarios.py#L28) · `detail` · operationId `detail_api_v1_usuarios__usuario_id__get`.
- Perfil: ADMIN.
- Escopo: Administração global de usuários.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | usuario_id | True | {   "type": "string",   "format": "uuid",   "title": "Usuario Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | UsuarioResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def detail(usuario_id: UUID, db: Session = Depends(get_database_session)):
    return UsuarioService(db).get(usuario_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`.

Caminho concreto da fixture: `GET /api/v1/usuarios/68645a85-7655-4b7b-8c68-9c216277f3d0`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "68645a85-7655-4b7b-8c68-9c216277f3d0",
  "nome": "Admin",
  "email": "admin@example.com",
  "perfil_id": "8ee366de-9bfd-402c-b429-5af1e02c1d02",
  "ativo": true,
  "created_at": "2026-11-23T14:55:10",
  "updated_at": "2026-11-23T14:55:10"
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_missing_records`.

```json
{
  "detail": "Usuario nao encontrado."
}
```

Matriz de respostas observadas: 200, 404.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_missing_records`

## API-013 — PATCH /api/v1/usuarios/{usuario_id}

Update

- Router/handler: [app/api/routes/usuarios.py:33](../../app/api/routes/usuarios.py#L33) · `update` · operationId `update_api_v1_usuarios__usuario_id__patch`.
- Perfil: ADMIN.
- Escopo: Administração global de usuários.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: UsuarioUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | usuario_id | True | {   "type": "string",   "format": "uuid",   "title": "Usuario Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | UsuarioResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def update(usuario_id: UUID, data: UsuarioUpdate, db: Session = Depends(get_database_session)):
    return UsuarioService(db).update(usuario_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_logical_deactivation`.

Caminho concreto da fixture: `PATCH /api/v1/usuarios/6b708d7a-834c-435a-a30f-80fd2383a71c`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "ativo": false
}
```

Resposta capturada:

```json
{
  "id": "6b708d7a-834c-435a-a30f-80fd2383a71c",
  "nome": "Leitor",
  "email": "reader@example.com",
  "perfil_id": "5cd5fd87-6bcc-469c-ada5-f382fe5007e5",
  "ativo": false,
  "created_at": "2026-11-23T14:55:11",
  "updated_at": "2026-11-23T14:55:11"
}
```

Cenário negativo comprovado: HTTP 403, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[GESTOR]`.

```json
{
  "detail": "Perfil sem permissao."
}
```

Matriz de respostas observadas: 200, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_duplicate_email_update`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_logical_deactivation`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[CONSULTA]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[GESTOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[OPERADOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_patch_explicit_null_rejected`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_patch_user_password_email`

## API-014 — POST /api/v1/empresas

Create

- Router/handler: [app/modules/empresas/routes.py:16](../../app/modules/empresas/routes.py#L16) · `create` · operationId `create_api_v1_empresas_post`.
- Perfil: ADMIN.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: EmpresaCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | EmpresaResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("", response_model=EmpresaResponse, status_code=201, dependencies=[Depends(admin)])
def create(data: EmpresaCreate, db: Session = Depends(get_database_session)):
    return EmpresaService(db).create(data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`.

Caminho concreto da fixture: `POST /api/v1/empresas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome": "Empresa teste",
  "tipo": "PRODUTOR"
}
```

Resposta capturada:

```json
{
  "id": "ebcdbebf-94d4-447c-bf19-f5987da64d88",
  "nome": "Empresa teste",
  "tipo": "PRODUTOR",
  "documento": null,
  "ativo": true,
  "created_at": "2026-11-23T14:55:06",
  "updated_at": "2026-11-23T14:55:06"
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_company_type`.

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": [
        "body",
        "tipo"
      ],
      "msg": "Input should be 'PRODUTOR', 'TRANSPORTADORA' or 'CLIENTE'"
    }
  ]
}
```

Matriz de respostas observadas: 201, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_types[CLIENTE]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_types[PRODUTOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_types[TRANSPORTADORA]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_membership`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_invalid_company_type`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_link_idempotent`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[CONSULTA]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[GESTOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_non_admin_forbidden[OPERADOR]`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_patch_company`

## API-015 — GET /api/v1/empresas

Companies

- Router/handler: [app/modules/empresas/routes.py:21](../../app/modules/empresas/routes.py#L21) · `companies` · operationId `companies_api_v1_empresas_get`.
- Perfil: Usuário ativo autenticado.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de EmpresaResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "get_current_user",
    "module": "app.api.deps",
    "children": [
      {
        "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
        "module": "fastapi.security.http",
        "children": []
      },
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("", response_model=list[EmpresaResponse])
def companies(offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).list(user, offset, limit)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`.

Caminho concreto da fixture: `GET /api/v1/empresas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "40b06f0a-2f60-4a12-9f37-da4f457d478e",
    "nome": "Empresa teste",
    "tipo": "PRODUTOR",
    "documento": null,
    "ativo": true,
    "created_at": "2026-11-23T14:55:10",
    "updated_at": "2026-11-23T14:55:10"
  }
]
```

Cenário negativo a verificar: parâmetros/body inválidos quando declarados → 422; em operação privada, JWT ausente/inválido → 401. Isso é uma recomendação de teste, não uma captura desta operação.

Matriz de respostas observadas: 200.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`

## API-016 — GET /api/v1/empresas/{empresa_id}

Detail

- Router/handler: [app/modules/empresas/routes.py:26](../../app/modules/empresas/routes.py#L26) · `detail` · operationId `detail_api_v1_empresas__empresa_id__get`.
- Perfil: Usuário ativo autenticado.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | empresa_id | True | {   "type": "string",   "format": "uuid",   "title": "Empresa Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | EmpresaResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "get_current_user",
    "module": "app.api.deps",
    "children": [
      {
        "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
        "module": "fastapi.security.http",
        "children": []
      },
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/{empresa_id}", response_model=EmpresaResponse)
def detail(empresa_id: UUID, user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).authorize(empresa_id, user)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`.

Caminho concreto da fixture: `GET /api/v1/empresas/40b06f0a-2f60-4a12-9f37-da4f457d478e`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "40b06f0a-2f60-4a12-9f37-da4f457d478e",
  "nome": "Empresa teste",
  "tipo": "PRODUTOR",
  "documento": null,
  "ativo": true,
  "created_at": "2026-11-23T14:55:10",
  "updated_at": "2026-11-23T14:55:10"
}
```

Cenário negativo comprovado: HTTP 403, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`.

```json
{
  "detail": "Acesso a empresa nao permitido."
}
```

Matriz de respostas observadas: 200, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_membership`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_lists_and_detail`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_missing_records`

## API-017 — PATCH /api/v1/empresas/{empresa_id}

Update

- Router/handler: [app/modules/empresas/routes.py:31](../../app/modules/empresas/routes.py#L31) · `update` · operationId `update_api_v1_empresas__empresa_id__patch`.
- Perfil: ADMIN.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: EmpresaUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | empresa_id | True | {   "type": "string",   "format": "uuid",   "title": "Empresa Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | EmpresaResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/{empresa_id}", response_model=EmpresaResponse, dependencies=[Depends(admin)])
def update(empresa_id: UUID, data: EmpresaUpdate, db: Session = Depends(get_database_session)):
    return EmpresaService(db).update(empresa_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_patch_company`.

Caminho concreto da fixture: `PATCH /api/v1/empresas/40d77858-4108-4981-8786-1b8459f57790`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome": "Atualizada",
  "ativo": false
}
```

Resposta capturada:

```json
{
  "id": "40d77858-4108-4981-8786-1b8459f57790",
  "nome": "Atualizada",
  "tipo": "PRODUTOR",
  "documento": null,
  "ativo": false,
  "created_at": "2026-11-23T14:55:16",
  "updated_at": "2026-11-23T14:55:16"
}
```

Cenário negativo comprovado: HTTP 409, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`.

```json
{
  "detail": "Tipo de empresa incompativel com os vinculos logisticos existentes."
}
```

Matriz de respostas observadas: 200, 409.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_patch_company`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_without_logistics_can_change_type`

## API-018 — POST /api/v1/empresas/{empresa_id}/usuarios/{usuario_id}

Link

- Router/handler: [app/modules/empresas/routes.py:36](../../app/modules/empresas/routes.py#L36) · `link` · operationId `link_api_v1_empresas__empresa_id__usuarios__usuario_id__post`.
- Perfil: ADMIN.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | empresa_id | True | {   "type": "string",   "format": "uuid",   "title": "Empresa Id" } |
| path | usuario_id | True | {   "type": "string",   "format": "uuid",   "title": "Usuario Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | VinculoResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/{empresa_id}/usuarios/{usuario_id}", response_model=VinculoResponse, dependencies=[Depends(admin)])
def link(empresa_id: UUID, usuario_id: UUID, db: Session = Depends(get_database_session)):
    return EmpresaService(db).link(empresa_id, usuario_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`.

Caminho concreto da fixture: `POST /api/v1/empresas/ebcdbebf-94d4-447c-bf19-f5987da64d88/usuarios/cd25c23b-894b-4fc2-9044-e344c61eec7f`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "388537a6-8e98-437b-93ae-11f8e235433d",
  "empresa_id": "ebcdbebf-94d4-447c-bf19-f5987da64d88",
  "usuario_id": "cd25c23b-894b-4fc2-9044-e344c61eec7f",
  "ativo": true
}
```

Cenário negativo a verificar: parâmetros/body inválidos quando declarados → 422; em operação privada, JWT ausente/inválido → 401. Isso é uma recomendação de teste, não uma captura desta operação.

Matriz de respostas observadas: 200.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_company_excluded`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_inactive_membership`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_link_idempotent`<br>[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_me_multi_company`

## API-019 — GET /api/v1/empresas/{empresa_id}/usuarios

Users

- Router/handler: [app/modules/empresas/routes.py:41](../../app/modules/empresas/routes.py#L41) · `users` · operationId `users_api_v1_empresas__empresa_id__usuarios_get`.
- Perfil: ADMIN/GESTOR.
- Escopo: EmpresaService.authorize/list; não ADMIN requer vínculo ativo; detalhe também exige empresa ativa.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | empresa_id | True | {   "type": "string",   "format": "uuid",   "title": "Empresa Id" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de UsuarioResponse; Successful Response |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_current_user",
    "module": "app.api.deps",
    "children": [
      {
        "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
        "module": "fastapi.security.http",
        "children": []
      },
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/{empresa_id}/usuarios", response_model=list[UsuarioResponse], dependencies=[Depends(require_profiles("ADMIN", "GESTOR"))])
def users(empresa_id: UUID, offset: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), user: Usuario = Depends(get_current_user), db: Session = Depends(get_database_session)):
    return EmpresaService(db).users(empresa_id, user, offset, limit)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`.

Caminho concreto da fixture: `GET /api/v1/empresas/f275d100-fa78-48f4-ad9a-1d2aa774a31d/usuarios`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "643ee003-eb67-4e0d-8a39-9fc4c5ef76ae",
    "nome": "Leitor",
    "email": "reader@example.com",
    "perfil_id": "32957cfe-38d0-4475-b85d-faf501375e7d",
    "ativo": true,
    "created_at": "2026-11-23T14:55:13",
    "updated_at": "2026-11-23T14:55:13"
  }
]
```

Cenário negativo comprovado: HTTP 403, [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`.

```json
{
  "detail": "Acesso a empresa nao permitido."
}
```

Matriz de respostas observadas: 200, 403.

Testes HTTP que atingiram esta rota:
[tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) `test_company_isolation`

## API-020 — POST /api/v1/produtos

Create

- Router/handler: [app/modules/produtos/routes.py:18](../../app/modules/produtos/routes.py#L18) · `create` · operationId `create_api_v1_produtos_post`.
- Perfil: ADMIN.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ProdutoCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | ProdutoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("", response_model=ProdutoResponse, status_code=201, dependencies=[Depends(require_profiles("ADMIN"))])
def create(data: ProdutoCreate, db: Session = Depends(get_database_session)):
    return ProdutoService(db).create(data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`.

Caminho concreto da fixture: `POST /api/v1/produtos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome": "Produto teste"
}
```

Resposta capturada:

```json
{
  "id": "0574b8e7-3467-44e3-9612-cdd4bef7cd17",
  "created_at": "2026-11-23T14:57:09",
  "updated_at": "2026-11-23T14:57:09",
  "nome": "Produto teste",
  "descricao": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 201, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-021 — GET /api/v1/produtos

Products

- Router/handler: [app/modules/produtos/routes.py:23](../../app/modules/produtos/routes.py#L23) · `products` · operationId `products_api_v1_produtos_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | ativo | False | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ],   "title": "Ativo" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de ProdutoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("", response_model=list[ProdutoResponse])
def products(ativo: bool | None = None, limit: int = Query(50, ge=1, le=100),
             offset: int = Query(0, ge=0), db: Session = Depends(get_database_session)):
    return ProdutoService(db).list({"ativo": ativo}, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`.

Caminho concreto da fixture: `GET /api/v1/produtos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "82055099-5033-4ddb-846e-215a3014033d",
    "created_at": "2026-11-23T14:57:17",
    "updated_at": "2026-11-23T14:57:17",
    "nome": "Produto teste",
    "descricao": null,
    "ativo": true
  }
]
```

Cenário negativo comprovado: HTTP 422, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`.

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": [
        "query",
        "limit"
      ],
      "msg": "Input should be less than or equal to 100"
    }
  ]
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unknown_profile_inactive_user_and_missing_profile_are_denied`

## API-022 — GET /api/v1/produtos/{produto_id}

Get

- Router/handler: [app/modules/produtos/routes.py:29](../../app/modules/produtos/routes.py#L29) · `get` · operationId `get_api_v1_produtos__produto_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | produto_id | True | {   "type": "string",   "format": "uuid",   "title": "Produto Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ProdutoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/{produto_id}", response_model=ProdutoResponse)
def get(produto_id: UUID, db: Session = Depends(get_database_session)):
    return ProdutoService(db).get(produto_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`.

Caminho concreto da fixture: `GET /api/v1/produtos/0574b8e7-3467-44e3-9612-cdd4bef7cd17`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "0574b8e7-3467-44e3-9612-cdd4bef7cd17",
  "created_at": "2026-11-23T14:57:09",
  "updated_at": "2026-11-23T14:57:09",
  "nome": "Produto teste",
  "descricao": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[produtos]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[produtos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-023 — PATCH /api/v1/produtos/{produto_id}

Update

- Router/handler: [app/modules/produtos/routes.py:34](../../app/modules/produtos/routes.py#L34) · `update` · operationId `update_api_v1_produtos__produto_id__patch`.
- Perfil: ADMIN.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ProdutoUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | produto_id | True | {   "type": "string",   "format": "uuid",   "title": "Produto Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ProdutoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/{produto_id}", response_model=ProdutoResponse, dependencies=[Depends(require_profiles("ADMIN"))])
def update(produto_id: UUID, data: ProdutoUpdate, db: Session = Depends(get_database_session)):
    return ProdutoService(db).update(produto_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`.

Caminho concreto da fixture: `PATCH /api/v1/produtos/d70d16b2-9817-4915-aec4-5bfd98e721f0`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome": "Atualizado",
  "ativo": false
}
```

Resposta capturada:

```json
{
  "id": "d70d16b2-9817-4915-aec4-5bfd98e721f0",
  "created_at": "2026-11-23T14:57:21",
  "updated_at": "2026-11-23T14:57:21",
  "nome": "Atualizado",
  "descricao": null,
  "ativo": false
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-024 — POST /api/v1/produtos/{produto_id}/parametros

Create Parameter

- Router/handler: [app/modules/produtos/routes.py:39](../../app/modules/produtos/routes.py#L39) · `create_parameter` · operationId `create_parameter_api_v1_produtos__produto_id__parametros_post`.
- Perfil: ADMIN.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ParametroCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | produto_id | True | {   "type": "string",   "format": "uuid",   "title": "Produto Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | ParametroResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/{produto_id}/parametros", response_model=ParametroResponse, status_code=201, dependencies=[Depends(require_profiles("ADMIN"))])
def create_parameter(produto_id: UUID, data: ParametroCreate, db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).create(data, produto_id=produto_id)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`.

Caminho concreto da fixture: `POST /api/v1/produtos/bc933013-9227-4070-ad0b-b6240e97fc94/parametros`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "nome_parametro": "temperatura"
}
```

Resposta capturada:

```json
{
  "id": "1130d296-0989-4c4e-9faa-19a7360d0a36",
  "created_at": "2026-11-23T14:57:25",
  "updated_at": "2026-11-23T14:57:25",
  "nome_parametro": "temperatura",
  "unidade": null,
  "valor_minimo": null,
  "valor_maximo": null,
  "observacao": null,
  "produto_id": "bc933013-9227-4070-ad0b-b6240e97fc94"
}
```

Cenário negativo comprovado: HTTP 409, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`.

```json
{
  "detail": "Identificador duplicado ou relacionamento invalido."
}
```

Matriz de respostas observadas: 201, 401, 403, 409.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-025 — GET /api/v1/produtos/{produto_id}/parametros

Parameters

- Router/handler: [app/modules/produtos/routes.py:44](../../app/modules/produtos/routes.py#L44) · `parameters` · operationId `parameters_api_v1_produtos__produto_id__parametros_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | produto_id | True | {   "type": "string",   "format": "uuid",   "title": "Produto Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de ParametroResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/{produto_id}/parametros", response_model=list[ParametroResponse])
def parameters(produto_id: UUID, limit: int = Query(50, ge=1, le=100),
               offset: int = Query(0, ge=0), db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).list_for_product(produto_id, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`.

Caminho concreto da fixture: `GET /api/v1/produtos/bc933013-9227-4070-ad0b-b6240e97fc94/parametros`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "1130d296-0989-4c4e-9faa-19a7360d0a36",
    "created_at": "2026-11-23T14:57:25",
    "updated_at": "2026-11-23T14:57:25",
    "nome_parametro": "temperatura",
    "unidade": null,
    "valor_minimo": null,
    "valor_maximo": null,
    "observacao": null,
    "produto_id": "bc933013-9227-4070-ad0b-b6240e97fc94"
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-026 — PATCH /api/v1/produtos/{produto_id}/parametros/{parametro_id}

Update Parameter

- Router/handler: [app/modules/produtos/routes.py:50](../../app/modules/produtos/routes.py#L50) · `update_parameter` · operationId `update_parameter_api_v1_produtos__produto_id__parametros__parametro_id__patch`.
- Perfil: ADMIN.
- Escopo: Catálogo global; IDs não concedem permissões.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ParametroUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | produto_id | True | {   "type": "string",   "format": "uuid",   "title": "Produto Id" } |
| path | parametro_id | True | {   "type": "string",   "format": "uuid",   "title": "Parametro Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ParametroResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "require_profiles.<locals>.dependency",
    "module": "app.api.deps",
    "children": [
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  },
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/{produto_id}/parametros/{parametro_id}", response_model=ParametroResponse, dependencies=[Depends(require_profiles("ADMIN"))])
def update_parameter(produto_id: UUID, parametro_id: UUID, data: ParametroUpdate,
                     db: Session = Depends(get_database_session)):
    return ParametroProdutoService(db).update_for_product(produto_id, parametro_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`.

Caminho concreto da fixture: `PATCH /api/v1/produtos/bc933013-9227-4070-ad0b-b6240e97fc94/parametros/1130d296-0989-4c4e-9faa-19a7360d0a36`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "valor_minimo": "1",
  "valor_maximo": "2",
  "observacao": "Valores sinteticos de teste"
}
```

Resposta capturada:

```json
{
  "id": "1130d296-0989-4c4e-9faa-19a7360d0a36",
  "created_at": "2026-11-23T14:57:25",
  "updated_at": "2026-11-23T14:57:25",
  "nome_parametro": "temperatura",
  "unidade": null,
  "valor_minimo": "1.0000",
  "valor_maximo": "2.0000",
  "observacao": "Valores sinteticos de teste",
  "produto_id": "bc933013-9227-4070-ad0b-b6240e97fc94"
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`.

```json
{
  "detail": "valor_minimo deve ser menor ou igual a valor_maximo."
}
```

Matriz de respostas observadas: 200, 401, 403, 404, 422.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[CONSULTA]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[GESTOR]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_global_product_catalog_is_read_only_for_non_admin[OPERADOR]`

## API-027 — POST /api/v1/veiculos

Create Veiculos

- Router/handler: [app/modules/logistica/routes.py:24](../../app/modules/logistica/routes.py#L24) · `create_veiculos` · operationId `create_veiculos_api_v1_veiculos_post`.
- Perfil: ADMIN/GESTOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: VeiculoCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | VeiculoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/veiculos", response_model=VeiculoResponse, status_code=201)
def create_veiculos(data: VeiculoCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Veiculo, data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`.

Caminho concreto da fixture: `POST /api/v1/veiculos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "identificador": "V-1"
}
```

Resposta capturada:

```json
{
  "id": "b9772d7f-d15a-4411-a78f-c38bb00a0764",
  "created_at": "2026-11-23T14:57:09",
  "updated_at": "2026-11-23T14:57:09",
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "identificador": "V-1",
  "placa": null,
  "modelo": null,
  "descricao": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_nonexistent_company[veiculos]`.

```json
{
  "detail": "Empresa nao encontrada."
}
```

Matriz de respostas observadas: 201, 401, 403, 404, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_nonexistent_company[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_fleet_management_requires_gestor_and_own_carrier[veiculos]`

## API-028 — GET /api/v1/veiculos

List Veiculos

- Router/handler: [app/modules/logistica/routes.py:29](../../app/modules/logistica/routes.py#L29) · `list_veiculos` · operationId `list_veiculos_api_v1_veiculos_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | empresa_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Empresa Id" } |
| query | ativo | False | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ],   "title": "Ativo" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de VeiculoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/veiculos", response_model=list[VeiculoResponse])
def list_veiculos(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Veiculo, {"empresa_id": empresa_id, "ativo": ativo}, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`.

Caminho concreto da fixture: `GET /api/v1/veiculos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "bba89ba1-1d05-4f75-8dea-19514f0607b9",
    "created_at": "2026-11-23T14:57:18",
    "updated_at": "2026-11-23T14:57:18",
    "empresa_id": "df81ca7a-c4b4-48ed-a64c-d3bcd65a9c66",
    "identificador": "V-1",
    "placa": null,
    "modelo": null,
    "descricao": null,
    "ativo": true
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unfiltered_and_explicit_lists_scope_before_pagination[veiculos]`

## API-029 — GET /api/v1/veiculos/{veiculo_id}

Get Veiculos

- Router/handler: [app/modules/logistica/routes.py:39](../../app/modules/logistica/routes.py#L39) · `get_veiculos` · operationId `get_veiculos_api_v1_veiculos__veiculo_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | veiculo_id | True | {   "type": "string",   "format": "uuid",   "title": "Veiculo Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | VeiculoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def get_veiculos(veiculo_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Veiculo, veiculo_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`.

Caminho concreto da fixture: `GET /api/v1/veiculos/dd388bc3-0dd9-4f5d-bc16-f8242fef2e32`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "dd388bc3-0dd9-4f5d-bc16-f8242fef2e32",
  "created_at": "2026-11-23T14:57:10",
  "updated_at": "2026-11-23T14:57:10",
  "empresa_id": "1f350ad4-383e-40df-a9c5-4618bcf7c3e5",
  "identificador": "V-1",
  "placa": null,
  "modelo": null,
  "descricao": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[veiculos]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[veiculos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[CONSULTA-veiculos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[GESTOR-veiculos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[OPERADOR-veiculos]`

## API-030 — PATCH /api/v1/veiculos/{veiculo_id}

Update Veiculos

- Router/handler: [app/modules/logistica/routes.py:44](../../app/modules/logistica/routes.py#L44) · `update_veiculos` · operationId `update_veiculos_api_v1_veiculos__veiculo_id__patch`.
- Perfil: ADMIN/GESTOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: VeiculoUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | veiculo_id | True | {   "type": "string",   "format": "uuid",   "title": "Veiculo Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | VeiculoResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/veiculos/{veiculo_id}", response_model=VeiculoResponse)
def update_veiculos(veiculo_id: UUID, data: VeiculoUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Veiculo, veiculo_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`.

Caminho concreto da fixture: `PATCH /api/v1/veiculos/62393e7c-324a-4151-b63e-aa210191e811`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "descricao": "Atualizado",
  "ativo": false
}
```

Resposta capturada:

```json
{
  "id": "62393e7c-324a-4151-b63e-aa210191e811",
  "created_at": "2026-11-23T14:57:21",
  "updated_at": "2026-11-23T14:57:21",
  "empresa_id": "11da6160-bf5f-4841-9afc-80612fb7b96b",
  "identificador": "V-1",
  "placa": null,
  "modelo": null,
  "descricao": "Atualizado",
  "ativo": false
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_fleet_management_requires_gestor_and_own_carrier[veiculos]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_foreign_update_is_denied_and_preserves_record[veiculos]`

## API-031 — POST /api/v1/motoristas

Create Motoristas

- Router/handler: [app/modules/logistica/routes.py:49](../../app/modules/logistica/routes.py#L49) · `create_motoristas` · operationId `create_motoristas_api_v1_motoristas_post`.
- Perfil: ADMIN/GESTOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: MotoristaCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | MotoristaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/motoristas", response_model=MotoristaResponse, status_code=201)
def create_motoristas(data: MotoristaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Motorista, data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`.

Caminho concreto da fixture: `POST /api/v1/motoristas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "nome": "Motorista teste"
}
```

Resposta capturada:

```json
{
  "id": "df7e29e5-5489-4337-9560-0c46d107378c",
  "created_at": "2026-11-23T14:57:09",
  "updated_at": "2026-11-23T14:57:09",
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "nome": "Motorista teste",
  "documento": null,
  "telefone": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_nonexistent_company[motoristas]`.

```json
{
  "detail": "Empresa nao encontrada."
}
```

Matriz de respostas observadas: 201, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_nonexistent_company[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_fleet_management_requires_gestor_and_own_carrier[motoristas]`

## API-032 — GET /api/v1/motoristas

List Motoristas

- Router/handler: [app/modules/logistica/routes.py:54](../../app/modules/logistica/routes.py#L54) · `list_motoristas` · operationId `list_motoristas_api_v1_motoristas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | empresa_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Empresa Id" } |
| query | ativo | False | {   "anyOf": [     {       "type": "boolean"     },     {       "type": "null"     }   ],   "title": "Ativo" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de MotoristaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/motoristas", response_model=list[MotoristaResponse])
def list_motoristas(
    empresa_id: UUID | None = None,
    ativo: bool | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Motorista, {"empresa_id": empresa_id, "ativo": ativo}, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`.

Caminho concreto da fixture: `GET /api/v1/motoristas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "7e0387df-0c91-4dd5-96b7-f030182be5bf",
    "created_at": "2026-11-23T14:57:18",
    "updated_at": "2026-11-23T14:57:18",
    "empresa_id": "c0bf9bf6-4c4d-449e-8528-8e04557afb23",
    "nome": "Motorista teste",
    "documento": null,
    "telefone": null,
    "ativo": true
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unfiltered_and_explicit_lists_scope_before_pagination[motoristas]`

## API-033 — GET /api/v1/motoristas/{motorista_id}

Get Motoristas

- Router/handler: [app/modules/logistica/routes.py:64](../../app/modules/logistica/routes.py#L64) · `get_motoristas` · operationId `get_motoristas_api_v1_motoristas__motorista_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | motorista_id | True | {   "type": "string",   "format": "uuid",   "title": "Motorista Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | MotoristaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def get_motoristas(motorista_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Motorista, motorista_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`.

Caminho concreto da fixture: `GET /api/v1/motoristas/32574113-8de9-4c1b-911b-86ecec392db6`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "32574113-8de9-4c1b-911b-86ecec392db6",
  "created_at": "2026-11-23T14:57:10",
  "updated_at": "2026-11-23T14:57:10",
  "empresa_id": "137a127a-9478-4130-a061-8d25d4f0137b",
  "nome": "Motorista teste",
  "documento": null,
  "telefone": null,
  "ativo": true
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[motoristas]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_with_only_one_inactive_link[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[motoristas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[CONSULTA-motoristas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[GESTOR-motoristas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[OPERADOR-motoristas]`

## API-034 — PATCH /api/v1/motoristas/{motorista_id}

Update Motoristas

- Router/handler: [app/modules/logistica/routes.py:69](../../app/modules/logistica/routes.py#L69) · `update_motoristas` · operationId `update_motoristas_api_v1_motoristas__motorista_id__patch`.
- Perfil: ADMIN/GESTOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: MotoristaUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | motorista_id | True | {   "type": "string",   "format": "uuid",   "title": "Motorista Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | MotoristaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/motoristas/{motorista_id}", response_model=MotoristaResponse)
def update_motoristas(motorista_id: UUID, data: MotoristaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Motorista, motorista_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`.

Caminho concreto da fixture: `PATCH /api/v1/motoristas/2d8db99c-89a6-4a56-b872-23e84e31bdc4`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "telefone": "teste",
  "ativo": false
}
```

Resposta capturada:

```json
{
  "id": "2d8db99c-89a6-4a56-b872-23e84e31bdc4",
  "created_at": "2026-11-23T14:57:22",
  "updated_at": "2026-11-23T14:57:22",
  "empresa_id": "4b6db159-0eca-4eb4-a992-1c14a53d1b1f",
  "nome": "Motorista teste",
  "documento": null,
  "telefone": "teste",
  "ativo": false
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_fleet_management_requires_gestor_and_own_carrier[motoristas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_foreign_update_is_denied_and_preserves_record[motoristas]`

## API-035 — POST /api/v1/viagens

Create Viagens

- Router/handler: [app/modules/logistica/routes.py:74](../../app/modules/logistica/routes.py#L74) · `create_viagens` · operationId `create_viagens_api_v1_viagens_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ViagemCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

Sem parâmetros de path/query declarados.

Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | ViagemResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/viagens", response_model=ViagemResponse, status_code=201)
def create_viagens(data: ViagemCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Viagem, data)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `POST /api/v1/viagens`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "transportadora_id": "9e18f4ec-122b-46ca-b99b-b97fd84e71ce",
  "veiculo_id": "14f1d169-0012-40e7-b75a-179c3ec78726",
  "motorista_id": "c99c2311-ea86-4298-8bda-ff73cb743c30",
  "origem": "Petrolina hipotetica",
  "destino": "Destino didatico",
  "saida_em": "2026-11-23T10:54:05.435676+00:00"
}
```

Resposta capturada:

```json
{
  "id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
  "created_at": "2026-11-23T14:57:06",
  "updated_at": "2026-11-23T14:57:06",
  "transportadora_id": "9e18f4ec-122b-46ca-b99b-b97fd84e71ce",
  "veiculo_id": "14f1d169-0012-40e7-b75a-179c3ec78726",
  "motorista_id": "c99c2311-ea86-4298-8bda-ff73cb743c30",
  "origem": "Petrolina hipotetica",
  "destino": "Destino didatico",
  "saida_em": "2026-11-23T10:54:05.435676",
  "previsao_chegada_em": null,
  "inicio_real": null,
  "chegada_em": null,
  "status": "PLANEJADA",
  "observacoes": null
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 201, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_trip_creation_does_not_trust_client_company_or_foreign_fleet`

## API-036 — GET /api/v1/viagens

List Viagens

- Router/handler: [app/modules/logistica/routes.py:79](../../app/modules/logistica/routes.py#L79) · `list_viagens` · operationId `list_viagens_api_v1_viagens_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| query | empresa_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Empresa Id" } |
| query | status | False | {   "anyOf": [     {       "$ref": "#/components/schemas/StatusViagem"     },     {       "type": "null"     }   ],   "title": "Status" } |
| query | veiculo_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Veiculo Id" } |
| query | motorista_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Motorista Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de ViagemResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/viagens", response_model=list[ViagemResponse])
def list_viagens(
    empresa_id: UUID | None = None,
    status: StatusViagem | None = None,
    veiculo_id: UUID | None = None,
    motorista_id: UUID | None = None,
    limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
    access: LogisticaAccess = Depends(authorized),
):
    return access.list_owned(Viagem, {"transportadora_id": empresa_id, "status": status, "veiculo_id": veiculo_id, "motorista_id": motorista_id}, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`.

Caminho concreto da fixture: `GET /api/v1/viagens`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "6ca2a474-1d07-448e-8882-a357b2b469fa",
    "created_at": "2026-11-23T14:57:20",
    "updated_at": "2026-11-23T14:57:20",
    "transportadora_id": "e7fb66b2-203e-41f3-96ed-cf2b53e10579",
    "veiculo_id": "d7d69122-e3c3-4249-b956-da6febb10115",
    "motorista_id": "af7a51a7-b6be-4e25-8427-5af32c50b7c8",
    "origem": "Origem teste",
    "destino": "Destino teste",
    "saida_em": "2026-10-07T12:00:00",
    "previsao_chegada_em": null,
    "inicio_real": null,
    "chegada_em": null,
    "status": "PLANEJADA",
    "observacoes": null
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_inactive_membership_company_and_multiple_carrier_links`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unfiltered_and_explicit_lists_scope_before_pagination[viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unknown_profile_inactive_user_and_missing_profile_are_denied`

## API-037 — GET /api/v1/viagens/{viagem_id}

Get Viagens

- Router/handler: [app/modules/logistica/routes.py:91](../../app/modules/logistica/routes.py#L91) · `get_viagens` · operationId `get_viagens_api_v1_viagens__viagem_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | viagem_id | True | {   "type": "string",   "format": "uuid",   "title": "Viagem Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ViagemResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/viagens/{viagem_id}", response_model=ViagemResponse)
def get_viagens(viagem_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Viagem, viagem_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`.

Caminho concreto da fixture: `GET /api/v1/viagens/cd5bd9cb-e0ee-4d9a-9a5d-feb0e3686086`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "cd5bd9cb-e0ee-4d9a-9a5d-feb0e3686086",
  "created_at": "2026-11-23T14:57:11",
  "updated_at": "2026-11-23T14:57:11",
  "transportadora_id": "d4f60422-2232-47bb-bc55-7654dea6285d",
  "veiculo_id": "16edbad9-03a3-4490-8eb7-01446419b593",
  "motorista_id": "e48e3da9-ca9c-40c5-b436-4b44bd1c626a",
  "origem": "Origem teste",
  "destino": "Destino teste",
  "saida_em": "2026-10-07T12:00:00",
  "previsao_chegada_em": null,
  "inicio_real": null,
  "chegada_em": null,
  "status": "PLANEJADA",
  "observacoes": null
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[viagens]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[CONSULTA-viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[GESTOR-viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[OPERADOR-viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_inactive_membership_company_and_multiple_carrier_links`

## API-038 — PATCH /api/v1/viagens/{viagem_id}

Update Viagens

- Router/handler: [app/modules/logistica/routes.py:96](../../app/modules/logistica/routes.py#L96) · `update_viagens` · operationId `update_viagens_api_v1_viagens__viagem_id__patch`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ViagemUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | viagem_id | True | {   "type": "string",   "format": "uuid",   "title": "Viagem Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ViagemResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/viagens/{viagem_id}", response_model=ViagemResponse)
def update_viagens(viagem_id: UUID, data: ViagemUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Viagem, viagem_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `PATCH /api/v1/viagens/46687c15-7e9a-411f-a2ae-6f5944eab8db`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "status": "EM_ANDAMENTO",
  "inicio_real": "2026-11-23T10:54:05.435676+00:00"
}
```

Resposta capturada:

```json
{
  "id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
  "created_at": "2026-11-23T14:57:06",
  "updated_at": "2026-11-23T14:57:06",
  "transportadora_id": "9e18f4ec-122b-46ca-b99b-b97fd84e71ce",
  "veiculo_id": "14f1d169-0012-40e7-b75a-179c3ec78726",
  "motorista_id": "c99c2311-ea86-4298-8bda-ff73cb743c30",
  "origem": "Petrolina hipotetica",
  "destino": "Destino didatico",
  "saida_em": "2026-11-23T10:54:05.435676",
  "previsao_chegada_em": null,
  "inicio_real": "2026-11-23T10:54:05.435676",
  "chegada_em": null,
  "status": "EM_ANDAMENTO",
  "observacoes": null
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`.

```json
{
  "detail": "Transicao de status nao permitida."
}
```

Matriz de respostas observadas: 200, 401, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_foreign_update_is_denied_and_preserves_record[viagens]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_inactive_membership_company_and_multiple_carrier_links`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_trip_creation_does_not_trust_client_company_or_foreign_fleet`

## API-039 — POST /api/v1/viagens/{viagem_id}/cargas

Create Carga

- Router/handler: [app/modules/logistica/routes.py:101](../../app/modules/logistica/routes.py#L101) · `create_carga` · operationId `create_carga_api_v1_viagens__viagem_id__cargas_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: CargaCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | viagem_id | True | {   "type": "string",   "format": "uuid",   "title": "Viagem Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | CargaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/viagens/{viagem_id}/cargas", response_model=CargaResponse, status_code=201)
def create_carga(viagem_id: UUID, data: CargaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Carga, data, parent_id=viagem_id)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `POST /api/v1/viagens/46687c15-7e9a-411f-a2ae-6f5944eab8db/cargas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "produto_id": "0ef738e6-1365-41c6-ba99-86896411a88e",
  "produtor_id": "47e0d6ea-e9b8-4f10-878b-852ecc9ca039",
  "identificacao": "ETAPA8-CARGA-HIPOTETICA",
  "observacoes": "Fixture didatica; sem dados de producao."
}
```

Resposta capturada:

```json
{
  "id": "f3cc932c-61f0-4bd4-96a8-9565d0eadbcb",
  "created_at": "2026-11-23T14:57:06",
  "updated_at": "2026-11-23T14:57:06",
  "produto_id": "0ef738e6-1365-41c6-ba99-86896411a88e",
  "produtor_id": "47e0d6ea-e9b8-4f10-878b-852ecc9ca039",
  "cliente_id": null,
  "identificacao": "ETAPA8-CARGA-HIPOTETICA",
  "quantidade_caixas": null,
  "quantidade": null,
  "unidade": null,
  "origem_produto": null,
  "observacoes": "Fixture didatica; sem dados de producao.",
  "viagem_id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
  "status": "PLANEJADA"
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 201, 401, 403, 404, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_cargo_and_box_writes_follow_parent_not_request_payload`

## API-040 — GET /api/v1/viagens/{viagem_id}/cargas

List Cargas

- Router/handler: [app/modules/logistica/routes.py:106](../../app/modules/logistica/routes.py#L106) · `list_cargas` · operationId `list_cargas_api_v1_viagens__viagem_id__cargas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | viagem_id | True | {   "type": "string",   "format": "uuid",   "title": "Viagem Id" } |
| query | produto_id | False | {   "anyOf": [     {       "type": "string",       "format": "uuid"     },     {       "type": "null"     }   ],   "title": "Produto Id" } |
| query | status | False | {   "anyOf": [     {       "$ref": "#/components/schemas/StatusCarga"     },     {       "type": "null"     }   ],   "title": "Status" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de CargaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/viagens/{viagem_id}/cargas", response_model=list[CargaResponse])
def list_cargas(viagem_id: UUID, produto_id: UUID | None = None, status: StatusCarga | None = None,
                limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                access: LogisticaAccess = Depends(authorized)):
    return access.list_cargas(viagem_id, {"produto_id": produto_id, "status": status}, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`.

Caminho concreto da fixture: `GET /api/v1/viagens/183a51fe-9d58-485e-bf1f-a2c459b9d0dc/cargas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "f97cc9de-8c93-447c-ab75-c439d716cf53",
    "created_at": "2026-11-23T14:57:37",
    "updated_at": "2026-11-23T14:57:37",
    "produto_id": "bfc15db1-5ddf-43ad-ad4f-742cb314f5d0",
    "produtor_id": "34bf53b4-3d8b-4114-afa7-c74458cce640",
    "cliente_id": "f7d53450-300c-4f7a-868c-336d5cb12229",
    "identificacao": "C-1",
    "quantidade_caixas": null,
    "quantidade": null,
    "unidade": null,
    "origem_produto": null,
    "observacoes": null,
    "viagem_id": "183a51fe-9d58-485e-bf1f-a2c459b9d0dc",
    "status": "PLANEJADA"
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_nested_lists_cannot_use_foreign_parent_ids[viagens-cargas]`

## API-041 — GET /api/v1/cargas/{carga_id}

Get Carga

- Router/handler: [app/modules/logistica/routes.py:113](../../app/modules/logistica/routes.py#L113) · `get_carga` · operationId `get_carga_api_v1_cargas__carga_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CargaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/cargas/{carga_id}", response_model=CargaResponse)
def get_carga(carga_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Carga, carga_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`.

Caminho concreto da fixture: `GET /api/v1/cargas/77a60645-35cc-4618-98db-0e87479f79d9`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "77a60645-35cc-4618-98db-0e87479f79d9",
  "created_at": "2026-11-23T14:57:13",
  "updated_at": "2026-11-23T14:57:13",
  "produto_id": "0c8f58bf-de0f-4459-abb3-3090581d1965",
  "produtor_id": "208f9f77-f04a-48c3-b3da-669d67ced25d",
  "cliente_id": "dd0a10b0-0968-4094-af3a-f4db413fd959",
  "identificacao": "C-1",
  "quantidade_caixas": null,
  "quantidade": null,
  "unidade": null,
  "origem_produto": null,
  "observacoes": null,
  "viagem_id": "9669778c-a70c-456a-ae14-a190f06c4768",
  "status": "PLANEJADA"
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[cargas]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_legacy_cargo_still_works_without_monitoring_configuration`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[CONSULTA-cargas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[GESTOR-cargas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[OPERADOR-cargas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_inactive_membership_company_and_multiple_carrier_links`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_secured_logistics_preserves_monitoring_snapshot_and_scope`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_unknown_profile_inactive_user_and_missing_profile_are_denied`

## API-042 — PATCH /api/v1/cargas/{carga_id}

Update Carga

- Router/handler: [app/modules/logistica/routes.py:118](../../app/modules/logistica/routes.py#L118) · `update_carga` · operationId `update_carga_api_v1_cargas__carga_id__patch`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: CargaUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CargaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/cargas/{carga_id}", response_model=CargaResponse)
def update_carga(carga_id: UUID, data: CargaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Carga, carga_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `PATCH /api/v1/cargas/f3cc932c-61f0-4bd4-96a8-9565d0eadbcb`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "status": "EM_TRANSITO"
}
```

Resposta capturada:

```json
{
  "id": "f3cc932c-61f0-4bd4-96a8-9565d0eadbcb",
  "created_at": "2026-11-23T14:57:06",
  "updated_at": "2026-11-23T14:57:06",
  "produto_id": "0ef738e6-1365-41c6-ba99-86896411a88e",
  "produtor_id": "47e0d6ea-e9b8-4f10-878b-852ecc9ca039",
  "cliente_id": null,
  "identificacao": "ETAPA8-CARGA-HIPOTETICA",
  "quantidade_caixas": null,
  "quantidade": null,
  "unidade": null,
  "origem_produto": null,
  "observacoes": "Fixture didatica; sem dados de producao.",
  "viagem_id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
  "status": "EM_TRANSITO"
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`.

```json
{
  "detail": "Carga em transito exige viagem em andamento."
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_legacy_cargo_still_works_without_monitoring_configuration`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_cargo_and_box_writes_follow_parent_not_request_payload`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_foreign_update_is_denied_and_preserves_record[cargas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_secured_logistics_preserves_monitoring_snapshot_and_scope`

## API-043 — POST /api/v1/cargas/{carga_id}/caixas

Create Caixa

- Router/handler: [app/modules/logistica/routes.py:123](../../app/modules/logistica/routes.py#L123) · `create_caixa` · operationId `create_caixa_api_v1_cargas__carga_id__caixas_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: CaixaCreate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | CaixaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/cargas/{carga_id}/caixas", response_model=CaixaResponse, status_code=201)
def create_caixa(carga_id: UUID, data: CaixaCreate, access: LogisticaAccess = Depends(authorized)):
    return access.create(Caixa, data, parent_id=carga_id)

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`.

Caminho concreto da fixture: `POST /api/v1/cargas/14d4e86a-86e5-43bf-8e42-1d3c3251a0f3/caixas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "identificacao": "CX-1"
}
```

Resposta capturada:

```json
{
  "id": "75a24b54-8cd8-48a5-80fa-de120cf77ed4",
  "created_at": "2026-11-23T14:57:09",
  "updated_at": "2026-11-23T14:57:09",
  "identificacao": "CX-1",
  "codigo_externo": null,
  "peso": null,
  "observacoes": null,
  "carga_id": "14d4e86a-86e5-43bf-8e42-1d3c3251a0f3",
  "status": "REGISTRADA"
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_box_parent`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 201, 401, 403, 404, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_filter[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_same_type_update_allowed`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[cargas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_inactive_vehicle_trip_start`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_legacy_trip_can_receive_notes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_cargos_filters`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[motoristas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[produtos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[veiculos]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_lists[viagens]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_box_parent`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[produto_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_cargo_reference[viagem_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[motorista_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[transportadora_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_trip_reference[veiculo_id]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_cargo_in_closed_trip_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_no_reparenting_or_physical_delete`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_pagination`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_has_no_default_scientific_values`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_merged_range_validation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_parameter_wrong_product`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[create]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_boxes_overflow_rejected_before_service[update]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_quantity_requires_unit`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_relationships`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_same_identifier_different_scope`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[box]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[cargo]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[parameter]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_scoped_duplicates[vehicle]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_skipping_trip_status_rejected`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_cancellation`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_company_mismatch`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_status_transitions`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_trip_time_order`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[cargas-data4]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[motoristas-data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[produtos-data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[veiculos-data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[viagens-data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_vehicle_requires_transportadora`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_cargo_and_box_writes_follow_parent_not_request_payload`

## API-044 — GET /api/v1/cargas/{carga_id}/caixas

List Caixas

- Router/handler: [app/modules/logistica/routes.py:128](../../app/modules/logistica/routes.py#L128) · `list_caixas` · operationId `list_caixas_api_v1_cargas__carga_id__caixas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de CaixaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/cargas/{carga_id}/caixas", response_model=list[CaixaResponse])
def list_caixas(carga_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                access: LogisticaAccess = Depends(authorized)):
    return access.list_caixas(carga_id, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`.

Caminho concreto da fixture: `GET /api/v1/cargas/4b58178b-3943-4a78-b4eb-53788618662d/caixas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "b625ec5c-763b-461d-b90b-3974438b7340",
    "created_at": "2026-11-23T14:57:38",
    "updated_at": "2026-11-23T14:57:38",
    "identificacao": "CX-1",
    "codigo_externo": null,
    "peso": null,
    "observacoes": null,
    "carga_id": "4b58178b-3943-4a78-b4eb-53788618662d",
    "status": "REGISTRADA"
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_list_boxes`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_nested_lists_cannot_use_foreign_parent_ids[cargas-caixas]`

## API-045 — GET /api/v1/caixas/{caixa_id}

Get Caixa

- Router/handler: [app/modules/logistica/routes.py:134](../../app/modules/logistica/routes.py#L134) · `get_caixa` · operationId `get_caixa_api_v1_caixas__caixa_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | caixa_id | True | {   "type": "string",   "format": "uuid",   "title": "Caixa Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CaixaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/caixas/{caixa_id}", response_model=CaixaResponse)
def get_caixa(caixa_id: UUID, access: LogisticaAccess = Depends(authorized)):
    return access.resource(Caixa, caixa_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`.

Caminho concreto da fixture: `GET /api/v1/caixas/20f8167b-b764-472c-b022-094b0f7fa24c`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "20f8167b-b764-472c-b022-094b0f7fa24c",
  "created_at": "2026-11-23T14:57:13",
  "updated_at": "2026-11-23T14:57:13",
  "identificacao": "CX-1",
  "codigo_externo": null,
  "peso": null,
  "observacoes": null,
  "carga_id": "00409e0e-85ce-4e98-8cce-5ccb8c8c090f",
  "status": "REGISTRADA"
}
```

Cenário negativo comprovado: HTTP 404, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[caixas]`.

```json
{
  "detail": "Registro nao encontrado."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[cliente-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[produtor-TRANSPORTADORA]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-CLIENTE]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_company_type_change_preserves_logistics[transportadora-PRODUTOR]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_creation_and_detail[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_missing_record[caixas]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[CONSULTA-caixas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[GESTOR-caixas]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_detail_isolation_by_stored_ancestry[OPERADOR-caixas]`

## API-046 — PATCH /api/v1/caixas/{caixa_id}

Update Caixa

- Router/handler: [app/modules/logistica/routes.py:139](../../app/modules/logistica/routes.py#L139) · `update_caixa` · operationId `update_caixa_api_v1_caixas__caixa_id__patch`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: CaixaUpdate.
- Efeito: Criação ou atualização ORM por service, commit/refresh; valida referências e transições. Não há endpoint DELETE.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | caixa_id | True | {   "type": "string",   "format": "uuid",   "title": "Caixa Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CaixaResponse; Successful Response |
| 401 | ; JWT ausente, invalido, expirado ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado. |
| 404 | ; Recurso inexistente. |
| 409 | ; Conflito de integridade ou transportadora inativa para escrita. |
| 422 | HTTPValidationError; Validation Error |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "authorized",
    "module": "app.modules.logistica.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.patch("/caixas/{caixa_id}", response_model=CaixaResponse)
def update_caixa(caixa_id: UUID, data: CaixaUpdate, access: LogisticaAccess = Depends(authorized)):
    return access.update(Caixa, caixa_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`.

Caminho concreto da fixture: `PATCH /api/v1/caixas/99e81a8f-919d-429b-b969-b00686671a62`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "peso": "1.5000",
  "codigo_externo": "codigo-teste"
}
```

Resposta capturada:

```json
{
  "id": "99e81a8f-919d-429b-b969-b00686671a62",
  "created_at": "2026-11-23T14:57:24",
  "updated_at": "2026-11-23T14:57:24",
  "identificacao": "CX-1",
  "codigo_externo": "codigo-teste",
  "peso": "1.5000",
  "observacoes": null,
  "carga_id": "ffc6df8a-b50e-48e0-820a-c6b0f33211dc",
  "status": "REGISTRADA"
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`.

```json
{
  "detail": "Caixa em transito exige carga em transito."
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_cargo_and_box_status_coherence`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data0]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data1]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data2]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_invalid_box_input[data3]`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_new_box_in_cancelled_trip_rejected_without_changing_children`<br>[tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) `test_updates[caixas-data5]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[expired]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[invalid]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_all_27_routes_reject_missing_invalid_or_expired_jwt[missing]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_cargo_and_box_writes_follow_parent_not_request_payload`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_foreign_update_is_denied_and_preserves_record[caixas]`

## API-047 — PUT /api/v1/cargas/{carga_id}/monitoramento

Declarar ou substituir os dados adicionais da carga

PUT idempotente, autorizado para ADMIN/GESTOR/OPERADOR da transportadora.

Identidade Tommy Atkins e lote hipotetico sao declarados pelo operador;
o produto existente da carga nao e renomeado ou inferido por seu nome.

- Router/handler: [app/modules/monitoramento/routes.py:28](../../app/modules/monitoramento/routes.py#L28) · `configurar` · operationId `configurar_api_v1_cargas__carga_id__monitoramento_put`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: CargaMonitoramentoPut.
- Efeito: Declaração versionada/snapshot da sessão e evento auditável; transições explícitas e replay conforme handler.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CargaMonitoramentoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.put("/cargas/{carga_id}/monitoramento", response_model=CargaMonitoramentoResponse,
            summary="Declarar ou substituir os dados adicionais da carga")
def configurar(carga_id: UUID, data: CargaMonitoramentoPut, svc: MonitoramentoService = Depends(service)):
    """PUT idempotente, autorizado para ADMIN/GESTOR/OPERADOR da transportadora.

    Identidade Tommy Atkins e lote hipotetico sao declarados pelo operador;
    o produto existente da carga nao e renomeado ou inferido por seu nome.
    """
    return svc.configurar(carga_id, data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`.

Caminho concreto da fixture: `PUT /api/v1/cargas/a8cfdcd2-0e50-45af-b994-28e3cfc6ddcd/monitoramento`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador."
}
```

Resposta capturada:

```json
{
  "id": "02d060ef-5c3b-4331-92b8-ad031f08567e",
  "created_at": "2026-11-23T14:54:09",
  "updated_at": "2026-11-23T14:54:09",
  "carga_id": "a8cfdcd2-0e50-45af-b994-28e3cfc6ddcd",
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "versao": 1,
  "atualizado_por_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_requires_explicit_cutoff_and_freezes_window`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_without_explicit_end_uses_exact_frozen_cutoff`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_all_readings_are_used_beyond_history_default_page`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[get]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[list]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[post]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_duplicate_request_is_stable_after_new_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_future_conflict_revision_does_not_mutate_old_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_g_not_supplied_is_persisted_configuration_incomplete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_gaps_are_partial_subtotal_never_window_total`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_historical_cut_excludes_later_consolidated_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_conflict_is_context_only`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_invalidity_cannot_change_temperature_calculation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[-1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0.0001]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[Infinity]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[True]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_interior_sample_is_a_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[25]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[9]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes2]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes4]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes5]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes6]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes7]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_locatable_persistence_error_is_a_temperature_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_mass_constraint_rejects_corrupt_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_configuration_is_explicit_conflict`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_no_measurements_and_no_acquisition_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_openapi_documents_three_authenticated_operations`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_out_of_order_input_is_sorted_by_existing_engine`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_precision_tiny_mass_no_binary_float_in_snapshot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_EXPLORATORIO-COMPLETO_NO_MODELO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_RESTRITO-SEM_ESTIMATIVA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_same_timestamp_equal_temperature_does_not_duplicate_exposure`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_snapshot_replays_actual_public_engine_without_live_queries`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[audit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[commit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unknown_maturity_is_not_corrected_and_snapshot_mass_used`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unlocatable_temperature_timestamp_prevents_false_complete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unsealed_revision_cannot_leak_into_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[CONSULTA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[OUTRO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_action_secret_validation_and_justification`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[action]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[get]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[history]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[list]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[request]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_approval_by_admin_and_self_approval_policy_is_explicit`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_clock_regression_rejects_transition_without_partial_state`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_commit_failure_rolls_back_request`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[duracao_planejada_s-value2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[estado-LIGADO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[iniciada_em-value3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[modalidade-FISICA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_failure_is_explicit_simulated_and_terminal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_idempotent_request_and_actions_return_existing_records`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inactive_company_allows_cleanup_but_not_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes0]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes10]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes11]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes12]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes13]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes14]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes15]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes1]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes4]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes5]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes6]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes7]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes8]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes9]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_logical_conflict_and_partial_unique_index`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[AUTORIZADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[EM_EXECUCAO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[SOLICITADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_openapi_is_virtual_authenticated_and_minimal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[AUTORIZAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[INICIAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[RECUSAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[REGISTRAR_FALHA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_precision_and_deadline_are_not_a_scientific_effect`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_replay_after_session_close_keeps_same_history`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[-----BEGIN PRIVATE KEY----- DEMO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[Bearer DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[api_key=DEMONSTRATION_SECRET]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[https://usuario:senha@example.invalid]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[password: DUMMY_PASSWORD]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[token=DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_failure_rolls_back_all_execution_fields`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_without_authorization_and_terminal_reopening_rejected`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transaction_failure_request_and_action_rollback`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_vehicle_change_does_not_move_execution_or_allow_new_start`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_acquires_mapped_fields_and_reuses_existing_measurement_tables`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_binding_snapshot_does_not_follow_later_config_changes`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_replay_is_not_a_new_complementation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_session_requires_explicit_elevated_audited_complement`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_consulta_can_read_history_but_not_incorporate`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_empty_history_and_no_operational_gap_default`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_existing_source_identity_of_other_sensor_is_not_reassigned`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_expired_execution_is_recoverable_and_old_key_is_not_reexecuted`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_global_deduplication_is_backed_by_existing_unique_identity`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_history_pagination_and_type_filter`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[404]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[429]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[500]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_httpx_info_logging_does_not_disclose_read_key`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_idempotency_rejects_different_payload`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change4]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[2026-10-01T12:00:00]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[invalid]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[100000000]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[13.12345]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[Infinity]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[NaN]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[True]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_complement_adds_revision_without_changing_previous_history`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_local_incorporation_does_not_fabricate_late_receipt`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_math_engine_is_not_called`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_midflight_end_requires_a_new_explicit_complement_request`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-leituras-params0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-qualidade-params2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-sincronizacoes-params1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[post-sincronizacoes-params3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_old_thingSpeak_endpoints_and_routes_are_still_registered`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_operational_lateness_limit_is_explicit_and_not_scientific`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_original_measurement_receipt_and_processing_are_distinct`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[leituras]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[qualidade]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[sincronizacoes]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_out_of_order_readings_are_sorted_without_changing_their_times`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_network_failure_preserves_already_received_pages`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_persistence_failure_keeps_the_other_fields`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_quality_requires_positive_operational_gap`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_queries_cannot_extend_session_window`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_repeat_sync_and_same_request_do_not_duplicate_readings`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_request_budget_reports_partial_instead_of_silent_truncation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_reuses_legacy_external_history_without_fabricating_receipt_time`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_running_request_replay_returns_202_and_second_key_is_blocked`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_conflicting_values_block_coverage_without_overwriting`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_same_value_is_not_double_exposure`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_session_window_filters_before_and_after_and_keeps_endpoint_sample`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_source_payload_conflict_creates_new_revision_not_a_value_overwrite`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_split_historical_requests_recover_more_than_one_page`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_temporal_gaps_are_not_filled`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[CONSULTA]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[OUTRO]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unrelated_channel_fields_are_not_imported`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_wrong_sensor_mapping_is_rejected_before_network`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_all_maturity_stages[DESCONHECIDA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_all_maturity_stages[EM_AMADURECIMENTO]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_all_maturity_stages[MADURA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_all_maturity_stages[MISTA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_all_maturity_stages[VERDE_MADURA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[ADMIN]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[GESTOR]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[OPERADOR]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>3]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_cancelled_sessions_reserve_their_historical_window`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_config_put_is_idempotent_and_versioned`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_configure_preserves_legacy_cargo_and_product`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_lifecycle_check_rejects_terminal_session_without_end`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_partial_uniqueness_rejects_duplicate_active_session`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_rejects_wrong_trip_even_with_existing_foreign_keys`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes3]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes4]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_declaration_validation[changes5]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[put-/cargas/{cargo}/monitoramento-config]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[cancelar-CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[encerrar-ENCERRADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_historical_overlap_rejected_and_next_adjacent_window_allowed`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_humidity_sensor_is_optional`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_idempotency_key_different_content_conflicts`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_inactive_identity_membership_or_company_denied[company]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_inactive_identity_membership_or_company_denied[membership]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_inactive_identity_membership_or_company_denied[user]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[-1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[0.00001]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[100000000]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[Infinity]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[NaN]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[None]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_invalid_mass_rejected_without_persistence[True]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[config]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_cargo]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_trip]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[session]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[start]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_same_creation_key_is_idempotent_even_after_end`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_same_source_cannot_monitor_two_cargos_simultaneously`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_second_active_session_of_same_cargo_conflicts`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_session_end_must_not_exceed_real_trip_arrival`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[inactive_device-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[inactive_sensor-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[missing-404]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[other_context-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[prototype-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[same-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[unit-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[wrong_type-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_records_real_window_cargo_trip_and_source_snapshot`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[CONCLUIDA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[PLANEJADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[ENTREGUE]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[PLANEJADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_terminal_session_has_no_implicit_measurement_association_endpoint`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_unbound_sensor_requires_admin_and_laboratory`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_unknown_profile_is_denied`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_unknown_stage_when_not_informed`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_valid_mass_limits[0.0001]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_valid_mass_limits[1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_valid_mass_limits[99999999.9999]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_idempotency_and_role`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_historical_cut_and_running_revision_exclude_future_data`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes0]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes10]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes11]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes12]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes13]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes1]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes2]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes3]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes4]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes5]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes6]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes7]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes8]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes9]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_no_readings_never_means_safe`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/alertas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/avaliacoes-preventivas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/configuracoes-ambientais]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_secured_logistics_preserves_monitoring_snapshot_and_scope`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`

## API-048 — GET /api/v1/cargas/{carga_id}/monitoramento

Consultar os dados adicionais de monitoramento

- Router/handler: [app/modules/monitoramento/routes.py:39](../../app/modules/monitoramento/routes.py#L39) · `configuracao` · operationId `configuracao_api_v1_cargas__carga_id__monitoramento_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | CargaMonitoramentoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/cargas/{carga_id}/monitoramento", response_model=CargaMonitoramentoResponse,
            summary="Consultar os dados adicionais de monitoramento")
def configuracao(carga_id: UUID, svc: MonitoramentoService = Depends(service)):
    return svc.consultar_configuracao(carga_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`.

Caminho concreto da fixture: `GET /api/v1/cargas/919fb95e-b852-4315-8912-4a8a51011524/monitoramento`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "0793b53d-ad65-4de1-bec3-0fff5de343da",
  "created_at": "2026-11-23T14:58:38",
  "updated_at": "2026-11-23T14:58:38",
  "carga_id": "919fb95e-b852-4315-8912-4a8a51011524",
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "versao": 1,
  "atualizado_por_id": "90dae862-a29a-4019-86d5-68a76467d5b9"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[get-/cargas/{cargo}/monitoramento-None]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_legacy_cargo_still_works_without_monitoring_configuration`

## API-049 — POST /api/v1/cargas/{carga_id}/monitoramentos

Iniciar uma sessao com janela efetiva explicita

Exige viagem EM_ANDAMENTO, carga EM_TRANSITO e configuracao valida.

Chave idempotente por usuario; repeticao igual retorna 200, conteudo diferente 409.
Inicio nao e a data de cadastro. Nao consulta ou associa medicoes.

- Router/handler: [app/modules/monitoramento/routes.py:45](../../app/modules/monitoramento/routes.py#L45) · `iniciar` · operationId `iniciar_api_v1_cargas__carga_id__monitoramentos_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: SessaoCreate.
- Efeito: Declaração versionada/snapshot da sessão e evento auditável; transições explícitas e replay conforme handler.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 201 | SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 200 | SessaoResponse-Input; Repeticao idempotente da criacao. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/cargas/{carga_id}/monitoramentos", response_model=SessaoResponse, status_code=201,
             responses={200: {"model": SessaoResponse, "description": "Repeticao idempotente da criacao."}},
             summary="Iniciar uma sessao com janela efetiva explicita")
def iniciar(carga_id: UUID, data: SessaoCreate, response: HttpResponse,
            svc: MonitoramentoService = Depends(service)):
    """Exige viagem EM_ANDAMENTO, carga EM_TRANSITO e configuracao valida.

    Chave idempotente por usuario; repeticao igual retorna 200, conteudo diferente 409.
    Inicio nao e a data de cadastro. Nao consulta ou associa medicoes.
    """
    sessao, criada = svc.criar_sessao(carga_id, data)
    response.status_code = 201 if criada else 200
    return sessao

```

Cenário de sucesso comprovado: HTTP 201, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`.

Caminho concreto da fixture: `POST /api/v1/cargas/a8cfdcd2-0e50-45af-b994-28e3cfc6ddcd/monitoramentos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "inicio": "2026-11-23T11:04:05.435676+00:00",
  "sensor_temperatura_id": "67a0548e-5508-423d-8007-4316cd532ef7",
  "sensor_umidade_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "chave_idempotencia": "7425b4af-7b91-47b3-bd92-4b69363c4d03"
}
```

Resposta capturada:

```json
{
  "id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
  "created_at": "2026-11-23T14:54:09",
  "updated_at": "2026-11-23T14:54:09",
  "carga_id": "a8cfdcd2-0e50-45af-b994-28e3cfc6ddcd",
  "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
  "configuracao_id": "02d060ef-5c3b-4331-92b8-ad031f08567e",
  "inicio": "2026-11-23T11:04:05.435676",
  "fim": null,
  "estado": "ATIVA",
  "sensor_temperatura_id": "67a0548e-5508-423d-8007-4316cd532ef7",
  "sensor_umidade_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "observacoes": null,
  "configuracao_versao": 1,
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "origem_sensor": {
    "temperatura": {
      "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
      "identificador": "TEMP",
      "tipo": "TEMPERATURA",
      "contexto": "AMBIENTE",
      "unidade": "C",
      "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
        "carga_id": null,
        "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
      }
    },
    "umidade": {
      "sensor_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
      "identificador": "HUM",
      "tipo": "UMIDADE",
      "contexto": "AMBIENTE",
      "unidade": "%",
      "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
        "carga_id": null,
        "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
      }
    }
  },
  "criada_por_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf",
  "finalizada_por_id": null,
  "motivo_fim": null,
  "chave_idempotencia": "7425b4af-7b91-47b3-bd92-4b69363c4d03"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 201, 401, 403, 404, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_requires_explicit_cutoff_and_freezes_window`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_without_explicit_end_uses_exact_frozen_cutoff`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_all_readings_are_used_beyond_history_default_page`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[get]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[list]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[post]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_duplicate_request_is_stable_after_new_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_future_conflict_revision_does_not_mutate_old_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_g_not_supplied_is_persisted_configuration_incomplete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_gaps_are_partial_subtotal_never_window_total`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_historical_cut_excludes_later_consolidated_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_conflict_is_context_only`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_invalidity_cannot_change_temperature_calculation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[-1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0.0001]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[Infinity]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[True]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_interior_sample_is_a_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[25]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[9]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes2]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes4]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes5]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes6]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes7]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_locatable_persistence_error_is_a_temperature_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_mass_constraint_rejects_corrupt_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_configuration_is_explicit_conflict`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_no_measurements_and_no_acquisition_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_openapi_documents_three_authenticated_operations`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_out_of_order_input_is_sorted_by_existing_engine`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_precision_tiny_mass_no_binary_float_in_snapshot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_EXPLORATORIO-COMPLETO_NO_MODELO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_RESTRITO-SEM_ESTIMATIVA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_same_timestamp_equal_temperature_does_not_duplicate_exposure`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_snapshot_replays_actual_public_engine_without_live_queries`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[audit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[commit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unknown_maturity_is_not_corrected_and_snapshot_mass_used`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unlocatable_temperature_timestamp_prevents_false_complete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unsealed_revision_cannot_leak_into_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[CONSULTA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[OUTRO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_action_secret_validation_and_justification`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[action]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[get]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[history]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[list]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[request]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_approval_by_admin_and_self_approval_policy_is_explicit`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_clock_regression_rejects_transition_without_partial_state`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_commit_failure_rolls_back_request`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[duracao_planejada_s-value2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[estado-LIGADO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[iniciada_em-value3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[modalidade-FISICA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_failure_is_explicit_simulated_and_terminal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_idempotent_request_and_actions_return_existing_records`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inactive_company_allows_cleanup_but_not_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes0]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes10]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes11]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes12]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes13]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes14]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes15]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes1]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes4]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes5]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes6]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes7]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes8]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes9]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_logical_conflict_and_partial_unique_index`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[AUTORIZADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[EM_EXECUCAO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[SOLICITADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_openapi_is_virtual_authenticated_and_minimal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[AUTORIZAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[INICIAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[RECUSAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[REGISTRAR_FALHA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_precision_and_deadline_are_not_a_scientific_effect`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_replay_after_session_close_keeps_same_history`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[-----BEGIN PRIVATE KEY----- DEMO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[Bearer DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[api_key=DEMONSTRATION_SECRET]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[https://usuario:senha@example.invalid]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[password: DUMMY_PASSWORD]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[token=DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_failure_rolls_back_all_execution_fields`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_without_authorization_and_terminal_reopening_rejected`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transaction_failure_request_and_action_rollback`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_vehicle_change_does_not_move_execution_or_allow_new_start`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_acquires_mapped_fields_and_reuses_existing_measurement_tables`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_binding_snapshot_does_not_follow_later_config_changes`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_replay_is_not_a_new_complementation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_session_requires_explicit_elevated_audited_complement`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_consulta_can_read_history_but_not_incorporate`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_empty_history_and_no_operational_gap_default`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_existing_source_identity_of_other_sensor_is_not_reassigned`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_expired_execution_is_recoverable_and_old_key_is_not_reexecuted`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_global_deduplication_is_backed_by_existing_unique_identity`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_history_pagination_and_type_filter`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[404]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[429]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[500]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_httpx_info_logging_does_not_disclose_read_key`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_idempotency_rejects_different_payload`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change4]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[2026-10-01T12:00:00]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[invalid]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[100000000]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[13.12345]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[Infinity]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[NaN]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[True]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_complement_adds_revision_without_changing_previous_history`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_local_incorporation_does_not_fabricate_late_receipt`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_math_engine_is_not_called`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_midflight_end_requires_a_new_explicit_complement_request`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-leituras-params0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-qualidade-params2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-sincronizacoes-params1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[post-sincronizacoes-params3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_old_thingSpeak_endpoints_and_routes_are_still_registered`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_operational_lateness_limit_is_explicit_and_not_scientific`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_original_measurement_receipt_and_processing_are_distinct`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[leituras]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[qualidade]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[sincronizacoes]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_out_of_order_readings_are_sorted_without_changing_their_times`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_network_failure_preserves_already_received_pages`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_persistence_failure_keeps_the_other_fields`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_quality_requires_positive_operational_gap`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_queries_cannot_extend_session_window`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_repeat_sync_and_same_request_do_not_duplicate_readings`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_request_budget_reports_partial_instead_of_silent_truncation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_reuses_legacy_external_history_without_fabricating_receipt_time`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_running_request_replay_returns_202_and_second_key_is_blocked`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_conflicting_values_block_coverage_without_overwriting`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_same_value_is_not_double_exposure`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_session_window_filters_before_and_after_and_keeps_endpoint_sample`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_source_payload_conflict_creates_new_revision_not_a_value_overwrite`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_split_historical_requests_recover_more_than_one_page`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_temporal_gaps_are_not_filled`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[CONSULTA]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[OUTRO]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unrelated_channel_fields_are_not_imported`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_wrong_sensor_mapping_is_rejected_before_network`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[ADMIN]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[GESTOR]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_allowed_roles_can_configure_and_start[OPERADOR]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>3]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_cancelled_sessions_reserve_their_historical_window`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_lifecycle_check_rejects_terminal_session_without_end`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_partial_uniqueness_rejects_duplicate_active_session`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_database_rejects_wrong_trip_even_with_existing_foreign_keys`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[post-/cargas/{cargo}/monitoramentos-start]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[cancelar-CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[encerrar-ENCERRADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_historical_overlap_rejected_and_next_adjacent_window_allowed`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_humidity_sensor_is_optional`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_idempotency_key_different_content_conflicts`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[config]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_cargo]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_trip]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[session]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[start]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_same_creation_key_is_idempotent_even_after_end`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_same_source_cannot_monitor_two_cargos_simultaneously`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_second_active_session_of_same_cargo_conflicts`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_session_end_must_not_exceed_real_trip_arrival`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[inactive_device-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[inactive_sensor-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[missing-404]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[other_context-409]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[prototype-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[same-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[unit-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_source_validation[wrong_type-422]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_records_real_window_cargo_trip_and_source_snapshot`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_rejects_bad_times[<lambda>2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_configuration`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[CONCLUIDA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_progress_trip[PLANEJADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[ENTREGUE]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_start_requires_in_transit_cargo[PLANEJADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_terminal_session_has_no_implicit_measurement_association_endpoint`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_unbound_sensor_requires_admin_and_laboratory`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_idempotency_and_role`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_historical_cut_and_running_revision_exclude_future_data`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes0]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes10]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes11]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes12]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes13]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes1]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes2]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes3]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes4]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes5]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes6]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes7]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes8]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes9]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_no_readings_never_means_safe`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/alertas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/avaliacoes-preventivas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/configuracoes-ambientais]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_secured_logistics_preserves_monitoring_snapshot_and_scope`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`

## API-050 — GET /api/v1/cargas/{carga_id}/monitoramentos

Listar sessoes da carga com paginacao

- Router/handler: [app/modules/monitoramento/routes.py:60](../../app/modules/monitoramento/routes.py#L60) · `listar_carga` · operationId `listar_carga_api_v1_cargas__carga_id__monitoramentos_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | carga_id | True | {   "type": "string",   "format": "uuid",   "title": "Carga Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/cargas/{carga_id}/monitoramentos", response_model=list[SessaoResponse],
            summary="Listar sessoes da carga com paginacao")
def listar_carga(carga_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                 svc: MonitoramentoService = Depends(service)):
    return svc.listar_carga(carga_id, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`.

Caminho concreto da fixture: `GET /api/v1/cargas/78bc3b93-6a00-4dd5-b58d-18e9cb1e26f5/monitoramentos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "eb50e606-bde3-4bfc-873d-4f62ae76baaa",
    "created_at": "2026-11-23T14:58:44",
    "updated_at": "2026-11-23T14:58:44",
    "carga_id": "78bc3b93-6a00-4dd5-b58d-18e9cb1e26f5",
    "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
    "configuracao_id": "2195e5eb-0cbb-4d14-b393-014d4276233c",
    "inicio": "2026-11-23T11:34:05.435676",
    "fim": null,
    "estado": "ATIVA",
    "sensor_temperatura_id": "3fbac5fd-b6a0-4209-b528-1960a90ebdef",
    "sensor_umidade_id": "fa4db231-42b0-49b8-a1ea-807f37ed8f61",
    "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
    "observacoes": null,
    "configuracao_versao": 1,
    "produto_identificado": "MANGA_TOMMY_ATKINS",
    "massa_kg": "1000.0000",
    "maturacao": "MISTA",
    "lote_codigo": "DEMO-001",
    "lote_hipotetico": true,
    "rastreabilidade": "Lote hipotetico; declaracao do operador.",
    "origem_sensor": {
      "temperatura": {
        "sensor_id": "3fbac5fd-b6a0-4209-b528-1960a90ebdef",
        "identificador": "TEMP",
        "tipo": "TEMPERATURA",
        "contexto": "AMBIENTE",
        "unidade": "C",
        "dispositivo_id": "5e528fd0-4eb6-4cfc-b706-1558f11806f8",
        "dispositivo": "ESP-1",
        "vinculos": {
          "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
          "carga_id": null,
          "veiculo_id": "c0586221-48da-4d19-83cb-1c2da78f8660"
        }
      },
      "umidade": {
        "sensor_id": "fa4db231-42b0-49b8-a1ea-807f37ed8f61",
        "identificador": "HUM",
        "tipo": "UMIDADE",
        "contexto": "AMBIENTE",
        "unidade": "%",
        "dispositivo_id": "5e528fd0-4eb6-4cfc-b706-1558f11806f8",
        "dispositivo": "ESP-1",
        "vinculos": {
          "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
          "carga_id": null,
          "veiculo_id": "c0586221-48da-4d19-83cb-1c2da78f8660"
        }
      }
    },
    "criada_por_id": "5f76363d-99ed-4a4e-8188-36cf0f804b97",
    "finalizada_por_id": null,
    "motivo_fim": null,
    "chave_idempotencia": "5e2174fd-8864-4df3-b023-1ca496756c37"
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[get-/cargas/{cargo}/monitoramentos-None]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_cargo]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_unknown_profile_is_denied`

## API-051 — GET /api/v1/viagens/{viagem_id}/monitoramentos

Listar sessoes da viagem com paginacao

- Router/handler: [app/modules/monitoramento/routes.py:67](../../app/modules/monitoramento/routes.py#L67) · `listar_viagem` · operationId `listar_viagem_api_v1_viagens__viagem_id__monitoramentos_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | viagem_id | True | {   "type": "string",   "format": "uuid",   "title": "Viagem Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 50,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | lista de SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/viagens/{viagem_id}/monitoramentos", response_model=list[SessaoResponse],
            summary="Listar sessoes da viagem com paginacao")
def listar_viagem(viagem_id: UUID, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0),
                  svc: MonitoramentoService = Depends(service)):
    return svc.listar_viagem(viagem_id, limit, offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`.

Caminho concreto da fixture: `GET /api/v1/viagens/ed0a91c4-185a-4c4f-8c2d-87728007aaf5/monitoramentos`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
[
  {
    "id": "eb50e606-bde3-4bfc-873d-4f62ae76baaa",
    "created_at": "2026-11-23T14:58:44",
    "updated_at": "2026-11-23T14:58:44",
    "carga_id": "78bc3b93-6a00-4dd5-b58d-18e9cb1e26f5",
    "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
    "configuracao_id": "2195e5eb-0cbb-4d14-b393-014d4276233c",
    "inicio": "2026-11-23T11:34:05.435676",
    "fim": null,
    "estado": "ATIVA",
    "sensor_temperatura_id": "3fbac5fd-b6a0-4209-b528-1960a90ebdef",
    "sensor_umidade_id": "fa4db231-42b0-49b8-a1ea-807f37ed8f61",
    "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
    "observacoes": null,
    "configuracao_versao": 1,
    "produto_identificado": "MANGA_TOMMY_ATKINS",
    "massa_kg": "1000.0000",
    "maturacao": "MISTA",
    "lote_codigo": "DEMO-001",
    "lote_hipotetico": true,
    "rastreabilidade": "Lote hipotetico; declaracao do operador.",
    "origem_sensor": {
      "temperatura": {
        "sensor_id": "3fbac5fd-b6a0-4209-b528-1960a90ebdef",
        "identificador": "TEMP",
        "tipo": "TEMPERATURA",
        "contexto": "AMBIENTE",
        "unidade": "C",
        "dispositivo_id": "5e528fd0-4eb6-4cfc-b706-1558f11806f8",
        "dispositivo": "ESP-1",
        "vinculos": {
          "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
          "carga_id": null,
          "veiculo_id": "c0586221-48da-4d19-83cb-1c2da78f8660"
        }
      },
      "umidade": {
        "sensor_id": "fa4db231-42b0-49b8-a1ea-807f37ed8f61",
        "identificador": "HUM",
        "tipo": "UMIDADE",
        "contexto": "AMBIENTE",
        "unidade": "%",
        "dispositivo_id": "5e528fd0-4eb6-4cfc-b706-1558f11806f8",
        "dispositivo": "ESP-1",
        "vinculos": {
          "viagem_id": "ed0a91c4-185a-4c4f-8c2d-87728007aaf5",
          "carga_id": null,
          "veiculo_id": "c0586221-48da-4d19-83cb-1c2da78f8660"
        }
      }
    },
    "criada_por_id": "5f76363d-99ed-4a4e-8188-36cf0f804b97",
    "finalizada_por_id": null,
    "motivo_fim": null,
    "chave_idempotencia": "5e2174fd-8864-4df3-b023-1ca496756c37"
  }
]
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[get-/viagens/{trip}/monitoramentos-None]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[list_trip]`

## API-052 — GET /api/v1/monitoramentos/{sessao_id}

Consultar a sessao e seu snapshot de rastreabilidade

- Router/handler: [app/modules/monitoramento/routes.py:74](../../app/modules/monitoramento/routes.py#L74) · `consultar` · operationId `consultar_api_v1_monitoramentos__sessao_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get("/monitoramentos/{sessao_id}", response_model=SessaoResponse,
            summary="Consultar a sessao e seu snapshot de rastreabilidade")
def consultar(sessao_id: UUID, svc: MonitoramentoService = Depends(service)):
    return svc.consultar_sessao(sessao_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/e758bc5d-4a23-4328-b387-17845e4e4ff7`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "e758bc5d-4a23-4328-b387-17845e4e4ff7",
  "created_at": "2026-11-23T14:58:31",
  "updated_at": "2026-11-23T14:58:32",
  "carga_id": "b4c21750-9190-4e83-9ce6-7b3facd30739",
  "viagem_id": "45bdc786-db2d-446b-bff5-2ebdb48ed4ee",
  "configuracao_id": "d74e5572-f3bf-407d-94f3-c0011f1eef03",
  "inicio": "2026-11-23T11:04:05.435676",
  "fim": "2026-11-23T11:34:05.435676",
  "estado": "ENCERRADA",
  "sensor_temperatura_id": "c22c0dc1-2b1e-4ab5-8b61-e96d9b9b5467",
  "sensor_umidade_id": "1939cb62-a2ef-4abf-848f-b97149e02d2e",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "observacoes": null,
  "configuracao_versao": 1,
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "origem_sensor": {
    "temperatura": {
      "sensor_id": "c22c0dc1-2b1e-4ab5-8b61-e96d9b9b5467",
      "identificador": "TEMP",
      "tipo": "TEMPERATURA",
      "contexto": "AMBIENTE",
      "unidade": "C",
      "dispositivo_id": "b5bd81fa-7ebd-432f-99a2-a8039f0ce8ee",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "45bdc786-db2d-446b-bff5-2ebdb48ed4ee",
        "carga_id": null,
        "veiculo_id": "644d199f-cd3c-4dda-b1dd-bd7b2ec2f568"
      }
    },
    "umidade": {
      "sensor_id": "1939cb62-a2ef-4abf-848f-b97149e02d2e",
      "identificador": "HUM",
      "tipo": "UMIDADE",
      "contexto": "AMBIENTE",
      "unidade": "%",
      "dispositivo_id": "b5bd81fa-7ebd-432f-99a2-a8039f0ce8ee",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "45bdc786-db2d-446b-bff5-2ebdb48ed4ee",
        "carga_id": null,
        "veiculo_id": "644d199f-cd3c-4dda-b1dd-bd7b2ec2f568"
      }
    }
  },
  "criada_por_id": "76e77141-fb74-49c6-8cac-7465e9e9ac6a",
  "finalizada_por_id": "76e77141-fb74-49c6-8cac-7465e9e9ac6a",
  "motivo_fim": "Operacao registrada",
  "chave_idempotencia": "8f83973f-afb7-487c-908b-a29681965785"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[get-/monitoramentos/{session}-None]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_other_company_cannot_access_objects_or_lists[session]`<br>[tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) `test_secured_logistics_preserves_monitoring_snapshot_and_scope`

## API-053 — POST /api/v1/monitoramentos/{sessao_id}/encerrar

Encerrar uma sessao ativa, com horario e motivo

Transicao imutavel e auditada. Repeticao identica e idempotente.

- Router/handler: [app/modules/monitoramento/routes.py:80](../../app/modules/monitoramento/routes.py#L80) · `encerrar` · operationId `encerrar_api_v1_monitoramentos__sessao_id__encerrar_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: SessaoFinalizar.
- Efeito: Declaração versionada/snapshot da sessão e evento auditável; transições explícitas e replay conforme handler.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/monitoramentos/{sessao_id}/encerrar", response_model=SessaoResponse,
             summary="Encerrar uma sessao ativa, com horario e motivo")
def encerrar(sessao_id: UUID, data: SessaoFinalizar, svc: MonitoramentoService = Depends(service)):
    """Transicao imutavel e auditada. Repeticao identica e idempotente."""
    return svc.finalizar(sessao_id, data, "ENCERRADA")

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/5efd78a3-01e1-4ef3-b984-c025a734ef37/encerrar`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "motivo": "Operacao registrada"
}
```

Resposta capturada:

```json
{
  "id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
  "created_at": "2026-11-23T14:54:09",
  "updated_at": "2026-11-23T14:54:09",
  "carga_id": "a8cfdcd2-0e50-45af-b994-28e3cfc6ddcd",
  "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
  "configuracao_id": "02d060ef-5c3b-4331-92b8-ad031f08567e",
  "inicio": "2026-11-23T11:04:05.435676",
  "fim": "2026-11-23T13:04:05.435676",
  "estado": "ENCERRADA",
  "sensor_temperatura_id": "67a0548e-5508-423d-8007-4316cd532ef7",
  "sensor_umidade_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "observacoes": null,
  "configuracao_versao": 1,
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "origem_sensor": {
    "temperatura": {
      "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
      "identificador": "TEMP",
      "tipo": "TEMPERATURA",
      "contexto": "AMBIENTE",
      "unidade": "C",
      "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
        "carga_id": null,
        "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
      }
    },
    "umidade": {
      "sensor_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
      "identificador": "HUM",
      "tipo": "UMIDADE",
      "contexto": "AMBIENTE",
      "unidade": "%",
      "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
        "carga_id": null,
        "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
      }
    }
  },
  "criada_por_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf",
  "finalizada_por_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf",
  "motivo_fim": "Operacao registrada",
  "chave_idempotencia": "7425b4af-7b91-47b3-bd92-4b69363c4d03"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_all_readings_are_used_beyond_history_default_page`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_g_not_supplied_is_persisted_configuration_incomplete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_gaps_are_partial_subtotal_never_window_total`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_invalidity_cannot_change_temperature_calculation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_interior_sample_is_a_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[25]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[9]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes2]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes4]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes5]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes6]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes7]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_out_of_order_input_is_sorted_by_existing_engine`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_precision_tiny_mass_no_binary_float_in_snapshot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_EXPLORATORIO-COMPLETO_NO_MODELO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_RESTRITO-SEM_ESTIMATIVA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_same_timestamp_equal_temperature_does_not_duplicate_exposure`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_snapshot_replays_actual_public_engine_without_live_queries`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[audit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[commit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unknown_maturity_is_not_corrected_and_snapshot_mass_used`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unlocatable_temperature_timestamp_prevents_false_complete`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_replay_after_session_close_keeps_same_history`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_replay_is_not_a_new_complementation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_session_requires_explicit_elevated_audited_complement`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_complement_adds_revision_without_changing_previous_history`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_local_incorporation_does_not_fabricate_late_receipt`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_queries_cannot_extend_session_window`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_session_window_filters_before_and_after_and_keeps_endpoint_sample`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_active_configuration_frozen_but_terminal_snapshot_survives_later_edit`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>0]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>1]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>2]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_bad_final_times_do_not_change_session[<lambda>3]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_consulta_can_read_but_not_write`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[post-/monitoramentos/{session}/encerrar-end]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[cancelar-CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[encerrar-ENCERRADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_historical_overlap_rejected_and_next_adjacent_window_allowed`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_lists_are_scoped_paginated_and_stably_ordered`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_same_creation_key_is_idempotent_even_after_end`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_session_end_must_not_exceed_real_trip_arrival`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_terminal_session_has_no_implicit_measurement_association_endpoint`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`

## API-054 — POST /api/v1/monitoramentos/{sessao_id}/cancelar

Cancelar uma sessao ativa, sem apagar sua janela historica

- Router/handler: [app/modules/monitoramento/routes.py:87](../../app/modules/monitoramento/routes.py#L87) · `cancelar` · operationId `cancelar_api_v1_monitoramentos__sessao_id__cancelar_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: SessaoFinalizar.
- Efeito: Declaração versionada/snapshot da sessão e evento auditável; transições explícitas e replay conforme handler.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | SessaoResponse-Output; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "service",
    "module": "app.modules.monitoramento.routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post("/monitoramentos/{sessao_id}/cancelar", response_model=SessaoResponse,
             summary="Cancelar uma sessao ativa, sem apagar sua janela historica")
def cancelar(sessao_id: UUID, data: SessaoFinalizar, svc: MonitoramentoService = Depends(service)):
    return svc.finalizar(sessao_id, data, "CANCELADA")

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/8ab2c429-694f-426e-b39b-1d7f3eefdc64/cancelar`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "motivo": "Operacao registrada"
}
```

Resposta capturada:

```json
{
  "id": "8ab2c429-694f-426e-b39b-1d7f3eefdc64",
  "created_at": "2026-11-23T14:54:31",
  "updated_at": "2026-11-23T14:54:31",
  "carga_id": "ec272d56-f221-457a-a0ca-48d2579647c8",
  "viagem_id": "3a4cce76-8244-43da-a2f1-d28477d5b6cc",
  "configuracao_id": "e8501da8-bffa-4f68-9c1e-80b9c594fab5",
  "inicio": "2026-11-23T11:04:05.435676",
  "fim": "2026-11-23T13:04:05.435676",
  "estado": "CANCELADA",
  "sensor_temperatura_id": "500ff15f-a49a-4160-b1be-a86a545bd736",
  "sensor_umidade_id": "9c4c3843-59be-4918-9999-426124a65391",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "observacoes": null,
  "configuracao_versao": 1,
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Lote hipotetico; declaracao do operador.",
  "origem_sensor": {
    "temperatura": {
      "sensor_id": "500ff15f-a49a-4160-b1be-a86a545bd736",
      "identificador": "TEMP",
      "tipo": "TEMPERATURA",
      "contexto": "AMBIENTE",
      "unidade": "C",
      "dispositivo_id": "72b6c87b-d1f7-4c4d-bfc6-802848bae8f8",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "3a4cce76-8244-43da-a2f1-d28477d5b6cc",
        "carga_id": null,
        "veiculo_id": "bbd91185-8c41-4574-bec9-1480107f4d77"
      }
    },
    "umidade": {
      "sensor_id": "9c4c3843-59be-4918-9999-426124a65391",
      "identificador": "HUM",
      "tipo": "UMIDADE",
      "contexto": "AMBIENTE",
      "unidade": "%",
      "dispositivo_id": "72b6c87b-d1f7-4c4d-bfc6-802848bae8f8",
      "dispositivo": "ESP-1",
      "vinculos": {
        "viagem_id": "3a4cce76-8244-43da-a2f1-d28477d5b6cc",
        "carga_id": null,
        "veiculo_id": "bbd91185-8c41-4574-bec9-1480107f4d77"
      }
    }
  },
  "criada_por_id": "ad5e62dc-50b5-4fe0-82ce-013c79bfd22c",
  "finalizada_por_id": "ad5e62dc-50b5-4fe0-82ce-013c79bfd22c",
  "motivo_fim": "Operacao registrada",
  "chave_idempotencia": "e5629c3d-d856-44de-ad00-22d621e7820f"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 409.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_cancelled_sessions_reserve_their_historical_window`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_every_new_endpoint_requires_authentication[post-/monitoramentos/{session}/cancelar-end]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[cancelar-CANCELADA]`<br>[tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) `test_finish_is_audited_and_idempotent[encerrar-ENCERRADA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`

## API-055 — POST /api/v1/monitoramentos/{sessao_id}/sincronizacoes

Sincronizar explicitamente o historico de uma sessao

THINGSPEAK usa o cliente existente; BANCO reassocia somente medicoes externas da origem fixada.

Encerrada exige complementar_encerrada, justificativa e ADMIN/GESTOR. Cancelada nao recebe dados.
Falha de aquisicao retorna estado FALHA/PARCIAL auditado; nao e confundida com sucesso de coleta.

- Router/handler: [app/modules/monitoramento/historico_routes.py:32](../../app/modules/monitoramento/historico_routes.py#L32) · `sincronizar` · operationId `sincronizar_api_v1_monitoramentos__sessao_id__sincronizacoes_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: SincronizacaoCreate.
- Efeito: Persiste tentativa, origem fixada, leituras/medicoes, incorporações e ocorrências; versões anteriores preservadas; falha pode ser estado FALHA/PARCIAL com HTTP 200.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | SincronizacaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 202 | SincronizacaoResponse; A mesma requisicao ainda esta em execucao. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "get_database_session",
    "module": "app.api.deps",
    "children": []
  },
  {
    "call": "get_current_user",
    "module": "app.api.deps",
    "children": [
      {
        "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
        "module": "fastapi.security.http",
        "children": []
      },
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      }
    ]
  },
  {
    "call": "thingspeak_service",
    "module": "app.modules.monitoramento.historico_routes",
    "children": []
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/{sessao_id}/sincronizacoes',response_model=SincronizacaoResponse,
             responses={202:{'model':SincronizacaoResponse,'description':'A mesma requisicao ainda esta em execucao.'}},
             summary='Sincronizar explicitamente o historico de uma sessao')
async def sincronizar(sessao_id:UUID,data:SincronizacaoCreate,response:Response,
                     db:Session=Depends(get_database_session),user:Usuario=Depends(get_current_user),
                     thingspeak=Depends(thingspeak_service)):
    """THINGSPEAK usa o cliente existente; BANCO reassocia somente medicoes externas da origem fixada.

    Encerrada exige complementar_encerrada, justificativa e ADMIN/GESTOR. Cancelada nao recebe dados.
    Falha de aquisicao retorna estado FALHA/PARCIAL auditado; nao e confundida com sucesso de coleta.
    """
    run=await HistoricoIoTService(db,user,thingspeak).sincronizar(sessao_id,data)
    if run.estado=='EM_EXECUCAO': response.status_code=202
    return run

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/5efd78a3-01e1-4ef3-b984-c025a734ef37/sincronizacoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "7eb10ec0-1c21-4f83-84f7-5e918c1aed7c"
}
```

Resposta capturada:

```json
{
  "id": "e62bba26-2c89-4bca-8458-9569c1f53f1d",
  "created_at": "2026-11-23T14:54:09",
  "updated_at": "2026-11-23T14:54:09",
  "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
  "usuario_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf",
  "revisao": 1,
  "chave_idempotencia": "7eb10ec0-1c21-4f83-84f7-5e918c1aed7c",
  "origem_dados": "THINGSPEAK",
  "estado": "CONCLUIDA",
  "inicio_janela": "2026-11-23T11:04:05.435676",
  "fim_janela": "2026-11-23T14:54:09.789094",
  "iniciada_em": "2026-11-23T14:54:09.789094",
  "finalizada_em": "2026-11-23T14:54:09.860475",
  "expira_em": "2026-11-23T14:55:25.789094",
  "complementacao": false,
  "justificativa": null,
  "resumo": {
    "janela_sessao_inicio": "2026-11-23T11:04:05.435676+00:00",
    "janela_sessao_fim": "2026-11-23T14:54:09.789094+00:00",
    "estado_sessao": "ATIVA",
    "limite_atraso_s": null,
    "limite_requisicoes": 16,
    "fontes": [
      {
        "id": "c0154340-5081-49b4-a63a-3a2f035aa469",
        "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
        "channel_id": "12345",
        "field_name": "field4",
        "tipo": "TEMPERATURA",
        "unidade": "C"
      },
      {
        "id": "5f26d909-e0b2-4fa1-a615-03cc0c961541",
        "sensor_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
        "channel_id": "12345",
        "field_name": "field7",
        "tipo": "UMIDADE",
        "unidade": "%"
      }
    ],
    "novas": 6,
    "duplicadas": 0,
    "invalidas": 0,
    "fora_janela": 0,
    "erros": 0,
    "tardias": 0,
    "fora_de_ordem": 0,
    "requisicoes": 1,
    "feeds_recebidos": 3
  }
}
```

Cenário negativo comprovado: HTTP 409, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_idempotency_rejects_different_payload`.

```json
{
  "detail": "Chave idempotente reutilizada com outro conteudo ou autor."
}
```

Matriz de respostas observadas: 200, 202, 401, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_requires_explicit_cutoff_and_freezes_window`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_without_explicit_end_uses_exact_frozen_cutoff`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_all_readings_are_used_beyond_history_default_page`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_duplicate_request_is_stable_after_new_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_future_conflict_revision_does_not_mutate_old_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_g_not_supplied_is_persisted_configuration_incomplete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_gaps_are_partial_subtotal_never_window_total`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_historical_cut_excludes_later_consolidated_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_conflict_is_context_only`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_invalidity_cannot_change_temperature_calculation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_interior_sample_is_a_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[25]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[9]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes2]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes4]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes5]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes6]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes7]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_locatable_persistence_error_is_a_temperature_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_out_of_order_input_is_sorted_by_existing_engine`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_precision_tiny_mass_no_binary_float_in_snapshot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_EXPLORATORIO-COMPLETO_NO_MODELO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_RESTRITO-SEM_ESTIMATIVA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_same_timestamp_equal_temperature_does_not_duplicate_exposure`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_snapshot_replays_actual_public_engine_without_live_queries`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[audit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[commit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unknown_maturity_is_not_corrected_and_snapshot_mass_used`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unlocatable_temperature_timestamp_prevents_false_complete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unsealed_revision_cannot_leak_into_analysis`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_acquires_mapped_fields_and_reuses_existing_measurement_tables`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_binding_snapshot_does_not_follow_later_config_changes`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_replay_is_not_a_new_complementation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_session_requires_explicit_elevated_audited_complement`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_consulta_can_read_history_but_not_incorporate`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_existing_source_identity_of_other_sensor_is_not_reassigned`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_expired_execution_is_recoverable_and_old_key_is_not_reexecuted`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_global_deduplication_is_backed_by_existing_unique_identity`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_history_pagination_and_type_filter`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[404]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[429]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_http_provider_errors_are_auditable_failures[500]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_httpx_info_logging_does_not_disclose_read_key`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_idempotency_rejects_different_payload`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_acquisition_parameters_are_rejected[change4]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[2026-10-01T12:00:00]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[invalid]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[100000000]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[13.12345]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[Infinity]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[NaN]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[True]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_complement_adds_revision_without_changing_previous_history`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_local_incorporation_does_not_fabricate_late_receipt`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_math_engine_is_not_called`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_midflight_end_requires_a_new_explicit_complement_request`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[post-sincronizacoes-params3]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_operational_lateness_limit_is_explicit_and_not_scientific`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_original_measurement_receipt_and_processing_are_distinct`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[leituras]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[qualidade]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[sincronizacoes]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_out_of_order_readings_are_sorted_without_changing_their_times`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_network_failure_preserves_already_received_pages`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_partial_persistence_failure_keeps_the_other_fields`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_queries_cannot_extend_session_window`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_repeat_sync_and_same_request_do_not_duplicate_readings`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_request_budget_reports_partial_instead_of_silent_truncation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_reuses_legacy_external_history_without_fabricating_receipt_time`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_running_request_replay_returns_202_and_second_key_is_blocked`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_conflicting_values_block_coverage_without_overwriting`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_same_value_is_not_double_exposure`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_session_window_filters_before_and_after_and_keeps_endpoint_sample`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_source_payload_conflict_creates_new_revision_not_a_value_overwrite`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_split_historical_requests_recover_more_than_one_page`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_temporal_gaps_are_not_filled`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[CONSULTA]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unauthorized_roles_cannot_sync[OUTRO]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unrelated_channel_fields_are_not_imported`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_wrong_sensor_mapping_is_rejected_before_network`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_historical_cut_and_running_revision_exclude_future_data`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`

## API-056 — GET /api/v1/monitoramentos/{sessao_id}/sincronizacoes

Consultar estado e tentativas de sincronizacao

- Router/handler: [app/modules/monitoramento/historico_routes.py:48](../../app/modules/monitoramento/historico_routes.py#L48) · `estado` · operationId `estado_api_v1_monitoramentos__sessao_id__sincronizacoes_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | EstadoSincronizacaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "consultas",
    "module": "app.modules.monitoramento.historico_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{sessao_id}/sincronizacoes',response_model=EstadoSincronizacaoResponse,
            summary='Consultar estado e tentativas de sincronizacao')
def estado(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(consultas)):
    return svc.estado(sessao_id,limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception0]`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/340bb664-67ea-48dc-ab34-585b7c4d5a0b/sincronizacoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "sessao_id": "340bb664-67ea-48dc-ab34-585b7c4d5a0b",
  "revisao_disponivel": 1,
  "em_execucao": null,
  "tentativas": [
    {
      "id": "82d0dafe-7b03-4a93-a797-9110cd436684",
      "created_at": "2026-11-23T14:56:28",
      "updated_at": "2026-11-23T14:56:28",
      "sessao_id": "340bb664-67ea-48dc-ab34-585b7c4d5a0b",
      "usuario_id": "d7a6d71a-7e03-4cdb-8502-9c100e20d5c5",
      "revisao": 1,
      "chave_idempotencia": "446ede53-c5ed-4cd8-8ad7-06e0a2a1f9e6",
      "origem_dados": "THINGSPEAK",
      "estado": "FALHA",
      "inicio_janela": "2026-11-23T11:04:05.435676",
      "fim_janela": "2026-11-23T14:56:28.550738",
      "iniciada_em": "2026-11-23T14:56:28.550738",
      "finalizada_em": "2026-11-23T14:56:28.585158",
      "expira_em": "2026-11-23T14:57:44.550738",
      "complementacao": false,
      "justificativa": null,
      "resumo": {
        "janela_sessao_inicio": "2026-11-23T11:04:05.435676+00:00",
        "janela_sessao_fim": "2026-11-23T14:56:28.550738+00:00",
        "estado_sessao": "ATIVA",
        "limite_atraso_s": null,
        "limite_requisicoes": 16,
        "fontes": [
          {
            "id": "38dddc03-ff66-4c0d-92f0-adde45a72d84",
            "sensor_id": "c604c06d-6232-490f-b760-820314d27ec6",
            "channel_id": "12345",
            "field_name": "field4",
            "tipo": "TEMPERATURA",
            "unidade": "C"
          },
          {
            "id": "cab0c613-ae7d-4292-baa1-349b644cc6e2",
            "sensor_id": "787a43ae-cd07-4a41-8766-42861dab8e85",
            "channel_id": "12345",
            "field_name": "field7",
            "tipo": "UMIDADE",
            "unidade": "%"
          }
        ],
        "novas": 0,
        "duplicadas": 0,
        "invalidas": 0,
        "fora_janela": 0,
        "erros": 1,
        "tardias": 0,
        "fora_de_ordem": 0,
        "requisicoes": 1,
        "feeds_recebidos": 0
      }
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-sincronizacoes-params1]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_communication_failure_is_persisted_without_secrets[exception1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-sincronizacoes-params1]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[sincronizacoes]`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`

## API-057 — GET /api/v1/monitoramentos/{sessao_id}/leituras

Consultar leituras e marcadores invalidos em ordem cronologica

Janela inclusiva de amostras [inicio,fim], com amostra final apenas para fechar intervalos.

Revisoes preservam a incorporacao anterior; nao se altera registro ou valor em silencio.
recebida_em=None identifica horario de recebimento desconhecido no historico legado.

- Router/handler: [app/modules/monitoramento/historico_routes.py:54](../../app/modules/monitoramento/historico_routes.py#L54) · `leituras` · operationId `leituras_api_v1_monitoramentos__sessao_id__leituras_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 1000,   "minimum": 1,   "default": 100,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | tipo | False | {   "anyOf": [     {       "type": "string",       "pattern": "^(TEMPERATURA\|UMIDADE)$"     },     {       "type": "null"     }   ],   "title": "Tipo" } |
| query | revisao | False | {   "anyOf": [     {       "type": "integer",       "minimum": 1     },     {       "type": "null"     }   ],   "title": "Revisao" } |
| query | inicio | False | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "title": "Inicio" } |
| query | fim | False | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "title": "Fim" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | HistoricoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "consultas",
    "module": "app.modules.monitoramento.historico_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{sessao_id}/leituras',response_model=HistoricoResponse,
            summary='Consultar leituras e marcadores invalidos em ordem cronologica')
def leituras(sessao_id:UUID,limit:int=Query(100,ge=1,le=1000),offset:int=Query(0,ge=0),
             tipo:str|None=Query(None,pattern='^(TEMPERATURA|UMIDADE)$'),revisao:int|None=Query(None,ge=1),
             inicio:AwareDatetime|None=None,fim:AwareDatetime|None=None,svc=Depends(consultas)):
    """Janela inclusiva de amostras [inicio,fim], com amostra final apenas para fechar intervalos.

    Revisoes preservam a incorporacao anterior; nao se altera registro ou valor em silencio.
    recebida_em=None identifica horario de recebimento desconhecido no historico legado.
    """
    return svc.historico(sessao_id,limit,offset,tipo,revisao,inicio,fim)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_acquires_mapped_fields_and_reuses_existing_measurement_tables`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/29c352f9-c3dc-4d18-be78-cc02607b9fea/leituras`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "sessao_id": "29c352f9-c3dc-4d18-be78-cc02607b9fea",
  "estado_sessao": "ATIVA",
  "revisao": 1,
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T14:56:18.208063Z",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "total": 6,
  "limit": 100,
  "offset": 0,
  "leituras": [
    {
      "id": "442e2255-d3e9-42fa-8037-00ca6311596d",
      "fonte_id": "0f325883-4d97-47a2-9ae6-3faed50bb73a",
      "medicao_id": "33da6d22-ef74-4f27-81e6-3d854985e874",
      "sensor_id": "203c50e4-adaf-4371-a9d3-8edd16c66d0d",
      "tipo": "TEMPERATURA",
      "channel_id": "12345",
      "field_name": "field4",
      "unidade": "C",
      "entry_id": 1,
      "medida_em": "2026-11-23T11:04:05.435676Z",
      "timestamp_origem": "2026-11-23T11:04:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.254947Z",
      "valor": "13.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    },
    {
      "id": "fee59a28-2f3d-4020-8aa1-ae555ab34d5d",
      "fonte_id": "d2a0ddd1-4505-4464-b09b-d20e24da4f08",
      "medicao_id": "deb75ee7-23e3-4fe9-9b70-365430e8c558",
      "sensor_id": "9743cb58-6619-430d-83e0-a8f36e23b459",
      "tipo": "UMIDADE",
      "channel_id": "12345",
      "field_name": "field7",
      "unidade": "%",
      "entry_id": 1,
      "medida_em": "2026-11-23T11:04:05.435676Z",
      "timestamp_origem": "2026-11-23T11:04:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.271218Z",
      "valor": "90.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    },
    {
      "id": "b0ac05ac-38fc-4bd4-961b-65e29efe3cfc",
      "fonte_id": "d2a0ddd1-4505-4464-b09b-d20e24da4f08",
      "medicao_id": "aec18c91-d2c0-4a19-86f7-6a63cf7df676",
      "sensor_id": "9743cb58-6619-430d-83e0-a8f36e23b459",
      "tipo": "UMIDADE",
      "channel_id": "12345",
      "field_name": "field7",
      "unidade": "%",
      "entry_id": 2,
      "medida_em": "2026-11-23T11:14:05.435676Z",
      "timestamp_origem": "2026-11-23T11:14:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.283508Z",
      "valor": "90.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    },
    {
      "id": "c3c60bb1-5bc6-4bcf-a280-dbb8728624ee",
      "fonte_id": "0f325883-4d97-47a2-9ae6-3faed50bb73a",
      "medicao_id": "d6d1d1e7-2cc1-475b-a24c-3a916e74dd44",
      "sensor_id": "203c50e4-adaf-4371-a9d3-8edd16c66d0d",
      "tipo": "TEMPERATURA",
      "channel_id": "12345",
      "field_name": "field4",
      "unidade": "C",
      "entry_id": 2,
      "medida_em": "2026-11-23T11:14:05.435676Z",
      "timestamp_origem": "2026-11-23T11:14:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.277679Z",
      "valor": "15.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    },
    {
      "id": "7aab6201-cb9d-4b3a-96dc-cca1f40c1ded",
      "fonte_id": "0f325883-4d97-47a2-9ae6-3faed50bb73a",
      "medicao_id": "9c341acb-d8a3-48b4-aaa4-44e5d3a7a528",
      "sensor_id": "203c50e4-adaf-4371-a9d3-8edd16c66d0d",
      "tipo": "TEMPERATURA",
      "channel_id": "12345",
      "field_name": "field4",
      "unidade": "C",
      "entry_id": 3,
      "medida_em": "2026-11-23T11:34:05.435676Z",
      "timestamp_origem": "2026-11-23T11:34:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.289225Z",
      "valor": "20.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    },
    {
      "id": "b9d33b3b-def9-427b-96dd-8f0925b953c4",
      "fonte_id": "d2a0ddd1-4505-4464-b09b-d20e24da4f08",
      "medicao_id": "6044bb55-45c5-4f7b-8a93-e1e5d7723e5e",
      "sensor_id": "9743cb58-6619-430d-83e0-a8f36e23b459",
      "tipo": "UMIDADE",
      "channel_id": "12345",
      "field_name": "field7",
      "unidade": "%",
      "entry_id": 3,
      "medida_em": "2026-11-23T11:34:05.435676Z",
      "timestamp_origem": "2026-11-23T11:34:05.435676+00:00",
      "recebida_em": "2026-11-23T14:56:18.230221Z",
      "processada_em": "2026-11-23T14:56:18.294967Z",
      "valor": "90.0000",
      "estado": "VALIDA",
      "motivo": null,
      "revisao_incorporacao": 1,
      "tardia": null,
      "apos_encerramento": false,
      "fora_de_ordem": false,
      "conflito_observado": false
    }
  ],
  "metadados_temporais_invalidos": false,
  "cancelada_para_analise": false,
  "ocorrencias": []
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_history_pagination_and_type_filter`.

```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": [
        "query",
        "limit"
      ],
      "msg": "Input should be less than or equal to 1000"
    }
  ]
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_acquires_mapped_fields_and_reuses_existing_measurement_tables`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_binding_snapshot_does_not_follow_later_config_changes`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_closed_session_requires_explicit_elevated_audited_complement`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_consulta_can_read_history_but_not_incorporate`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_empty_history_and_no_operational_gap_default`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_existing_source_identity_of_other_sensor_is_not_reassigned`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_history_pagination_and_type_filter`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[2026-10-01T12:00:00]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[invalid]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[100000000]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[13.12345]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[Infinity]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[NaN]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_values_are_markers_not_zero[True]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_complement_adds_revision_without_changing_previous_history`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_late_local_incorporation_does_not_fabricate_late_receipt`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_math_engine_is_not_called`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-leituras-params0]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_original_measurement_receipt_and_processing_are_distinct`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[leituras]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_out_of_order_readings_are_sorted_without_changing_their_times`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_queries_cannot_extend_session_window`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_repeat_sync_and_same_request_do_not_duplicate_readings`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_reuses_legacy_external_history_without_fabricating_receipt_time`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_session_window_filters_before_and_after_and_keeps_endpoint_sample`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_source_payload_conflict_creates_new_revision_not_a_value_overwrite`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_split_historical_requests_recover_more_than_one_page`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_unrelated_channel_fields_are_not_imported`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`

## API-058 — GET /api/v1/monitoramentos/{sessao_id}/qualidade

Consultar lacunas e cobertura temporal, sem estimativa de etileno

G e parametro operacional obrigatorio, sem valor padrao cientifico.

Dois extremos utilizaveis, gaps integrais, sem interpolacao ou extrapolacao.
Cobertura de aquisicao nao e cobertura de aplicabilidade do modelo cientifico.

- Router/handler: [app/modules/monitoramento/historico_routes.py:67](../../app/modules/monitoramento/historico_routes.py#L67) · `qualidade` · operationId `qualidade_api_v1_monitoramentos__sessao_id__qualidade_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | intervalo_maximo_s | True | {   "anyOf": [     {       "type": "number",       "exclusiveMinimum": 0.0     },     {       "type": "string"     }   ],   "title": "Intervalo Maximo S" } |
| query | revisao | False | {   "anyOf": [     {       "type": "integer",       "minimum": 1     },     {       "type": "null"     }   ],   "title": "Revisao" } |
| query | inicio | False | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "title": "Inicio" } |
| query | fim | False | {   "anyOf": [     {       "type": "string",       "format": "date-time"     },     {       "type": "null"     }   ],   "title": "Fim" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | QualidadeResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "consultas",
    "module": "app.modules.monitoramento.historico_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{sessao_id}/qualidade',response_model=QualidadeResponse,
            summary='Consultar lacunas e cobertura temporal, sem estimativa de etileno')
def qualidade(sessao_id:UUID,intervalo_maximo_s:Decimal=Query(...,gt=0,max_digits=12,decimal_places=3),
              revisao:int|None=Query(None,ge=1),inicio:AwareDatetime|None=None,fim:AwareDatetime|None=None,
              svc=Depends(consultas)):
    """G e parametro operacional obrigatorio, sem valor padrao cientifico.

    Dois extremos utilizaveis, gaps integrais, sem interpolacao ou extrapolacao.
    Cobertura de aquisicao nao e cobertura de aplicabilidade do modelo cientifico.
    """
    return svc.qualidade(sessao_id,intervalo_maximo_s,revisao,inicio,fim)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/3f42e373-92ac-4eee-8fb8-91dad1eb4e12/qualidade`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.

Exemplo estrutural da chamada com query obrigatória (valor ilustrativo, não captura): `GET /api/v1/monitoramentos/{sessao_id}/qualidade?intervalo_maximo_s=3600`.
Resposta capturada:

```json
{
  "sessao_id": "3f42e373-92ac-4eee-8fb8-91dad1eb4e12",
  "revisao": 1,
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T11:34:05.435676Z",
  "intervalo_maximo_s": "600",
  "natureza": "COBERTURA_TEMPORAL_DE_AQUISICAO_NAO_E_ESTIMATIVA_DE_ETILENO",
  "metadados_temporais_invalidos": false,
  "cancelada_para_analise": true,
  "indicadores": [
    {
      "sensor_id": "d47cddeb-d76a-42e0-948f-529e9e4ce68f",
      "tipo": "TEMPERATURA",
      "unidade": "C",
      "registros": 3,
      "invalidos": 0,
      "instantes_conflitantes": 0,
      "tardias": 0,
      "atraso_nao_classificado": 3,
      "fora_de_ordem": 0,
      "duracao_janela_s": "1800",
      "duracao_coberta_s": "600",
      "duracao_nao_coberta_s": "1200",
      "percentual_cobertura": "33.333333333333333333333333333333333333333333333333",
      "intervalos": [
        {
          "inicio": "2026-11-23T11:04:05.435676Z",
          "fim": "2026-11-23T11:14:05.435676Z",
          "duracao_s": "600",
          "motivo": null
        },
        {
          "inicio": "2026-11-23T11:14:05.435676Z",
          "fim": "2026-11-23T11:34:05.435676Z",
          "duracao_s": "1200",
          "motivo": "LACUNA_EXCESSIVA"
        }
      ]
    },
    {
      "sensor_id": "c0390f57-735d-4da6-ad41-2a46628d4f75",
      "tipo": "UMIDADE",
      "unidade": "%",
      "registros": 3,
      "invalidos": 0,
      "instantes_conflitantes": 0,
      "tardias": 0,
      "atraso_nao_classificado": 3,
      "fora_de_ordem": 0,
      "duracao_janela_s": "1800",
      "duracao_coberta_s": "600",
      "duracao_nao_coberta_s": "1200",
      "percentual_cobertura": "33.333333333333333333333333333333333333333333333333",
      "intervalos": [
        {
          "inicio": "2026-11-23T11:04:05.435676Z",
          "fim": "2026-11-23T11:14:05.435676Z",
          "duracao_s": "600",
          "motivo": null
        },
        {
          "inicio": "2026-11-23T11:14:05.435676Z",
          "fim": "2026-11-23T11:34:05.435676Z",
          "duracao_s": "1200",
          "motivo": "LACUNA_EXCESSIVA"
        }
      ]
    }
  ],
  "codigos_ocorrencias": [],
  "limites": "Sem interpolacao temporal ou preenchimento. Aplicabilidade termica e q(T) pertencem somente a Etapa 5."
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_empty_history_and_no_operational_gap_default`.

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "intervalo_maximo_s"
      ],
      "msg": "Field required"
    }
  ]
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_cancelled_session_is_readable_but_not_synchronizable`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_empty_history_and_no_operational_gap_default`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[2026-10-01T12:00:00]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[None]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_invalid_timestamp_is_audited_and_prevents_false_complete_coverage[invalid]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_math_engine_is_not_called`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_missing_or_bad_numeric_field_preserves_a_barrier_and_valid_sibling`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_new_endpoints_require_authentication[get-qualidade-params2]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_other_company_cannot_read_acquisition[qualidade]`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_quality_requires_positive_operational_gap`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_request_budget_reports_partial_instead_of_silent_truncation`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_conflicting_values_block_coverage_without_overwriting`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_same_timestamp_same_value_is_not_double_exposure`<br>[tests/test_historico_iot.py](../../tests/test_historico_iot.py) `test_temporal_gaps_are_not_filled`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) `test_scoped_reader_can_see_own_session_history_but_not_global_channel`

## API-059 — POST /api/v1/monitoramentos/{sessao_id}/analises-etileno

Calcular e persistir producao potencial com o motor cientifico existente

Fixa janela, corte, revisao e snapshots. ATIVA exige corte explicito; CANCELADA rejeita novas analises.

G ausente gera CONFIGURACAO_INCOMPLETA. Subtotal coberto nunca substitui total da janela.
Mesma chave/autor/payload recupera o resultado anterior. Nova chave cria outra analise.
Decimais sao strings JSON. Risco permanece NAO_AVALIADO, sem inferir concentracao real.

- Router/handler: [app/modules/monitoramento/analises_routes.py:18](../../app/modules/monitoramento/analises_routes.py#L18) · `executar` · operationId `executar_api_v1_monitoramentos__sessao_id__analises_etileno_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: AnaliseCreate.
- Efeito: Persiste AnaliseEtileno, snapshots, hashes e EventoMonitoramento na mesma transação; replay retorna anterior.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AnaliseResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha de persistencia; consulte ou repita a mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.analises_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/{sessao_id}/analises-etileno',response_model=AnaliseResponse,
    responses={503:{'description':'Falha de persistencia; consulte ou repita a mesma chave idempotente.'}},
    summary='Calcular e persistir producao potencial com o motor cientifico existente')
def executar(sessao_id:UUID,data:AnaliseCreate,svc=Depends(servico)):
    """Fixa janela, corte, revisao e snapshots. ATIVA exige corte explicito; CANCELADA rejeita novas analises.

    G ausente gera CONFIGURACAO_INCOMPLETA. Subtotal coberto nunca substitui total da janela.
    Mesma chave/autor/payload recupera o resultado anterior. Nova chave cria outra analise.
    Decimais sao strings JSON. Risco permanece NAO_AVALIADO, sem inferir concentracao real.
    """
    return svc.executar(sessao_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/5efd78a3-01e1-4ef3-b984-c025a734ef37/analises-etileno`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "de4d4eb1-3a50-4617-99a6-729fdd32be96",
  "intervalo_maximo_s": "3600",
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "corte_aquisicao": "2026-11-23T14:54:09.896209+00:00"
}
```

Resposta capturada:

```json
{
  "id": "6fe0a598-6f86-434c-8642-9868ca827037",
  "created_at": "2026-11-23T14:54:09Z",
  "updated_at": "2026-11-23T14:54:09Z",
  "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
  "usuario_id": "323f3bb8-9d60-4da1-a5b3-c9bcbabe8dcf",
  "chave_idempotencia": "de4d4eb1-3a50-4617-99a6-729fdd32be96",
  "executada_em": "2026-11-23T14:54:09.923329Z",
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T13:04:05.435676Z",
  "corte_aquisicao": "2026-11-23T14:54:09.896209Z",
  "revisao_aquisicao": 1,
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "modo": "MODO_RESTRITO",
  "intervalo_maximo_s": "3600.000",
  "versao_modelo": "chicosense-etileno-1.0.0",
  "status_calculo": "COMPLETO_NO_MODELO",
  "classificacao_risco_etileno": "NAO_AVALIADO",
  "hash_entrada": "57c2b293f5fa83c60823e6c65f06fe5e5ee094c01ba7134f3b143252869fc577",
  "hash_resultado": "d2831e74a22b6a3a2d2f6330db66e4d0b592b5514903b061c21b33ef1823b634",
  "entrada_snapshot": {
    "versao_adaptador": "chicosense-sessao-etileno-1",
    "entrada": {
      "massa": "1000.0000",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
      "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
      "leituras": [
        {
          "medida_em": "2026-11-23T11:04:05.435676Z",
          "temperatura": "13.0000",
          "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
          "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
          "unidade": "C",
          "identificador_externo": "c0154340-5081-49b4-a63a-3a2f035aa469:1",
          "recebida_em": "2026-11-23T14:54:09.811158Z"
        },
        {
          "medida_em": "2026-11-23T12:04:05.435676Z",
          "temperatura": "20.0000",
          "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
          "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
          "unidade": "C",
          "identificador_externo": "c0154340-5081-49b4-a63a-3a2f035aa469:2",
          "recebida_em": "2026-11-23T14:54:09.811158Z"
        },
        {
          "medida_em": "2026-11-23T13:04:05.435676Z",
          "temperatura": "20.0000",
          "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
          "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
          "unidade": "C",
          "identificador_externo": "c0154340-5081-49b4-a63a-3a2f035aa469:3",
          "recebida_em": "2026-11-23T14:54:09.811158Z"
        }
      ],
      "intervalo_maximo_s": "3600",
      "modo": "MODO_RESTRITO",
      "maturacao": "MISTA",
      "unidade_massa": "kg",
      "corte_aquisicao": "2026-11-23T14:54:09.896209Z"
    },
    "registros": [
      {
        "registro_id": "4e63e951-b72b-4eea-8012-93916484cb2a",
        "medicao_id": "9c3f3f65-01a9-4fd0-9db7-841e6a4ae376",
        "fonte_id": "c0154340-5081-49b4-a63a-3a2f035aa469",
        "sincronizacao_id": "e62bba26-2c89-4bca-8458-9569c1f53f1d",
        "revisao": 1,
        "entry_id": 1,
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:09.811158Z",
        "processada_em": "2026-11-23T14:54:09.828947Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "b36240d6a9923c71c66f1bd7b9b3c8e79a4e96cbc781dbb5a6431aa81042f681"
      },
      {
        "registro_id": "12d5b967-c352-4084-8b50-37b732b142b7",
        "medicao_id": "817fae23-d72d-46b8-a7b2-9334d20db228",
        "fonte_id": "c0154340-5081-49b4-a63a-3a2f035aa469",
        "sincronizacao_id": "e62bba26-2c89-4bca-8458-9569c1f53f1d",
        "revisao": 1,
        "entry_id": 2,
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:09.811158Z",
        "processada_em": "2026-11-23T14:54:09.841850Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "326189eb4075a1d550efe255b9056d637a1626f2788f8bf120e2cd9a79980d09"
      },
      {
        "registro_id": "55e4e4bb-b250-496d-9c6b-e10d5e3b9b6f",
        "medicao_id": "e9a54043-d43f-435c-9855-6db3baa68bcf",
        "fonte_id": "c0154340-5081-49b4-a63a-3a2f035aa469",
        "sincronizacao_id": "e62bba26-2c89-4bca-8458-9569c1f53f1d",
        "revisao": 1,
        "entry_id": 3,
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:09.811158Z",
        "processada_em": "2026-11-23T14:54:09.853136Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "da70577bcdebaeaeb4897f427a8a0c69e60b16dc15f2f24a2fce9a0f0fd2f2d1"
      }
    ],
    "ocorrencias": [],
    "fontes_temperatura": [
      {
        "id": "c0154340-5081-49b4-a63a-3a2f035aa469",
        "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field4",
        "unidade": "C",
        "contexto": "AMBIENTE"
      }
    ],
    "contexto_umidade": {
      "sensor_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
      "referencia": "Historico IoT da mesma sessao e revisao; nao integra a formula."
    },
    "sessao": {
      "id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
      "estado": "ENCERRADA",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "configuracao_id": "02d060ef-5c3b-4331-92b8-ad031f08567e",
      "configuracao_versao": 1,
      "produto_identificado": "MANGA_TOMMY_ATKINS",
      "lote_codigo": "DEMO-001",
      "lote_hipotetico": true,
      "origem_sensor": {
        "temperatura": {
          "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
          "identificador": "TEMP",
          "tipo": "TEMPERATURA",
          "contexto": "AMBIENTE",
          "unidade": "C",
          "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
          "dispositivo": "ESP-1",
          "vinculos": {
            "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
            "carga_id": null,
            "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
          }
        },
        "umidade": {
          "sensor_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
          "identificador": "HUM",
          "tipo": "UMIDADE",
          "contexto": "AMBIENTE",
          "unidade": "%",
          "dispositivo_id": "81eeb38c-c3af-4497-a060-04c5e34b0207",
          "dispositivo": "ESP-1",
          "vinculos": {
            "viagem_id": "592effa8-87ce-4c9d-8f29-3fa64f83afd9",
            "carga_id": null,
            "veiculo_id": "b02e42d6-77d9-4153-9786-d96d1dcfab0a"
          }
        }
      }
    },
    "aquisicao": {
      "revisao": 1,
      "corte": "2026-11-23T14:54:09.896209Z",
      "tentativas": [
        {
          "id": "e62bba26-2c89-4bca-8458-9569c1f53f1d",
          "revisao": 1,
          "estado": "CONCLUIDA",
          "finalizada_em": "2026-11-23T14:54:09.860475Z",
          "inicio_janela": "2026-11-23T11:04:05.435676Z",
          "fim_janela": "2026-11-23T14:54:09.789094Z"
        }
      ]
    }
  },
  "resultado": {
    "status_calculo": "COMPLETO_NO_MODELO",
    "volume_coberto_min_ul": "700.000000",
    "volume_coberto_max_ul": "9000.000000",
    "volume_janela_min_ul": "700.000000",
    "volume_janela_max_ul": "9000.000000",
    "duracao_coberta_s": "7200",
    "duracao_nao_coberta_s": "0",
    "percentual_cobertura": "100",
    "unidade_volume": "µL",
    "motivos": [],
    "limitacoes": [
      "Referencias gerais de manga, sem validacao especifica para Tommy Atkins.",
      "Extremos nao sao limites fisicos garantidos nem intervalo de confianca.",
      "Temperatura do ar pode diferir da polpa; representatividade depende do sensor.",
      "Retencao da temperatura inicial nao revela variacoes entre amostras.",
      "Massa constante; maturacao, atmosfera e tratamentos nao sao modelados.",
      "Volume potencial nao e concentracao, dano, vida util ou remocao por exaustao.",
      "Maturacao mista: nao se presume uniformidade ou proporcao de estagios."
    ],
    "classificacao_risco_etileno": "NAO_AVALIADO",
    "motivo_risco": "SEM_LIMIAR_VALIDADO",
    "versao_modelo": "chicosense-etileno-1.0.0",
    "intervalos": [
      {
        "inicio": "2026-11-23T11:04:05.435676Z",
        "fim": "2026-11-23T12:04:05.435676Z",
        "duracao_s": "3600",
        "temperatura_inicio_c": "13.0000",
        "taxa_min_ul_kg_h": "0.2",
        "taxa_max_ul_kg_h": "1.0",
        "volume_min_ul": "200.00000",
        "volume_max_ul": "1000.00000",
        "motivos": []
      },
      {
        "inicio": "2026-11-23T12:04:05.435676Z",
        "fim": "2026-11-23T13:04:05.435676Z",
        "duracao_s": "3600",
        "temperatura_inicio_c": "20.0000",
        "taxa_min_ul_kg_h": "0.5",
        "taxa_max_ul_kg_h": "8.0",
        "volume_min_ul": "500.00000",
        "volume_max_ul": "8000.00000",
        "motivos": []
      }
    ],
    "massa_kg": "1000.0000",
    "inicio": "2026-11-23T11:04:05.435676Z",
    "fim": "2026-11-23T13:04:05.435676Z",
    "modo": "MODO_RESTRITO",
    "maturacao": "MISTA",
    "intervalo_maximo_s": "3600",
    "corte_aquisicao": "2026-11-23T14:54:09.896209Z",
    "sensor_id": "67a0548e-5508-423d-8007-4316cd532ef7",
    "sessao_id": "5efd78a3-01e1-4ef3-b984-c025a734ef37",
    "tabela_referencia": [
      {
        "temperatura_c": "10",
        "minimo_ul_kg_h": "0.1",
        "maximo_ul_kg_h": "0.5"
      },
      {
        "temperatura_c": "13",
        "minimo_ul_kg_h": "0.2",
        "maximo_ul_kg_h": "1.0"
      },
      {
        "temperatura_c": "15",
        "minimo_ul_kg_h": "0.3",
        "maximo_ul_kg_h": "4.0"
      },
      {
        "temperatura_c": "20",
        "minimo_ul_kg_h": "0.5",
        "maximo_ul_kg_h": "8.0"
      }
    ],
    "cobertura": "1",
    "duracao_janela_s": "7200",
    "duplicatas_descartadas": 0,
    "interpolacao_utilizada": false,
    "perfil": "UC_DAVIS_PONTOS_V1",
    "metodologia": "Retencao a esquerda, dois extremos validos, sem extensao de bordas.",
    "fonte": "https://postharvest.ucdavis.edu/produce-facts-sheets/mango",
    "referencia": "Kader, A. A. Mango. UC Davis PREC. Atualizacao: fevereiro de 1997.",
    "data_consulta": "2026-10-23",
    "aplicabilidade": "REFERENCIA_GERAL_NAO_VALIDADA_PARA_TOMMY_ATKINS"
  }
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0]`.

```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": [
        "body",
        "intervalo_maximo_s"
      ],
      "msg": "Input should be greater than 0"
    }
  ]
}
```

Matriz de respostas observadas: 200, 401, 403, 404, 409, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_requires_explicit_cutoff_and_freezes_window`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_active_without_explicit_end_uses_exact_frozen_cutoff`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_all_readings_are_used_beyond_history_default_page`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[post]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_duplicate_request_is_stable_after_new_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_future_conflict_revision_does_not_mutate_old_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_g_not_supplied_is_persisted_configuration_incomplete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_gaps_are_partial_subtotal_never_window_total`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_historical_cut_excludes_later_consolidated_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_conflict_is_context_only`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_humidity_invalidity_cannot_change_temperature_calculation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[-1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0.0001]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[Infinity]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_gap_rejected_at_api[True]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_interior_sample_is_a_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[25]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[9]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[NaN]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_or_out_of_domain_is_not_zero[None1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes0]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes2]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes4]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes5]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes6]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_invalid_window_cutoff_and_mode_rejected[changes7]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_locatable_persistence_error_is_a_temperature_barrier`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_configuration_is_explicit_conflict`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_no_measurements_and_no_acquisition_revision`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_out_of_order_input_is_sorted_by_existing_engine`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_precision_tiny_mass_no_binary_float_in_snapshot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_end_to_end_700_9000_and_persistence`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_EXPLORATORIO-COMPLETO_NO_MODELO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_restricted_and_exploratory_delegate_rates_to_engine[MODO_RESTRITO-SEM_ESTIMATIVA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_same_timestamp_equal_temperature_does_not_duplicate_exposure`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_snapshot_replays_actual_public_engine_without_live_queries`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[audit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_transaction_failure_rolls_back_analysis_and_audit[commit]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unknown_maturity_is_not_corrected_and_snapshot_mass_used`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unlocatable_temperature_timestamp_prevents_false_complete`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_unsealed_revision_cannot_leak_into_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[CONSULTA]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_write_role_denied[OUTRO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`

## API-060 — GET /api/v1/monitoramentos/{sessao_id}/analises-etileno

Listar analises preservadas da sessao

- Router/handler: [app/modules/monitoramento/analises_routes.py:31](../../app/modules/monitoramento/analises_routes.py#L31) · `listar` · operationId `listar_api_v1_monitoramentos__sessao_id__analises_etileno_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AnaliseLista; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.analises_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{sessao_id}/analises-etileno',response_model=AnaliseLista,summary='Listar analises preservadas da sessao')
def listar(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/5a7abec7-0028-4311-a698-5b2f936ea347/analises-etileno`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
  "total": 2,
  "limit": 1,
  "offset": 0,
  "analises": [
    {
      "id": "f80aee54-7dcf-4a73-b126-0e75bd110262",
      "created_at": "2026-11-23T14:54:11Z",
      "updated_at": "2026-11-23T14:54:11Z",
      "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
      "usuario_id": "bb7a44d1-c27a-4f6f-82f5-e9deaa2587d5",
      "chave_idempotencia": "8d4a08de-49ff-441f-8ebd-72900f9156ab",
      "executada_em": "2026-11-23T14:54:11.469822Z",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "corte_aquisicao": "2026-11-23T14:54:11.455166Z",
      "revisao_aquisicao": 1,
      "massa_kg": "1000.0000",
      "maturacao": "MISTA",
      "modo": "MODO_RESTRITO",
      "intervalo_maximo_s": "3600.000",
      "versao_modelo": "chicosense-etileno-1.0.0",
      "status_calculo": "COMPLETO_NO_MODELO",
      "classificacao_risco_etileno": "NAO_AVALIADO",
      "hash_entrada": "403719a1000b97dec6adf2b88bc3c2921ad2fffb5bd19f50dc70f44d3d3068a9",
      "hash_resultado": "1677fcc76cd5d955271ed1b6a4d1219b4240d62bb570522c899b9ae83302690f",
      "entrada_snapshot": {
        "versao_adaptador": "chicosense-sessao-etileno-1",
        "entrada": {
          "massa": "1000.0000",
          "inicio": "2026-11-23T11:04:05.435676Z",
          "fim": "2026-11-23T13:04:05.435676Z",
          "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
          "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
          "leituras": [
            {
              "medida_em": "2026-11-23T11:04:05.435676Z",
              "temperatura": "13.0000",
              "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
              "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
              "unidade": "C",
              "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:1",
              "recebida_em": "2026-11-23T14:54:11.308997Z"
            },
            {
              "medida_em": "2026-11-23T12:04:05.435676Z",
              "temperatura": "20.0000",
              "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
              "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
              "unidade": "C",
              "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:2",
              "recebida_em": "2026-11-23T14:54:11.308997Z"
            },
            {
              "medida_em": "2026-11-23T13:04:05.435676Z",
              "temperatura": "20.0000",
              "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
              "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
              "unidade": "C",
              "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:3",
              "recebida_em": "2026-11-23T14:54:11.308997Z"
            }
          ],
          "intervalo_maximo_s": "3600",
          "modo": "MODO_RESTRITO",
          "maturacao": "MISTA",
          "unidade_massa": "kg",
          "corte_aquisicao": "2026-11-23T14:54:11.455166Z"
        },
        "registros": [
          {
            "registro_id": "c22f1911-92fe-4b9e-a563-e68b8cc66a9c",
            "medicao_id": "394a5990-1f7e-421e-bdc3-19df20c217cc",
            "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
            "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
            "revisao": 1,
            "entry_id": 1,
            "medida_em": "2026-11-23T11:04:05.435676Z",
            "recebida_em": "2026-11-23T14:54:11.308997Z",
            "processada_em": "2026-11-23T14:54:11.332149Z",
            "estado": "VALIDA",
            "motivo": null,
            "tardia": null,
            "apos_encerramento": false,
            "fora_de_ordem": false,
            "assinatura": "f57177268929003c110df414fbb1906ca461a979ddff44add2075fbd64fdcb92"
          },
          {
            "registro_id": "4e14ddca-dabc-4e0c-bc97-f0857f745bea",
            "medicao_id": "6da6104b-22d1-4a52-ac81-9043eea12c03",
            "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
            "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
            "revisao": 1,
            "entry_id": 2,
            "medida_em": "2026-11-23T12:04:05.435676Z",
            "recebida_em": "2026-11-23T14:54:11.308997Z",
            "processada_em": "2026-11-23T14:54:11.346845Z",
            "estado": "VALIDA",
            "motivo": null,
            "tardia": null,
            "apos_encerramento": false,
            "fora_de_ordem": false,
            "assinatura": "b3fa7498339e5ea793d03c02b4ff15f4a4a79a33150acfe2b03cf40fce2af8cc"
          },
          {
            "registro_id": "1c0698c0-9782-463f-8c4a-acfa490e2495",
            "medicao_id": "502742c4-7876-474f-995d-0d8f7c65e357",
            "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
            "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
            "revisao": 1,
            "entry_id": 3,
            "medida_em": "2026-11-23T13:04:05.435676Z",
            "recebida_em": "2026-11-23T14:54:11.308997Z",
            "processada_em": "2026-11-23T14:54:11.358306Z",
            "estado": "VALIDA",
            "motivo": null,
            "tardia": null,
            "apos_encerramento": false,
            "fora_de_ordem": false,
            "assinatura": "98695f55142f9b113651588582c6702e25fee299d1b110208d4aaa4eba569dd9"
          }
        ],
        "ocorrencias": [],
        "fontes_temperatura": [
          {
            "id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
            "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
            "origem": "THINGSPEAK",
            "channel_id": "12345",
            "field_name": "field4",
            "unidade": "C",
            "contexto": "AMBIENTE"
          }
        ],
        "contexto_umidade": {
          "sensor_id": "ad487f0c-0909-46b2-aae1-a4bc95488097",
          "referencia": "Historico IoT da mesma sessao e revisao; nao integra a formula."
        },
        "sessao": {
          "id": "5a7abec7-0028-4311-a698-5b2f936ea347",
          "estado": "ENCERRADA",
          "inicio": "2026-11-23T11:04:05.435676Z",
          "fim": "2026-11-23T13:04:05.435676Z",
          "configuracao_id": "158e5695-a61e-4e0a-8c8a-931619d51e96",
          "configuracao_versao": 1,
          "produto_identificado": "MANGA_TOMMY_ATKINS",
          "lote_codigo": "DEMO-001",
          "lote_hipotetico": true,
          "origem_sensor": {
            "temperatura": {
              "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
              "identificador": "TEMP",
              "tipo": "TEMPERATURA",
              "contexto": "AMBIENTE",
              "unidade": "C",
              "dispositivo_id": "5e2de585-ba64-4b74-8bdb-72def3622827",
              "dispositivo": "ESP-1",
              "vinculos": {
                "viagem_id": "e687604b-e142-4001-afc3-1bd6d84b27b9",
                "carga_id": null,
                "veiculo_id": "478b6f05-c374-4161-85ef-eb4d914fceee"
              }
            },
            "umidade": {
              "sensor_id": "ad487f0c-0909-46b2-aae1-a4bc95488097",
              "identificador": "HUM",
              "tipo": "UMIDADE",
              "contexto": "AMBIENTE",
              "unidade": "%",
              "dispositivo_id": "5e2de585-ba64-4b74-8bdb-72def3622827",
              "dispositivo": "ESP-1",
              "vinculos": {
                "viagem_id": "e687604b-e142-4001-afc3-1bd6d84b27b9",
                "carga_id": null,
                "veiculo_id": "478b6f05-c374-4161-85ef-eb4d914fceee"
              }
            }
          }
        },
        "aquisicao": {
          "revisao": 1,
          "corte": "2026-11-23T14:54:11.455166Z",
          "tentativas": [
            {
              "id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
              "revisao": 1,
              "estado": "CONCLUIDA",
              "finalizada_em": "2026-11-23T14:54:11.365823Z",
              "inicio_janela": "2026-11-23T11:04:05.435676Z",
              "fim_janela": "2026-11-23T14:54:11.286871Z"
            }
          ]
        }
      },
      "resultado": {
        "status_calculo": "COMPLETO_NO_MODELO",
        "volume_coberto_min_ul": "700.000000",
        "volume_coberto_max_ul": "9000.000000",
        "volume_janela_min_ul": "700.000000",
        "volume_janela_max_ul": "9000.000000",
        "duracao_coberta_s": "7200",
        "duracao_nao_coberta_s": "0",
        "percentual_cobertura": "100",
        "unidade_volume": "µL",
        "motivos": [],
        "limitacoes": [
          "Referencias gerais de manga, sem validacao especifica para Tommy Atkins.",
          "Extremos nao sao limites fisicos garantidos nem intervalo de confianca.",
          "Temperatura do ar pode diferir da polpa; representatividade depende do sensor.",
          "Retencao da temperatura inicial nao revela variacoes entre amostras.",
          "Massa constante; maturacao, atmosfera e tratamentos nao sao modelados.",
          "Volume potencial nao e concentracao, dano, vida util ou remocao por exaustao.",
          "Maturacao mista: nao se presume uniformidade ou proporcao de estagios."
        ],
        "classificacao_risco_etileno": "NAO_AVALIADO",
        "motivo_risco": "SEM_LIMIAR_VALIDADO",
        "versao_modelo": "chicosense-etileno-1.0.0",
        "intervalos": [
          {
            "inicio": "2026-11-23T11:04:05.435676Z",
            "fim": "2026-11-23T12:04:05.435676Z",
            "duracao_s": "3600",
            "temperatura_inicio_c": "13.0000",
            "taxa_min_ul_kg_h": "0.2",
            "taxa_max_ul_kg_h": "1.0",
            "volume_min_ul": "200.00000",
            "volume_max_ul": "1000.00000",
            "motivos": []
          },
          {
            "inicio": "2026-11-23T12:04:05.435676Z",
            "fim": "2026-11-23T13:04:05.435676Z",
            "duracao_s": "3600",
            "temperatura_inicio_c": "20.0000",
            "taxa_min_ul_kg_h": "0.5",
            "taxa_max_ul_kg_h": "8.0",
            "volume_min_ul": "500.00000",
            "volume_max_ul": "8000.00000",
            "motivos": []
          }
        ],
        "massa_kg": "1000.0000",
        "inicio": "2026-11-23T11:04:05.435676Z",
        "fim": "2026-11-23T13:04:05.435676Z",
        "modo": "MODO_RESTRITO",
        "maturacao": "MISTA",
        "intervalo_maximo_s": "3600",
        "corte_aquisicao": "2026-11-23T14:54:11.455166Z",
        "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
        "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
        "tabela_referencia": [
          {
            "temperatura_c": "10",
            "minimo_ul_kg_h": "0.1",
            "maximo_ul_kg_h": "0.5"
          },
          {
            "temperatura_c": "13",
            "minimo_ul_kg_h": "0.2",
            "maximo_ul_kg_h": "1.0"
          },
          {
            "temperatura_c": "15",
            "minimo_ul_kg_h": "0.3",
            "maximo_ul_kg_h": "4.0"
          },
          {
            "temperatura_c": "20",
            "minimo_ul_kg_h": "0.5",
            "maximo_ul_kg_h": "8.0"
          }
        ],
        "cobertura": "1",
        "duracao_janela_s": "7200",
        "duplicatas_descartadas": 0,
        "interpolacao_utilizada": false,
        "perfil": "UC_DAVIS_PONTOS_V1",
        "metodologia": "Retencao a esquerda, dois extremos validos, sem extensao de bordas.",
        "fonte": "https://postharvest.ucdavis.edu/produce-facts-sheets/mango",
        "referencia": "Kader, A. A. Mango. UC Davis PREC. Atualizacao: fevereiro de 1997.",
        "data_consulta": "2026-10-23",
        "aplicabilidade": "REFERENCIA_GERAL_NAO_VALIDADA_PARA_TOMMY_ATKINS"
      }
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[list]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[list]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`

## API-061 — GET /api/v1/monitoramentos/{sessao_id}/analises-etileno/{analise_id}

Consultar resultado e entradas fixados, sem recalcular

- Router/handler: [app/modules/monitoramento/analises_routes.py:36](../../app/modules/monitoramento/analises_routes.py#L36) · `consultar` · operationId `consultar_api_v1_monitoramentos__sessao_id__analises_etileno__analise_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | analise_id | True | {   "type": "string",   "format": "uuid",   "title": "Analise Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AnaliseResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.analises_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{sessao_id}/analises-etileno/{analise_id}',response_model=AnaliseResponse,
    summary='Consultar resultado e entradas fixados, sem recalcular')
def consultar(sessao_id:UUID,analise_id:UUID,svc=Depends(servico)):
    return svc.consultar(sessao_id,analise_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/5a7abec7-0028-4311-a698-5b2f936ea347/analises-etileno/fb00c514-ffec-4266-8a8f-1ab0e0428d57`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "fb00c514-ffec-4266-8a8f-1ab0e0428d57",
  "created_at": "2026-11-23T14:54:11Z",
  "updated_at": "2026-11-23T14:54:11Z",
  "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
  "usuario_id": "bb7a44d1-c27a-4f6f-82f5-e9deaa2587d5",
  "chave_idempotencia": "637c3eec-e0ca-4351-a9a1-68f4579bc0be",
  "executada_em": "2026-11-23T14:54:11.414619Z",
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T13:04:05.435676Z",
  "corte_aquisicao": "2026-11-23T14:54:11.396675Z",
  "revisao_aquisicao": 1,
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "modo": "MODO_RESTRITO",
  "intervalo_maximo_s": "3600.000",
  "versao_modelo": "chicosense-etileno-1.0.0",
  "status_calculo": "COMPLETO_NO_MODELO",
  "classificacao_risco_etileno": "NAO_AVALIADO",
  "hash_entrada": "450b0b6981bc8150cd107ed7326dab2f89a2628494d9abb6c9cbdf7b0a6e7c29",
  "hash_resultado": "7c063bfb9b9fa46507e5f818270c6892a0d018f2209c20385c048a4fe33df3f2",
  "entrada_snapshot": {
    "versao_adaptador": "chicosense-sessao-etileno-1",
    "entrada": {
      "massa": "1000.0000",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
      "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
      "leituras": [
        {
          "medida_em": "2026-11-23T11:04:05.435676Z",
          "temperatura": "13.0000",
          "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
          "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
          "unidade": "C",
          "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:1",
          "recebida_em": "2026-11-23T14:54:11.308997Z"
        },
        {
          "medida_em": "2026-11-23T12:04:05.435676Z",
          "temperatura": "20.0000",
          "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
          "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
          "unidade": "C",
          "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:2",
          "recebida_em": "2026-11-23T14:54:11.308997Z"
        },
        {
          "medida_em": "2026-11-23T13:04:05.435676Z",
          "temperatura": "20.0000",
          "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
          "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
          "unidade": "C",
          "identificador_externo": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49:3",
          "recebida_em": "2026-11-23T14:54:11.308997Z"
        }
      ],
      "intervalo_maximo_s": "3600",
      "modo": "MODO_RESTRITO",
      "maturacao": "MISTA",
      "unidade_massa": "kg",
      "corte_aquisicao": "2026-11-23T14:54:11.396675Z"
    },
    "registros": [
      {
        "registro_id": "c22f1911-92fe-4b9e-a563-e68b8cc66a9c",
        "medicao_id": "394a5990-1f7e-421e-bdc3-19df20c217cc",
        "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
        "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
        "revisao": 1,
        "entry_id": 1,
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:11.308997Z",
        "processada_em": "2026-11-23T14:54:11.332149Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "f57177268929003c110df414fbb1906ca461a979ddff44add2075fbd64fdcb92"
      },
      {
        "registro_id": "4e14ddca-dabc-4e0c-bc97-f0857f745bea",
        "medicao_id": "6da6104b-22d1-4a52-ac81-9043eea12c03",
        "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
        "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
        "revisao": 1,
        "entry_id": 2,
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:11.308997Z",
        "processada_em": "2026-11-23T14:54:11.346845Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "b3fa7498339e5ea793d03c02b4ff15f4a4a79a33150acfe2b03cf40fce2af8cc"
      },
      {
        "registro_id": "1c0698c0-9782-463f-8c4a-acfa490e2495",
        "medicao_id": "502742c4-7876-474f-995d-0d8f7c65e357",
        "fonte_id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
        "sincronizacao_id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
        "revisao": 1,
        "entry_id": 3,
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:54:11.308997Z",
        "processada_em": "2026-11-23T14:54:11.358306Z",
        "estado": "VALIDA",
        "motivo": null,
        "tardia": null,
        "apos_encerramento": false,
        "fora_de_ordem": false,
        "assinatura": "98695f55142f9b113651588582c6702e25fee299d1b110208d4aaa4eba569dd9"
      }
    ],
    "ocorrencias": [],
    "fontes_temperatura": [
      {
        "id": "e0d22bbc-cca5-44e2-b30c-b27c08e7fa49",
        "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field4",
        "unidade": "C",
        "contexto": "AMBIENTE"
      }
    ],
    "contexto_umidade": {
      "sensor_id": "ad487f0c-0909-46b2-aae1-a4bc95488097",
      "referencia": "Historico IoT da mesma sessao e revisao; nao integra a formula."
    },
    "sessao": {
      "id": "5a7abec7-0028-4311-a698-5b2f936ea347",
      "estado": "ENCERRADA",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "configuracao_id": "158e5695-a61e-4e0a-8c8a-931619d51e96",
      "configuracao_versao": 1,
      "produto_identificado": "MANGA_TOMMY_ATKINS",
      "lote_codigo": "DEMO-001",
      "lote_hipotetico": true,
      "origem_sensor": {
        "temperatura": {
          "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
          "identificador": "TEMP",
          "tipo": "TEMPERATURA",
          "contexto": "AMBIENTE",
          "unidade": "C",
          "dispositivo_id": "5e2de585-ba64-4b74-8bdb-72def3622827",
          "dispositivo": "ESP-1",
          "vinculos": {
            "viagem_id": "e687604b-e142-4001-afc3-1bd6d84b27b9",
            "carga_id": null,
            "veiculo_id": "478b6f05-c374-4161-85ef-eb4d914fceee"
          }
        },
        "umidade": {
          "sensor_id": "ad487f0c-0909-46b2-aae1-a4bc95488097",
          "identificador": "HUM",
          "tipo": "UMIDADE",
          "contexto": "AMBIENTE",
          "unidade": "%",
          "dispositivo_id": "5e2de585-ba64-4b74-8bdb-72def3622827",
          "dispositivo": "ESP-1",
          "vinculos": {
            "viagem_id": "e687604b-e142-4001-afc3-1bd6d84b27b9",
            "carga_id": null,
            "veiculo_id": "478b6f05-c374-4161-85ef-eb4d914fceee"
          }
        }
      }
    },
    "aquisicao": {
      "revisao": 1,
      "corte": "2026-11-23T14:54:11.396675Z",
      "tentativas": [
        {
          "id": "0cab1068-4a4f-41f3-83ef-38fec7dea299",
          "revisao": 1,
          "estado": "CONCLUIDA",
          "finalizada_em": "2026-11-23T14:54:11.365823Z",
          "inicio_janela": "2026-11-23T11:04:05.435676Z",
          "fim_janela": "2026-11-23T14:54:11.286871Z"
        }
      ]
    }
  },
  "resultado": {
    "status_calculo": "COMPLETO_NO_MODELO",
    "volume_coberto_min_ul": "700.000000",
    "volume_coberto_max_ul": "9000.000000",
    "volume_janela_min_ul": "700.000000",
    "volume_janela_max_ul": "9000.000000",
    "duracao_coberta_s": "7200",
    "duracao_nao_coberta_s": "0",
    "percentual_cobertura": "100",
    "unidade_volume": "µL",
    "motivos": [],
    "limitacoes": [
      "Referencias gerais de manga, sem validacao especifica para Tommy Atkins.",
      "Extremos nao sao limites fisicos garantidos nem intervalo de confianca.",
      "Temperatura do ar pode diferir da polpa; representatividade depende do sensor.",
      "Retencao da temperatura inicial nao revela variacoes entre amostras.",
      "Massa constante; maturacao, atmosfera e tratamentos nao sao modelados.",
      "Volume potencial nao e concentracao, dano, vida util ou remocao por exaustao.",
      "Maturacao mista: nao se presume uniformidade ou proporcao de estagios."
    ],
    "classificacao_risco_etileno": "NAO_AVALIADO",
    "motivo_risco": "SEM_LIMIAR_VALIDADO",
    "versao_modelo": "chicosense-etileno-1.0.0",
    "intervalos": [
      {
        "inicio": "2026-11-23T11:04:05.435676Z",
        "fim": "2026-11-23T12:04:05.435676Z",
        "duracao_s": "3600",
        "temperatura_inicio_c": "13.0000",
        "taxa_min_ul_kg_h": "0.2",
        "taxa_max_ul_kg_h": "1.0",
        "volume_min_ul": "200.00000",
        "volume_max_ul": "1000.00000",
        "motivos": []
      },
      {
        "inicio": "2026-11-23T12:04:05.435676Z",
        "fim": "2026-11-23T13:04:05.435676Z",
        "duracao_s": "3600",
        "temperatura_inicio_c": "20.0000",
        "taxa_min_ul_kg_h": "0.5",
        "taxa_max_ul_kg_h": "8.0",
        "volume_min_ul": "500.00000",
        "volume_max_ul": "8000.00000",
        "motivos": []
      }
    ],
    "massa_kg": "1000.0000",
    "inicio": "2026-11-23T11:04:05.435676Z",
    "fim": "2026-11-23T13:04:05.435676Z",
    "modo": "MODO_RESTRITO",
    "maturacao": "MISTA",
    "intervalo_maximo_s": "3600",
    "corte_aquisicao": "2026-11-23T14:54:11.396675Z",
    "sensor_id": "f287a888-2a44-4118-a4ff-f9d0525dead3",
    "sessao_id": "5a7abec7-0028-4311-a698-5b2f936ea347",
    "tabela_referencia": [
      {
        "temperatura_c": "10",
        "minimo_ul_kg_h": "0.1",
        "maximo_ul_kg_h": "0.5"
      },
      {
        "temperatura_c": "13",
        "minimo_ul_kg_h": "0.2",
        "maximo_ul_kg_h": "1.0"
      },
      {
        "temperatura_c": "15",
        "minimo_ul_kg_h": "0.3",
        "maximo_ul_kg_h": "4.0"
      },
      {
        "temperatura_c": "20",
        "minimo_ul_kg_h": "0.5",
        "maximo_ul_kg_h": "8.0"
      }
    ],
    "cobertura": "1",
    "duracao_janela_s": "7200",
    "duplicatas_descartadas": 0,
    "interpolacao_utilizada": false,
    "perfil": "UC_DAVIS_PONTOS_V1",
    "metodologia": "Retencao a esquerda, dois extremos validos, sem extensao de bordas.",
    "fonte": "https://postharvest.ucdavis.edu/produce-facts-sheets/mango",
    "referencia": "Kader, A. A. Mango. UC Davis PREC. Atualizacao: fevereiro de 1997.",
    "data_consulta": "2026-10-23",
    "aplicabilidade": "REFERENCIA_GERAL_NAO_VALIDADA_PARA_TOMMY_ATKINS"
  }
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[get]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_authentication_required[get]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_cancelled_preserves_old_analyses_and_exact_replay`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[classificacao_risco_etileno-BAIXO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[fim-value3]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[revisao_aquisicao--1]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_database_checks_reject_inconsistent_analysis[status_calculo-SUCESSO]`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_future_conflict_revision_does_not_mutate_old_analysis`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_get_and_paginated_stable_history`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_late_complement_requires_new_analysis_not_mutation`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_missing_session_and_analysis_or_wrong_session`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_reader_can_read_but_other_company_cannot`<br>[tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) `test_real_engine_called_once_and_get_never_recalculates`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## API-062 — POST /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais

Registrar versao imutavel de parametros operacionais

ADMIN/GESTOR. Sem faixas ou duracoes cientificas automaticas. Maturacao/ambiente precisam corresponder explicitamente a sessao.

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:20](../../app/modules/monitoramento/preventivo_routes.py#L20) · `configurar` · operationId `configurar_api_v1_monitoramentos__sessao_id__configuracoes_ambientais_post`.
- Perfil: ADMIN/GESTOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: ConfiguracaoCreate.
- Efeito: Acrescenta versão ConfiguracaoAmbiental e evento; não edita versões.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ConfiguracaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/configuracoes-ambientais',response_model=ConfiguracaoResponse,summary='Registrar versao imutavel de parametros operacionais')
def configurar(sessao_id:UUID,data:ConfiguracaoCreate,svc=Depends(servico)):
    """ADMIN/GESTOR. Sem faixas ou duracoes cientificas automaticas. Maturacao/ambiente precisam corresponder explicitamente a sessao."""
    return svc.configurar(sessao_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/7430aaa0-fe6f-4593-a461-c88e56f9dc10/configuracoes-ambientais`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "b01b85c2-12d8-400b-879c-1617e47f33a0",
  "temperatura_min_c": "12",
  "temperatura_max_c": "14",
  "umidade_min_percentual": "90",
  "umidade_max_percentual": "95",
  "intervalo_maximo_s": "3600",
  "cobertura_min_percentual": "100",
  "exposicao_continua_s": "3600",
  "maturacoes_aplicaveis": [
    "MISTA"
  ],
  "ambiente": "TRANSPORTE_REFRIGERADO",
  "fundamento": "EXPERIMENTAL",
  "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
  "prioridade": "ATENCAO"
}
```

Resposta capturada:

```json
{
  "id": "44d1f18c-2b67-4e69-8d8b-ee5fca380715",
  "created_at": "2026-11-23T14:55:24Z",
  "updated_at": "2026-11-23T14:55:24Z",
  "sessao_id": "7430aaa0-fe6f-4593-a461-c88e56f9dc10",
  "usuario_id": "e0858143-c495-4f21-bfce-eaec243e8331",
  "chave_idempotencia": "b01b85c2-12d8-400b-879c-1617e47f33a0",
  "versao": 1,
  "registrada_em": "2026-11-23T14:55:24.454672Z",
  "parametros": {
    "temperatura_min_c": "12",
    "temperatura_max_c": "14",
    "umidade_min_percentual": "90",
    "umidade_max_percentual": "95",
    "intervalo_maximo_s": "3600",
    "cobertura_min_percentual": "100",
    "exposicao_continua_s": "3600",
    "maturacoes_aplicaveis": [
      "MISTA"
    ],
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "fundamento": "EXPERIMENTAL",
    "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
    "referencias": [],
    "prioridade": "ATENCAO"
  }
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 409, 422.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_idempotency_and_role`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_historical_cut_and_running_revision_exclude_future_data`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes0]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes10]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes11]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes12]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes13]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes1]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes2]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes3]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes4]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes5]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes6]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes7]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes8]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_configuration_rejected[changes9]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_no_readings_never_means_safe`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`

## API-063 — GET /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais

Listar versoes da configuracao operacional

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:26](../../app/modules/monitoramento/preventivo_routes.py#L26) · `configuracoes` · operationId `configuracoes_api_v1_monitoramentos__sessao_id__configuracoes_ambientais_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaConfiguracoes; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/configuracoes-ambientais',response_model=ListaConfiguracoes,summary='Listar versoes da configuracao operacional')
def configuracoes(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,'configuracoes',limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/77003970-beec-401e-ae85-94a4d627df4e/configuracoes-ambientais`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 2,
  "limit": 1,
  "offset": 0,
  "configuracoes": [
    {
      "id": "f2053489-83d2-4003-990a-6c8a16dcad07",
      "created_at": "2026-11-23T14:59:10Z",
      "updated_at": "2026-11-23T14:59:10Z",
      "sessao_id": "77003970-beec-401e-ae85-94a4d627df4e",
      "usuario_id": "75ecd804-145d-452f-8ac9-afc0bebf5fe1",
      "chave_idempotencia": "e1c219fa-f422-4f19-b0ef-b4bfff84e4cc",
      "versao": 2,
      "registrada_em": "2026-11-23T14:59:10.110319Z",
      "parametros": {
        "temperatura_min_c": "12",
        "temperatura_max_c": "12.5",
        "umidade_min_percentual": "90",
        "umidade_max_percentual": "95",
        "intervalo_maximo_s": "3600",
        "cobertura_min_percentual": "100",
        "exposicao_continua_s": "3600",
        "maturacoes_aplicaveis": [
          "MISTA"
        ],
        "ambiente": "TRANSPORTE_REFRIGERADO",
        "fundamento": "EXPERIMENTAL",
        "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
        "referencias": [],
        "prioridade": "ATENCAO"
      }
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/configuracoes-ambientais]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`

## API-064 — POST /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas

Avaliar dados ambientais e registrar alertas explicaveis

ATIVA exige corte explicito. Fixa revisao, configuracao e evidencias. Nova chave gera avaliacao relacionada a anterior.

Evidencia igual reutiliza alerta. Evidencia nova se vincula ao caso aberto da regra/configuracao; sem sobrescrita.
Ausencia de dados e inconclusiva. Analise de etileno opcional e somente contextual, da mesma janela/revisao.
Nao mede gas, nao classifica risco cientifico e nao determina intervencao. Risco etileno NAO_AVALIADO.

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:31](../../app/modules/monitoramento/preventivo_routes.py#L31) · `avaliar` · operationId `avaliar_api_v1_monitoramentos__sessao_id__avaliacoes_preventivas_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: AvaliacaoCreate.
- Efeito: Persiste avaliação, evidências, vínculos de alertas, decisão inicial CRIAR/ocorrência e evento; evidência equivalente pode reutilizar caso.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AvaliacaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/avaliacoes-preventivas',response_model=AvaliacaoResponse,summary='Avaliar dados ambientais e registrar alertas explicaveis')
def avaliar(sessao_id:UUID,data:AvaliacaoCreate,svc=Depends(servico)):
    """ATIVA exige corte explicito. Fixa revisao, configuracao e evidencias. Nova chave gera avaliacao relacionada a anterior.

    Evidencia igual reutiliza alerta. Evidencia nova se vincula ao caso aberto da regra/configuracao; sem sobrescrita.
    Ausencia de dados e inconclusiva. Analise de etileno opcional e somente contextual, da mesma janela/revisao.
    Nao mede gas, nao classifica risco cientifico e nao determina intervencao. Risco etileno NAO_AVALIADO.
    """
    return svc.avaliar(sessao_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/7430aaa0-fe6f-4593-a461-c88e56f9dc10/avaliacoes-preventivas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "9fa4a56a-5232-4ae9-b980-70e7d2011c21",
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "corte_aquisicao": "2026-11-23T14:55:24.565950+00:00"
}
```

Resposta capturada:

```json
{
  "id": "9516a3df-0ce2-45cf-b42e-fafe153b9e12",
  "created_at": "2026-11-23T14:55:24Z",
  "updated_at": "2026-11-23T14:55:24Z",
  "sessao_id": "7430aaa0-fe6f-4593-a461-c88e56f9dc10",
  "usuario_id": "1010201f-a676-44c3-aa3b-6d458e0977be",
  "configuracao_id": "44d1f18c-2b67-4e69-8d8b-ee5fca380715",
  "anterior_id": null,
  "analise_etileno_id": null,
  "chave_idempotencia": "9fa4a56a-5232-4ae9-b980-70e7d2011c21",
  "executada_em": "2026-11-23T14:55:24.591170Z",
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T13:04:05.435676Z",
  "corte_aquisicao": "2026-11-23T14:55:24.565950Z",
  "revisao": 1,
  "hash_entrada": "a2ec403ff3bd64afc2114f99f8819fdd6ba8c809804e1c3fcb02538a995d1ede",
  "hash_resultado": "879f26a09224d9d1bc9903fa47ed815cfc2d0ad0085769998c5f83e051b571a9",
  "entrada_snapshot": {
    "versao_avaliador": "chicosense-preventivo-1.0.0",
    "inicio": "2026-11-23T11:04:05.435676Z",
    "fim": "2026-11-23T13:04:05.435676Z",
    "corte_aquisicao": "2026-11-23T14:55:24.565950Z",
    "revisao": 1,
    "sessao": {
      "id": "7430aaa0-fe6f-4593-a461-c88e56f9dc10",
      "estado": "ATIVA",
      "maturacao": "MISTA",
      "ambiente": "TRANSPORTE_REFRIGERADO",
      "sensor_temperatura_id": "364ba93c-10fc-4616-b248-ff5da4e36453",
      "sensor_umidade_id": "8bac3f46-25a8-4402-ac9e-396b642c0b4f"
    },
    "configuracao": {
      "temperatura_min_c": "12",
      "temperatura_max_c": "14",
      "umidade_min_percentual": "90",
      "umidade_max_percentual": "95",
      "intervalo_maximo_s": "3600",
      "cobertura_min_percentual": "100",
      "exposicao_continua_s": "3600",
      "maturacoes_aplicaveis": [
        "MISTA"
      ],
      "ambiente": "TRANSPORTE_REFRIGERADO",
      "fundamento": "EXPERIMENTAL",
      "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
      "referencias": [],
      "prioridade": "ATENCAO"
    },
    "configuracao_id": "44d1f18c-2b67-4e69-8d8b-ee5fca380715",
    "configuracao_versao": 1,
    "fontes": [
      {
        "id": "d7f50e1a-abf5-40d6-baf2-5359f7605ed1",
        "tipo": "TEMPERATURA",
        "sensor_id": "364ba93c-10fc-4616-b248-ff5da4e36453",
        "unidade": "C",
        "contexto": "AMBIENTE",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field4"
      },
      {
        "id": "29a75041-a08a-4d12-88a6-3b80fd6a0239",
        "tipo": "UMIDADE",
        "sensor_id": "8bac3f46-25a8-4402-ac9e-396b642c0b4f",
        "unidade": "%",
        "contexto": "AMBIENTE",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field7"
      }
    ],
    "leituras": [
      {
        "id": "1a67d742-adb5-4023-9f2e-ff55bfa9432b",
        "medicao_id": "b23f450c-f2a7-45ff-8031-decdd411960a",
        "fonte_id": "29a75041-a08a-4d12-88a6-3b80fd6a0239",
        "tipo": "UMIDADE",
        "sensor_id": "8bac3f46-25a8-4402-ac9e-396b642c0b4f",
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.532824Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 1,
        "revisao": 1,
        "assinatura": "af72d0b8b4c5ce523c91f9ffd5712c14dcec8b6221ccf61401e696013b47c08b",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "bdf6263c-01ba-44c9-a7db-a3fa769cefaf",
        "medicao_id": "014ef2db-f0bf-4bcf-97db-dba2edb5d9fa",
        "fonte_id": "d7f50e1a-abf5-40d6-baf2-5359f7605ed1",
        "tipo": "TEMPERATURA",
        "sensor_id": "364ba93c-10fc-4616-b248-ff5da4e36453",
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.524584Z",
        "valor": "20.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 1,
        "revisao": 1,
        "assinatura": "6597cd1391d517b0ce9423963c65de4a05fd34720579ec98cdc4aa45d2b6cbd6",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "235ad488-5ae2-4d67-a757-3761d94ebc4c",
        "medicao_id": "0fa54f0b-0266-4a69-bb63-18fc19035cd3",
        "fonte_id": "d7f50e1a-abf5-40d6-baf2-5359f7605ed1",
        "tipo": "TEMPERATURA",
        "sensor_id": "364ba93c-10fc-4616-b248-ff5da4e36453",
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.538697Z",
        "valor": "13.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 2,
        "revisao": 1,
        "assinatura": "ee53083c1f07ca18ae32f27ee6d2bedc739e276edc1ceae3ceaaadddd1194615",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "b7ad897b-2b93-45ae-a8ed-2d92462fe40d",
        "medicao_id": "0b70f6e3-2b87-4680-a6e4-e2f499db5ca0",
        "fonte_id": "29a75041-a08a-4d12-88a6-3b80fd6a0239",
        "tipo": "UMIDADE",
        "sensor_id": "8bac3f46-25a8-4402-ac9e-396b642c0b4f",
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.544488Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 2,
        "revisao": 1,
        "assinatura": "a6e622c03570597e9a0b5c2718f1a979eb71067adf24619c8e00aa6c38505d0b",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "00f67cfb-785d-464c-9700-bbbb10b1f2bb",
        "medicao_id": "824cae9b-6348-482a-ab79-3e8f38dedee2",
        "fonte_id": "d7f50e1a-abf5-40d6-baf2-5359f7605ed1",
        "tipo": "TEMPERATURA",
        "sensor_id": "364ba93c-10fc-4616-b248-ff5da4e36453",
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.550418Z",
        "valor": "13.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 3,
        "revisao": 1,
        "assinatura": "5ae24acf62bcb8c823a39ae9940cbc02a2e9104ad1be6cb37fca5de77ced04f9",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "0e443c1a-b427-400e-981e-32d9da6cea74",
        "medicao_id": "41125219-4cfa-4c2b-96df-7819107d2638",
        "fonte_id": "29a75041-a08a-4d12-88a6-3b80fd6a0239",
        "tipo": "UMIDADE",
        "sensor_id": "8bac3f46-25a8-4402-ac9e-396b642c0b4f",
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:55:24.500614Z",
        "processada_em": "2026-11-23T14:55:24.554953Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 3,
        "revisao": 1,
        "assinatura": "2811fc0303eb910c5f1cdcd7d104182dc80f9dfc254efbbe043805a6df192808",
        "tardia": null,
        "apos_encerramento": false
      }
    ],
    "ocorrencias": [],
    "tentativas": [
      {
        "id": "ca2c267b-9c47-44b2-8178-e52dc8b74015",
        "revisao": 1,
        "estado": "CONCLUIDA",
        "finalizada_em": "2026-11-23T14:55:24.556356Z"
      }
    ],
    "estimativa_etileno_contextual": null
  },
  "resultado": {
    "versao_avaliador": "chicosense-preventivo-1.0.0",
    "classificacao_risco_etileno": "NAO_AVALIADO",
    "limitacoes": [
      "Prioridade operacional; sem criterios validados de dano fisiologico.",
      "Amostras nao comprovam ausencia de variacao entre medicoes; sensor pode medir ar, nao polpa.",
      "Duracao usa dois extremos fora da mesma faixa/lado e retencao operacional entre amostras; sem preencher lacunas.",
      "Ausencia de alerta nao comprova seguranca ou ausencia de etileno.",
      "Intervencao depende de avaliacao humana; alerta ambiental nao recomenda automaticamente exaustao.",
      "Maturacao mista/desconhecida; aplicacao explicitamente operacional, sem presumir fruta verde ou madura."
    ],
    "achados": [
      {
        "regra": "TEMPERATURA_FORA_DA_FAIXA",
        "mensagem": "Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.",
        "evidencia": {
          "tipo": "TEMPERATURA",
          "minimo": "12",
          "maximo": "14",
          "pontos": [
            {
              "medida_em": "2026-11-23T11:04:05.435676Z",
              "valor": "20.0000",
              "registros": [
                "bdf6263c-01ba-44c9-a7db-a3fa769cefaf"
              ],
              "lado": "ACIMA"
            }
          ],
          "unidade": "C"
        },
        "nivel": "ATENCAO"
      }
    ],
    "canais": [
      {
        "tipo": "TEMPERATURA",
        "unidade": "C",
        "duracao_janela_s": "7200",
        "duracao_coberta_s": "7200",
        "duracao_nao_coberta_s": "0",
        "percentual_cobertura": "100",
        "intervalos": [
          {
            "inicio": "2026-11-23T11:04:05.435676Z",
            "fim": "2026-11-23T12:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          },
          {
            "inicio": "2026-11-23T12:04:05.435676Z",
            "fim": "2026-11-23T13:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          }
        ],
        "metadados_temporais_inconclusivos": false
      },
      {
        "tipo": "UMIDADE",
        "unidade": "%",
        "duracao_janela_s": "7200",
        "duracao_coberta_s": "7200",
        "duracao_nao_coberta_s": "0",
        "percentual_cobertura": "100",
        "intervalos": [
          {
            "inicio": "2026-11-23T11:04:05.435676Z",
            "fim": "2026-11-23T12:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          },
          {
            "inicio": "2026-11-23T12:04:05.435676Z",
            "fim": "2026-11-23T13:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          }
        ],
        "metadados_temporais_inconclusivos": false
      }
    ],
    "status": "AVALIADO"
  },
  "alertas_ids": [
    "fad7d1e0-1caa-49aa-ada8-2feaa7a5ec22"
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404, 409, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_configuration_can_disable_duration_rule_explicitly`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_environment_never_invokes_ethylene_calculation`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[audit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_atomic_on_failure[commit]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_evaluation_idempotency_and_alert_dedup_across_duplicate_revision`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_gaps_are_not_bridged_and_coverage_is_inconclusive`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_historical_cut_and_running_revision_exclude_future_data`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_in_range_has_no_alert_and_reproduces_without_io`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[-1000-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[13-NaN]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_invalid_sensor_data_is_not_treated_as_normal[NaN-92]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_isolated_outlier_does_not_prove_prolonged_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[DESCONHECIDA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_maturity_requires_explicit_applicability[MISTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_no_readings_never_means_safe`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_out_of_order_and_duplicates_do_not_extend_exposure`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_persisted_ethylen_analysis_context_preserved`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[12-90]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_range_boundaries_are_inclusive[14-95]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_tolerance_threshold_is_configured_and_not_physiological`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_unknown_timestamp_disables_duration_and_coverage_claims`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[CONSULTA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_writes_require_operational_role[OUTRO]`

## API-065 — GET /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas

Listar avaliacoes imutaveis

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:42](../../app/modules/monitoramento/preventivo_routes.py#L42) · `avaliacoes` · operationId `avaliacoes_api_v1_monitoramentos__sessao_id__avaliacoes_preventivas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaAvaliacoes; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/avaliacoes-preventivas',response_model=ListaAvaliacoes,summary='Listar avaliacoes imutaveis')
def avaliacoes(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.listar(sessao_id,'avaliacoes',limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/d0f29618-904b-4b75-8d0b-8870dd0522bf/avaliacoes-preventivas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 2,
  "limit": 1,
  "offset": 0,
  "avaliacoes": [
    {
      "id": "678b9fd3-b4c4-45ca-a4ee-8d9084c88efd",
      "created_at": "2026-11-23T14:59:16Z",
      "updated_at": "2026-11-23T14:59:16Z",
      "sessao_id": "d0f29618-904b-4b75-8d0b-8870dd0522bf",
      "usuario_id": "d11e7429-3a7e-4a9d-99f0-912012b379ff",
      "configuracao_id": "76aee7db-bac4-4f86-a0da-b9206e914188",
      "anterior_id": "9deb7e43-0ac1-4749-a951-e0c63a62138a",
      "analise_etileno_id": null,
      "chave_idempotencia": "6df2272c-ebf0-45bb-8b1b-552afe0f103d",
      "executada_em": "2026-11-23T14:59:16.311033Z",
      "inicio": "2026-11-23T11:04:05.435676Z",
      "fim": "2026-11-23T13:04:05.435676Z",
      "corte_aquisicao": "2026-11-23T14:59:16.306404Z",
      "revisao": 1,
      "hash_entrada": "afaa56487be55baeab5a02985844e9a4aebc3e08c200425c1ad65cdb535071cf",
      "hash_resultado": "4afb2f8a8c7123810834c2eb37fc8357212bba17deb99a2607e287bee6be4d62",
      "entrada_snapshot": {
        "versao_avaliador": "chicosense-preventivo-1.0.0",
        "inicio": "2026-11-23T11:04:05.435676Z",
        "fim": "2026-11-23T13:04:05.435676Z",
        "corte_aquisicao": "2026-11-23T14:59:16.306404Z",
        "revisao": 1,
        "sessao": {
          "id": "d0f29618-904b-4b75-8d0b-8870dd0522bf",
          "estado": "ENCERRADA",
          "maturacao": "MISTA",
          "ambiente": "TRANSPORTE_REFRIGERADO",
          "sensor_temperatura_id": "f6628d4f-f1fd-4d2e-b0ce-9875e693c89a",
          "sensor_umidade_id": "e779a6e9-68a3-4778-807e-2bfc8af89c22"
        },
        "configuracao": {
          "temperatura_min_c": "12",
          "temperatura_max_c": "14",
          "umidade_min_percentual": "90",
          "umidade_max_percentual": "95",
          "intervalo_maximo_s": "3600",
          "cobertura_min_percentual": "100",
          "exposicao_continua_s": "3600",
          "maturacoes_aplicaveis": [
            "MISTA"
          ],
          "ambiente": "TRANSPORTE_REFRIGERADO",
          "fundamento": "EXPERIMENTAL",
          "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
          "referencias": [],
          "prioridade": "ATENCAO"
        },
        "configuracao_id": "76aee7db-bac4-4f86-a0da-b9206e914188",
        "configuracao_versao": 1,
        "fontes": [
          {
            "id": "a802f823-37d4-4d22-b067-37fdecc24e6c",
            "tipo": "TEMPERATURA",
            "sensor_id": "f6628d4f-f1fd-4d2e-b0ce-9875e693c89a",
            "unidade": "C",
            "contexto": "AMBIENTE",
            "origem": "THINGSPEAK",
            "channel_id": "12345",
            "field_name": "field4"
          },
          {
            "id": "5a6505a3-8ee4-4a00-80f5-a4f61dca1010",
            "tipo": "UMIDADE",
            "sensor_id": "e779a6e9-68a3-4778-807e-2bfc8af89c22",
            "unidade": "%",
            "contexto": "AMBIENTE",
            "origem": "THINGSPEAK",
            "channel_id": "12345",
            "field_name": "field7"
          }
        ],
        "leituras": [
          {
            "id": "2e1fcbb4-c6ff-421f-ae8c-b2cea5c41ceb",
            "medicao_id": "afdd2617-42d1-468a-95a4-26f7131a6fdb",
            "fonte_id": "a802f823-37d4-4d22-b067-37fdecc24e6c",
            "tipo": "TEMPERATURA",
            "sensor_id": "f6628d4f-f1fd-4d2e-b0ce-9875e693c89a",
            "medida_em": "2026-11-23T11:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.240923Z",
            "valor": "20.0000",
            "unidade": "C",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 1,
            "revisao": 1,
            "assinatura": "bb70b0d71382c20d16009f87b2d0bf8cfc69b91967ab333e30c52c6b54cedb88",
            "tardia": null,
            "apos_encerramento": false
          },
          {
            "id": "5dfca8fb-808c-4a44-9740-5fff93e7da47",
            "medicao_id": "9b5ffbe3-fe48-4d1d-80f7-02b8b169bc7d",
            "fonte_id": "5a6505a3-8ee4-4a00-80f5-a4f61dca1010",
            "tipo": "UMIDADE",
            "sensor_id": "e779a6e9-68a3-4778-807e-2bfc8af89c22",
            "medida_em": "2026-11-23T11:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.243233Z",
            "valor": "92.0000",
            "unidade": "%",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 1,
            "revisao": 1,
            "assinatura": "7853be3e31d7b6175037826a521891c68533ce7c9af8602cc492af11870c8715",
            "tardia": null,
            "apos_encerramento": false
          },
          {
            "id": "57e46f3b-a175-4ee6-99bd-fdfdf1a3bf55",
            "medicao_id": "ce9ef1f2-8713-417a-bd6f-0963236b8f78",
            "fonte_id": "5a6505a3-8ee4-4a00-80f5-a4f61dca1010",
            "tipo": "UMIDADE",
            "sensor_id": "e779a6e9-68a3-4778-807e-2bfc8af89c22",
            "medida_em": "2026-11-23T12:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.246483Z",
            "valor": "92.0000",
            "unidade": "%",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 2,
            "revisao": 1,
            "assinatura": "43ccaa631a37d950a397f3c2c8b28399b484350d78286efdc75b1a7ae4e5f52a",
            "tardia": null,
            "apos_encerramento": false
          },
          {
            "id": "db81ecd4-5a40-4003-b223-1adc39909c98",
            "medicao_id": "c1ece4cb-d559-4d5b-8f86-b690202a5536",
            "fonte_id": "a802f823-37d4-4d22-b067-37fdecc24e6c",
            "tipo": "TEMPERATURA",
            "sensor_id": "f6628d4f-f1fd-4d2e-b0ce-9875e693c89a",
            "medida_em": "2026-11-23T12:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.244864Z",
            "valor": "13.0000",
            "unidade": "C",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 2,
            "revisao": 1,
            "assinatura": "3ca020da838e1be6eb2ef3207d90f6b026917f26994e37f8c0046d9009634508",
            "tardia": null,
            "apos_encerramento": false
          },
          {
            "id": "27c1943e-7a0b-4d52-8a8c-da2f1699ff4e",
            "medicao_id": "8c021bb5-4350-4936-820f-198a35d4c99e",
            "fonte_id": "5a6505a3-8ee4-4a00-80f5-a4f61dca1010",
            "tipo": "UMIDADE",
            "sensor_id": "e779a6e9-68a3-4778-807e-2bfc8af89c22",
            "medida_em": "2026-11-23T13:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.252208Z",
            "valor": "92.0000",
            "unidade": "%",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 3,
            "revisao": 1,
            "assinatura": "a9b25a8544a5d2fcdb981a5e659ed1b6b3f0fe112023dabe4eb34930555843fa",
            "tardia": null,
            "apos_encerramento": false
          },
          {
            "id": "e8c18c60-96c1-48a0-a1de-0a0797574c2e",
            "medicao_id": "b42438ce-7985-4dca-b44c-9c61096013a4",
            "fonte_id": "a802f823-37d4-4d22-b067-37fdecc24e6c",
            "tipo": "TEMPERATURA",
            "sensor_id": "f6628d4f-f1fd-4d2e-b0ce-9875e693c89a",
            "medida_em": "2026-11-23T13:04:05.435676Z",
            "recebida_em": "2026-11-23T14:59:16.234036Z",
            "processada_em": "2026-11-23T14:59:16.248995Z",
            "valor": "13.0000",
            "unidade": "C",
            "estado": "VALIDA",
            "motivo": null,
            "entry_id": 3,
            "revisao": 1,
            "assinatura": "dee4f35b67696dd51d70ba40e90bca48a6915931cb6955d722c90337fcc45462",
            "tardia": null,
            "apos_encerramento": false
          }
        ],
        "ocorrencias": [],
        "tentativas": [
          {
            "id": "9e1c869a-7440-4cd7-9d05-e1539ef6e141",
            "revisao": 1,
            "estado": "CONCLUIDA",
            "finalizada_em": "2026-11-23T14:59:16.252893Z"
          }
        ],
        "estimativa_etileno_contextual": null
      },
      "resultado": {
        "versao_avaliador": "chicosense-preventivo-1.0.0",
        "classificacao_risco_etileno": "NAO_AVALIADO",
        "limitacoes": [
          "Prioridade operacional; sem criterios validados de dano fisiologico.",
          "Amostras nao comprovam ausencia de variacao entre medicoes; sensor pode medir ar, nao polpa.",
          "Duracao usa dois extremos fora da mesma faixa/lado e retencao operacional entre amostras; sem preencher lacunas.",
          "Ausencia de alerta nao comprova seguranca ou ausencia de etileno.",
          "Intervencao depende de avaliacao humana; alerta ambiental nao recomenda automaticamente exaustao.",
          "Maturacao mista/desconhecida; aplicacao explicitamente operacional, sem presumir fruta verde ou madura."
        ],
        "achados": [
          {
            "regra": "TEMPERATURA_FORA_DA_FAIXA",
            "mensagem": "Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.",
            "evidencia": {
              "tipo": "TEMPERATURA",
              "minimo": "12",
              "maximo": "14",
              "pontos": [
                {
                  "medida_em": "2026-11-23T11:04:05.435676Z",
                  "valor": "20.0000",
                  "registros": [
                    "2e1fcbb4-c6ff-421f-ae8c-b2cea5c41ceb"
                  ],
                  "lado": "ACIMA"
                }
              ],
              "unidade": "C"
            },
            "nivel": "ATENCAO"
          }
        ],
        "canais": [
          {
            "tipo": "TEMPERATURA",
            "unidade": "C",
            "duracao_janela_s": "7200",
            "duracao_coberta_s": "7200",
            "duracao_nao_coberta_s": "0",
            "percentual_cobertura": "100",
            "intervalos": [
              {
                "inicio": "2026-11-23T11:04:05.435676Z",
                "fim": "2026-11-23T12:04:05.435676Z",
                "duracao_s": "3600",
                "motivo": null
              },
              {
                "inicio": "2026-11-23T12:04:05.435676Z",
                "fim": "2026-11-23T13:04:05.435676Z",
                "duracao_s": "3600",
                "motivo": null
              }
            ],
            "metadados_temporais_inconclusivos": false
          },
          {
            "tipo": "UMIDADE",
            "unidade": "%",
            "duracao_janela_s": "7200",
            "duracao_coberta_s": "7200",
            "duracao_nao_coberta_s": "0",
            "percentual_cobertura": "100",
            "intervalos": [
              {
                "inicio": "2026-11-23T11:04:05.435676Z",
                "fim": "2026-11-23T12:04:05.435676Z",
                "duracao_s": "3600",
                "motivo": null
              },
              {
                "inicio": "2026-11-23T12:04:05.435676Z",
                "fim": "2026-11-23T13:04:05.435676Z",
                "duracao_s": "3600",
                "motivo": null
              }
            ],
            "metadados_temporais_inconclusivos": false
          }
        ],
        "status": "AVALIADO"
      },
      "alertas_ids": [
        "e250a169-ee19-4d8e-874f-16f57a11eff5"
      ]
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/avaliacoes-preventivas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`

## API-066 — GET /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id}

Consultar snapshot e resultado sem reavaliar

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:47](../../app/modules/monitoramento/preventivo_routes.py#L47) · `avaliacao` · operationId `avaliacao_api_v1_monitoramentos__sessao_id__avaliacoes_preventivas__avaliacao_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | avaliacao_id | True | {   "type": "string",   "format": "uuid",   "title": "Avaliacao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AvaliacaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/avaliacoes-preventivas/{avaliacao_id}',response_model=AvaliacaoResponse,summary='Consultar snapshot e resultado sem reavaliar')
def avaliacao(sessao_id:UUID,avaliacao_id:UUID,svc=Depends(servico)):
    return svc.consultar_avaliacao(sessao_id,avaliacao_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/77003970-beec-401e-ae85-94a4d627df4e/avaliacoes-preventivas/0d671f53-5544-4665-ad06-8e6971a5bbe6`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "0d671f53-5544-4665-ad06-8e6971a5bbe6",
  "created_at": "2026-11-23T14:59:10Z",
  "updated_at": "2026-11-23T14:59:10Z",
  "sessao_id": "77003970-beec-401e-ae85-94a4d627df4e",
  "usuario_id": "00f88c78-d447-4069-8f19-508d0e86eb63",
  "configuracao_id": "ab6b69ba-dbaf-4f2d-9d8f-2004296fa4b8",
  "anterior_id": null,
  "analise_etileno_id": null,
  "chave_idempotencia": "1bd3f88d-c2fa-4717-ad8a-63e2b6beeba0",
  "executada_em": "2026-11-23T14:59:10.081340Z",
  "inicio": "2026-11-23T11:04:05.435676Z",
  "fim": "2026-11-23T13:04:05.435676Z",
  "corte_aquisicao": "2026-11-23T14:59:10.074475Z",
  "revisao": 1,
  "hash_entrada": "0d444cb2aac592273708562da19f609e4f0e05c6bd25a23d58959be871c8293b",
  "hash_resultado": "3a993ef460f5d338493d5795dbf301f9544dc9efe254f218214f3d179758e177",
  "entrada_snapshot": {
    "versao_avaliador": "chicosense-preventivo-1.0.0",
    "inicio": "2026-11-23T11:04:05.435676Z",
    "fim": "2026-11-23T13:04:05.435676Z",
    "corte_aquisicao": "2026-11-23T14:59:10.074475Z",
    "revisao": 1,
    "sessao": {
      "id": "77003970-beec-401e-ae85-94a4d627df4e",
      "estado": "ATIVA",
      "maturacao": "MISTA",
      "ambiente": "TRANSPORTE_REFRIGERADO",
      "sensor_temperatura_id": "463cc76f-e5ba-4ecf-aa80-f245092791b9",
      "sensor_umidade_id": "1402f39c-d317-4a3b-a81f-1f499e146312"
    },
    "configuracao": {
      "temperatura_min_c": "12",
      "temperatura_max_c": "14",
      "umidade_min_percentual": "90",
      "umidade_max_percentual": "95",
      "intervalo_maximo_s": "3600",
      "cobertura_min_percentual": "100",
      "exposicao_continua_s": "3600",
      "maturacoes_aplicaveis": [
        "MISTA"
      ],
      "ambiente": "TRANSPORTE_REFRIGERADO",
      "fundamento": "EXPERIMENTAL",
      "justificativa": "Fixture hipotetica; limites operacionais sem validacao fisiologica.",
      "referencias": [],
      "prioridade": "ATENCAO"
    },
    "configuracao_id": "ab6b69ba-dbaf-4f2d-9d8f-2004296fa4b8",
    "configuracao_versao": 1,
    "fontes": [
      {
        "id": "3365d81b-1c09-404d-80b6-735734bd66a6",
        "tipo": "TEMPERATURA",
        "sensor_id": "463cc76f-e5ba-4ecf-aa80-f245092791b9",
        "unidade": "C",
        "contexto": "AMBIENTE",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field4"
      },
      {
        "id": "bef852b3-3ed2-40f8-8b7d-b5e1e6d5972e",
        "tipo": "UMIDADE",
        "sensor_id": "1402f39c-d317-4a3b-a81f-1f499e146312",
        "unidade": "%",
        "contexto": "AMBIENTE",
        "origem": "THINGSPEAK",
        "channel_id": "12345",
        "field_name": "field7"
      }
    ],
    "leituras": [
      {
        "id": "069a7b66-f9f7-4c7e-b46e-951e20873c8f",
        "medicao_id": "c82da072-f7a3-4075-ac5a-90cca979972b",
        "fonte_id": "3365d81b-1c09-404d-80b6-735734bd66a6",
        "tipo": "TEMPERATURA",
        "sensor_id": "463cc76f-e5ba-4ecf-aa80-f245092791b9",
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.060759Z",
        "valor": "13.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 1,
        "revisao": 1,
        "assinatura": "3ccfe740881ad012739a5639fa61012fe8ddb335fb7eb86e2c6fa0efb3c12a21",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "cc0c03fc-6235-47c0-bcd2-b0a80650bee9",
        "medicao_id": "d466d6d9-71e5-4109-8b42-154577fc7765",
        "fonte_id": "bef852b3-3ed2-40f8-8b7d-b5e1e6d5972e",
        "tipo": "UMIDADE",
        "sensor_id": "1402f39c-d317-4a3b-a81f-1f499e146312",
        "medida_em": "2026-11-23T11:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.063681Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 1,
        "revisao": 1,
        "assinatura": "c7f5c74932b0d7972cc63430caccf88bef73567917d614b4ec56a1447a00e92f",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "16e4f991-c1a0-44ca-aac1-ed821fac76c2",
        "medicao_id": "606d848a-9372-4984-b9c8-205a244f38f4",
        "fonte_id": "3365d81b-1c09-404d-80b6-735734bd66a6",
        "tipo": "TEMPERATURA",
        "sensor_id": "463cc76f-e5ba-4ecf-aa80-f245092791b9",
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.065611Z",
        "valor": "13.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 2,
        "revisao": 1,
        "assinatura": "bf96e89c63507e739285ecba7901aaff7e3dffad31df1e8c26a49c5db027d320",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "ffa34ea7-461c-4466-b7b5-aae30ad6165c",
        "medicao_id": "6ab0a491-a103-411d-ab3e-b2a25ad883a5",
        "fonte_id": "bef852b3-3ed2-40f8-8b7d-b5e1e6d5972e",
        "tipo": "UMIDADE",
        "sensor_id": "1402f39c-d317-4a3b-a81f-1f499e146312",
        "medida_em": "2026-11-23T12:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.067310Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 2,
        "revisao": 1,
        "assinatura": "4431b28d845f43eb3acadef773189d88ef61e33a58b719372e5786576e20e42a",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "3f1f3fc9-6f00-4616-af8b-077a3d952cfd",
        "medicao_id": "bb1a000d-e515-46aa-bd6e-8f46cd28eb21",
        "fonte_id": "3365d81b-1c09-404d-80b6-735734bd66a6",
        "tipo": "TEMPERATURA",
        "sensor_id": "463cc76f-e5ba-4ecf-aa80-f245092791b9",
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.069116Z",
        "valor": "13.0000",
        "unidade": "C",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 3,
        "revisao": 1,
        "assinatura": "b33c65f6bb942b4d7c1c1019d74bb25eff1ead5f5ccdc869e1ca234001c5ac84",
        "tardia": null,
        "apos_encerramento": false
      },
      {
        "id": "d1af09b7-7ba2-41fd-9786-02a36e937d26",
        "medicao_id": "48939fec-e4aa-4e58-a58b-b45dd407150c",
        "fonte_id": "bef852b3-3ed2-40f8-8b7d-b5e1e6d5972e",
        "tipo": "UMIDADE",
        "sensor_id": "1402f39c-d317-4a3b-a81f-1f499e146312",
        "medida_em": "2026-11-23T13:04:05.435676Z",
        "recebida_em": "2026-11-23T14:59:10.051273Z",
        "processada_em": "2026-11-23T14:59:10.070797Z",
        "valor": "92.0000",
        "unidade": "%",
        "estado": "VALIDA",
        "motivo": null,
        "entry_id": 3,
        "revisao": 1,
        "assinatura": "b60e63aa523b2e10dfe6d722ba144180577cbfe5aecae5c2b86bf93b1cda542d",
        "tardia": null,
        "apos_encerramento": false
      }
    ],
    "ocorrencias": [],
    "tentativas": [
      {
        "id": "5fd5d30d-7c2b-4ac1-9691-5a2b64ce373d",
        "revisao": 1,
        "estado": "CONCLUIDA",
        "finalizada_em": "2026-11-23T14:59:10.071205Z"
      }
    ],
    "estimativa_etileno_contextual": null
  },
  "resultado": {
    "versao_avaliador": "chicosense-preventivo-1.0.0",
    "classificacao_risco_etileno": "NAO_AVALIADO",
    "limitacoes": [
      "Prioridade operacional; sem criterios validados de dano fisiologico.",
      "Amostras nao comprovam ausencia de variacao entre medicoes; sensor pode medir ar, nao polpa.",
      "Duracao usa dois extremos fora da mesma faixa/lado e retencao operacional entre amostras; sem preencher lacunas.",
      "Ausencia de alerta nao comprova seguranca ou ausencia de etileno.",
      "Intervencao depende de avaliacao humana; alerta ambiental nao recomenda automaticamente exaustao.",
      "Maturacao mista/desconhecida; aplicacao explicitamente operacional, sem presumir fruta verde ou madura."
    ],
    "achados": [],
    "canais": [
      {
        "tipo": "TEMPERATURA",
        "unidade": "C",
        "duracao_janela_s": "7200",
        "duracao_coberta_s": "7200",
        "duracao_nao_coberta_s": "0",
        "percentual_cobertura": "100",
        "intervalos": [
          {
            "inicio": "2026-11-23T11:04:05.435676Z",
            "fim": "2026-11-23T12:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          },
          {
            "inicio": "2026-11-23T12:04:05.435676Z",
            "fim": "2026-11-23T13:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          }
        ],
        "metadados_temporais_inconclusivos": false
      },
      {
        "tipo": "UMIDADE",
        "unidade": "%",
        "duracao_janela_s": "7200",
        "duracao_coberta_s": "7200",
        "duracao_nao_coberta_s": "0",
        "percentual_cobertura": "100",
        "intervalos": [
          {
            "inicio": "2026-11-23T11:04:05.435676Z",
            "fim": "2026-11-23T12:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          },
          {
            "inicio": "2026-11-23T12:04:05.435676Z",
            "fim": "2026-11-23T13:04:05.435676Z",
            "duracao_s": "3600",
            "motivo": null
          }
        ],
        "metadados_temporais_inconclusivos": false
      }
    ],
    "status": "AVALIADO"
  },
  "alertas_ids": []
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_config_versions_immutable_and_old_evaluation_frozen`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_revision_conflict_creates_new_evidence_preserves_previous`

## API-067 — GET /api/v1/monitoramentos/{sessao_id}/alertas

Listar alertas operacionais da sessao

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:52](../../app/modules/monitoramento/preventivo_routes.py#L52) · `alertas` · operationId `alertas_api_v1_monitoramentos__sessao_id__alertas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | status | False | {   "anyOf": [     {       "type": "string",       "pattern": "^(ABERTO\|EM_ANALISE\|RESOLVIDO\|DESCARTADO)$"     },     {       "type": "null"     }   ],   "title": "Status" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaAlertas; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/alertas',response_model=ListaAlertas,summary='Listar alertas operacionais da sessao')
def alertas(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),
    status:str|None=Query(None,pattern='^(ABERTO|EM_ANALISE|RESOLVIDO|DESCARTADO)$'),svc=Depends(servico)):
    return svc.listar(sessao_id,'alertas',limit,offset,status)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/9efe84e5-cbe9-4596-be57-04e56c5e7f9e/alertas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 2,
  "limit": 20,
  "offset": 0,
  "alertas": [
    {
      "id": "8ef3f653-5485-4ccc-9a02-37c8ce7e40df",
      "sessao_id": "9efe84e5-cbe9-4596-be57-04e56c5e7f9e",
      "viagem_id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
      "carga_id": "f3cc932c-61f0-4bd4-96a8-9565d0eadbcb",
      "tipo": "TEMPERATURA_FORA_DA_FAIXA",
      "nivel": "ATENCAO",
      "status": "ABERTO",
      "iniciado_em": "2026-11-23T14:57:06.951928Z",
      "finalizado_em": null,
      "evidencias_total": 1,
      "classificacao_risco_etileno": "NAO_AVALIADO",
      "intervencao": "AVALIACAO_HUMANA_NECESSARIA"
    },
    {
      "id": "7c626e70-1f75-45b4-ab1c-1e85cb97e0de",
      "sessao_id": "9efe84e5-cbe9-4596-be57-04e56c5e7f9e",
      "viagem_id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
      "carga_id": "f3cc932c-61f0-4bd4-96a8-9565d0eadbcb",
      "tipo": "EXPOSICAO_AMBIENTAL_PROLONGADA",
      "nivel": "ATENCAO",
      "status": "ABERTO",
      "iniciado_em": "2026-11-23T14:57:06.951928Z",
      "finalizado_em": null,
      "evidencias_total": 1,
      "classificacao_risco_etileno": "NAO_AVALIADO",
      "intervencao": "AVALIACAO_HUMANA_NECESSARIA"
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 422.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_read_auth_required[/alertas]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`

## API-068 — GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}

Consultar alerta ambiental

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:58](../../app/modules/monitoramento/preventivo_routes.py#L58) · `alerta` · operationId `alerta_api_v1_monitoramentos__sessao_id__alertas__alerta_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | alerta_id | True | {   "type": "string",   "format": "uuid",   "title": "Alerta Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AlertaResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/alertas/{alerta_id}',response_model=AlertaResponse,summary='Consultar alerta ambiental')
def alerta(sessao_id:UUID,alerta_id:UUID,svc=Depends(servico)):
    return svc.consultar_alerta(sessao_id,alerta_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/9efe84e5-cbe9-4596-be57-04e56c5e7f9e/alertas/8ef3f653-5485-4ccc-9a02-37c8ce7e40df`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "8ef3f653-5485-4ccc-9a02-37c8ce7e40df",
  "sessao_id": "9efe84e5-cbe9-4596-be57-04e56c5e7f9e",
  "viagem_id": "46687c15-7e9a-411f-a2ae-6f5944eab8db",
  "carga_id": "f3cc932c-61f0-4bd4-96a8-9565d0eadbcb",
  "tipo": "TEMPERATURA_FORA_DA_FAIXA",
  "nivel": "ATENCAO",
  "status": "EM_ANALISE",
  "iniciado_em": "2026-11-23T14:57:06.951928Z",
  "finalizado_em": null,
  "evidencias_total": 1,
  "classificacao_risco_etileno": "NAO_AVALIADO",
  "intervencao": "AVALIACAO_HUMANA_NECESSARIA"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_cutoff_revision_window_and_session_scoping`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_closed_late_complement_adds_evidence_without_rewriting_old`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_missing_configuration_is_informational_not_scientific_guess`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[11-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-89-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[13-96-UMIDADE_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[15-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_observed_outside_range_has_explainable_evidence[25-92-TEMPERATURA_FORA_DA_FAIXA]`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_openapi_and_no_gas_detection_labels`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_return_to_range_never_auto_resolves_alerts`

## API-069 — POST /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes

Reconhecer, observar, resolver ou descartar com justificativa

RECONHECER: ABERTO→EM_ANALISE (estado legado). Resolver/descartar: ABERTO ou EM_ANALISE→terminal.

Justificativa, ator e horario sao obrigatorios. OBSERVAR acrescenta nota sem mudar estado, inclusive apos fechamento.
Nenhuma transicao ou leitura posterior reabre ou encerra automaticamente um alerta.

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:63](../../app/modules/monitoramento/preventivo_routes.py#L63) · `decidir` · operationId `decidir_api_v1_monitoramentos__sessao_id__alertas__alerta_id__decisoes_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: DecisaoCreate.
- Efeito: Registra decisão/ocorrência e transição humana do alerta; OBSERVAR não muda estado.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | alerta_id | True | {   "type": "string",   "format": "uuid",   "title": "Alerta Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | DecisaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/alertas/{alerta_id}/decisoes',response_model=DecisaoResponse,summary='Reconhecer, observar, resolver ou descartar com justificativa')
def decidir(sessao_id:UUID,alerta_id:UUID,data:DecisaoCreate,svc=Depends(servico)):
    """RECONHECER: ABERTO→EM_ANALISE (estado legado). Resolver/descartar: ABERTO ou EM_ANALISE→terminal.

    Justificativa, ator e horario sao obrigatorios. OBSERVAR acrescenta nota sem mudar estado, inclusive apos fechamento.
    Nenhuma transicao ou leitura posterior reabre ou encerra automaticamente um alerta.
    """
    return svc.decidir(sessao_id,alerta_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/206579f7-e203-4d8d-9de3-afcd793b7aa0/alertas/fee9fb6a-aedc-4c8a-b817-a075258bd396/decisoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "9aae6235-b0e0-4400-8409-2bd02b455893",
  "acao": "RESOLVER",
  "justificativa": "Operador verificou a evidencia ambiental."
}
```

Resposta capturada:

```json
{
  "id": "102fddfc-51bc-4dad-81cd-88d7b133c5d0",
  "created_at": "2026-11-23T14:55:50Z",
  "updated_at": "2026-11-23T14:55:50Z",
  "sessao_id": "206579f7-e203-4d8d-9de3-afcd793b7aa0",
  "alerta_id": "fee9fb6a-aedc-4c8a-b817-a075258bd396",
  "ocorrencia_id": "3dcc9a7d-701a-4a1f-9c7e-efdc934fa707",
  "usuario_id": "77947cc1-422c-4ca9-b46e-c6bfe6ff8948",
  "acao": "RESOLVER",
  "justificativa": "Operador verificou a evidencia ambiental.",
  "estado_anterior": "ABERTO",
  "estado_posterior": "RESOLVIDO",
  "registrada_em": "2026-11-23T14:55:50.267074Z"
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 409, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cancelled_keeps_decisions_and_rejects_new_eval_config`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_failure_rolls_back_status_and_history`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_real_new_condition_after_resolution_creates_new_case`

## API-070 — GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes

Consultar historico auditavel de decisoes

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:73](../../app/modules/monitoramento/preventivo_routes.py#L73) · `decisoes` · operationId `decisoes_api_v1_monitoramentos__sessao_id__alertas__alerta_id__decisoes_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | alerta_id | True | {   "type": "string",   "format": "uuid",   "title": "Alerta Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaDecisoes; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/alertas/{alerta_id}/decisoes',response_model=ListaDecisoes,summary='Consultar historico auditavel de decisoes')
def decisoes(sessao_id:UUID,alerta_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,alerta_id,'decisoes',limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/67179868-7694-4b31-b667-f7ea94effa39/alertas/673eb9fe-42d8-4e52-a114-7e7495d74fa4/decisoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 4,
  "limit": 20,
  "offset": 0,
  "decisoes": [
    {
      "id": "e7aea26b-3f6d-4b58-80cb-f6fa5e9d9c71",
      "created_at": "2026-11-23T14:59:12Z",
      "updated_at": "2026-11-23T14:59:12Z",
      "sessao_id": "67179868-7694-4b31-b667-f7ea94effa39",
      "alerta_id": "673eb9fe-42d8-4e52-a114-7e7495d74fa4",
      "ocorrencia_id": "27a876a0-476e-449c-a482-b05d465b1e3f",
      "usuario_id": "dd02cf45-03a7-411c-8721-3017107629fc",
      "acao": "CRIAR",
      "justificativa": "Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.",
      "estado_anterior": null,
      "estado_posterior": "ABERTO",
      "registrada_em": "2026-11-23T14:59:12.870296Z"
    },
    {
      "id": "e61fbfbb-fa8b-4f49-b104-1ab118b4d6b4",
      "created_at": "2026-11-23T14:59:12Z",
      "updated_at": "2026-11-23T14:59:12Z",
      "sessao_id": "67179868-7694-4b31-b667-f7ea94effa39",
      "alerta_id": "673eb9fe-42d8-4e52-a114-7e7495d74fa4",
      "ocorrencia_id": "51e9ae7d-ef90-43cd-85fb-5b8e88904c0f",
      "usuario_id": "dd02cf45-03a7-411c-8721-3017107629fc",
      "acao": "RECONHECER",
      "justificativa": "Operador iniciou verificacao presencial.",
      "estado_anterior": "ABERTO",
      "estado_posterior": "EM_ANALISE",
      "registrada_em": "2026-11-23T14:59:12.904717Z"
    },
    {
      "id": "92c7fab0-4186-41f6-a3ff-085f2ae43ea5",
      "created_at": "2026-11-23T14:59:12Z",
      "updated_at": "2026-11-23T14:59:12Z",
      "sessao_id": "67179868-7694-4b31-b667-f7ea94effa39",
      "alerta_id": "673eb9fe-42d8-4e52-a114-7e7495d74fa4",
      "ocorrencia_id": "04459812-e3de-4249-964f-d35d3a979f19",
      "usuario_id": "dd02cf45-03a7-411c-8721-3017107629fc",
      "acao": "OBSERVAR",
      "justificativa": "Operador verificou a evidencia ambiental.",
      "estado_anterior": "EM_ANALISE",
      "estado_posterior": "EM_ANALISE",
      "registrada_em": "2026-11-23T14:59:12.937413Z"
    },
    {
      "id": "7d75c89c-8943-4734-9a50-bda82522bd22",
      "created_at": "2026-11-23T14:59:12Z",
      "updated_at": "2026-11-23T14:59:12Z",
      "sessao_id": "67179868-7694-4b31-b667-f7ea94effa39",
      "alerta_id": "673eb9fe-42d8-4e52-a114-7e7495d74fa4",
      "ocorrencia_id": "b60f87e3-048e-4e2b-bc1a-268188275acf",
      "usuario_id": "dd02cf45-03a7-411c-8721-3017107629fc",
      "acao": "RESOLVER",
      "justificativa": "Operador verificou a evidencia ambiental.",
      "estado_anterior": "EM_ANALISE",
      "estado_posterior": "RESOLVIDO",
      "registrada_em": "2026-11-23T14:59:12.945571Z"
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_decision_lifecycle_reuses_existing_alert_occurrence_models`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_exemplo_executavel_alerta_reconhecimento_historico`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`

## API-071 — GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/evidencias

Consultar evidencias e avaliacoes que sustentam o alerta

- Router/handler: [app/modules/monitoramento/preventivo_routes.py:78](../../app/modules/monitoramento/preventivo_routes.py#L78) · `evidencias` · operationId `evidencias_api_v1_monitoramentos__sessao_id__alertas__alerta_id__evidencias_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | alerta_id | True | {   "type": "string",   "format": "uuid",   "title": "Alerta Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaEvidencias; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consultar ou repetir mesma chave idempotente. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.preventivo_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/alertas/{alerta_id}/evidencias',response_model=ListaEvidencias,summary='Consultar evidencias e avaliacoes que sustentam o alerta')
def evidencias(sessao_id:UUID,alerta_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,alerta_id,'evidencias',limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/9371b9f5-121f-4b4d-9e7a-e579eb01276b/alertas/324d1f2b-c8cf-436a-bd3a-d7a5d21ffb21/evidencias`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 2,
  "limit": 20,
  "offset": 0,
  "evidencias": [
    {
      "id": "5dfdec95-06a2-4d5b-923e-5b4faca6a7bf",
      "avaliacao_id": "1bbb1f40-33d6-44f4-882a-9d5c2cc59e15",
      "alerta_id": "324d1f2b-c8cf-436a-bd3a-d7a5d21ffb21",
      "identidade": "dbcd2199b28e457769ed24ebd66804067099fcb54c26c86747312ae9b6f46f5c",
      "evidencia": {
        "regra": "TEMPERATURA_FORA_DA_FAIXA",
        "mensagem": "Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.",
        "evidencia": {
          "tipo": "TEMPERATURA",
          "minimo": "12",
          "maximo": "14",
          "pontos": [
            {
              "medida_em": "2026-11-23T11:04:05.435676Z",
              "valor": "20.0000",
              "registros": [
                "51916e10-9167-4d65-bd94-811173497537"
              ],
              "lado": "ACIMA"
            }
          ],
          "unidade": "C"
        },
        "nivel": "ATENCAO"
      }
    },
    {
      "id": "b9d1f584-3722-4354-87a2-aa93d57e623e",
      "avaliacao_id": "deb9a2c5-1e7d-46fa-8d9a-58d3fde8f17f",
      "alerta_id": "324d1f2b-c8cf-436a-bd3a-d7a5d21ffb21",
      "identidade": "dbcd2199b28e457769ed24ebd66804067099fcb54c26c86747312ae9b6f46f5c",
      "evidencia": {
        "regra": "TEMPERATURA_FORA_DA_FAIXA",
        "mensagem": "Valores ambientais observados fora da faixa operacional configurada; sem inferir dano ou etileno.",
        "evidencia": {
          "tipo": "TEMPERATURA",
          "minimo": "12",
          "maximo": "14",
          "pontos": [
            {
              "medida_em": "2026-11-23T11:04:05.435676Z",
              "valor": "20.0000",
              "registros": [
                "51916e10-9167-4d65-bd94-811173497537"
              ],
              "lado": "ACIMA"
            }
          ],
          "unidade": "C"
        },
        "nivel": "ATENCAO"
      }
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_active_extension_attaches_evidence_to_existing_open_cases`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_cross_session_api_and_composite_evidence_fk`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_discard_requires_justification_and_terminal_evidence_stays`<br>[tests/test_preventivo.py](../../tests/test_preventivo.py) `test_reader_scope_and_pagination`

## API-072 — POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas

Solicitar intervencao virtual com justificativa humana

Sessao/logistica ativas; alerta opcional da mesma sessao, ABERTO ou EM_ANALISE.

Uma solicitacao nao autoriza nem inicia. Duracao de demonstracao <=86400s, sem eficacia cientifica.
Referencias sao contextuais. Payload nao aceita dispositivos, protocolo, comandos fisicos ou estado imposto.

- Router/handler: [app/modules/monitoramento/exaustao_routes.py:19](../../app/modules/monitoramento/exaustao_routes.py#L19) · `solicitar` · operationId `solicitar_api_v1_monitoramentos__sessao_id__intervencoes_simuladas_post`.
- Perfil: ADMIN/GESTOR/OPERADOR.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: IntervencaoCreate.
- Efeito: Registra solicitação/ação, snapshots e ocorrência; locks e unicidade por veículo em EM_EXECUCAO. Nenhum comando físico.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | IntervencaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consulte ou repita mesma chave. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.exaustao_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('',response_model=IntervencaoResponse,summary='Solicitar intervencao virtual com justificativa humana')
def solicitar(sessao_id:UUID,data:IntervencaoCreate,svc=Depends(servico)):
    """Sessao/logistica ativas; alerta opcional da mesma sessao, ABERTO ou EM_ANALISE.

    Uma solicitacao nao autoriza nem inicia. Duracao de demonstracao <=86400s, sem eficacia cientifica.
    Referencias sao contextuais. Payload nao aceita dispositivos, protocolo, comandos fisicos ou estado imposto.
    """
    return svc.solicitar(sessao_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/a0c9293d-5650-4d54-b7be-723c2ce31118/intervencoes-simuladas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "45760043-e607-4aa4-abd3-dea1c663c2db",
  "justificativa": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
  "duracao_planejada_s": "60"
}
```

Resposta capturada:

```json
{
  "id": "76a7e6bb-92ca-4a5f-8f94-4e9eb2179628",
  "created_at": "2026-11-23T14:55:23Z",
  "updated_at": "2026-11-23T14:55:23Z",
  "sessao_id": "a0c9293d-5650-4d54-b7be-723c2ce31118",
  "viagem_id": "c1c5de51-9a64-497a-9488-d3b5e1a6c0bb",
  "carga_id": "c1b05719-b598-4820-9d35-7851679245e0",
  "veiculo_id": "bb663110-cfe6-4b14-9909-7bd6a579f3df",
  "atuador_virtual_id": "EXAUSTOR_VIRTUAL:VEICULO:bb663110-cfe6-4b14-9909-7bd6a579f3df",
  "alerta_id": null,
  "avaliacao_id": null,
  "analise_etileno_id": null,
  "solicitante_id": "5cd776b7-eddb-4df5-9871-a3fa81d99091",
  "decidida_por_id": null,
  "iniciada_por_id": null,
  "finalizada_por_id": null,
  "modalidade": "SIMULADA",
  "estado": "SOLICITADA",
  "chave_idempotencia": "45760043-e607-4aa4-abd3-dea1c663c2db",
  "justificativa_solicitacao": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
  "motivo_fim": null,
  "solicitada_em": "2026-11-23T14:55:23.031202Z",
  "decidida_em": null,
  "iniciada_em": null,
  "prazo_planejado_em": null,
  "finalizada_em": null,
  "duracao_planejada_s": "60.000",
  "duracao_registrada_s": null,
  "referencias_snapshot": {
    "sessao_id": "a0c9293d-5650-4d54-b7be-723c2ce31118",
    "estado_sessao": "ATIVA",
    "viagem_id": "c1c5de51-9a64-497a-9488-d3b5e1a6c0bb",
    "carga_id": "c1b05719-b598-4820-9d35-7851679245e0",
    "maturacao": "MISTA",
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "alerta": null,
    "avaliacao": null,
    "analise": null,
    "veiculo_id": "bb663110-cfe6-4b14-9909-7bd6a579f3df"
  },
  "hash_referencias": "917b7d4fd2ec5ec41a288f4a2c03a43d9ff0c3b3711da34f657b46e0bac7d031",
  "referencias_atuais": {
    "sessao_id": "a0c9293d-5650-4d54-b7be-723c2ce31118",
    "estado_sessao": "ATIVA",
    "viagem_id": "c1c5de51-9a64-497a-9488-d3b5e1a6c0bb",
    "carga_id": "c1b05719-b598-4820-9d35-7851679245e0",
    "maturacao": "MISTA",
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "alerta": null,
    "avaliacao": null,
    "analise": null
  },
  "hash_referencias_atuais": "8e41d54ce77595da1c04c450ccebc573adeabf0f38c58be535b379e8e008e9fb",
  "virtual_ligado": false,
  "atuador_virtual_ocupado": false,
  "prazo_excedido": false,
  "consultado_em": "2026-11-23T14:55:23.031202Z",
  "sessao_terminal_com_execucao": false,
  "contexto_logistico_alterado": false,
  "acoes_permitidas": [
    "CANCELAR"
  ],
  "classificacao_risco_etileno": "NAO_AVALIADO",
  "resultado_operacional": "ESTADO_VIRTUAL_SOLICITADA",
  "limitacoes": [
    "Atuador exclusivamente virtual; nenhuma mensagem ou comando fisico e enviado.",
    "Duracao de demonstracao, sem eficacia cientifica ou encerramento automatico.",
    "Nao altera medicoes, analises, amadurecimento, concentracao ou volume de etileno.",
    "Finalizacao comprova somente a transicao logica registrada; risco etileno NAO_AVALIADO."
  ]
}
```

Cenário negativo comprovado: HTTP 422, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes0]`.

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "justificativa"
      ],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

Matriz de respostas observadas: 200, 401, 403, 404, 409, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_action_secret_validation_and_justification`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[request]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_approval_by_admin_and_self_approval_policy_is_explicit`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_clock_regression_rejects_transition_without_partial_state`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_commit_failure_rolls_back_request`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[duracao_planejada_s-value2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[estado-LIGADO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[iniciada_em-value3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[modalidade-FISICA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_evaluation_must_sustain_selected_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_failure_is_explicit_simulated_and_terminal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_idempotent_request_and_actions_return_existing_records`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inactive_company_allows_cleanup_but_not_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes0]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes10]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes11]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes12]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes13]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes14]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes15]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes1]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes4]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes5]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes6]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes7]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes8]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_invalid_request_or_hardware_fields_rejected[changes9]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_logical_conflict_and_partial_unique_index`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[AUTORIZADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[EM_EXECUCAO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[SOLICITADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[AUTORIZAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[INICIAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[RECUSAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[REGISTRAR_FALHA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_precision_and_deadline_are_not_a_scientific_effect`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_replay_after_session_close_keeps_same_history`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[-----BEGIN PRIVATE KEY----- DEMO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[Bearer DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[api_key=DEMONSTRATION_SECRET]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[https://usuario:senha@example.invalid]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[password: DUMMY_PASSWORD]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_sensitive_justification_not_persisted[token=DUMMY_TOKEN]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_failure_rolls_back_all_execution_fields`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_without_authorization_and_terminal_reopening_rejected`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transaction_failure_request_and_action_rollback`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_vehicle_change_does_not_move_execution_or_allow_new_start`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_validation_errors_and_cors_do_not_expose_request_secrets`

## API-073 — GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas

Listar intervencoes da sessao

- Router/handler: [app/modules/monitoramento/exaustao_routes.py:29](../../app/modules/monitoramento/exaustao_routes.py#L29) · `listar` · operationId `listar_api_v1_monitoramentos__sessao_id__intervencoes_simuladas_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |
| query | estado | False | {   "anyOf": [     {       "enum": [         "SOLICITADA",         "AUTORIZADA",         "RECUSADA",         "EM_EXECUCAO",         "CONCLUIDA",         "CANCELADA",         "FALHA_SIMULACAO"       ],       "type": "string"     },     {       "type": "null"     }   ],   "title": "Estado" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaIntervencoes; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consulte ou repita mesma chave. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.exaustao_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('',response_model=ListaIntervencoes,summary='Listar intervencoes da sessao')
def listar(sessao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),estado:EstadoIntervencao|None=None,svc=Depends(servico)):
    return svc.listar(sessao_id,limit,offset,estado)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/eb7121c5-fc78-4a16-afdb-d0891440d07b/intervencoes-simuladas`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 2,
  "limit": 1,
  "offset": 0,
  "intervencoes": [
    {
      "id": "23181379-437e-4cdf-bfe6-8ffa6bf74839",
      "created_at": "2026-11-23T14:55:57Z",
      "updated_at": "2026-11-23T14:55:57Z",
      "sessao_id": "eb7121c5-fc78-4a16-afdb-d0891440d07b",
      "viagem_id": "81387e2c-cd78-4958-95a1-30e117e9c191",
      "carga_id": "55d28552-93d5-419a-aaa4-ffdcefd0bcab",
      "veiculo_id": "8a30c68d-0194-4fe1-a17a-88e7c3564434",
      "atuador_virtual_id": "EXAUSTOR_VIRTUAL:VEICULO:8a30c68d-0194-4fe1-a17a-88e7c3564434",
      "alerta_id": null,
      "avaliacao_id": null,
      "analise_etileno_id": null,
      "solicitante_id": "db323499-f432-4520-8df7-ed1f88ca6234",
      "decidida_por_id": null,
      "iniciada_por_id": null,
      "finalizada_por_id": null,
      "modalidade": "SIMULADA",
      "estado": "SOLICITADA",
      "chave_idempotencia": "50f2ffaa-0a41-4a39-80ff-90786c98f782",
      "justificativa_solicitacao": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
      "motivo_fim": null,
      "solicitada_em": "2026-11-23T14:55:58.220725Z",
      "decidida_em": null,
      "iniciada_em": null,
      "prazo_planejado_em": null,
      "finalizada_em": null,
      "duracao_planejada_s": "60.000",
      "duracao_registrada_s": null,
      "referencias_snapshot": {
        "sessao_id": "eb7121c5-fc78-4a16-afdb-d0891440d07b",
        "estado_sessao": "ATIVA",
        "viagem_id": "81387e2c-cd78-4958-95a1-30e117e9c191",
        "carga_id": "55d28552-93d5-419a-aaa4-ffdcefd0bcab",
        "maturacao": "MISTA",
        "ambiente": "TRANSPORTE_REFRIGERADO",
        "alerta": null,
        "avaliacao": null,
        "analise": null,
        "veiculo_id": "8a30c68d-0194-4fe1-a17a-88e7c3564434"
      },
      "hash_referencias": "0b40c99f0cfd1fa7b62846c78b8c5128960938f7af4c4bd2129ecd170a63a6a1",
      "referencias_atuais": {
        "sessao_id": "eb7121c5-fc78-4a16-afdb-d0891440d07b",
        "estado_sessao": "ATIVA",
        "viagem_id": "81387e2c-cd78-4958-95a1-30e117e9c191",
        "carga_id": "55d28552-93d5-419a-aaa4-ffdcefd0bcab",
        "maturacao": "MISTA",
        "ambiente": "TRANSPORTE_REFRIGERADO",
        "alerta": null,
        "avaliacao": null,
        "analise": null
      },
      "hash_referencias_atuais": "6fb1f62d7d264b1686469940692b60ca91e30964f5fc80f32a51e8860d0c8d26",
      "virtual_ligado": false,
      "atuador_virtual_ocupado": false,
      "prazo_excedido": false,
      "consultado_em": "2026-11-23T14:55:58.220725Z",
      "sessao_terminal_com_execucao": false,
      "contexto_logistico_alterado": false,
      "acoes_permitidas": [],
      "classificacao_risco_etileno": "NAO_AVALIADO",
      "resultado_operacional": "ESTADO_VIRTUAL_SOLICITADA",
      "limitacoes": [
        "Atuador exclusivamente virtual; nenhuma mensagem ou comando fisico e enviado.",
        "Duracao de demonstracao, sem eficacia cientifica ou encerramento automatico.",
        "Nao altera medicoes, analises, amadurecimento, concentracao ou volume de etileno.",
        "Finalizacao comprova somente a transicao logica registrada; risco etileno NAO_AVALIADO."
      ]
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[list]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[list]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## API-074 — GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}

Consultar estado logico e permissoes atuais

virtual_ligado reflete apenas EM_EXECUCAO persistido. Prazo excedido nao conclui a execucao.

consultado_em fixa o instante da projecao; nenhuma consulta altera estado. Nao estima remocao de gas.

- Router/handler: [app/modules/monitoramento/exaustao_routes.py:34](../../app/modules/monitoramento/exaustao_routes.py#L34) · `consultar` · operationId `consultar_api_v1_monitoramentos__sessao_id__intervencoes_simuladas__intervencao_id__get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | intervencao_id | True | {   "type": "string",   "format": "uuid",   "title": "Intervencao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | IntervencaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consulte ou repita mesma chave. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.exaustao_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{intervencao_id}',response_model=IntervencaoResponse,summary='Consultar estado logico e permissoes atuais')
def consultar(sessao_id:UUID,intervencao_id:UUID,svc=Depends(servico)):
    """virtual_ligado reflete apenas EM_EXECUCAO persistido. Prazo excedido nao conclui a execucao.

    consultado_em fixa o instante da projecao; nenhuma consulta altera estado. Nao estima remocao de gas.
    """
    return svc.consultar(sessao_id,intervencao_id)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/c1d88a62-50af-4c88-b1bd-4e0572521a80/intervencoes-simuladas/5074a674-253e-4dd0-bfc9-e267a61f0790`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "id": "5074a674-253e-4dd0-bfc9-e267a61f0790",
  "created_at": "2026-11-23T14:55:23Z",
  "updated_at": "2026-11-23T14:55:23Z",
  "sessao_id": "c1d88a62-50af-4c88-b1bd-4e0572521a80",
  "viagem_id": "c34b7bfd-2db5-4f39-8721-e9391f7eb4c5",
  "carga_id": "795cab47-0009-4b1c-a661-efa96b63c640",
  "veiculo_id": "7a605910-8b3c-4a52-adb2-b85895630feb",
  "atuador_virtual_id": "EXAUSTOR_VIRTUAL:VEICULO:7a605910-8b3c-4a52-adb2-b85895630feb",
  "alerta_id": null,
  "avaliacao_id": null,
  "analise_etileno_id": null,
  "solicitante_id": "2b696300-8087-4060-bab6-de674fe5dffa",
  "decidida_por_id": "f0dbf3d8-15cc-40be-bf2d-6ef257d04928",
  "iniciada_por_id": null,
  "finalizada_por_id": null,
  "modalidade": "SIMULADA",
  "estado": "AUTORIZADA",
  "chave_idempotencia": "b2343ed8-d329-4d56-b0c1-a05165215950",
  "justificativa_solicitacao": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
  "motivo_fim": null,
  "solicitada_em": "2026-11-23T14:55:23.652140Z",
  "decidida_em": "2026-11-23T14:55:23.652140Z",
  "iniciada_em": null,
  "prazo_planejado_em": null,
  "finalizada_em": null,
  "duracao_planejada_s": "60.000",
  "duracao_registrada_s": null,
  "referencias_snapshot": {
    "sessao_id": "c1d88a62-50af-4c88-b1bd-4e0572521a80",
    "estado_sessao": "ATIVA",
    "viagem_id": "c34b7bfd-2db5-4f39-8721-e9391f7eb4c5",
    "carga_id": "795cab47-0009-4b1c-a661-efa96b63c640",
    "maturacao": "MISTA",
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "alerta": null,
    "avaliacao": null,
    "analise": null,
    "veiculo_id": "7a605910-8b3c-4a52-adb2-b85895630feb"
  },
  "hash_referencias": "6812c2402c7b67c7e4b9e4dbcbac4201bf7d8142c2ada1ddd38ef9bba78421a7",
  "referencias_atuais": {
    "sessao_id": "c1d88a62-50af-4c88-b1bd-4e0572521a80",
    "estado_sessao": "ATIVA",
    "viagem_id": "c34b7bfd-2db5-4f39-8721-e9391f7eb4c5",
    "carga_id": "795cab47-0009-4b1c-a661-efa96b63c640",
    "maturacao": "MISTA",
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "alerta": null,
    "avaliacao": null,
    "analise": null
  },
  "hash_referencias_atuais": "37574c2297e4c28b9905a0ab585b8eea76e2e70dc3737ef91c12c9e20a24fb50",
  "virtual_ligado": false,
  "atuador_virtual_ocupado": false,
  "prazo_excedido": false,
  "consultado_em": "2026-11-23T14:55:23.652140Z",
  "sessao_terminal_com_execucao": false,
  "contexto_logistico_alterado": false,
  "acoes_permitidas": [],
  "classificacao_risco_etileno": "NAO_AVALIADO",
  "resultado_operacional": "ESTADO_VIRTUAL_AUTORIZADA",
  "limitacoes": [
    "Atuador exclusivamente virtual; nenhuma mensagem ou comando fisico e enviado.",
    "Duracao de demonstracao, sem eficacia cientifica ou encerramento automatico.",
    "Nao altera medicoes, analises, amadurecimento, concentracao ou volume de etileno.",
    "Finalizacao comprova somente a transicao logica registrada; risco etileno NAO_AVALIADO."
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[get]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[get]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_clock_regression_rejects_transition_without_partial_state`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[duracao_planejada_s-value2]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[estado-LIGADO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[iniciada_em-value3]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_database_checks_reject_inconsistent_intervention[modalidade-FISICA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_failure_is_explicit_simulated_and_terminal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_logical_conflict_and_partial_unique_index`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[AUTORIZADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[EM_EXECUCAO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[SOLICITADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_precision_and_deadline_are_not_a_scientific_effect`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_failure_rolls_back_all_execution_fields`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_without_authorization_and_terminal_reopening_rejected`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transaction_failure_request_and_action_rollback`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_vehicle_change_does_not_move_execution_or_allow_new_start`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## API-075 — POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes

Registrar decisao humana ou transicao virtual

GESTOR/ADMIN autoriza, recusa, inicia, cancela e registra falha. Solicitante OPERADOR retira
SOLICITADA ou encerra a propria execucao. CONSULTA somente le. Encerramento administrativo funciona
mesmo apos fim/cancelamento da sessao. Autorizacao e inicio sao acoes separadas; nao ha scheduler.
Justificativa obrigatoria, sem credenciais. Repeticao idempotente recupera a mesma acao historica.

- Router/handler: [app/modules/monitoramento/exaustao_routes.py:43](../../app/modules/monitoramento/exaustao_routes.py#L43) · `agir` · operationId `agir_api_v1_monitoramentos__sessao_id__intervencoes_simuladas__intervencao_id__acoes_post`.
- Perfil: Por ação: ADMIN/GESTOR; OPERADOR somente cancela SOLICITADA própria ou encerra execução própria.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; `Content-Type: application/json`.
- Body: obrigatório; application/json: AcaoCreate.
- Efeito: Registra solicitação/ação, snapshots e ocorrência; locks e unicidade por veículo em EM_EXECUCAO. Nenhum comando físico.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | intervencao_id | True | {   "type": "string",   "format": "uuid",   "title": "Intervencao Id" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | AcaoResponse; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consulte ou repita mesma chave. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.exaustao_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.post('/{intervencao_id}/acoes',response_model=AcaoResponse,summary='Registrar decisao humana ou transicao virtual')
def agir(sessao_id:UUID,intervencao_id:UUID,data:AcaoCreate,svc=Depends(servico)):
    """GESTOR/ADMIN autoriza, recusa, inicia, cancela e registra falha. Solicitante OPERADOR retira
    SOLICITADA ou encerra a propria execucao. CONSULTA somente le. Encerramento administrativo funciona
    mesmo apos fim/cancelamento da sessao. Autorizacao e inicio sao acoes separadas; nao ha scheduler.
    Justificativa obrigatoria, sem credenciais. Repeticao idempotente recupera a mesma acao historica.
    """
    return svc.agir(sessao_id,intervencao_id,data)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`.

Caminho concreto da fixture: `POST /api/v1/monitoramentos/c1d88a62-50af-4c88-b1bd-4e0572521a80/intervencoes-simuladas/5074a674-253e-4dd0-bfc9-e267a61f0790/acoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
```json
{
  "chave_idempotencia": "bc592a73-5e07-4d49-bd7c-21c8871543d1",
  "acao": "AUTORIZAR",
  "justificativa": "Responsavel confirmou a decisao virtual."
}
```

Resposta capturada:

```json
{
  "id": "bafd1e73-d8ad-436c-b35d-518ad4ac9f37",
  "created_at": "2026-11-23T14:55:23Z",
  "updated_at": "2026-11-23T14:55:23Z",
  "sessao_id": "c1d88a62-50af-4c88-b1bd-4e0572521a80",
  "intervencao_id": "5074a674-253e-4dd0-bfc9-e267a61f0790",
  "ocorrencia_id": "bec31080-cd90-40b3-957c-53846559a506",
  "usuario_id": "f0dbf3d8-15cc-40be-bf2d-6ef257d04928",
  "chave_idempotencia": "bc592a73-5e07-4d49-bd7c-21c8871543d1",
  "numero": 2,
  "acao": "AUTORIZAR",
  "justificativa": "Responsavel confirmou a decisao virtual.",
  "estado_anterior": "SOLICITADA",
  "estado_posterior": "AUTORIZADA",
  "registrada_em": "2026-11-23T14:55:23.652140Z",
  "contexto_snapshot": {
    "sessao_id": "c1d88a62-50af-4c88-b1bd-4e0572521a80",
    "estado_sessao": "ATIVA",
    "viagem_id": "c34b7bfd-2db5-4f39-8721-e9391f7eb4c5",
    "carga_id": "795cab47-0009-4b1c-a661-efa96b63c640",
    "maturacao": "MISTA",
    "ambiente": "TRANSPORTE_REFRIGERADO",
    "alerta": null,
    "avaliacao": null,
    "analise": null,
    "contexto_logistico_alterado": false,
    "modalidade": "SIMULADA",
    "hash_referencias_solicitacao": "6812c2402c7b67c7e4b9e4dbcbac4201bf7d8142c2ada1ddd38ef9bba78421a7"
  }
}
```

Cenário negativo comprovado: HTTP 409, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`.

```json
{
  "detail": "Transicao de intervencao invalida; terminal nao pode ser reaberto."
}
```

Matriz de respostas observadas: 200, 401, 403, 404, 409, 422, 503.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_action_secret_validation_and_justification`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[action]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_approval_by_admin_and_self_approval_policy_is_explicit`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_clock_regression_rejects_transition_without_partial_state`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_closed_session_after_authorization_prevents_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_failure_is_explicit_simulated_and_terminal`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_idempotent_request_and_actions_return_existing_records`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inactive_company_allows_cleanup_but_not_start`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_logical_conflict_and_partial_unique_index`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[AUTORIZADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[EM_EXECUCAO]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_manager_cancels_each_nonterminal_state[SOLICITADA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_no_automatic_actions_or_data_changes_when_time_passes`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[AUTORIZAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[INICIAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[RECUSAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_operator_cannot_make_privileged_decisions[REGISTRAR_FALHA]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_precision_and_deadline_are_not_a_scientific_effect`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_recognized_alert_is_context_not_automatic_authorization`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_refusal_never_resolves_original_alert`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_scientific_records_and_alerts_are_unchanged_and_no_io`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_failure_rolls_back_all_execution_fields`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_start_without_authorization_and_terminal_reopening_rejected`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[DESCARTAR]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_alert_blocks_request_authorization_and_start[RESOLVER]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[cancelar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_terminal_session_blocks_new_actions_but_allows_administrative_stop[encerrar]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transaction_failure_request_and_action_rollback`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_vehicle_change_does_not_move_execution_or_allow_new_start`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## API-076 — GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes

Consultar trilha ordenada de decisoes e transicoes

- Router/handler: [app/modules/monitoramento/exaustao_routes.py:53](../../app/modules/monitoramento/exaustao_routes.py#L53) · `historico` · operationId `historico_api_v1_monitoramentos__sessao_id__intervencoes_simuladas__intervencao_id__acoes_get`.
- Perfil: ADMIN/GESTOR/OPERADOR/CONSULTA.
- Escopo: Viagem → transportadora persistida; carga → viagem; sessão → carga/viagem. ADMIN global; demais com vínculo/empresa ativos.
- Headers: `Authorization: Bearer <JWT>`; sem body declarado.
- Body: ausente.
- Efeito: Consulta; não produz transição de estado. Login/me e projeções seguem seus handlers.

| Local | Nome | Obrigatório | Tipo / validações declaradas |
| --- | --- | --- | --- |
| path | sessao_id | True | {   "type": "string",   "format": "uuid",   "title": "Sessao Id" } |
| path | intervencao_id | True | {   "type": "string",   "format": "uuid",   "title": "Intervencao Id" } |
| query | limit | False | {   "type": "integer",   "maximum": 100,   "minimum": 1,   "default": 20,   "title": "Limit" } |
| query | offset | False | {   "type": "integer",   "minimum": 0,   "default": 0,   "title": "Offset" } |


Respostas declaradas no Swagger (não equivalem a todos os erros do serviço):

| HTTP | Schema / descrição |
| --- | --- |
| 200 | ListaAcoes; Successful Response |
| 401 | ; Autenticacao ausente, invalida ou usuario inativo. |
| 403 | ; Perfil ou vinculo empresarial sem permissao. |
| 404 | ; Carga, viagem, configuracao, sessao ou sensor nao encontrado. |
| 409 | ; Conflito temporal, estado, integridade ou chave idempotente. |
| 422 | ; Dados, horarios, massa ou sensores invalidos. |
| 503 | ; Falha transacional; consulte ou repita mesma chave. |


Dependências reais (recursivas; incluem banco, JWT e factories de services):

```json
[
  {
    "call": "servico",
    "module": "app.modules.monitoramento.exaustao_routes",
    "children": [
      {
        "call": "get_database_session",
        "module": "app.api.deps",
        "children": []
      },
      {
        "call": "get_current_user",
        "module": "app.api.deps",
        "children": [
          {
            "call": "<fastapi.security.http.HTTPBearer object at 0x000001A30469FB60>",
            "module": "fastapi.security.http",
            "children": []
          },
          {
            "call": "get_database_session",
            "module": "app.api.deps",
            "children": []
          }
        ]
      }
    ]
  }
]
```

Encaminhamento e condições documentadas pelo handler:

```python
@router.get('/{intervencao_id}/acoes',response_model=ListaAcoes,summary='Consultar trilha ordenada de decisoes e transicoes')
def historico(sessao_id:UUID,intervencao_id:UUID,limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),svc=Depends(servico)):
    return svc.historico(sessao_id,intervencao_id,limit,offset)

```

Cenário de sucesso comprovado: HTTP 200, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`.

Caminho concreto da fixture: `GET /api/v1/monitoramentos/a0c9293d-5650-4d54-b7be-723c2ce31118/intervencoes-simuladas/76a7e6bb-92ca-4a5f-8f94-4e9eb2179628/acoes`. A captura não retém query/headers; consultar o teste vinculado para reproduzir o cenário exato.
Resposta capturada:

```json
{
  "total": 1,
  "limit": 20,
  "offset": 0,
  "acoes": [
    {
      "id": "863f6513-6715-4bce-86c9-f8e87dd711d5",
      "created_at": "2026-11-23T14:55:23Z",
      "updated_at": "2026-11-23T14:55:23Z",
      "sessao_id": "a0c9293d-5650-4d54-b7be-723c2ce31118",
      "intervencao_id": "76a7e6bb-92ca-4a5f-8f94-4e9eb2179628",
      "ocorrencia_id": "03a839dd-bd35-4ddd-816b-c3744f97d87a",
      "usuario_id": "5cd776b7-eddb-4df5-9871-a3fa81d99091",
      "chave_idempotencia": "45760043-e607-4aa4-abd3-dea1c663c2db",
      "numero": 1,
      "acao": "SOLICITAR",
      "justificativa": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
      "estado_anterior": null,
      "estado_posterior": "SOLICITADA",
      "registrada_em": "2026-11-23T14:55:23.031202Z",
      "contexto_snapshot": {
        "sessao_id": "a0c9293d-5650-4d54-b7be-723c2ce31118",
        "estado_sessao": "ATIVA",
        "viagem_id": "c1c5de51-9a64-497a-9488-d3b5e1a6c0bb",
        "carga_id": "c1b05719-b598-4820-9d35-7851679245e0",
        "maturacao": "MISTA",
        "ambiente": "TRANSPORTE_REFRIGERADO",
        "alerta": null,
        "avaliacao": null,
        "analise": null,
        "veiculo_id": "bb663110-cfe6-4b14-9909-7bd6a579f3df"
      }
    }
  ]
}
```

Cenário negativo comprovado: HTTP 401, [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[history]`.

```json
{
  "detail": "Credenciais invalidas."
}
```

Matriz de respostas observadas: 200, 401, 403, 404.

Testes HTTP que atingiram esta rota:
[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_all_routes_require_authentication[history]`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_authorization_is_separate_from_start_and_explicit_end`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_decisions_pin_evidence_set_as_it_existed_at_each_action`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_exemplo_executavel_solicitar_autorizar_iniciar_encerrar`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_foreign_session_alert_evaluation_analysis_and_intervention_are_denied`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_inconsistent_references_do_not_prevent_administrative_stop`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_reader_pagination_and_ownership_rules`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_replay_after_session_close_keeps_same_history`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_request_without_alert_is_pending_and_audited`<br>[tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) `test_transport_scope_applies_to_reads_writes_and_cleanup`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_all_new_monitoring_routes_declare_and_enforce_bearer_auth`<br>[tests/test_integracao_etapa8.py](../../tests/test_integracao_etapa8.py) `test_fluxo_integrado_ponta_a_ponta_etapa8`

## Dicionário integral de schemas

`required` identifica presença obrigatória; aceitar null é outra propriedade. `default` não é evidência de aplicação científica. Decimal possui caminhos de entrada numérica/string e saída string. Os validadores de domínio podem impor requisitos adicionais; consultar RN e inventário de erros.

### AcaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "acao": {
      "type": "string",
      "enum": [
        "AUTORIZAR",
        "RECUSAR",
        "INICIAR",
        "ENCERRAR",
        "CANCELAR",
        "REGISTRAR_FALHA"
      ],
      "title": "Acao"
    },
    "justificativa": {
      "type": "string",
      "maxLength": 4000,
      "minLength": 1,
      "title": "Justificativa"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia",
    "acao",
    "justificativa"
  ],
  "title": "AcaoCreate"
}
```

### AcaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "intervencao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Intervencao Id"
    },
    "ocorrencia_id": {
      "type": "string",
      "format": "uuid",
      "title": "Ocorrencia Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "numero": {
      "type": "integer",
      "title": "Numero"
    },
    "acao": {
      "type": "string",
      "title": "Acao"
    },
    "justificativa": {
      "type": "string",
      "title": "Justificativa"
    },
    "estado_anterior": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Estado Anterior"
    },
    "estado_posterior": {
      "type": "string",
      "enum": [
        "SOLICITADA",
        "AUTORIZADA",
        "RECUSADA",
        "EM_EXECUCAO",
        "CONCLUIDA",
        "CANCELADA",
        "FALHA_SIMULACAO"
      ],
      "title": "Estado Posterior"
    },
    "registrada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Registrada Em"
    },
    "contexto_snapshot": {
      "type": "object",
      "title": "Contexto Snapshot"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "intervencao_id",
    "ocorrencia_id",
    "usuario_id",
    "chave_idempotencia",
    "numero",
    "acao",
    "justificativa",
    "estado_anterior",
    "estado_posterior",
    "registrada_em",
    "contexto_snapshot"
  ],
  "title": "AcaoResponse"
}
```

### AlertaResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "viagem_id": {
      "type": "string",
      "format": "uuid",
      "title": "Viagem Id"
    },
    "carga_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Carga Id"
    },
    "tipo": {
      "type": "string",
      "title": "Tipo"
    },
    "nivel": {
      "type": "string",
      "enum": [
        "INFORMATIVO",
        "ATENCAO",
        "CRITICO"
      ],
      "title": "Nivel"
    },
    "status": {
      "type": "string",
      "enum": [
        "ABERTO",
        "EM_ANALISE",
        "RESOLVIDO",
        "DESCARTADO"
      ],
      "title": "Status"
    },
    "iniciado_em": {
      "type": "string",
      "format": "date-time",
      "title": "Iniciado Em"
    },
    "finalizado_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizado Em"
    },
    "evidencias_total": {
      "type": "integer",
      "title": "Evidencias Total"
    },
    "classificacao_risco_etileno": {
      "type": "string",
      "enum": [
        "NAO_AVALIADO"
      ],
      "const": "NAO_AVALIADO",
      "title": "Classificacao Risco Etileno",
      "default": "NAO_AVALIADO"
    },
    "intervencao": {
      "type": "string",
      "enum": [
        "AVALIACAO_HUMANA_NECESSARIA"
      ],
      "const": "AVALIACAO_HUMANA_NECESSARIA",
      "title": "Intervencao",
      "default": "AVALIACAO_HUMANA_NECESSARIA"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "sessao_id",
    "viagem_id",
    "carga_id",
    "tipo",
    "nivel",
    "status",
    "iniciado_em",
    "finalizado_em",
    "evidencias_total"
  ],
  "title": "AlertaResponse"
}
```

### AnaliseCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "modo": {
      "$ref": "#/components/schemas/ModoCalculo",
      "default": "MODO_RESTRITO"
    },
    "intervalo_maximo_s": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Intervalo Maximo S",
      "description": "G operacional explicito. Ausencia persiste CONFIGURACAO_INCOMPLETA, sem volumes."
    },
    "inicio": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "corte_aquisicao": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Corte Aquisicao",
      "description": "Obrigatorio para sessao ativa; inclui apenas revisoes consolidadas ate este instante. Nunca futuro."
    },
    "revisao_aquisicao": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0.0
        },
        {
          "type": "null"
        }
      ],
      "title": "Revisao Aquisicao",
      "description": "Revisao consolidada; 0 representa ausencia de aquisicao. Omissao fixa a ultima elegivel no corte."
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia"
  ],
  "title": "AnaliseCreate"
}
```

### AnaliseLista

```json
{
  "properties": {
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "analises": {
      "items": {
        "$ref": "#/components/schemas/AnaliseResponse"
      },
      "type": "array",
      "title": "Analises"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "sessao_id",
    "total",
    "limit",
    "offset",
    "analises"
  ],
  "title": "AnaliseLista"
}
```

### AnaliseResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "executada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Executada Em"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "corte_aquisicao": {
      "type": "string",
      "format": "date-time",
      "title": "Corte Aquisicao"
    },
    "revisao_aquisicao": {
      "type": "integer",
      "title": "Revisao Aquisicao"
    },
    "massa_kg": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Massa Kg"
    },
    "maturacao": {
      "type": "string",
      "title": "Maturacao"
    },
    "modo": {
      "$ref": "#/components/schemas/ModoCalculo"
    },
    "intervalo_maximo_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Intervalo Maximo S"
    },
    "versao_modelo": {
      "type": "string",
      "title": "Versao Modelo"
    },
    "status_calculo": {
      "$ref": "#/components/schemas/StatusCalculo"
    },
    "classificacao_risco_etileno": {
      "type": "string",
      "enum": [
        "NAO_AVALIADO"
      ],
      "const": "NAO_AVALIADO",
      "title": "Classificacao Risco Etileno"
    },
    "hash_entrada": {
      "type": "string",
      "title": "Hash Entrada"
    },
    "hash_resultado": {
      "type": "string",
      "title": "Hash Resultado"
    },
    "entrada_snapshot": {
      "type": "object",
      "title": "Entrada Snapshot"
    },
    "resultado": {
      "$ref": "#/components/schemas/ResultadoResponse"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "usuario_id",
    "chave_idempotencia",
    "executada_em",
    "inicio",
    "fim",
    "corte_aquisicao",
    "revisao_aquisicao",
    "massa_kg",
    "maturacao",
    "modo",
    "intervalo_maximo_s",
    "versao_modelo",
    "status_calculo",
    "classificacao_risco_etileno",
    "hash_entrada",
    "hash_resultado",
    "entrada_snapshot",
    "resultado"
  ],
  "title": "AnaliseResponse"
}
```

### AvaliacaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "configuracao_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Configuracao Id"
    },
    "inicio": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "corte_aquisicao": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Corte Aquisicao"
    },
    "revisao": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0.0
        },
        {
          "type": "null"
        }
      ],
      "title": "Revisao"
    },
    "analise_etileno_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Analise Etileno Id"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia"
  ],
  "title": "AvaliacaoCreate"
}
```

### AvaliacaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "configuracao_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Configuracao Id"
    },
    "anterior_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Anterior Id"
    },
    "analise_etileno_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Analise Etileno Id"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "executada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Executada Em"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "corte_aquisicao": {
      "type": "string",
      "format": "date-time",
      "title": "Corte Aquisicao"
    },
    "revisao": {
      "type": "integer",
      "title": "Revisao"
    },
    "hash_entrada": {
      "type": "string",
      "title": "Hash Entrada"
    },
    "hash_resultado": {
      "type": "string",
      "title": "Hash Resultado"
    },
    "entrada_snapshot": {
      "type": "object",
      "title": "Entrada Snapshot"
    },
    "resultado": {
      "type": "object",
      "title": "Resultado"
    },
    "alertas_ids": {
      "items": {
        "type": "string",
        "format": "uuid"
      },
      "type": "array",
      "title": "Alertas Ids"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "usuario_id",
    "configuracao_id",
    "anterior_id",
    "analise_etileno_id",
    "chave_idempotencia",
    "executada_em",
    "inicio",
    "fim",
    "corte_aquisicao",
    "revisao",
    "hash_entrada",
    "hash_resultado",
    "entrada_snapshot",
    "resultado",
    "alertas_ids"
  ],
  "title": "AvaliacaoResponse"
}
```

### CaixaCreate

```json
{
  "properties": {
    "identificacao": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Identificacao"
    },
    "codigo_externo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Codigo Externo"
    },
    "peso": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Peso"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "identificacao"
  ],
  "title": "CaixaCreate"
}
```

### CaixaResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "identificacao": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Identificacao"
    },
    "codigo_externo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Codigo Externo"
    },
    "peso": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Peso"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "carga_id": {
      "type": "string",
      "format": "uuid",
      "title": "Carga Id"
    },
    "status": {
      "$ref": "#/components/schemas/StatusCaixa"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "identificacao",
    "carga_id",
    "status"
  ],
  "title": "CaixaResponse"
}
```

### CaixaUpdate

```json
{
  "properties": {
    "identificacao": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Identificacao"
    },
    "codigo_externo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Codigo Externo"
    },
    "peso": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Peso"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "status": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/StatusCaixa"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "CaixaUpdate"
}
```

### CargaCreate

```json
{
  "properties": {
    "produto_id": {
      "type": "string",
      "format": "uuid",
      "title": "Produto Id"
    },
    "produtor_id": {
      "type": "string",
      "format": "uuid",
      "title": "Produtor Id"
    },
    "cliente_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Cliente Id"
    },
    "identificacao": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Identificacao"
    },
    "quantidade_caixas": {
      "anyOf": [
        {
          "type": "integer",
          "maximum": 2147483647.0,
          "minimum": 0.0
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade Caixas"
    },
    "quantidade": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "origem_produto": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255
        },
        {
          "type": "null"
        }
      ],
      "title": "Origem Produto"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "produto_id",
    "produtor_id",
    "identificacao"
  ],
  "title": "CargaCreate"
}
```

### CargaMonitoramentoPut

```json
{
  "properties": {
    "produto_identificado": {
      "type": "string",
      "enum": [
        "MANGA_TOMMY_ATKINS"
      ],
      "const": "MANGA_TOMMY_ATKINS",
      "title": "Produto Identificado"
    },
    "massa_kg": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Massa Kg"
    },
    "maturacao": {
      "$ref": "#/components/schemas/MaturacaoCarga",
      "default": "DESCONHECIDA"
    },
    "lote_codigo": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Lote Codigo"
    },
    "lote_hipotetico": {
      "type": "boolean",
      "title": "Lote Hipotetico"
    },
    "rastreabilidade": {
      "type": "string",
      "maxLength": 2000,
      "minLength": 1,
      "title": "Rastreabilidade"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "produto_identificado",
    "massa_kg",
    "lote_codigo",
    "lote_hipotetico",
    "rastreabilidade"
  ],
  "title": "CargaMonitoramentoPut"
}
```

### CargaMonitoramentoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "carga_id": {
      "type": "string",
      "format": "uuid",
      "title": "Carga Id"
    },
    "produto_identificado": {
      "type": "string",
      "title": "Produto Identificado"
    },
    "massa_kg": {
      "type": "string",
      "title": "Massa Kg"
    },
    "maturacao": {
      "$ref": "#/components/schemas/MaturacaoCarga"
    },
    "lote_codigo": {
      "type": "string",
      "title": "Lote Codigo"
    },
    "lote_hipotetico": {
      "type": "boolean",
      "title": "Lote Hipotetico"
    },
    "rastreabilidade": {
      "type": "string",
      "title": "Rastreabilidade"
    },
    "versao": {
      "type": "integer",
      "title": "Versao"
    },
    "atualizado_por_id": {
      "type": "string",
      "format": "uuid",
      "title": "Atualizado Por Id"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "carga_id",
    "produto_identificado",
    "massa_kg",
    "maturacao",
    "lote_codigo",
    "lote_hipotetico",
    "rastreabilidade",
    "versao",
    "atualizado_por_id"
  ],
  "title": "CargaMonitoramentoResponse"
}
```

### CargaResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "produto_id": {
      "type": "string",
      "format": "uuid",
      "title": "Produto Id"
    },
    "produtor_id": {
      "type": "string",
      "format": "uuid",
      "title": "Produtor Id"
    },
    "cliente_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Cliente Id"
    },
    "identificacao": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Identificacao"
    },
    "quantidade_caixas": {
      "anyOf": [
        {
          "type": "integer",
          "maximum": 2147483647.0,
          "minimum": 0.0
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade Caixas"
    },
    "quantidade": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "origem_produto": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255
        },
        {
          "type": "null"
        }
      ],
      "title": "Origem Produto"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "viagem_id": {
      "type": "string",
      "format": "uuid",
      "title": "Viagem Id"
    },
    "status": {
      "$ref": "#/components/schemas/StatusCarga"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "produto_id",
    "produtor_id",
    "identificacao",
    "viagem_id",
    "status"
  ],
  "title": "CargaResponse"
}
```

### CargaUpdate

```json
{
  "properties": {
    "identificacao": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Identificacao"
    },
    "quantidade_caixas": {
      "anyOf": [
        {
          "type": "integer",
          "maximum": 2147483647.0,
          "minimum": 0.0
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade Caixas"
    },
    "quantidade": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Quantidade"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "origem_produto": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255
        },
        {
          "type": "null"
        }
      ],
      "title": "Origem Produto"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "status": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/StatusCarga"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "CargaUpdate"
}
```

### ConfiguracaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "temperatura_min_c": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        }
      ],
      "title": "Temperatura Min C"
    },
    "temperatura_max_c": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        }
      ],
      "title": "Temperatura Max C"
    },
    "umidade_min_percentual": {
      "anyOf": [
        {
          "type": "number",
          "maximum": 100.0,
          "minimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Umidade Min Percentual"
    },
    "umidade_max_percentual": {
      "anyOf": [
        {
          "type": "number",
          "maximum": 100.0,
          "minimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Umidade Max Percentual"
    },
    "intervalo_maximo_s": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Intervalo Maximo S"
    },
    "cobertura_min_percentual": {
      "anyOf": [
        {
          "type": "number",
          "maximum": 100.0,
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Cobertura Min Percentual"
    },
    "exposicao_continua_s": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Exposicao Continua S"
    },
    "maturacoes_aplicaveis": {
      "items": {
        "$ref": "#/components/schemas/EstagioMaturacao"
      },
      "type": "array",
      "maxItems": 5,
      "minItems": 1,
      "title": "Maturacoes Aplicaveis"
    },
    "ambiente": {
      "type": "string",
      "enum": [
        "TRANSPORTE_REFRIGERADO",
        "LABORATORIO"
      ],
      "title": "Ambiente"
    },
    "fundamento": {
      "type": "string",
      "enum": [
        "OPERACIONAL",
        "EXPERIMENTAL"
      ],
      "title": "Fundamento"
    },
    "justificativa": {
      "type": "string",
      "maxLength": 4000,
      "minLength": 10,
      "title": "Justificativa"
    },
    "referencias": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "maxItems": 10,
      "title": "Referencias"
    },
    "prioridade": {
      "type": "string",
      "enum": [
        "INFORMATIVO",
        "ATENCAO"
      ],
      "title": "Prioridade",
      "default": "ATENCAO"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia",
    "temperatura_min_c",
    "temperatura_max_c",
    "umidade_min_percentual",
    "umidade_max_percentual",
    "intervalo_maximo_s",
    "cobertura_min_percentual",
    "maturacoes_aplicaveis",
    "ambiente",
    "fundamento",
    "justificativa"
  ],
  "title": "ConfiguracaoCreate"
}
```

### ConfiguracaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "versao": {
      "type": "integer",
      "title": "Versao"
    },
    "registrada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Registrada Em"
    },
    "parametros": {
      "type": "object",
      "title": "Parametros"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "usuario_id",
    "chave_idempotencia",
    "versao",
    "registrada_em",
    "parametros"
  ],
  "title": "ConfiguracaoResponse"
}
```

### CurrentUserResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "nome": {
      "type": "string",
      "title": "Nome"
    },
    "email": {
      "type": "string",
      "title": "Email"
    },
    "perfil_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Perfil Id"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "perfil": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Perfil"
    },
    "empresas": {
      "items": {
        "$ref": "#/components/schemas/EmpresaResponse"
      },
      "type": "array",
      "title": "Empresas"
    }
  },
  "type": "object",
  "required": [
    "id",
    "nome",
    "email",
    "perfil_id",
    "ativo",
    "created_at",
    "updated_at",
    "perfil",
    "empresas"
  ],
  "title": "CurrentUserResponse"
}
```

### DecisaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "acao": {
      "type": "string",
      "enum": [
        "RECONHECER",
        "OBSERVAR",
        "RESOLVER",
        "DESCARTAR"
      ],
      "title": "Acao"
    },
    "justificativa": {
      "type": "string",
      "maxLength": 4000,
      "minLength": 1,
      "title": "Justificativa"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia",
    "acao",
    "justificativa"
  ],
  "title": "DecisaoCreate"
}
```

### DecisaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "alerta_id": {
      "type": "string",
      "format": "uuid",
      "title": "Alerta Id"
    },
    "ocorrencia_id": {
      "type": "string",
      "format": "uuid",
      "title": "Ocorrencia Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "acao": {
      "type": "string",
      "title": "Acao"
    },
    "justificativa": {
      "type": "string",
      "title": "Justificativa"
    },
    "estado_anterior": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Estado Anterior"
    },
    "estado_posterior": {
      "type": "string",
      "title": "Estado Posterior"
    },
    "registrada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Registrada Em"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "alerta_id",
    "ocorrencia_id",
    "usuario_id",
    "acao",
    "justificativa",
    "estado_anterior",
    "estado_posterior",
    "registrada_em"
  ],
  "title": "DecisaoResponse"
}
```

### EmpresaCreate

```json
{
  "properties": {
    "nome": {
      "type": "string",
      "maxLength": 180,
      "minLength": 1,
      "title": "Nome"
    },
    "tipo": {
      "$ref": "#/components/schemas/TipoEmpresa"
    },
    "documento": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "type": "object",
  "required": [
    "nome",
    "tipo"
  ],
  "title": "EmpresaCreate"
}
```

### EmpresaResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "nome": {
      "type": "string",
      "title": "Nome"
    },
    "tipo": {
      "$ref": "#/components/schemas/TipoEmpresa"
    },
    "documento": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    }
  },
  "type": "object",
  "required": [
    "id",
    "nome",
    "tipo",
    "documento",
    "ativo",
    "created_at",
    "updated_at"
  ],
  "title": "EmpresaResponse"
}
```

### EmpresaUpdate

```json
{
  "properties": {
    "nome": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 180,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Nome"
    },
    "tipo": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/TipoEmpresa"
        },
        {
          "type": "null"
        }
      ]
    },
    "documento": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "ativo": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ativo"
    }
  },
  "type": "object",
  "title": "EmpresaUpdate"
}
```

### EstadoSincronizacaoResponse

```json
{
  "properties": {
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "revisao_disponivel": {
      "type": "integer",
      "title": "Revisao Disponivel"
    },
    "em_execucao": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Em Execucao"
    },
    "tentativas": {
      "items": {
        "$ref": "#/components/schemas/SincronizacaoResponse"
      },
      "type": "array",
      "title": "Tentativas"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "sessao_id",
    "revisao_disponivel",
    "em_execucao",
    "tentativas"
  ],
  "title": "EstadoSincronizacaoResponse"
}
```

### EstagioMaturacao

```json
{
  "type": "string",
  "enum": [
    "VERDE_MADURA",
    "EM_AMADURECIMENTO",
    "MADURA",
    "MISTA",
    "DESCONHECIDA"
  ],
  "title": "EstagioMaturacao"
}
```

### HTTPValidationError

```json
{
  "properties": {
    "detail": {
      "items": {
        "$ref": "#/components/schemas/ValidationError"
      },
      "type": "array",
      "title": "Detail"
    }
  },
  "type": "object",
  "title": "HTTPValidationError"
}
```

### HistoricoResponse

```json
{
  "properties": {
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "estado_sessao": {
      "type": "string",
      "title": "Estado Sessao"
    },
    "revisao": {
      "type": "integer",
      "title": "Revisao"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "massa_kg": {
      "type": "string",
      "title": "Massa Kg"
    },
    "maturacao": {
      "type": "string",
      "title": "Maturacao"
    },
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "leituras": {
      "items": {
        "$ref": "#/components/schemas/LeituraHistoricoResponse"
      },
      "type": "array",
      "title": "Leituras"
    },
    "metadados_temporais_invalidos": {
      "type": "boolean",
      "title": "Metadados Temporais Invalidos"
    },
    "cancelada_para_analise": {
      "type": "boolean",
      "title": "Cancelada Para Analise"
    },
    "ocorrencias": {
      "items": {
        "type": "object"
      },
      "type": "array",
      "title": "Ocorrencias"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "sessao_id",
    "estado_sessao",
    "revisao",
    "inicio",
    "fim",
    "massa_kg",
    "maturacao",
    "total",
    "limit",
    "offset",
    "leituras",
    "metadados_temporais_invalidos",
    "cancelada_para_analise",
    "ocorrencias"
  ],
  "title": "HistoricoResponse"
}
```

### IntervaloResponse

```json
{
  "properties": {
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "duracao_s": {
      "type": "string",
      "title": "Duracao S"
    },
    "temperatura_inicio_c": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Temperatura Inicio C"
    },
    "taxa_min_ul_kg_h": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Taxa Min Ul Kg H"
    },
    "taxa_max_ul_kg_h": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Taxa Max Ul Kg H"
    },
    "volume_min_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Min Ul"
    },
    "volume_max_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Max Ul"
    },
    "motivos": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Motivos"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "inicio",
    "fim",
    "duracao_s",
    "temperatura_inicio_c",
    "taxa_min_ul_kg_h",
    "taxa_max_ul_kg_h",
    "volume_min_ul",
    "volume_max_ul",
    "motivos"
  ],
  "title": "IntervaloResponse"
}
```

### IntervencaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "justificativa": {
      "type": "string",
      "maxLength": 4000,
      "minLength": 1,
      "title": "Justificativa"
    },
    "duracao_planejada_s": {
      "anyOf": [
        {
          "type": "number",
          "maximum": 86400.0,
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        }
      ],
      "title": "Duracao Planejada S",
      "description": "Duracao de demonstracao, ate 24h; sem eficacia cientifica ou encerramento automatico."
    },
    "alerta_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Alerta Id"
    },
    "avaliacao_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Avaliacao Id"
    },
    "analise_etileno_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Analise Etileno Id"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia",
    "justificativa",
    "duracao_planejada_s"
  ],
  "title": "IntervencaoCreate"
}
```

### IntervencaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "viagem_id": {
      "type": "string",
      "format": "uuid",
      "title": "Viagem Id"
    },
    "carga_id": {
      "type": "string",
      "format": "uuid",
      "title": "Carga Id"
    },
    "veiculo_id": {
      "type": "string",
      "format": "uuid",
      "title": "Veiculo Id"
    },
    "atuador_virtual_id": {
      "type": "string",
      "title": "Atuador Virtual Id"
    },
    "alerta_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Alerta Id"
    },
    "avaliacao_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Avaliacao Id"
    },
    "analise_etileno_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Analise Etileno Id"
    },
    "solicitante_id": {
      "type": "string",
      "format": "uuid",
      "title": "Solicitante Id"
    },
    "decidida_por_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Decidida Por Id"
    },
    "iniciada_por_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Iniciada Por Id"
    },
    "finalizada_por_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizada Por Id"
    },
    "modalidade": {
      "type": "string",
      "enum": [
        "SIMULADA"
      ],
      "const": "SIMULADA",
      "title": "Modalidade"
    },
    "estado": {
      "type": "string",
      "enum": [
        "SOLICITADA",
        "AUTORIZADA",
        "RECUSADA",
        "EM_EXECUCAO",
        "CONCLUIDA",
        "CANCELADA",
        "FALHA_SIMULACAO"
      ],
      "title": "Estado"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "justificativa_solicitacao": {
      "type": "string",
      "title": "Justificativa Solicitacao"
    },
    "motivo_fim": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motivo Fim"
    },
    "solicitada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Solicitada Em"
    },
    "decidida_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Decidida Em"
    },
    "iniciada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Iniciada Em"
    },
    "prazo_planejado_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Prazo Planejado Em"
    },
    "finalizada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizada Em"
    },
    "duracao_planejada_s": {
      "type": "string",
      "title": "Duracao Planejada S"
    },
    "duracao_registrada_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duracao Registrada S"
    },
    "referencias_snapshot": {
      "type": "object",
      "title": "Referencias Snapshot"
    },
    "hash_referencias": {
      "type": "string",
      "title": "Hash Referencias"
    },
    "referencias_atuais": {
      "type": "object",
      "title": "Referencias Atuais"
    },
    "hash_referencias_atuais": {
      "type": "string",
      "title": "Hash Referencias Atuais"
    },
    "virtual_ligado": {
      "type": "boolean",
      "title": "Virtual Ligado"
    },
    "atuador_virtual_ocupado": {
      "type": "boolean",
      "title": "Atuador Virtual Ocupado"
    },
    "prazo_excedido": {
      "type": "boolean",
      "title": "Prazo Excedido"
    },
    "consultado_em": {
      "type": "string",
      "format": "date-time",
      "title": "Consultado Em"
    },
    "sessao_terminal_com_execucao": {
      "type": "boolean",
      "title": "Sessao Terminal Com Execucao"
    },
    "contexto_logistico_alterado": {
      "type": "boolean",
      "title": "Contexto Logistico Alterado"
    },
    "acoes_permitidas": {
      "items": {
        "type": "string",
        "enum": [
          "AUTORIZAR",
          "RECUSAR",
          "INICIAR",
          "ENCERRAR",
          "CANCELAR",
          "REGISTRAR_FALHA"
        ]
      },
      "type": "array",
      "title": "Acoes Permitidas"
    },
    "classificacao_risco_etileno": {
      "type": "string",
      "enum": [
        "NAO_AVALIADO"
      ],
      "const": "NAO_AVALIADO",
      "title": "Classificacao Risco Etileno",
      "default": "NAO_AVALIADO"
    },
    "resultado_operacional": {
      "type": "string",
      "title": "Resultado Operacional"
    },
    "limitacoes": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Limitacoes"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "viagem_id",
    "carga_id",
    "veiculo_id",
    "atuador_virtual_id",
    "alerta_id",
    "avaliacao_id",
    "analise_etileno_id",
    "solicitante_id",
    "decidida_por_id",
    "iniciada_por_id",
    "finalizada_por_id",
    "modalidade",
    "estado",
    "chave_idempotencia",
    "justificativa_solicitacao",
    "motivo_fim",
    "solicitada_em",
    "decidida_em",
    "iniciada_em",
    "prazo_planejado_em",
    "finalizada_em",
    "duracao_planejada_s",
    "duracao_registrada_s",
    "referencias_snapshot",
    "hash_referencias",
    "referencias_atuais",
    "hash_referencias_atuais",
    "virtual_ligado",
    "atuador_virtual_ocupado",
    "prazo_excedido",
    "consultado_em",
    "sessao_terminal_com_execucao",
    "contexto_logistico_alterado",
    "acoes_permitidas",
    "resultado_operacional",
    "limitacoes"
  ],
  "title": "IntervencaoResponse"
}
```

### LeituraHistoricoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "fonte_id": {
      "type": "string",
      "format": "uuid",
      "title": "Fonte Id"
    },
    "medicao_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Medicao Id"
    },
    "sensor_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sensor Id"
    },
    "tipo": {
      "type": "string",
      "title": "Tipo"
    },
    "channel_id": {
      "type": "string",
      "title": "Channel Id"
    },
    "field_name": {
      "type": "string",
      "title": "Field Name"
    },
    "unidade": {
      "type": "string",
      "title": "Unidade"
    },
    "entry_id": {
      "type": "integer",
      "title": "Entry Id"
    },
    "medida_em": {
      "type": "string",
      "format": "date-time",
      "title": "Medida Em"
    },
    "timestamp_origem": {
      "type": "string",
      "title": "Timestamp Origem"
    },
    "recebida_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Recebida Em"
    },
    "processada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Processada Em"
    },
    "valor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor"
    },
    "estado": {
      "type": "string",
      "title": "Estado"
    },
    "motivo": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motivo"
    },
    "revisao_incorporacao": {
      "type": "integer",
      "title": "Revisao Incorporacao"
    },
    "tardia": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Tardia"
    },
    "apos_encerramento": {
      "type": "boolean",
      "title": "Apos Encerramento"
    },
    "fora_de_ordem": {
      "type": "boolean",
      "title": "Fora De Ordem"
    },
    "conflito_observado": {
      "type": "boolean",
      "title": "Conflito Observado"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "fonte_id",
    "medicao_id",
    "sensor_id",
    "tipo",
    "channel_id",
    "field_name",
    "unidade",
    "entry_id",
    "medida_em",
    "timestamp_origem",
    "recebida_em",
    "processada_em",
    "valor",
    "estado",
    "motivo",
    "revisao_incorporacao",
    "tardia",
    "apos_encerramento",
    "fora_de_ordem",
    "conflito_observado"
  ],
  "title": "LeituraHistoricoResponse"
}
```

### ListaAcoes

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "acoes": {
      "items": {
        "$ref": "#/components/schemas/AcaoResponse"
      },
      "type": "array",
      "title": "Acoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "acoes"
  ],
  "title": "ListaAcoes"
}
```

### ListaAlertas

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "alertas": {
      "items": {
        "$ref": "#/components/schemas/AlertaResponse"
      },
      "type": "array",
      "title": "Alertas"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "alertas"
  ],
  "title": "ListaAlertas"
}
```

### ListaAvaliacoes

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "avaliacoes": {
      "items": {
        "$ref": "#/components/schemas/AvaliacaoResponse"
      },
      "type": "array",
      "title": "Avaliacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "avaliacoes"
  ],
  "title": "ListaAvaliacoes"
}
```

### ListaConfiguracoes

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "configuracoes": {
      "items": {
        "$ref": "#/components/schemas/ConfiguracaoResponse"
      },
      "type": "array",
      "title": "Configuracoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "configuracoes"
  ],
  "title": "ListaConfiguracoes"
}
```

### ListaDecisoes

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "decisoes": {
      "items": {
        "$ref": "#/components/schemas/DecisaoResponse"
      },
      "type": "array",
      "title": "Decisoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "decisoes"
  ],
  "title": "ListaDecisoes"
}
```

### ListaEvidencias

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "evidencias": {
      "items": {
        "type": "object"
      },
      "type": "array",
      "title": "Evidencias"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "evidencias"
  ],
  "title": "ListaEvidencias"
}
```

### ListaIntervencoes

```json
{
  "properties": {
    "total": {
      "type": "integer",
      "title": "Total"
    },
    "limit": {
      "type": "integer",
      "title": "Limit"
    },
    "offset": {
      "type": "integer",
      "title": "Offset"
    },
    "intervencoes": {
      "items": {
        "$ref": "#/components/schemas/IntervencaoResponse"
      },
      "type": "array",
      "title": "Intervencoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "total",
    "limit",
    "offset",
    "intervencoes"
  ],
  "title": "ListaIntervencoes"
}
```

### LoginRequest

```json
{
  "properties": {
    "email": {
      "type": "string",
      "format": "email",
      "title": "Email"
    },
    "senha": {
      "type": "string",
      "maxLength": 128,
      "minLength": 1,
      "format": "password",
      "title": "Senha",
      "writeOnly": true
    }
  },
  "type": "object",
  "required": [
    "email",
    "senha"
  ],
  "title": "LoginRequest"
}
```

### MaturacaoCarga

```json
{
  "type": "string",
  "enum": [
    "VERDE_MADURA",
    "EM_AMADURECIMENTO",
    "MADURA",
    "MISTA",
    "DESCONHECIDA"
  ],
  "title": "MaturacaoCarga"
}
```

### ModoCalculo

```json
{
  "type": "string",
  "enum": [
    "MODO_RESTRITO",
    "MODO_EXPLORATORIO"
  ],
  "title": "ModoCalculo"
}
```

### MotoristaCreate

```json
{
  "properties": {
    "empresa_id": {
      "type": "string",
      "format": "uuid",
      "title": "Empresa Id"
    },
    "nome": {
      "type": "string",
      "maxLength": 150,
      "minLength": 1,
      "title": "Nome"
    },
    "documento": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "telefone": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40
        },
        {
          "type": "null"
        }
      ],
      "title": "Telefone"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "empresa_id",
    "nome"
  ],
  "title": "MotoristaCreate"
}
```

### MotoristaResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "empresa_id": {
      "type": "string",
      "format": "uuid",
      "title": "Empresa Id"
    },
    "nome": {
      "type": "string",
      "maxLength": 150,
      "minLength": 1,
      "title": "Nome"
    },
    "documento": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "telefone": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40
        },
        {
          "type": "null"
        }
      ],
      "title": "Telefone"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "empresa_id",
    "nome"
  ],
  "title": "MotoristaResponse"
}
```

### MotoristaUpdate

```json
{
  "properties": {
    "nome": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 150,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Nome"
    },
    "documento": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Documento"
    },
    "telefone": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 40
        },
        {
          "type": "null"
        }
      ],
      "title": "Telefone"
    },
    "ativo": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ativo"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "MotoristaUpdate"
}
```

### NormalizedThingSpeakReading

```json
{
  "properties": {
    "source": {
      "type": "string",
      "title": "Source",
      "default": "thingspeak"
    },
    "channel_id": {
      "type": "string",
      "title": "Channel Id"
    },
    "entry_id": {
      "type": "integer",
      "title": "Entry Id"
    },
    "field_name": {
      "type": "string",
      "title": "Field Name"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "sensor_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Sensor Id"
    },
    "tipo": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Tipo"
    },
    "contexto": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Contexto"
    },
    "valor": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "viagem_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Viagem Id"
    },
    "carga_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Carga Id"
    },
    "caixa_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Caixa Id"
    },
    "valor_original": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Original"
    },
    "ignorada": {
      "type": "boolean",
      "title": "Ignorada",
      "default": false
    },
    "motivo_ignorada": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motivo Ignorada"
    }
  },
  "type": "object",
  "required": [
    "channel_id",
    "entry_id",
    "field_name",
    "created_at"
  ],
  "title": "NormalizedThingSpeakReading"
}
```

### ParametroCreate

```json
{
  "properties": {
    "nome_parametro": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Nome Parametro"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "valor_minimo": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Minimo"
    },
    "valor_maximo": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Maximo"
    },
    "observacao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacao"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "nome_parametro"
  ],
  "title": "ParametroCreate"
}
```

### ParametroResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "nome_parametro": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Nome Parametro"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "valor_minimo": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Minimo"
    },
    "valor_maximo": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Maximo"
    },
    "observacao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacao"
    },
    "produto_id": {
      "type": "string",
      "format": "uuid",
      "title": "Produto Id"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "nome_parametro",
    "produto_id"
  ],
  "title": "ParametroResponse"
}
```

### ParametroUpdate

```json
{
  "properties": {
    "nome_parametro": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Nome Parametro"
    },
    "unidade": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 30
        },
        {
          "type": "null"
        }
      ],
      "title": "Unidade"
    },
    "valor_minimo": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Minimo"
    },
    "valor_maximo": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Valor Maximo"
    },
    "observacao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacao"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "ParametroUpdate"
}
```

### PerfilResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "nome": {
      "type": "string",
      "title": "Nome"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    }
  },
  "type": "object",
  "required": [
    "id",
    "nome",
    "descricao"
  ],
  "title": "PerfilResponse"
}
```

### ProdutoCreate

```json
{
  "properties": {
    "nome": {
      "type": "string",
      "maxLength": 120,
      "minLength": 1,
      "title": "Nome"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "nome"
  ],
  "title": "ProdutoCreate"
}
```

### ProdutoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "nome": {
      "type": "string",
      "title": "Nome"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "nome",
    "descricao",
    "ativo"
  ],
  "title": "ProdutoResponse"
}
```

### ProdutoUpdate

```json
{
  "properties": {
    "nome": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Nome"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ativo"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "ProdutoUpdate"
}
```

### QualidadeResponse

```json
{
  "properties": {
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "revisao": {
      "type": "integer",
      "title": "Revisao"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "intervalo_maximo_s": {
      "type": "string",
      "title": "Intervalo Maximo S"
    },
    "natureza": {
      "type": "string",
      "title": "Natureza"
    },
    "metadados_temporais_invalidos": {
      "type": "boolean",
      "title": "Metadados Temporais Invalidos"
    },
    "cancelada_para_analise": {
      "type": "boolean",
      "title": "Cancelada Para Analise"
    },
    "indicadores": {
      "items": {
        "type": "object"
      },
      "type": "array",
      "title": "Indicadores"
    },
    "codigos_ocorrencias": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Codigos Ocorrencias"
    },
    "limites": {
      "type": "string",
      "title": "Limites"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "sessao_id",
    "revisao",
    "inicio",
    "fim",
    "intervalo_maximo_s",
    "natureza",
    "metadados_temporais_invalidos",
    "cancelada_para_analise",
    "indicadores",
    "codigos_ocorrencias",
    "limites"
  ],
  "title": "QualidadeResponse"
}
```

### ResultadoResponse

```json
{
  "properties": {
    "status_calculo": {
      "$ref": "#/components/schemas/StatusCalculo"
    },
    "volume_coberto_min_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Coberto Min Ul"
    },
    "volume_coberto_max_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Coberto Max Ul"
    },
    "volume_janela_min_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Janela Min Ul"
    },
    "volume_janela_max_ul": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Volume Janela Max Ul"
    },
    "duracao_coberta_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duracao Coberta S"
    },
    "duracao_nao_coberta_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duracao Nao Coberta S"
    },
    "percentual_cobertura": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Percentual Cobertura"
    },
    "unidade_volume": {
      "type": "string",
      "title": "Unidade Volume"
    },
    "motivos": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Motivos"
    },
    "limitacoes": {
      "items": {
        "type": "string"
      },
      "type": "array",
      "title": "Limitacoes"
    },
    "classificacao_risco_etileno": {
      "type": "string",
      "enum": [
        "NAO_AVALIADO"
      ],
      "const": "NAO_AVALIADO",
      "title": "Classificacao Risco Etileno"
    },
    "motivo_risco": {
      "type": "string",
      "enum": [
        "SEM_LIMIAR_VALIDADO"
      ],
      "const": "SEM_LIMIAR_VALIDADO",
      "title": "Motivo Risco"
    },
    "versao_modelo": {
      "type": "string",
      "title": "Versao Modelo"
    },
    "intervalos": {
      "items": {
        "$ref": "#/components/schemas/IntervaloResponse"
      },
      "type": "array",
      "title": "Intervalos"
    },
    "massa_kg": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Massa Kg"
    },
    "inicio": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "modo": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/ModoCalculo"
        },
        {
          "type": "null"
        }
      ]
    },
    "maturacao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Maturacao"
    },
    "intervalo_maximo_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Intervalo Maximo S"
    },
    "corte_aquisicao": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Corte Aquisicao"
    },
    "sensor_id": {
      "type": "string",
      "title": "Sensor Id"
    },
    "sessao_id": {
      "type": "string",
      "title": "Sessao Id"
    },
    "tabela_referencia": {
      "items": {
        "type": "object"
      },
      "type": "array",
      "title": "Tabela Referencia"
    },
    "cobertura": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Cobertura"
    },
    "duracao_janela_s": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Duracao Janela S"
    },
    "duplicatas_descartadas": {
      "type": "integer",
      "title": "Duplicatas Descartadas"
    },
    "interpolacao_utilizada": {
      "type": "boolean",
      "title": "Interpolacao Utilizada"
    },
    "perfil": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Perfil"
    },
    "metodologia": {
      "type": "string",
      "title": "Metodologia"
    },
    "fonte": {
      "type": "string",
      "title": "Fonte"
    },
    "referencia": {
      "type": "string",
      "title": "Referencia"
    },
    "data_consulta": {
      "type": "string",
      "title": "Data Consulta"
    },
    "aplicabilidade": {
      "type": "string",
      "title": "Aplicabilidade"
    }
  },
  "additionalProperties": true,
  "type": "object",
  "required": [
    "status_calculo",
    "volume_coberto_min_ul",
    "volume_coberto_max_ul",
    "volume_janela_min_ul",
    "volume_janela_max_ul",
    "duracao_coberta_s",
    "duracao_nao_coberta_s",
    "percentual_cobertura",
    "unidade_volume",
    "motivos",
    "limitacoes",
    "classificacao_risco_etileno",
    "motivo_risco",
    "versao_modelo",
    "intervalos",
    "massa_kg",
    "inicio",
    "fim",
    "modo",
    "maturacao",
    "intervalo_maximo_s",
    "corte_aquisicao",
    "sensor_id",
    "sessao_id",
    "tabela_referencia",
    "cobertura",
    "duracao_janela_s",
    "duplicatas_descartadas",
    "interpolacao_utilizada",
    "perfil",
    "metodologia",
    "fonte",
    "referencia",
    "data_consulta",
    "aplicabilidade"
  ],
  "title": "ResultadoResponse"
}
```

### SessaoCreate

```json
{
  "properties": {
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "sensor_temperatura_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sensor Temperatura Id"
    },
    "sensor_umidade_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Sensor Umidade Id"
    },
    "ambiente_aquisicao": {
      "type": "string",
      "enum": [
        "LABORATORIO",
        "TRANSPORTE_REFRIGERADO"
      ],
      "title": "Ambiente Aquisicao"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 2000
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "inicio",
    "sensor_temperatura_id",
    "ambiente_aquisicao",
    "chave_idempotencia"
  ],
  "title": "SessaoCreate"
}
```

### SessaoFinalizar

```json
{
  "properties": {
    "fim": {
      "type": "string",
      "format": "date-time",
      "title": "Fim"
    },
    "motivo": {
      "type": "string",
      "maxLength": 2000,
      "minLength": 1,
      "title": "Motivo"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "fim",
    "motivo"
  ],
  "title": "SessaoFinalizar"
}
```

### SessaoResponse-Input

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "carga_id": {
      "type": "string",
      "format": "uuid",
      "title": "Carga Id"
    },
    "viagem_id": {
      "type": "string",
      "format": "uuid",
      "title": "Viagem Id"
    },
    "configuracao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Configuracao Id"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "estado": {
      "$ref": "#/components/schemas/StatusSessao"
    },
    "sensor_temperatura_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sensor Temperatura Id"
    },
    "sensor_umidade_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Sensor Umidade Id"
    },
    "ambiente_aquisicao": {
      "type": "string",
      "title": "Ambiente Aquisicao"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "configuracao_versao": {
      "type": "integer",
      "title": "Configuracao Versao"
    },
    "produto_identificado": {
      "type": "string",
      "title": "Produto Identificado"
    },
    "massa_kg": {
      "anyOf": [
        {
          "type": "number"
        },
        {
          "type": "string"
        }
      ],
      "title": "Massa Kg"
    },
    "maturacao": {
      "$ref": "#/components/schemas/MaturacaoCarga"
    },
    "lote_codigo": {
      "type": "string",
      "title": "Lote Codigo"
    },
    "lote_hipotetico": {
      "type": "boolean",
      "title": "Lote Hipotetico"
    },
    "rastreabilidade": {
      "type": "string",
      "title": "Rastreabilidade"
    },
    "origem_sensor": {
      "type": "object",
      "title": "Origem Sensor"
    },
    "criada_por_id": {
      "type": "string",
      "format": "uuid",
      "title": "Criada Por Id"
    },
    "finalizada_por_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizada Por Id"
    },
    "motivo_fim": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motivo Fim"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "carga_id",
    "viagem_id",
    "configuracao_id",
    "inicio",
    "fim",
    "estado",
    "sensor_temperatura_id",
    "sensor_umidade_id",
    "ambiente_aquisicao",
    "observacoes",
    "configuracao_versao",
    "produto_identificado",
    "massa_kg",
    "maturacao",
    "lote_codigo",
    "lote_hipotetico",
    "rastreabilidade",
    "origem_sensor",
    "criada_por_id",
    "finalizada_por_id",
    "motivo_fim",
    "chave_idempotencia"
  ],
  "title": "SessaoResponse"
}
```

### SessaoResponse-Output

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "carga_id": {
      "type": "string",
      "format": "uuid",
      "title": "Carga Id"
    },
    "viagem_id": {
      "type": "string",
      "format": "uuid",
      "title": "Viagem Id"
    },
    "configuracao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Configuracao Id"
    },
    "inicio": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "estado": {
      "$ref": "#/components/schemas/StatusSessao"
    },
    "sensor_temperatura_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sensor Temperatura Id"
    },
    "sensor_umidade_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Sensor Umidade Id"
    },
    "ambiente_aquisicao": {
      "type": "string",
      "title": "Ambiente Aquisicao"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    },
    "configuracao_versao": {
      "type": "integer",
      "title": "Configuracao Versao"
    },
    "produto_identificado": {
      "type": "string",
      "title": "Produto Identificado"
    },
    "massa_kg": {
      "type": "string",
      "title": "Massa Kg"
    },
    "maturacao": {
      "$ref": "#/components/schemas/MaturacaoCarga"
    },
    "lote_codigo": {
      "type": "string",
      "title": "Lote Codigo"
    },
    "lote_hipotetico": {
      "type": "boolean",
      "title": "Lote Hipotetico"
    },
    "rastreabilidade": {
      "type": "string",
      "title": "Rastreabilidade"
    },
    "origem_sensor": {
      "type": "object",
      "title": "Origem Sensor"
    },
    "criada_por_id": {
      "type": "string",
      "format": "uuid",
      "title": "Criada Por Id"
    },
    "finalizada_por_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizada Por Id"
    },
    "motivo_fim": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motivo Fim"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "carga_id",
    "viagem_id",
    "configuracao_id",
    "inicio",
    "fim",
    "estado",
    "sensor_temperatura_id",
    "sensor_umidade_id",
    "ambiente_aquisicao",
    "observacoes",
    "configuracao_versao",
    "produto_identificado",
    "massa_kg",
    "maturacao",
    "lote_codigo",
    "lote_hipotetico",
    "rastreabilidade",
    "origem_sensor",
    "criada_por_id",
    "finalizada_por_id",
    "motivo_fim",
    "chave_idempotencia"
  ],
  "title": "SessaoResponse"
}
```

### SincronizacaoCreate

```json
{
  "properties": {
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "origem_dados": {
      "type": "string",
      "enum": [
        "THINGSPEAK",
        "BANCO"
      ],
      "title": "Origem Dados",
      "default": "THINGSPEAK"
    },
    "inicio": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio"
    },
    "fim": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Fim"
    },
    "complementar_encerrada": {
      "type": "boolean",
      "title": "Complementar Encerrada",
      "default": false
    },
    "justificativa": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 2000,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Justificativa"
    },
    "limite_atraso_s": {
      "anyOf": [
        {
          "type": "number",
          "exclusiveMinimum": 0.0
        },
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Limite Atraso S"
    },
    "max_requisicoes": {
      "type": "integer",
      "maximum": 32.0,
      "minimum": 1.0,
      "title": "Max Requisicoes",
      "default": 16
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "chave_idempotencia"
  ],
  "title": "SincronizacaoCreate"
}
```

### SincronizacaoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "sessao_id": {
      "type": "string",
      "format": "uuid",
      "title": "Sessao Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "revisao": {
      "type": "integer",
      "title": "Revisao"
    },
    "chave_idempotencia": {
      "type": "string",
      "format": "uuid",
      "title": "Chave Idempotencia"
    },
    "origem_dados": {
      "type": "string",
      "title": "Origem Dados"
    },
    "estado": {
      "type": "string",
      "title": "Estado"
    },
    "inicio_janela": {
      "type": "string",
      "format": "date-time",
      "title": "Inicio Janela"
    },
    "fim_janela": {
      "type": "string",
      "format": "date-time",
      "title": "Fim Janela"
    },
    "iniciada_em": {
      "type": "string",
      "format": "date-time",
      "title": "Iniciada Em"
    },
    "finalizada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Finalizada Em"
    },
    "expira_em": {
      "type": "string",
      "format": "date-time",
      "title": "Expira Em"
    },
    "complementacao": {
      "type": "boolean",
      "title": "Complementacao"
    },
    "justificativa": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Justificativa"
    },
    "resumo": {
      "type": "object",
      "title": "Resumo"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "sessao_id",
    "usuario_id",
    "revisao",
    "chave_idempotencia",
    "origem_dados",
    "estado",
    "inicio_janela",
    "fim_janela",
    "iniciada_em",
    "finalizada_em",
    "expira_em",
    "complementacao",
    "justificativa",
    "resumo"
  ],
  "title": "SincronizacaoResponse"
}
```

### StatusCaixa

```json
{
  "type": "string",
  "enum": [
    "REGISTRADA",
    "EM_TRANSITO",
    "ENTREGUE",
    "AVARIADA"
  ],
  "title": "StatusCaixa"
}
```

### StatusCalculo

```json
{
  "type": "string",
  "enum": [
    "ENTRADA_INVALIDA",
    "CONFIGURACAO_INCOMPLETA",
    "SEM_ESTIMATIVA",
    "PARCIAL",
    "COMPLETO_NO_MODELO"
  ],
  "title": "StatusCalculo"
}
```

### StatusCarga

```json
{
  "type": "string",
  "enum": [
    "PLANEJADA",
    "EM_TRANSITO",
    "ENTREGUE",
    "CANCELADA"
  ],
  "title": "StatusCarga"
}
```

### StatusSessao

```json
{
  "type": "string",
  "enum": [
    "ATIVA",
    "ENCERRADA",
    "CANCELADA"
  ],
  "title": "StatusSessao"
}
```

### StatusViagem

```json
{
  "type": "string",
  "enum": [
    "PLANEJADA",
    "EM_ANDAMENTO",
    "CONCLUIDA",
    "CANCELADA"
  ],
  "title": "StatusViagem"
}
```

### ThingSpeakFeed

```json
{
  "properties": {
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "entry_id": {
      "type": "integer",
      "title": "Entry Id"
    },
    "fields": {
      "additionalProperties": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ]
      },
      "type": "object",
      "title": "Fields"
    },
    "raw": {
      "type": "object",
      "title": "Raw"
    }
  },
  "type": "object",
  "required": [
    "created_at",
    "entry_id"
  ],
  "title": "ThingSpeakFeed"
}
```

### ThingSpeakMappingResult

```json
{
  "properties": {
    "channel_id": {
      "type": "string",
      "title": "Channel Id"
    },
    "feeds_processados": {
      "type": "integer",
      "title": "Feeds Processados"
    },
    "leituras_normalizadas": {
      "items": {
        "$ref": "#/components/schemas/NormalizedThingSpeakReading"
      },
      "type": "array",
      "title": "Leituras Normalizadas"
    },
    "ignorados": {
      "type": "integer",
      "title": "Ignorados",
      "default": 0
    }
  },
  "type": "object",
  "required": [
    "channel_id",
    "feeds_processados"
  ],
  "title": "ThingSpeakMappingResult"
}
```

### ThingSpeakStatusResponse

```json
{
  "properties": {
    "configured": {
      "type": "boolean",
      "title": "Configured"
    },
    "base_url": {
      "type": "string",
      "title": "Base Url"
    },
    "channel_id": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Channel Id"
    },
    "message": {
      "type": "string",
      "title": "Message"
    }
  },
  "type": "object",
  "required": [
    "configured",
    "base_url",
    "message"
  ],
  "title": "ThingSpeakStatusResponse"
}
```

### ThingSpeakSyncError

```json
{
  "properties": {
    "entry_id": {
      "type": "integer",
      "title": "Entry Id"
    },
    "field_name": {
      "type": "string",
      "title": "Field Name"
    },
    "motivo": {
      "type": "string",
      "title": "Motivo"
    }
  },
  "type": "object",
  "required": [
    "entry_id",
    "field_name",
    "motivo"
  ],
  "title": "ThingSpeakSyncError"
}
```

### ThingSpeakSyncSummary

```json
{
  "properties": {
    "feeds_recebidos": {
      "type": "integer",
      "title": "Feeds Recebidos"
    },
    "fields_processados": {
      "type": "integer",
      "title": "Fields Processados"
    },
    "medicoes_criadas": {
      "type": "integer",
      "title": "Medicoes Criadas"
    },
    "duplicados": {
      "type": "integer",
      "title": "Duplicados"
    },
    "ignorados": {
      "type": "integer",
      "title": "Ignorados"
    },
    "erros": {
      "items": {
        "$ref": "#/components/schemas/ThingSpeakSyncError"
      },
      "type": "array",
      "title": "Erros"
    }
  },
  "type": "object",
  "required": [
    "feeds_recebidos",
    "fields_processados",
    "medicoes_criadas",
    "duplicados",
    "ignorados"
  ],
  "title": "ThingSpeakSyncSummary"
}
```

### TipoEmpresa

```json
{
  "type": "string",
  "enum": [
    "PRODUTOR",
    "TRANSPORTADORA",
    "CLIENTE"
  ],
  "title": "TipoEmpresa"
}
```

### TokenResponse

```json
{
  "properties": {
    "access_token": {
      "type": "string",
      "title": "Access Token"
    },
    "token_type": {
      "type": "string",
      "title": "Token Type",
      "default": "bearer"
    },
    "expires_in": {
      "type": "integer",
      "title": "Expires In"
    }
  },
  "type": "object",
  "required": [
    "access_token",
    "expires_in"
  ],
  "title": "TokenResponse"
}
```

### UsuarioCreate

```json
{
  "properties": {
    "nome": {
      "type": "string",
      "maxLength": 150,
      "minLength": 1,
      "title": "Nome"
    },
    "email": {
      "type": "string",
      "maxLength": 255,
      "format": "email",
      "title": "Email"
    },
    "senha": {
      "type": "string",
      "maxLength": 128,
      "minLength": 12,
      "format": "password",
      "title": "Senha",
      "writeOnly": true
    },
    "perfil_id": {
      "type": "string",
      "format": "uuid",
      "title": "Perfil Id"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "type": "object",
  "required": [
    "nome",
    "email",
    "senha",
    "perfil_id"
  ],
  "title": "UsuarioCreate"
}
```

### UsuarioResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "nome": {
      "type": "string",
      "title": "Nome"
    },
    "email": {
      "type": "string",
      "title": "Email"
    },
    "perfil_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Perfil Id"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    }
  },
  "type": "object",
  "required": [
    "id",
    "nome",
    "email",
    "perfil_id",
    "ativo",
    "created_at",
    "updated_at"
  ],
  "title": "UsuarioResponse"
}
```

### UsuarioUpdate

```json
{
  "properties": {
    "nome": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 150,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Nome"
    },
    "email": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255,
          "format": "email"
        },
        {
          "type": "null"
        }
      ],
      "title": "Email"
    },
    "senha": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 128,
          "minLength": 12,
          "format": "password",
          "writeOnly": true
        },
        {
          "type": "null"
        }
      ],
      "title": "Senha"
    },
    "perfil_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Perfil Id"
    },
    "ativo": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ativo"
    }
  },
  "type": "object",
  "title": "UsuarioUpdate"
}
```

### ValidationError

```json
{
  "properties": {
    "loc": {
      "items": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "integer"
          }
        ]
      },
      "type": "array",
      "title": "Location"
    },
    "msg": {
      "type": "string",
      "title": "Message"
    },
    "type": {
      "type": "string",
      "title": "Error Type"
    }
  },
  "type": "object",
  "required": [
    "loc",
    "msg",
    "type"
  ],
  "title": "ValidationError"
}
```

### VeiculoCreate

```json
{
  "properties": {
    "empresa_id": {
      "type": "string",
      "format": "uuid",
      "title": "Empresa Id"
    },
    "identificador": {
      "type": "string",
      "maxLength": 80,
      "minLength": 1,
      "title": "Identificador"
    },
    "placa": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 20,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Placa"
    },
    "modelo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Modelo"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "empresa_id",
    "identificador"
  ],
  "title": "VeiculoCreate"
}
```

### VeiculoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "empresa_id": {
      "type": "string",
      "format": "uuid",
      "title": "Empresa Id"
    },
    "identificador": {
      "type": "string",
      "maxLength": 80,
      "minLength": 1,
      "title": "Identificador"
    },
    "placa": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 20,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Placa"
    },
    "modelo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Modelo"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo",
      "default": true
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "empresa_id",
    "identificador"
  ],
  "title": "VeiculoResponse"
}
```

### VeiculoUpdate

```json
{
  "properties": {
    "identificador": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 80,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Identificador"
    },
    "placa": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 20,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Placa"
    },
    "modelo": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 120
        },
        {
          "type": "null"
        }
      ],
      "title": "Modelo"
    },
    "descricao": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Descricao"
    },
    "ativo": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ],
      "title": "Ativo"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "VeiculoUpdate"
}
```

### ViagemCreate

```json
{
  "properties": {
    "transportadora_id": {
      "type": "string",
      "format": "uuid",
      "title": "Transportadora Id"
    },
    "veiculo_id": {
      "type": "string",
      "format": "uuid",
      "title": "Veiculo Id"
    },
    "motorista_id": {
      "type": "string",
      "format": "uuid",
      "title": "Motorista Id"
    },
    "origem": {
      "type": "string",
      "maxLength": 255,
      "minLength": 1,
      "title": "Origem"
    },
    "destino": {
      "type": "string",
      "maxLength": 255,
      "minLength": 1,
      "title": "Destino"
    },
    "saida_em": {
      "type": "string",
      "format": "date-time",
      "title": "Saida Em"
    },
    "previsao_chegada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Previsao Chegada Em"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "required": [
    "transportadora_id",
    "veiculo_id",
    "motorista_id",
    "origem",
    "destino",
    "saida_em"
  ],
  "title": "ViagemCreate"
}
```

### ViagemResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "title": "Created At"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "title": "Updated At"
    },
    "transportadora_id": {
      "type": "string",
      "format": "uuid",
      "title": "Transportadora Id"
    },
    "veiculo_id": {
      "type": "string",
      "format": "uuid",
      "title": "Veiculo Id"
    },
    "motorista_id": {
      "type": "string",
      "format": "uuid",
      "title": "Motorista Id"
    },
    "origem": {
      "type": "string",
      "title": "Origem"
    },
    "destino": {
      "type": "string",
      "title": "Destino"
    },
    "saida_em": {
      "type": "string",
      "format": "date-time",
      "title": "Saida Em"
    },
    "previsao_chegada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Previsao Chegada Em"
    },
    "inicio_real": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio Real"
    },
    "chegada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Chegada Em"
    },
    "status": {
      "$ref": "#/components/schemas/StatusViagem"
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "type": "object",
  "required": [
    "id",
    "created_at",
    "updated_at",
    "transportadora_id",
    "veiculo_id",
    "motorista_id",
    "origem",
    "destino",
    "saida_em",
    "previsao_chegada_em",
    "inicio_real",
    "chegada_em",
    "status",
    "observacoes"
  ],
  "title": "ViagemResponse"
}
```

### ViagemUpdate

```json
{
  "properties": {
    "veiculo_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Veiculo Id"
    },
    "motorista_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ],
      "title": "Motorista Id"
    },
    "origem": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Origem"
    },
    "destino": {
      "anyOf": [
        {
          "type": "string",
          "maxLength": 255,
          "minLength": 1
        },
        {
          "type": "null"
        }
      ],
      "title": "Destino"
    },
    "saida_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Saida Em"
    },
    "previsao_chegada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Previsao Chegada Em"
    },
    "inicio_real": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Inicio Real"
    },
    "chegada_em": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ],
      "title": "Chegada Em"
    },
    "status": {
      "anyOf": [
        {
          "$ref": "#/components/schemas/StatusViagem"
        },
        {
          "type": "null"
        }
      ]
    },
    "observacoes": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "title": "Observacoes"
    }
  },
  "additionalProperties": false,
  "type": "object",
  "title": "ViagemUpdate"
}
```

### VinculoResponse

```json
{
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid",
      "title": "Id"
    },
    "empresa_id": {
      "type": "string",
      "format": "uuid",
      "title": "Empresa Id"
    },
    "usuario_id": {
      "type": "string",
      "format": "uuid",
      "title": "Usuario Id"
    },
    "ativo": {
      "type": "boolean",
      "title": "Ativo"
    }
  },
  "type": "object",
  "required": [
    "id",
    "empresa_id",
    "usuario_id",
    "ativo"
  ],
  "title": "VinculoResponse"
}
```

## Rotas registradas fora do OpenAPI

| Métodos | Caminho | Função | Origem |
| --- | --- | --- | --- |
| GET,HEAD | /openapi.json | FastAPI.setup.<locals>.openapi | .venv/Lib/site-packages/fastapi/applications.py |
| GET,HEAD | /docs | FastAPI.setup.<locals>.swagger_ui_html | .venv/Lib/site-packages/fastapi/applications.py |
| GET,HEAD | /docs/oauth2-redirect | FastAPI.setup.<locals>.swagger_ui_redirect | .venv/Lib/site-packages/fastapi/applications.py |
| GET,HEAD | /redoc | FastAPI.setup.<locals>.redoc_html | .venv/Lib/site-packages/fastapi/applications.py |
