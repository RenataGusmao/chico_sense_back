# Guia de testes e fluxos no Swagger

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## GUIA DE TESTES E FLUXOS NO SWAGGER

Este roteiro requer banco **local descartável** com migrations e seed mínimo. Não aponta para ambiente publicado. `/docs`, `/redoc`, `/openapi.json` e `/docs/oauth2-redirect` estão habilitados, públicos e fora das 76 operações. `/health` verifica processo/configuração, não faz SELECT e não é readiness do banco. Não há endpoint dedicado de readiness.

Em `/docs`, execute login (JSON, não OAuth2 password form). Copie `access_token`, clique Authorize em HTTPBearer e cole somente o token; o Swagger produz o header Bearer. Não publique capturas com token/senha. `/auth/me` informa perfil e empresas. Sem login/escopo válido, não prossiga.

IDs simbólicos deste guia representam campos copiados das respostas, não registros preexistentes. Para UUIDs nos exemplos reais de fixture do catálogo, substitua por seus próprios IDs. Nunca envie `{sessao_id}` literal em campo UUID. A data hipotética dos exemplos deve ser adaptada coerentemente ao início real, à janela de aquisição e ao corte não futuro.

### Pré-requisito que o Swagger não cria

Não há CRUD HTTP de sensores/dispositivos ou endpoint para configurar o mapping ThingSpeak. Infra/backend deve provisionar Sensor e Dispositivo com contexto/logística compatíveis e configurar `THINGSPEAK_FIELD_MAPPING_JSON` no servidor isolado. `setup_prototipo.py` cria contexto PROTOTIPO, que **não comprova transporte refrigerado** e é rejeitado nesse ambiente da sessão. Não o use como atalho para uma sessão TRANSPORTE_REFRIGERADO. Sem esse pré-requisito, pare na criação de sessão e registre o bloqueio. Alternativa totalmente automatizada: executar o teste integrado que monta sensores e mocka ThingSpeak.

### Sequência operacional

Para cada operação a seguir, request/response completos, parâmetros e status estão no catálogo. As tabelas explicitam os dados que devem ser copiados e a persistência a confirmar. Perfis são sempre subordinados ao vínculo empresarial.

### 01 — Verificar API

| Item | Procedimento |
| --- | --- |
| Endpoint | GET /health |
| Perfil | Público |
| Pré-requisitos | API local iniciada |
| Dados / request | Sem body |
| Resposta | status=ok; service=chicosense-api |
| Copiar | Nenhum |
| Banco | Nenhuma escrita; não prova disponibilidade do DB |
| Erros | Falha de rede/500; confirmar processo e URL |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-002](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-002` no documento.

### 02 — Autenticar

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/auth/login |
| Perfil | Usuário ativo |
| Pré-requisitos | ADMIN inicial provisionado localmente |
| Dados / request | email e senha da conta de teste |
| Resposta | 200 TokenResponse |
| Copiar | access_token; expires_in |
| Banco | Usuário/hash lidos; nenhum login persistido |
| Erros | 401 inválido/inativo; 422 formato; 503 chave não configurada |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-007](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-007` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "email": "ADMIN@EXAMPLE.COM",
  "senha": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA"
}
```

### 03 — Conferir identidade

| Item | Procedimento |
| --- | --- |
| Endpoint | GET /api/v1/auth/me |
| Perfil | Autenticado |
| Pré-requisitos | Authorize aplicado |
| Dados / request | Sem body |
| Resposta | 200 CurrentUserResponse |
| Copiar | id; perfil; empresas[].id |
| Banco | Consulta usuário/vínculos |
| Erros | 401 token ausente/expirado |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-008](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-008` no documento.

