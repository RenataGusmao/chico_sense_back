# PostgreSQL real — execução opcional

**Qualificado em PostgreSQL 17.11 local (29/10/2026): 757 aprovados, zero falhas/skips.**
Os 12 casos PostgreSQL e três repetições de nove testes concorrentes passaram.
Fora do ambiente opcional configurado, skip continua significando pendência.
O ambiente padrão não usa DATABASE_URL para estes testes nem conecta ao Supabase.
Consultar também [docs/chicosense/validacao.md](../docs/chicosense/validacao.md)
para resultados e limites; relatórios históricos detalhados ficam fora do Git.

## Travas

Exigir no processo, nunca no .env:

- CHICOSENSE_TEST_DATABASE_URL: driver postgresql+psycopg, IP literal 127.0.0.1/::1,
  porta explícita >=1024, usuário chicosense_test_user, senha dedicada e banco
  chicosense_test_<token>. Query parameters são proibidos (inclusive service/host).
- CHICOSENSE_TEST_DISPOSABLE_TOKEN: 32 dígitos hexadecimais minúsculos.
- CHICOSENSE_TEST_SYSTEM_IDENTIFIER: identidade obtida separadamente **no cluster
  local recém-criado**, não aprendida automaticamente de um destino desconhecido.

Falta completa: skip. Configuração parcial/inválida: erro. Nenhum fallback remoto.
Hostaddr também é fixado, impedindo redirecionamento por PGHOSTADDR.
Antes de DDL/TRUNCATE: conferir database, usuário/proprietário, comentário
chicosense-disposable:<token>, identidade pg_control_system, versão >=14 e recovery
inativo. Ausência de privilégio de inspeção bloqueia execução.
O bootstrap recusa objetos/tipos/funções existentes em public, schemas particulares
ou extensões adicionais. Advisory lock impede duas suítes no mesmo banco. Limpeza
exige inventário exato das tabelas conhecidas e não usa CASCADE. Não há DROP DATABASE.
Não compartilhar esse cluster com aplicações ou outras conexões durante os testes.

## Roteiro para disponibilizar outro cluster novo no Windows

