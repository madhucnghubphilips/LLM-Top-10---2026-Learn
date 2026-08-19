<!-- Vendor-neutral OWASP Top 10 for LLM Applications (2025) defensive training lab. -->
# LLM04 - ADAS Supply Chain Vulnerabilities

Hands-on Streamlit lab for OWASP LLM04: Supply Chain Vulnerabilities in an ADAS software-update workflow.

## What This Lab Covers

- Risks from untrusted packages, models, datasets, and plugins
- Dependency and provenance validation practices
- Secure release gates and drift detection
- Vulnerable behavior vs secure behavior
- A 15 guided step workshop flow, ending with `15. Live Supply Chain Simulation`

## Run The Lab

Windows:

```bat
LLM03,04,06,07,10\launch_llm03_04_06_07_10_labs.bat
```

macOS/Linux:

```bash
bash "LLM03,04,06,07,10/launch_llm03_04_06_07_10_labs.sh"
```

Run the grouped launcher commands from the repository root.

Manual (any OS):

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 21080
```

Local URL: `http://localhost:21080`

## Safety Note

This demo is intentionally educational and defensive. It does not execute real malicious supply chain behavior.
