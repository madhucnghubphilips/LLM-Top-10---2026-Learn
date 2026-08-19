<!-- The OWASP Top 10 for LLM Applications (2025) training was designed and developed by CN Madhu (madhu.cn@philips.com). This program combines industry-relevant content and practical labs to showcase real-world AI security risks, vulnerabilities, and defense strategies in healthcare environments. -->
# LLM08 - Vector and Embedding Weaknesses

Hands-on Streamlit lab for OWASP LLM08: Vector and Embedding Weaknesses using a local RAG workflow.

## What This Lab Covers

- Poisoned retrieval context and embedding-pipeline risk
- How untrusted chunks can steer model outputs
- Retrieval guardrails and source filtering controls
- Vulnerable behavior vs secure behavior

## Prerequisites (LLM08 Only)

- Install Ollama: https://ollama.com
- Pull required models:

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

- Start Ollama if needed:

```bash
ollama serve
```

## Run The Lab

Windows:

```bat
launch_llm08_vector_lab.bat
```

macOS/Linux:

```bash
bash launch_llm08_vector_lab.sh
```

Run these commands from this folder. From the repository root, use `LLM08 - Vector and Embedding Weaknesses\launch_llm08_vector_lab.bat` on Windows or `bash "LLM08 - Vector and Embedding Weaknesses/launch_llm08_vector_lab.sh"` on macOS/Linux. The launcher prepares this lab's local AI resources and starts the app at `http://localhost:20555`.

Manual (any OS):

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 20555
```

Local URL: `http://localhost:20555`

## Safety Note

This lab is intentionally educational and defensive. It is designed to demonstrate retrieval risk and mitigations in a controlled local environment.
