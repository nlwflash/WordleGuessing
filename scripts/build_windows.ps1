param(
    [string]$Version = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$releaseRoot = Join-Path $repoRoot "release"
$distRoot = Join-Path $releaseRoot "dist"
$buildRoot = Join-Path $releaseRoot "build"
$specRoot = Join-Path $releaseRoot "spec"
$packageRoot = Join-Path $repoRoot "packaging\\windows"
$versionTemplatePath = Join-Path $packageRoot "version_info.txt"
$resolvedVersionPath = Join-Path $releaseRoot "version_info.txt"
$iconPath = Join-Path $repoRoot "source_code\\resource\\wordleguessing.ico"
$entryPath = Join-Path $repoRoot "source_code\\__main__.py"
$zipPath = Join-Path $releaseRoot "WordleGuessing-windows.zip"

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = python -c "import pathlib, tomllib; data = tomllib.loads(pathlib.Path('pyproject.toml').read_text(encoding='utf-8')); print(data['project']['version'])"
}

$versionParts = @($Version.Split(".") | Where-Object { $_ -ne "" })
while ($versionParts.Count -lt 4) {
    $versionParts += "0"
}
$versionCommas = ($versionParts[0..3] -join ",")
$versionDots = ($versionParts[0..3] -join ".")

New-Item -ItemType Directory -Path $releaseRoot -Force | Out-Null
Remove-Item -LiteralPath $distRoot, $buildRoot, $specRoot, $resolvedVersionPath, $zipPath -Recurse -Force -ErrorAction SilentlyContinue

$template = Get-Content -Raw $versionTemplatePath
$template = $template.Replace("{{VERSION_COMMAS}}", $versionCommas)
$template = $template.Replace("{{VERSION_DOTS}}", $versionDots)
Set-Content -Path $resolvedVersionPath -Value $template -Encoding UTF8

python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onedir `
    --name WordleGuessing `
    --icon $iconPath `
    --version-file $resolvedVersionPath `
    --distpath $distRoot `
    --workpath $buildRoot `
    --specpath $specRoot `
    --collect-data source_code.resource `
    $entryPath

Compress-Archive -Path (Join-Path $distRoot "WordleGuessing") -DestinationPath $zipPath -Force
Write-Host "Created $zipPath"