### 04 — Criar/consultar empresas

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/empresas |
| Perfil | ADMIN |
| Pré-requisitos | ADMIN autenticado |
| Dados / request | EmpresaCreate; tipo TRANSPORTADORA; repetir PRODUTOR e CLIENTE se necessário |
| Resposta | 201 EmpresaResponse |
| Copiar | id → transportadora_id/produtor_id/cliente_id |
| Banco | empresas |
| Erros | 422 tipo/dados; 409 documento; não ADMIN 403 |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-014](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-014` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "nome": "Empresa teste",
  "tipo": "PRODUTOR"
}
```

### 05 — Criar usuários/vínculos

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/usuarios |
| Perfil | ADMIN |
| Pré-requisitos | GET /perfis retorna perfil_id |
| Dados / request | UsuarioCreate; depois POST /empresas/{empresa_id}/usuarios/{usuario_id} sem body |
| Resposta | 201 usuário; 200 vínculo |
| Copiar | usuario_id; perfil_id |
| Banco | usuarios; empresas_usuarios |
| Erros | 409 email normalizado duplicado; 404 referência |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-010](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-010` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "nome": "Gestor",
  "email": " GESTOR@EXAMPLE.COM ",
  "senha": "VALOR_FICTICIO_REMOVIDO_PELA_AUDITORIA",
  "perfil_id": "ebc97e30-5f8f-4c66-b65d-3d88cdd39c9b"
}
```

### 06 — Criar produto

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/produtos |
| Perfil | ADMIN |
| Pré-requisitos | Catálogo disponível |
| Dados / request | ProdutoCreate; nome e campos do schema |
| Resposta | 201 ProdutoResponse |
| Copiar | id → produto_id |
| Banco | produtos |
| Erros | 403 escrita por não ADMIN; 422 entrada |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-020](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-020` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "nome": "Produto teste"
}
```

### 07 — Criar veículo

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/veiculos |
| Perfil | ADMIN/GESTOR |
| Pré-requisitos | Transportadora ativa e autorizada |
| Dados / request | empresa_id; identificador; placa opcional |
| Resposta | 201 VeiculoResponse |
| Copiar | id → veiculo_id |
| Banco | veiculos.empresa_id |
| Erros | 403 transportadora externa; 422;409 unicidade |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-027](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-027` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "identificador": "V-1"
}
```

### 08 — Criar motorista

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/motoristas |
| Perfil | ADMIN/GESTOR |
| Pré-requisitos | Mesma transportadora |
| Dados / request | empresa_id; nome; documento opcional |
| Resposta | 201 MotoristaResponse |
| Copiar | id → motorista_id |
| Banco | motoristas.empresa_id |
| Erros | 403 escopo; 422 formato |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-031](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-031` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "empresa_id": "c5201eff-c262-4c6a-a1a3-5a509ac086aa",
  "nome": "Motorista teste"
}
```

### 09 — Criar viagem

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/viagens |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Frota/motorista ativos e mesma empresa |
| Dados / request | transportadora_id; veiculo_id; motorista_id; origem; destino; saida_em com fuso |
| Resposta | 201 PLANEJADA |
| Copiar | id → viagem_id |
| Banco | viagens com FK válidas |
| Erros | 403 escopo; 404 inexistente; 422 vínculos/tempo |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-035](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-035` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

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

### 10 — Criar carga

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/viagens/{viagem_id}/cargas |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Produto/produtor ativos e viagem aberta |
| Dados / request | CargaCreate: produto_id; produtor_id; identificacao; cliente_id opcional |
| Resposta | 201 PLANEJADA |
| Copiar | id → carga_id |
| Banco | cargas.viagem_id do path |
| Erros | 422 quantidade sem unidade ou tipo de empresa; 404 referência |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-039](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-039` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "produto_id": "0ef738e6-1365-41c6-ba99-86896411a88e",
  "produtor_id": "47e0d6ea-e9b8-4f10-878b-852ecc9ca039",
  "identificacao": "ETAPA8-CARGA-HIPOTETICA",
  "observacoes": "Fixture didatica; sem dados de producao."
}
```

### 11 — Iniciar viagem

| Item | Procedimento |
| --- | --- |
| Endpoint | PATCH /api/v1/viagens/{viagem_id} |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | PLANEJADA |
| Dados / request | status=EM_ANDAMENTO; inicio_real explícito e coerente |
| Resposta | 200 EM_ANDAMENTO |
| Copiar | inicio_real |
| Banco | viagens.status/inicio_real |
| Erros | 422 transição ou estrutura inválida |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-038](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-038` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "status": "EM_ANDAMENTO",
  "inicio_real": "2026-11-23T10:54:05.435676+00:00"
}
```

### 12 — Colocar carga em trânsito

| Item | Procedimento |
| --- | --- |
| Endpoint | PATCH /api/v1/cargas/{carga_id} |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Viagem EM_ANDAMENTO |
| Dados / request | status=EM_TRANSITO |
| Resposta | 200 EM_TRANSITO |
| Copiar | carga_id mantido |
| Banco | cargas.status |
| Erros | 422 viagem ainda planejada |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-042](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-042` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "status": "EM_TRANSITO"
}
```

### 13 — Declarar monitoramento

| Item | Procedimento |
| --- | --- |
| Endpoint | PUT /api/v1/cargas/{carga_id}/monitoramento |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Sem sessão ativa; sensores provisionados separadamente |
| Dados / request | CargaMonitoramentoPut: produto_identificado=MANGA_TOMMY_ATKINS; massa_kg positiva; maturacao; lote_hipotetico |
| Resposta | 200 declaração versionada |
| Copiar | id/configuração; massa e maturacao |
| Banco | cargas_monitoramento; eventos_monitoramento |
| Erros | 422 massa; 409 carga terminal/sessão ativa |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-047](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-047` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

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

