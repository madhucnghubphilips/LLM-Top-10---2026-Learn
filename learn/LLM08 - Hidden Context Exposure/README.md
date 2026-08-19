<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM07 - System Prompt Leakage

Hands-on Streamlit lab for OWASP LLM07: System Prompt Leakage with healthcare-oriented scenarios.

## What This Lab Covers

- Prompt extraction and hidden-instruction disclosure attempts
- Why system prompts should not contain secrets
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
streamlit run app.py --server.port 20444
```

Local URL: `http://localhost:20444`

## Safety Note

All records, identifiers, prompts, and outputs are synthetic demo content for security education only.

