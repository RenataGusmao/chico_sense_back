# Leitura separada por produtor e cliente

Preparação local de 24/11/2026, branch `feature/escopo-produtor-cliente`.
Base: `816bc4b728c711065cf01567c3bac491210e2277`. Nenhuma escrita de produção,
criação de conta no Supabase, migration ou publicação foi executada nesta etapa.

## Regra de acesso

Os papéis permanecem ADMIN, GESTOR, OPERADOR e CONSULTA. PRODUTOR, CLIENTE e
TRANSPORTADORA continuam sendo tipos de empresa. Não há aliases, papéis novos
ou vínculo artificial do produtor/cliente à transportadora.

| Conta planejada | Papel | Vínculo empresarial | Escopo |
|---|---|---|---|
| Logística de demonstração | GESTOR | Transportadora de demonstração | Operações e leitura de suas viagens/cargas |
| Produtor de demonstração | CONSULTA | Somente seu produtor | Leitura das cargas cujo produtor_id corresponde a vínculo ativo |
| Cliente de demonstração | CONSULTA | Somente seu cliente | Leitura das cargas cujo cliente_id corresponde a vínculo ativo |

Uma viagem pode ser consultada por produtor/cliente quando contém ao menos uma
carga autorizada. O DTO de viagem permanece o mesmo (trajeto, horários e IDs
logísticos); ele não inclui relação completa de cargas. A listagem de cargas e
de sessões dessa viagem é filtrada por carga **antes** da paginação.
Ter uma carga numa viagem não concede acesso às outras cargas da mesma viagem.

A consulta ao histórico, qualidade, análise, configuração/avaliação preventiva,
alertas, evidências, decisões e intervenções acompanha o escopo da **carga da
sessão**, inclusive ao informar IDs diretamente. O índice de sessões da viagem
não permite descobrir sessões de cargas alheias.

Leitura exige usuário, vínculo, empresa vinculada e transportadora ativos.
ADMIN mantém sua abrangência e recuperação administrativa existentes. Múltiplos
vínculos ativos produzem a união dos escopos legítimos; um ID enviado pelo cliente
não é um vínculo. O parâmetro empresa_id de GET /viagens continua significando
transportadora, e não produtor/cliente. Ele só filtra viagens já autorizadas.

## Escrita e dados compartilhados

Produtor/cliente não passam a administrar a viagem por possuírem carga nela.
Escrita continua exigindo papel apropriado **e vínculo com a transportadora**,
mesmo quando o usuário da empresa produtora/cliente possui GESTOR.
Autorizações e ações da exaustão virtual mantêm essa exigência; leitores recebem
acoes_permitidas vazio. Não há mudança no motor científico ou ação física.

Frota e motoristas continuam restritos à transportadora; ler o ID desses recursos
no DTO de uma viagem autorizada não permite consultar seus detalhes privados.
Dados cadastrais da transportadora/outras empresas também não são liberados por
esse relacionamento. ThingSpeak global continua exclusivo ADMIN.
O catálogo de produtos continua global para os quatro papéis, conforme contrato
anterior; ele não é uma coleção privada de cada produtor.

Inexistente mantém 404; recurso existente fora do escopo retorna 403 genérico.
Usuário inativo/token ausente ou inválido continua sujeito a 401. ADMIN conserva
404 ao filtrar por empresa inexistente. Nenhum payload ou endpoint foi adicionado.

Essa política vale também para vínculos de produtor/cliente que já existam no
banco quando o código for publicado: passarão a consultar suas próprias cargas.
Isso precisa ser revisado antes da publicação; não é uma exceção oculta exclusiva
das contas DEMO. A publicação não cria, promove ou vincula usuários por si só.

## Implementação

- [EscopoLogistico](../../app/modules/logistica/escopo.py): subqueries de vínculos
  ativos tipados, predicados SQL para cargas/viagens e limites de operação.
- [LogisticaAccess](../../app/modules/logistica/access.py): detalhes, listas,
  filtros e paginação conforme escopo.