### 14 — Iniciar sessão

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/cargas/{carga_id}/monitoramentos |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Declaração e sensores compatíveis |
| Dados / request | SessaoCreate: inicio com fuso; sensor_temperatura_id; sensor_umidade_id opcional; ambiente_aquisicao; chave_idempotencia |
| Resposta | 201; replay 200 |
| Copiar | id → sessao_id; snapshot |
| Banco | sessoes_monitoramento; eventos; fonte histórica fixada ao adquirir |
| Erros | 409 sobreposição; 403 sensor sem contexto; 422 horário/unidade |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-049](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-049` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "inicio": "2026-11-23T11:04:05.435676+00:00",
  "sensor_temperatura_id": "67a0548e-5508-423d-8007-4316cd532ef7",
  "sensor_umidade_id": "62a07818-78ad-4fe8-a628-02d816c9c78e",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "chave_idempotencia": "7425b4af-7b91-47b3-bd92-4b69363c4d03"
}
```

### 15 — Diagnóstico IoT global

| Item | Procedimento |
| --- | --- |
| Endpoint | GET /api/v1/integracoes/thingspeak/status |
| Perfil | ADMIN |
| Pré-requisitos | Configuração do servidor; não fornece propriedade de canal |
| Dados / request | Sem body |
| Resposta | 200 diagnóstico privado; configured pode ser false |
| Copiar | Sem chave ou segredo |
| Banco | Sem escrita |
| Erros | 403 não ADMIN; 503 configuração insegura |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-003](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-003` no documento.

### 16 — Sincronizar sessão

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/sincronizacoes |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Sessão ATIVA; fonte/mapping válidos |
| Dados / request | SincronizacaoCreate: chave_idempotencia; origem_dados THINGSPEAK ou BANCO |
| Resposta | 200 estado; replay EM_EXECUCAO 202; examinar estado/resumo |
| Copiar | revisao; id da tentativa |
| Banco | fontes; leituras externas; medicoes; registros/incorporações/ocorrências |
| Erros | 409 mapping/chave; estado FALHA/PARCIAL não é coleta completa |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-055](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-055` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "7eb10ec0-1c21-4f83-84f7-5e918c1aed7c"
}
```

### 17 — Consultar histórico

| Item | Procedimento |
| --- | --- |
| Endpoint | GET /api/v1/monitoramentos/{sessao_id}/leituras |
| Perfil | Quatro perfis |
| Pré-requisitos | Aquisição consolidada |
| Dados / request | query revisao, inicio, fim, limit, offset; qualidade exige intervalo_maximo_s |
| Resposta | 200 envelope com leituras; vazio é válido |
| Copiar | revisao; timestamps; origem |
| Banco | Consulta sem alteração |
| Erros | 422 janela/G;403 escopo |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-057](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-057` no documento.

