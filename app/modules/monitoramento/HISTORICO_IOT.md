# Historico IoT de sessoes — Etapa 4

Este incremento associa aquisicao a sessoes; nao calcula etileno. O motor em
`etileno/` e as regras de criacao/encerramento da Etapa 3 permanecem intactos.

## Origem e reaproveitamento

Reutilizam-se ThingSpeakService.from_settings, ThingSpeakClient._get_json,
ThingSpeakFieldMapper, MedicaoRepository e LeituraExternaRepository. O cliente
existente recebeu somente uma operacao adicional get_feeds_historicos; suas
rotas/metodos antigos conservam seus contratos. Nao existe segundo cliente HTTP.

O mapeamento fieldN e configuravel. No ambiente inspecionado: field1 TEMPERATURA
(C), field2 UMIDADE (%), ambos PROTOTIPO. O codigo nao fixa esses campos. Os testes
usam field4/field7 para demonstrar independencia dos nomes do prototipo.

Na primeira sincronizacao, exige-se exatamente um campo configurado por sensor
da sessao. Tipo/contexto/unidade devem coincidir com o snapshot; referencias
explicitas de carga/viagem, se presentes, devem corresponder a sessao. Mapeamento
por caixa nao e aceito neste incremento. A origem fica fixada em fontes_sessao_iot:
canal, campo, sensor, unidade/contexto e snapshot, sem credencial. Mudancas futuras
da configuracao nao remapeiam sessoes existentes. Nao ha remapeamento implicito.

## Endpoints autenticados

Prefixo `/api/v1/monitoramentos/{sessao_id}`:

- POST /sincronizacoes — execucao explicita com chave UUID idempotente.
- GET /sincronizacoes — estado e tentativas/revisoes paginadas.
- GET /leituras — historico paginado, filtro tipo, periodo e revisao.
- GET /qualidade — indicadores temporais; intervalo_maximo_s obrigatorio.

Escrita usa ADMIN/GESTOR/OPERADOR com o escopo de transportadora da Etapa 3;
CONSULTA pode ler nesse escopo. Dados de outra empresa nao sao acessiveis.
As rotas antigas do ThingSpeak continuam registradas e nao foram redirecionadas.

POST aceita origem_dados THINGSPEAK (padrao) ou BANCO, inicio/fim opcionais,
chave_idempotencia, limite_atraso_s opcional, max_requisicoes de 1 a 32 (padrao
tecnico 16), complementar_encerrada e justificativa. Sem endpoints redundantes de
captura ou configuracao de credenciais. BANCO consulta apenas Medicao/LeituraExterna
compativeis com o vinculo de origem, sem fazer chamada HTTP.

CONCLUIDA significa que a consulta/incorporacao terminou sem sinal de falha ou
truncamento, nao que o transporte teve medicao continua. PARCIAL e FALHA ficam
persistidas e auditadas. HTTP 200 pode conter FALHA: consulte o estado, nao apenas
o codigo HTTP. Repeticao ainda em execucao retorna 202; conteudo divergente com
mesma chave retorna 409. GET nao coleta ou modifica dados.

## Tempo e janela

created_at do feed e preservado como horario registrado na origem e normalizado
UTC. Nao prova um relogio fisico de aquisicao independente do sensor; sem outro
campo documentado, esse e o timestamp disponivel no ThingSpeak.

Registro guarda medida_em, timestamp_origem, recebida_em e processada_em distintos.
HTTP: recebida_em e o instante local apos receber a resposta; processada_em marca
a incorporacao. BANCO: recebida_em=None porque created_at de Medicao e data de
persistencia, nao evidencia de recebimento fisico. Nesse modo, timestamp_origem
representa o instante persistido em UTC; a grafia/offset original de dados legados
pode ser desconhecida. Nao se inventam esses metadados.

Amostras sao selecionadas em [inicio,fim], incluindo a amostra de fechamento.
Isso prepara pares [t_i,t_i+1) compativeis com o motor. Uma leitura final pode ser
compartilhada como extremo com a proxima sessao, sem duplicar a medicao global.
Sessao ativa tem corte capturado ao solicitar a sincronizacao; nao se usa horario
de consulta para reescrever medida_em. Consultas por revisao em sessao ativa usam
o corte da tentativa escolhida. Sessao encerrada sempre respeita seu fim atual.
Periodos solicitados fora da sessao sao rejeitados; leituras externas fora da
janela sao descartadas e contabilizadas, sem alterar a janela.

As consultas ao provedor usam start/end/timezone=UTC, sem average/round/timescale.
O limite documentado de 8000 feeds por resposta e tratado por subdivisao temporal
limitada. Consultas sobrepostas nas bordas sao deduplicadas. Saturacao sem divisao
possivel ou esgotamento do limite de requisicoes fica como aquisicao PARCIAL,
nunca como historico completo garantido. Nova chave/periodo pode retomar lacunas.
Fonte: https://www.mathworks.com/help/thingspeak/readdata.html.

## Complementacao tardia e revisoes

