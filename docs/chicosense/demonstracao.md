# ChicoSense — Roteiro técnico da demonstração do backend

Data: 28/10/2026. Branch feature/monitoramento-etileno-manga.
Consolidado após segurança logística/ThingSpeak e qualificação PostgreSQL; use os contratos atuais.
Escopo: API e demonstração local automatizada, sem frontend, deploy ou equipamento físico.

## 1. Ambiente e execução segura

A demonstração executável usa TestClient, SQLite descartável, senha/hash/JWT de
fixtures e httpx.MockTransport para o ThingSpeak. Não inicia servidor, não usa o
DATABASE_URL remoto para consultas e não exige equipamentos ou credenciais reais.

Na raiz do backend:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_integracao_etapa8.py::test_fluxo_integrado_ponta_a_ponta_etapa8 -q -s -p no:cacheprovider --tb=short
```

O teste imprime IDs e resultado resumido; não imprime senha, JWT ou chave de leitura.
O relógio virtual da intervenção é controlado em fixture; não há scheduler nem
espera física de 60 s. A emissão/verificação de JWT e o motor matemático são reais.
A aquisição e os dados ambientais são hipotéticos. Nada é cadastrado no Supabase.

Para verificar todos os testes da etapa:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_integracao_etapa8.py -q -p no:cacheprovider --tb=short
```

## 2. O que demonstrar e o que afirmar

| Componente | Execução neste roteiro | Limite da afirmação |
|---|---|---|
| Login/JWT | Verificação real de hash e emissão de token para usuário fictício | Não usa conta/chave real de produção |
| Carga/viagem/sessão | Rotas reais sobre SQLite | Este roteiro usa SQLite; PostgreSQL real foi qualificado separadamente |
| Sensor/origem | Cadastro prévio em fixture, vínculo real na sessão/mapping | Não há aquisição física validada nem CRUD público de sensores |
| ThingSpeak | Cliente/mapper reais com HTTP mockado | Não comprova disponibilidade, cadência ou calibração do hardware |
| Etileno | Motor real, Decimal, análise persistida | Produção potencial; sem medição ou concentração real |
| Avaliação/alerta | Regras reais com configuração EXPERIMENTAL didática | Não valida dano, risco fisiológico ou adequação da exaustão |
| Decisão humana | Requisições explícitas com JWT de cada papel | Nenhum acionamento automático |
| Exaustão | Máquina de estados e histórico reais, atuador virtual | Sem remoção de gás, mudança térmica ou eficácia comprovada |

## 3. Sequência comentada

1. **Autenticar.** Login real de OPERADOR, GESTOR e CONSULTA; consultar /auth/me.
   Explicar que perfil e vínculo com transportadora condicionam as operações novas.
2. **Cadastrar viagem e carga.** Criar viagem hipotética e carga Tommy Atkins via
   endpoints logísticos. Mostrar os IDs e a associação pelo caminho /viagens/{id}/cargas.
   Esses endpoints agora exigem JWT e autorização por perfil/transportadora.
   O cenário continua em banco descartável; cadastros globais são preparados por ADMIN.
3. **Preparar transporte.** Viagem EM_ANDAMENTO com inicio_real; carga EM_TRANSITO.
   A fixture associa o dispositivo/sensores preexistentes à viagem criada; isso é
   preparação explícita do laboratório, não uma rota de cadastro inexistente.
4. **Declarar perfil.** Massa líquida 1000 kg, MANGA_TOMMY_ATKINS, maturação MISTA,
   lote_hipotetico=true e rastreabilidade textual. Não presumir fruta verde/madura.
5. **Abrir sessão.** Início explícito; sensor de temperatura e UR; ambiente de teste
   identificado; chave idempotente. Confirmar carga/viagem/sensores no snapshot.
6. **Adquirir histórico.** Sincronização explícita. O mock responde field4 para
   temperatura e field7 para UR, demonstrando que não se fixa field1/field2 no código.
   Retorno CONCLUIDA, revisão 1, três pontos de cada variável.
7. **Consultar histórico/qualidade.** Fixar revisão e fim; examinar medida_em,
   recebida_em/processada_em, unidades e percentual de cobertura. G=3600 s é didático.
8. **Executar análise.** Sessão ativa usa corte_aquisicao explícito e fim no ponto
   de fechamento. Mostrar faixa, total/subtotal, status, cobertura e limitações.
