<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>

# PAXECT Data Policy — AEAD Hybrid Plugin

The **PAXECT AEAD Hybrid Plugin** enforces a strict and transparent data-size policy  
to guarantee deterministic performance, prevent misuse, and maintain predictable encryption behavior.  
This policy aligns with professional standards found in systems like Kafka, MQTT, and gRPC.

---

## 1. Technical Limit

- **Default limit:** Maximum **512 MB** per encryption or decryption operation.  
- **Configurable:**  
  You can increase this limit via an environment variable:

  ```bash
  export PAXECT_MAX_INPUT_MB=8192  # Allow up to 8 GB



 
 **Error message when exceeded:**

  ```
  ❌ Input size exceeds PAXECT AEAD policy limit (default 512 MB).
  Adjust limit using PAXECT_MAX_INPUT_MB if necessary.
  ```

---

## 2. Applicability

* The limit applies **per operation**, **per pipeline**, and **per plugin instance**.
* Large data must be handled via **chunked streaming** or **file-based I/O**.
* AEAD frames are authenticated individually to preserve deterministic reproducibility.
* Other plugins (Core, Polyglot, Link, SelfTune) may define additional limits in their own policies.

---

## 3. Positioned as a Feature

PAXECT’s deliberate data-size policy ensures **reliability, security, and deterministic output**.
Just like other enterprise data frameworks, it is a **safeguard** — not a restriction.

> *“PAXECT AEAD guarantees stable, verifiable encryption up to 512 MB per run.
> For enterprise workloads, limits are configurable and scale predictably.”*

---

**Questions or requests?**
📧 **[PAXECT-Team@outlook.com](mailto:PAXECT-Team@outlook.com)** or open an **Issue / Discussion** on GitHub.

---

© 2025 PAXECT Systems. All rights reserved.

```


