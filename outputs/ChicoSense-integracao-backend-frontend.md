# ChicoSense — integração operacional do backend com o frontend

24/11/2026. Backend na branch `feature/integracao-operacional-frontend`, criada
da `origin/main` em `a3831c4`. Frontend na branch
`feature-integracao-operacional-backend`, base publicada `f07aa46`.
Implementação validada localmente; posteriormente o usuário autorizou os commits
e a publicação exclusivamente das duas branches de desenvolvimento. Essa
autorização não inclui merge, migration remota ou deploy manual. Nenhuma consulta
ao Supabase, alteração de `.env` ou credencial.

## O que estava bloqueado

1. A interface conhecia sensores apenas pelos snapshots de sessões anteriores:
   uma carga sem histórico não conseguia abrir sua primeira sessão.
2. GESTOR consultava somente suas empresas vinculadas e não podia descobrir
   produtores/clientes para cadastrar cargas legitimamente. Aceitar UUID livre
   ou conceder vínculos artificiais de usuário não resolveria a autorização.
3. Dashboard não tinha totais autorizados no servidor. Qualidade retornava todos
   os intervalos e `revisao=0` não era aceita nas consultas de aquisição.

O usuário aprovou expressamente parceiros comerciais autorizados pelo ADMIN e
os ajustes do frontend necessários para consumir os novos contratos.

## Novos contratos e permissões

| Método e rota | Permissão e comportamento |
|---|---|
| GET `/api/v1/transportadoras/{id}/parceiros` | ADMIN ou GESTOR/OPERADOR com vínculo ativo com a transportadora. DTO mínimo: id, nome, tipo, ativo, aprovado e autorizado_para_novas_cargas. Não expõe documento, usuários ou credenciais. |
| PUT `/api/v1/transportadoras/{id}/parceiros/{empresa_id}` | Somente ADMIN. Body `{ "ativo": true, "justificativa": "Aprovação comercial" }`. `false` revoga sem apagar histórico. |
| GET `/api/v1/cargas/{id}/sensores-disponiveis` | ADMIN/GESTOR/OPERADOR autorizado a operar a transportadora da carga. Exige ambiente; início explícito recomendado. Consulta não reserva nem cria sensores. |
| POST `/api/v1/cargas/{id}/sensores` | Somente ADMIN. Novo dispositivo com 1–2 sensores, vinculados à carga, viagem e veículo atuais. Não atualiza dispositivos existentes. |
| GET `/api/v1/monitoramento/resumo` | Quatro papéis oficiais, somente recursos do escopo ativo. Contagens em uma única instrução SQL, sem buscar todas as páginas pela API. |
| GET `/api/v1/monitoramentos/{id}/qualidade/intervalos` | Mesmo escopo de leitura da sessão/carga, paginado, sem gravações. |

Ausência/JWT inválido permanece 401. Perfil ou escopo negado, 403 genérico;
registro inexistente segue a política anterior. Validações 422 e conflitos 409.
Produtor e cliente são tipos de empresa, não novos papéis. CONSULTA e usuários
com vínculo apenas com produtor/cliente não descobrem dispositivos ou parceiros
da transportadora. Acesso à sessão continua restrito à carga, inclusive numa
viagem compartilhada por várias empresas.

### Aprovação comercial

O catálogo aceita `tipo=PRODUTOR|CLIENTE`, `limit` 1–100 e `offset` >=0.
GESTOR/OPERADOR recebem apenas empresas ativas aprovadas para sua transportadora.
`incluir_historico=true` permite consultar empresas de cargas anteriores, mas
registros sem aprovação retornam `autorizado_para_novas_cargas=false`.
Histórico não concede aprovação para uma nova carga.

ADMIN mantém o alcance administrativo existente: pode selecionar qualquer
produtor/cliente ativo e cadastrar cargas, mesmo antes da aprovação comercial.
O campo `aprovado` informa o vínculo específico com a transportadora; ele não
é confundido com o alcance global do ADMIN.

POST de carga feito por GESTOR/OPERADOR revalida as aprovações do produtor e,
quando informado, do cliente. UUID do cliente não substitui autorização.
A relação aprovada é bloqueada durante a criação para serializar com revogação.
Não se alteram cargas antigas ao revogar. Edição logística existente continua
preservando viagem/produto/produtor/cliente; não é criada troca de titularidade.

PUT repetido reutiliza a relação única transportadora/empresa. Armazena autor do
registro inicial, autor da última alteração, justificativa atual e timestamps.
Essa tabela é estado atual, não uma trilha imutável de todas as justificativas.
Não concede vínculo `EmpresaUsuario`, papel, acesso a frota ou leitura de novas
cargas a produtor/cliente sem os relacionamentos logísticos existentes.

### Sensores e primeira sessão

Exemplo de consulta:

