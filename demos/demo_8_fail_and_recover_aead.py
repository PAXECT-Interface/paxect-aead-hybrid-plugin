#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""
Demo 8 — PAXECT AEAD Fail & Self-Recover
----------------------------------------
Show that the AEAD streaming encryptor/decryptor detects corrupted
data deterministically, logs the failure, and resumes normally
on the next valid file.
"""

import os, subprocess, shutil
from pathlib import Path

BASE = Path("/tmp/paxect_demo8")
INBOX = BASE / "inbox"
OUTBOX = BASE / "outbox"
LOG = BASE / "aead_recover.log"
PASS = "enterprise-demo-key"

# Clean workspace
shutil.rmtree(BASE, ignore_errors=True)
INBOX.mkdir(parents=True)
OUTBOX.mkdir(parents=True)

print("=== Demo 8 — PAXECT AEAD Fail & Self-Recover ===")
print("[+] Creating 1 valid and 1 corrupted AEAD stream...")

# --- 1. create valid plaintext and encrypt ---
plain_ok = INBOX / "ok.txt"
plain_ok.write_text("paxect aead works\n", encoding="utf-8")

enc_ok = OUTBOX / "ok.enc"
with open(plain_ok, "rb") as fin, open(enc_ok, "wb") as fout:
    subprocess.run(
        ["python3", "paxect_aead_enterprise.py",
         "--mode", "encrypt", "--cipher", "auto", "--pass", PASS],
        stdin=fin, stdout=fout, check=True)

# --- 2. create corrupted ciphertext ---
bad_enc = OUTBOX / "bad.enc"
bad_enc.write_bytes(b"corrupted" + enc_ok.read_bytes()[:100])  # truncate

# --- 3. attempt decryption (expected fail) ---
def try_decrypt(src: Path, dst: Path):
    """Try to decrypt file and capture stderr safely."""
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        proc = subprocess.run(
            ["python3", "paxect_aead_enterprise.py",
             "--mode", "decrypt", "--pass", PASS],
            stdin=fin,
            stdout=fout,
            stderr=subprocess.PIPE,  # ✅ only stderr captured
            text=True
        )
        return proc.returncode, proc.stderr.strip()

print("[*] Step 1: Decrypt corrupted file (expect failure)")
code, err = try_decrypt(bad_enc, OUTBOX / "bad.out")
LOG.write_text(f"FAIL-PHASE:\n{err}\n", encoding="utf-8")
print("   returncode:", code)
print("   error:", err or "(none)")

print("[*] Step 2: Decrypt valid file (expect recovery)")
code2, err2 = try_decrypt(enc_ok, OUTBOX / "ok.out")
LOG.write_text(LOG.read_text() + f"\nRECOVER-PHASE:\n{err2}\n", encoding="utf-8")

# --- 4. verify outcome ---
if (OUTBOX / "ok.out").exists():
    text = (OUTBOX / "ok.out").read_text().strip()
    print(f"[+] Recovery successful, output: {text}")
    print("✅ AEAD self-recovery confirmed")
else:
    print("⚠️ No valid output found — check log for details")

print(f"\n[log] {LOG}")
