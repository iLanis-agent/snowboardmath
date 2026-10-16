# Snowboard Math

Snowboard sizing honesty. The chin test was never a measurement; the chart counts kilograms,
and your boots count millimeters.

- Landing: `index.html`
- App: `app.html` (loads `engine.js`)

## What it does

Stand a board on its tail and every chin gets the same answer, whatever the rider weighs.
Three panels of honest arithmetic:

- **The length truth** - rider weight read against the labeled all-mountain chart
  (interpolated), adjusted by style: freestyle -3 cm, freeride +2 cm, as a plus-or-minus
  2 cm window.
- **The width truth** - boot size (US men's) to mondo (US + 17) to an outsole norm
  (+20 mm), weighed against the board's waist with a 15 mm toe-and-heel overhang allowance:
  clears the drag line, lands on it, or comes up short.
- **The stance truth** - rider height x 0.29 (labeled norm) weighed against the board's
  reference stance: wider, narrower, or matched.

## Norms used (labeled, illustrative)

- Length chart anchors: 40 kg -> 140 cm through 100 kg -> 165 cm, linear between.
- Mondo = US men's + 17; outsole = mondo + 20 mm; overhang allowance 15 mm per side.
- Stance norm: 29% of rider height.

Every figure is hypothetical arithmetic on labeled norms, not a statement about any real
rider, boot or board. Try the board or trust the shop's fit session.

## Tests

`oracle.py` generates `expected.json` from a Python mirror of the engine (same operation
order, same rounding). `node test.js` checks the JavaScript engine against it:

```
python3 oracle.py
node test.js
```
