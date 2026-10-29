# ChicoSense — especificação do modelo científico de produção potencial de etileno

Versão documental: 1.0 — fundamentação de referência da implementação.
Na especificação, PONTOS corresponde a MODO_RESTRITO e LINEAR a MODO_EXPLORATORIO.
Os nomes de campos da API estão nos contratos, não devem ser inferidos das notações matemáticas.
Decisões efetivamente implementadas: [README do motor](../../app/modules/monitoramento/etileno/README.md).
Data: 23/10/2026.
Branch conferida: `feature/monitoramento-etileno-manga`.
Commit do backend: `acf00589e701452d8bfee6117f1dc173da062d0b`.
Origem: diagnóstico e especificação científica de 23/10/2026, preservados no workspace histórico.

**Natureza:** especificação matemática determinística apoiada em referências gerais de manga. Não é um modelo validado de produção da cultivar Tommy Atkins. O histórico de decisões abaixo foi preservado como fundamentação; execução atual e contratos estão documentados no README do motor e na API.

## 1. Objetivo e escopo

Definir uma estimativa reproduzível de produção potencial de etileno a partir da massa líquida da fruta e de uma série temporal de temperatura, com faixas de referência e cobertura temporal explícitas.

O cenário é uma carga hipotética de manga Tommy Atkins, com leituras reais. Registrar o local real da medição: dados de laboratório não se tornam dados de caminhão refrigerado por associação a uma carga hipotética.

O cálculo é um cenário de referência condicionado às hipóteses declaradas. Não mede etileno, não determina concentração, não prevê dano, maturação ou vida útil e não calcula remoção por ventilação. Não utiliza IA ou aprendizado de máquina.

| Responsabilidade independente | Entrada e saída |
|---|---|
| Estimativa potencial | Temperatura, massa e tempo → faixa em µL, cobertura e limitações |
| Descrição ambiental | Temperatura, umidade e tempo → histórico, distribuição temporal e desvios de referência identificada |
| Classificação de risco | Regras justificadas e validadas → classificação operacional, quando houver base aplicável |

Uma faixa de produção potencial não autoriza chamar a condição de risco baixo, médio ou alto. A primeira versão retorna `NAO_AVALIADO` para risco por etileno.

## 2. Fundamentação científica

Referência efetivamente consultada nesta etapa:

**Kader, A. A. Mango. UC Davis Postharvest Research and Extension Center. Atualização da ficha: fevereiro de 1997. Acesso: 23/10/2026.** [Ficha original](https://postharvest.ucdavis.edu/produce-facts-sheets/mango).

A ficha publica taxas gerais de produção de etileno nos quatro pontos da seção 3. Informa temperatura recomendada de 13 °C para manga verde-madura e 10 °C para parcialmente madura/madura, e umidade relativa de 90–95%. Reconhece dependência de cultivar, maturação e exposição nos danos pelo frio. Essas recomendações são gerais, não limites universais de dano ou regras temporais para Tommy Atkins. A data de atualização da ficha difere da atualização geral do site.

A página não identifica os extremos das taxas como percentis ou intervalo de confiança, não fornece estratificação suficiente por cultivar/maturação e não apresenta a base experimental detalhada necessária para calibrar este projeto. Sua própria seção de referências não lista estudos para reconstrução da tabela.

**Conclusão:** os valores são referências publicadas, não parâmetros experimentalmente validados para nossa carga. A soma dos extremos também não constitui limites garantidos da produção real.

Não derivar regras de risco de doses de etileno aplicadas para amadurecimento: concentração exógena e produção endógena por massa/tempo são grandezas distintas. A bibliografia mencionada no diagnóstico continua como material para aprofundamento; não foram extraídas dela novas constantes nesta etapa.

## 3. Parâmetros e fontes

### 3.1 Tabela publicada

Origem: seção “Rates of Ethylene Production” da [UC Davis](https://postharvest.ucdavis.edu/produce-facts-sheets/mango). Atribuição: Adel A. Kader; UC Davis PREC; direitos da ficha pertencem à University of California.

| Temperatura (°C) | q_min (µL de C₂H₄/kg/h) | q_max (µL de C₂H₄/kg/h) |
|---|---:|---:|
| 10 | 0,1 | 0,5 |
| 13 | 0,2 | 1,0 |
| 15 | 0,3 | 4,0 |
| 20 | 0,5 | 8,0 |

Não confundir com as taxas respiratórias em mL de CO₂/kg/h presentes na mesma página.

### 3.2 Natureza dos parâmetros

| Elemento | Natureza | Situação |
|---|---|---|
| Quatro pares de taxas | Referência bibliográfica geral | Confirmados na fonte; adequação à cultivar pendente |
| Massa líquida em kg | Dado cadastral | Obrigatória, sem valor padrão |
| Temperatura e horário | Dado observado | Origem/unidade/contexto verificáveis |
| Umidade | Dado ambiental independente | Não integra q nem corrige o cálculo |
| Maturação | Informação da carga | Sem fator quantitativo justificável nesta fonte |
| Temperatura inicial mantida no intervalo | Hipótese numérica | Regra desta especificação, sem validação biológica |
| Interpolação linear das taxas | Hipótese matemática opcional | Não fornecida pela UC Davis; identificação obrigatória |
| Temperatura do ar como proxy da fruta | Hipótese de aplicação | Limitação obrigatória, sem correção térmica inventada |
| G: intervalo máximo entre amostras | Política de qualidade operacional | Obrigatório; valor real ainda a definir |
| Limiares baixo/médio/alto por volume | Regra de risco | Não disponíveis; não criar |

### 3.3 Dois modos de taxa, sem ativação implícita

**Base: `UC_DAVIS_PONTOS_V1`.** Domínio de q: conjunto discreto `{10,13,15,20}` °C. Não interpola. Uma temperatura de 12 °C ou 13,1 °C não tem taxa neste modo, embora esteja entre o menor e o maior ponto. Isso limita sua utilidade com sensor real, mas evita atribuir à fonte uma curva não publicada.

**Exploratório: `UC_DAVIS_LINEAR_EXPLORATORIO_V1`.** Domínio computacional: `[10,20]` °C, inclusive, com interpolação linear entre pontos adjacentes. Exige escolha explícita e registro da hipótese no resultado. A faixa computacional não equivale a faixa segura de conservação ou domínio biológico validado.

Para pontos adjacentes T_a e T_b, e cada limite k em `{min,max}`:

`α = (T − T_a)/(T_b − T_a)`

`q_k(T) = q_k(T_a) + α × [q_k(T_b) − q_k(T_a)]`, para `T_a ≤ T ≤ T_b`.

Nos pontos publicados, ambos os modos retornam exatamente as mesmas taxas. Não arredondar a leitura para o ponto mais próximo, usar tolerância oculta, média entre extremos, Q10 ou fator de maturação. Precisão declarada do sensor não justifica alterar silenciosamente seu valor.

Fora de `[10,20]`, nenhum modo extrapola ou fixa q no extremo. Alternativa conservadora: não estimar o intervalo e registrar lacuna de aplicabilidade. “Conservadora” significa limitar a conclusão, não garantir limite superior do gás real. Um envelope entre pontos vizinhos também exigiria hipótese sobre o comportamento entre eles; não será adotado como fato científico.

## 4. Modelo matemático

### 4.1 Variáveis, unidades e conversões

| Símbolo | Significado | Unidade/regra |
|---|---|---|
| W = [a,b) | Janela solicitada | Instantes absolutos; b > a |
| M | Massa líquida total de manga | kg, finita e positiva |
| t_i | Horário de medição, não recebimento | Timezone obrigatório; normalização UTC |
| T_i | Temperatura selecionada | °C, finita |
| q_min/q_max | Limites da taxa de referência | µL/kg/h |
| Δt_i | Duração elegível | h = segundos decorridos/3600 |
| V_min/V_max | Soma dos intervalos elegíveis | µL |
| D_W | Duração da janela | segundos |
| D_c | Duração com contribuição calculável | segundos |
| D_n | Duração sem contribuição | D_W − D_c |

Conversões só com unidade declarada: kg = g/1000; kg = toneladas métricas × 1000; °C = (°F−32)×5/9; °C = K−273,15. Em saídas, mL = µL/1000 e L = µL/1.000.000. Não converter caixas/unidades em massa sem informação verificável. Massa é de fruta, sem embalagem/pallet.

Usar decimais finitos; booleanos não são números aceitos. Converter timestamps para UTC antes de subtrair e preservar offset original para auditoria. Não arredondar temperatura antes de consultar o domínio. Duração é tempo decorrido, inclusive em mudança de fuso, sem subtrair horários locais ingênuos.

Futura implementação: aritmética decimal com precisão de trabalho de pelo menos 28 dígitos; sem quantização por intervalo. Saídas podem usar seis casas em µL com ROUND_HALF_EVEN, arredondando só as somas finais e preservando entradas. Se um positivo arredondar para zero, apresentar “abaixo da resolução de apresentação”; zero exibido não significa ausência de gás. Seis casas não representam precisão científica.

### 4.2 Construção dos intervalos

Política V1: aquisição de pontos incluindo ambas as bordas da janela, integração em intervalos semiabertos e nenhuma extensão da última leitura.

1. Selecionar um único sensor de temperatura e uma sessão/carga/contexto explícitos. Não calcular média nem concatenar sensores sem outro perfil.
2. Validar massa, janela, modo e G; G deve ser finito, positivo e em segundos. Sem G configurado, não executar. Não há G padrão científico.
3. Selecionar observações com `a ≤ t ≤ b`. A amostra em b pode encerrar o último intervalo, sem iniciar exposição dentro de W. V1 não usa amostra anterior a a ou posterior a b para preencher bordas.
4. Ordenar por medição, deduplicar e resolver conflitos pela seção 5. Preservar marcadores inválidos ou fora do domínio com horário conhecido; não removê-los para unir pontos dos dois lados.
5. Para horários consecutivos distintos, formar `I_i = [t_i,t_{i+1})`. Ambos os extremos precisam de temperatura válida no modo escolhido, mesmo que só T_i determine a contribuição. Essa verificação é política de qualidade, não regra da UC Davis.
6. Exigir `0 < t_{i+1}−t_i ≤ G`. Igualdade com G é aceita. Se exceder G, rejeitar o par inteiro; não preencher automaticamente seus primeiros G segundos.
7. No par elegível, adotar `T(t) = T_i`. A retenção à esquerda é aproximação, não medição contínua. Não interpolar temperatura no tempo na V1. A interpolação opcional da seção 3 é de taxa em função de temperatura, uma operação distinta.
8. `[a,t_primeira)` e `[t_ultima,b)` ficam descobertos quando positivos. Uma leitura nunca determina intervalo elegível. Sem leitura, não há produção estimável.

Uma leitura fora do domínio invalida pares adjacentes, por impedir a verificação dos extremos. Isso também vale no fim da janela. A escolha perde cobertura deliberadamente, evitando reconstruir exposição não observada. Não garante que temperatura permaneceu constante ou dentro do domínio entre dois pontos aceitos.

### 4.3 Integral discreta e cobertura

E é o conjunto de intervalos elegíveis:

`Δt_i_h = (t_{i+1} − t_i)_segundos/3600`

`v_i_min/max = q_min/max(T_i) × M × Δt_i_h`

`V_min = Σ_(i∈E) v_i_min`; `V_max = Σ_(i∈E) v_i_max`.

Dimensão: `(µL/kg/h) × kg × h = µL`.

O contrato de resultado separa:

- `volume_coberto_min_ul`, `volume_coberto_max_ul`: soma do subconjunto coberto; null se E vazio.
- `volume_janela_min_ul`, `volume_janela_max_ul`: iguais à soma coberta somente quando D_c = D_W; caso contrário, null.
- `duracao_janela_s`, `duracao_coberta_s`, `duracao_nao_coberta_s` e `cobertura = D_c/D_W`.

Com cobertura parcial, o subtotal não estima a janela completa, não é limite inferior garantido da produção real e não permite completar o máximo com o pior ponto conhecido. Produção dos trechos omitidos permanece indeterminada.

A partição do tempo é completa, sem sobreposição. Classificar cada trecho descoberto por um motivo principal; guardar causas adicionais sem duplicar duração. Precedência proposta em pares: conflito → temperatura inválida → fora do domínio → lacuna excessiva. Bordas sem amostras são contabilizadas separadamente. Se massa/configuração/janela forem inválidas, a cobertura do modelo fica null; diagnóstico temporal opcional é separado.

### 4.4 Maturação, aplicabilidade e reprodutibilidade

Toda saída numérica traz `aplicabilidade = REFERENCIA_GERAL_NAO_VALIDADA_PARA_TOMMY_ATKINS`, mesmo com maturação conhecida.

Estágios propostos: VERDE_MADURA, EM_AMADURECIMENTO, MADURA, MISTA e DESCONHECIDA. Verde-madura não significa fisiologicamente imatura. Informação ausente vira DESCONHECIDA explicitamente. Não mapear escalas diferentes sem critério documentado.

DESCONHECIDA/MISTA não bloqueiam o cenário geral, mas exigem limitação própria: não há correspondência demonstrada das taxas com estágio homogêneo da carga. O intervalo publicado não foi provado abrangente de toda maturação. Não estreitar faixas ou escolher extremos por estágio. Não inferir maturação por temperatura, umidade ou tempo de viagem. Condição sabidamente imatura, sobremadura ou não contemplada recebe aplicabilidade não estabelecida, sem enquadramento automático no estágio próximo.

Fixar massa, estágio e perfil em snapshot. Mudanças durante a sessão exigem nova janela/versionamento, sem reescrever análises anteriores. A extensão por sublotes `Σ_i Σ_j q(T_i,s_j) × M_j × Δt_i` exige taxas sustentadas por estágio e composição em massa; não integra V1.

Registrar IDs/valores originais e normalizados, sensor/contexto, horários de medição/recebimento, janela, G, modo, tabela/fonte/data de acesso, hipóteses, algoritmo e exclusões. Mesma entrada/configuração produz mesmo resultado, independentemente da ordem de chegada. Leitura atrasada gera nova revisão vinculada à anterior; não somar o novo total ao antigo.

O hash deve considerar entradas ordenadas, marcadores inválidos/conflitantes e configuração. O horário de execução não afeta o cálculo. Serialização canônica será fixada antes da persistência.

## 5. Política de tratamento dos dados

### 5.1 Validação sem preenchimento implícito

| Situação | Comportamento V1 |
|---|---|
| Nenhuma leitura ou só uma | Sem pares; volumes null; risco não avaliado |
| Falta de leitura nas bordas | Trecho sem cobertura; não extrapolar |
| Horários irregulares | Duração exata por par, sem reamostragem ou média de cadência |
| Mesmo ID externo/payload igual | Uma observação, sem dupla contagem; registrar duplicata |
| Mesmo ID/payload divergente | Conflito; horário unívoco vira marcador inválido; horários divergentes interrompem análise até resolver identidade |
| IDs diferentes, mesmo sensor/instante/temperatura normalizada | Uma observação temporal, preservando IDs |
| Mesmo sensor/instante com valores diferentes ou um inválido | Marcador conflitante; sem média, último vencedor ou desempate arbitrário |
| Fora de ordem | Ordenar por medição; chegada tardia exige revisão |
| Temperatura ausente, não numérica, infinita ou NaN | Marcador inválido no horário conhecido; não atravessá-lo unindo vizinhos |
| Temperatura fora do domínio do modo | Pares adjacentes sem cálculo; preservar valor/motivo |
| Intervalo maior que G | Par inteiro descoberto; sem preenchimento parcial ou taxa zero |
| Massa ausente/zero/negativa/não finita/booleana ou unidade indefinida | Estimativa indisponível; volumes/cobertura null; sem inferência |
| Estágio omitido | DESCONHECIDA e limitação; cenário geral permitido |
| Maturação MISTA | Sem uniformidade, fator ou proporção inventados |
| Umidade ausente/inválida | Não bloqueia q; descrição de umidade fica indisponível/incompleta |
| Timezone ausente/horário não interpretável | Rejeitar análise: não é possível posicionar a observação com segurança; não assumir fuso local |
| Horário futuro em relação ao corte de aquisição | Rejeitar a análise por inconsistência temporal até resolver; não aceitar tolerância oculta |
| Outra carga/sessão/sensor | Excluir na seleção; não relabelar como leitura alvo |
| G/modo ausente ou inválido | Configuração incompleta ou inválida; volumes null |

Temperatura finita fora de 10–20 °C não significa instrumento defeituoso: significa falta de taxa neste perfil. Faixa física do sensor depende do datasheet/calibração, ainda pendentes.

### 5.2 Estados e nulidade

Estados de `status_calculo`, com precedência ENTRADA_INVALIDA → CONFIGURACAO_INCOMPLETA → demais:

- `ENTRADA_INVALIDA`: massa, janela, metadado temporal indispensável, identidade contraditória ou valor inválido de configuração impede execução confiável.
- `CONFIGURACAO_INCOMPLETA`: falta modo ou G; sem default silencioso.
- `SEM_ESTIMATIVA`: entrada executável, mas nenhum par elegível; falta de leituras, fora do domínio ou lacunas excessivas são motivos complementares.
- `PARCIAL`: D_c > 0 e D_c < D_W; só subtotal coberto é numérico.
- `COMPLETO_NO_MODELO`: D_c = D_W; cobertura completa sob hipóteses, sem validação biológica.

Se tudo estiver fora do domínio, retornar SEM_ESTIMATIVA com motivo FORA_DO_DOMINIO. Em PONTOS, intermediários entre 10 e 20 recebem SEM_TAXA_NO_MODO. Guardar `motivos` separados de `limitacoes`.

Em janela válida sem amostras, D_c = 0 e D_n = D_W são conhecidos, mas volumes null. Soma vazia não será exposta como produção zero. Ausência de massa não será massa zero.

Consumidores não devem preencher null com zero em relatório, gráfico, média, exportação ou agregação. Somar cargas não cobre automaticamente um caminhão: massas/janelas/cobertura precisam ser compatíveis e sem dupla contagem.

### 5.3 Primeira versão sem escore de risco

Retornar `classificacao_risco_etileno = NAO_AVALIADO`, motivo `SEM_LIMIAR_VALIDADO`. Não transformar volume ou percentual de cobertura em risco baixo/médio/alto.

Alternativa útil: faixa calculada, cobertura, trechos sem estimativa e indicadores de qualidade. Descrição ambiental informa medidas e tempo em faixas configuradas, sem chamá-los de detecção de gás. Comparações com recomendações exigem estágio/contexto aplicável; um ponto recomendado não determina tolerância instrumental, duração admissível ou gravidade do desvio. Estágio desconhecido impede selecionar automaticamente recomendação de estágio conhecido.

Alertas futuros podem comunicar dados ausentes, sensor desatualizado ou condição fora de perfil operacional aprovado. São regras de informação/atenção versionadas, não escore científico de gás. A especificação científica não define alertas ou acionamento; o módulo operacional atual é separado e a intervenção é exclusivamente virtual.

## 6. Limitações científicas

1. Taxas gerais não foram validadas para Tommy Atkins. A transferência é aproximação explícita.
2. Extremos não são limites físicos garantidos ou percentis conhecidos; não há probabilidade associada à faixa.
3. Interpolação opcional não foi fornecida pela fonte nem resolve falta de validação biológica.
4. Ar pode divergir da polpa; atraso térmico/variação espacial não são modelados. Posicionamento/calibração devem ser justificados.
5. Pontos discretos não revelam excursões entre leituras; cobertura completa é da regra numérica.
6. Massa constante e um sinal térmico representativo são hipóteses; mistura e gradientes não são resolvidos pela faixa genérica.
7. Não são quantificados amadurecimento temporal, ferimentos, tratamentos, idade pós-colheita ou atmosfera. Cenário sabidamente incompatível exige suspensão do perfil; informação ausente permanece limitação.
8. Umidade não mede gás nem corrige q.
9. V em µL é integral de referência; ppm é razão de gás no compartimento em um instante, exigindo balanço de massa e volume livre/ventilação/mistura/condições de contorno. Não converter V em ppm dividindo pelo volume nominal do caminhão.
10. Exaustão simulada não altera q ou reduz produção acumulada e não comprova remoção real.
11. Modelo não valida conservação ou segurança da carga; ausência de estimativa nunca significa condição segura.

## 7. Exemplos calculados

**Cargas/leituras desta seção são hipotéticas.** Taxas nos pontos vêm da seção 3; demais números são aritmética desta especificação. Data: 01/10/2026; horários HH:MM em UTC. G = 3600 s é fixture didática para contas em horas, sem valor científico ou aprovação para aquisição real. Salvo indicação: modo PONTOS, maturação VERDE_MADURA, °C e kg.

### E01 — temperatura constante

M = 1000; W = [00:00,02:00). Leituras: (00:00,13),(01:00,13),(02:00,13).

Dois intervalos de 1 h; q = [0,2;1,0].

`V_min = 0,2 × 1000 × (1+1) = 400 µL`.

`V_max = 1,0 × 1000 × (1+1) = 2000 µL`.

D_c = D_W = 7200 s. COMPLETO_NO_MODELO; total [400;2000] µL = [0,4;2] mL.

### E02 — temperatura variável

M = 1000; W = [00:00,02:00). Leituras: (00:00,13),(01:00,20),(02:00,20).

00:00–01:00 usa 13 °C: [200;1000] µL. 01:00–02:00 usa 20 °C: [500;8000] µL.

`V = [200+500;1000+8000] = [700;9000] µL`.

COMPLETO_NO_MODELO. Usar 20 °C nas duas horas daria [1000;16000] µL e viola esta especificação.

### E03 — horários irregulares e conversão de massa

M = 500.000 g → 500 kg; W = [00:00,01:00). Leituras: (00:00,10),(00:15,13),(01:00,13).

Durações: 900/3600 = 0,25 h; 2700/3600 = 0,75 h.

`V_min = 0,1 × 500 × 0,25 + 0,2 × 500 × 0,75 = 12,5+75 = 87,5 µL`.

`V_max = 0,5 × 500 × 0,25 + 1,0 × 500 × 0,75 = 62,5+375 = 437,5 µL`.

COMPLETO_NO_MODELO. Não atribuir 30 minutos fictícios a cada par.

### E04 — dados incompletos por intervalo longo

M = 1000; W = [00:00,03:00). Leituras: (00:00,13),(01:00,13),(03:00,13).

Primeiro intervalo: [200;1000] µL. Segundo tem 7200 s > G e é todo excluído.

PARCIAL; D_c = 3600, D_n = 7200 s; cobertura = 1/3. Subtotal [200;1000] µL; total da janela null. Não preencher ausência com zero ou multiplicar subtotal por três.

### E05 — nenhuma leitura ou apenas uma

M = 1000; W = [00:00,02:00). Série vazia ou somente (01:00,13).

SEM_ESTIMATIVA; D_c = 0, D_n = 7200 s; todos os volumes null. Não retornar [0;0].

### E06 — fora do domínio

M = 1000; W = [00:00,03:00). Leituras: (00:00,13),(01:00,13),(02:00,25),(03:00,13).

00:00–01:00 aceito: [200;1000] µL. Outros dois pares têm extremo a 25 °C e são excluídos. PARCIAL; D_c = 3600, D_n = 7200 s; subtotal [200;1000] µL; total null.

Variante: W = [00:00,01:00), leituras (00:00,25),(01:00,25) → SEM_ESTIMATIVA/FORA_DO_DOMINIO, D_c = 0; volumes null nos dois modos.

### E07 — maturação desconhecida ou mista

Repetir E01 com DESCONHECIDA e, separadamente, MISTA.

Aritmética permanece [400;2000] µL no cenário geral, sem correção. Limitação de estágio obrigatória; aplicação não validada para cultivar e risco NAO_AVALIADO. Não afirmar que extremos abrangem toda variação da carga. Uma exigência futura de estimativa específica por estágio permanece indisponível até validar outra referência.

### E08 — massa inválida

Usar janela/leituras de E01 com M ausente, 0, −100, NaN, infinito, true ou “10 caixas” sem conversão verificável.

ENTRADA_INVALIDA por massa; volumes e cobertura do modelo null. Não calcular com M = 0 nem reaproveitar massa de outra carga.

### E09 — intermediário e interpolação explícita

M = 1000; W = [00:00,01:00). Leituras: (00:00,12),(01:00,12).

PONTOS: SEM_ESTIMATIVA/SEM_TAXA_NO_MODO, D_c = 0; volumes null.

LINEAR: `α = (12−10)/(13−10) = 2/3`.

`q_min = 0,1 + (2/3)×(0,2−0,1) = 1/6`.

`q_max = 0,5 + (2/3)×(1,0−0,5) = 5/6`.

V = [1000/6;5000/6] µL → seis casas: [166,666667;833,333333] µL. COMPLETO_NO_MODELO com interpolação exploratória explícita; não são taxas medidas pela fonte a 12 °C.

### E10 — duplicatas e fora de ordem

Receber E02 em ordem 02:00,00:00,01:00 e repetir 01:00 com mesmo ID/payload.

Após normalizar: dois intervalos e [700;9000] µL. Duplicata não acrescenta duração. Se outra observação em 01:00 contradisser a primeira, com 15 °C em vez de 20 °C, ambos os pares ficam sem estimativa pelo marcador de conflito; volumes null até resolução.

### E11 — bordas e limite de lacuna

M = 1000; W = [00:00,02:00). Leituras: (00:30,13),(01:30,13).

Par de 3600 s = G aceito: subtotal [200;1000] µL. Bordas somam 3600 s descobertos. PARCIAL; cobertura 50%; total null.

Variante: duas leituras separadas por 3601 s, janela exatamente entre elas, G = 3600 s → SEM_ESTIMATIVA, volumes null. Não truncar para 3600 s.

### E12 — umidade ausente

E01 sem leituras de umidade: potencial continua [400;2000] µL; descrição de umidade indisponível, risco por etileno NAO_AVALIADO. Não fabricar umidade nem inferir gás a partir dela.

### Resumo de resultados

| ID | Subtotal min µL | Subtotal max µL | Cobertura | Total da janela |
|---|---:|---:|---|---|
| E01 | 400 | 2000 | 100% | Igual ao subtotal |
| E02 | 700 | 9000 | 100% | Igual ao subtotal |
| E03 | 87,5 | 437,5 | 100% | Igual ao subtotal |
| E04 | 200 | 1000 | 1/3 | null |
| E05 | null | null | 0% | null |
| E06 principal | 200 | 1000 | 1/3 | null |
| E07 | 400 | 2000 | 100% | Igual ao subtotal, limitado |
| E08 | null | null | null | null |
| E09 PONTOS | null | null | 0% | null |
| E09 LINEAR | 166,666667 | 833,333333 | 100% | Igual ao subtotal, exploratório |
| E10 sem conflito | 700 | 9000 | 100% | Igual ao subtotal |
| E11 principal | 200 | 1000 | 50% | null |
| E12 | 400 | 2000 | 100% | Igual ao subtotal |

## 8. Critérios de aceite científicos e computacionais

1. Reproduzir E01–E12: contas, estado, nulidade, cobertura e limitações; saída com seis casas segue arredondamento definido.
2. Testar dimensionalidade, conversões declaradas g/t/°F/K, UTC com offsets equivalentes e durações fracionárias. 55,4 °F e 286,15 K convertem em 13 °C; 55 °F não será arredondado para 13 °C silenciosamente.
3. Aceitar extremos 10 e 20 °C nos dois modos; rejeitar 9,999 e 20,001. PONTOS rejeita 13,1; LINEAR usa fórmula explícita, sem extrapolação.
4. Permutar recebimento ou repetir dados idênticos não altera resultados. Conflitos não viram média/último vencedor.
5. Não atravessar ponto inválido/fora do domínio; não contar duração descoberta duas vezes.
6. Testar par igual a G e maior por um segundo. G ausente/zero/negativo/não finito impede cálculo. 3600 s dos exemplos não é default.
7. Nenhuma/uma leitura não retorna volume zero; massa ausente/inválida não produz volume. Rejeitar booleano numérico e horário sem timezone.
8. Na execução calculável: 0 ≤ D_c ≤ D_W; D_c+D_n = D_W; volume min ≤ max. E vazio implica null. Massa/duração positivas e taxas publicadas produzem contribuição positiva antes do arredondamento.
9. Total só é numérico em COMPLETO_NO_MODELO. PARCIAL retorna subtotal e motivo, sem extrapolação.
10. Temperatura futura não reescreve contribuição anterior. Correção histórica gera revisão; nunca somar acumulados de revisões.
11. Conhecido/desconhecido/misto não habilitam correção sem fonte. Toda estimativa informa aplicação geral não validada para Tommy Atkins.
12. Umidade não altera volumes; sua ausência não bloqueia q. Exaustão não altera volumes.
13. Risco permanece NAO_AVALIADO/SEM_LIMIAR_VALIDADO em todos os exemplos. Ausência de dados não será “seguro”.
14. Selecionar sensor/sessão impede mistura de viagens; vínculo atual de dispositivo não reinterpreta história.
15. Snapshot traz fonte, tabela, hipóteses, G e versões para recomputar. Testar precisão/arredondamento com frações recorrentes.
16. Preservar 151 testes existentes. Implementação futura deve acrescentar testes próprios e manter regressão; testes unitários não comprovam validade biológica.

Validação desta etapa: conferência da fonte, revisão dimensional e verificação aritmética dos exemplos. Nenhuma função de backend foi implementada ou teste contra produção executado. Os 151 testes passaram no diagnóstico; não foram reexecutados nesta etapa documental porque o backend não mudou.

## 9. Decisões da especificação e validações ainda necessárias

| Decisão | Proposta/alternativa conservadora | Evidência/definição necessária |
|---|---|---|
| Modo com sensor real | PONTOS é base; LINEAR exige escolha explícita exploratória | Aceitação da hipótese e eventual comparação experimental |
| Aplicação a Tommy Atkins | Rotular geral não validada, sem taxa inventada | Estudos/ensaio de frutos inteiros em condições comparáveis |
| G real | Sem default; não calcular até configurar | Cadência, perdas e política de qualidade justificadas |
| Representatividade térmica | Identificar ar/polpa/local; sem correção arbitrária | Datasheet, calibração, posição e comparação térmica |
| Maturação | Desconhecido/misto sem correção quantitativa | Método/data de avaliação e eventual composição |
| Regras ambientais | Medidas/cobertura; desvios com perfil explícito | Tolerâncias, duração e contexto justificados |
| Risco por volume | Indisponível nesta versão | Relação validada com exposição/desfecho; não há concentração medida |
| Relógio e corte de aquisição | Rejeitar inconsistências, sem tolerância oculta | Sincronização e política de relógio |
| Horizonte temporal da aplicação | Sem afirmar que q constante descreve todo amadurecimento | Horizonte e condições a validar; G não substitui esse horizonte |
| Hash e serialização | Snapshot imutável, independente da chegada | Formato canônico implementado em snapshots e hashes; sem alterar parâmetros científicos |

### Ajustes pontuais ao diagnóstico anterior

O diagnóstico foi preservado integralmente. Esta especificação esclarece:

- Domínio contínuo 10–20 °C depende de interpolação; a referência fornece quatro pontos discretos.
- Min/max não significa limites físicos/estatísticos validados, inclusive para maturação mista/desconhecida.
- Interpolação sugerida permanece hipótese opcional, sem validação científica demonstrada.
- Extensão provisória da última leitura até o presente, antes aventada, não integra V1; exigem-se dois extremos e não se preenchem bordas.
- Marcadores inválidos impedem atravessar falhas ao procurar a próxima leitura válida; ambos os extremos devem ser utilizáveis.
- Estado único de cálculo com motivos complementares evita ambiguidade entre fora do domínio e insuficiência.
- O exemplo anterior de 700–9000 µL continua correto, agora com amostra final explicitada em E02.
- Data da ficha (1997) e ausência de bibliografia detalhada são limites agora registrados, sem invalidar a transcrição das taxas gerais.

**Critério para seguir:** implementação posterior da função determinística pode usar esta especificação, mantendo rótulo exploratório e bloqueios de configuração. Alegações de produção real específica, risco, concentração ou efeito de ventilação continuam dependentes de fundamentação adicional.
