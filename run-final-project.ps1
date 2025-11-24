<#
.SYNOPSIS
  Wrapper to run the `final_project` package from the repository root.

.DESCRIPTION
  This script sets `PYTHONPATH` to the repo `src/` folder so the
  `final_project` package (located under `src/final_project`) is importable
  and then forwards any arguments to `python -m final_project`.

.EXAMPLE
  .\run-final-project.ps1 task add "Write report" --description "..."
#>

[CmdletBinding(DefaultParameterSetName='Run')]
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]] $RemainingArgs
)

# Determine the repository root as the directory containing this script
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

if (-not (Test-Path (Join-Path $repoRoot 'src'))) {
    Write-Error "Expected 'src' directory under repo root ($repoRoot). Run this script from the repository root or move it there."
    exit 1
}

$env:PYTHONPATH = (Join-Path $repoRoot 'src')
Write-Host "PYTHONPATH set to: $env:PYTHONPATH" -ForegroundColor Cyan

Write-Host "Running: python -m final_project $($RemainingArgs -join ' ')" -ForegroundColor Green

try {
    & python -m final_project @RemainingArgs
    exit $LASTEXITCODE
} catch {
    Write-Error "Failed to run final_project: $_"
    exit 1
}