Nesta máquina foi usado PostgreSQL portátil em diretório próprio, sem registrar
serviço. O roteiro abaixo serve para outro cluster novo; não recrie o cluster preservado. A página oficial aponta para ZIPs EDB sem instalador:
[PostgreSQL Windows](https://www.postgresql.org/download/windows/).
Baixar/verificar um ZIP x64 PostgreSQL 17.x compatível com o Windows. Se faltar runtime
do sistema, parar e obter autorização específica; não instalar globalmente.
Substituir somente o caminho do ZIP abaixo. Confirmar que a porta 35432 está livre.

```powershell
$testToken = [guid]::NewGuid().ToString('N')
$testDb = "chicosense_test_$testToken"
$pgTaskRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("chicosense-pg-tests-$testToken")
$pgArchive = 'C:\CAMINHO\postgresql-17-windows-x64-binaries.zip'
New-Item -ItemType Directory -Path $pgTaskRoot -ErrorAction Stop | Out-Null
Expand-Archive -LiteralPath $pgArchive -DestinationPath $pgTaskRoot -ErrorAction Stop
$pgBin = Join-Path $pgTaskRoot 'pgsql\bin'
$pgData = Join-Path $pgTaskRoot 'data'
$pgPasswordFile = Join-Path $pgTaskRoot 'test-password.tmp'
$pgTestPassword = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
Set-Content -LiteralPath $pgPasswordFile -Value $pgTestPassword -NoNewline -Encoding ascii
& "$pgBin\initdb.exe" -D $pgData -U chicosense_test_user --auth=scram-sha-256 --encoding=UTF8 --locale=C --pwfile=$pgPasswordFile
if ($LASTEXITCODE -ne 0) { throw 'initdb falhou' }
& "$pgBin\pg_ctl.exe" -D $pgData -l "$pgTaskRoot\postgres.log" -o '-h 127.0.0.1 -p 35432' -w start
if ($LASTEXITCODE -ne 0) { throw 'Instância nova não iniciou; não reutilizar servidor existente' }
```

Usar o executável desse diretório e confirmar o data recém-criado. A conta de bootstrap
é superusuário **somente deste cluster descartável**, para inspecionar a identidade;
não copiar permissões para produção. Executar da raiz do backend:

```powershell
$pgPreviousPassword = $env:PGPASSWORD
$pgPreviousHostaddr = $env:PGHOSTADDR
try {
    $env:PGPASSWORD = $pgTestPassword
    $env:PGHOSTADDR = '127.0.0.1'
    & "$pgBin\createdb.exe" -h 127.0.0.1 -p 35432 -U chicosense_test_user $testDb
    if ($LASTEXITCODE -ne 0) { throw 'createdb falhou' }
    & "$pgBin\psql.exe" -h 127.0.0.1 -p 35432 -U chicosense_test_user -d $testDb -v ON_ERROR_STOP=1 -c "COMMENT ON DATABASE $testDb IS 'chicosense-disposable:$testToken';"
    if ($LASTEXITCODE -ne 0) { throw 'Marcação falhou' }
    $pgSystemId = (& "$pgBin\psql.exe" -h 127.0.0.1 -p 35432 -U chicosense_test_user -d $testDb -At -v ON_ERROR_STOP=1 -c 'SELECT system_identifier FROM pg_control_system();').Trim()
    if ($LASTEXITCODE -ne 0 -or $pgSystemId -notmatch '^\d{10,20}$') { throw 'Identidade não confirmada' }
    $env:CHICOSENSE_TEST_DATABASE_URL = "postgresql+psycopg://chicosense_test_user:${pgTestPassword}@127.0.0.1:35432/$testDb"
    $env:CHICOSENSE_TEST_DISPOSABLE_TOKEN = $testToken
    $env:CHICOSENSE_TEST_SYSTEM_IDENTIFIER = $pgSystemId
    .\.venv\Scripts\python.exe -B -m pytest tests/test_postgresql_real.py -v -rs -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { throw 'Testes falharam; preservar cluster/logs para diagnóstico' }
} finally {
    $env:PGPASSWORD = $pgPreviousPassword
    $env:PGHOSTADDR = $pgPreviousHostaddr
    Remove-Item Env:CHICOSENSE_TEST_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:CHICOSENSE_TEST_DISPOSABLE_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:CHICOSENSE_TEST_SYSTEM_IDENTIFIER -ErrorAction SilentlyContinue
    & "$pgBin\pg_ctl.exe" -D $pgData -m fast -w stop
}
```

Nenhuma DATABASE_URL existente é alterada. Não imprimir senha/DSN. Após revisar os
resultados, remover apenas a senha fictícia com Remove-Item -LiteralPath $pgPasswordFile.
O cluster fica parado para inspeção; não há exclusão recursiva. Não versionar dados,
binários, senha nem log. Para repetir, criar **outro banco vazio/token**; o bootstrap
recusa tabelas pré-existentes. Nunca executar alembic CLI com o .env atual.

Alternativa, se disponibilizado/aprovado: Docker com postgres:17 e publicação
127.0.0.1:35432:5432, sem dados existentes, mesmos usuário/banco/marcador e identidade
obtida via docker exec no container específico. Instalação Docker/WSL é separada.

## Casos e configuração das requests

O módulo test_postgresql_real.py tem 12 casos: cadeia completa upgrade/downgrade/
upgrade; catálogo versus ORM; FK/CHECK e rollback; sessões concorrentes (criar e
encerrar); aquisição mesma chave; deduplicação/revisões entre transações; análise
idempotente com resultado 700–9000 µL; complemento tardio preservando snapshot;
alertas equivalentes e decisões concorrentes; duas sessões/viagens iniciando no
mesmo veículo; encerramento versus início de outra intervenção.

Cada corrida abre duas conexões antes da barreira e confere PIDs distintos. ContextVar
transmite a conexão ao HTTP; a dependência de banco verifica pg_backend_pid dentro
de cada request. Cada requisição tem sua Session. Asserções finais usam outra Session
e registros persistidos, incluindo eventos, decisões e ações, não apenas HTTP.
Barreiras ficam antes dos locks; há timeouts de conexão/lock/statement/futuros.
Não usar pytest-xdist neste ambiente. Repetir corridas após uma primeira rodada verde.
JWT/domínio/SQL são reais quando PostgreSQL existir; somente o provedor ThingSpeak
é mockado. A coleta/skip não comprova funcionamento deste suporte nem do PostgreSQL.


## Metadata, auditoria e autogenerate

As requests usam SessionLocal da aplicação, substituindo somente o bind pelo
engine/conexão de teste verificado. A Session de seed permanece separada. Não
alterar expire_on_commit/autoflush das requests para facilitar testes de replay.
O caso de decisões considera o baseline CRIAR, preserva seus IDs e exige exatamente
o acréscimo das transições bem-sucedidas, sem decisões/ocorrências duplicadas.

O metadata de usuários preserva UNIQUE(email), ix_usuarios_email não único e o
índice funcional único de normalização. A comparação de catálogo confere
expressões e predicados pelo parser/deparser PostgreSQL, incluindo os índices
refletidos com column_names=[null], sem dispensar sua unicidade.

Alembic 1.13.2 pode propor remove_index/add_index redundante para o mesmo índice
funcional devido a trim(email) versus TRIM(BOTH FROM email). O teste verifica
estritamente esse par e sua equivalência, rejeitando qualquer outro diff e também
a expressão sem trim. Não há hook global nem alteração em migrations. Revisar
revision --autogenerate manualmente e não aplicar essa recriação desnecessária.
