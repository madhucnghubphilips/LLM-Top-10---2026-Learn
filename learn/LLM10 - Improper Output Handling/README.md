<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM05 - Improper Output Handling

Hands-on Streamlit lab for OWASP LLM05: Improper Output Handling with healthcare-oriented scenarios.

## What This Lab Covers

- Why LLM output must be treated as untrusted data
- Risks from unsafe rendering/execution of generated content
- Vulnerable behavior vs secure behavior
- Interactive challenge mode for workshops

## Run The Lab

Windows:

```bat
LLM01,02,05,09\launch_llm01_02_05_09_labs.bat
```

macOS/Linux:

```bash
bash "LLM01,02,05,09/launch_llm01_02_05_09_labs.sh"
```

Run the grouped launcher commands from the repository root.

Manual (any OS):

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 20222
```

Local URL: `http://localhost:20222`

## Safety Note

All records, identifiers, prompts, and outputs are synthetic demo content for security education only.

