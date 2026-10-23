# Conformance

Test data every APE implementation (SDKs and receivers) should run in its own tests, so they all accept and reject the same events. `npm test` at the repository root checks these files against [`ape/v0.1.json`](../ape/v0.1.json) and the card-number rule in [`docs/FIELDS.md`](../docs/FIELDS.md#cross-field-rules).

| File | What it holds |
| --- | --- |
| [`events.json`](events.json) | Events with the verdict an implementation must give. `expect` is `valid` or `invalid`; for an invalid event, `rule` says why: `schema` (the JSON Schema rejects it) or `pan` (it passes the schema, but a free-text field holds a possible card number). |
| [`sign-vector.json`](sign-vector.json) | One event, its RFC 8785 canonical form, a key pair and the detached JWS. Re-signing the event with `private_jwk` must give exactly `sig`; Ed25519 is deterministic. |
| [`jcs-vectors.json`](jcs-vectors.json) | Canonical JSON for numbers (as IEEE 754 bit patterns, including RFC 8785 appendix B) and for objects with tricky keys and strings. Generated from the TypeScript SDK's `canonicalize`. |

A producer SDK that redacts before validating should run `events.json` through its validator directly, not through its emit path: redaction would remove the card numbers that the `pan` cases test for.

## Status of the SDKs

Run on 2026-10-23 against this revision.

| Implementation | `events.json` | Differences |
| --- | --- | --- |
| `halvorai_ingest` (Dart) | 40 / 40 | none |
| `@halvorai/ingest` (Node.js, zod model) | 37 / 40 | Not yet checking `payee.website`, `payee.resource_url` and label keys for card numbers |
| `halvorai-ingest` (Python) | 36 / 40 | The same three, and it accepts `null` for optional fields (`null-optional-field`) |
