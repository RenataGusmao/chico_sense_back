# Cadastro e sessoes de monitoramento — Etapa 3

Este modulo prepara os vinculos de carga/viagem/sensor e as janelas temporais.
Nao consulta ThingSpeak, nao associa medicoes e nao executa o motor `etileno`.

## Dados adicionais sem backfill do legado

A carga logistica existente continua sendo a unica entidade Carga. Seus IDs,
viagem, produto cadastrado e identificacao sao reutilizados. O perfil 1:1
`cargas_monitoramento` guarda somente dados novos: massa liquida kg, maturacao,
lote hipotetico ou real explicitamente declarado e rastreabilidade. Nenhuma
carga anterior recebe massa, maturacao ou lote inventados.

`produto_identificado=MANGA_TOMMY_ATKINS` e uma declaracao explicita do operador
sobre a carga. Nao se deduz cultivar de `Produto.nome`, que pode ser generico,
e nao se renomeia o produto compartilhado do catalogo. Essa declaracao deve ser
conferida pelo responsavel; a API nao certifica identidade botanica da fruta.

Massa exige Decimal finito, positivo e compativel com NUMERIC(12,4): maximo
99999999.9999 kg, minimo representavel 0.0001 kg. Esse limite de armazenamento
nao e parametro cientifico. Maturacao e descritiva: VERDE_MADURA,
EM_AMADURECIMENTO, MADURA, MISTA ou DESCONHECIDA. Omissao numa nova declaracao
usa DESCONHECIDA; cargas antigas continuam sem perfil. Nao existe fator de
correcao matematica por maturacao.

PUT de perfil e substituicao completa. Repeticao igual nao altera versao/auditoria;
alteracao incrementa versao e registra antes/depois/autor. Perfil nao pode mudar
com sessao ativa nem apos encerramento da carga/viagem. Cada sessao guarda snapshot,
portanto edicoes posteriores nao reescrevem o historico.

## Janela e conflitos

Abertura exige viagem EM_ANDAMENTO, carga EM_TRANSITO, produto cadastrado ativo e
inicio efetivo explicito, com timezone, nao futuro e >= inicio_real da viagem.
A data de cadastro nao determina o inicio. Sessao nasce ATIVA e reserva [inicio,+infinito).
Encerramento/cancelamento exige fim > inicio, nao futuro, motivo e usuario autorizado;
se existir chegada real, fim nao pode excede-la.

Estados terminais ENCERRADA e CANCELADA sao imutaveis. Repetir a mesma finalizacao
retorna o estado existente; mudar horario/motivo ou tentar outra transicao retorna 409.
A janela historica cancelada permanece reservada, mas nao representa dados aptos
para futura analise automatica. Uma nova janela pode comecar exatamente no fim da
anterior. Nao ha reabertura ou endpoint de associacao de medicoes nesta etapa.

Uma carga e um sensor podem integrar apenas uma sessao ativa. Pares de sensores
sao bloqueados em ordem estavel; a viagem/carga tambem recebem SELECT FOR UPDATE.
A verificacao de conflito considera historico encerrado/cancelado, sem sobreposicao.
Indices unicos parciais garantem exclusividade ativa no banco; FKs compostas
impedem associar sessao a outra viagem ou ao perfil de outra carga.

Os dados precisam de sensor de temperatura existente/ativo, tipo e unidade
compativeis. Umidade e opcional. Dispositivo deve estar ativo e seus vinculos
logisticos, quando presentes, precisam corresponder a carga/viagem/veiculo.
Dispositivo totalmente sem vinculo so e permitido a ADMIN em LABORATORIO.
PROTOTIPO nao e aceito como origem TRANSPORTE_REFRIGERADO. O snapshot de origem
identifica os sensores registrados e contexto, sem afirmar mapeamento ThingSpeak.

## Autenticacao e idempotencia

Todas as rotas novas exigem JWT valido e usuario ativo. Escrita: ADMIN ou
GESTOR/OPERADOR com vinculo ativo a transportadora. Leitura: esses perfis e
CONSULTA, com o mesmo escopo. ADMIN pode consultar sem vinculo; escrita exige
transportadora ativa. Produtor/cliente sem vinculo a transportadora nao recebe
acesso automaticamente. Rotas legadas conservam seus contratos atuais.

Criacao usa chave UUID idempotente por usuario. Mesmo usuario/chave/payload
normalizado retorna 200 com sessao existente, inclusive se ja finalizada; novo
registro retorna 201. Payload diferente com a mesma chave retorna 409.
A assinatura inclui carga, inicio normalizado UTC, sensores, ambiente e observacoes.
Revalidar permissao continua obrigatorio em repeticoes. PUT e finalizacao sao
idempotentes pelos dados/estado e nao geram auditoria duplicada.

Cada operacao de escrita possui um commit; falhas fazem rollback. Repositorio nao
faz commit. Eventos e alteracoes sao gravados na mesma transacao. A auditoria
possui configuracao, sessao opcional, ator autenticado, tipo, instante e dados.

## Endpoints (prefixo /api/v1)

- PUT /cargas/{carga_id}/monitoramento — registrar/substituir perfil (200).
- GET /cargas/{carga_id}/monitoramento — consultar perfil (200 ou 404).
- POST /cargas/{carga_id}/monitoramentos — abrir sessao (201, repeticao 200).
- GET /cargas/{carga_id}/monitoramentos — listar por carga, limit/offset.
- GET /viagens/{viagem_id}/monitoramentos — listar por viagem, limit/offset.
- GET /monitoramentos/{sessao_id} — consultar snapshot e estado.
- POST /monitoramentos/{sessao_id}/encerrar — finalizar com fim/motivo (200).
- POST /monitoramentos/{sessao_id}/cancelar — cancelar com fim/motivo (200).

Erros documentados no OpenAPI: 401 autenticacao, 403 permissao, 404 inexistente,
409 conflito e 422 validacao. Listas tem limite maximo 100 e ordenacao inicio/id.
Nenhuma rota expoe campo de calculo, risco, alerta ou exaustao.

## Migration e limites operacionais

20261028_0006_monitoramento depende de 20261007_0005_logistica. Cria tres tabelas
e indice unico de suporte em cargas(id,viagem_id). Nao altera colunas de produtos,
cargas ou medicoes, nem preenche registros antigos. Downgrade descarta somente
as novas tabelas e o indice de suporte, incluindo seus dados; nao e executado
automaticamente. Confirmar a revisao efetiva do Supabase antes de futuro rollout.

A migration foi testada em SQLite em memoria e compilada offline para PostgreSQL.
Validacao de concorrencia real sob PostgreSQL continua necessaria: SQLite nao
executa SELECT FOR UPDATE. Nao usar o ambiente remoto para esses testes.

As rotas legadas nao foram refatoradas ou protegidas nesta etapa. Mudancas de
estado de viagem/carga por esses contratos nao encerram sessoes automaticamente.
Se dados legados contradisserem uma sessao, a integracao posterior precisara de
procedimento auditado; esta entrega nao altera historico silenciosamente.
Tambem nao ha bloqueio de escrita SQL administrativa direta ou trigger de
imutabilidade: as regras historicas sao garantidas nos novos casos de uso, com
FKs/checks/indices no banco como defesa complementar.

Antes da ingestao, definir vinculo temporal de medicoes, validacao de janela e
estado em cada associacao, importacao tardia auditada, captura incremental e G
operacional. Sessoes terminais nao tem via de associacao de medicoes nesta etapa.
O motor matematico da Etapa 2 permanece isolado e inalterado.
