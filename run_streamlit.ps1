$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$streamlit = Get-Command streamlit -ErrorAction Stop
Write-Host "Starting 数据结构智能复习助手..."
Write-Host "Project: $root"
Write-Host "URL: http://localhost:8505"

& $streamlit.Path run app/streamlit_app.py --server.port 8505 --server.headless false

