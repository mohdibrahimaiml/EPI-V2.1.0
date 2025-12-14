# EPI - Evidence Packaged Infrastructure
> **The "PDF" for AI Evidence**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-MVP-orange.svg)](https://pypi.org/project/epi-recorder/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohdibrahimaiml/EPI-V2.0.0/blob/main/colab_demo.ipynb)

---

## 💡 The Concept

**EPI files are self-contained evidence packages.**

Just as a **PDF** captures a document's layout, fonts, and images so it looks the same everywhere, an **EPI** file captures an AI workflow's code, inputs, model calls, and environment so it **runs the same everywhere**.

| Feature | 📄 PDF (Document Standard) | 📦 EPI (Execution Standard) |
| :--- | :--- | :--- |
| **Purpose** | Visual fidelity | Computational fidelity |
| **Captures** | Text, Layout, Images | Code, API Calls, Environment |
| **Verification** | None (Visual only) | **Cryptographic (Ed25519)** |
| **Safety** | Reader executes JS (Unsafe) | **Static HTML Viewer (Safe)** |
| **Analogy** | A photograph of a document | A black-box recording of a process |

---

## 🚀 Quick Start (30 Seconds)

### 1. Install
```bash
pip install epi-recorder
```

### 2. Record
Run your script with `epi record`. It captures everything automatically.
```bash
epi record --out my_run.epi -- python train_model.py
```

### 3. View
Open the evidence package in your browser. No internet required.
```bash
epi view my_run.epi
```

> **Try it now:** [Open the Live Demo in Google Colab](https://colab.research.google.com/github/mohdibrahimaiml/EPI-V1.1/blob/main/colab_demo.ipynb)

---

## ⚙️ How It Works

EPI transforms opaque AI runs into transparent, verifiable proofs by unifying three components:

### 1. The Recorder (`epi record`)
Intercepts execution at the system level.
- **Shell**: Commands, stdout/stderr, exit codes.
- **LLM APIs**: OpenAI, Ollama, Anthropic (inputs/outputs logged & cached).
- **Files**: Inputs read and artifacts written.
- **Environment**: OS, Python packages, git state.

### 2. The Container (`.epi`)
A ZIP-based format that holds the truth.
```text
my_run.epi
├── manifest.json        # Metadata + Ed25519 Signature
├── steps.jsonl          # Chronological timeline of events
├── artifacts/           # Content-addressed files (sha256)
├── cache/               # Cached LLM responses (for deterministic replay)
└── viewer/              # Embedded HTML/JS viewer (Zero-install)
```

### 3. The Verifier (`epi verify`)
Ensures the package hasn't been tampered with.
- Checks **SHA-256** hashes of every step.
- Validates **Ed25519** cryptographic signature.
- Re-executes checks (e.g., "Accuracy > 90%").

---

## 🧩 Architecture

```mermaid
graph LR
    User[User Script] -->|Intercepts| Recorder
    Recorder -->|Writes| Evidence[.EPI File]
    
    subgraph "The .EPI Container"
        Evidence --> Manifest[Manifest]
        Evidence --> Timeline[Steps & Logs]
        Evidence --> Artifacts[Files & Data]
        Evidence --> Sig[Signature]
    end
    
    Evidence -->|Reads| Verifier
    Evidence -->|Renders| Viewer
    
    Verifier -->|Outputs| Report[Integrity Report]
    Viewer -->|Displays| UI[Browser Interface]
```

---

## 🔐 Security & Privacy

### "Safe by Default"
- **Read-Only**: The Viewer is just static HTML/JSON. It **never executes code** from the file.
- **Redaction**: API keys (OpenAI, AWS, etc.) are automatically detected and redacted before saving.
- **Sandboxed**: Replaying a workflow (`epi replay`) runs in a constrained environment.

---

## 🐍 Python API

For deeper integration, use the Python context manager.

```python
from epi_recorder import record

# Everything inside this block is recorded
with record("experiment.epi", goal="Test Llama-3 Performance"):
    
    # 1. This LLM call is intercepted & cached
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # 2. Files created here are saved as artifacts
    with open("result.txt", "w") as f:
        f.write(response.choices[0].message.content)

# result.epi is now saved and signed!
```

---

## 📄 License
**Apache 2.0** - Open Source and compatible with commercial use.

---

<p align="center">
  <b>Built for the future of AI Transparency.</b><br>
  <i>Turning opaque runs into verifiable proofs.</i>
</p>
