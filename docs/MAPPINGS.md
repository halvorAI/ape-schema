# Mappings

How receivers read AP2 and Verifiable Intent credentials, and how each source maps onto APE fields.

## 4. Normalised mandate (receiver side)

APE does not define a mandate format of its own. Receivers parse AP2 / VI credentials from `evidence[]` into one internal constraint vocabulary so the same evaluation runs whatever the source. HalvorAI stores this in `mandates`.

| Normalised constraint | AP2 constraint `type` | Verifiable Intent constraint `type` | Evaluated against |
|---|---|---|---|
| `amount_range {min,max,currency}` | `payment.amount_range` | `mandate.payment.amount_range` | `payment.amount` |
| `budget {max,currency}` | `payment.budget` | `mandate.payment.budget` | sum of settled payments under this mandate |
| `recurrence {frequency,max_occurrences}` | `payment.agent_recurrence` | `mandate.payment.agent_recurrence` (agent-managed) or `mandate.payment.recurrence` (merchant-managed) | count and spacing of payments |
| `reference` (checkout ↔ payment binding) | `payment.reference` | `mandate.payment.reference` | v0.2 `payment.checkout_digest` against the constraint's `transaction_id`, `checkout_hash` or `checkout_digest`; not evaluable without a digest. Verifiable Intent's `conditional_transaction_id` hashes the L2 checkout disclosure, not the checkout, so it is checked in the chain instead (L3a `transaction_id` equals the event's digest) |
| `allowed_payees [ {id,name,website} ]` | `payment.allowed_payees` | `mandate.payment.allowed_payees` | `payee.id` / `payee.website` |
| `allowed_merchants [ … ]` | `checkout.allowed_merchants` (open checkout mandate) | `mandate.checkout.allowed_merchants` | `payee` |
| `allowed_instruments [ {id,type} ]` | `payment.allowed_payment_instruments` | — | `instrument` |
| `allowed_pisps [ … ]` | `payment.allowed_pisps` | — | `rail_ref.pisp` |
| `execution_window {not_before,not_after}` | `payment.execution_date` | — | `occurred_at` |
| `line_items [ … ]` | `checkout.line_items` | `mandate.checkout.line_items` | evidence checkout JWT, informational only |
| `agent_key` (JWK thumbprint) | `cnf.jwk` on open mandates | `cnf.jwk` in L2 mandates | `agent.key_thumbprint` |

AP2 and Verifiable Intent share the `vct` values `mandate.checkout.1`, `mandate.checkout.open.1`, `mandate.payment.1` and `mandate.payment.open.1`. Constraint `type` names differ only by prefix (AP2 `payment.budget`, VI `mandate.payment.budget`). All names in this table were checked against the AP2 JSON Schemas (`code/sdk/schemas/ap2/open_*_mandate.json`) and VI `spec/constraints.md` §4 on 17 Oct 2026. VI is a v0.1 draft, so the parser must accept both prefixes and log unknown types rather than reject them.

**Units of money constraints.** The normaliser turns every money constraint into integer minor units of its currency, so evaluation never sees a fraction:

| Source | `amount_range` min / max | `budget.max` |
|---|---|---|
| AP2 | minor units, as given | **major units**, × 10^exponent of the currency, rounded to the nearest minor unit (0.29 USD is 29 cents, not 28) |
| Verifiable Intent | minor units, as given | minor units, as given |

This follows the AP2 SDK (0.1.1), which compares `int(max * 100)` for the budget and the raw value for `amount_range`. A value that is not a number, is negative, is fractional where minor units are expected, or has an unknown currency is kept with an `error` and evaluates as `not_evaluable` with that error as the detail; it never fails the job. The budget running total is kept in USD minor units, so a budget in another currency is `not_evaluable` (detail `currency`) until FX on mandates is built.

**List key.** `allowed_payees` and `allowed_merchants` read their list from `allowed` (AP2 SDK 0.1.1, `verifiable-intent` 0.1.0), then fall back to `payees` / `merchants`, then `value`.

## 5. Field mappings by source

Notation: `src.path → ape.path`. "verbatim" means the whole object also goes into `evidence[]`.

### 5.1 x402 v2 (confirmed against the x402 v2 specification)

| x402 | APE |
|---|---|
| `PaymentRequired` received by client | event `payment.requested` |
| `PaymentRequired.resource.url` | `payee.resource_url` |
| `PaymentRequired.resource.serviceName` | `payee.name` (fallback: URL host) |
| `PaymentRequirements.scheme` (`exact`, `upto`, `batch-settlement`, `auth-capture`) | `payment.rail_ref.scheme` |
| `PaymentRequirements.network` (CAIP-2) | `payment.rail_ref.network`, `payment.amount.asset.network`, `payee.wallet.network` |
| `PaymentRequirements.asset` | `payment.amount.asset.address` (or `currency` when an ISO 4217 code) |
| `PaymentRequirements.amount` (atomic) | `payment.amount.value`, `unit: atomic` |
| `PaymentRequirements.payTo` | `payee.wallet.address`, `payee.type: wallet` (or `api_provider` when resource set) |
| `PaymentRequirements.extra.paymentFlow` | `payment.rail_ref.payment_flow` |
| `PaymentPayload` sent | event `payment.authorized`; verbatim as `x402.payment_payload` |
| `PaymentPayload.payload.authorization.from` | `instrument.wallet.address`, `instrument.type: wallet` |
| `PaymentPayload.payload.authorization.nonce` | `payment.rail_ref.nonce` |
| `SettlementResponse.success = true` | event `payment.settled`; verbatim as `x402.settlement` |
| `SettlementResponse.transaction` | `payment.rail_ref.tx_hash` |
| `SettlementResponse.amount` | overrides `payment.amount.value` (actual amount for `upto`) |
| `SettlementResponse.errorReason` | event `payment.failed`, `payment.failure_reason` |
| `payment_id` on `payment.authorized`, `payment.settled`, `payment.failed` | `x402:<network>:<nonce>`, the same on every stage so the events of one payment join. A seller that saw only the settlement has no nonce: then it is `x402:<network>:tx:<transaction hash>`, else `x402:<network>:event:<event id>`, never a shared constant. A `tx:` id cannot join a payer-side record that carries the nonce. |
| `payment_id` on `payment.requested` | `x402:<network>:requested:<event id>`. No nonce exists before the client signs, and a fixed `x402:<network>:requested` would give every challenge on a network the same id. The `payment.authorized` event that answers the challenge sets `related.previous_event_id` to the requested event's `id`. |

### 5.2 Stripe (PaymentIntents and Issuing)

| Stripe | APE |
|---|---|
| `payment_intent.amount_capturable_updated` | `payment.authorized` |
| `payment_intent.succeeded` | `payment.settled` |
| `payment_intent.payment_failed` | `payment.failed`, `failure_reason = last_payment_error.code` |
| `charge.refunded` | `payment.refunded` |
| `charge.dispute.created` | `payment.disputed` |
| `PaymentIntent.id` | `payment.payment_id`, `rail_ref.payment_intent` |
| `amount`, `currency` | `payment.amount` (`unit: minor`, currency upper-cased) |
| `metadata.halvor_agent_id`, `metadata.halvor_owner_id`, `metadata.halvor_instruction_id` | `agent.id`, `owner.id`, `instruction.id` (the SDK's `tagPaymentIntent()` helper writes these at creation) |
| `description` | `payment.description` |
| Connect `transfer_data.destination` or `on_behalf_of` | `payee.id` |
| Shared Payment Token used to confirm | `instrument.type: stripe_spt`, `rail_ref.shared_payment_token` |
| `issuing_authorization.created` | `payment.authorized`, `rail: card`, `rail_ref.processor: stripe-issuing` |
| `issuing_transaction.created` | `payment.settled` (or `refunded` when `type = refund`) |
| `issuing.authorization.merchant_data.{name, category_code, country, network_id}` | `payee.name`, `payee.mcc`, `payee.country`, `payee.id` |
| `issuing.card.metadata.halvor_agent_id` | `agent.id` (one card per agent is the recommended setup) |

Stripe Issuing matters: many agent-card startups issue on Stripe, so this adapter covers the `card` rail in the MVP without a separate processor integration.

### 5.3 MPP (Machine Payments Protocol via `mppx`)

MPP returns HTTP 402 with a challenge; the agent retries with a credential; the server records a Stripe PaymentIntent (SPT card payments) or receives stablecoins on Tempo. The `mpp-server` adapter wraps `mppx.charge()`. Field names confirmed against `mppx@0.7` (`Challenge`, `Receipt` types):

| MPP | APE |
|---|---|
| 402 + `WWW-Authenticate: Payment …` challenge | event `payment.requested` |
| `Challenge.id` | `payment.rail_ref.challenge_id` |
| `Challenge.method` (`tempo`, `stripe`, …) | `payment.rail_ref.method` (`stripe` stored as `spt`) |
| `Challenge.intent` | labels `mpp_intent` when present |
| `Challenge.request.amount` | `payment.amount.value` |
| `Challenge.request.currency` (token address) | `payment.amount.asset.address` when `method = tempo` (`unit: atomic`) |
| `Challenge.request.recipient` | `payee.wallet.address` |
| `Challenge.description` / `realm` | `payment.description` / payee name fallback |
| successful charge + `Payment-Receipt` header | event `payment.settled`; receipt verbatim as `mpp.receipt` |
| `Receipt.method` | `rail_ref.method` (same mapping) |
| `Receipt.reference` for `tempo` | `rail_ref.tx_hash` |
| `Receipt.reference` for `stripe` / `stripe/charge` | `rail_ref.payment_intent` |
| `Receipt.timestamp` | informs `occurred_at` when no better clock |
| `payment_id` | `mpp:<method>:<challenge.id\|receipt.reference>` |

### 5.4 AP2 mandates (confirmed against `code/sdk/schemas/ap2/*.json` in google-agentic-commerce/AP2)

| AP2 claim | APE use |
|---|---|
| Closed Payment Mandate `vct = mandate.payment.1`: `transaction_id` | `related` binding: must equal the rail payment id or the checkout hash the SDK records |
| `payee {id, name, website}` | compared with `payee`; mismatch is a finding |
| `payment_amount {amount (minor units, integer), currency}` | compared with `payment.amount` |
| `payment_instrument {id, type, description}` | compared with `instrument` |
| `pisp`, `execution_date`, `risk_data`, `iat`, `exp` | stored on the normalised mandate |
| Open Payment Mandate `mandate.payment.open.1`: `constraints[]`, `cnf` | normalised constraints (§4); `cnf.jwk` thumbprint compared with `agent.key_thumbprint` |
| Checkout Mandate `mandate.checkout.1`: `checkout_jwt`, `checkout_hash` | `payment.description` from the checkout; hash binding to the payment mandate |

### 5.5 Mastercard Verifiable Intent (draft v0.1, agent-intent/verifiable-intent)

| VI layer | APE use |
|---|---|
| L1 SD-JWT from credential provider: `iss`, `sub`, `vct = https://credentials.mastercard.com/card`, `pan_last_four`, `scheme`, `card_id`, `cnf.jwk` (user device key) | `instrument.last4`, `instrument.network`, `owner` binding (via `sub` hash, not raw) |
| L2 KB-SD-JWT signed by user device key; Immediate (final values, ~15 min) or Autonomous (constraints + `cnf.jwk` agent key, 24 h to 30 days) | normalised mandate; `mode` stored; agent key thumbprint compared |
| L3a (payment, to network): `transaction_id`, `payment_instrument`, final values; L3b (checkout, to merchant): `checkout_jwt`, `checkout_hash` | per-payment binding; L3a `transaction_id` must equal L3b `checkout_hash` |

A `vi.chain` evidence value is the layers tilde-joined in order (L1, L2, then L3a and L3b when present), each a compact JWT followed by its own disclosures and a trailing `~`, so each layer's serialization is exactly what the next layer's `sd_hash` covers. Checked against `agent-intent/verifiable-intent` `spec/credential-format.md` on 25 Nov 2026. VI money constraints are integer minor units (§4).

### 5.6 Visa Trusted Agent Protocol (RFC 9421)

Confirmed against Visa Merchant Specifications (Trusted Agent Protocol) and `visa/trusted-agent-protocol` `cdn-proxy/server.js` on 18 Oct 2026.

| TAP | APE use |
|---|---|
| `Signature-Input` params: covered components (`"@authority" "@path"`), `created`, `expires`, `keyId` / `keyid`, `alg`, `nonce`, `tag` | stored verbatim in `tap.signature`; `tag` is `agent-browser-auth` (browsing) or `agent-payer-auth` (checkout) |
| `keyId` | `agent.kya = { provider: "visa-tap", subject: keyId }` |
| Maximum signature window | `expires - created` ≤ **8 minutes** (Visa); HalvorAI also requires `created` ≤ `occurred_at` ≤ `expires`. Nonce replay store retains 24 h per `specs/06-monitoring.md` (Visa live merchants keep 8 min). |
| Key directory | Visa JWKS: `https://mcp.visa.com/.well-known/jwks` (also `GET /keys?keyID=`). Configured in `packages/verify/src/anchors.ts` as `TAP_KEY_DIRECTORY_URL`. |
| `Agentic Consumer Recognition Object` (`agenticConsumer`): `nonce` (must match message signature), `idToken` (JWT / JWS), `contextualData` (device and location identifiers), `kid`, `alg`, `signature` | `owner.kyc_ref` from `idToken` subject when present; loyalty / other consented identifiers in `contextualData` map to `owner.kyc_ref` or labels; device identifiers stay in evidence |
| Payment container (signed payment credentials in the request body; content varies by channel) | `instrument.par` / network token fields when present; otherwise verbatim in evidence |

Open: exact `contextualData` and payment-container field names for Visa Intelligent Commerce beyond the object envelope above are still thin in the public pages; parsers accept additional members without rejecting.

### 5.7 Mastercard Agentic Tokens (partial)

There is no public field-level spec. Agentic Token data reaches a startup through its issuer processor. v0.1 accepts `instrument.type = agentic_token`, `instrument.token_ref`, and the processor's metadata verbatim as `agentic_token.metadata`. When a design partner shares processor field docs, we add a mapping here in v0.2. If the transaction also carries a Verifiable Intent chain, §5.5 applies.

## APE v0.2: who observed the payment

A seller-side (payee-observed) x402 or MPP record sees a wallet, not the agent, its owner, the instruction or a mandate. In v0.2 it says so instead of carrying placeholders: `source.perspective: "payee"`, `owner: { "id": "unattributed", "type": "unknown", "unknown_reason": "not_visible_to_observer" }`, and `attribution_gaps` listing `agent`, `owner`, `instruction` and `mandate`. The payer wallet stays in `instrument.wallet` and is never the agent id. A payer-side record sets `perspective: "payer"`; the two join on `payment_id`.
