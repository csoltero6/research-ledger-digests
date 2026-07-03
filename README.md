# research-ledger-digests

Hash-chain digests and a verifiable export of the btc-tracker Research OS
event ledger (a transparent quantitative-research platform for prediction
markets — paper trading).

## What's here

- `chain_digest.json` — the current SHA-256 chain head and per-segment
  summary. Every commit to this repo timestamps a head: the commit history
  proves the ledger existing at any commit date has not been rewritten since.
- `ledger-export/` — the full event ledger. Public events appear as their
  exact original JSON lines; private events (raw trade rows, exact rule
  triggers) appear as hash commitments revealing only `prev_hash` and
  `line_sha256` — nothing about content, everything needed for verification.
- `verify_export.py` — a stdlib-only verifier. Run:

      python3 verify_export.py

  It recomputes the hash chain from genesis across every event (public and
  redacted alike) and checks the head against `chain_digest.json`. If any
  historical line was edited, inserted, or deleted, it fails at that line.

You do not need to trust the operator to run this — that is the point.
