# Changelog

All notable changes to the Agent Payment Event (APE) schema. Versions follow `MAJOR.MINOR`; minor versions only add optional fields. Until v1.0, a minor version may still make breaking changes, and the changelog will say so.

## 0.2.0

Adds optional fields and one event type. A `0.1` event is unchanged and stays valid; an event says `"ape_version": "0.2"` to use anything below. The JWS header `ape` matches the event's `ape_version`.

- **Unknown owner:** `owner.type` may be `unknown`, with an optional `owner.unknown_reason` (`not_visible_to_observer`, `not_provided`).
- **Attribution gaps:** `attribution_gaps` says which of owner, agent, instruction and mandate are missing, and why.
- **Observer:** `source.perspective` is `payer`, `payee`, `facilitator` or `network`, so payer-side and payee-side records of one payment can be joined.
- **Delivery:** `delivery` carries request and response hashes, response size, HTTP status and a short summary of what the payment bought.
- **Payment:**
  - `payment.payer_amount` and `payment.fees` say what the payer was debited when it differs from what the payee received.
  - `payment.checkout_digest` names the checkout the payment is for.
  - `payment.intermediary` names a marketplace or referrer and its reconciliation tag.
  - `rail_ref.submitter` (x402, stablecoin) is the address that submitted the transaction.
- **Instruction:** `instruction.normalised_hash` with `instruction.normalisation` (`ws-lower-v1`), so two runs of one task can be matched. `hash` is unchanged.
- **Payee:** `payee.receipt_key` is the key the payee signs receipts with (carried, not verified).
- **Evidence kinds:** `chain.receipt` (the on-chain receipt) and `tool.response` (what a tool showed the agent).
- **New event type** `agent.reported`: what the agent told its owner about an instruction. It has no payment; it has `instruction` and a `report` with the claimed payment count and amount, and a hash of the message.
- **Examples:** a payee-observed x402 payment with attribution gaps, a payer-side payment with fees and a tool response, and an agent report.

## Unreleased (v0.1 clarifications, included in 0.2.0)

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
