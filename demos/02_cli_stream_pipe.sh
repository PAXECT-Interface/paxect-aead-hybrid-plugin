#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# PAXECT AEAD Hybrid Plugin — Demo 02: CLI Stream Pipeline
# v1.0.1
#
# Demonstrates streaming encryption/decryption via stdin/stdout pipes.
# Ideal for DevOps, CI/CD, and data-processing pipelines.

set -euo pipefail

PLUGIN="./paxect_aead_enterprise.py"
PASS="demo123"

echo "=== PAXECT AEAD Demo 02 — CLI Stream Pipeline ==="
echo "Local time : $(date '+%Y-%m-%d %H:%M:%S')"
echo "UTC time   : $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
TMPDIR=$(mktemp -d -t paxect_demo02_XXXX)
SRC="$TMPDIR/input.txt"
ENC="$TMPDIR/output.aead"
DEC="$TMPDIR/decrypted.txt"
echo "Temp dir   : $TMPDIR"
echo

# 1️⃣ Create input file
echo "[1] Generating source file..."
{
  echo "PAXECT AEAD Demo 02 — CLI Stream Pipeline Test"
  echo "Generated at UTC: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "Platform: $(uname -s) $(uname -m)"
} > "$SRC"

# 2️⃣ Encrypt via stdin/stdout
echo "[2] Encrypting via pipe → $ENC"
cat "$SRC" | python3 "$PLUGIN" --mode encrypt --cipher auto --pass "$PASS" > "$ENC"

# 3️⃣ Decrypt via stdin/stdout
echo "[3] Decrypting via pipe → $DEC"
cat "$ENC" | python3 "$PLUGIN" --mode decrypt --pass "$PASS" > "$DEC"

# 4️⃣ Verify integrity
echo "[4] Verifying integrity (SHA-256)"
SHA_SRC=$(sha256sum "$SRC" | awk '{print $1}')
SHA_DEC=$(sha256sum "$DEC" | awk '{print $1}')
echo "Source SHA-256    : $SHA_SRC"
echo "Decrypted SHA-256 : $SHA_DEC"

if [ "$SHA_SRC" = "$SHA_DEC" ]; then
  echo "✅  Stream pipeline integrity verified"
else
  echo "❌  Integrity mismatch!"
  exit 2
fi

echo
echo "[5] Environment summary:"
echo "    OS      : $(uname -s)"
echo "    Arch    : $(uname -m)"
echo "    Python  : $(python3 --version | awk '{print $2}')"
echo "    Date    : $(date -u)"
echo
echo "Temporary files stored in: $TMPDIR"
echo "=== Demo 02 completed successfully ==="

