#!/usr/bin/env bash
# stop_all_ports.sh
# Stops any processes listening on ports used by the OWASP LLM Security Labs.

declare -A LABS=(
    [20001]="Combined RAG Demo (Lab 1)"
    [21010]="LLM01 - Prompt Injection"
    [21025]="LLM02 - Sensitive Information Disclosure"
    [21123]="LLM04 - Data and Model Poisoning"
    [20222]="LLM05 - Improper Output Handling"
    [21080]="LLM03 - Supply Chain Vulnerabilities"
    [20333]="LLM06 - Excessive Agency"
    [20555]="LLM08 - Vector & Embedding Weakness"
    [20444]="LLM07 - System Prompt Leakage"
    [20666]="LLM09 - Misinformation"
    [21777]="LLM10 - Unbounded Consumption"
)

# Ordered list so output is deterministic
PORTS=(20001 21010 21025 21123 20222 21080 20333 20555 20444 20666 21777)

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
GRAY='\033[0;90m'
RESET='\033[0m'

echo ""
echo -e "${CYAN}=== OWASP LLM Security Labs - Stop All Ports ===${RESET}"
echo ""

any_killed=false

free_port() {
    local port="$1"
    local pids=""

    # Try lsof first (macOS + most Linux)
    if command -v lsof &>/dev/null; then
        pids=$(lsof -ti :"$port" 2>/dev/null) || true
    fi

    # Fallback: ss (Linux)
    if [ -z "$pids" ] && command -v ss &>/dev/null; then
        pids=$(ss -lptn "sport = :$port" 2>/dev/null \
            | grep -o 'pid=[0-9]*' | cut -d= -f2) || true
    fi

    # Fallback: fuser (Linux)
    if [ -z "$pids" ] && command -v fuser &>/dev/null; then
        pids=$(fuser "${port}/tcp" 2>/dev/null \
            | tr -s ' ' | tr ' ' '\n' | grep -E '^[0-9]+$') || true
    fi

    echo "$pids"
}

for port in "${PORTS[@]}"; do
    lab="${LABS[$port]}"
    pids=$(free_port "$port")

    if [ -n "$pids" ]; then
        for target_pid in $pids; do
            proc_name=$(ps -p "$target_pid" -o comm= 2>/dev/null || echo "unknown")
            if kill -9 "$target_pid" 2>/dev/null; then
                echo -e "  ${GREEN}[STOPPED]${RESET} Port $port  |  PID $target_pid ($proc_name)  |  $lab"
                any_killed=true
            else
                echo -e "  ${RED}[FAILED] ${RESET} Port $port  |  PID $target_pid  |  $lab"
            fi
        done
    else
        echo -e "  ${GRAY}[FREE]    Port $port  |  $lab${RESET}"
    fi
done

echo ""
if [ "$any_killed" = true ]; then
    echo -e "${CYAN}Done. All active lab ports have been released.${RESET}"
else
    echo -e "${CYAN}Done. No lab ports were in use.${RESET}"
fi
echo ""
