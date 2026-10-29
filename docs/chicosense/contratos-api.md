# ChicoSense — Contratos da API para frontend

Contratos consolidados em 29/10/2026, exportados da implementação qualificada.
Os exemplos são hipotéticos e não contêm dados de produção.
Fonte canônica: [openapi.json](openapi.json).
OpenAPI 3.1.0; info.version 0.1.0; prefixo funcional /api/v1. O número de etapa
não cria outra versão de URL. Inventário completo: 50 paths, 76 operações, 84 schemas.

## 1. Desenvolvimento, segurança e autenticação

URL-base de desenvolvimento convencional: http://127.0.0.1:8000.
Swagger: /docs; schema vivo: /openapi.json. A porta é a do comando de execução,
não uma configuração fixada pelo backend. O snapshot não anuncia servidores remotos.
CORS local permite http://localhost:5173 e http://127.0.0.1:5173.

**URL local não garante banco local. Confirme o destino de banco e prepare um
ambiente isolado antes de executar a demonstração interativa.**
O teste integrado usa overrides do banco SQLite e do ThingSpeak, sem ler/gravar
no Supabase. Uso manual da API depende de ambiente local/isolado devidamente preparado.

POST /api/v1/auth/login aceita email e senha; verifica hash e emite access_token,
token_type=bearer e expires_in em segundos. Usar Authorization: Bearer <token> nas
rotas protegidas. GET /api/v1/auth/me informa perfil e empresas autorizadas.
Não há contrato de refresh/logout no backend atual. Não presumir que exista.
Senha/token não devem constar em logs, URLs, evidências ou justificativas.

Exemplo estrutural fictício, sem cadastro ou credencial real:

```json
{"email":"operador@example.com","senha":"SENHA_FICTICIA_DO_AMBIENTE_DE_TESTE"}
```

Há 30 operações de monitoramento e 27 de produtos/logística com Bearer declarado.
As 27 rotas corrigidas rejeitam JWT ausente, inválido ou expirado; consultas e
escritas validam perfil e escopo. A antiga lacuna dos CRUDs logísticos foi corrigida.
As quatro rotas globais ThingSpeak agora são privadas e exclusivas de ADMIN.
O canal não tem propriedade empresarial persistida; acesso a um sensor não autoriza
a leitura do canal inteiro. GESTOR/OPERADOR/CONSULTA usam histórico por sessão.
Públicos no OpenAPI: GET /, GET /health e POST /api/v1/auth/login. Swagger/ReDoc e
seus metadados permanecem públicos. Não existe autenticação de máquina implementada.

## 2. Perfis, responsabilidade e diferenças conceituais

| Operação | OPERADOR | GESTOR/ADMIN | CONSULTA |
|---|---|---|---|
| Consultar monitoramento/logística no escopo empresarial | Sim | Sim | Sim |
| Consultar/sincronizar canal global ThingSpeak | Não | Somente ADMIN | Não |
| Ler catálogo global de produtos/parâmetros | Sim | Sim | Sim |
| Alterar catálogo global de produtos/parâmetros | Não | Somente ADMIN | Não |
| Criar/alterar veículos e motoristas | Não | Sim | Não |
| Criar/alterar viagens, cargas e caixas | Sim | Sim | Não |
| Configurar carga e criar/encerrar/cancelar sessão | Sim | Sim | Não |
| Sincronizar sessão ativa / analisar etileno | Sim | Sim | Não |
| Complementar aquisição de sessão encerrada | Não | Sim, com justificativa e flag explícita | Não |
| Criar configuração ambiental versionada | Não | Sim | Não |
| Avaliar ambiente e decidir sobre alertas | Sim | Sim | Não |
| Solicitar intervenção | Sim | Sim | Não |
| Autorizar, recusar ou iniciar intervenção | Não | Sim | Não |
| Encerrar intervenção | Somente a própria solicitação | Sim | Não |
| Cancelar intervenção | Própria, apenas SOLICITADA | Sim, nos estados não terminais | Não |
| Registrar falha da simulação | Não | Sim | Não |

ADMIN pode recuperar finalização com empresa inativa; os demais mantêm o bloqueio
empresarial existente. Aprovação por dois usuários distintos não é exigida:
GESTOR/ADMIN pode autorizar uma solicitação própria; OPERADOR não se autoautoriza.

- Temperatura/UR: valores medidos, sujeitos a validade, calibração e representatividade.
- Produção potencial: faixa matemática em µL, sem medir gás, concentração ou acúmulo.
- Avaliação ambiental: regra operacional configurada, separada da estimativa científica.
- Alerta: caso para acompanhamento humano, sem risco fisiológico validado.
- Exaustão virtual: estado lógico supervisionado, sem efeito físico ou eficácia científica.

Risco de etileno permanece NAO_AVALIADO. Não usar linguagem de detecção, remoção,
concentração perigosa, conservação garantida ou início da liberação do gás.
Ausência de dados não é produção zero nem condição segura.

## 3. Ordem recomendada das chamadas

1. Login e /auth/me; estabelecer empresa/perfil. A existência de token não substitui autorização.
2. Cadastrar/selecionar produto, produtor, veículo, motorista e viagem de teste.
   Catálogo global: ADMIN escreve; veículos/motoristas: GESTOR/ADMIN; operações
   de viagem/carga/caixa: OPERADOR/GESTOR/ADMIN, sempre no escopo empresarial.
3. POST /viagens/{viagem_id}/cargas; a viagem_id vem do caminho, não do body CargaCreate.
4. PATCH viagem para EM_ANDAMENTO com inicio_real e carga para EM_TRANSITO.
5. PUT /cargas/{carga_id}/monitoramento: declarar massa líquida kg, cultivar, lote e maturação.
6. Provisionar sensores/dispositivo e mapping do servidor; não há CRUD público desses sensores.
   A fixture faz essa preparação. Não colocar chave ThingSpeak no frontend.
7. POST /cargas/{carga_id}/monitoramentos: início explícito, sensores e chave idempotente.
8. POST /monitoramentos/{sessao_id}/sincronizacoes; consultar seu estado.
9. GET /leituras e /qualidade, fixando revisão e janela; G é obrigatório para qualidade.
10. POST /analises-etileno; sessão ativa exige corte_aquisicao explícito.
    Consultar/listar análise armazenada sem recálculo.
11. GESTOR/ADMIN: POST /configuracoes-ambientais com parâmetros EXPERIMENTAL/OPERACIONAL.
12. POST /avaliacoes-preventivas; análise de etileno é contexto opcional da mesma janela/revisão.
13. GET /alertas e /evidencias; OPERADOR registra RECONHECER em /decisoes após examinar o caso.
14. POST /intervencoes-simuladas com justificativa. Nenhum alerta solicita ou autoriza sozinho.
15. GESTOR/ADMIN examina contexto e envia AUTORIZAR; em outra requisição, INICIAR.
16. Acompanhar estado e ocupação; ENCERRAR explicitamente pelo responsável/gestor.
    Consultar /acoes. Não concluir por um timer do frontend.

Não encerrar a sessão antes do início pretendido da intervenção. Sessão encerrada/
cancelada bloqueia novos acionamentos, mas mantém consulta e finalização administrativa.
Essa sequência é exercitada pelo teste ponta a ponta da Etapa 8.

### Canal global ThingSpeak e compatibilidade

GET /integracoes/thingspeak/status, /feeds e /ultima-leitura e POST /sincronizar
exigem JWT ADMIN. Não há body para informar canal ou empresa e somente results é
um parâmetro funcional das consultas/sincronização que o declaram. IDs extras não
autorizam origem nem alteram a configuração do servidor. ADMIN tem abrangência global.
Não usar essas rotas como histórico empresarial; preferir /monitoramentos/{id}/leituras.

Os schemas e parâmetros permanecem iguais. Por segurança, raw da última leitura
conserva created_at, entry_id e os fields documentados; metadados opacos adicionais
são omitidos. Credenciais reconhecidas são removidas/mascaradas em cópias da resposta,
sem alterar feeds internos ou dados armazenados. Mensagens de erro upstream não
são ecoadas. URL-base com userinfo/query/fragmento e canal inválido retornam 503 sem
mostrar valores. Canal ausente mantém status privado configured=false e leituras 400.

