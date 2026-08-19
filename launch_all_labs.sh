#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
VENV_DIR="$REPO_ROOT/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
PID_FILE="${TMPDIR:-/tmp}/owasp_llm_all_pids_$$.txt"
LOG_DIR="${TMPDIR:-/tmp}/owasp_llm_all_logs_$$"

LABS=(
  "LLM01|Prompt Injection|learn/LLM01 - Prompt Injection|21010"
  "LLM02|Sensitive Data Disclosure|learn/LLM02 - Sensitive Data Disclosure|21025"
  "LLM03|Excessive Agency|learn/LLM03 - Excessive Agency|20333"
  "LLM04|Supply Chain Vulnerabilities|learn/LLM04 - Supply Chain Vulnerabilities|21080"
  "LLM05|Data and Model Poisoning|learn/LLM05 - Data and Model Poisoning|21123"
  "LLM06|Unbounded Consumption|learn/LLM06 - Unbounded Consumption|21777"
  "LLM07|Misinformation|learn/LLM07 - Misinformation|20666"
  "LLM08|Hidden Context Exposure|learn/LLM08 - Hidden Context Exposure|20444"
  "LLM09|Vector and Embedding Weaknesses|learn/LLM09 - Vector and Embedding Weaknesses|20555"
  "LLM10|Improper Output Handling|learn/LLM10 - Improper Output Handling|20222"
)

cleanup() {
  if [[ -f "$PID_FILE" ]]; then
    echo
    echo "[*] Stopping lab servers..."
    while IFS= read -r target_pid; do
      if [[ "$target_pid" =~ ^[0-9]+$ ]]; then
        kill "$target_pid" 2>/dev/null || true
      fi
    done < "$PID_FILE"
    rm -f "$PID_FILE"
  fi
}
trap cleanup EXIT INT TERM

select_python() {
  if command -v python3 >/dev/null 2>&1; then
    echo python3
  elif command -v python >/dev/null 2>&1; then
    echo python
  else
    return 1
  fi
}

free_port() {
  local port="$1"
  local pids=""
  if command -v lsof >/dev/null 2>&1; then
    pids="$(lsof -ti tcp:"$port" 2>/dev/null || true)"
  elif command -v fuser >/dev/null 2>&1; then
    pids="$(fuser "$port"/tcp 2>/dev/null || true)"
  fi
  if [[ -n "$pids" ]]; then
    kill $pids 2>/dev/null || true
    sleep 1
  fi
}

open_url() {
  local url="$1"
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$url" >/dev/null 2>&1 || true
  elif command -v open >/dev/null 2>&1; then
    open "$url" >/dev/null 2>&1 || true
  fi
}

echo "OWASP LLM Security Labs - Start All Streamlit Apps"
echo "=================================================="
echo

PYTHON_BIN="$(select_python)" || {
  echo "Python was not found. Install Python 3.10 or newer and run this launcher again."
  exit 1
}

echo "Selected Python:"
"$PYTHON_BIN" --version

echo
echo "[*] Preparing shared Python environment..."
if [[ ! -x "$VENV_PYTHON" ]]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi
"$VENV_PYTHON" -m ensurepip --upgrade >/dev/null 2>&1 || true
"$VENV_PYTHON" -m pip install --upgrade pip --quiet --disable-pip-version-check

for lab in "${LABS[@]}"; do
  IFS='|' read -r lab_id lab_title lab_path port <<< "$lab"
  req_file="$REPO_ROOT/$lab_path/requirements.txt"
  if [[ -f "$req_file" ]]; then
    echo "[*] Installing requirements for $lab_id - $lab_title"
    "$VENV_PYTHON" -m pip install -r "$req_file" --quiet --disable-pip-version-check
  fi
done

mkdir -p "$LOG_DIR"

for lab in "${LABS[@]}"; do
  IFS='|' read -r lab_id lab_title lab_path port <<< "$lab"
  app_dir="$REPO_ROOT/$lab_path"
  if [[ ! -f "$app_dir/app.py" ]]; then
    echo "Missing app.py for $lab_id at $app_dir"
    exit 1
  fi
  free_port "$port"
  echo "[*] Starting $lab_id - $lab_title on port $port"
  (
    cd "$app_dir"
    "$VENV_PYTHON" -m streamlit run app.py --server.port "$port" --server.headless true
  ) >"$LOG_DIR/$lab_id.log" 2>"$LOG_DIR/$lab_id.err.log" &
  echo "$!" >> "$PID_FILE"
done

echo
echo "Started all maintained OWASP LLM Streamlit apps:"
for lab in "${LABS[@]}"; do
  IFS='|' read -r lab_id lab_title lab_path port <<< "$lab"
  echo "  $lab_id: http://localhost:$port"
done
echo
echo "Logs: $LOG_DIR"
echo

sleep 5
for lab in "${LABS[@]}"; do
  IFS='|' read -r lab_id lab_title lab_path port <<< "$lab"
  open_url "http://localhost:$port"
done

echo "Keep this launcher running. Press Enter here to stop all labs."
read -r _
