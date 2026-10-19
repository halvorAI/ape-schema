# Changelog

All notable changes to the Agent Payment Event (APE) schema. Versions follow `MAJOR.MINOR`; minor versions only add optional fields. Until v1.0, a minor version may still make breaking changes, and the changelog will say so.

## 0.1.0

First public draft.

- Event envelope: `event` plus a detached EdDSA JWS (`sig`) over the RFC 8785 canonical form of the event.
- Event types: `payment.requested`, `payment.authorized`, `payment.settled`, `payment.failed`, `payment.refunded`, `payment.disputed`.
- Rails: `card`, `stripe`, `x402`, `mpp`, `stablecoin`, `bank_transfer`, each with its own allowed `rail_ref` keys.
- Attribution blocks for agent, owner and instruction (hash plus optional redacted summary).
- Amounts as decimal integer strings in minor units (with ISO 4217 currency) or atomic units (with a CAIP-2 asset).
- Evidence array carrying network proofs verbatim: AP2 mandates, Verifiable Intent chains, Visa TAP signatures, x402 payloads and settlements, MPP receipts, Stripe objects, agentic token metadata and KYA attestations.
- Mapping tables for x402 v2, Stripe, MPP, AP2, Mastercard Verifiable Intent, Visa TAP and Mastercard Agentic Tokens.
