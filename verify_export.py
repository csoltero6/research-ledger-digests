#!/usr/bin/env python3
"""Independent verifier for the research-ledger export. Stdlib only.

Usage:  python3 verify_export.py [export_dir]

Recomputes the ledger hash chain from genesis across every exported segment.
Public events are full JSON lines (hash recomputed from their exact bytes);
redacted events are commitments revealing only prev_hash and line_sha256 —
enough to verify linkage without revealing content. If ANY historical line
was edited, inserted, or deleted, verification fails at that exact line.
Compare the final head against chain_digest.json in this repository (and its
git commit history, which timestamps every head).
"""
import glob
import hashlib
import json
import os
import sys

GENESIS = "sha256:" + hashlib.sha256(b"research-os-genesis:btc-tracker").hexdigest()


def main(export_dir="ledger-export"):
    head = GENESIS
    n_public = n_redacted = 0
    paths = sorted(glob.glob(os.path.join(export_dir, "*.jsonl")))
    if not paths:
        print(f"no segments found under {export_dir}/"); return 1
    for path in paths:
        with open(path, "rb") as f:
            for i, raw in enumerate(f, 1):
                line = raw.rstrip(b"\n")
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("prev_hash") != head:
                    print(f"CHAIN BROKEN at {os.path.basename(path)}:{i} "
                          f"(event {rec.get('event_id')}): prev_hash "
                          f"{rec.get('prev_hash')} != expected {head}")
                    return 1
                if rec.get("redacted"):
                    head = rec["line_sha256"]
                    n_redacted += 1
                else:
                    head = "sha256:" + hashlib.sha256(line).hexdigest()
                    n_public += 1
    print(f"CHAIN OK — {n_public + n_redacted} events verified "
          f"({n_public} public, {n_redacted} redacted commitments)")
    print(f"chain head: {head}")
    try:
        with open(os.path.join(os.path.dirname(export_dir.rstrip("/")) or ".",
                               "chain_digest.json")) as f:
            digest = json.load(f)
        match = digest.get("chain_head") == head
        print(f"matches chain_digest.json: {'YES' if match else 'NO — MISMATCH'}")
        return 0 if match else 1
    except OSError:
        print("chain_digest.json not found next to export dir; "
              "compare the head manually")
        return 0


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:] or [])))