Não há configuração administrativa via HTTP, nem um fluxo de autenticação de máquina.
Chamadas internas aos serviços não dependem de token HTTP. Consumidores externos
ainda não identificados devem ser inventariados e migrados conscientemente.

## 4. Estados e interpretação da resposta

- Sessão: ATIVA, ENCERRADA, CANCELADA.
- Aquisição: EM_EXECUCAO, CONCLUIDA, PARCIAL, FALHA, INTERROMPIDA.
- Cálculo: ENTRADA_INVALIDA, CONFIGURACAO_INCOMPLETA, SEM_ESTIMATIVA, PARCIAL, COMPLETO_NO_MODELO.
- Avaliação operacional: AVALIADO, INCONCLUSIVO, CONFIGURACAO_INSUFICIENTE.
- Alerta: ABERTO, EM_ANALISE (reconhecido), RESOLVIDO, DESCARTADO.
- Intervenção: SOLICITADA, AUTORIZADA, RECUSADA, EM_EXECUCAO, CONCLUIDA, CANCELADA, FALHA_SIMULACAO.

Análise PARCIAL: volume_coberto_min/max_ul é subtotal; volume_janela_min/max_ul
continua null. Não somar outro zero ou exibir subtotal como total. G omitido na
análise gera CONFIGURACAO_INCOMPLETA; valor G inválido é rejeitado na entrada.
MODO_RESTRITO usa apenas pontos de referência; MODO_EXPLORATORIO interpola no domínio.

Qualidade é cobertura de aquisição, não aplicabilidade do modelo. Temperatura
intermediária pode ser medida válida e não ter taxa no modo restrito.
Umidade não entra na fórmula de etileno. Maturação mista/desconhecida não é corrigida
para verde/madura. O frontend deve mostrar explicitamente as limitações retornadas.

AVALIADO não significa seguro ou sem alertas. Prioridades configuráveis nesta versão:
INFORMATIVO/ATENCAO. CRITICO existe no enum legado, mas não é gerado/configurável no novo motor.
Retorno posterior à faixa não resolve alertas automaticamente.

virtual_ligado refere-se à intervenção consultada. atuador_virtual_ocupado refere-se
ao veículo compartilhado. acoes_permitidas ajuda a tela, mas o servidor revalida tudo.
prazo_excedido e consultado_em são projeções, não uma transição concluída.
Duração planejada é didática, até 86400 s; encerramento registra duração efetiva,
que pode superar o planejado. Não converter tempo virtual em eficácia física.

## 5. Idempotência, precisão, paginação e falhas

Persistir a chave e TODO o payload da operação antes de enviar. Em retry de rede,
reutilizar a mesma chave/payload; não regenerar corte, justificativa ou UUID.
Outra chave significa nova solicitação/avaliação/análise. Chave incompatível retorna 409.
A criação de sessão usa chave por autor; sincronização/análise/avaliação/intervenção
usam escopo de sessão; decisões/ações usam o caso/intervenção. O ator também é validado.
PUT da declaração da carga tem comportamento idempotente por conteúdo.

Listagens usam limit/offset, sem cursor. O padrão e o limite máximo constam em cada
operação no inventário; não assumir o mesmo para todas. Sessões legadas retornam
listas simples; histórico/análises/alertas/intervenções usam envelopes próprios.
Histórico IoT: fixar revisão e janela ao paginar. Novos registros podem deslocar
páginas de listagens ordenadas por execução; a API não oferece cursor de snapshot.

Enviar Decimal como string para preservar precisão no JavaScript. As saídas
científicas retornam strings; não calcular/quantizar volumes com Number no frontend.
Datas da requisição precisam conter fuso quando indicado como AwareDatetime;
prefira UTC Z. A apresentação de datas legadas pode ter diferenças de offset na
camada SQLite; não remover o fuso para fazer contas. Não usar instante de consulta
como horário de medição.

HTTP: 401 autenticação/expiração; 403 papel/empresa; 404 recurso no escopo;
409 estado, revisão, idempotência, referência ou atuador ocupado; 422 validação;
503 falha de configuração/persistência. Erros de validação: detail é uma lista de
{type,loc,msg}; erros de domínio: detail geralmente é string. Não depender de input/ctx.
O OpenAPI legado de login não enumera todos os erros 401/503, mas o serviço os produz.
Sincronização pode retornar 202 ainda em execução, ou 200 com FALHA/PARCIAL; 200 não
garante aquisição completa. Criação de sessão retorna 201 ou 200 em replay.
Em 409, consultar estado antes de tentar nova decisão; não repetir início automaticamente.

## 6. Payloads válidos e didáticos

Os UUIDs abaixo são fictícios; trocar pelos IDs obtidos nas respostas. Datas são
hipotéticas: devem estar dentro da sessão e até o corte real. Os limites ambientais
e G dos exemplos não são parâmetros científicos validados de dano.


### CargaCreate

```json
{
  "produto_id": "00000000-0000-0000-0000-000000000001",
  "produtor_id": "00000000-0000-0000-0000-000000000002",
  "identificacao": "DEMO-TOMMY-001",
  "observacoes": "Carga hipotetica em ambiente de testes."
}
```


### CargaMonitoramentoPut

```json
{
  "produto_identificado": "MANGA_TOMMY_ATKINS",
  "massa_kg": "1000.0000",
  "maturacao": "MISTA",
  "lote_codigo": "DEMO-001",
  "lote_hipotetico": true,
  "rastreabilidade": "Dados hipoteticos para demonstracao local."
}
```


### SessaoCreate

```json
{
  "inicio": "2026-10-28T08:00:00Z",
  "sensor_temperatura_id": "00000000-0000-0000-0000-000000000003",
  "sensor_umidade_id": "00000000-0000-0000-0000-000000000004",
  "ambiente_aquisicao": "TRANSPORTE_REFRIGERADO",
  "chave_idempotencia": "00000000-0000-0000-0000-000000000005"
}
```


### SincronizacaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000006",
  "origem_dados": "THINGSPEAK"
}
```


### AnaliseCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000007",
  "intervalo_maximo_s": "3600",
  "modo": "MODO_RESTRITO",
  "fim": "2026-10-28T10:00:00Z",
  "corte_aquisicao": "2026-10-28T11:00:00Z"
}
```


### ConfiguracaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000008",
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
  "justificativa": "Limites didaticos sem validacao de dano fisiologico.",
  "prioridade": "ATENCAO"
}
```


### AvaliacaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000009",
  "fim": "2026-10-28T10:00:00Z",
  "corte_aquisicao": "2026-10-28T11:00:00Z"
}
```


### DecisaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000010",
  "acao": "RECONHECER",
  "justificativa": "Operador examinou a evidencia ambiental."
}
```


### IntervencaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000011",
  "justificativa": "Solicitacao humana de demonstracao supervisionada.",
  "duracao_planejada_s": "60"
}
```


### AcaoCreate

```json
{
  "chave_idempotencia": "00000000-0000-0000-0000-000000000012",
  "acao": "AUTORIZAR",
  "justificativa": "Gestor autoriza somente a demonstracao virtual."
}
```


## 7. Inventário real das operações

Método/caminho, segurança declarada, body, parâmetros e schemas de resposta abaixo são extraídos do OpenAPI. Somente raiz, health e login são públicos no OpenAPI; operações privadas exigem JWT e suas permissões de perfil/escopo.


### GET /

Read Root

- Segurança declarada: **sem Bearer declarado (legado ou rota pública)**.

- Body: nenhum.

- HTTP 200: object.


### GET /health

Health Check

- Segurança declarada: **sem Bearer declarado (legado ou rota pública)**.

- Body: nenhum.

- HTTP 200: object.


### GET /api/v1/integracoes/thingspeak/status

Diagnostico administrativo privado da integracao global

- Segurança declarada: Bearer.

- Body: nenhum.

- HTTP 200: ThingSpeakStatusResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN..

- HTTP 503: Configuracao insegura/invalida ou indisponibilidade da integracao..


### GET /api/v1/integracoes/thingspeak/feeds

Consultar leituras do canal global como ADMIN

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro results em query: integer; minimum=1; maximum=8000 ou null; obrigatório=false; padrão=10.

- HTTP 200: ThingSpeakMappingResult.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN..

