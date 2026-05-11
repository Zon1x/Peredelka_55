# Запуск dev-сервера из корня проекта с «свежей» версией статики в URL.
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path '.\venv\Scripts\Activate.ps1')) {
    Write-Error 'Не найден venv. Создайте: py -m venv venv && .\venv\Scripts\pip install -r requirements.txt'
}

$env:ASSET_VERSION = Get-Date -Format 'yyyyMMddHHmm'
Write-Host "ASSET_VERSION=$($env:ASSET_VERSION) (сброс кэша CSS/JS)" -ForegroundColor Cyan

. .\venv\Scripts\Activate.ps1
python manage.py bootstrap_tz_content --demo-reviews
python manage.py runserver 0.0.0.0:8000
