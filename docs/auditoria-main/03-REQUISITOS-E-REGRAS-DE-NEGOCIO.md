# Requisitos e regras de negócio

Auditoria de 23/11/2026 · `main` · `c9785fa6b4656c73e3e35ac5db310c48e65d2fe5`.

[Índice](00-INDICE-GERAL.md) · [Pendências](09-PENDENCIAS-E-INCONSISTENCIAS.md)

## Requisitos e classificação

RF: autenticar, cadastrar contexto logístico, declarar carga, iniciar/finalizar sessão, adquirir histórico, preservar revisões, calcular potencial, avaliar ambiente, acompanhar alertas/decisões e simular intervenção humana. RNF: isolamento empresarial no backend, precisão Decimal, snapshots auditáveis, rollback, idempotência e testes locais reproduzíveis. Validação computacional não é validação biológica.

As regras abaixo são síntese vinculada a código e testes. “Validada na execução atual” refere-se aos testes locais relacionados aprovados; PostgreSQL histórico é separado. Requisitos condicionais e exceções estão descritos no próprio texto e nos erros extraídos ao final.

### RN-001 · AUTH

JWT ausente/inválido/expirado ou usuário inativo → 401; chave placeholder/curta impede autenticação com 503.

- Implementação: [app/modules/auth/service.py](../../app/modules/auth/service.py).
- Operações: `auth/login; auth/me e rotas privadas`.
- Teste: [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) · `test_invalid_jwt`.
- Resultado desta execução: {'passed': 7}.

### RN-002 · AUTH

ADMIN administra usuários/perfis; senha é hash Argon2, DTO de usuário não expõe senha_hash.

- Implementação: [app/api/routes/usuarios.py](../../app/api/routes/usuarios.py).
- Operações: `usuarios; perfis`.
- Teste: [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) · `test_non_admin_forbidden`.
- Resultado desta execução: {'passed': 3}.

### RN-003 · EMP

Não ADMIN depende de vínculo ativo; empresa inativa bloqueia detalhe. ADMIN global. Listagem usa repository específico, não regra genérica de perfil.

- Implementação: [app/modules/empresas/service.py](../../app/modules/empresas/service.py).
- Operações: `empresas`.
- Teste: [tests/test_auth_usuarios_empresas.py](../../tests/test_auth_usuarios_empresas.py) · `test_company_isolation`.
- Resultado desta execução: {'passed': 1}.

### RN-004 · LOG

Todas as 27 operações de logística/produtos exigem JWT; OPERADOR não altera frota; CONSULTA não escreve.

- Implementação: [app/modules/logistica/access.py](../../app/modules/logistica/access.py).
- Operações: `veiculos; motoristas; viagens; cargas; caixas; produtos`.
- Teste: [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) · `test_all_27_routes_reject_missing_invalid_or_expired_jwt`.
- Resultado desta execução: {'passed': 3}.

### RN-005 · LOG

Escopo vem da ancestralidade persistida; IDs enviados são referências, nunca autorização. SQL limita listagem antes de paginação.

- Implementação: [app/modules/logistica/access.py](../../app/modules/logistica/access.py).
- Operações: `viagens; cargas; caixas`.
- Teste: [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) · `test_unfiltered_and_explicit_lists_scope_before_pagination`.
- Resultado desta execução: {'passed': 3}.

### RN-006 · LOG

Catálogo global produtos/parâmetros: leitura quatro papéis, escrita somente ADMIN.

- Implementação: [app/modules/produtos/routes.py](../../app/modules/produtos/routes.py).
- Operações: `produtos`.
- Teste: [tests/test_seguranca_logistica.py](../../tests/test_seguranca_logistica.py) · `test_global_product_catalog_is_read_only_for_non_admin`.
- Resultado desta execução: {'passed': 3}.

### RN-007 · LOG

Viagem requer frota e motorista ativos da mesma transportadora; transições PLANEJADA→EM_ANDAMENTO/CANCELADA, EM_ANDAMENTO→CONCLUIDA. Estrutura iniciada é congelada.

- Implementação: [app/modules/logistica/service.py](../../app/modules/logistica/service.py).
- Operações: `viagens`.
- Teste: [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) (módulo completo; detalhamento na matriz de testes).
- Resultado desta execução: {'passed': 82}.

### RN-008 · LOG

Carga requer produto ativo, produtor de tipo PRODUTOR e cliente opcional CLIENTE; quantidade e unidade juntos. EM_TRANSITO exige viagem em andamento.

- Implementação: [app/modules/logistica/service.py](../../app/modules/logistica/service.py).
- Operações: `viagens/{id}/cargas; cargas/{id}`.
- Teste: [tests/test_logistica_operacional.py](../../tests/test_logistica_operacional.py) (módulo completo; detalhamento na matriz de testes).
- Resultado desta execução: {'passed': 82}.

### RN-009 · SESS

Massa líquida declarada válida, identidade Tommy Atkins explícita; não renomeia produto legado nem infere massa de caixas.

- Implementação: [app/modules/monitoramento/schemas.py](../../app/modules/monitoramento/schemas.py).
- Operações: `cargas/{id}/monitoramento`.
- Teste: [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) · `test_configure_preserves_legacy_cargo_and_product`.
- Resultado desta execução: {'passed': 1}.