- HTTP 503: Configuracao insegura/invalida ou indisponibilidade da integracao..

- HTTP 422: HTTPValidationError.


### GET /api/v1/integracoes/thingspeak/ultima-leitura

Consultar ultimo feed do canal global como ADMIN

- Segurança declarada: Bearer.

- Body: nenhum.

- HTTP 200: ThingSpeakFeed ou null.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN..

- HTTP 503: Configuracao insegura/invalida ou indisponibilidade da integracao..


### POST /api/v1/integracoes/thingspeak/sincronizar

Sincronizacao manual administrativa do canal global

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro results em query: integer; minimum=1; maximum=8000 ou null; obrigatório=false; padrão=100.

- HTTP 200: ThingSpeakSyncSummary.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Canal global sem propriedade empresarial persistida: acesso exclusivo de ADMIN..

- HTTP 503: Configuracao insegura/invalida ou indisponibilidade da integracao..

- HTTP 422: HTTPValidationError.


### POST /api/v1/auth/login

Login

- Segurança declarada: **sem Bearer declarado (legado ou rota pública)**.

- Body: LoginRequest.

- HTTP 200: TokenResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/auth/me

Me

- Segurança declarada: Bearer.

- Body: nenhum.

- HTTP 200: CurrentUserResponse.


### GET /api/v1/perfis

Profiles

- Segurança declarada: Bearer.

- Body: nenhum.

- HTTP 200: lista de PerfilResponse.


### POST /api/v1/usuarios

Create

- Segurança declarada: Bearer.

- Body: UsuarioCreate.

- HTTP 201: UsuarioResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/usuarios

Users

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- HTTP 200: lista de UsuarioResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/usuarios/{usuario_id}

Detail

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro usuario_id em path: string (uuid); obrigatório=true.

- HTTP 200: UsuarioResponse.

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/usuarios/{usuario_id}

Update

- Segurança declarada: Bearer.

- Body: UsuarioUpdate.

- Parâmetro usuario_id em path: string (uuid); obrigatório=true.

- HTTP 200: UsuarioResponse.

- HTTP 422: HTTPValidationError.


### POST /api/v1/empresas

Create

- Segurança declarada: Bearer.

- Body: EmpresaCreate.

- HTTP 201: EmpresaResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/empresas

Companies

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- HTTP 200: lista de EmpresaResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/empresas/{empresa_id}

Detail

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em path: string (uuid); obrigatório=true.

- HTTP 200: EmpresaResponse.

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/empresas/{empresa_id}

Update

- Segurança declarada: Bearer.

- Body: EmpresaUpdate.

- Parâmetro empresa_id em path: string (uuid); obrigatório=true.

- HTTP 200: EmpresaResponse.

- HTTP 422: HTTPValidationError.


### POST /api/v1/empresas/{empresa_id}/usuarios/{usuario_id}

Link

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em path: string (uuid); obrigatório=true.

- Parâmetro usuario_id em path: string (uuid); obrigatório=true.

- HTTP 200: VinculoResponse.

- HTTP 422: HTTPValidationError.


### GET /api/v1/empresas/{empresa_id}/usuarios

Users

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em path: string (uuid); obrigatório=true.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- HTTP 200: lista de UsuarioResponse.

- HTTP 422: HTTPValidationError.


### POST /api/v1/produtos

Create

- Segurança declarada: Bearer.

- Body: ProdutoCreate.

- HTTP 201: ProdutoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/produtos

Products

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro ativo em query: boolean ou null; obrigatório=false.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de ProdutoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/produtos/{produto_id}

Get

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro produto_id em path: string (uuid); obrigatório=true.

- HTTP 200: ProdutoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/produtos/{produto_id}

Update

- Segurança declarada: Bearer.

- Body: ProdutoUpdate.

- Parâmetro produto_id em path: string (uuid); obrigatório=true.

- HTTP 200: ProdutoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/produtos/{produto_id}/parametros

Create Parameter

- Segurança declarada: Bearer.

- Body: ParametroCreate.

- Parâmetro produto_id em path: string (uuid); obrigatório=true.

- HTTP 201: ParametroResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/produtos/{produto_id}/parametros

Parameters

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro produto_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de ParametroResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/produtos/{produto_id}/parametros/{parametro_id}

Update Parameter

- Segurança declarada: Bearer.

- Body: ParametroUpdate.

- Parâmetro produto_id em path: string (uuid); obrigatório=true.

- Parâmetro parametro_id em path: string (uuid); obrigatório=true.

- HTTP 200: ParametroResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/veiculos

Create Veiculos

- Segurança declarada: Bearer.

- Body: VeiculoCreate.

- HTTP 201: VeiculoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/veiculos

List Veiculos

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro ativo em query: boolean ou null; obrigatório=false.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de VeiculoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/veiculos/{veiculo_id}

Get Veiculos

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro veiculo_id em path: string (uuid); obrigatório=true.

- HTTP 200: VeiculoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/veiculos/{veiculo_id}

Update Veiculos

- Segurança declarada: Bearer.

- Body: VeiculoUpdate.

- Parâmetro veiculo_id em path: string (uuid); obrigatório=true.

- HTTP 200: VeiculoResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/motoristas

Create Motoristas

- Segurança declarada: Bearer.

- Body: MotoristaCreate.

- HTTP 201: MotoristaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/motoristas

List Motoristas

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro ativo em query: boolean ou null; obrigatório=false.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de MotoristaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/motoristas/{motorista_id}

Get Motoristas

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro motorista_id em path: string (uuid); obrigatório=true.

- HTTP 200: MotoristaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/motoristas/{motorista_id}

Update Motoristas

- Segurança declarada: Bearer.

- Body: MotoristaUpdate.

- Parâmetro motorista_id em path: string (uuid); obrigatório=true.

- HTTP 200: MotoristaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/viagens

Create Viagens

- Segurança declarada: Bearer.

- Body: ViagemCreate.

- HTTP 201: ViagemResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/viagens

List Viagens

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro empresa_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro status em query: StatusViagem ou null; obrigatório=false.

- Parâmetro veiculo_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro motorista_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de ViagemResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/viagens/{viagem_id}

Get Viagens

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro viagem_id em path: string (uuid); obrigatório=true.

- HTTP 200: ViagemResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/viagens/{viagem_id}

Update Viagens

- Segurança declarada: Bearer.

- Body: ViagemUpdate.

- Parâmetro viagem_id em path: string (uuid); obrigatório=true.

- HTTP 200: ViagemResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/viagens/{viagem_id}/cargas

Create Carga

- Segurança declarada: Bearer.

- Body: CargaCreate.

- Parâmetro viagem_id em path: string (uuid); obrigatório=true.

- HTTP 201: CargaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/viagens/{viagem_id}/cargas

List Cargas

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro viagem_id em path: string (uuid); obrigatório=true.

- Parâmetro produto_id em query: string (uuid) ou null; obrigatório=false.

- Parâmetro status em query: StatusCarga ou null; obrigatório=false.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de CargaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/cargas/{carga_id}

Get Carga

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 200: CargaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/cargas/{carga_id}

Update Carga

- Segurança declarada: Bearer.

- Body: CargaUpdate.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 200: CargaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### POST /api/v1/cargas/{carga_id}/caixas

Create Caixa

- Segurança declarada: Bearer.

- Body: CaixaCreate.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 201: CaixaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/cargas/{carga_id}/caixas

List Caixas

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de CaixaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### GET /api/v1/caixas/{caixa_id}

Get Caixa

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro caixa_id em path: string (uuid); obrigatório=true.

- HTTP 200: CaixaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PATCH /api/v1/caixas/{caixa_id}

Update Caixa

- Segurança declarada: Bearer.

- Body: CaixaUpdate.

- Parâmetro caixa_id em path: string (uuid); obrigatório=true.

- HTTP 200: CaixaResponse.

- HTTP 401: JWT ausente, invalido, expirado ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao; nenhum dado do recurso e retornado..

- HTTP 404: Recurso inexistente..

- HTTP 409: Conflito de integridade ou transportadora inativa para escrita..

- HTTP 422: HTTPValidationError.


### PUT /api/v1/cargas/{carga_id}/monitoramento

Declarar ou substituir os dados adicionais da carga

- Segurança declarada: Bearer.

