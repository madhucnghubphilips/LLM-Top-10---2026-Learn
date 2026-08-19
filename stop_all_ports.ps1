# stop_all_ports.ps1
# Stops any processes listening on the ports used by the OWASP LLM Security Labs.

$ports = @(
    @{ Port = 20001; Lab = "Combined RAG Demo (Lab 1)" },
    @{ Port = 21010; Lab = "LLM01 - Prompt Injection" },
    @{ Port = 21025; Lab = "LLM02 - Sensitive Information Disclosure" },
    @{ Port = 21123; Lab = "LLM04 - Data and Model Poisoning" },
    @{ Port = 20222; Lab = "LLM05 - Improper Output Handling" },
    @{ Port = 21080; Lab = "LLM03 - Supply Chain Vulnerabilities" },
    @{ Port = 20333; Lab = "LLM06 - Excessive Agency" },
    @{ Port = 20555; Lab = "LLM08 - Vector & Embedding Weakness" },
    @{ Port = 20444; Lab = "LLM07 - System Prompt Leakage" },
    @{ Port = 20666; Lab = "LLM09 - Misinformation" },
    @{ Port = 21777; Lab = "LLM10 - Unbounded Consumption" }
)

Write-Host ""
Write-Host "=== OWASP LLM Security Labs - Stop All Ports ===" -ForegroundColor Cyan
Write-Host ""

$anyKilled = $false

foreach ($entry in $ports) {
    $port = $entry.Port
    $lab  = $entry.Lab

    # Find PIDs listening on this TCP port
    $connections = netstat -ano | Select-String "LISTENING" | Select-String ":$port "
    $pids = $connections |
        ForEach-Object { ($_ -split '\s+')[-1] } |
        Where-Object { $_ -match '^\d+$' } |
        Select-Object -Unique

    if ($pids) {
        foreach ($procPid in $pids) {
            try {
                $proc = Get-Process -Id $procPid -ErrorAction SilentlyContinue
                $procName = if ($proc) { $proc.Name } else { "unknown" }
                Stop-Process -Id $procPid -Force -ErrorAction Stop
                Write-Host "  [STOPPED] Port $port  |  PID $procPid ($procName)  |  $lab" -ForegroundColor Green
                $anyKilled = $true
            } catch {
                Write-Host "  [FAILED]  Port $port  |  PID $procPid  |  $lab  |  $_" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  [FREE]    Port $port  |  $lab" -ForegroundColor DarkGray
    }
}

Write-Host ""
if ($anyKilled) {
    Write-Host "Done. All active lab ports have been released." -ForegroundColor Cyan
} else {
    Write-Host "Done. No lab ports were in use." -ForegroundColor Cyan
}
Write-Host ""