### RN-010 · SESS

PUT repetido igual não cria versão/evento; alteração exige ausência de sessão ativa; snapshot terminal permanece.

- Implementação: [app/modules/monitoramento/service.py](../../app/modules/monitoramento/service.py).
- Operações: `cargas/{id}/monitoramento`.
- Teste: [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) · `test_config_put_is_idempotent_and_versioned`.
- Resultado desta execução: {'passed': 1}.

### RN-011 · SESS

Início exige viagem EM_ANDAMENTO, carga EM_TRANSITO e configuração; uma sessão ativa por carga e fonte sem sobreposição.

- Implementação: [app/modules/monitoramento/service.py](../../app/modules/monitoramento/service.py).
- Operações: `cargas/{id}/monitoramentos`.
- Teste: [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) · `test_same_source_cannot_monitor_two_cargos_simultaneously`.
- Resultado desta execução: {'passed': 1}.

### RN-012 · SESS

Sensores devem ter tipo/unidade/contexto compatíveis, dispositivo ativo e vínculo logístico. Sensor sem vínculo exige ADMIN e LABORATORIO.

- Implementação: [app/modules/monitoramento/service.py](../../app/modules/monitoramento/service.py).
- Operações: `cargas/{id}/monitoramentos`.
- Teste: [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) · `test_unbound_sensor_requires_admin_and_laboratory`.
- Resultado desta execução: {'passed': 1}.

### RN-013 · SESS

Encerrar/cancelar exige motivo e horário coerente; preserva janela; replay igual retorna estado sem novo evento. Cancelada reserva história.

- Implementação: [app/modules/monitoramento/service.py](../../app/modules/monitoramento/service.py).
- Operações: `monitoramentos/{id}/encerrar; cancelar`.
- Teste: [tests/test_monitoramento_sessoes.py](../../tests/test_monitoramento_sessoes.py) · `test_finish_is_audited_and_idempotent`.
- Resultado desta execução: {'passed': 2}.

### RN-014 · IOT

Canal global ThingSpeak é exclusivo ADMIN; não existe ownership de canal que autorize outra empresa.

- Implementação: [app/modules/integracoes/thingspeak/routes.py](../../app/modules/integracoes/thingspeak/routes.py).
- Operações: `integracoes/thingspeak/*`.
- Teste: [tests/test_seguranca_thingspeak.py](../../tests/test_seguranca_thingspeak.py) (módulo completo; detalhamento na matriz de testes).
- Resultado desta execução: {'passed': 36}.

### RN-015 · IOT

Fonte da sessão é fixada; alteração posterior de mapping não reinterpreta histórico; campos não relacionados não são importados.

- Implementação: [app/modules/monitoramento/historico_service.py](../../app/modules/monitoramento/historico_service.py).
- Operações: `sincronizacoes`.
- Teste: [tests/test_historico_iot.py](../../tests/test_historico_iot.py) · `test_binding_snapshot_does_not_follow_later_config_changes`.
- Resultado desta execução: {'passed': 1}.

### RN-016 · IOT

Deduplicação não duplica exposição; conflito gera revisão/ocorrência sem sobrescrever valor anterior; fora de ordem ordena por medida_em.

- Implementação: [app/modules/monitoramento/incorporacao_iot.py](../../app/modules/monitoramento/incorporacao_iot.py).
- Operações: `sincronizacoes; leituras`.
- Teste: [tests/test_historico_iot.py](../../tests/test_historico_iot.py) · `test_source_payload_conflict_creates_new_revision_not_a_value_overwrite`.
- Resultado desta execução: {'passed': 1}.

### RN-017 · IOT

Sessão encerrada só complementa com flag, justificativa e ADMIN/GESTOR; cancelada somente consulta; falha parcial é persistida e visível.

- Implementação: [app/modules/monitoramento/historico_service.py](../../app/modules/monitoramento/historico_service.py).
- Operações: `sincronizacoes`.
- Teste: [tests/test_historico_iot.py](../../tests/test_historico_iot.py) · `test_closed_session_requires_explicit_elevated_audited_complement`.
- Resultado desta execução: {'passed': 1}.

### RN-018 · IOT

Janela de leituras inclui amostra final para fechar intervalos; G explícito, dois extremos utilizáveis, sem preencher lacunas/bordas.

- Implementação: [app/modules/monitoramento/cobertura_iot.py](../../app/modules/monitoramento/cobertura_iot.py).
- Operações: `leituras; qualidade`.
- Teste: [tests/test_historico_iot.py](../../tests/test_historico_iot.py) · `test_temporal_gaps_are_not_filled`.
- Resultado desta execução: {'passed': 1}.

### RN-019 · ETI

V=Σq(T inicial)×massa_kg×duração_h; Decimal, referência geral quatro temperaturas; restrito sem interpolação, exploratório linear 10–20°C sem extrapolar.

- Implementação: [app/modules/monitoramento/etileno/motor.py](../../app/modules/monitoramento/etileno/motor.py).
- Operações: `analises-etileno`.
- Teste: [tests/test_etileno_motor.py](../../tests/test_etileno_motor.py) (módulo completo; detalhamento na matriz de testes).
- Resultado desta execução: {'passed': 96}.