- Body: CargaMonitoramentoPut.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 200: CargaMonitoramentoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/cargas/{carga_id}/monitoramento

Consultar os dados adicionais de monitoramento

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 200: CargaMonitoramentoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/cargas/{carga_id}/monitoramentos

Iniciar uma sessao com janela efetiva explicita

- Segurança declarada: Bearer.

- Body: SessaoCreate.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- HTTP 201: SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 200: SessaoResponse-Input.


### GET /api/v1/cargas/{carga_id}/monitoramentos

Listar sessoes da carga com paginacao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro carga_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/viagens/{viagem_id}/monitoramentos

Listar sessoes da viagem com paginacao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro viagem_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=50.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: lista de SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/monitoramentos/{sessao_id}

Consultar a sessao e seu snapshot de rastreabilidade

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/monitoramentos/{sessao_id}/encerrar

Encerrar uma sessao ativa, com horario e motivo

- Segurança declarada: Bearer.

- Body: SessaoFinalizar.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/monitoramentos/{sessao_id}/cancelar

Cancelar uma sessao ativa, sem apagar sua janela historica

- Segurança declarada: Bearer.

- Body: SessaoFinalizar.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: SessaoResponse-Output.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/monitoramentos/{sessao_id}/sincronizacoes

Sincronizar explicitamente o historico de uma sessao

- Segurança declarada: Bearer.

- Body: SincronizacaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: SincronizacaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 202: SincronizacaoResponse.


### GET /api/v1/monitoramentos/{sessao_id}/sincronizacoes

Consultar estado e tentativas de sincronizacao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: EstadoSincronizacaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/monitoramentos/{sessao_id}/leituras

Consultar leituras e marcadores invalidos em ordem cronologica

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=1000; obrigatório=false; padrão=100.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro tipo em query: string; pattern=^(TEMPERATURA|UMIDADE)$ ou null; obrigatório=false.

- Parâmetro revisao em query: integer; minimum=1 ou null; obrigatório=false.

- Parâmetro inicio em query: string (date-time) ou null; obrigatório=false.

- Parâmetro fim em query: string (date-time) ou null; obrigatório=false.

- HTTP 200: HistoricoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/monitoramentos/{sessao_id}/qualidade

Consultar lacunas e cobertura temporal, sem estimativa de etileno

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro intervalo_maximo_s em query: number; exclusiveMinimum=0.0 ou string; obrigatório=true.

- Parâmetro revisao em query: integer; minimum=1 ou null; obrigatório=false.

- Parâmetro inicio em query: string (date-time) ou null; obrigatório=false.

- Parâmetro fim em query: string (date-time) ou null; obrigatório=false.

- HTTP 200: QualidadeResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/monitoramentos/{sessao_id}/analises-etileno

Calcular e persistir producao potencial com o motor cientifico existente

- Segurança declarada: Bearer.

- Body: AnaliseCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: AnaliseResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha de persistencia; consulte ou repita a mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/analises-etileno

Listar analises preservadas da sessao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: AnaliseLista.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### GET /api/v1/monitoramentos/{sessao_id}/analises-etileno/{analise_id}

Consultar resultado e entradas fixados, sem recalcular

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro analise_id em path: string (uuid); obrigatório=true.

- HTTP 200: AnaliseResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..


### POST /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais

Registrar versao imutavel de parametros operacionais

- Segurança declarada: Bearer.

- Body: ConfiguracaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: ConfiguracaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/configuracoes-ambientais

Listar versoes da configuracao operacional

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: ListaConfiguracoes.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### POST /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas

Avaliar dados ambientais e registrar alertas explicaveis

- Segurança declarada: Bearer.

- Body: AvaliacaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: AvaliacaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas

Listar avaliacoes imutaveis

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: ListaAvaliacoes.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/avaliacoes-preventivas/{avaliacao_id}

Consultar snapshot e resultado sem reavaliar

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro avaliacao_id em path: string (uuid); obrigatório=true.

- HTTP 200: AvaliacaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/alertas

Listar alertas operacionais da sessao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro status em query: string; pattern=^(ABERTO|EM_ANALISE|RESOLVIDO|DESCARTADO)$ ou null; obrigatório=false.

- HTTP 200: ListaAlertas.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}

Consultar alerta ambiental

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro alerta_id em path: string (uuid); obrigatório=true.

- HTTP 200: AlertaResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### POST /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes

Reconhecer, observar, resolver ou descartar com justificativa

- Segurança declarada: Bearer.

- Body: DecisaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro alerta_id em path: string (uuid); obrigatório=true.

- HTTP 200: DecisaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/decisoes

Consultar historico auditavel de decisoes

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro alerta_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: ListaDecisoes.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### GET /api/v1/monitoramentos/{sessao_id}/alertas/{alerta_id}/evidencias

Consultar evidencias e avaliacoes que sustentam o alerta

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro alerta_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: ListaEvidencias.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consultar ou repetir mesma chave idempotente..


### POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas

Solicitar intervencao virtual com justificativa humana

- Segurança declarada: Bearer.

- Body: IntervencaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- HTTP 200: IntervencaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consulte ou repita mesma chave..


### GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas

Listar intervencoes da sessao

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- Parâmetro estado em query: enum: SOLICITADA, AUTORIZADA, RECUSADA, EM_EXECUCAO, CONCLUIDA, CANCELADA, FALHA_SIMULACAO ou null; obrigatório=false.

- HTTP 200: ListaIntervencoes.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consulte ou repita mesma chave..


### GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}

Consultar estado logico e permissoes atuais

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro intervencao_id em path: string (uuid); obrigatório=true.

- HTTP 200: IntervencaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consulte ou repita mesma chave..


### POST /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes

Registrar decisao humana ou transicao virtual

- Segurança declarada: Bearer.

- Body: AcaoCreate.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro intervencao_id em path: string (uuid); obrigatório=true.

- HTTP 200: AcaoResponse.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consulte ou repita mesma chave..


### GET /api/v1/monitoramentos/{sessao_id}/intervencoes-simuladas/{intervencao_id}/acoes

Consultar trilha ordenada de decisoes e transicoes

- Segurança declarada: Bearer.

- Body: nenhum.

- Parâmetro sessao_id em path: string (uuid); obrigatório=true.

- Parâmetro intervencao_id em path: string (uuid); obrigatório=true.

- Parâmetro limit em query: integer; minimum=1; maximum=100; obrigatório=false; padrão=20.

- Parâmetro offset em query: integer; minimum=0; obrigatório=false; padrão=0.

- HTTP 200: ListaAcoes.

- HTTP 401: Autenticacao ausente, invalida ou usuario inativo..

- HTTP 403: Perfil ou vinculo empresarial sem permissao..

- HTTP 404: Carga, viagem, configuracao, sessao ou sensor nao encontrado..

- HTTP 409: Conflito temporal, estado, integridade ou chave idempotente..

- HTTP 422: Dados, horarios, massa ou sensores invalidos..

- HTTP 503: Falha transacional; consulte ou repita mesma chave..


## 8. Dicionário completo dos schemas reais

Obrigatório vem de required no JSON Schema; null permitido é indicado no tipo. Campos de resposta podem ser obrigatórios e nullable. Objetos dict/livres não possuem estrutura integral descrita pelo OpenAPI; a documentação do módulo e a resposta armazenada são necessários para seu conteúdo interno.


### AcaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| acao | sim | enum: AUTORIZAR, RECUSAR, INICIAR, ENCERRAR, CANCELAR, REGISTRAR_FALHA | — |  |

| justificativa | sim | string; maxLength=4000; minLength=1 | — |  |


### AcaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| intervencao_id | sim | string (uuid) | — |  |

| ocorrencia_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| numero | sim | integer | — |  |

| acao | sim | string | — |  |

| justificativa | sim | string | — |  |

| estado_anterior | sim | string ou null | — |  |

| estado_posterior | sim | enum: SOLICITADA, AUTORIZADA, RECUSADA, EM_EXECUCAO, CONCLUIDA, CANCELADA, FALHA_SIMULACAO | — |  |

| registrada_em | sim | string (date-time) | — |  |

| contexto_snapshot | sim | object | — |  |


### AlertaResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| viagem_id | sim | string (uuid) | — |  |

