<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM04 - Data and Model Poisoning

Hands-on Streamlit lab for OWASP LLM04: Data and Model Poisoning with healthcare-oriented scenarios.

## What This Lab Covers

- Poisoned training, fine-tuning, and retrieval data effects
- Backdoor and manipulation scenarios in healthcare context
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
streamlit run app.py --server.port 21123
```

Local URL: `http://localhost:21123`

## Safety Note

All records, identifiers, prompts, and outputs are synthetic demo content for security education only.
