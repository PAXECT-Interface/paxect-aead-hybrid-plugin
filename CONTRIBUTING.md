

#  **Contributing Guidelines**

Thank you for your interest in contributing to the **PAXECT AEAD Hybrid Plugin**.

---

## Overview

This repository is part of the **PAXECT Interface Ecosystem**.
All contributions must remain:

* **Deterministic:** no randomization or non-reproducible behavior
* **Cross-platform:** must run identically on Linux, macOS, and Windows
* **Secure:** compliant with PAXECT Core’s privacy-by-default and offline-first policy
* **Dependency-free:** no external network, telemetry, or AI/ML frameworks
* **Consistent:** AES-GCM and ChaCha20-Poly1305 must produce reproducible results under all conditions

Each change must preserve **byte-identical behavior** and maintain **authenticated encryption integrity** across supported environments.

---

##  Development Setup

### 1. Fork the repository

Create your own fork to contribute safely.

### 2. Clone your fork locally

```bash
git clone https://github.com/<your-username>/paxect-aead-hybrid-plugin.git
cd paxect-aead-hybrid-plugin
```

### 3. (Optional) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 5. Run a basic verification

```bash
python3 demos/demo_01_quick_encrypt_decrypt.py
```

---

##  Testing Standards

* Use **pytest** for all new tests (`tests/` directory).
* Keep tests **deterministic and platform-neutral**.
* Validate both **streaming (stdin/stdout)** and **file-based** I/O modes.
* Avoid hardcoded paths — always use `tempfile` for temporary data.
* Ensure AES-GCM and ChaCha20-Poly1305 both pass round-trip integrity verification.

Example:

```bash
python3 -m pytest -v
```

---

##  Pull Requests

* Use branch names like:
  `feature/<short-description>` or `fix/<issue-id>`
* Add a clear description and link related issues.
* Verify that **all 7 demos** still pass successfully:

  ```bash
  ./demos/demo_07_cross_platform_smoke.sh
  ```
* Code must pass static linting:

  ```bash
  flake8 && black --check .
  ```

---

##  Security and Compliance

* No third-party telemetry, analytics, or network dependencies.
* Avoid AI-generated randomness or heuristic encryption behavior.
* Each PR is automatically checked for **deterministic compliance** and **AEAD integrity safety**.
* Secrets, keys, or credentials **must never** be committed in source code.

For confidential security concerns, report privately to:
📧 **security@[paxect-team@outlook.com](mailto:paxect-team@outlook.com)**

---

##  Communication

* **Issues:** Bug reports, feature ideas, or reproducibility feedback
* **Discussions:** Technical proposals or cryptographic architecture topics
* **Security:** Coordinated disclosure via private email


##  License

All contributions fall under the **Apache 2.0 License**
and are subject to **PAXECT’s deterministic, audit-compliant development policies**.

---

 **Deterministic · Secure · Offline · Enterprise-Ready**
 
 © 2025 PAXECT Systems — Authenticated Encryption for the Modern Enterprise
