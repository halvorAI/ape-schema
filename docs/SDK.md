# SDK behaviour

What every HalvorAI ingest SDK does, so that the same input gives the same events, the same signatures and the same delivery outcome in every language. The Node.js, Python and Go SDKs follow it; a new SDK must too.

The event format itself is in [`ape/v0.1.json`](../ape/v0.1.json) and [`FIELDS.md`](FIELDS.md). The x402, Stripe and other rail mappings are in [`MAPPINGS.md`](MAPPINGS.md).

## 1. Never in the payment path

- `emit` returns the event id at once. It never throws, never blocks on the network or the disk, and never changes the caller's objects.
- Configuration mistakes never throw either. A missing or malformed source key or API key disables the client: it reports one `config` error and counts every later event as `dropped_disabled`.
- Adapters only read payment headers and webhook bodies. Requests and responses pass through unchanged, and a mapping error is reported as `invalid_event`, never raised to the caller.

## 2. Building an event

In this order:

1. **Id.** The input's `id` if it is a string, else `evt_` and a ULID.
2. **Fill.** `ape_version` `"0.1"`; `occurred_at` now (RFC 3339 UTC with milliseconds) when missing; `environment` the client's when missing (`live` for an `hk_live_` key, else `test`).
3. **Source.** `{ id: <source key kid>, sdk: <package>@<version>, adapter }`. The input may set `adapter` only (default `custom`).
4. **Attribution.** `agent`, `owner` and `instruction` from the event, else from the agent context, else `agent: { id: "unattributed" }` and `owner: { id: "unattributed", type: "business" }`. Nested contexts keep the outer value of any field the inner one leaves out.
5. **Instruction.** An event-level instruction replaces the context one. `text` is hashed locally (`sha256:` + hex of its UTF-8 bytes) and never sent. Only `id`, `hash`, `summary`, `channel`, `issued_at` and `tool_call_id` are kept; without an `id` or a hash the instruction is left out.
6. **Optional fields.** `instrument`, `evidence`, `related` and `labels` are copied when present and not null.
7. **Redaction** (section 3).
8. **Validation** against the schema and the card-number rule. An invalid event is dropped, counted as `dropped_invalid` and reported as `invalid_event` with the problems found. Null is never allowed: an optional field is left out.

## 3. Redaction

Before signing, these are removed from free text:

| Pattern | Replaced with |
|---|---|
| Card number: a Luhn-valid run of 13 to 19 digits, single spaces or dashes allowed between digits | `[redacted:pan]` |
| CVC after `cvc`, `cvv`, `cvv2` or `security code` (any case) | `[redacted:cvc]` |
| `sk_live_`, `sk_test_`, `rk_live_`, `whsec_`, `hk_live_`, `hk_test_` keys | `[redacted:secret-key]` |
| PEM private keys, and the `d` of a JWK | `[redacted:private-key]` |

Fields redacted: `payment.description`, `payment.category`, `payment.failure_reason`, `agent.name`, `owner.display_name`, `payee.name`, `payee.website`, `payee.resource_url`, `instruction.summary`, every label key and value, and every string inside `evidence[].value` when `format` is `json`. After redacting JSON evidence, its `sha256` is recomputed.

## 4. Signing

- Canonical form: RFC 8785 (JCS), as JavaScript writes it: ECMAScript number formatting, object keys sorted by UTF-16 code units, strings escaped like `JSON.stringify` (a lone surrogate becomes a lowercase `\udXXX` escape).
- Signature: Ed25519 over `<header>.<base64url(JCS bytes)>`. The protected header is exactly `{"alg":"EdDSA","kid":<event.source.id>,"typ":"ape+jws","ape":"0.1"}`. The SDK sends the detached form `<header>..<signature>`.
- An SDK must reproduce [`conformance/sign-vector.json`](../conformance/) byte for byte, and pass every case in [`conformance/events.json`](../conformance/events.json) and [`conformance/jcs-vectors.json`](../conformance/jcs-vectors.json) in its CI.

## 5. Delivery

- **Batching.** A background worker sends at most 100 events per request, every flush interval (default 1 second), or at once when a batch is full or `flush` is called.
- **Request.** `POST <endpoint>/v1/events` with `Authorization: Bearer <API key>` and `{"events":[{"event":…,"sig":…}]}`. The default endpoint is `https://api.halvorai.com` for `hk_live_` keys and `https://api.sandbox.halvorai.com` otherwise; `HALVOR_ENDPOINT` overrides it, and an endpoint ending in `/v1/events` is used as is.
- **Outcomes by status:**

| Status | Outcome |
|---|---|
| 2xx | Each event is counted by its result: `accepted`, `duplicate` or `rejected`. A rejected event is reported with the API's `serverCode`. An event with no result counts as accepted. |
| Network error, 408, 425, 429, 5xx, other non-2xx | Retried after 1, 2, 4, 8, 16 and 32 seconds, each with up to 20 % jitter. Then spooled, or dropped and reported as `delivery_failed` without a spool. |
| 400, 401, 403, 404, 405, 409, 410, 415, 422 | Not retried. The batch is counted as dropped once, written to `dead/`, and reported as `unauthorized` (401, 403) or `delivery_failed`, with the API's `serverCode`, `details` and `requestId`. |
| 413 (the API takes up to 1 MB per request) | The batch is split in two and each half sent again. A single event that is too large is dropped and reported with `serverCode: payload_too_large`. |

- **Errors** read from the body `{"error":{"code","message","details","request_id"}}`, with the `request-id` header as a fallback for the request id.

## 6. Spool

- One JSON Lines file per batch, one `{"event":…,"sig":…}` envelope per line, named `halvor-spool-<15-digit epoch ms>-<8 hex>.jsonl` so that name order is age order. Files are written atomically (temporary file, then rename). The format is shared: a file written by one SDK can be replayed by another.
- Batches the API will never accept go to `<spool>/dead/` and are never replayed.
- Limits per folder: 50 MB and 7 days by default. The oldest files are evicted first; evicted events count as dropped and are reported as `spool`.
- Replay runs on start (when files are waiting) and on every `flush`, oldest file first, one file at a time. A file that is rejected for good is dead-lettered and replay continues. A file that is partly delivered keeps only its undelivered envelopes. When the API is still down, replay stops and waits for the last retry delay before trying again.

## 7. Counters and errors

Every emitted event ends up in exactly one of `accepted`, `duplicates`, `rejected`, `dropped`, `dropped_invalid`, `dropped_disabled` or `dropped_closed`, or is still queued or spooled. Also counted: `emitted`, `queued`, `retries`, `spooled` and `replayed`. Reading the counters returns a copy.

Error codes passed to the error callback: `config`, `invalid_event`, `rejected`, `unauthorized`, `delivery_failed`, `spool`. A report carries the code, a message and, when known, `serverCode`, `requestId`, `eventId` and `details`. A failing callback is ignored.

## 8. Shutdown

`close` refuses new events (counted as `dropped_closed`), sends what is queued and stops the worker; the spool stays on disk for the next process. `flush` takes a timeout and reports whether everything was handled. Where the language has an exit hook, the SDK flushes for up to 2 seconds at normal exit; where it does not (Go), the README says to close the client.