### 18 — Analisar etileno

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/analises-etileno |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Janela positiva, revisão consolidada; ATIVA exige corte |
| Dados / request | AnaliseCreate: chave; intervalo_maximo_s; modo; fim; corte_aquisicao; início/revisão opcionais |
| Resposta | 200 AnaliseResponse, inclusive SEM_ESTIMATIVA/CONFIGURACAO_INCOMPLETA |
| Copiar | id → analise_id; hash_entrada/hash_resultado; revisão |
| Banco | analises_etileno; evento atômico |
| Erros | 422 corte futuro;409 revisão/chave;503 rollback |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-059](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-059` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "de4d4eb1-3a50-4617-99a6-729fdd32be96",
  "intervalo_maximo_s": "3600",
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "corte_aquisicao": "2026-11-23T14:54:09.896209+00:00"
}
```

### 19 — Versionar configuração

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais |
| Perfil | ADMIN/GESTOR |
| Pré-requisitos | Maturação/ambiente explícitos da sessão |
| Dados / request | ConfiguracaoCreate completa; limites didáticos devem ser justificados, não científicos |
| Resposta | 200 versão imutável |
| Copiar | id → configuracao_id; versao; registrada_em |
| Banco | configuracoes_ambientais; evento |
| Erros | 403 OPERADOR;422 min>=max;409 incompatibilidade |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-062](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-062` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

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

### 20 — Avaliar ambiente

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Configuração precisa existir no corte escolhido |
| Dados / request | AvaliacaoCreate; chave; corte atual após configuração; fim da janela medida; configuracao_id; revisão; análise contextual opcional compatível |
| Resposta | 200 AVALIADO/INCONCLUSIVO/CONFIGURACAO_INSUFICIENTE em resultado |
| Copiar | id → avaliacao_id; alertas_ids |
| Banco | avaliacoes; evidências; alertas; decisão CRIAR; eventos |
| Erros | 409 análise de janela/revisão distinta;422 corte |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-064](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-064` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "9fa4a56a-5232-4ae9-b980-70e7d2011c21",
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "corte_aquisicao": "2026-11-23T14:55:24.565950+00:00"
}
```

### 21 — Consultar alerta/evidência

| Item | Procedimento |
| --- | --- |
| Endpoint | GET /api/v1/monitoramentos/{sessao_id}/alertas |
| Perfil | Quatro perfis |
| Pré-requisitos | Avaliação pode não produzir alertas |
| Dados / request | Listar; GET /alertas/{alerta_id}; /evidencias |
| Resposta | 200 lista/envelope; vazio não significa seguro |
| Copiar | alerta_id da avaliação ou listagem |
| Banco | Sem escrita |
| Erros | 404 alerta não pertence à sessão;403 escopo |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-067](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-067` no documento.

