# Changelog

All notable changes to the Agent Payment Event (APE) schema. Versions follow `MAJOR.MINOR`; minor versions only add optional fields. Until v1.0, a minor version may still make breaking changes, and the changelog will say so.

## Unreleased

Clarifications to v0.1, plus one tightening. The JSON Schema is unchanged.

- **Tightening:** the free-text fields checked for card numbers are now listed exactly in `docs/FIELDS.md`, and include `payee.website`, `payee.resource_url` and `labels` keys. Receivers adopting this reject events with a card number in those fields (`pan_detected`). Identifiers and `evidence[].value` are never checked.
- `rail_ref` keys are closed per rail, as the schema already says. The README and `docs/FIELDS.md` no longer say receivers ignore unknown `rail_ref` keys. `labels` and `evidence[].value` stay open.
- x402 mapping: `payment_id` is `x402:<network>:<nonce>` on every stage after the challenge, never the transaction hash. `payment.requested` uses `x402:<network>:requested:<event id>`, and the answering `payment.authorized` links back with `related.previous_event_id`.
- New `conformance/` folder: events with their expected verdicts, a signing vector and canonical-JSON vectors, checked in CI by `npm test`.

## 0.1.0

First public draft.

- Event envelope: `event` plus a detached EdDSA JWS (`sig`) over the RFC 8785 canonical form of the event.
- Event types: `payment.requested`, `payment.authorized`, `payment.settled`, `payment.failed`, `payment.refunded`, `payment.disputed`.
- Rails: `card`, `stripe`, `x402`, `mpp`, `stablecoin`, `bank_transfer`, each with its own allowed `rail_ref` keys.
- Attribution blocks for agent, owner and instruction (hash plus optional redacted summary).
- Amounts as decimal integer strings in minor units (with ISO 4217 currency) or atomic units (with a CAIP-2 asset).
- Evidence array carrying network proofs verbatim: AP2 mandates, Verifiable Intent chains, Visa TAP signatures, x402 payloads and settlements, MPP receipts, Stripe objects, agentic token metadata and KYA attestations.
- Mapping tables for x402 v2, Stripe, MPP, AP2, Mastercard Verifiable Intent, Visa TAP and Mastercard Agentic Tokens.
