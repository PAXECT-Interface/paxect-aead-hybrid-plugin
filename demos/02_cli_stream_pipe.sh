#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# PAXECT AEAD Hybrid Plugin — Demo 02: CLI Stream Pipeline
# v1.0.0
#
# Shows how to use the plugin in streaming mode via stdin/stdout.
# Perfect for DevOps, CI/CD and data pipelines.

set -euo pipefail

PLUGIN="./paxect_aead_enterprise.py"
PASS="demo123"

echo "=== PAXECT AEAD Demo 02 — CLI Stream Pipeline ==="
TMPDIR=$(mktemp -d -t paxect_demo02_XXXX)
SRC="$TMPDIR/input.txt"
ENC="$TMPDIR/output.aead"
DEC="$TMPDIR/decrypted.txt"

# 1️⃣ Create input file
echo "[1] Generating source file: $SRC"
{
  echo "PAXECT AEAD Demo 02 — CLI Stream Pipeline Test"
  echo "Generated at: $(date -u)"
  echo "CPU Architecture: $(uname -m)"
} > "$SRC"

# 2️⃣ Encrypt via stdin/stdout pipe
echo "[2] Encrypting via pipe → $ENC"
cat "$SRC" | python3 "$PLUGIN" --mode encrypt --cipher auto --pass "$PASS" > "$ENC"

# 3️⃣ Decrypt via pipe
echo "[3] Decrypting via pipe → $DEC"
cat "$ENC" | python3 "$PLUGIN" --mode decrypt --pass "$PASS" > "$DEC"

# 4️⃣ Verify integrity
echo "[4] Verifying integrity (SHA-256)"
SHA_SRC=$(sha256sum "$SRC" | awk '{print $1}')
SHA_DEC=$(sha256sum "$DEC" | awk '{print $1}')
echo "Source SHA:    $SHA_SRC"
echo "Decrypted SHA: $SHA_DEC"

if [ "$SHA_SRC" = "$SHA_DEC" ]; then
  echo "✅  Stream pipeline integrity verified!"
else
  echo "❌  Integrity mismatch!"
  exit 2
fi

echo "Temporary files in: $TMPDIR"
echo "=== Demo 02 completed successfully ==="