### 22 — Decidir alerta

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Caso ABERTO para RECONHECER |
| Dados / request | DecisaoCreate: chave; acao=RECONHECER; justificativa; depois OBSERVAR/RESOLVER/DESCARTAR conforme estado |
| Resposta | 200 DecisaoResponse; histórico GET /decisoes |
| Copiar | ocorrencia_id; estado_posterior |
| Banco | decisoes_alertas; ocorrencias; status alerta |
| Erros | 409 transição/chave;422 justificativa |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-069](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-069` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "9aae6235-b0e0-4400-8409-2bd02b455893",
  "acao": "RESOLVER",
  "justificativa": "Operador verificou a evidencia ambiental."
}
```

### 23 — Solicitar simulação

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Sessão/logística ativas; alerta opcional não terminal |
| Dados / request | IntervencaoCreate: chave; justificativa; duracao_planejada_s; referências opcionais da mesma sessão |
| Resposta | 200 SOLICITADA; virtual_ligado=false |
| Copiar | id → intervencao_id |
| Banco | intervencoes_simuladas; ação inicial/ocorrência |
| Erros | 409 contexto terminal;422 campo de hardware/segredo |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-072](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-072` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "45760043-e607-4aa4-abd3-dea1c663c2db",
  "justificativa": "Demonstracao supervisionada; sem efeito fisico ou cientifico.",
  "duracao_planejada_s": "60"
}
```

### 24 — Autorizar e iniciar

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes |
| Perfil | ADMIN/GESTOR |
| Pré-requisitos | SOLICITADA; contexto ainda válido |
| Dados / request | AcaoCreate AUTORIZAR; depois outra chave INICIAR, justificativas próprias |
| Resposta | 200 AUTORIZADA; depois EM_EXECUCAO |
| Copiar | estado_posterior; id ação |
| Banco | ações/ocorrências; índice único parcial por veículo |
| Erros | 403 OPERADOR;409 sem autorização ou veículo ocupado |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-075](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-075` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "bc592a73-5e07-4d49-bd7c-21c8871543d1",
  "acao": "AUTORIZAR",
  "justificativa": "Responsavel confirmou a decisao virtual."
}
```

### 25 — Encerrar simulação

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes |
| Perfil | ADMIN/GESTOR ou solicitante OPERADOR |
| Pré-requisitos | EM_EXECUCAO; não depende de timer |
| Dados / request | AcaoCreate ENCERRAR + chave + justificativa |
| Resposta | 200 CONCLUIDA; GET intervenção: virtual_ligado=false; /acoes histórico |
| Copiar | duracao_registrada_s; finalizada_em |
| Banco | Estado terminal e ação auditada |
| Erros | 409 transição/chave;403 solicitante externo |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-075](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-075` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "chave_idempotencia": "bc592a73-5e07-4d49-bd7c-21c8871543d1",
  "acao": "AUTORIZAR",
  "justificativa": "Responsavel confirmou a decisao virtual."
}
```

### 26 — Encerrar monitoramento

| Item | Procedimento |
| --- | --- |
| Endpoint | POST /api/v1/monitoramentos/{sessao_id}/encerrar |
| Perfil | ADMIN/GESTOR/OPERADOR |
| Pré-requisitos | Encerrar execução virtual antes; horário dentro da viagem |
| Dados / request | SessaoFinalizar: fim com fuso; motivo |
| Resposta | 200 ENCERRADA; consultar sessão/análises/alertas/históricos |
| Copiar | fim; estado final |
| Banco | Sessão/evento; históricos mantidos |
| Erros | 409 transição;422 fim incoerente; cancelar é rota alternativa, não apagar |
| Como conferir | Consultar recurso por GET e comparar IDs/estado; registros/tabelas conforme dicionário do banco. Não inferir sucesso de coleta pelo HTTP 200. |


Request/response completos: [Catálogo API-053](04-CATALOGO-COMPLETO-DA-API.md). Localizar o identificador `API-053` no documento.

Exemplo local comprovado (substituir IDs/datas e chave em cada nova ação):

```json
{
  "fim": "2026-11-23T13:04:05.435676+00:00",
  "motivo": "Operacao registrada"
}
```

## Idempotência e bifurcações

Guarde chave e payload antes do envio; retry usa exatamente os mesmos valores. Não atualize corte em retry. Outra chave cria outra operação. Após 409, consulte estado e não faça loop de início. Sessão ENCERRADA permite complemento elevado com flag/justificativa; CANCELADA não aceita novos dados/análises/avaliações, mas mantém histórico e decisões permitidas. Intervenção terminal nunca reabre. Uma sessão terminal pode ainda ter execução virtual a encerrar administrativamente; a API não encerra equipamento nem agenda ações.

Para cancelar em vez de encerrar, use POST `/monitoramentos/{sessao_id}/cancelar` com SessaoFinalizar. Para recusar simulação, use `RECUSAR` quando SOLICITADA. Para falha didática, `REGISTRAR_FALHA` em EM_EXECUCAO com perfil privilegiado. Não há endpoint separado “ligar exaustor”.

## Validação do Swagger

Os quatro recursos de documentação foram requisitados com TestClient, sem banco externo. OpenAPI vivo foi comparado ao snapshot anterior. HTTPBearer declara mecanismo, mas não codifica perfis/escopo por operação. A maioria dos schemas é detalhada; campos dict/snapshots permanecem abertos. Respostas 401/403/503 legadas não estão integralmente descritas. O formato sanitizado de 422 (loc/msg/type) coincide com ValidationError do schema; não foi constatada divergência estrutural nessa resposta. Não há exemplos globais suficientes no Swagger; os exemplos executados desta auditoria complementam o guia. Nenhuma anotação de endpoint foi corrigida.

## Demonstração automatizada equivalente

`python -B -m pytest tests/test_integracao_etapa8.py::test_fluxo_integrado_ponta_a_ponta_etapa8 -v -p no:cacheprovider` exercita JWT, logística, sessão, ThingSpeak mockado, análise [700;9000] µL, avaliação, alerta e intervenção. A fixture faz seed ORM; portanto sua aprovação não prova que o Swagger sozinho consegue provisionar todos os recursos. Consulte a matriz para os testes de encerramento e fluxos alternativos.
