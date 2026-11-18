# Contributing to APE schema

The Agent Payment Event (APE) schema is meant to be shared, not owned by one company. Proposals from people who build agent payments, wallets and checkout are the most useful contributions we get.

## What we welcome

- **Rail mappings.** A new table in [`docs/MAPPINGS.md`](docs/MAPPINGS.md) for a rail or protocol APE doesn't cover yet, with one synthetic example event.
- **Examples** in [`examples/`](examples/) that an implementer can check independently.
- **Conformance cases** in [`conformance/events.json`](conformance/events.json): events every implementation must accept or reject.
- **Documentation fixes** where [`docs/FIELDS.md`](docs/FIELDS.md) or the mappings are unclear or wrong.

## Out of scope for now

- **Changes to `ape/v0.1.json` itself.** v0.1 is published, and receivers pick the schema by `ape_version`. A new field, `rail` value or `rail_ref` key goes into the next version. Open a proposal issue first; don't start with a PR.
- **Rules that need more than one event** (for example "one invoice is settled only once"). The conformance runner checks one event at a time today. Raise these as a proposal so we can decide where they belong.

## Set up and run the checks

Requirements: Node.js 22 or later and npm. No account or API key is needed.

```bash
git clone https://github.com/halvorAI/ape-schema.git
cd ape-schema
npm ci
npm test
```

`npm test` runs [`scripts/check-conformance.mjs`](scripts/check-conformance.mjs). It checks every conformance case, every file in `examples/` and the signing and JCS vectors against `ape/v0.1.json`, and should end with `All N conformance checks passed.` CI runs the same command on every pull request.

## Your first contribution

Look for issues labeled [`good first issue`](https://github.com/halvorAI/ape-schema/labels/good%20first%20issue) or [`help wanted`](https://github.com/halvorAI/ape-schema/labels/help%20wanted). For a new rail, open a **Rail mapping proposal** first so we can agree on the field choices before you write the table.

1. **Comment on the issue** to say you're taking it, so two people don't do the same work. For anything not covered by an issue, open one first and say what you plan to change.
2. **Fork the repository** and create a branch.
3. **Keep the pull request small**: one change, with its tests or examples.
4. **Run the checks above** before you push.
5. **Open the pull request** and fill in the template. Leave the "Brain update" section empty; a maintainer fills it in.

## Tests, fixtures and docs

- Use synthetic data only: made-up IDs, wallet addresses, invoice numbers and amounts. Never a real customer, card number, wallet you control or API key.
- Every new file in `examples/` must pass `npm test`.
- A new case in `conformance/events.json` needs a short `name`, an `expect` of `valid` or `invalid`, and for an invalid event a `rule` (`schema` or `pan`).
- If you change how a field is read, update `docs/FIELDS.md` or `docs/MAPPINGS.md` in the same pull request, and add a line to `CHANGELOG.md`.

## How we respond

The maintainers are [@hedge-waleed](https://github.com/hedge-waleed) (reviewer) and [@hedge-usama](https://github.com/hedge-usama) (backup reviewer). In business days, we aim to:

| What you open | First response |
| --- | --- |
| An issue | Acknowledged within 1 business day |
| An issue | Triaged within 2 business days: accepted, needs more information, needs design discussion, or out of scope |
| A pull request | A substantive first review within 3 business days |

We won't promise a merge date before a review and a green CI run. If we miss these times, a polite ping on the issue or pull request is welcome.

Questions are welcome as issues too. You don't need to email us or know anyone at HalvorAI to contribute.

## Security

Please don't report vulnerabilities in public issues. Email **hello@halvorai.com** with the details instead, and we'll reply privately. See [SECURITY.md](SECURITY.md).

## License

By contributing, you agree that your contribution is licensed under the Apache License 2.0, the same license as this repository.
