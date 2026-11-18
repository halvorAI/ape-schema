# Conformance

Test data every APE implementation (SDKs and receivers) should run in its own tests, so they all accept and reject the same events. `npm test` at the repository root checks these files against [`ape/v0.1.json`](../ape/v0.1.json) and the card-number rule in [`docs/FIELDS.md`](../docs/FIELDS.md#cross-field-rules).

| File | What it holds |
| --- | --- |
| [`events.json`](events.json) | Events with the verdict an implementation must give. `expect` is `valid` or `invalid`; for an invalid event, `rule` says why: `schema` (the JSON Schema rejects it) or `pan` (it passes the schema, but a free-text field holds a possible card number). |
| [`sign-vector.json`](sign-vector.json) | One event, its RFC 8785 canonical form, a key pair and the detached JWS. Re-signing the event with `private_jwk` must give exactly `sig`; Ed25519 is deterministic. |
| [`jcs-vectors.json`](jcs-vectors.json) | Canonical JSON for numbers (as IEEE 754 bit patterns, including RFC 8785 appendix B) and for objects with tricky keys and strings. Generated from the TypeScript SDK's `canonicalize`. |

A producer SDK that redacts before validating should run `events.json` through its validator directly, not through its emit path: redaction would remove the card numbers that the `pan` cases test for.

## Status of the SDKs

Run on 2026-11-18 against this revision.

| Implementation | `events.json` | Differences |
| --- | --- | --- |
| [`@halvorai/ingest`](https://github.com/halvorAI/ingest-js) (Node.js) | 40 / 40 | none |
| [`halvorai-ingest`](https://github.com/halvorAI/ingest-python) (Python) | 40 / 40 | none |

Both SDKs keep a copy of these files in their own test fixtures; the copies matched this revision on that date. The Go and Java SDKs are frozen, and the Dart SDK is archived.