ATIVA permite captura comum. ENCERRADA exige complementar_encerrada=true,
justificativa e ADMIN/GESTOR. CANCELADA permite consulta, mas nao nova incorporacao.
O estado/janela e revalidado depois da chamada HTTP; encerramento durante consulta
impede incorporacao ordinaria e exige outra operacao explicita de complemento.

Esta e a alteracao de politica autorizada na Etapa 4: encerra-se a aquisicao
ordinaria, mas permite-se complemento auditado dentro da janela original. Nao se
reabre ou alonga a sessao. O servico de ciclo de vida da Etapa 3 nao foi modificado.

Cada tentativa tem revisao sequencial, ator, periodo, chave/assinatura, controles
operacionais, estado e resumo. Registros incorporados referenciam essa tentativa.
Repetir chave/payload/autor retorna a mesma tentativa sem nova consulta ou leitura.
Outra chave inicia nova revisao e deduplica o que ja existe. Tentativa em execucao
reserva a sessao; prazo tecnico permite recuperacao explicita de tentativa perdida,
sem que um trabalhador antigo grave depois de ser interrompido.

apos_encerramento identifica incorporacao posterior. tardia classifica recebimento
somente quando conhecido: recepcao apos o fim da sessao ou latencia acima de um
limite_atraso_s explicitamente informado. Sem evidencia, tardia=None. Recuperacao
local apos o fim nao inventa recebimento tardio.

Medicao e reaproveitada; LeituraExterna continua deduplicando origem/canal/entry/campo.
Novas Medicao guardam o valor do sensor; o contexto logistico canonico fica no
vinculo RegistroSessaoIoT → sessao. Nao se reatribui carga/viagem em uma Medicao
legada, e vinculo logistico antigo contraditorio e tratado como conflito.

Registros ja incorporados nao sao sobrescritos. Mesma identidade com valor/horario
contraditorio gera ocorrencia, bloqueando os pontos afetados nas consultas de
qualidade/latest. Consulta de revisao anterior mantem os valores anteriores. Nao
ha resolucao automatica de correcoes da origem: ela exigira procedimento auditado.

Na Etapa 5, analises deverao fixar revisao, janela efetiva, IDs/valores/parametros
e hash proprio. Acrescentar historico nao deve recalcular ou atualizar analises
existentes implicitamente. Mudancas posteriores de estado/fim da sessao tambem
precisam ser registradas no snapshot da analise; revisao de aquisicao sozinha nao
substitui um snapshot completo dos seus inputs.

## Qualidade sem inferencia cientifica

Numeros invalidos, nulos, umidade fora de 0–100% ou valores nao representaveis em
NUMERIC(12,4) viram marcadores invalidos, nunca zero. Leituras sem ID/horario valido
sao ocorrencias, nao medicoes fabricadas. Falhas por campo usam savepoints e nao
precisam descartar os campos validos da mesma resposta.

Historico ordena por medida_em/id. Campos fora_de_ordem/tardia registram a aquisicao,
sem alterar os timestamps. Pontos iguais no mesmo instante nao duplicam exposicao;
valores conflitantes nesse instante ou conflitos da origem formam barreiras.

GET qualidade exige G operacional finito e positivo; nao ha valor padrao cientifico.
Dois extremos utilizaveis e intervalo <=G geram cobertura temporal; gap >G e todo
nao coberto. Nao se preenchem bordas nem se prolonga a ultima temperatura. Nenhuma
leitura implica tempo coberto zero conhecido, sem afirmar volume produzido zero.
Timestamp nao localizavel torna percentual inconclusivo (None), com a ocorrencia.

Indicadores medem aquisicao ambiental, sem q(T), interpolacao de taxas, volumes,
concentracao ou risco. Temperatura intermediaria pode ser valida ambientalmente
e ainda nao possuir taxa no modo restrito do motor. A validacao cientifica de
dominio pertence a Etapa 5. Umidade nao e proxy de etileno.

## Persistencia e operacao

Migration 20261028_0007_historico_iot depende de 20261028_0006_monitoramento:
fontes_sessao_iot, sincronizacoes_iot, registros_sessao_iot e ocorrencias_iot.
As tabelas antigas e snapshots de sessoes nao sao reescritos. A cadeia antiga nao
foi alterada. Downgrade remove somente as quatro tabelas novas e seus dados.

Reservar/finalizar usa os bloqueios/escopo da Etapa 3. HTTP ocorre fora de bloqueios
de carga/sessao. Estado e permissoes sao revalidados ao finalizar. FKs compostas,
chaves unicas e um indice parcial protegem os vinculos e a execucao por sessao.
Erros de integridade nao sao contados genericamente como duplicidade.

Nenhuma migration foi aplicada remotamente; testes usam SQLite em memoria, mocks
HTTP e SQL PostgreSQL offline. Concorrencia PostgreSQL real, calibracao e aquisicao
fisica do canal permanecem pendentes. Os endpoints sao manuais, nao um scheduler.
A protecao de logs HTTPX na chamada historica mascara api_key; nenhuma credencial
esta presente nas tabelas ou respostas deste incremento.
