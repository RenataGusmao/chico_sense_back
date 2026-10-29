# Motor isolado de estimativa de etileno

`estimar_etileno(EntradaEstimativa)` é uma função pura: não importa FastAPI,
SQLAlchemy, configurações de ambiente ou cliente HTTP. Não consulta relógio,
não persiste dados e não integra sensores, endpoints, alertas ou exaustão.
Somente a biblioteca padrão do Python é utilizada.

## Estrutura

- `parametros.py`: tabela imutável de referência, fonte, versão e limitações.
- `tipos.py`: entradas, observações, intervalos e resultados com dataclasses frozen.
- `motor.py`: conversões explícitas, validação, normalização e integração.
- `__init__.py`: interface pública do componente.
- `tests/test_etileno_motor.py`: exemplos E01–E12 e políticas de falha.

## Contrato e decisões

A especificação científica externa é `outputs/ChicoSense-modelo-cientifico-etileno.md`,
no workspace da análise. O pedido da Etapa 2 prevalece no único ajuste de contrato:
**modo omitido adota MODO_RESTRITO**. A especificação anterior exigia escolher
um modo. `modo=None` explícito continua sendo configuração incompleta; um valor
desconhecido é entrada inválida.

`intervalo_maximo_s` não tem default numérico: ausência retorna
CONFIGURACAO_INCOMPLETA, valor não positivo/não finito/booleano retorna
ENTRADA_INVALIDA. O 3600 usado nos exemplos é exclusivamente didático.

- MODO_RESTRITO → perfil UC_DAVIS_PONTOS_V1, apenas 10/13/15/20 °C.
- MODO_EXPLORATORIO → perfil UC_DAVIS_LINEAR_EXPLORATORIO_V1, interpolação
  linear de cada limite entre pontos adjacentes, em [10,20] °C.
- Nenhum modo extrapola, arredonda temperatura para pontos ou corrige por maturação.
- O resultado informa modo/perfil/metodologia e se uma contribuição efetivamente
  utilizou temperatura interpolada. O modo exploratório sempre inclui sua limitação,
  inclusive quando todas as temperaturas usadas coincidem com pontos publicados.

Massa: unidade declarada kg (default), g ou t métrica. Temperatura: C/°C (default),
F/°F ou K. Valores numéricos aceitam Decimal, int, float ou string decimal finita;
booleanos não são números válidos. Prefira Decimal/strings decimais para evitar
arredondamento anterior pelo chamador. Strings numéricas usam ponto decimal.
Timestamps são objetos datetime conscientes de fuso; strings ISO devem ser
interpretadas pelo adaptador antes de chamar o componente. Unidade/identidade inválida
é erro de entrada ou marcador, nunca inferência automática.

Uma entrada identifica um sensor e uma sessão; leituras de outros sensores/sessões
são excluídas. IDs externos devem ser strings opcionais, não vazias e qualificadas
pela origem (por exemplo origem/canal/entrada/campo); não passar apenas um entry_id
sem namespace quando houver múltiplas fontes. Não se importam enums/modelos ORM.

`corte_aquisicao` permite detectar observações futuras em relação ao corte declarado.
Se omitido, o motor usa o fim da janela como corte determinístico. **Um adaptador
para aquisição ao vivo deve fornecer explicitamente seu corte real**: o motor puro
não detecta o horário atual por conta própria. recebida_em é metadado de auditoria,
não substitui medida_em nem escolhe um vencedor entre leituras conflitantes.

## Integração e indisponibilidade

Apenas amostras dentro de [inicio,fim], incluindo a amostra de fechamento, são usadas.
O tempo integrado é [inicio,fim). Cada par consecutivo requer ambos os extremos
válidos e duração ≤ intervalo_maximo_s. Usa-se a temperatura inicial do par.
Não há interpolação temporal, extensão de bordas ou preenchimento parcial de gaps.

