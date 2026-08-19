<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM06 - Excessive Agency

Hands-on Streamlit lab for OWASP LLM06: Excessive Agency with healthcare-oriented scenarios.

## What This Lab Covers

- Risks from over-privileged or over-autonomous AI actions
- Missing approval and human-in-the-loop controls
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
streamlit run app.py --server.port 20333
```

Local URL: `http://localhost:20333`

## Safety Note

All records, identifiers, prompts, and outputs are synthetic demo content for security education only.

