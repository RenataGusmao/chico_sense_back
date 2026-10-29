# ChicoSense â€” Roteiro tÃ©cnico da demonstraÃ§Ã£o do backend

Data: 28/10/2026. Branch feature/monitoramento-etileno-manga.
Consolidado apÃ³s seguranÃ§a logÃ­stica/ThingSpeak e qualificaÃ§Ã£o PostgreSQL; use os contratos atuais.
Escopo: API e demonstraÃ§Ã£o local automatizada, sem frontend, deploy ou equipamento fÃ­sico.

## 1. Ambiente e execuÃ§Ã£o segura

A demonstraÃ§Ã£o executÃ¡vel usa TestClient, SQLite descartÃ¡vel, senha/hash/JWT de
fixtures e httpx.MockTransport para o ThingSpeak. NÃ£o inicia servidor, nÃ£o usa o
DATABASE_URL remoto para consultas e nÃ£o exige equipamentos ou credenciais reais.

Na raiz do backend:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_integracao_etapa8.py::test_fluxo_integrado_ponta_a_ponta_etapa8 -q -s -p no:cacheprovider --tb=short
```

O teste imprime IDs e resultado resumido; nÃ£o imprime senha, JWT ou chave de leitura.
O relÃ³gio virtual da intervenÃ§Ã£o Ã© controlado em fixture; nÃ£o hÃ¡ scheduler nem
espera fÃ­sica de 60 s. A emissÃ£o/verificaÃ§Ã£o de JWT e o motor matemÃ¡tico sÃ£o reais.
A aquisiÃ§Ã£o e os dados ambientais sÃ£o hipotÃ©ticos. Nada Ã© cadastrado no Supabase.

Para verificar todos os testes da etapa:

```powershell
.\.venv\Scripts\python.exe -B -m pytest tests/test_integracao_etapa8.py -q -p no:cacheprovider --tb=short
```

## 2. O que demonstrar e o que afirmar

| Componente | ExecuÃ§Ã£o neste roteiro | Limite da afirmaÃ§Ã£o |
|---|---|---|
| Login/JWT | VerificaÃ§Ã£o real de hash e emissÃ£o de token para usuÃ¡rio fictÃ­cio | NÃ£o usa conta/chave real de produÃ§Ã£o |
| Carga/viagem/sessÃ£o | Rotas reais sobre SQLite | Este roteiro usa SQLite; PostgreSQL real foi qualificado separadamente |
| Sensor/origem | Cadastro prÃ©vio em fixture, vÃ­nculo real na sessÃ£o/mapping | NÃ£o hÃ¡ aquisiÃ§Ã£o fÃ­sica validada nem CRUD pÃºblico de sensores |
| ThingSpeak | Cliente/mapper reais com HTTP mockado | NÃ£o comprova disponibilidade, cadÃªncia ou calibraÃ§Ã£o do hardware |
| Etileno | Motor real, Decimal, anÃ¡lise persistida | ProduÃ§Ã£o potencial; sem mediÃ§Ã£o ou concentraÃ§Ã£o real |
| AvaliaÃ§Ã£o/alerta | Regras reais com configuraÃ§Ã£o EXPERIMENTAL didÃ¡tica | NÃ£o valida dano, risco fisiolÃ³gico ou adequaÃ§Ã£o da exaustÃ£o |
| DecisÃ£o humana | RequisiÃ§Ãµes explÃ­citas com JWT de cada papel | Nenhum acionamento automÃ¡tico |
| ExaustÃ£o | MÃ¡quina de estados e histÃ³rico reais, atuador virtual | Sem remoÃ§Ã£o de gÃ¡s, mudanÃ§a tÃ©rmica ou eficÃ¡cia comprovada |

## 3. SequÃªncia comentada

1. **Autenticar.** Login real de OPERADOR, GESTOR e CONSULTA; consultar /auth/me.
   Explicar que perfil e vÃ­nculo com transportadora condicionam as operaÃ§Ãµes novas.
2. **Cadastrar viagem e carga.** Criar viagem hipotÃ©tica e carga Tommy Atkins via
   endpoints logÃ­sticos. Mostrar os IDs e a associaÃ§Ã£o pelo caminho /viagens/{id}/cargas.
   Esses endpoints agora exigem JWT e autorizaÃ§Ã£o por perfil/transportadora.
   O cenÃ¡rio continua em banco descartÃ¡vel; cadastros globais sÃ£o preparados por ADMIN.
3. **Preparar transporte.** Viagem EM_ANDAMENTO com inicio_real; carga EM_TRANSITO.
   A fixture associa o dispositivo/sensores preexistentes Ã  viagem criada; isso Ã©
   preparaÃ§Ã£o explÃ­cita do laboratÃ³rio, nÃ£o uma rota de cadastro inexistente.
4. **Declarar perfil.** Massa lÃ­quida 1000 kg, MANGA_TOMMY_ATKINS, maturaÃ§Ã£o MISTA,
   lote_hipotetico=true e rastreabilidade textual. NÃ£o presumir fruta verde/madura.
5. **Abrir sessÃ£o.** InÃ­cio explÃ­cito; sensor de temperatura e UR; ambiente de teste
   identificado; chave idempotente. Confirmar carga/viagem/sensores no snapshot.
6. **Adquirir histÃ³rico.** SincronizaÃ§Ã£o explÃ­cita. O mock responde field4 para
   temperatura e field7 para UR, demonstrando que nÃ£o se fixa field1/field2 no cÃ³digo.
   Retorno CONCLUIDA, revisÃ£o 1, trÃªs pontos de cada variÃ¡vel.
7. **Consultar histÃ³rico/qualidade.** Fixar revisÃ£o e fim; examinar medida_em,
   recebida_em/processada_em, unidades e percentual de cobertura. G=3600 s Ã© didÃ¡tico.
8. **Executar anÃ¡lise.** SessÃ£o ativa usa corte_aquisicao explÃ­cito e fim no ponto
   de fechamento. Mostrar faixa, total/subtotal, status, cobertura e limitaÃ§Ãµes.
9. **Consultar persistÃªncia.** GET da anÃ¡lise devolve o mesmo resultado; nÃ£o recalcula.
10. **Configurar ambiente.** GESTOR registra versÃ£o EXPERIMENTAL: temperatura 12â€“14 Â°C,
    UR 90â€“95%, G=3600 s, cobertura mÃ­nima 100%, duraÃ§Ã£o contÃ­nua 3600 s e MISTA
    explicitamente aplicÃ¡vel. SÃ£o nÃºmeros didÃ¡ticos, sem validaÃ§Ã£o de dano.
11. **Avaliar.** Fixar janela/revisÃ£o, opcionalmente referenciando a anÃ¡lise cientÃ­fica.
    O contexto cientÃ­fico nÃ£o altera as regras ambientais ou cria risco por volume.
12. **Mostrar alertas.** TEMPERATURA_FORA_DA_FAIXA e EXPOSICAO_AMBIENTAL_PROLONGADA.
    Examinar evidÃªncias, valores e limites. A duraÃ§Ã£o Ã© hipÃ³tese operacional entre
    extremos concordantes, nÃ£o observaÃ§Ã£o contÃ­nua de cada instante.
13. **Reconhecer.** OPERADOR registra RECONHECER, com justificativa. Estado EM_ANALISE,
    ator/horÃ¡rio e Ocorrencia persistidos. Reconhecer nÃ£o autoriza a exaustÃ£o.
14. **Solicitar intervenÃ§Ã£o.** Vincular alerta, avaliaÃ§Ã£o e anÃ¡lise; justificar a
    demonstraÃ§Ã£o virtual. Estado SOLICITADA, virtual_ligado=false.
15. **Autorizar.** GESTOR examina contexto e envia AUTORIZAR. Continua desligado.
16. **Iniciar.** Outra requisiÃ§Ã£o explÃ­cita do GESTOR envia INICIAR. Recurso Ã© Ãºnico
    por veÃ­culo; mostrar ocupaÃ§Ã£o e estado EM_EXECUCAO.
17. **Encerrar.** Fixture avanÃ§a 60 s e o solicitante envia ENCERRAR. Estado CONCLUIDA,
    duraÃ§Ã£o registrada 60.000000 s. NÃ£o afirmar reduÃ§Ã£o de etileno/temperatura.
18. **Conferir histÃ³rico.** Quatro aÃ§Ãµes: SOLICITAR, AUTORIZAR, INICIAR, ENCERRAR.
    IDs de carga/viagem/sessÃ£o/anÃ¡lise/alerta/intervenÃ§Ã£o permanecem coerentes.
    A anÃ¡lise permanece igual e o alerta continua EM_ANALISE, sem resoluÃ§Ã£o automÃ¡tica.

O teste faz 32 chamadas locais (incluindo trÃªs logins), uma chamada HTTP mockada ao
ThingSpeak e nenhuma aquisiÃ§Ã£o fÃ­sica real. SÃ£o usados os contratos atuais,
sem criar endpoints para apresentaÃ§Ã£o.

## 4. CÃ¡lculo verificÃ¡vel manualmente

Amostras t0â†’13 Â°C, t0+1hâ†’20 Â°C, t0+2hâ†’20 Â°C; UR 92%; massa 1000 kg.

- Primeira hora: [0,2;1] Ã— 1000 Ã— 1 = [200;1000] ÂµL.
- Segunda hora: [0,5;8] Ã— 1000 Ã— 1 = [500;8000] ÂµL.
- Total potencial [700;9000] ÂµL, 100%, COMPLETO_NO_MODELO, risco NAO_AVALIADO.

A Ãºltima leitura fecha o intervalo, sem prolongar exposiÃ§Ã£o. Essas taxas sÃ£o as
referÃªncias gerais jÃ¡ documentadas na Etapa 1/2; nÃ£o sÃ£o validaÃ§Ã£o experimental da cultivar.

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

## 5. DemonstraÃ§Ã£o interativa futura

A API pode ser apresentada em http://127.0.0.1:8000/docs somente apÃ³s preparar um
ambiente isolado. **A configuraÃ§Ã£o atual aponta para banco remoto; localhost na URL
da API nÃ£o impede gravaÃ§Ã£o remota. NÃ£o usar a configuraÃ§Ã£o atual para semear a demo.**

PrÃ©-requisitos ainda externos a este roteiro: PostgreSQL descartÃ¡vel identificado,
conta de teste com papÃ©is/vÃ­nculos, entidades de laboratÃ³rio, configuraÃ§Ã£o do canal/
fields fora do frontend e origem de dados autorizada. NÃ£o foram instalados serviÃ§os,
criadas contas de produÃ§Ã£o ou alterados .env/credenciais nesta etapa.

Uso real do ThingSpeak exigirÃ¡ acesso de rede, canal/sensores provisionados,
validaÃ§Ã£o da origem temporal, mapping, calibraÃ§Ã£o/representatividade e cadÃªncia.
Mesmo com HTTP real, a leitura do provedor nÃ£o valida automaticamente a instalaÃ§Ã£o
fÃ­sica ou a temperatura da polpa. Uma futura aquisiÃ§Ã£o real deve ter relatÃ³rio prÃ³prio.

A exaustÃ£o continuarÃ¡ virtual. NÃ£o hÃ¡ endpoint, credencial ou transporte para
hardware e nenhuma operaÃ§Ã£o deverÃ¡ apresentar eficÃ¡cia de remoÃ§Ã£o de etileno.

## 6. EvidÃªncias e limites para a apresentaÃ§Ã£o

Usar conjuntamente os documentos de validaÃ§Ã£o integrada e contratos do frontend.
Distinguir teste ponta a ponta local de PostgreSQL/concorrÃªncia real: estes Ãºltimos
continuam pendentes por falta de recurso isolado identificado. NÃ£o apresentar a
quantidade de testes ou a demonstraÃ§Ã£o mockada como validaÃ§Ã£o fÃ­sica dos sensores.