Observação inválida, conflitante ou fora do domínio é preservada como barreira.
Removê-la para unir seus vizinhos violaria a especificação. O primeiro motivo de
cada intervalo é a causa principal; motivos adicionais não duplicam sua duração.
Duplicatas idênticas não acrescentam exposição. Mesmo ID com horário divergente
invalida a análise; mesmo instante com temperaturas conflitantes invalida os pares
adjacentes. IDs diferentes e mesma temperatura normalizada no mesmo instante
formam um único ponto, mantendo as origens.

- COMPLETO_NO_MODELO: total da janela = subtotal coberto, com hipóteses explícitas.
- PARCIAL: somente subtotal coberto é numérico; total da janela é None.
- SEM_ESTIMATIVA: nenhum par elegível; volumes None, nunca soma vazia zero.
- ENTRADA_INVALIDA / CONFIGURACAO_INCOMPLETA: volumes/cobertura None.

Resultados contêm a entrada imutável, observações originais/normalizadas, tabela,
fonte/data de consulta, versão do modelo, configuração, intervalos e motivos.
Normalização e aritmética independem da ordem de chegada e do contexto Decimal
global. Não há geração de hash, revisão persistida ou serialização canônica nesta
etapa; esses mecanismos pertencem à integração posterior.

Cálculos usam Decimal em contexto local de 50 dígitos, sem arredondamento por
intervalo; apenas a soma final é quantizada a seis casas em µL, ROUND_HALF_EVEN.
Contribuição positiva abaixo da resolução de apresentação recebe motivo
RESOLUCAO_APRESENTACAO e permanece positiva nos intervalos antes do arredondamento.
Esse zero arredondado não é produção zero ou ausência de dados. Exceção aritmética
retorna indisponibilidade identificada, sem volume falso. Unidades inválidas e valores
não finitos nos conversores públicos levantam ValueError; o motor traduz essas
condições para os estados/marcadores documentados.

## Exemplo executável no diretório raiz do repositório

```python
from datetime import datetime, timedelta, timezone
from app.modules.monitoramento.etileno import (
    EntradaEstimativa, LeituraTemperatura, estimar_etileno,
)

inicio = datetime(2026, 10, 1, tzinfo=timezone.utc)
entrada = EntradaEstimativa(
    massa="1000", inicio=inicio, fim=inicio + timedelta(hours=2),
    sensor_id="temp-1", sessao_id="lote-hipotetico",
    intervalo_maximo_s=3600,  # fixture didática, não limite científico
    leituras=tuple(
        LeituraTemperatura(inicio + timedelta(hours=h), t, "temp-1", "lote-hipotetico")
        for h, t in ((0, 13), (1, 20), (2, 20))
    ),
)
r = estimar_etileno(entrada)
print(r.status_calculo.value)  # COMPLETO_NO_MODELO
print(r.volume_janela_min_ul, r.volume_janela_max_ul)  # 700.000000 9000.000000
print(r.percentual_cobertura)  # 100
```

Para exploração explícita, passar `modo=ModoCalculo.MODO_EXPLORATORIO`.
Não interpretar o exemplo como leitura real de caminhão.

## Interpretação científica e testes

Fonte geral: Kader, A. A., Mango, UC Davis PREC (ficha atualizada em fevereiro/1997),
consultada em 23/10/2026: https://postharvest.ucdavis.edu/produce-facts-sheets/mango.
Taxas em µL/kg/h: 10 °C [0.1,0.5], 13 °C [0.2,1.0], 15 °C [0.3,4.0], 20 °C [0.5,8.0].
Não são parâmetros específicos validados para Tommy Atkins. Estágio desconhecido/misto
não altera q; há limitações explícitas. Nenhum resultado infere concentração ou
remoção por exaustão. classificacao_risco_etileno permanece NAO_AVALIADO.

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_etileno_motor.py -q -p no:cacheprovider
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

Próximas integrações precisam definir G real, seleção temporal de sensor/carga,
calibração/contexto, corte de aquisição, persistência/versionamento e serialização.
Não fazem parte desta entrega.
