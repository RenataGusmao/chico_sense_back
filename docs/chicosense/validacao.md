# Validação e reprodução do ChicoSense

Qualificação em 29/10/2026, PostgreSQL portátil **17.11**, distribuição EDB 17.11-5
Windows x64. **757 testes aprovados, zero falhas/skips e um warning conhecido.**
A suíte contém 12 testes reais PostgreSQL, além dos testes puros/SQLite/HTTP mockado.
Não houve aquisição física, acesso ao Supabase ou deploy nessa qualificação.

## Evidências técnicas

- Cadeia inicial 20260930_0001 → head única 20261028_0010_exaustao_virtual.
- Upgrade completo, downgrade base sem enums residuais e novo upgrade.
- 34 tabelas ORM, 411 colunas, 91 FKs, 31 CHECKs e dez enums inspecionados.
- UUID, JSONB, NUMERIC, índices parciais, unicidade e rollback exercitados no servidor.
- Mesma chave de análise: respostas exatamente iguais, uma análise e um evento,
  snapshot/hash preservados, resultado hipotético 700–9000 µL.
- Decisões incluem CRIAR e somam somente transições confirmadas ao baseline.
- Veículo não mantém duas execuções virtuais ativas, mesmo entre sessões distintas.

Depois dos 12 verdes foram executadas três rodadas de nove testes concorrentes,
cada uma em outro banco vazio. Dez corridas por rodada (alertas têm duas).
Qualificação final: 10 corridas iniciais +30 nas repetições +10 na suíte completa
= **50 corridas entre conexões independentes**. PIDs foram conferidos dentro do HTTP;
estado final foi consultado em outra Session. As repetições não aumentam o número
de casos únicos. Asserções não se limitam aos códigos HTTP.

| Execução | Resultado |
|---|---|
| PostgreSQL dedicado | 12 aprovados, 35,27 s |
| Concorrência 1/2/3 | 9 aprovados cada; 29,79/31,53/32,46 s |
| Suíte completa com PostgreSQL | 757 aprovados, 270,95 s |

O warning conhecido é a depreciação BlockingPortal em Starlette/TestClient.

## Reprodução segura

```powershell
python -B -m pytest -q -rs -p no:cacheprovider
```

Sem o ambiente opcional PostgreSQL: **745 aprovados e 12 skips**. Isso não comprova
PostgreSQL nessa execução. A qualificação real exige os três opt-ins, identidade
e marcador do banco descartável, schema inicialmente vazio e conexões independentes.
Usar [o procedimento completo](../../tests/POSTGRESQL.md) e a trava
[scripts/pg_test_safety.py](../../scripts/pg_test_safety.py). Nunca fornecer a URL da
aplicação ou um banco previamente ocupado como substituto do banco de teste.

Um novo banco é necessário para cada rodada, mesmo reutilizando o cluster dedicado.
Os diretórios/credenciais/logs da execução local permanecem fora do Git; não são
pré-requisito oculto para executar os testes ou justificativa para ignorar a trava.

## Efeito conhecido de autogenerate

O metadata preserva UNIQUE(email), ix_usuarios_email não único e o índice funcional
único de e-mail normalizado. Alembic 1.13.2 pode propor remove_index/add_index
redundante devido à grafia trim(email)/TRIM(BOTH FROM email). O teste confere o
índice inteiro, sua unicidade e equivalência de expressão no PostgreSQL; também
rejeita remover trim. Outras diferenças continuam falhando. Revisar manualmente
futuras migrations autogeradas; não aplicar essa recriação desnecessária.
Nenhuma migration histórica foi reescrita para produzir esse resultado.

## Limites e integração

Os 96 testes do motor científico verificam o cálculo determinístico, não validam
experimentalmente a cultivar. A avaliação ambiental é operacional. HTTP ThingSpeak
é mockado nos testes; a intervenção é exclusivamente virtual. Sensores/calibração,
ventilação real, concentração e eficácia exigem validação própria.

[Contratos do frontend](contratos-api.md), [exemplos hipotéticos](exemplos-frontend.json)
e [demonstração automatizada](demonstracao.md) documentam os fluxos existentes.
O snapshot [OpenAPI](openapi.json) foi comparado ao schema vivo ao consolidar e era
idêntico; uma mudança de contrato exige nova revisão do snapshot e desses documentos.

Os relatórios históricos completos e logs de auditoria são preservados no workspace
da entrega, não incorporados ao repositório. O resultado acima registra a execução
real anterior à organização dos commits; alterações apenas documentais/organização
não são apresentadas como uma nova execução do servidor PostgreSQL.
