# Agent Payment Event (APE) v0.1

An open, rail-neutral record of one AI agent payment: which agent paid, for whom, on whose instruction, on which rail, and the network proofs that came with it.

- **Schema:** [`ape/v0.1.json`](ape/v0.1.json), JSON Schema 2020-12. Canonical URL: `https://schema.halvorai.com/ape/v0.1.json`.
- **Fields:** [`docs/FIELDS.md`](docs/FIELDS.md), generated from the schema.
- **Mappings** to AP2, Mastercard Verifiable Intent, Visa Trusted Agent Protocol, x402 v2, MPP and Stripe: [`docs/MAPPINGS.md`](docs/MAPPINGS.md).
- **Examples:** [`examples/`](examples/): x402 settled, Stripe Issuing authorization with AP2 and TAP evidence, Stripe failed payment.

## Design goals

1. Rail-neutral: one event shape for card, Stripe, x402, MPP, stablecoin and bank transfer payments.
2. Attributed: every event names the agent, the owner it acts for, and the instruction it acted on.
3. Evidence travels with the payment: network proofs are attached verbatim so any party can verify them later.
4. No spend limits of its own: mandate constraints come from the network credential.
5. Tamper-evident: producers sign each event; receivers chain them.
6. Privacy by default: instructions are a hash plus an optional redacted summary; card numbers never appear.

## Validate an event

```js
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import schema from './ape/v0.1.json' with { type: 'json' };

const ajv = new Ajv2020({ strict: false });
addFormats(ajv);
const validate = ajv.compile(schema);

if (!validate(event)) console.error(validate.errors);
```

JSON Schema cannot express every rule. Receivers should also reject free-text fields that contain a Luhn-valid 13 to 19 digit sequence (a possible card number).

## Signing

An envelope is `{ "event": { ... }, "sig": "<detached JWS>" }`. The JWS header is `{"alg":"EdDSA","kid":"<source id>","typ":"ape+jws","ape":"0.1"}` and the payload is the RFC 8785 (JCS) canonical form of `event`, detached per RFC 7515 Appendix F.

## Versioning

`ape_version` is `MAJOR.MINOR`. Minor versions only add optional fields. Receivers must ignore unknown keys in `labels`, `rail_ref` and `evidence[].value`, and reject unknown top-level fields. v0.x may change between minors until v1.0.

The `sha256` values in the examples are placeholders; real events carry the digest of their evidence value.

## Feedback

Open an issue, or write to hello@halvorai.com. Open questions for reviewers are in the issue tracker.

## License

Apache-2.0. See [`LICENSE`](LICENSE).