```text
GET /api/v1/cargas/{carga_id}/sensores-disponiveis
    ?ambiente=TRANSPORTE_REFRIGERADO&inicio=2026-11-24T12:00:00Z&limit=21&offset=0
```

A data é apenas exemplo; deve estar dentro da viagem real e não ser futura.
Resultado contém carga, viagem, ambiente, início consultado, total, limit, offset,
sensores e `disponibilidade_revalidada_ao_iniciar=true`. Cada sensor expõe somente
id, identificador, tipo, contexto, unidade e dispositivo_id.

Filtro SQL aplica estado ativo de sensor/dispositivo, tipo/unidade compatíveis,
todos os vínculos logísticos existentes e reservas temporais de sessões.
PROTOTIPO não aparece para transporte refrigerado. Dispositivo sem vínculo só
é candidato para ADMIN em LABORATORIO, preservando a regra anterior de início.
Uma reserva da carga ou sensor em janela conflitante impede nova seleção.
O POST de sessão ainda revalida disponibilidade/conflitos: GET não é uma reserva.

Cadastro administrativo mínimo:

```json
{
  "identificador_dispositivo": "IDENTIFICADOR-REAL-OU-DEMO-EXPLICITO",
  "sensores": [
    {"identificador":"TEMP-1","tipo":"TEMPERATURA","contexto":"AMBIENTE","unidade":"C"},
    {"identificador":"UR-1","tipo":"UMIDADE","contexto":"AMBIENTE","unidade":"%"}
  ]
}
```

No máximo um sensor de cada tipo. Identificadores duplicados retornam conflito;
não se atualiza ou reatribui dispositivo alheio em silêncio. Esse POST não possui
UUID idempotente: após resposta incerta, consultar catálogo antes de nova ação;
repetir o mesmo identificador global não cria dispositivo duplicado.
Não cadastra chave, canal, field ou comando físico. A origem de ingestão deve ser
configurada separadamente pelo fluxo ADMIN já existente de ThingSpeak.
Cadastro de sensor não comprova conexão, ingestão ou funcionamento de hardware.

### Resumo, revisão zero e qualidade

Resumo retorna `consultado_em`, `viagens_total`, `viagens_em_transito`,
`cargas_total`, `cargas_monitoradas`, `sessoes_ativas`, `alertas_abertos`.
Carga monitorada significa declaração registrada, sem garantia de aquisição.
Alertas abertos incluem ABERTO e EM_ANALISE de cargas autorizadas, não alertas
legados sem carga que poderiam revelar informações de outra empresa.
Nenhuma contagem é classificação de risco ou medição de gás.

Leituras, qualidade e intervalos passam a aceitar revisão zero explicitamente:
o snapshot sem aquisição não muda para a revisão mais recente quando chega uma
nova sincronização. Omitir revisão mantém o comportamento anterior de última
revisão consolidada. `incluir_intervalos=false` na qualidade omite as listas,
mantendo indicadores e acrescentando `intervalos_total` em cada fonte.
O padrão continua `true`, preservando clientes antigos.

A nova listagem de intervalos aceita a mesma janela, revisão e G, limit 1–100 e
offset >=0. Retorna metadados, total e intervalos de todas as fontes em ordem
determinística. Os indicadores usam a sequência completa, não somente a página.
**Limite de escala:** reduz tráfego e DOM, mas o cálculo de cobertura ainda lê a
sequência completa no backend. Não se declara memória constante ou processamento
streaming. Nenhum algoritmo científico/de cobertura foi alterado.

## Integração nas telas

- Administração → empresas → vínculos da transportadora → Gerenciar parceiros
  comerciais: ADMIN aprova, reativa ou revoga com justificativa.
- Nova carga: produto mantém catálogo anterior; produtor/cliente vêm do catálogo
  aprovado da transportadora da viagem, sem UUID digitado livremente.
- Carga/Monitoramento → declaração e sessões: ADMIN pode cadastrar sensores.
  No início, informar data/ambiente aciona catálogo atual, inclusive sem histórico;
  paginação incremental e revalidação final mantêm restrições de contexto.
- Dashboard consulta contagens do servidor, com indisponibilidade explícita em
  falha e atualização manual. A tabela de viagens continua delimitada às páginas
  carregadas; ela não é confundida com os indicadores globais autorizados.
- Aquisição pede qualidade compacta, fixa revisão zero e consulta intervalos
  paginados na mesma janela, revisão e G.

O histórico de sessões ainda é consultado no formulário de início para detectar
sessão já aberta e reconciliar tentativas incertas. Não se removeu essa proteção.

## Banco e ordem de publicação

Nova revisão Alembic: **`20261124_0011_parceiros`**, após
`20261028_0010_exaustao_virtual`. Cria somente `parceiros_comerciais`, com FKs,
unicidade por par, check de empresas diferentes e índice transportadora/ativo.
Sem backfill, DELETE, alterações nas tabelas científicas ou migrations antigas.