| carga_id | sim | string (uuid) ou null | — |  |

| tipo | sim | string | — |  |

| nivel | sim | enum: INFORMATIVO, ATENCAO, CRITICO | — |  |

| status | sim | enum: ABERTO, EM_ANALISE, RESOLVIDO, DESCARTADO | — |  |

| iniciado_em | sim | string (date-time) | — |  |

| finalizado_em | sim | string (date-time) ou null | — |  |

| evidencias_total | sim | integer | — |  |

| classificacao_risco_etileno | não | enum: NAO_AVALIADO | "NAO_AVALIADO" |  |

| intervencao | não | enum: AVALIACAO_HUMANA_NECESSARIA | "AVALIACAO_HUMANA_NECESSARIA" |  |


### AnaliseCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| modo | não | ModoCalculo | "MODO_RESTRITO" |  |

| intervalo_maximo_s | não | number; exclusiveMinimum=0.0 ou string ou null | — | G operacional explicito. Ausencia persiste CONFIGURACAO_INCOMPLETA, sem volumes. |

| inicio | não | string (date-time) ou null | — |  |

| fim | não | string (date-time) ou null | — |  |

| corte_aquisicao | não | string (date-time) ou null | — | Obrigatorio para sessao ativa; inclui apenas revisoes consolidadas ate este instante. Nunca futuro. |

| revisao_aquisicao | não | integer; minimum=0.0 ou null | — | Revisao consolidada; 0 representa ausencia de aquisicao. Omissao fixa a ultima elegivel no corte. |


### AnaliseLista

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| sessao_id | sim | string (uuid) | — |  |

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| analises | sim | lista de AnaliseResponse | — |  |


### AnaliseResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| executada_em | sim | string (date-time) | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) | — |  |

| corte_aquisicao | sim | string (date-time) | — |  |

| revisao_aquisicao | sim | integer | — |  |

| massa_kg | sim | string ou null | — |  |

| maturacao | sim | string | — |  |

| modo | sim | ModoCalculo | — |  |

| intervalo_maximo_s | sim | string ou null | — |  |

| versao_modelo | sim | string | — |  |

| status_calculo | sim | StatusCalculo | — |  |

| classificacao_risco_etileno | sim | enum: NAO_AVALIADO | — |  |

| hash_entrada | sim | string | — |  |

| hash_resultado | sim | string | — |  |

| entrada_snapshot | sim | object | — |  |

| resultado | sim | ResultadoResponse | — |  |


### AvaliacaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| configuracao_id | não | string (uuid) ou null | — |  |

| inicio | não | string (date-time) ou null | — |  |

| fim | não | string (date-time) ou null | — |  |

| corte_aquisicao | não | string (date-time) ou null | — |  |

| revisao | não | integer; minimum=0.0 ou null | — |  |

| analise_etileno_id | não | string (uuid) ou null | — |  |


### AvaliacaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| configuracao_id | sim | string (uuid) ou null | — |  |

| anterior_id | sim | string (uuid) ou null | — |  |

| analise_etileno_id | sim | string (uuid) ou null | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| executada_em | sim | string (date-time) | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) | — |  |

| corte_aquisicao | sim | string (date-time) | — |  |

| revisao | sim | integer | — |  |

| hash_entrada | sim | string | — |  |

| hash_resultado | sim | string | — |  |

| entrada_snapshot | sim | object | — |  |

| resultado | sim | object | — |  |

| alertas_ids | sim | lista de string (uuid) | — |  |


### CaixaCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| identificacao | sim | string; maxLength=120; minLength=1 | — |  |

| codigo_externo | não | string; maxLength=120 ou null | — |  |

| peso | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| observacoes | não | string ou null | — |  |


### CaixaResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| identificacao | sim | string; maxLength=120; minLength=1 | — |  |

| codigo_externo | não | string; maxLength=120 ou null | — |  |

| peso | não | string ou null | — |  |

| observacoes | não | string ou null | — |  |

| carga_id | sim | string (uuid) | — |  |

| status | sim | StatusCaixa | — |  |


### CaixaUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| identificacao | não | string; maxLength=120; minLength=1 ou null | — |  |

| codigo_externo | não | string; maxLength=120 ou null | — |  |

| peso | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| observacoes | não | string ou null | — |  |

| status | não | StatusCaixa ou null | — |  |


### CargaCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| produto_id | sim | string (uuid) | — |  |

| produtor_id | sim | string (uuid) | — |  |

| cliente_id | não | string (uuid) ou null | — |  |

| identificacao | sim | string; maxLength=120; minLength=1 | — |  |

| quantidade_caixas | não | integer; minimum=0.0; maximum=2147483647.0 ou null | — |  |

| quantidade | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| unidade | não | string; maxLength=30; minLength=1 ou null | — |  |

| origem_produto | não | string; maxLength=255 ou null | — |  |

| observacoes | não | string ou null | — |  |


### CargaMonitoramentoPut

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| produto_identificado | sim | enum: MANGA_TOMMY_ATKINS | — |  |

| massa_kg | sim | number; exclusiveMinimum=0.0 ou string | — |  |

| maturacao | não | MaturacaoCarga | "DESCONHECIDA" |  |

| lote_codigo | sim | string; maxLength=120; minLength=1 | — |  |

| lote_hipotetico | sim | boolean | — |  |

| rastreabilidade | sim | string; maxLength=2000; minLength=1 | — |  |


### CargaMonitoramentoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| carga_id | sim | string (uuid) | — |  |

| produto_identificado | sim | string | — |  |

| massa_kg | sim | string | — |  |

| maturacao | sim | MaturacaoCarga | — |  |

| lote_codigo | sim | string | — |  |

| lote_hipotetico | sim | boolean | — |  |

| rastreabilidade | sim | string | — |  |

| versao | sim | integer | — |  |

| atualizado_por_id | sim | string (uuid) | — |  |


### CargaResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| produto_id | sim | string (uuid) | — |  |

| produtor_id | sim | string (uuid) | — |  |

| cliente_id | não | string (uuid) ou null | — |  |

| identificacao | sim | string; maxLength=120; minLength=1 | — |  |

| quantidade_caixas | não | integer; minimum=0.0; maximum=2147483647.0 ou null | — |  |

| quantidade | não | string ou null | — |  |

| unidade | não | string; maxLength=30; minLength=1 ou null | — |  |

| origem_produto | não | string; maxLength=255 ou null | — |  |

| observacoes | não | string ou null | — |  |

| viagem_id | sim | string (uuid) | — |  |

| status | sim | StatusCarga | — |  |


### CargaUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| identificacao | não | string; maxLength=120; minLength=1 ou null | — |  |

| quantidade_caixas | não | integer; minimum=0.0; maximum=2147483647.0 ou null | — |  |

| quantidade | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| unidade | não | string; maxLength=30; minLength=1 ou null | — |  |

| origem_produto | não | string; maxLength=255 ou null | — |  |

| observacoes | não | string ou null | — |  |

| status | não | StatusCarga ou null | — |  |


### ConfiguracaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| temperatura_min_c | sim | number ou string | — |  |

| temperatura_max_c | sim | number ou string | — |  |

| umidade_min_percentual | sim | number; minimum=0.0; maximum=100.0 ou string | — |  |

| umidade_max_percentual | sim | number; minimum=0.0; maximum=100.0 ou string | — |  |

| intervalo_maximo_s | sim | number; exclusiveMinimum=0.0 ou string | — |  |

| cobertura_min_percentual | sim | number; exclusiveMinimum=0.0; maximum=100.0 ou string | — |  |

| exposicao_continua_s | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| maturacoes_aplicaveis | sim | lista de EstagioMaturacao; maxItems=5; minItems=1 | — |  |

| ambiente | sim | enum: TRANSPORTE_REFRIGERADO, LABORATORIO | — |  |

| fundamento | sim | enum: OPERACIONAL, EXPERIMENTAL | — |  |

| justificativa | sim | string; maxLength=4000; minLength=10 | — |  |

| referencias | não | lista de string; maxItems=10 | — |  |

| prioridade | não | enum: INFORMATIVO, ATENCAO | "ATENCAO" |  |


### ConfiguracaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| versao | sim | integer | — |  |

| registrada_em | sim | string (date-time) | — |  |

| parametros | sim | object | — |  |


### CurrentUserResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| nome | sim | string | — |  |

| email | sim | string | — |  |

| perfil_id | sim | string (uuid) ou null | — |  |

| ativo | sim | boolean | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| perfil | sim | string ou null | — |  |

| empresas | sim | lista de EmpresaResponse | — |  |


### DecisaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| acao | sim | enum: RECONHECER, OBSERVAR, RESOLVER, DESCARTAR | — |  |

| justificativa | sim | string; maxLength=4000; minLength=1 | — |  |


### DecisaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| alerta_id | sim | string (uuid) | — |  |

| ocorrencia_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| acao | sim | string | — |  |

| justificativa | sim | string | — |  |

| estado_anterior | sim | string ou null | — |  |

| estado_posterior | sim | string | — |  |

| registrada_em | sim | string (date-time) | — |  |


### EmpresaCreate

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | sim | string; maxLength=180; minLength=1 | — |  |

| tipo | sim | TipoEmpresa | — |  |

| documento | não | string; maxLength=40; minLength=1 ou null | — |  |

| ativo | não | boolean | true |  |


### EmpresaResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| nome | sim | string | — |  |

| tipo | sim | TipoEmpresa | — |  |

| documento | sim | string ou null | — |  |

| ativo | sim | boolean | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |


### EmpresaUpdate

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | não | string; maxLength=180; minLength=1 ou null | — |  |

| tipo | não | TipoEmpresa ou null | — |  |

| documento | não | string; maxLength=40; minLength=1 ou null | — |  |

| ativo | não | boolean ou null | — |  |


### EstadoSincronizacaoResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| sessao_id | sim | string (uuid) | — |  |

| revisao_disponivel | sim | integer | — |  |

| em_execucao | sim | string (uuid) ou null | — |  |

| tentativas | sim | lista de SincronizacaoResponse | — |  |


### EstagioMaturacao

enum: VERDE_MADURA, EM_AMADURECIMENTO, MADURA, MISTA, DESCONHECIDA


### HTTPValidationError

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| detail | não | lista de ValidationError | — |  |


### HistoricoResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| sessao_id | sim | string (uuid) | — |  |

| estado_sessao | sim | string | — |  |

| revisao | sim | integer | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) | — |  |

| massa_kg | sim | string | — |  |

| maturacao | sim | string | — |  |

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| leituras | sim | lista de LeituraHistoricoResponse | — |  |

| metadados_temporais_invalidos | sim | boolean | — |  |

| cancelada_para_analise | sim | boolean | — |  |

| ocorrencias | sim | lista de object | — |  |


### IntervaloResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) | — |  |

| duracao_s | sim | string | — |  |

| temperatura_inicio_c | sim | string ou null | — |  |

| taxa_min_ul_kg_h | sim | string ou null | — |  |

| taxa_max_ul_kg_h | sim | string ou null | — |  |

| volume_min_ul | sim | string ou null | — |  |

| volume_max_ul | sim | string ou null | — |  |

| motivos | sim | lista de string | — |  |


### IntervencaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| justificativa | sim | string; maxLength=4000; minLength=1 | — |  |

| duracao_planejada_s | sim | number; exclusiveMinimum=0.0; maximum=86400.0 ou string | — | Duracao de demonstracao, ate 24h; sem eficacia cientifica ou encerramento automatico. |

| alerta_id | não | string (uuid) ou null | — |  |

| avaliacao_id | não | string (uuid) ou null | — |  |

| analise_etileno_id | não | string (uuid) ou null | — |  |


### IntervencaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| viagem_id | sim | string (uuid) | — |  |

| carga_id | sim | string (uuid) | — |  |

| veiculo_id | sim | string (uuid) | — |  |

| atuador_virtual_id | sim | string | — |  |

| alerta_id | sim | string (uuid) ou null | — |  |

| avaliacao_id | sim | string (uuid) ou null | — |  |

| analise_etileno_id | sim | string (uuid) ou null | — |  |

| solicitante_id | sim | string (uuid) | — |  |

| decidida_por_id | sim | string (uuid) ou null | — |  |

| iniciada_por_id | sim | string (uuid) ou null | — |  |

| finalizada_por_id | sim | string (uuid) ou null | — |  |

| modalidade | sim | enum: SIMULADA | — |  |

| estado | sim | enum: SOLICITADA, AUTORIZADA, RECUSADA, EM_EXECUCAO, CONCLUIDA, CANCELADA, FALHA_SIMULACAO | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| justificativa_solicitacao | sim | string | — |  |

| motivo_fim | sim | string ou null | — |  |

| solicitada_em | sim | string (date-time) | — |  |

| decidida_em | sim | string (date-time) ou null | — |  |

| iniciada_em | sim | string (date-time) ou null | — |  |

| prazo_planejado_em | sim | string (date-time) ou null | — |  |

| finalizada_em | sim | string (date-time) ou null | — |  |

| duracao_planejada_s | sim | string | — |  |

| duracao_registrada_s | sim | string ou null | — |  |

| referencias_snapshot | sim | object | — |  |

| hash_referencias | sim | string | — |  |

| referencias_atuais | sim | object | — |  |

| hash_referencias_atuais | sim | string | — |  |

| virtual_ligado | sim | boolean | — |  |

| atuador_virtual_ocupado | sim | boolean | — |  |

| prazo_excedido | sim | boolean | — |  |

| consultado_em | sim | string (date-time) | — |  |

| sessao_terminal_com_execucao | sim | boolean | — |  |

| contexto_logistico_alterado | sim | boolean | — |  |

| acoes_permitidas | sim | lista de enum: AUTORIZAR, RECUSAR, INICIAR, ENCERRAR, CANCELAR, REGISTRAR_FALHA | — |  |

| classificacao_risco_etileno | não | enum: NAO_AVALIADO | "NAO_AVALIADO" |  |

| resultado_operacional | sim | string | — |  |

| limitacoes | sim | lista de string | — |  |


### LeituraHistoricoResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| fonte_id | sim | string (uuid) | — |  |

| medicao_id | sim | string (uuid) ou null | — |  |

| sensor_id | sim | string (uuid) | — |  |

| tipo | sim | string | — |  |

| channel_id | sim | string | — |  |

| field_name | sim | string | — |  |

| unidade | sim | string | — |  |

| entry_id | sim | integer | — |  |

| medida_em | sim | string (date-time) | — |  |

| timestamp_origem | sim | string | — |  |

| recebida_em | sim | string (date-time) ou null | — |  |

| processada_em | sim | string (date-time) | — |  |

| valor | sim | string ou null | — |  |

| estado | sim | string | — |  |

| motivo | sim | string ou null | — |  |

| revisao_incorporacao | sim | integer | — |  |

| tardia | sim | boolean ou null | — |  |

| apos_encerramento | sim | boolean | — |  |

| fora_de_ordem | sim | boolean | — |  |

| conflito_observado | sim | boolean | — |  |


### ListaAcoes

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| acoes | sim | lista de AcaoResponse | — |  |


### ListaAlertas

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| alertas | sim | lista de AlertaResponse | — |  |


### ListaAvaliacoes

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| avaliacoes | sim | lista de AvaliacaoResponse | — |  |


### ListaConfiguracoes

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| configuracoes | sim | lista de ConfiguracaoResponse | — |  |


### ListaDecisoes

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| decisoes | sim | lista de DecisaoResponse | — |  |


### ListaEvidencias

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| evidencias | sim | lista de object | — |  |


### ListaIntervencoes

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| total | sim | integer | — |  |

| limit | sim | integer | — |  |

| offset | sim | integer | — |  |

| intervencoes | sim | lista de IntervencaoResponse | — |  |


### LoginRequest

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| email | sim | string (email) | — |  |

| senha | sim | string (password); maxLength=128; minLength=1 | — |  |


### MaturacaoCarga

enum: VERDE_MADURA, EM_AMADURECIMENTO, MADURA, MISTA, DESCONHECIDA


### ModoCalculo

enum: MODO_RESTRITO, MODO_EXPLORATORIO


### MotoristaCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| empresa_id | sim | string (uuid) | — |  |

| nome | sim | string; maxLength=150; minLength=1 | — |  |

| documento | não | string; maxLength=40; minLength=1 ou null | — |  |

