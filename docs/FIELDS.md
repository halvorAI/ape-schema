# Fields

Generated from [`ape/v0.2.json`](../ape/v0.2.json). Every v0.1 event is valid v0.2 once it says `"ape_version": "0.2"`; v0.1 stays published at [`ape/v0.1.json`](../ape/v0.1.json).

## Payment event fields

| Field | Type | Required | Constraints |
|---|---|---|---|
| `ape_version` | const | yes | `"0.2"` |
| `id` | string | yes | length 8 to 128 |
| `occurred_at` | string | yes | format date-time |
| `environment` | enum | yes | `test`, `live` |
| `source` | object | yes | |
| `source.id` | string | yes | max length 64 |
| `source.sdk` | string | yes | max length 64 |
| `source.adapter` | enum | yes | `stripe`, `stripe-issuing`, `x402-client`, `x402-server`, `mpp-server`, `mcp`, `manual`, `custom` |
| `source.perspective` | enum | no | `payer`, `payee`, `facilitator`, `network` |
| `agent` | object | yes | |
| `agent.id` | string | yes | max length 128 |
| `agent.name` | string | no | max length 128 |
| `agent.framework` | string | no | max length 64 |
| `agent.version` | string | no | max length 64 |
| `agent.key_thumbprint` | string | no | max length 64 |
| `agent.kya` | object | no | |
| `agent.kya.provider` | string | yes | max length 64 |
| `agent.kya.subject` | string | yes | max length 256 |
| `agent.kya.assurance` | string | no | max length 64 |
| `agent.kya.verified_at` | string | no | format date-time |
| `owner` | object | yes | |
| `owner.id` | string | yes | max length 128 |
| `owner.type` | enum | yes | `person`, `business`, `unknown` |
| `owner.display_name` | string | no | max length 128 |
| `owner.country` | string | no | pattern `^[A-Z]{2}$` |
| `owner.kyc_ref` | string | no | max length 128 |
| `owner.unknown_reason` | enum | no | `not_visible_to_observer`, `not_provided` |
| `evidence` | array | no | at most 16 items |
| `evidence[].kind` | enum | yes | `ap2.payment_mandate`, `ap2.checkout_mandate`, `vi.chain`, `tap.signature`, `x402.payment_payload`, `x402.settlement`, `mpp.receipt`, `stripe.object`, `agentic_token.metadata`, `kya.attestation`, `chain.receipt`, `tool.response` |
| `evidence[].format` | enum | yes | `sd-jwt`, `kb-sd-jwt`, `jws`, `http-signature`, `json` |
| `evidence[].value` | string / object | no | |
| `evidence[].uri` | string | no | format uri |
| `evidence[].sha256` | string | yes | pattern `^sha256:[0-9a-f]{64}$` |
| `evidence[].captured_at` | string | no | format date-time |
| `related` | object | no | |
| `related.previous_event_id` | string | no | max length 128 |
| `related.corrects_event_id` | string | no | max length 128 |
| `related.session_id` | string | no | max length 128 |
| `labels` | object | no | at most 20 properties |
| `type` | enum | yes | `payment.requested`, `payment.authorized`, `payment.settled`, `payment.failed`, `payment.refunded`, `payment.disputed` |
| `instruction` | object | no | |
| `instruction.id` | string | yes | max length 128 |
| `instruction.hash` | string | yes | pattern `^sha256:[0-9a-f]{64}$` |
| `instruction.summary` | string | no | max length 500 |
| `instruction.channel` | enum | no | `chat`, `api`, `schedule`, `email`, `agent`, `other` |
| `instruction.issued_at` | string | no | format date-time |
| `instruction.tool_call_id` | string | no | max length 128 |
| `instruction.normalised_hash` | string | no | pattern `^sha256:[0-9a-f]{64}$` |
| `instruction.normalisation` | enum | no | `ws-lower-v1` |
| `payment` | object | yes | |
| `payment.payment_id` | string | yes | max length 256 |
| `payment.rail` | enum | yes | `stripe`, `card`, `x402`, `mpp`, `stablecoin`, `bank_transfer` |
| `payment.amount` | object | yes | |
| `payment.amount.value` | string | yes | pattern `^(0\|[1-9][0-9]*)$` |
| `payment.amount.unit` | enum | yes | `minor`, `atomic` |
| `payment.amount.currency` | string | no | pattern `^[A-Z]{3}$` |
| `payment.amount.asset` | object | no | |
| `payment.amount.asset.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `payment.amount.asset.address` | string | yes | max length 128 |
| `payment.amount.asset.symbol` | string | no | max length 16 |
| `payment.amount.asset.decimals` | integer | no | from 0 to 36 |
| `payment.status` | enum | yes | `requested`, `authorized`, `settled`, `failed`, `refunded`, `disputed` |
| `payment.failure_reason` | string | no | max length 128 |
| `payment.description` | string | no | max length 256 |
| `payment.category` | string | no | max length 64 |
| `payment.rail_ref` | object | yes | |
| `payment.payer_amount` | object | no | |
| `payment.payer_amount.value` | string | yes | pattern `^(0\|[1-9][0-9]*)$` |
| `payment.payer_amount.unit` | enum | yes | `minor`, `atomic` |
| `payment.payer_amount.currency` | string | no | pattern `^[A-Z]{3}$` |
| `payment.payer_amount.asset` | object | no | |
| `payment.payer_amount.asset.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `payment.payer_amount.asset.address` | string | yes | max length 128 |
| `payment.payer_amount.asset.symbol` | string | no | max length 16 |
| `payment.payer_amount.asset.decimals` | integer | no | from 0 to 36 |
| `payment.fees` | array | no | at most 8 items |
| `payment.fees[].kind` | enum | yes | `bridge`, `network`, `slippage`, `platform`, `fx`, `other` |
| `payment.fees[].amount` | object | yes | |
| `payment.fees[].amount.value` | string | yes | pattern `^(0\|[1-9][0-9]*)$` |
| `payment.fees[].amount.unit` | enum | yes | `minor`, `atomic` |
| `payment.fees[].amount.currency` | string | no | pattern `^[A-Z]{3}$` |
| `payment.fees[].amount.asset` | object | no | |
| `payment.fees[].amount.asset.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `payment.fees[].amount.asset.address` | string | yes | max length 128 |
| `payment.fees[].amount.asset.symbol` | string | no | max length 16 |
| `payment.fees[].amount.asset.decimals` | integer | no | from 0 to 36 |
| `payment.checkout_digest` | string | no | pattern `^[A-Za-z0-9_-]{43}$` |
| `payment.intermediary` | object | no | |
| `payment.intermediary.name` | string | no | max length 128 |
| `payment.intermediary.id` | string | no | max length 128 |
| `payment.intermediary.ref_tag` | string | no | max length 128 |
| `payee` | object | yes | |
| `payee.type` | enum | yes | `merchant`, `api_provider`, `wallet`, `business`, `person` |
| `payee.name` | string | no | max length 256 |
| `payee.id` | string | no | max length 128 |
| `payee.website` | string | no | format uri |
| `payee.country` | string | no | pattern `^[A-Z]{2}$` |
| `payee.mcc` | string | no | pattern `^[0-9]{4}$` |
| `payee.wallet` | object | no | |
| `payee.wallet.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `payee.wallet.address` | string | yes | max length 128 |
| `payee.resource_url` | string | no | format uri |
| `payee.receipt_key` | object | no | |
| `payee.receipt_key.kid` | string | no | max length 128 |
| `payee.receipt_key.jwk` | object | no | |
| `payee.receipt_key.jwks_uri` | string | no | format uri |
| `instrument` | object | no | |
| `instrument.type` | enum | yes | `card`, `agentic_token`, `stripe_spt`, `wallet`, `bank_account` |
| `instrument.network` | string | no | max length 32 |
| `instrument.last4` | string | no | pattern `^[0-9]{4}$` |
| `instrument.par` | string | no | max length 64 |
| `instrument.token_ref` | string | no | max length 128 |
| `instrument.wallet` | object | no | |
| `instrument.wallet.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `instrument.wallet.address` | string | yes | max length 128 |
| `instrument.issuer` | string | no | max length 128 |
| `attribution_gaps` | array | no | at most 4 items |
| `attribution_gaps[].field` | enum | yes | `owner`, `agent`, `instruction`, `mandate` |
| `attribution_gaps[].reason` | enum | yes | `not_visible_to_observer`, `not_provided` |
| `delivery` | object | no | |
| `delivery.request_sha256` | string | no | pattern `^sha256:[0-9a-f]{64}$` |
| `delivery.response_sha256` | string | no | pattern `^sha256:[0-9a-f]{64}$` |
| `delivery.response_bytes` | integer | no | |
| `delivery.http_status` | integer | no | from 100 to 599 |
| `delivery.summary` | string | no | max length 256 |

## `agent.reported` event fields

| Field | Type | Required | Constraints |
|---|---|---|---|
| `ape_version` | const | yes | `"0.2"` |
| `id` | string | yes | length 8 to 128 |
| `occurred_at` | string | yes | format date-time |
| `environment` | enum | yes | `test`, `live` |
| `source` | object | yes | |
| `source.id` | string | yes | max length 64 |
| `source.sdk` | string | yes | max length 64 |
| `source.adapter` | enum | yes | `stripe`, `stripe-issuing`, `x402-client`, `x402-server`, `mpp-server`, `mcp`, `manual`, `custom` |
| `source.perspective` | enum | no | `payer`, `payee`, `facilitator`, `network` |
| `agent` | object | yes | |
| `agent.id` | string | yes | max length 128 |
| `agent.name` | string | no | max length 128 |
| `agent.framework` | string | no | max length 64 |
| `agent.version` | string | no | max length 64 |
| `agent.key_thumbprint` | string | no | max length 64 |
| `agent.kya` | object | no | |
| `agent.kya.provider` | string | yes | max length 64 |
| `agent.kya.subject` | string | yes | max length 256 |
| `agent.kya.assurance` | string | no | max length 64 |
| `agent.kya.verified_at` | string | no | format date-time |
| `owner` | object | yes | |
| `owner.id` | string | yes | max length 128 |
| `owner.type` | enum | yes | `person`, `business`, `unknown` |
| `owner.display_name` | string | no | max length 128 |
| `owner.country` | string | no | pattern `^[A-Z]{2}$` |
| `owner.kyc_ref` | string | no | max length 128 |
| `owner.unknown_reason` | enum | no | `not_visible_to_observer`, `not_provided` |
| `evidence` | array | no | at most 16 items |
| `evidence[].kind` | enum | yes | `ap2.payment_mandate`, `ap2.checkout_mandate`, `vi.chain`, `tap.signature`, `x402.payment_payload`, `x402.settlement`, `mpp.receipt`, `stripe.object`, `agentic_token.metadata`, `kya.attestation`, `chain.receipt`, `tool.response` |
| `evidence[].format` | enum | yes | `sd-jwt`, `kb-sd-jwt`, `jws`, `http-signature`, `json` |
| `evidence[].value` | string / object | no | |
| `evidence[].uri` | string | no | format uri |
| `evidence[].sha256` | string | yes | pattern `^sha256:[0-9a-f]{64}$` |
| `evidence[].captured_at` | string | no | format date-time |
| `related` | object | no | |
| `related.previous_event_id` | string | no | max length 128 |
| `related.corrects_event_id` | string | no | max length 128 |
| `related.session_id` | string | no | max length 128 |
| `labels` | object | no | at most 20 properties |
| `type` | const | yes | `"agent.reported"` |
| `instruction` | object | yes | |
| `instruction.id` | string | yes | max length 128 |
| `instruction.hash` | string | yes | pattern `^sha256:[0-9a-f]{64}$` |
| `instruction.summary` | string | no | max length 500 |
| `instruction.channel` | enum | no | `chat`, `api`, `schedule`, `email`, `agent`, `other` |
| `instruction.issued_at` | string | no | format date-time |
| `instruction.tool_call_id` | string | no | max length 128 |
| `instruction.normalised_hash` | string | no | pattern `^sha256:[0-9a-f]{64}$` |
| `instruction.normalisation` | enum | no | `ws-lower-v1` |
| `attribution_gaps` | array | no | at most 4 items |
| `attribution_gaps[].field` | enum | yes | `owner`, `agent`, `instruction`, `mandate` |
| `attribution_gaps[].reason` | enum | yes | `not_visible_to_observer`, `not_provided` |
| `report` | object | yes | |
| `report.channel` | enum | no | `chat`, `api`, `email`, `other` |
| `report.summary` | string | no | max length 500 |
| `report.payments_claimed` | integer | no | |
| `report.amount_claimed` | object | no | |
| `report.amount_claimed.value` | string | yes | pattern `^(0\|[1-9][0-9]*)$` |
| `report.amount_claimed.unit` | enum | yes | `minor`, `atomic` |
| `report.amount_claimed.currency` | string | no | pattern `^[A-Z]{3}$` |
| `report.amount_claimed.asset` | object | no | |
| `report.amount_claimed.asset.network` | string | yes | pattern `^[-a-z0-9]{3,8}:[-_a-zA-Z0-9]{1,32}$`; CAIP-2 chain id |
| `report.amount_claimed.asset.address` | string | yes | max length 128 |
| `report.amount_claimed.asset.symbol` | string | no | max length 16 |
| `report.amount_claimed.asset.decimals` | integer | no | from 0 to 36 |
| `report.body_sha256` | string | yes | pattern `^sha256:[0-9a-f]{64}$` |

## `rail_ref` keys by rail

| Rail | Allowed `rail_ref` keys |
|---|---|
| `stripe` | `account`, `payment_intent`, `charge`, `refund`, `dispute`, `shared_payment_token` |
| `card` | `authorization_id`, `transaction_id`, `network_transaction_id`, `processor` |
| `x402` | `scheme`, `network`, `nonce`, `tx_hash`, `facilitator`, `payment_flow`, `submitter` |
| `mpp` | `method`, `challenge_id`, `payment_intent`, `tx_hash` |
| `stablecoin` | `network`, `tx_hash`, `log_index`, `submitter` |
| `bank_transfer` | `scheme`, `end_to_end_id`, `pisp` |

## Cross-field rules

- If `payment.amount.unit` is `minor`, `currency` (ISO 4217) is required. If it is `atomic`, `asset` is required.
- If `payment.status` is `failed`, `payment.failure_reason` is required.
- `payee` needs at least one of `name`, `wallet` or `id`.
- Each `evidence[]` item has exactly one of `value` or `uri`.
- `payment.rail_ref` accepts only the keys listed for the event's rail. An unknown `rail_ref` key is rejected, like an unknown top-level field. A new key arrives with a new `ape_version`, and receivers pick the schema by that version.
- `labels` and `evidence[].value` are open: any keys are allowed, and receivers ignore the ones they do not use.
- Free-text fields must not contain a possible card number: a run of 13 to 19 digits, with single spaces or dashes allowed between digits, that passes the Luhn check. Producers redact such runs before signing (as `[redacted:pan]`); receivers reject an event that still has one, with `pan_detected`. JSON Schema cannot express this check. The free-text fields are exactly:
  - `payment.description`, `payment.category`, `payment.failure_reason`
  - `instruction.summary`
  - `agent.name`, `owner.display_name`
  - `payee.name`, `payee.website`, `payee.resource_url`
  - every key and every value of `labels`
  - v0.2: `delivery.summary` and `report.summary`

  Identifiers are not free text and are never checked or redacted: ids, `payment.payment_id`, every `rail_ref` value, `instrument.*` and `related.*`. Card networks issue numeric transaction ids that pass the Luhn check about one time in ten, so checking them would corrupt or reject real events. `evidence[].value` is not checked either: it is a third party's proof, carried verbatim, and changing it would break its signature.

### v0.2 rules

- A `0.1` event may not use any v0.2 field; set `"ape_version": "0.2"` to use one. The JWS header `ape` equals the event's `ape_version`.
- `owner.unknown_reason` only with `owner.type: "unknown"`.
- `instruction.normalised_hash` and `instruction.normalisation` go together. `ws-lower-v1`: Unicode NFC, lowercase, each URL's scheme, host and port removed (path kept), runs of whitespace collapsed to one space, trimmed. `instruction.hash` stays over the exact text.
- Each `attribution_gaps` field appears at most once. JSON Schema cannot express this check.
- An `agent.reported` event has no `payment`, `payee`, `instrument` or `delivery`, and requires `instruction` and `report`. It is not a payment.
- `tool.response` and `chain.receipt` evidence are captured by the producer, so receivers keep and hash them but report them as unverifiable, never invalid.
