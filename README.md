# research-ledger-digests

Hash-chain digests of the btc-tracker Research OS event ledger.

Each commit records the SHA-256 chain head of an append-only event ledger.
The ledger itself is private (for now); these digests prove, via this repo's
commit history, that the ledger existing at any commit date has not been
rewritten since. When ledger history is published later, anyone can recompute
the chain and match it against these digests.