9. **Consultar persistência.** GET da análise devolve o mesmo resultado; não recalcula.
10. **Configurar ambiente.** GESTOR registra versão EXPERIMENTAL: temperatura 12–14 °C,
    UR 90–95%, G=3600 s, cobertura mínima 100%, duração contínua 3600 s e MISTA
    explicitamente aplicável. São números didáticos, sem validação de dano.
11. **Avaliar.** Fixar janela/revisão, opcionalmente referenciando a análise científica.
    O contexto científico não altera as regras ambientais ou cria risco por volume.
12. **Mostrar alertas.** TEMPERATURA_FORA_DA_FAIXA e EXPOSICAO_AMBIENTAL_PROLONGADA.
    Examinar evidências, valores e limites. A duração é hipótese operacional entre
    extremos concordantes, não observação contínua de cada instante.
13. **Reconhecer.** OPERADOR registra RECONHECER, com justificativa. Estado EM_ANALISE,
    ator/horário e Ocorrencia persistidos. Reconhecer não autoriza a exaustão.
14. **Solicitar intervenção.** Vincular alerta, avaliação e análise; justificar a
    demonstração virtual. Estado SOLICITADA, virtual_ligado=false.
15. **Autorizar.** GESTOR examina contexto e envia AUTORIZAR. Continua desligado.
16. **Iniciar.** Outra requisição explícita do GESTOR envia INICIAR. Recurso é único
    por veículo; mostrar ocupação e estado EM_EXECUCAO.
17. **Encerrar.** Fixture avança 60 s e o solicitante envia ENCERRAR. Estado CONCLUIDA,
    duração registrada 60.000000 s. Não afirmar redução de etileno/temperatura.
18. **Conferir histórico.** Quatro ações: SOLICITAR, AUTORIZAR, INICIAR, ENCERRAR.
    IDs de carga/viagem/sessão/análise/alerta/intervenção permanecem coerentes.
    A análise permanece igual e o alerta continua EM_ANALISE, sem resolução automática.

O teste faz 32 chamadas locais (incluindo três logins), uma chamada HTTP mockada ao
ThingSpeak e nenhuma aquisição física real. São usados os contratos atuais,
sem criar endpoints para apresentação.

## 4. Cálculo verificável manualmente

Amostras t0→13 °C, t0+1h→20 °C, t0+2h→20 °C; UR 92%; massa 1000 kg.

- Primeira hora: [0,2;1] × 1000 × 1 = [200;1000] µL.
- Segunda hora: [0,5;8] × 1000 × 1 = [500;8000] µL.
- Total potencial [700;9000] µL, 100%, COMPLETO_NO_MODELO, risco NAO_AVALIADO.

A última leitura fecha o intervalo, sem prolongar exposição. Essas taxas são as
referências gerais já documentadas na Etapa 1/2; não são validação experimental da cultivar.

Resumo esperado impresso pelo teste:

```json
{
  "volume_potencial_ul": ["700.000000", "9000.000000"],
  "cobertura_percentual": "100",
  "risco_etileno": "NAO_AVALIADO",
  "estado_virtual": "CONCLUIDA",
  "acoes": ["SOLICITAR", "AUTORIZAR", "INICIAR", "ENCERRAR"],
  "operacoes_http_locais": 32,
  "aquisicoes_fisicas": 0
}
```

## 5. Demonstração interativa futura

A API pode ser apresentada em http://127.0.0.1:8000/docs somente após preparar um
ambiente isolado. **A configuração atual aponta para banco remoto; localhost na URL
da API não impede gravação remota. Não usar a configuração atual para semear a demo.**

Pré-requisitos ainda externos a este roteiro: PostgreSQL descartável identificado,
conta de teste com papéis/vínculos, entidades de laboratório, configuração do canal/
fields fora do frontend e origem de dados autorizada. Não foram instalados serviços,
criadas contas de produção ou alterados .env/credenciais nesta etapa.

Uso real do ThingSpeak exigirá acesso de rede, canal/sensores provisionados,
validação da origem temporal, mapping, calibração/representatividade e cadência.
Mesmo com HTTP real, a leitura do provedor não valida automaticamente a instalação
física ou a temperatura da polpa. Uma futura aquisição real deve ter relatório próprio.

A exaustão continuará virtual. Não há endpoint, credencial ou transporte para
hardware e nenhuma operação deverá apresentar eficácia de remoção de etileno.

## 6. Evidências e limites para a apresentação

Usar conjuntamente os documentos de validação integrada e contratos do frontend.
Distinguir teste ponta a ponta local de PostgreSQL/concorrência real: estes últimos
continuam pendentes por falta de recurso isolado identificado. Não apresentar a
quantidade de testes ou a demonstração mockada como validação física dos sensores.
