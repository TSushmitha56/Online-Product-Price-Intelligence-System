# ============================================================
# PriceIntel - Package for Transfer Script
# Run: powershell -ExecutionPolicy Bypass -File package_for_transfer.ps1
# Creates: PriceIntel_transfer.zip (excludes venv/node_modules)
# ============================================================

$projectRoot = $PSScriptRoot
$outputZip   = Join-Path $projectRoot "PriceIntel_transfer.zip"

$excludeNames = @("venv",".venv","dt_venv","node_modules","__pycache__",".pytest_cache",".git",".github")

Write-Host "Packaging PriceIntel for transfer..."
Write-Host "Source: $projectRoot"
Write-Host "Output: $outputZip"

if (Test-Path $outputZip) {
    Remove-Item $outputZip -Force
    Write-Host "Removed old zip."
}

# Collect all files, skipping excluded folder names
$allFiles = Get-ChildItem -Path $projectRoot -Recurse -File | Where-Object {
    $parts = $_.FullName.Substring($projectRoot.Length + 1).Split([IO.Path]::DirectorySeparatorChar)
    $skip  = $false
    foreach ($part in $parts) {
        if ($excludeNames -contains $part) { $skip = $true; break }
    }
    # Also skip *.pyc files and the zip itself
    if ($_.Extension -eq ".pyc") { $skip = $true }
    if ($_.Name -eq "PriceIntel_transfer.zip") { $skip = $true }
    -not $skip
}

Write-Host "Files to include: $($allFiles.Count)"

# Build a temp folder structure then compress
$tempDir = Join-Path $env:TEMP "PriceIntel_pkg"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
New-Item -ItemType Directory -Path $tempDir | Out-Null

foreach ($file in $allFiles) {
    $relative   = $file.FullName.Substring($projectRoot.Length + 1)
    $destPath   = Join-Path $tempDir $relative
    $destFolder = Split-Path $destPath -Parent
    if (-not (Test-Path $destFolder)) { New-Item -ItemType Directory -Path $destFolder -Force | Out-Null }
    Copy-Item $file.FullName -Destination $destPath
}

Compress-Archive -Path "$tempDir\*" -DestinationPath $outputZip -Force
Remove-Item $tempDir -Recurse -Force

$sizeMB = [math]::Round((Get-Item $outputZip).Length / 1MB, 1)
Write-Host "Done! Created PriceIntel_transfer.zip ($sizeMB MB)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Copy PriceIntel_transfer.zip to a USB drive or send it."
Write-Host "  2. On the new laptop, right-click the zip > Extract All."
Write-Host "  3. Follow TRANSFER_SETUP_GUIDE.md inside the extracted folder."
