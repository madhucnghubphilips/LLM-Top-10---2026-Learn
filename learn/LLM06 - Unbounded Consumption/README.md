<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM10 - Unbounded Consumption

Hands-on Streamlit lab for OWASP LLM10: Unbounded Consumption.

## What This Lab Covers

- Cost and performance abuse patterns in LLM apps
- Resource exhaustion and availability impact
- Vulnerable behavior vs secure behavior
- Interactive challenge mode for workshops

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
streamlit run app.py --server.port 21777
```

Local URL: `http://localhost:21777`

## Safety Note

This demo is intentionally educational and defensive. It does not perform real attacks or call production services.
