param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
$activateScript = Join-Path $repoRoot ".venv\Scripts\Activate.ps1"
$targetScript = Join-Path $scriptDir "decode.py"

if (-not (Test-Path $activateScript)) {
    throw "Nu am găsit mediul virtual: $activateScript"
}

if (-not (Test-Path $targetScript)) {
    throw "Nu am găsit fișierul: $targetScript"
}

Set-Location $repoRoot
. $activateScript
& python $targetScript @Args
exit $LASTEXITCODE