| telefone | não | string; maxLength=40 ou null | — |  |

| ativo | não | boolean | true |  |


### MotoristaResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| empresa_id | sim | string (uuid) | — |  |

| nome | sim | string; maxLength=150; minLength=1 | — |  |

| documento | não | string; maxLength=40; minLength=1 ou null | — |  |

| telefone | não | string; maxLength=40 ou null | — |  |

| ativo | não | boolean | true |  |


### MotoristaUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | não | string; maxLength=150; minLength=1 ou null | — |  |

| documento | não | string; maxLength=40; minLength=1 ou null | — |  |

| telefone | não | string; maxLength=40 ou null | — |  |

| ativo | não | boolean ou null | — |  |


### NormalizedThingSpeakReading

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| source | não | string | "thingspeak" |  |

| channel_id | sim | string | — |  |

| entry_id | sim | integer | — |  |

| field_name | sim | string | — |  |

| created_at | sim | string (date-time) | — |  |

| sensor_id | não | string (uuid) ou null | — |  |

| tipo | não | string ou null | — |  |

| contexto | não | string ou null | — |  |

| valor | não | string ou null | — |  |

| unidade | não | string ou null | — |  |

| viagem_id | não | string (uuid) ou null | — |  |

| carga_id | não | string (uuid) ou null | — |  |

| caixa_id | não | string (uuid) ou null | — |  |

| valor_original | não | string ou null | — |  |

| ignorada | não | boolean | false |  |

| motivo_ignorada | não | string ou null | — |  |


### ParametroCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome_parametro | sim | string; maxLength=120; minLength=1 | — |  |

| unidade | não | string; maxLength=30 ou null | — |  |

| valor_minimo | não | number ou string ou null | — |  |

| valor_maximo | não | number ou string ou null | — |  |

| observacao | não | string ou null | — |  |


### ParametroResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| nome_parametro | sim | string; maxLength=120; minLength=1 | — |  |

| unidade | não | string; maxLength=30 ou null | — |  |

| valor_minimo | não | string ou null | — |  |

| valor_maximo | não | string ou null | — |  |

| observacao | não | string ou null | — |  |

| produto_id | sim | string (uuid) | — |  |


### ParametroUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome_parametro | não | string; maxLength=120; minLength=1 ou null | — |  |

| unidade | não | string; maxLength=30 ou null | — |  |

| valor_minimo | não | number ou string ou null | — |  |

| valor_maximo | não | number ou string ou null | — |  |

| observacao | não | string ou null | — |  |


### PerfilResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| nome | sim | string | — |  |

| descricao | sim | string ou null | — |  |


### ProdutoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | sim | string; maxLength=120; minLength=1 | — |  |

| descricao | não | string ou null | — |  |

| ativo | não | boolean | true |  |


### ProdutoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| nome | sim | string | — |  |

| descricao | sim | string ou null | — |  |

| ativo | sim | boolean | — |  |


### ProdutoUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | não | string; maxLength=120; minLength=1 ou null | — |  |

| descricao | não | string ou null | — |  |

| ativo | não | boolean ou null | — |  |


### QualidadeResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| sessao_id | sim | string (uuid) | — |  |

| revisao | sim | integer | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) | — |  |

| intervalo_maximo_s | sim | string | — |  |

| natureza | sim | string | — |  |

| metadados_temporais_invalidos | sim | boolean | — |  |

| cancelada_para_analise | sim | boolean | — |  |

| indicadores | sim | lista de object | — |  |

| codigos_ocorrencias | sim | lista de string | — |  |

| limites | sim | string | — |  |


### ResultadoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| status_calculo | sim | StatusCalculo | — |  |

| volume_coberto_min_ul | sim | string ou null | — |  |

| volume_coberto_max_ul | sim | string ou null | — |  |

| volume_janela_min_ul | sim | string ou null | — |  |

| volume_janela_max_ul | sim | string ou null | — |  |

| duracao_coberta_s | sim | string ou null | — |  |

| duracao_nao_coberta_s | sim | string ou null | — |  |

| percentual_cobertura | sim | string ou null | — |  |

| unidade_volume | sim | string | — |  |

| motivos | sim | lista de string | — |  |

| limitacoes | sim | lista de string | — |  |

| classificacao_risco_etileno | sim | enum: NAO_AVALIADO | — |  |

| motivo_risco | sim | enum: SEM_LIMIAR_VALIDADO | — |  |

| versao_modelo | sim | string | — |  |

| intervalos | sim | lista de IntervaloResponse | — |  |

| massa_kg | sim | string ou null | — |  |

| inicio | sim | string (date-time) ou null | — |  |

| fim | sim | string (date-time) ou null | — |  |

| modo | sim | ModoCalculo ou null | — |  |

| maturacao | sim | string ou null | — |  |

| intervalo_maximo_s | sim | string ou null | — |  |

| corte_aquisicao | sim | string (date-time) ou null | — |  |

| sensor_id | sim | string | — |  |

| sessao_id | sim | string | — |  |

| tabela_referencia | sim | lista de object | — |  |

| cobertura | sim | string ou null | — |  |

| duracao_janela_s | sim | string ou null | — |  |

| duplicatas_descartadas | sim | integer | — |  |

| interpolacao_utilizada | sim | boolean | — |  |

| perfil | sim | string ou null | — |  |

| metodologia | sim | string | — |  |

| fonte | sim | string | — |  |

| referencia | sim | string | — |  |

| data_consulta | sim | string | — |  |

| aplicabilidade | sim | string | — |  |


### SessaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| inicio | sim | string (date-time) | — |  |

| sensor_temperatura_id | sim | string (uuid) | — |  |

| sensor_umidade_id | não | string (uuid) ou null | — |  |

| ambiente_aquisicao | sim | enum: LABORATORIO, TRANSPORTE_REFRIGERADO | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| observacoes | não | string; maxLength=2000 ou null | — |  |


### SessaoFinalizar

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| fim | sim | string (date-time) | — |  |

| motivo | sim | string; maxLength=2000; minLength=1 | — |  |


### SessaoResponse-Input

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| carga_id | sim | string (uuid) | — |  |

| viagem_id | sim | string (uuid) | — |  |

| configuracao_id | sim | string (uuid) | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) ou null | — |  |

| estado | sim | StatusSessao | — |  |

| sensor_temperatura_id | sim | string (uuid) | — |  |

| sensor_umidade_id | sim | string (uuid) ou null | — |  |

| ambiente_aquisicao | sim | string | — |  |

| observacoes | sim | string ou null | — |  |

| configuracao_versao | sim | integer | — |  |

| produto_identificado | sim | string | — |  |

| massa_kg | sim | number ou string | — |  |

| maturacao | sim | MaturacaoCarga | — |  |

| lote_codigo | sim | string | — |  |

| lote_hipotetico | sim | boolean | — |  |

| rastreabilidade | sim | string | — |  |

| origem_sensor | sim | object | — |  |

| criada_por_id | sim | string (uuid) | — |  |

| finalizada_por_id | sim | string (uuid) ou null | — |  |

| motivo_fim | sim | string ou null | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |


### SessaoResponse-Output

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| carga_id | sim | string (uuid) | — |  |

| viagem_id | sim | string (uuid) | — |  |

| configuracao_id | sim | string (uuid) | — |  |

| inicio | sim | string (date-time) | — |  |

| fim | sim | string (date-time) ou null | — |  |

| estado | sim | StatusSessao | — |  |

| sensor_temperatura_id | sim | string (uuid) | — |  |

| sensor_umidade_id | sim | string (uuid) ou null | — |  |

| ambiente_aquisicao | sim | string | — |  |

| observacoes | sim | string ou null | — |  |

| configuracao_versao | sim | integer | — |  |

| produto_identificado | sim | string | — |  |

| massa_kg | sim | string | — |  |

| maturacao | sim | MaturacaoCarga | — |  |

| lote_codigo | sim | string | — |  |

| lote_hipotetico | sim | boolean | — |  |

| rastreabilidade | sim | string | — |  |

| origem_sensor | sim | object | — |  |

| criada_por_id | sim | string (uuid) | — |  |

| finalizada_por_id | sim | string (uuid) ou null | — |  |

| motivo_fim | sim | string ou null | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |


### SincronizacaoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| chave_idempotencia | sim | string (uuid) | — |  |