Antes de liberar tráfego na nova versão, o responsável deverá:

1. Revisar e publicar as branches dos dois repositórios após autorização.
2. Conferir banco de destino, backup e revisão atual. Aplicar a nova migration
   pelo procedimento autorizado do projeto: `alembic upgrade 20261124_0011_parceiros`.
   **Este documento não executa nem autoriza acesso remoto por conta própria.**
3. Atualizar o backend no Render com o código compatível. Subir código sem a
   tabela nova faz as novas operações comerciais falharem; não há fallback aberto.
4. Publicar o frontend em Preview, configurando VITE_API_URL em Preview para a
   API pretendida. Conferir o domínio exato do preview no CORS_ALLOWED_ORIGINS
   do Render, em JSON válido; preservar demais origens necessárias, sem wildcard.
5. ADMIN aprova explicitamente os parceiros de teste. Nenhuma empresa/conta
   existente recebe aprovação ou mudança de papel automaticamente.
6. Executar o roteiro abaixo. Não é necessário unir a main para testar uma branch
   num serviço de teste Render e no Preview Vercel. Nenhum desses serviços foi
   configurado ou atualizado automaticamente nesta tarefa.

## Roteiro para a equipe de frontend

1. ADMIN: conferir empresas/perfis; aprovar produtor/cliente da transportadora.
2. Logística GESTOR: cadastrar viagem, carga e caixas; iniciar viagem/trânsito.
   Parceiro não aprovado, de outra transportadora ou inativo deve ser rejeitado.
3. Declarar massa/maturação/lote explicitamente. ADMIN cadastra ou prepara
   sensores; logística seleciona início/ambiente/sensores e abre a primeira sessão.
4. Abrir aquisição: sem leituras deve aparecer ausência, nunca produção zero.
   Sincronização exige origem realmente configurada, sem inventar amostras.
5. Consultar qualidade/G, páginas e revisão zero. Solicitar estimativa científica
   e avaliação ambiental separadamente; risco de etileno continua NAO_AVALIADO.
6. Registrar decisões justificadas e simulação virtual: solicitar, autorizar,
   iniciar e encerrar em ações humanas separadas; sem hardware.
7. Produtor e cliente CONSULTA: ver somente suas cargas/sessões, inclusive viagem
   compartilhada. Trocar IDs não deve permitir carga alheia nem escrita.
8. Conferir totais autorizados de cada conta, paginação, estados vazios, 401/403,
   recuperação de falha e apresentação em desktop/celular.

## Validação e status

SQLite isolado: **819 aprovados, 12 PostgreSQL não executados, zero falhas**.
Frontend: **321 aprovados**, build e lint sem erros, com avisos anteriores.
Os testes legados afetados agora preparam aprovação ADMIN ou esperam rejeição.
A asserção de JWT cobre 32 rotas de monitoramento em vez de 30; não foi removida.
Testes de migração conferem o novo head sem modificar o histórico anterior.

PostgreSQL portátil 17.11: pacote e executáveis reconferidos, cluster anterior
atestado, loopback 127.0.0.1:35432, credencial de teste via DPAPI sem exibição,
bancos novos descartáveis com travas existentes. Primeiros **12 testes aprovados**;
repetição dos **9 concorrentes aprovada**. Suíte completa real:
**831 aprovados, zero falhas, zero skips, um warning conhecido**, em 362,15 s.
Checagem HTTP/JWT adicional no PostgreSQL: **1 teste aprovado**, cobrindo catálogo,
restrição de CONSULTA, aprovação ADMIN, nova carga, provisionamento, primeira
sessão, bloqueio por reserva, resumo autorizado e intervalos na revisão zero.
Essa checagem adicional é separada dos 831 testes da suíte do repositório.
Não houve banco remoto nem criação de usuário real.

O primeiro executor local foi interrompido antes de rodar testes por restrições
do Windows/captura de processos; o marcador do processo já encerrado foi salvo
como evidência antes da retomada. Não é falha de migration ou regra de negócio.
Uma primeira tentativa completa atingiu o timeout de 600 s do executor e não foi
contada como aprovação. A repetição com log contínuo passou integralmente.
O executor corrigido usou logs próprios e verificou a identidade antes de criar
bancos. O cluster foi encerrado de forma controlada após cada rodada concluída;
bancos, logs e evidências ficaram preservados no diretório descartável.

Evidências locais fora do Git: grupo PostgreSQL e repetição concorrente em
`backend-integracao-e4fbe24119-*.log`, suíte completa em
`backend-integracao-48db1289cb-full-suite.log`; o manifesto da rodada complementar
fica em `work/backend-integration-pg-results.json` no workspace da conversa.

Não é homologação contra Vercel/Render: publicação, CORS do preview e a aplicação
remota da migration permanecem passos do responsável. Os arquivos dos dois
repositórios foram revisados antes dos commits autorizados; as mains permanecem
fora do escopo da publicação.
