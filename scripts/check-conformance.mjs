// Checks the conformance cases, the examples and the test vectors against ape/v0.1.json and
// the card-number rule in docs/FIELDS.md. Run with `npm test`.
import { readFileSync, readdirSync } from 'node:fs';
import Ajv2020 from 'ajv/dist/2020.js';
import addFormats from 'ajv-formats';
import { compactVerify, importJWK } from 'jose';

const read = (path) => JSON.parse(readFileSync(new URL(`../${path}`, import.meta.url), 'utf8'));

const ajv = new Ajv2020({ strict: false, allErrors: true });
addFormats(ajv);
const validate = ajv.compile(read('ape/v0.1.json'));

// The free-text fields, exactly as docs/FIELDS.md lists them.
function freeText(event) {
  const at = (a, b) => (typeof event[a]?.[b] === 'string' ? [[`${a}.${b}`, event[a][b]]] : []);
  const labels = event.labels && typeof event.labels === 'object' ? event.labels : {};
  return [
    ...at('payment', 'description'),
    ...at('payment', 'category'),
    ...at('payment', 'failure_reason'),
    ...at('instruction', 'summary'),
    ...at('agent', 'name'),
    ...at('owner', 'display_name'),
    ...at('payee', 'name'),
    ...at('payee', 'website'),
    ...at('payee', 'resource_url'),
    ...Object.keys(labels).map((k) => ['labels (key)', k]),
    ...Object.entries(labels).filter(([, v]) => typeof v === 'string').map(([k, v]) => [`labels.${k}`, v]),
  ];
}

function luhn(digits) {
  let sum = 0;
  for (let i = 0; i < digits.length; i++) {
    let d = digits.charCodeAt(digits.length - 1 - i) - 48;
    if (i % 2 === 1) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
  }
  return sum % 10 === 0;
}

function containsPan(text) {
  return (text.match(/\d(?:[ -]?\d)*/g) ?? []).some((run) => {
    const digits = run.replace(/[ -]/g, '');
    return digits.length >= 13 && digits.length <= 19 && luhn(digits);
  });
}

/** 'valid', or the first rule an event breaks: 'schema' or 'pan'. */
function verdict(event) {
  if (!validate(event)) return { result: 'schema', why: ajv.errorsText(validate.errors) };
  const hit = freeText(event).find(([, text]) => containsPan(text));
  if (hit) return { result: 'pan', why: `card number in ${hit[0]}` };
  return { result: 'valid' };
}

// RFC 8785, as the TypeScript SDK's canonicalize.
function canonicalize(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  const keys = Object.keys(value).sort();
  return `{${keys.map((k) => `${JSON.stringify(k)}:${canonicalize(value[k])}`).join(',')}}`;
}

const failures = [];
let passed = 0;
const check = (ok, label) => (ok ? passed++ : failures.push(label));

for (const c of read('conformance/events.json').cases) {
  const v = verdict(c.event);
  const expected = c.expect === 'valid' ? 'valid' : c.rule;
  check(v.result === expected, `events.json ${c.name}: expected ${expected}, got ${v.result}${v.why ? ` (${v.why})` : ''}`);
}

for (const file of readdirSync(new URL('../examples', import.meta.url)).filter((f) => f.endsWith('.json'))) {
  const v = verdict(read(`examples/${file}`));
  check(v.result === 'valid', `examples/${file}: ${v.result} (${v.why})`);
}

const sign = read('conformance/sign-vector.json');
check(canonicalize(sign.event) === sign.canonical_jcs, 'sign-vector.json: canonical form differs');
try {
  const [header, , signature] = sign.sig.split('.');
  const payload = Buffer.from(sign.canonical_jcs, 'utf8').toString('base64url');
  const { protectedHeader } = await compactVerify(
    `${header}.${payload}.${signature}`,
    await importJWK(sign.public_jwk, 'EdDSA'),
    { algorithms: ['EdDSA'] },
  );
  check(
    protectedHeader.typ === 'ape+jws' && protectedHeader.ape === '0.1' && protectedHeader.kid === sign.event.source.id,
    'sign-vector.json: header does not match the spec',
  );
} catch (err) {
  check(false, `sign-vector.json: signature does not verify (${err.message})`);
}

const jcs = read('conformance/jcs-vectors.json');
const view = new DataView(new ArrayBuffer(8));
for (const { bits, expected } of jcs.numbers) {
  view.setBigUint64(0, BigInt(`0x${bits}`));
  check(canonicalize(view.getFloat64(0)) === expected, `jcs-vectors.json number ${bits}`);
}
jcs.objects.forEach(({ json, expected }, i) => check(canonicalize(JSON.parse(json)) === expected, `jcs-vectors.json object ${i}`));

if (failures.length > 0) {
  console.error(`${failures.length} failed, ${passed} passed:\n  ${failures.join('\n  ')}`);
  process.exit(1);
}
console.log(`All ${passed} conformance checks passed.`);