### RN-020 · ETI

Ausência de dados não é zero. PARCIAL permite subtotal coberto mas total null; desconhecida/mista não corrige taxa; risco NAO_AVALIADO.

- Implementação: [app/modules/monitoramento/etileno/motor.py](../../app/modules/monitoramento/etileno/motor.py).
- Operações: `analises-etileno`.
- Teste: [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) · `test_gaps_are_partial_subtotal_never_window_total`.
- Resultado desta execução: {'passed': 1}.

### RN-021 · ETI

ATIVA exige corte explícito não futuro; revisão precisa estar consolidada; snapshot/hash imutáveis; consulta nunca recalcula.

- Implementação: [app/modules/monitoramento/analises_service.py](../../app/modules/monitoramento/analises_service.py).
- Operações: `analises-etileno`.
- Teste: [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) · `test_real_engine_called_once_and_get_never_recalculates`.
- Resultado desta execução: {'passed': 1}.

### RN-022 · ENV

Configuração nova somente ADMIN/GESTOR; versão imutável e maturação/ambiente explicitamente aplicáveis; min<max; UR 0–100.

- Implementação: [app/modules/monitoramento/preventivo_service.py](../../app/modules/monitoramento/preventivo_service.py).
- Operações: `configuracoes-ambientais`.
- Teste: [tests/test_preventivo.py](../../tests/test_preventivo.py) · `test_config_versions_immutable_and_old_evaluation_frozen`.
- Resultado desta execução: {'passed': 1}.

### RN-023 · ENV

Sem configuração aplicável → CONFIGURACAO_INSUFICIENTE; cobertura insuficiente → INCONCLUSIVO; nunca seguro por falta de dados.

- Implementação: [app/modules/monitoramento/preventivo_motor.py](../../app/modules/monitoramento/preventivo_motor.py).
- Operações: `avaliacoes-preventivas`.
- Teste: [tests/test_preventivo.py](../../tests/test_preventivo.py) · `test_no_readings_never_means_safe`.
- Resultado desta execução: {'passed': 1}.

### RN-024 · ENV

Faixas inclusivas; persistência fora da faixa exige dois extremos no mesmo lado, gap≤G; ponto isolado não prova duração. Umidade é ambiental, não entra em q(T).

- Implementação: [app/modules/monitoramento/preventivo_motor.py](../../app/modules/monitoramento/preventivo_motor.py).
- Operações: `avaliacoes-preventivas`.
- Teste: [tests/test_preventivo.py](../../tests/test_preventivo.py) · `test_isolated_outlier_does_not_prove_prolonged_exposure`.
- Resultado desta execução: {'passed': 1}.

### RN-025 · ALR

Evidência equivalente reutiliza alerta; caso aberto de regra/configuração recebe nova evidência; retorno à faixa não resolve automaticamente.

- Implementação: [app/modules/monitoramento/preventivo_service.py](../../app/modules/monitoramento/preventivo_service.py).
- Operações: `alertas; avaliacoes-preventivas`.
- Teste: [tests/test_preventivo.py](../../tests/test_preventivo.py) · `test_return_to_range_never_auto_resolves_alerts`.
- Resultado desta execução: {'passed': 1}.

### RN-026 · ALR

RECONHECER ABERTO→EM_ANALISE; RESOLVER/DESCARTAR → terminal; OBSERVAR adiciona nota inclusive terminal; toda ação tem ator/justificativa/ocorrência.

- Implementação: [app/modules/monitoramento/preventivo_service.py](../../app/modules/monitoramento/preventivo_service.py).
- Operações: `alertas/{id}/decisoes`.
- Teste: [tests/test_preventivo.py](../../tests/test_preventivo.py) · `test_decision_lifecycle_reuses_existing_alert_occurrence_models`.
- Resultado desta execução: {'passed': 1}.

### RN-027 · EXA

Solicitar não autoriza nem inicia; GESTOR/ADMIN autoriza/recusa/inicia; OPERADOR encerra própria execução ou cancela própria SOLICITADA. CONSULTA somente leitura.

- Implementação: [app/modules/monitoramento/exaustao_service.py](../../app/modules/monitoramento/exaustao_service.py).
- Operações: `intervencoes-simuladas; acoes`.
- Teste: [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) · `test_operator_cannot_make_privileged_decisions`.
- Resultado desta execução: {'passed': 4}.

### RN-028 · EXA

Somente uma EM_EXECUCAO por veículo; locks + índice parcial. Contexto alterado/terminal bloqueia iniciar, mas permite parada administrativa.

- Implementação: [app/modules/monitoramento/exaustao_service.py](../../app/modules/monitoramento/exaustao_service.py).
- Operações: `intervencoes-simuladas/{id}/acoes`.
- Teste: [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) · `test_one_vehicle_excludes_simultaneous_runs_from_different_sessions`.
- Resultado desta execução: {'passed': 1}.

### RN-029 · EXA

Prazo excedido é projeção; não existe scheduler de encerramento. Duração≤86400 na solicitação é didática; execução efetiva pode ultrapassar. Não altera ciência/alerta nem transmite comandos.

