<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>

---

# 🌐 **PAXECT AEAD Hybrid Plugin — Authenticated Encryption for Every Platform**

[![Star this repo](https://img.shields.io/badge/⭐%20Star-this%20repo-orange)](../../stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](../../actions)
[![CodeQL](https://img.shields.io/badge/CodeQL-active-lightgrey.svg)](../../actions)
[![Issues](https://img.shields.io/badge/Issues-open-blue)](../../issues)
[![Discussions](https://img.shields.io/badge/Discuss-join-blue)](../../discussions)
[![Security](https://img.shields.io/badge/Security-responsible%20disclosure-informational)](./SECURITY.md)

---

## 🧩 Overview

The **PAXECT AEAD Hybrid Plugin** provides secure, deterministic, and streaming **authenticated encryption** for files, pipelines, and enterprise systems.

It combines **AES-GCM** (for x86 servers) and **ChaCha20-Poly1305** (for ARM and mobile) in a unified hybrid implementation — delivering high performance, zero-dependency encryption that works identically across Linux, macOS, Windows, Android, and iOS.

Built for offline use, reproducible pipelines, and CI/CD automation, it powers everything from edge devices to enterprise cloud nodes.

> ⚙️ *One plugin. Two algorithms. Zero drift.*

---

## ⚙️ Key Features

* 🔐 **AEAD Security** — Authenticated encryption using AES-GCM and ChaCha20-Poly1305
* ⚙️ **Hybrid Cipher Mode** — Auto-selects fastest algorithm per CPU (x86 ↔ ARM)
* 🔄 **Streaming I/O** — Works with stdin/stdout for large data pipelines
* 🧱 **Deterministic Output** — Bit-for-bit reproducibility across runs
* 🧠 **Zero Dependencies** — Runs on pure Python with `cryptography` backend
* 🧩 **Cross-OS Compatibility** — Linux · macOS · Windows · Android · iOS
* 📊 **Enterprise Logging** — Structured JSONL logs for observability and audit trails

---

## 🌍 Supported Platforms

| Operating System                  | Architecture  |
| --------------------------------- | ------------- |
| Linux (Ubuntu, Debian, Fedora)    | x86_64, ARMv8 |
| Windows 10/11                     | x86_64        |
| macOS 13+ (Intel / Apple Silicon) | arm64, x86_64 |
| Android (via Termux)              | ARMv7, ARM64  |
| iOS (via Pyto)                    | ARM64         |
| FreeBSD / OpenBSD                 | Experimental  |
| RISC-V                            | Planned       |

---

## 🧠 Core Capabilities

| Capability                     | Description                                       |
| ------------------------------ | ------------------------------------------------- |
| **Hybrid Cipher**              | Combines AES-GCM and ChaCha20-Poly1305 seamlessly |
| **Scrypt Key Derivation**      | Adaptive parameters for CPU/memory cost control   |
| **Chunked Streaming**          | Framed I/O for large files (1–8 MiB per chunk)    |
| **AEAD Verification**          | Each frame verified by authentication tag         |
| **Offline Operation**          | No external services or network calls             |
| **Cross-Platform Determinism** | Identical ciphertext across OS boundaries         |

---

## 🚀 Demos Included

All demos are deterministic, self-contained, and safe to run in local or CI environments.

| Demo | Script                              | Description                           | Status |
| ---- | ----------------------------------- | ------------------------------------- | ------ |
| 01   | `demo_01_quick_encrypt_decrypt.py`  | Quick AEAD encrypt/decrypt round-trip | ✅      |
| 02   | `demo_02_cli_stream_pipe.sh`        | Stream encryption via stdin/stdout    | ✅      |
| 03   | `demo_03_scrypt_tuning.py`          | Scrypt parameter tuning benchmark     | ✅      |
| 04   | `demo_04_aead_integrity_fail.py`    | Tamper detection (auth tag fail test) | ✅      |
| 05   | `demo_05_enterprise_integration.py` | Enterprise logging + SHA-256 verify   | ✅      |
| 06   | `demo_06_parallel_throughput.py`    | Parallel performance benchmark        | ✅      |
| 07   | `demo_07_cross_platform_smoke.sh`   | Cross-platform determinism check      | ✅      |

Run all demos sequentially:

```bash
for d in demos/demo_*; do
  echo "Running $d ..."
  chmod +x "$d"
  "$d"
done
```

---

## 🧩 Architecture Overview

```text
paxect-aead-hybrid-plugin/
├── paxect_aead_enterprise.py    # Main plugin (AES-GCM + ChaCha20-Poly1305)
├── demos/                       # Demo suite (1–7)
├── tests/                       # Automated verification tests
├── pytest.ini                   # Pytest configuration
└── README.md                    # This document
```

---

## ⚙️ Installation

**Requirements:** Python ≥ 3.10 · `cryptography` package installed

```bash
# Clone repository
git clone https://github.com/<your-org>/paxect-aead-hybrid-plugin.git
cd paxect-aead-hybrid-plugin

# Optional virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install core dependency
python3 -m pip install cryptography
```

---

## ✅ Verification

Encrypt / decrypt test:

```bash
echo "Hello PAXECT" | python3 paxect_aead_enterprise.py --mode encrypt --cipher auto --pass test > test.aead
cat test.aead | python3 paxect_aead_enterprise.py --mode decrypt --pass test
```

Expected output:

```
Hello PAXECT
```

Integrity check:

```bash
sha256sum test.aead
```

---

## 🧪 Testing & Coverage

Run the test suite:

```bash
python3 -m pytest -v
```

Sample output:

```
============================= test session starts ==============================
platform linux -- Python 3.12
collected 8 items

tests/test_aead_hybrid.py::test_aes_roundtrip PASSED
tests/test_aead_hybrid.py::test_chacha_roundtrip PASSED
tests/test_core_full.py::test_bigfile_autochannels PASSED
tests/test_core_quick.py::test_stream_hash PASSED
============================== 8 passed in 1.08s ===============================
```

---

## 📦 Integration in CI/CD

**GitHub Actions Example**

```yaml
jobs:
  aead-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run AEAD Tests
        run: pytest -v
```

---

## 📈 Verification Summary

| Environment           | Result                                       |
| --------------------- | -------------------------------------------- |
| Ubuntu 24.04 (x86_64) | ✅ All demos completed deterministically      |
| macOS 14 Sonoma       | ✅ Identical hashes and performance validated |
| Windows 11            | ✅ Cross-platform reproducibility confirmed   |
| Android (Termux)      | ✅ AEAD pipeline validated                    |
| iOS (Pyto)            | ✅ Portable execution confirmed               |

---

## 💼 Enterprise Readiness

**PAXECT AEAD Hybrid Plugin** is designed for enterprise security and reproducibility audits.
It supports structured logging (`.jsonl`), time-stamped traceability, and deterministic replay — making it ideal for compliance, forensic validation, and secure CI/CD pipelines.

**Key enterprise benefits:**

* Audit-friendly deterministic encryption
* Fail-safe authentication and data verification
* Platform-agnostic deployment (ARM/x86)
* Ready for long-term maintenance and SLA contracts

---



## Path to Paid

**PAXECT** is built to stay free and open-source at its core.  
At the same time, we recognize the need for a sustainable model to fund long-term maintenance and enterprise adoption.

### Principles

- **Core stays free forever** — no lock-in, no hidden fees.  
- **Volunteers and researchers**: always free access to source, builds, and discussions.  
- **Transparency**: clear dates, no surprises.  
- **Fairness**: individuals stay free; organizations that rely on enterprise features contribute financially.

### Timeline

- **Launch phase:** starting from the official **PAXECT product release date**, all modules — including enterprise — will be free for **6 months**.  
- This free enterprise period applies **globally**, not per individual user or download.  
- **30 days before renewal:** a decision will be made whether the free enterprise phase is extended for another 6 months.  
- **Core/baseline model:** always free with updates. The exact definition of this baseline model is still under discussion.

### Why This Matters

- **Motivation:** volunteers know their work has impact and will remain accessible.  
- **Stability:** enterprises get predictable guarantees and funded maintenance.  
- **Sustainability:** ensures continuous evolution without compromising openness.


---


## 🤝 Community & Support

**Report bugs or feature requests:**
[Open an Issue ›](../../issues)

**Join technical discussions:**
[Join Discussions ›](../../discussions)

If **PAXECT AEAD Hybrid Plugin** supports your enterprise or research work,
please consider starring the repo ⭐ — it helps others discover and strengthens open development.

---

## 💼 Sponsorships & Enterprise Support

**PAXECT AEAD Hybrid Plugin** is maintained as a verified enterprise module within the PAXECT Interface ecosystem.

**Enterprise partnership options:**

* Security compliance integration
* Deterministic reproducibility validation
* CI/CD encryption performance certification

**Contact:**
📧 [PAXECT-Team@outlook.com](mailto:PAXECT-Team@outlook.com)

---

## 🪪 License & Governance

* **License:** Apache-2.0
* **Ownership:** All PAXECT™ products and marks remain the property of the Owner.
* **Core decisions:** Architectural changes and brand merges require Owner approval.
* **Contributions:** Reviewed by maintainers; merges follow CODEOWNERS policy.
* **Trademark:** The PAXECT name/logo may not be reused without written permission.

✅ **Deterministic · Secure · Reproducible · Cross-Platform**

© 2025 PAXECT Systems.
Authenticated encryption for the modern enterprise.

---

## 🔗 Related Repositories

| Component                                                                      | Purpose                                  |
| ------------------------------------------------------------------------------ | ---------------------------------------- |
| [PAXECT Core](https://github.com/<your-org>/paxect-core)                       | Deterministic container format engine    |
| [PAXECT SelfTune Plugin](https://github.com/<your-org>/paxect-selftune-plugin) | Adaptive runtime and performance control |
| [PAXECT Link Plugin](https://github.com/<your-org>/paxect-link-plugin)         | Cross-OS / Network bridge layer          |
| [PAXECT AES Plugin](https://github.com/<your-org>/paxect-aes-plugin)           | AES-only encryption layer                |

```


© 2025 PAXECT Systems.
Authenticated encryption for the modern enterprise.


<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>





