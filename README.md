<!--
The OWASP Top 10 for LLM Applications (2025) training was designed and developed by
CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and
practical labs to showcase real-world AI security risks, vulnerabilities, and defense
strategies in healthcare environments.
-->

# OWASP Top 10 for LLM Applications (2025) - Healthcare Security Labs

A hands-on, self-contained training environment that teaches the **OWASP Top 10 for
Large Language Model (LLM) Applications (2025)** through interactive, healthcare-themed
labs. Each risk category is paired with a runnable demo that contrasts **vulnerable**
behavior against **secure** behavior, plus guided challenges and workshop flows.

Everything runs **locally** on your machine. No cloud accounts, no production services,
and only **synthetic** data are used.

---

## Table of Contents

- [Overview](#overview)
- [OWASP LLM Top 10 (2025) Coverage](#owasp-llm-top-10-2025-coverage)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Lab Groups and Launchers](#lab-groups-and-launchers)
- [Port Reference](#port-reference)
- [The Combined RAG Demo (Lab 1)](#the-combined-rag-demo-lab-1)
- [How the Labs Work](#how-the-labs-work)
- [Stopping the Labs](#stopping-the-labs)
- [Running a Single Lab Manually](#running-a-single-lab-manually)
- [Troubleshooting](#troubleshooting)
- [Safety and Responsible Use](#safety-and-responsible-use)
- [Credits](#credits)

---

## Overview

This repository packages two complementary learning experiences:

1. **Learning labs** — A set of focused **Streamlit** apps (one per OWASP LLM risk).
   Each app explains the risk, demonstrates an insecure implementation, shows the secure
   alternative, and includes an interactive challenge mode for workshops.

2. **Combined RAG demo** — A **FastAPI + FAISS + Ollama** capture-the-flag (CTF) style
   environment that chains several risks together inside a realistic Retrieval-Augmented
   Generation (RAG) assistant for a healthcare scenario.

The labs are designed for security awareness training, engineering education, and
workshop delivery. They emphasize **defensive** understanding: how these weaknesses
arise and how to mitigate them.

---

## OWASP LLM Top 10 (2025) Coverage

| Risk | Topic | What the lab demonstrates |
| --- | --- | --- |
| **LLM01** | Prompt Injection | Direct/indirect injection, instruction-hierarchy abuse (system vs user intent) |
| **LLM02** | Sensitive Information Disclosure | PHI/PII leakage through unsafe prompting and context handling |
| **LLM03** | Supply Chain Vulnerabilities | Untrusted packages/models/datasets/plugins, provenance and drift controls |
| **LLM04** | Data and Model Poisoning | Poisoned training/fine-tuning/retrieval data and backdoor scenarios |
| **LLM05** | Improper Output Handling | Treating model output as untrusted; unsafe rendering/execution risks |
| **LLM06** | Excessive Agency | Over-privileged/over-autonomous actions, missing human-in-the-loop controls |
| **LLM07** | System Prompt Leakage | Prompt extraction and why secrets must not live in system prompts |
| **LLM08** | Vector and Embedding Weaknesses | Poisoned retrieval context and embedding-pipeline risk in RAG |
| **LLM09** | Misinformation | Hallucinations, unsupported claims, and confidence vs reliability |
| **LLM10** | Unbounded Consumption | Cost/performance abuse, resource exhaustion, and availability impact |

---

## Repository Structure

```
OWASP-LLM-Security-Labs/
├── stop_all_ports.bat / .ps1 / .sh        # Stop every lab port in one command
│
├── 1_Labs01,02,04,05,07,09,10/            # Combined RAG CTF demo (FastAPI + FAISS + Ollama)
│   ├── launch_combined_rag_demo.bat / .sh
│   ├── Modelfile-ctf                       # Ollama model definition (dolphin-mistral based)
│   ├── README.txt
│   └── app/                                # rag_server.py, rag.py, labs, knowledge_base, tests
│
├── 2_Learn_01,02,04,05/                    # Streamlit learning labs
│   ├── launch_llm01_02_04_05_labs.bat / .sh
│   ├── LLM01 - Prompt Injection with lab/
│   ├── LLM02 - Sensitive Information Disclosure with lab/
│   ├── LLM04 - Data and Model Poisoning/
│   └── LLM05 - Improper Output Handling with lab/
│
├── 3_Learn_03/                             # Streamlit learning lab
│   ├── launch_llm03_lab.bat / .sh
│   └── LLM03 - Supply Chain Vulnerabilities/
│
├── 4_Learn_Labs_06,08/                     # Streamlit learning labs
│   ├── launch_llm06_08_labs.bat / .sh
│   ├── LLM06 - Excessive Agency/
│   └── LLM08 - Vector & Embedding Weakness/   # Uses Ollama (local RAG)
│
└── 5_Learn_07,09,10/                       # Streamlit learning labs
    ├── launch_llm07_09_10_labs.bat / .sh
    ├── LLM07 - System Prompt Leakage/
    ├── LLM09 - Misinformation  with lab/
    └── LLM10 - Unbounded Consumption/
```

Each lab folder contains its own `app.py`, `requirements.txt`, `README.md`, and an
`assets/` directory. A single shared virtual environment is created at the repository
root (`.venv/`) and reused by every launcher.

---

## Prerequisites

- **Python 3.10 or newer** — required by all labs.
  Download from <https://www.python.org/downloads/> if not installed.
- **Ollama** — required only for the **Combined RAG demo (Lab 1)** and **LLM08**.
  Download from <https://ollama.com>.
- **A modern web browser** — the labs open automatically at `http://localhost:<port>`.

The launchers try to help you along the way:

- If Python 3.10+ is missing, the launchers can attempt to install it using your system
  package manager (Windows `winget`; Linux `apt`/`dnf`/`yum`/`pacman`/`zypper`; macOS `brew`).
- If Ollama is missing, the Combined RAG launcher can attempt to install it
  (Windows via `winget`; macOS/Linux via the official installer script).
- A corporate-proxy SSL fallback is built into dependency installation.

> All Python dependencies are installed into the repo-level `.venv/` only. Your global
> Python installation is left untouched.

---

## Quick Start

### Windows

From File Explorer, open a lab group folder and **double-click** its launcher, or run it
from a terminal at the repository root:

```bat
REM Combined RAG CTF demo (requires Ollama)
"1_Labs01,02,04,05,07,09,10\launch_combined_rag_demo.bat"

REM Learning labs: LLM01, LLM02, LLM04, LLM05
"2_Learn_01,02,04,05\launch_llm01_02_04_05_labs.bat"

REM Learning lab: LLM03
"3_Learn_03\launch_llm03_lab.bat"

REM Learning labs: LLM06, LLM08 (LLM08 uses Ollama)
"4_Learn_Labs_06,08\launch_llm06_08_labs.bat"

REM Learning labs: LLM07, LLM09, LLM10
"5_Learn_07,09,10\launch_llm07_09_10_labs.bat"
```

### macOS / Linux

Run the matching shell launcher from the repository root:

```bash
# Combined RAG CTF demo (requires Ollama)
bash "1_Labs01,02,04,05,07,09,10/launch_combined_rag_demo.sh"

# Learning labs: LLM01, LLM02, LLM04, LLM05
bash "2_Learn_01,02,04,05/launch_llm01_02_04_05_labs.sh"

# Learning lab: LLM03
bash "3_Learn_03/launch_llm03_lab.sh"

# Learning labs: LLM06, LLM08 (LLM08 uses Ollama)
bash "4_Learn_Labs_06,08/launch_llm06_08_labs.sh"

# Learning labs: LLM07, LLM09, LLM10
bash "5_Learn_07,09,10/launch_llm07_09_10_labs.sh"
```

Each launcher:

1. Detects a suitable Python interpreter.
2. Creates/reuses the shared `.venv/` at the repository root.
3. Installs the group's dependencies once.
4. Frees the target ports if they are already in use.
5. Starts the app(s) and opens the URL(s) in your browser.

**Keep the launcher window open** while using the labs. Press `Ctrl+C` (or close the
window) to stop them.

---

## Lab Groups and Launchers

| Group folder | Launcher | Labs started |
| --- | --- | --- |
| `1_Labs01,02,04,05,07,09,10/` | `launch_combined_rag_demo` | Combined RAG CTF demo |
| `2_Learn_01,02,04,05/` | `launch_llm01_02_04_05_labs` | LLM01, LLM02, LLM04, LLM05 |
| `3_Learn_03/` | `launch_llm03_lab` | LLM03 |
| `4_Learn_Labs_06,08/` | `launch_llm06_08_labs` | LLM06, LLM08 |
| `5_Learn_07,09,10/` | `launch_llm07_09_10_labs` | LLM07, LLM09, LLM10 |

Multi-lab launchers start every app in the group at once, each on its own port, and open
all of the URLs.

---

## Port Reference

| Lab | Topic | URL |
| --- | --- | --- |
| Combined RAG Demo | LLM01/02/04/05/07/09 (CTF) | <http://localhost:20001/labs> |
| LLM01 | Prompt Injection | <http://localhost:21010> |
| LLM02 | Sensitive Information Disclosure | <http://localhost:21025> |
| LLM03 | Supply Chain Vulnerabilities | <http://localhost:21080> |
| LLM04 | Data and Model Poisoning | <http://localhost:21123> |
| LLM05 | Improper Output Handling | <http://localhost:20222> |
| LLM06 | Excessive Agency | <http://localhost:20333> |
| LLM07 | System Prompt Leakage | <http://localhost:20444> |
| LLM08 | Vector & Embedding Weakness | <http://localhost:20555> |
| LLM09 | Misinformation | <http://localhost:20666> |
| LLM10 | Unbounded Consumption | <http://localhost:21777> |

---

## The Combined RAG Demo (Lab 1)

`1_Labs01,02,04,05,07,09,10/` is a CTF-style, single-server environment that stitches
several OWASP LLM risks into one realistic healthcare RAG assistant. It is the most
feature-rich lab and the only one served by FastAPI instead of Streamlit.

- **Server:** FastAPI served by Uvicorn (`app.rag_server:app`) at
  <http://localhost:20001/labs>.
- **Retrieval:** A local **FAISS** vector index over a synthetic healthcare knowledge base.
- **Local models via Ollama:**
  - `dolphin-ctf` — a chat model the launcher builds from `Modelfile-ctf`
    (based on `dolphin-mistral:latest`).
  - `nomic-embed-text` — the embedding model used for retrieval.
- **Included scenarios:** prompt injection, sensitive-information disclosure, MRI
  maintenance data poisoning, improper output handling, system-prompt leakage, and a
  misinformation/file lab.
- **Challenge validation:** An intent-based evaluator scores detected attack objectives
  and accepts equivalent wording rather than one exact expected prompt. It returns
  feedback on missing components without revealing a full solution.

The Windows and shell launchers handle the full setup for this lab: verifying Python and
Ollama, building/pulling the required models, preparing the search index, and starting
the server.

> **Progress:** Lab progress is stored in your browser's local storage. To reset it,
> open Developer Tools → Application → Local Storage and delete the `ctf_progress` key.

---

## How the Labs Work

Each Streamlit learning lab follows a consistent teaching pattern:

- **Overview** — a visual introduction to the OWASP risk.
- **Vulnerable vs Secure** — side-by-side behavior so the mitigation is concrete.
- **Interactive challenge mode** — try inputs and observe how a hardened system responds.

A few labs have extra depth:

- **LLM03 (Supply Chain)** ships a 15-step guided workshop that ends with a
  *Live Supply Chain Simulation*.
- **LLM08 (Vector & Embedding)** runs a local RAG workflow and demonstrates how poisoned
  chunks steer model output, plus retrieval guardrails and source filtering.

---

## Stopping the Labs

Closing a launcher window stops the apps it started. To forcefully release **every** lab
port at once (useful if something was left running), use the repo-root helper:

**Windows (PowerShell):**

```powershell
.\stop_all_ports.ps1
```

**Windows (Command Prompt):**

```bat
stop_all_ports.bat
```

**macOS / Linux:**

```bash
bash stop_all_ports.sh
```

This scans ports `20001`, `21010`, `21025`, `21080`, `21123`, `20222`, `20333`, `20444`,
`20555`, `20666`, and `21777`, and stops any process listening on them.

---

## Running a Single Lab Manually

If you prefer to run one Streamlit lab without a launcher, activate the shared
environment and start the app on its assigned port. For example, LLM01:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
cd "2_Learn_01,02,04,05\LLM01 - Prompt Injection with lab"
pip install -r requirements.txt
streamlit run app.py --server.port 21010
```

**macOS / Linux:**

```bash
source .venv/bin/activate
cd "2_Learn_01,02,04,05/LLM01 - Prompt Injection with lab"
pip install -r requirements.txt
streamlit run app.py --server.port 21010
```

Use the matching port from the [Port Reference](#port-reference) for other labs.

> **LLM08 and the Combined RAG demo** additionally require Ollama. For LLM08, pull the
> models first:
>
> ```bash
> ollama pull llama3.1
> ollama pull nomic-embed-text
> ollama serve   # if the service is not already running
> ```

---

## Troubleshooting

- **"Python 3.10 or newer was not found."** Install Python from
  <https://www.python.org/downloads/> and re-run the launcher. On Windows, ensure
  "Add Python to PATH" is selected during installation.
- **Dependency install fails behind a corporate proxy.** The launchers automatically
  retry with `--trusted-host pypi.org --trusted-host files.pythonhosted.org`. If it still
  fails, ask IT to allow access to `pypi.org` and `files.pythonhosted.org`.
- **Ollama not found (Lab 1 / LLM08).** Install from <https://ollama.com>, confirm
  `ollama --version` works, and make sure the service is running (`ollama serve`).
- **A port is already in use.** Launchers free their ports automatically. To clear
  everything manually, run the [stop-all-ports](#stopping-the-labs) helper.
- **A lab won't open in the browser.** Open the URL from the
  [Port Reference](#port-reference) manually.
- **Reset Combined RAG demo progress.** Delete the `ctf_progress` key in the browser's
  local storage (Developer Tools → Application → Local Storage).

---

## Safety and Responsible Use

- These labs are for **training and awareness in controlled settings only**.
- All records, identifiers, prompts, secrets, and outputs are **synthetic** demo content.
- The labs are **intentionally educational and defensive**. They do not perform real
  attacks, execute malicious supply-chain behavior, or call production services.
- Do not point these tools at real systems, real patient data, or any environment you are
  not authorized to test.

---

## Credits

The OWASP Top 10 for LLM Applications (2025) training was designed and developed by
**CN Madhu** (madhu.cn@philips.com). This program combines industry-relevant content and
practical labs to showcase real-world AI security risks, vulnerabilities, and defense
strategies in healthcare environments.

Reference: [OWASP Top 10 for LLM Applications](https://genai.owasp.org/).
