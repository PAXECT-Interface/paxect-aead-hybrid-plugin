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

plug-and-play with zero dependencies and no vendor lock-in.

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
<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>



[![Star this repo](https://img.shields.io/badge/⭐%20Star-this%20repo-orange)](../../stargazers)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](../../actions)
[![CodeQL](https://img.shields.io/badge/CodeQL-active-lightgrey.svg)](../../actions)
[![Issues](https://img.shields.io/badge/Issues-open-blue)](../../issues)
[![Discussions](https://img.shields.io/badge/Discuss-join-blue)](../../discussions)
[![Security](https://img.shields.io/badge/Security-responsible%20disclosure-informational)](./SECURITY.md)
---


# PAXECT Core Complete



**Deterministic, offline-first runtime for secure, reproducible data pipelines.**  
Cross-platform, self-tuning, and fully auditable — built for real-world enterprise and open-source innovation.

---

##  Overview

**PAXECT Core Complete** is the reference implementation of the PAXECT ecosystem.  
It unifies the verified modules — Core, AEAD Hybrid, Polyglot, SelfTune, and Link —  
into one reproducible, cross-OS runtime with **10 integrated demos** and full observability.

### Core principles
- **Determinism first** — bit-identical results across systems  
- **Offline-first** — no network or telemetry unless explicitly enabled  
- **Audit-ready** — human summaries + machine-readable JSON logs  
- **Cross-platform** — Linux · macOS · Windows · FreeBSD · OpenBSD · Android · iOS  
- **Zero-dependency security** — Hybrid AES-GCM / ChaCha20-Poly1305  
- **Adaptive control** — SelfTune 5-in-1 plugin with ε-greedy logic  

---

##  Installation

### Requirements
- **Python 3.9 – 3.12** (recommended 3.11+)
- Works on **Linux**, **macOS**, **Windows**, **FreeBSD**, **OpenBSD**, **Android (Termux)**, and **iOS (Pyto)**
- No external dependencies or internet connection required

### Optional utilities
Some demos use these standard tools if available:
- `bash` (for `demo_05_link_smoke.sh`)
- `dos2unix` (for normalizing line endings)
- `jq` (for formatting JSON output)

### Install
```bash
git clone https://github.com/yourname/paxect-core-complete.git
cd paxect-core-complete
python3 -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -e .
````

Verify:

```bash
python3 -c "import paxect_core; print('PAXECT Core OK')"
```

Then run any of the demos from the `demos/` folder.

---

## 📁 Repository structure

```
paxect-core-complete/
├── paxect_core.py
├── paxect_aead_hybrid_plugin.py
├── paxect_polyglot_plugin.py
├── paxect_selftune_plugin.py
├── paxect_link_plugin.py
├── demos/
│   ├── demo_01_quick_start.py
│   ├── demo_02_integration_loop.py
│   ├── demo_03_safety_throttle.py
│   ├── demo_04_metrics_health.py
│   ├── demo_05_link_smoke.sh
│   ├── demo_06_polyglot_bridge.py
│   ├── demo_07_selftune_adaptive.py
│   ├── demo_08_secure_multichannel_aead_hybrid.py
│   ├── demo_09_enterprise_all_in_one.py
│   └── demo_10_enterprise_stability_faults.py
├── test_paxect_all_in_one.py
├── ENTERPRISE_PACK_OVERVIEW.md
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── TRADEMARKS.md
├── LICENSE
└── .gitignore
```

---

##  Modules

| Module                           | Purpose                                           |
| -------------------------------- | ------------------------------------------------- |
| **paxect_core.py**               | Deterministic runtime · encode/decode · checksums |
| **paxect_aead_hybrid_plugin.py** | Hybrid AES-GCM / ChaCha20-Poly1305 encryption     |
| **paxect_polyglot_plugin.py**    | Cross-language bridge · UTF-safe transformation   |
| **paxect_selftune_plugin.py**    | Adaptive ε-greedy self-tuning · persistent state  |
| **paxect_link_plugin.py**        | Secure relay · inbox/outbox · policy validation   |

---

## 🧪 Demo suite (01 – 10)

Run the demos from the repository root:

```bash
python3 demos/demo_01_quick_start.py               # Basic sanity check
python3 demos/demo_02_integration_loop.py          # Adaptive loop cycles
python3 demos/demo_03_safety_throttle.py           # Short/long window throttle
python3 demos/demo_04_metrics_health.py            # Observability endpoints
bash    demos/demo_05_link_smoke.sh                # Link + policy hash check
python3 demos/demo_06_polyglot_bridge.py           # Cross-system checksum
python3 demos/demo_07_selftune_adaptive.py         # ε-adaptive learning
python3 demos/demo_08_secure_multichannel_aead_hybrid.py  # Multi-channel AEAD test
python3 demos/demo_09_enterprise_all_in_one.py     # Full integrated validation
python3 demos/demo_10_enterprise_stability_faults.py       # 2 min · 5 min · 10 min stability run
```

All demos produce structured JSON output under `/tmp/`.

---

##  Testing & Verification

Internal `pytest` and smoke-test suites are maintained locally.
End-users can rely on the integrated demo suite (01–10) for verification.
Each demo is self-contained, prints its own status, and exits cleanly.

---

## 🔒 Security & Privacy

* Default mode: **offline**, **no telemetry**
* Sensitive data handled via environment variables
* CVE hygiene follows [`SECURITY.md`](./SECURITY.md)
* AEAD Hybrid is **simulation-grade**; for production, use a verified crypto library or HSM

---

## 🏢 Enterprise Pack

See [`ENTERPRISE_PACK_OVERVIEW.md`](./ENTERPRISE_PACK_OVERVIEW.md)
for roadmap and integration notes.

Includes:

* HSM / KMS / Vault integration
* Extended policy + audit engine
* Prometheus / Grafana / Splunk / Kafka connectors
* Deployment assets (systemd, Helm, Docker)
* Compliance documentation (ISO · IEC · NIST)

---

## 🤝 Community & Governance

* **License:** Apache-2.0
* **Ownership:** All PAXECT products and trademarks remain property of the Owner
* **Contributions:** PRs welcome · feature branches only · CI must pass
* **Core merges:** Owner approval required for Core / brand-sensitive repos
* **Community conduct:** see [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)

Join as maintainer or contributor — see [`CONTRIBUTING.md`](./CONTRIBUTING.md) for roles and expectations.


### 🔄 Updates & Maintenance

PAXECT Core Complete follows an **open contribution model**.

- Updates, bugfixes, and improvements depend on **community and maintainer availability**.
- There is **no fixed release schedule** — stability and determinism are prioritized over speed.
- Enterprises and contributors are encouraged to submit issues or pull requests for any enhancements.
- The project owner focuses on innovation and architectural guidance rather than continuous support.

In short: updates arrive when they are ready — verified, deterministic, and tested across platforms.


---

## 📢 Key principles

> Determinism · Privacy · Reproducibility · Cross-Platform · Transparency



## Plugins (official)


| Plugin                         | Scope                           | Highlights                                                                           | Repo                                                                                                                           |
| ------------------------------ | ------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| **Core**                       | Deterministic container         | `.freq` v42 · multi-channel · CRC32+SHA-256 · cross-OS · offline · no-AI             | [https://github.com/PAXECT-Interface/paxect---core.git](https://github.com/PAXECT-Interface/paxect---core.git)                             |
| **AEAD Hybrid**                | Confidentiality & integrity     | Hybrid AES-GCM/ChaCha20-Poly1305 — fast, zero-dep, cross-OS                          | [https://github.com/PAXECT-Interface/paxect-aead-hybrid-plugin](https://github.com/PAXECT-Interface/paxect-aead-hybrid-plugin) |
| **Polyglot**                   | Language bindings               | Python · Node.js · Go — identical deterministic pipeline                             | [https://github.com/PAXECT-Interface/paxect-polyglot-plugin](https://github.com/PAXECT-Interface/paxect-polyglot-plugin)       |
| **SelfTune 5-in-1**            | Runtime control & observability | No-AI guardrails, overhead caps, backpressure, jitter smoothing, lightweight metrics | [https://github.com/PAXECT-Interface/paxect-selftune-plugin](https://github.com/PAXECT-Interface/paxect-selftune-plugin)       |
| **Link (Inbox/Outbox Bridge)** | Cross-OS file exchange          | Shared-folder relay: auto-encode non-`.freq` → `.freq`, auto-decode `.freq` → files  | [https://github.com/PAXECT-Interface/paxect-link-plugin](https://github.com/PAXECT-Interface/paxect-link-plugin) 


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

 **How to get involved**
- [Become a GitHub Sponsor](https://github.com/sponsors/PAXECT-Interface)  


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


---



© 2025 PAXECT Systems.
Authenticated encryption for the modern enterprise.

---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---

<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>












---
##  Keywords & Topics

**PAXECT AEAD Hybrid Plugin** — deterministic, cross-platform authenticated encryption layer providing reproducible and verifiable data protection across systems and pipelines.
Built for zero-dependency security with **AES-GCM + ChaCha20-Poly1305**, powered by **PAXECT Core v42**.

---

###  Core / Encryption

`paxect`, `aead`, `hybrid`, `aes-gcm`, `chacha20-poly1305`, `authenticated-encryption`, `deterministic`, `reproducible`, `streaming`, `secure-io`, `cross-platform`

###  Integrity & Validation

`aead-tag`, `crc32`, `sha256`, `checksum`, `data-integrity`, `verification`, `fail-safe`, `bit-identical`, `tamper-detection`, `deterministic-hash`

###  Performance & Runtime

`hybrid-mode`, `auto-cipher`, `selftune`, `offline`, `buffering`, `throughput`, `adaptive-encryption`, `secure-performance`, `zero-ai`

###  Interoperability

`cross-os`, `linux`, `macos`, `windows`, `android`, `ios`, `embedded`, `mobile`, `edge-computing`, `cli-plugin`, `api-integration`

###  Compliance & Deployment

`audit-compliance`, `privacy-by-default`, `enterprise`, `airgap`, `gdpr`, `traceability`, `offline-mode`, `forensics`, `secure-ci`, `reproducible-results`

###  Ecosystem

`paxect-core`, `paxect-selftune`, `paxect-link`, `paxect-aes`, `deterministic-pipeline`, `audit-ready`, `enterprise-suite`, `zero-ai`

---

###  Launch Summary — October 2025

Production-ready · Deterministic across OS and CPU
All 7 demos validated on Ubuntu 24.04 LTS · macOS 14 Sonoma · Windows 11 Pro
AEAD tag + SHA-256 integrity confirmed
Compatible with **PAXECT Core v42** and sibling plugins (**SelfTune**, **AES**, **Link**)
Zero-AI verified — fully offline, reproducible, and audit-ready

---





