# Ожидает доступность ВМ и выполняет полный деплой Foodgram.
$ErrorActionPreference = 'Stop'
$HostIP = '81.26.183.233'
$SshUser = 'ubuntu'
$KeyPath = "$env:USERPROFILE\.ssh\foodgram_vm"
$Archive = "$env:TEMP\foodgram.tar.gz"
$ProjectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (Test-Path (Join-Path (Split-Path $PSScriptRoot -Parent) 'backend')) {
    $ProjectRoot = Split-Path $PSScriptRoot -Parent
}

Write-Host "=== Foodgram deploy ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot"

$bundle = "$env:TEMP\foodgram-bundle"
Remove-Item $bundle -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $bundle -Force | Out-Null
Copy-Item "$ProjectRoot\backend","$ProjectRoot\frontend","$ProjectRoot\infra","$ProjectRoot\docs","$ProjectRoot\data","$ProjectRoot\postman_collection" -Destination $bundle -Recurse -Force
Copy-Item "$ProjectRoot\tests.yml","$ProjectRoot\setup.cfg" -Destination $bundle -ErrorAction SilentlyContinue
Remove-Item $Archive -Force -ErrorAction SilentlyContinue
tar -czf $Archive -C $bundle .
Write-Host "Archive: $Archive ($((Get-Item $Archive).Length) bytes)"

$maxAttempts = 60
for ($i = 1; $i -le $maxAttempts; $i++) {
    Write-Host "[$i/$maxAttempts] Checking $HostIP ..."
    $ping = Test-Connection -ComputerName $HostIP -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($ping) {
        $sshTest = ssh -i $KeyPath -o ConnectTimeout=10 -o BatchMode=yes "${SshUser}@${HostIP}" "echo OK" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "VM is online." -ForegroundColor Green
            break
        }
    }
    if ($i -eq $maxAttempts) {
        Write-Host "VM not reachable. Start VM in Yandex Cloud: r-backend-vm-1670829377" -ForegroundColor Red
        exit 1
    }
    Start-Sleep -Seconds 15
}

Write-Host "Uploading archive..."
scp -i $KeyPath -o StrictHostKeyChecking=accept-new $Archive "${SshUser}@${HostIP}:/tmp/foodgram.tar.gz"

Write-Host "Deploying on server..."
$deployScript = @'
set -e
ARCHIVE=/tmp/foodgram.tar.gz
test -f "$ARCHIVE"
mkdir -p "$HOME/foodgram"
[ -f "$HOME/foodgram/infra/.env" ] && cp "$HOME/foodgram/infra/.env" /tmp/foodgram.env.bak
tar xzf "$ARCHIVE" -C "$HOME/foodgram"
[ -f /tmp/foodgram.env.bak ] && cp /tmp/foodgram.env.bak "$HOME/foodgram/infra/.env"
[ ! -f "$HOME/foodgram/infra/.env" ] && cp "$HOME/foodgram/infra/.env.production.example "$HOME/foodgram/infra/.env"
sed -i 's/\r$//' "$HOME/foodgram/backend/entrypoint.sh"
chmod +x "$HOME/foodgram/backend/entrypoint.sh"
mkdir -p "$HOME/foodgram/backend/data"
test -f "$HOME/foodgram/backend/data/ingredients.csv" || cp "$HOME/foodgram/data/ingredients.csv" "$HOME/foodgram/backend/data/" 2>/dev/null || true
cd "$HOME/foodgram/infra"
sed -i "s/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=81.26.183.233,127.0.0.1,localhost,backend/" .env
docker compose down --remove-orphans --timeout 30 || true
for n in foodgram-db foodgram-backend foodgram-front foodgram-proxy; do docker rm -f "$n" 2>/dev/null || true; done
docker ps -a --format '{{.Names}}' | grep -E 'foodgram' | xargs -r docker rm -f || true
docker compose up -d --build --force-recreate --remove-orphans
sleep 20
docker run --rm -v "$HOME/foodgram/frontend/build:/out" alpine sh -c 'rm -rf /out/* /out/.[!.]* 2>/dev/null || true'
docker run --rm -v "$HOME/foodgram/frontend/build:/out" infra-frontend sh -c 'cp -r /app/build/. /out/' 2>/dev/null || \
docker run --rm -v "$HOME/foodgram/frontend/build:/out" infra_frontend sh -c 'cp -r /app/build/. /out/'
docker compose restart nginx
docker compose ps
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1/ || true
'@

ssh -i $KeyPath "${SshUser}@${HostIP}" $deployScript
Write-Host "Done. Open http://$HostIP/" -ForegroundColor Green
