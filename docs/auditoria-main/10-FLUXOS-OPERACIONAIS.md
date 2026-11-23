# Fluxos operacionais

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Fluxo integrado e pré-requisitos reais

As rotas de leitura não fazem aquisição automática. Sincronização não calcula etileno; análise não gera risco/alerta; avaliação ambiental pode usar análise apenas como contexto. Alerta não solicita simulação. São comandos explícitos e separados.

```mermaid
flowchart TD
 Start[API local / docs / health] --> Seed{Banco local e seed prontos?}
 Seed -- Não --> Stop[Preparar infraestrutura / parar fluxo afetado]
 Seed -- Sim --> Login[Login / Authorize / me]
 Login --> Auth{JWT e perfil/escopo válidos?}
 Auth -- Não --> E1[401 ou 403 / não contornar]
 Auth -- Sim --> Log[Produto / empresas / frota / motorista / viagem / carga]
 Log --> Transit[Viagem EM_ANDAMENTO e carga EM_TRANSITO]
 Transit --> Conf[Declaração da carga]
 Conf --> Sensor{Sensores e mapping provisionados?}
 Sensor -- Não --> Stop
 Sensor -- Sim --> Session[Iniciar sessão / snapshot]
 Session --> Sync[Sincronização explícita]
 Sync --> Data{Aquisição consolidada suficiente?}
 Data -- Não --> Incon[Estado de falha/parcial / cobertura inconclusiva]
 Data -- Sim --> Hist[Fixar janela / corte / revisão]
 Incon --> Hist
 Hist --> Ana[Análise potencial / snapshots / null se insuficiente]
 Hist --> Env[Configuração ambiental versionada / avaliação]
 Ana -. contexto opcional compatível .-> Env
 Env --> Alerts[Consultar achados / alertas / evidências]
 Alerts --> Human[Decisão humana justificada]
 Human --> Want{Solicitar demonstração virtual?}
 Want -- Não --> Close[Encerrar ou cancelar monitoramento]
 Want -- Sim --> Req[SOLICITADA]
 Req --> Manage{GESTOR/ADMIN decide}
 Manage -- Recusa --> Ref[RECUSADA / histórico preservado]
 Manage -- Autoriza --> Approved[AUTORIZADA]
 Approved --> Valid{Contexto ativo e veículo livre?}
 Valid -- Não --> Conflict[409 / consultar estado / não repetir cegamente]
 Valid -- Sim --> Running[INICIAR / EM_EXECUCAO]
 Running --> Explicit[ENCERRAR / CANCELAR / REGISTRAR_FALHA]
 Explicit --> Terminal[Estado terminal / ações auditadas]
 Terminal --> Close
 Ref --> Close
 Close --> Read[Consultar história imutável]
```

## Transições

| Entidade | Origem | Ação/destino | Exceção ou guarda |
|---|---|---|---|
| Viagem | PLANEJADA | EM_ANDAMENTO ou CANCELADA | Frota/empresa válidas; horários coerentes |
| Viagem | EM_ANDAMENTO | CONCLUIDA | Chegada não anterior ao início; estrutura congelada |
| Carga | PLANEJADA | EM_TRANSITO ou CANCELADA | Trânsito exige viagem EM_ANDAMENTO |
| Carga | EM_TRANSITO | ENTREGUE | Viagem iniciada; terminal não reabre |
| Caixa | REGISTRADA | EM_TRANSITO ou AVARIADA | Trânsito exige carga EM_TRANSITO |
| Caixa | EM_TRANSITO | ENTREGUE ou AVARIADA | Integridade da carga; terminal não reabre |
| Sessão | ATIVA | ENCERRADA ou CANCELADA | Horário/motivo explícitos; sem apagar janela |
| Alerta | ABERTO | RECONHECER→EM_ANALISE | Ator operacional, justificativa, chave |
| Alerta | ABERTO/EM_ANALISE | RESOLVER→RESOLVIDO; DESCARTAR→DESCARTADO | Não há resolução automática |
| Alerta | Qualquer | OBSERVAR, mesmo estado | Nota auditada, inclusive terminal |
| Intervenção | SOLICITADA | AUTORIZAR→AUTORIZADA; RECUSAR→RECUSADA; CANCELAR→CANCELADA | Por perfil/solicitante |
| Intervenção | AUTORIZADA | INICIAR→EM_EXECUCAO; CANCELAR→CANCELADA | Sessão/logística ativas, veículo livre |
| Intervenção | EM_EXECUCAO | ENCERRAR→CONCLUIDA; CANCELAR→CANCELADA; REGISTRAR_FALHA→FALHA_SIMULACAO | Encerramento administrativo preservado |

Estado de cálculo não é ciclo operacional: ENTRADA_INVALIDA, CONFIGURACAO_INCOMPLETA, SEM_ESTIMATIVA, PARCIAL, COMPLETO_NO_MODELO são resultados científicos computacionais. Estado ambiental AVALIADO/INCONCLUSIVO/CONFIGURACAO_INSUFICIENTE é outra dimensão. Aquisição EM_EXECUCAO/CONCLUIDA/PARCIAL/FALHA/INTERROMPIDA também não altera esses conceitos automaticamente.

```mermaid
stateDiagram-v2
 [*] --> SOLICITADA
 SOLICITADA --> AUTORIZADA: AUTORIZAR
 SOLICITADA --> RECUSADA: RECUSAR
 SOLICITADA --> CANCELADA: CANCELAR
 AUTORIZADA --> EM_EXECUCAO: INICIAR
 AUTORIZADA --> CANCELADA: CANCELAR
 EM_EXECUCAO --> CONCLUIDA: ENCERRAR
 EM_EXECUCAO --> CANCELADA: CANCELAR
 EM_EXECUCAO --> FALHA_SIMULACAO: REGISTRAR_FALHA
```

## Erros e recuperação

401: novo login; 403: conferir identidade/vínculo, sem tentar IDs de outra empresa; 404: conferir recurso/pertencimento à sessão; 409: consultar estado/revisão/payload da chave; 422: corrigir dados, sem converter null em zero; 503: consultar antes de retry idempotente. Uma FALHA/PARCIAL de sincronização pode vir em 200: examinar estado, resumo e ocorrências.

Mesma chave e payload recuperam resultado anterior quando autorizado. Nova aquisição não modifica snapshot de análise anterior; nova análise é comando com nova chave. Complemento de sessão ENCERRADA requer flag/perfil/justificativa; CANCELADA preserva consultas e bloqueia novas análises/avaliações. Depois de iniciar simulação, prazo excedido exige ação humana; GET não altera estado.

Fontes: `app/modules/logistica/service.py` (transitions); `monitoramento/service.py` (sessão); `preventivo_service.py:decidir`; `exaustao_service.py:TRANSICOES,agir`. Todos estão vinculados nos documentos de arquitetura/RN/catálogo; testes específicos constam na matriz.