- Implementação: [app/modules/monitoramento/exaustao_service.py](../../app/modules/monitoramento/exaustao_service.py).
- Operações: `intervencoes-simuladas`.
- Teste: [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) · `test_no_automatic_actions_or_data_changes_when_time_passes`.
- Resultado desta execução: {'passed': 1}.

### RN-030 · EXA

GESTOR/ADMIN pode autorizar solicitação própria: não há aprovação por duas pessoas distintas. Tentativas de credencial na justificativa são rejeitadas.

- Implementação: [app/modules/monitoramento/exaustao_service.py](../../app/modules/monitoramento/exaustao_service.py).
- Operações: `intervencoes-simuladas/{id}/acoes`.
- Teste: [tests/test_exaustao_simulada.py](../../tests/test_exaustao_simulada.py) · `test_approval_by_admin_and_self_approval_policy_is_explicit`.
- Resultado desta execução: {'passed': 1}.

### RN-031 · TX

Idempotência valida autor+assinatura no escopo da operação; conflito 409; falha transacional não deve deixar estado/evento parcial.

- Implementação: [app/modules/monitoramento/analises_service.py](../../app/modules/monitoramento/analises_service.py).
- Operações: `operações idempotentes`.
- Teste: [tests/test_analises_etileno.py](../../tests/test_analises_etileno.py) · `test_transaction_failure_rolls_back_analysis_and_audit`.
- Resultado desta execução: {'passed': 2}.

### RN-032 · PG

Concorrência PostgreSQL exige conexões/PIDs distintos dentro do HTTP e verificação final em outra sessão; guardas de cluster proíbem fallback externo.

- Implementação: [tests/pg_support.py](../../tests/pg_support.py).
- Operações: `integração PostgreSQL opcional`.
- Teste: [tests/test_postgresql_real.py](../../tests/test_postgresql_real.py) (módulo completo; detalhamento na matriz de testes).
- Resultado desta execução: {'skipped': 12}.

## Inventário de rejeições do código

Todas as chamadas diretas a HTTPException identificadas estaticamente; helper `invalid`, validação Pydantic e constraints também podem rejeitar entradas. Não se pode inferir que cada erro é atingível em toda rota do módulo. Para vincular uma rota, seguir o handler e a dependência no catálogo.