| origem_dados | não | enum: THINGSPEAK, BANCO | "THINGSPEAK" |  |

| inicio | não | string (date-time) ou null | — |  |

| fim | não | string (date-time) ou null | — |  |

| complementar_encerrada | não | boolean | false |  |

| justificativa | não | string; maxLength=2000; minLength=1 ou null | — |  |

| limite_atraso_s | não | number; exclusiveMinimum=0.0 ou string ou null | — |  |

| max_requisicoes | não | integer; minimum=1.0; maximum=32.0 | 16 |  |


### SincronizacaoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| sessao_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| revisao | sim | integer | — |  |

| chave_idempotencia | sim | string (uuid) | — |  |

| origem_dados | sim | string | — |  |

| estado | sim | string | — |  |

| inicio_janela | sim | string (date-time) | — |  |

| fim_janela | sim | string (date-time) | — |  |

| iniciada_em | sim | string (date-time) | — |  |

| finalizada_em | sim | string (date-time) ou null | — |  |

| expira_em | sim | string (date-time) | — |  |

| complementacao | sim | boolean | — |  |

| justificativa | sim | string ou null | — |  |

| resumo | sim | object | — |  |


### StatusCaixa

enum: REGISTRADA, EM_TRANSITO, ENTREGUE, AVARIADA


### StatusCalculo

enum: ENTRADA_INVALIDA, CONFIGURACAO_INCOMPLETA, SEM_ESTIMATIVA, PARCIAL, COMPLETO_NO_MODELO


### StatusCarga

enum: PLANEJADA, EM_TRANSITO, ENTREGUE, CANCELADA


### StatusSessao

enum: ATIVA, ENCERRADA, CANCELADA


### StatusViagem

enum: PLANEJADA, EM_ANDAMENTO, CONCLUIDA, CANCELADA


### ThingSpeakFeed

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| created_at | sim | string (date-time) | — |  |

| entry_id | sim | integer | — |  |

| fields | não | object | — |  |

| raw | não | object | — |  |


### ThingSpeakMappingResult

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| channel_id | sim | string | — |  |

| feeds_processados | sim | integer | — |  |

| leituras_normalizadas | não | lista de NormalizedThingSpeakReading | — |  |

| ignorados | não | integer | 0 |  |


### ThingSpeakStatusResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| configured | sim | boolean | — |  |

| base_url | sim | string | — |  |

| channel_id | não | string ou null | — |  |

| message | sim | string | — |  |


### ThingSpeakSyncError

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| entry_id | sim | integer | — |  |

| field_name | sim | string | — |  |

| motivo | sim | string | — |  |


### ThingSpeakSyncSummary

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| feeds_recebidos | sim | integer | — |  |

| fields_processados | sim | integer | — |  |

| medicoes_criadas | sim | integer | — |  |

| duplicados | sim | integer | — |  |

| ignorados | sim | integer | — |  |

| erros | não | lista de ThingSpeakSyncError | — |  |


### TipoEmpresa

enum: PRODUTOR, TRANSPORTADORA, CLIENTE


### TokenResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| access_token | sim | string | — |  |

| token_type | não | string | "bearer" |  |

| expires_in | sim | integer | — |  |


### UsuarioCreate

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | sim | string; maxLength=150; minLength=1 | — |  |

| email | sim | string (email); maxLength=255 | — |  |

| senha | sim | string (password); maxLength=128; minLength=12 | — |  |

| perfil_id | sim | string (uuid) | — |  |

| ativo | não | boolean | true |  |


### UsuarioResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| nome | sim | string | — |  |

| email | sim | string | — |  |

| perfil_id | sim | string (uuid) ou null | — |  |

| ativo | sim | boolean | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |


### UsuarioUpdate

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| nome | não | string; maxLength=150; minLength=1 ou null | — |  |

| email | não | string (email); maxLength=255 ou null | — |  |

| senha | não | string (password); maxLength=128; minLength=12 ou null | — |  |

| perfil_id | não | string (uuid) ou null | — |  |

| ativo | não | boolean ou null | — |  |


### ValidationError

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| loc | sim | lista de string ou integer | — |  |

| msg | sim | string | — |  |

| type | sim | string | — |  |


### VeiculoCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| empresa_id | sim | string (uuid) | — |  |

| identificador | sim | string; maxLength=80; minLength=1 | — |  |

| placa | não | string; maxLength=20; minLength=1 ou null | — |  |

| modelo | não | string; maxLength=120 ou null | — |  |

| descricao | não | string ou null | — |  |

| ativo | não | boolean | true |  |


### VeiculoResponse

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| empresa_id | sim | string (uuid) | — |  |

| identificador | sim | string; maxLength=80; minLength=1 | — |  |

| placa | não | string; maxLength=20; minLength=1 ou null | — |  |

| modelo | não | string; maxLength=120 ou null | — |  |

| descricao | não | string ou null | — |  |

| ativo | não | boolean | true |  |


### VeiculoUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| identificador | não | string; maxLength=80; minLength=1 ou null | — |  |

| placa | não | string; maxLength=20; minLength=1 ou null | — |  |

| modelo | não | string; maxLength=120 ou null | — |  |

| descricao | não | string ou null | — |  |

| ativo | não | boolean ou null | — |  |


### ViagemCreate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| transportadora_id | sim | string (uuid) | — |  |

| veiculo_id | sim | string (uuid) | — |  |

| motorista_id | sim | string (uuid) | — |  |

| origem | sim | string; maxLength=255; minLength=1 | — |  |

| destino | sim | string; maxLength=255; minLength=1 | — |  |

| saida_em | sim | string (date-time) | — |  |

| previsao_chegada_em | não | string (date-time) ou null | — |  |

| observacoes | não | string ou null | — |  |


### ViagemResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| created_at | sim | string (date-time) | — |  |

| updated_at | sim | string (date-time) | — |  |

| transportadora_id | sim | string (uuid) | — |  |

| veiculo_id | sim | string (uuid) | — |  |

| motorista_id | sim | string (uuid) | — |  |

| origem | sim | string | — |  |

| destino | sim | string | — |  |

| saida_em | sim | string (date-time) | — |  |

| previsao_chegada_em | sim | string (date-time) ou null | — |  |

| inicio_real | sim | string (date-time) ou null | — |  |

| chegada_em | sim | string (date-time) ou null | — |  |

| status | sim | StatusViagem | — |  |

| observacoes | sim | string ou null | — |  |


### ViagemUpdate

Campos extras rejeitados (additionalProperties=false).

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| veiculo_id | não | string (uuid) ou null | — |  |

| motorista_id | não | string (uuid) ou null | — |  |

| origem | não | string; maxLength=255; minLength=1 ou null | — |  |

| destino | não | string; maxLength=255; minLength=1 ou null | — |  |

| saida_em | não | string (date-time) ou null | — |  |

| previsao_chegada_em | não | string (date-time) ou null | — |  |

| inicio_real | não | string (date-time) ou null | — |  |

| chegada_em | não | string (date-time) ou null | — |  |

| status | não | StatusViagem ou null | — |  |

| observacoes | não | string ou null | — |  |


### VinculoResponse

| Campo | Obrigatório | Tipo/restrições | Padrão | Descrição |

|---|---|---|---|---|

| id | sim | string (uuid) | — |  |

| empresa_id | sim | string (uuid) | — |  |

| usuario_id | sim | string (uuid) | — |  |

| ativo | sim | boolean | — |  |


## 9. Limites do contrato atual

Não há endpoint agregador de dashboard, paginação por cursor, refresh de JWT, CRUD de sensores ou push de estados. Não inferir rotas pelo nome de uma entidade. Snapshots/resultados operacionais possuem campos dict livres: congelar seus formatos em contratos tipados pode ser uma evolução posterior, sem inventar campos agora. A confirmação otimista de hash de contexto em decisão humana ainda não existe. O backend foi qualificado em PostgreSQL 17.11 real: 757 aprovados, zero falhas/skips e 50 corridas na qualificação final. A publicação exige revisão e autorização próprias. Os CRUDs logísticos e as quatro rotas globais ThingSpeak já estão protegidos. Máquina/serviço externo exige uma identidade própria futuramente especificada; não reutilizar a chave do canal como autenticação do backend.