- [MonitoramentoService](../../app/modules/monitoramento/service.py) e
  [repository](../../app/repositories/monitoramento.py): autorização por carga
  em consultas de sessão e filtragem de sessões por viagem.
- [ExaustaoSimuladaService](../../app/modules/monitoramento/exaustao_service.py):
  preserva a fronteira operacional da transportadora, inclusive nas ações
  administrativas e nas permissões projetadas pela consulta.
- [Testes](../../tests/test_escopo_produtor_cliente.py): viagens compartilhadas,
  relações produtor/cliente diferentes, listagem/paginação, troca de IDs, vínculos
  revogados, empresas inativas/tipos incompatíveis, frota, escrita e recursos
  científicos/preventivos da carga. Também testa que GESTOR de produtor não
  autoriza intervenções virtuais e que o 404 legado de filtro ADMIN é preservado.

O OpenAPI mantém os mesmos contratos. O histórico da auditoria anterior continua
descrevendo o commit auditado e não foi reescrito para representar esta mudança.

## Preparação da ingestão de demonstração

A ingestão real depende primeiro de revisão/publicação desta autorização no
backend e verificação do processo ativo. Criar contas com o backend antigo não
permite acesso separado; adicionar vínculo de transportadora contornaria o
requisito expresso pelo usuário e não faz parte do plano.

Plano inicial proposto, ainda não executado:

- 1 transportadora exclusiva DEMO, 2 produtores e 2 clientes exclusivos DEMO.
- 3 contas: logística GESTOR, produtor A CONSULTA e cliente A CONSULTA.
  Os produtores/clientes B são dados de controle, sem novas contas de acesso.
- 5 viagens com 2 cargas cada, totalizando 10 cargas/10 sessões.
- 20 sensores sintéticos; 500 amostras por sensor; **10.000 leituras de entrada**.
- Cargas alternam produtores/clientes para que as visões sejam diferentes:
  logística 10 cargas; produtor A 5; cliente A 6, com interseção legítima.
- Prefixo DEMO, lote_hipotetico=true, justificativas de geração e fonte
  DEMO_SINTETICO. Não apresentar dados gerados como aquisição real ThingSpeak,
  calibração, gás medido ou validação experimental de Tommy Atkins.
- Chaves/IDs exclusivos da execução, manifestos para identificar o lote e
  abortar em colisão. Nunca atualizar usuário real ou reaproveitar conta existente.
- Senhas exclusivas a definir/gerar no procedimento de criação, com hash pelo
  serviço existente; nenhuma senha foi escrita nesta documentação.
- Conferir projeto Supabase, permissões, migrations aplicadas e destino exato
  antes de qualquer escrita; nenhum fallback implícito de teste para DATABASE_URL.
- Validar três logins e escopos antes de ampliar o lote. Avaliar capacidade e
  espaço; este conjunto é demonstração funcional, não teste de estresse em produção.
- Registrar contagens, tempos e IDs. Qualquer remoção futura exige delimitação
  pelo manifesto e autorização; não há limpeza ampla/TRUNCATE no banco real.

O total de linhas de banco será maior que o número de leituras, devido a medições,
proveniência, incorporações, snapshots e auditoria. A geração de análises/alertas
deve usar os serviços existentes. Não criar decisões humanas ou intervenções
executadas como se fossem atos reais da equipe.

## Limites de validação

Os testes desta preparação usam SQLite em memória, JWT real e aquisição mockada.
Não fazem conexões ao Supabase. PostgreSQL opcional/concorrência real só podem
ser executados em banco descartável com as travas de tests/POSTGRESQL.md; os skips
não contam como aprovação. Não houve nova medição de desempenho do banco real.

Validação final local: **792 aprovados, 12 skips PostgreSQL, zero falhas e um
warning conhecido** (BlockingPortal), em 201,58 s. São 27 casos novos de escopo,
além dos 765 aprovados anteriormente. Os contratos OpenAPI permanecem idênticos:
50 caminhos, 76 operações; sem mudança de schemas, modelos ou migrations.
Os 12 skips não repetem a qualificação PostgreSQL real histórica.