| Origem | Rejeição implementada |
| --- | --- |
| [app/api/deps.py:30](../../app/api/deps.py#L30) | `HTTPException(403, 'Perfil sem permissao.')` |
| [app/modules/auth/service.py:14](../../app/modules/auth/service.py#L14) | `HTTPException(401, 'Credenciais invalidas.', headers={'WWW-Authenticate': 'Bearer'})` |
| [app/modules/auth/service.py:30](../../app/modules/auth/service.py#L30) | `HTTPException(503, 'Autenticacao nao configurada.')` |
| [app/modules/auth/service.py:39](../../app/modules/auth/service.py#L39) | `HTTPException(503, 'Autenticacao nao configurada.')` |
| [app/modules/empresas/service.py:27](../../app/modules/empresas/service.py#L27) | `HTTPException(404, 'Empresa nao encontrada.')` |
| [app/modules/empresas/service.py:37](../../app/modules/empresas/service.py#L37) | `HTTPException(403, 'Empresa inativa.')` |
| [app/modules/empresas/service.py:66](../../app/modules/empresas/service.py#L66) | `HTTPException(404, 'Usuario nao encontrado.')` |
| [app/modules/empresas/service.py:34](../../app/modules/empresas/service.py#L34) | `HTTPException(403, 'Acesso a empresa nao permitido.')` |
| [app/modules/empresas/service.py:54](../../app/modules/empresas/service.py#L54) | `HTTPException(409, 'Tipo de empresa incompativel com os vinculos logisticos existentes.')` |
| [app/modules/integracoes/thingspeak/routes.py:83](../../app/modules/integracoes/thingspeak/routes.py#L83) | `HTTPException(code, detail)` |
| [app/modules/integracoes/thingspeak/routes.py:30](../../app/modules/integracoes/thingspeak/routes.py#L30) | `HTTPException(503, 'Configuracao HTTP ThingSpeak invalida ou insegura.')` |
| [app/modules/integracoes/thingspeak/routes.py:70](../../app/modules/integracoes/thingspeak/routes.py#L70) | `HTTPException(503, 'ThingSpeak synchronization persistence failed.')` |
| [app/modules/logistica/access.py:24](../../app/modules/logistica/access.py#L24) | `HTTPException(403, 'Perfil sem permissao para esta operacao logistica.')` |
| [app/modules/logistica/access.py:29](../../app/modules/logistica/access.py#L29) | `HTTPException(409, 'Transportadora inativa nao permite escrita logistica.')` |
| [app/modules/logistica/service.py:17](../../app/modules/logistica/service.py#L17) | `HTTPException(404, 'Empresa nao encontrada.')` |
| [app/modules/monitoramento/analises_service.py:93](../../app/modules/monitoramento/analises_service.py#L93) | `HTTPException(404, 'Analise inexistente nesta sessao.')` |
| [app/modules/monitoramento/analises_service.py:88](../../app/modules/monitoramento/analises_service.py#L88) | `HTTPException(503, 'Falha ao confirmar a analise; consulte ou repita a mesma chave idempotente.')` |
| [app/modules/monitoramento/analises_service.py:29](../../app/modules/monitoramento/analises_service.py#L29) | `HTTPException(409, 'Sessao cancelada permite consultar analises anteriores, sem novas execucoes.')` |
| [app/modules/monitoramento/analises_service.py:31](../../app/modules/monitoramento/analises_service.py#L31) | `HTTPException(409, 'Sessao sem configuracao de carga rastreavel.')` |
| [app/modules/monitoramento/analises_service.py:34](../../app/modules/monitoramento/analises_service.py#L34) | `HTTPException(422, 'Sessao ativa exige corte_aquisicao explicito.')` |
| [app/modules/monitoramento/analises_service.py:36](../../app/modules/monitoramento/analises_service.py#L36) | `HTTPException(422, 'Corte de aquisicao nao pode estar no futuro.')` |
| [app/modules/monitoramento/analises_service.py:41](../../app/modules/monitoramento/analises_service.py#L41) | `HTTPException(422, 'Janela deve ser positiva e estar integralmente dentro da sessao e do corte.')` |
| [app/modules/monitoramento/analises_service.py:26](../../app/modules/monitoramento/analises_service.py#L26) | `HTTPException(409, 'Chave idempotente ja utilizada com outro autor ou parametros.')` |
| [app/modules/monitoramento/analises_service.py:52](../../app/modules/monitoramento/analises_service.py#L52) | `HTTPException(404, 'Revisao de aquisicao inexistente.')` |
| [app/modules/monitoramento/analises_service.py:54](../../app/modules/monitoramento/analises_service.py#L54) | `HTTPException(409, 'Revisao ainda nao consolidada no corte solicitado.')` |
| [app/modules/monitoramento/exaustao_service.py:40](../../app/modules/monitoramento/exaustao_service.py#L40) | `HTTPException(422, 'Justificativa contem possivel credencial; remova o segredo antes de registrar.')` |
| [app/modules/monitoramento/exaustao_service.py:59](../../app/modules/monitoramento/exaustao_service.py#L59) | `HTTPException(403, 'Perfil sem permissao para intervencoes simuladas.')` |
| [app/modules/monitoramento/exaustao_service.py:71](../../app/modules/monitoramento/exaustao_service.py#L71) | `HTTPException(409, 'Contexto da sessao mudou durante a operacao; repita a consulta.')` |
| [app/modules/monitoramento/exaustao_service.py:133](../../app/modules/monitoramento/exaustao_service.py#L133) | `HTTPException(409, 'Chave idempotente ja utilizada com outro autor ou parametros.')` |
| [app/modules/monitoramento/exaustao_service.py:228](../../app/modules/monitoramento/exaustao_service.py#L228) | `HTTPException(404, 'Intervencao inexistente nesta sessao.')` |
| [app/modules/monitoramento/exaustao_service.py:55](../../app/modules/monitoramento/exaustao_service.py#L55) | `HTTPException(503, 'Falha ao confirmar intervencao; consulte ou repita a mesma chave idempotente.')` |
| [app/modules/monitoramento/exaustao_service.py:82](../../app/modules/monitoramento/exaustao_service.py#L82) | `HTTPException(404, 'Alerta inexistente nesta sessao.')` |
| [app/modules/monitoramento/exaustao_service.py:93](../../app/modules/monitoramento/exaustao_service.py#L93) | `HTTPException(404, 'Avaliacao inexistente nesta sessao.')` |
| [app/modules/monitoramento/exaustao_service.py:96](../../app/modules/monitoramento/exaustao_service.py#L96) | `HTTPException(409, 'Avaliacao indicada nao sustenta o alerta selecionado.')` |
| [app/modules/monitoramento/exaustao_service.py:101](../../app/modules/monitoramento/exaustao_service.py#L101) | `HTTPException(404, 'Analise inexistente nesta sessao.')` |
| [app/modules/monitoramento/exaustao_service.py:149](../../app/modules/monitoramento/exaustao_service.py#L149) | `HTTPException(409, 'Nova solicitacao exige sessao/logistica ativas e alerta nao terminal/compativel, quando indicado.')` |
| [app/modules/monitoramento/exaustao_service.py:181](../../app/modules/monitoramento/exaustao_service.py#L181) | `HTTPException(403, 'Acao exige GESTOR/ADMIN ou responsabilidade de encerramento/retirada da propria solicitacao.')` |
| [app/modules/monitoramento/exaustao_service.py:183](../../app/modules/monitoramento/exaustao_service.py#L183) | `HTTPException(409, 'Transicao de intervencao invalida; terminal nao pode ser reaberto.')` |
| [app/modules/monitoramento/exaustao_service.py:187](../../app/modules/monitoramento/exaustao_service.py#L187) | `HTTPException(409, 'Autorizacao/inicio exige sessao/logistica ativas e contexto/alerta compativeis.')` |
| [app/modules/monitoramento/exaustao_service.py:190](../../app/modules/monitoramento/exaustao_service.py#L190) | `HTTPException(409, 'Exaustor virtual deste veiculo ja esta em execucao.')` |
| [app/modules/monitoramento/exaustao_service.py:193](../../app/modules/monitoramento/exaustao_service.py#L193) | `HTTPException(409, 'Relogio anterior ao ultimo evento; transicao nao registrada.')` |
| [app/modules/monitoramento/exaustao_service.py:105](../../app/modules/monitoramento/exaustao_service.py#L105) | `HTTPException(409, 'Analise e avaliacao devem ter a mesma janela e revisao.')` |
| [app/modules/monitoramento/historico_consulta.py:33](../../app/modules/monitoramento/historico_consulta.py#L33) | `HTTPException(422, 'Janela de consulta invalida.')` |
| [app/modules/monitoramento/historico_consulta.py:23](../../app/modules/monitoramento/historico_consulta.py#L23) | `HTTPException(404, 'Revisao de aquisicao inexistente.')` |
| [app/modules/monitoramento/historico_consulta.py:24](../../app/modules/monitoramento/historico_consulta.py#L24) | `HTTPException(409, 'Revisao em execucao ainda nao esta consolidada.')` |
| [app/modules/monitoramento/historico_consulta.py:28](../../app/modules/monitoramento/historico_consulta.py#L28) | `HTTPException(422, 'Inicio de consulta fora da sessao.')` |
| [app/modules/monitoramento/historico_consulta.py:31](../../app/modules/monitoramento/historico_consulta.py#L31) | `HTTPException(422, 'Fim de consulta fora da sessao/corte de aquisicao.')` |
| [app/modules/monitoramento/historico_routes.py:25](../../app/modules/monitoramento/historico_routes.py#L25) | `HTTPException(409, 'Configuracao ThingSpeak invalida; nenhum segredo e retornado.')` |
| [app/modules/monitoramento/historico_service.py:36](../../app/modules/monitoramento/historico_service.py#L36) | `HTTPException(409, 'Sessao cancelada permite consulta, mas nao incorporacao de leituras.')` |
| [app/modules/monitoramento/historico_service.py:48](../../app/modules/monitoramento/historico_service.py#L48) | `HTTPException(409, 'Canal ThingSpeak nao configurado.')` |
| [app/modules/monitoramento/historico_service.py:51](../../app/modules/monitoramento/historico_service.py#L51) | `HTTPException(409, 'Identificador de canal invalido.')` |
| [app/modules/monitoramento/historico_service.py:39](../../app/modules/monitoramento/historico_service.py#L39) | `HTTPException(409, 'Sessao encerrada exige complementacao explicita e justificada.')` |
| [app/modules/monitoramento/historico_service.py:41](../../app/modules/monitoramento/historico_service.py#L41) | `HTTPException(403, 'Complementacao de sessao encerrada exige ADMIN ou GESTOR.')` |
| [app/modules/monitoramento/historico_service.py:59](../../app/modules/monitoramento/historico_service.py#L59) | `HTTPException(409, 'Mapeamento ausente ou ambiguo para um sensor da sessao.')` |
| [app/modules/monitoramento/historico_service.py:65](../../app/modules/monitoramento/historico_service.py#L65) | `HTTPException(409, 'Mapeamento incompativel com o snapshot; corrija a configuracao antes de sincronizar.')` |
| [app/modules/monitoramento/historico_service.py:105](../../app/modules/monitoramento/historico_service.py#L105) | `HTTPException(422, 'Periodo solicitado deve estar dentro da janela da sessao.')` |
| [app/modules/monitoramento/historico_service.py:84](../../app/modules/monitoramento/historico_service.py#L84) | `HTTPException(409, 'Chave idempotente reutilizada com outro conteudo ou autor.')` |
| [app/modules/monitoramento/historico_service.py:95](../../app/modules/monitoramento/historico_service.py#L95) | `HTTPException(409, 'Ja existe sincronizacao em execucao para a sessao.')` |
| [app/modules/monitoramento/historico_service.py:171](../../app/modules/monitoramento/historico_service.py#L171) | `HTTPException(409, 'Janela alterada durante a aquisicao.')` |
| [app/modules/monitoramento/preventivo_service.py:50](../../app/modules/monitoramento/preventivo_service.py#L50) | `HTTPException(409, 'Chave idempotente ja usada com outro autor ou parametros.')` |
| [app/modules/monitoramento/preventivo_service.py:53](../../app/modules/monitoramento/preventivo_service.py#L53) | `HTTPException(422, 'Sessao ativa exige corte_aquisicao explicito.')` |
| [app/modules/monitoramento/preventivo_service.py:59](../../app/modules/monitoramento/preventivo_service.py#L59) | `HTTPException(422, 'Janela positiva deve estar integralmente na sessao e no corte nao futuro.')` |
| [app/modules/monitoramento/preventivo_service.py:174](../../app/modules/monitoramento/preventivo_service.py#L174) | `HTTPException(404, 'Alerta inexistente nesta sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:223](../../app/modules/monitoramento/preventivo_service.py#L223) | `HTTPException(404, 'Avaliacao inexistente nesta sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:26](../../app/modules/monitoramento/preventivo_service.py#L26) | `HTTPException(503, 'Falha ao confirmar operacao; consulte ou repita a mesma chave idempotente.')` |
| [app/modules/monitoramento/preventivo_service.py:31](../../app/modules/monitoramento/preventivo_service.py#L31) | `HTTPException(403, 'Configuracao exige ADMIN ou GESTOR.')` |
| [app/modules/monitoramento/preventivo_service.py:37](../../app/modules/monitoramento/preventivo_service.py#L37) | `HTTPException(409, 'Sessao cancelada nao recebe nova configuracao.')` |
| [app/modules/monitoramento/preventivo_service.py:39](../../app/modules/monitoramento/preventivo_service.py#L39) | `HTTPException(409, 'Configuracao deve incluir explicitamente maturacao e ambiente da sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:94](../../app/modules/monitoramento/preventivo_service.py#L94) | `HTTPException(404, 'Analise de etileno inexistente nesta sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:96](../../app/modules/monitoramento/preventivo_service.py#L96) | `HTTPException(409, 'Analise contextual deve corresponder a mesma janela e revisao.')` |
| [app/modules/monitoramento/preventivo_service.py:117](../../app/modules/monitoramento/preventivo_service.py#L117) | `HTTPException(409, 'Sessao cancelada preserva consultas/decisoes, sem novas avaliacoes.')` |
| [app/modules/monitoramento/preventivo_service.py:68](../../app/modules/monitoramento/preventivo_service.py#L68) | `HTTPException(404, 'Revisao inexistente nesta sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:70](../../app/modules/monitoramento/preventivo_service.py#L70) | `HTTPException(409, 'Revisao nao consolidada no corte.')` |
| [app/modules/monitoramento/preventivo_service.py:122](../../app/modules/monitoramento/preventivo_service.py#L122) | `HTTPException(404, 'Configuracao inexistente nesta sessao.')` |
| [app/modules/monitoramento/preventivo_service.py:123](../../app/modules/monitoramento/preventivo_service.py#L123) | `HTTPException(409, 'Configuracao ainda nao existia no corte.')` |
| [app/modules/monitoramento/preventivo_service.py:198](../../app/modules/monitoramento/preventivo_service.py#L198) | `HTTPException(409, 'Transicao de alerta invalida; estado terminal nao e reaberto automaticamente.')` |
| [app/modules/monitoramento/service.py:55](../../app/modules/monitoramento/service.py#L55) | `HTTPException(404, 'Registro nao encontrado.')` |
| [app/modules/monitoramento/service.py:60](../../app/modules/monitoramento/service.py#L60) | `HTTPException(403, 'Usuario sem permissao para monitoramento.')` |
| [app/modules/monitoramento/service.py:63](../../app/modules/monitoramento/service.py#L63) | `HTTPException(403, 'Perfil sem permissao para esta operacao.')` |
| [app/modules/monitoramento/service.py:66](../../app/modules/monitoramento/service.py#L66) | `HTTPException(409, 'Transportadora inativa.')` |
| [app/modules/monitoramento/service.py:119](../../app/modules/monitoramento/service.py#L119) | `HTTPException(404, 'Carga ainda nao configurada para monitoramento.')` |
| [app/modules/monitoramento/service.py:125](../../app/modules/monitoramento/service.py#L125) | `HTTPException(422, 'Sensores de temperatura e umidade devem ser distintos.')` |
| [app/modules/monitoramento/service.py:218](../../app/modules/monitoramento/service.py#L218) | `HTTPException(422, 'Estado final invalido.')` |
| [app/modules/monitoramento/service.py:44](../../app/modules/monitoramento/service.py#L44) | `HTTPException(409, 'Conflito de integridade ou requisicao simultanea; consulte o estado e tente novamente.')` |
| [app/modules/monitoramento/service.py:75](../../app/modules/monitoramento/service.py#L75) | `HTTPException(409, 'O vinculo da carga foi alterado; repita a operacao.')` |
| [app/modules/monitoramento/service.py:97](../../app/modules/monitoramento/service.py#L97) | `HTTPException(409, 'Carga ou viagem encerrada nao permite alterar a declaracao.')` |
| [app/modules/monitoramento/service.py:99](../../app/modules/monitoramento/service.py#L99) | `HTTPException(409, 'Produto cadastrado esta inativo.')` |
| [app/modules/monitoramento/service.py:101](../../app/modules/monitoramento/service.py#L101) | `HTTPException(409, 'Encerre a sessao ativa antes de alterar os dados da carga.')` |
| [app/modules/monitoramento/service.py:141](../../app/modules/monitoramento/service.py#L141) | `HTTPException(422, 'Tipo de sensor incompativel com a funcao selecionada.')` |
| [app/modules/monitoramento/service.py:144](../../app/modules/monitoramento/service.py#L144) | `HTTPException(422, 'Unidade do sensor nao suportada.')` |
| [app/modules/monitoramento/service.py:146](../../app/modules/monitoramento/service.py#L146) | `HTTPException(409, 'Sensor ou dispositivo nao esta ativo.')` |
| [app/modules/monitoramento/service.py:149](../../app/modules/monitoramento/service.py#L149) | `HTTPException(409, 'Dispositivo vinculado a outro contexto logistico.')` |
| [app/modules/monitoramento/service.py:154](../../app/modules/monitoramento/service.py#L154) | `HTTPException(422, 'Sensor de prototipo nao comprova aquisicao em transporte refrigerado.')` |
| [app/modules/monitoramento/service.py:177](../../app/modules/monitoramento/service.py#L177) | `HTTPException(409, 'Configure os dados de monitoramento da carga primeiro.')` |
| [app/modules/monitoramento/service.py:179](../../app/modules/monitoramento/service.py#L179) | `HTTPException(409, 'Inicio exige viagem em andamento e carga em transito.')` |
| [app/modules/monitoramento/service.py:181](../../app/modules/monitoramento/service.py#L181) | `HTTPException(409, 'Produto cadastrado esta inativo.')` |
| [app/modules/monitoramento/service.py:184](../../app/modules/monitoramento/service.py#L184) | `HTTPException(422, 'Inicio efetivo nao pode estar no futuro.')` |
| [app/modules/monitoramento/service.py:186](../../app/modules/monitoramento/service.py#L186) | `HTTPException(422, 'Sessao exige inicio real da viagem anterior ou igual.')` |
| [app/modules/monitoramento/service.py:190](../../app/modules/monitoramento/service.py#L190) | `HTTPException(409, 'Janela conflitante com outra sessao da carga ou dos sensores.')` |
| [app/modules/monitoramento/service.py:227](../../app/modules/monitoramento/service.py#L227) | `HTTPException(409, 'Sessao finalizada e imutavel; nao pode ser reaberta ou alterada.')` |
| [app/modules/monitoramento/service.py:229](../../app/modules/monitoramento/service.py#L229) | `HTTPException(422, 'Fim deve ser posterior ao inicio e nao estar no futuro.')` |
| [app/modules/monitoramento/service.py:231](../../app/modules/monitoramento/service.py#L231) | `HTTPException(422, 'Fim da sessao posterior a chegada real da viagem.')` |
| [app/modules/monitoramento/service.py:233](../../app/modules/monitoramento/service.py#L233) | `HTTPException(409, 'Viagem cancelada exige cancelamento da sessao.')` |
| [app/modules/monitoramento/service.py:152](../../app/modules/monitoramento/service.py#L152) | `HTTPException(403, 'Sensor sem contexto logistico exige ADMIN e ambiente de laboratorio.')` |
| [app/modules/monitoramento/service.py:173](../../app/modules/monitoramento/service.py#L173) | `HTTPException(409, 'Chave idempotente reutilizada com conteudo diferente.')` |
| [app/modules/produtos/service.py:24](../../app/modules/produtos/service.py#L24) | `HTTPException(404, 'Parametro nao pertence ao produto.')` |
| [app/repositories/operacional.py:37](../../app/repositories/operacional.py#L37) | `HTTPException(409, 'Identificador duplicado ou relacionamento invalido.')` |
| [app/services/operacional.py:5](../../app/services/operacional.py#L5) | `HTTPException(422, message)` |
| [app/services/operacional.py:18](../../app/services/operacional.py#L18) | `HTTPException(404, 'Registro nao encontrado.')` |
| [app/services/persistence.py:11](../../app/services/persistence.py#L11) | `HTTPException(409, 'Registro duplicado ou vinculo invalido.')` |
| [app/services/usuarios.py:22](../../app/services/usuarios.py#L22) | `HTTPException(404, 'Usuario nao encontrado.')` |
| [app/services/usuarios.py:27](../../app/services/usuarios.py#L27) | `HTTPException(409, 'Email ja cadastrado.')` |
| [app/services/usuarios.py:29](../../app/services/usuarios.py#L29) | `HTTPException(404, 'Perfil nao encontrado.')` |
| [app/services/usuarios.py:47](../../app/services/usuarios.py#L47) | `HTTPException(404, 'Perfil nao encontrado.')` |
| [app/services/usuarios.py:45](../../app/services/usuarios.py#L45) | `HTTPException(409, 'Email ja cadastrado.')` |


## Limitações científicas implementadas

Tabela de referência em [app/modules/monitoramento/etileno/parametros.py](../../app/modules/monitoramento/etileno/parametros.py): 10°C [0,1;0,5], 13°C [0,2;1], 15°C [0,3;4], 20°C [0,5;8] µL·kg⁻¹·h⁻¹. A referência UC Davis é registrada no código, sem nova revisão bibliográfica nesta auditoria. O documento [docs/chicosense/modelo-cientifico.md](../../docs/chicosense/modelo-cientifico.md) é a especificação anterior; afirmações de atividade futura nele não anulam a implementação atual.

Horas=segundos/3600; 1000 µL=1 mL. Ambos os extremos de cada par precisam ser utilizáveis; usa-se T do primeiro. Leituras inválidas/conflitantes interrompem a integração, não se procura o próximo ponto atravessando barreira. Massa e maturação vêm do snapshot da sessão. Sem extrapolação, sem preenchimento de bordas, sem limiar de volume para risco. Exemplo em 1000 kg, 1h a 13°C + 1h a 20°C: [200+500;1000+8000]=[700;9000] µL. Maturação MISTA/DESCONHECIDA conserva aritmética e explicita limitação. UR não entra no volume, tampouco exaustão simulada.
