// Snowboard Math engine - hypothetical arithmetic on labeled norms only.
// Weight charts, mondo conversion, outsole and stance figures are labeled
// norms, not measurements of your body, boots or boards.

function plural(n, one, many) { return n === 1 ? one : many; }
function tenths(x) { return Math.floor(x * 10 + 0.5) / 10; }
function fixed1(x) { return tenths(x).toFixed(1); }

// labeled norm: all-mountain length chart anchors (kg -> cm)
const KG = [40, 50, 60, 70, 80, 90, 100];
const CM = [140, 147, 152, 156, 159, 162, 165];
const STYLE = ["freestyle", "all-mountain", "freeride"];
const OFFSET = [-3, 0, 2]; // labeled norm: style offset in cm

function chartLength(kg) {
  if (kg <= KG[0]) return CM[0] + (kg - KG[0]) * (CM[1] - CM[0]) / (KG[1] - KG[0]);
  for (let i = 0; i < KG.length - 1; i++) {
    if (kg <= KG[i + 1]) return CM[i] + (kg - KG[i]) * (CM[i + 1] - CM[i]) / (KG[i + 1] - KG[i]);
  }
  const n = KG.length - 1;
  return CM[n] + (kg - KG[n]) * (CM[n] - CM[n - 1]) / (KG[n] - KG[n - 1]);
}

function lengthTruth(kg, style) {
  if (!(kg > 0)) throw new Error("the rider weight must be above zero");
  const base = chartLength(kg) + OFFSET[style];
  return `At ${kg} kg the ${STYLE[style]} chart reads ${fixed1(base - 2)} to ${fixed1(base + 2)} cm; the chin test never asked your weight honestly.`;
}

function widthTruth(us, waist) {
  if (!(us > 0)) throw new Error("the boot size must be above zero");
  if (!(waist > 0)) throw new Error("the waist width must be above zero");
  const sole = (us + 17) * 10 + 20; // labeled norm: mondo + outsole allowance, mm
  const need = sole - 30; // labeled norm: 15 mm of toe and heel overhang each
  const dm = tenths(waist - need);
  let verdict;
  if (dm > 0) verdict = `clears the drag line by ${fixed1(dm)} mm honestly`;
  else if (dm < 0) verdict = `comes ${fixed1(-dm)} mm short of the drag line honestly`;
  else verdict = "lands exactly on the drag line honestly";
  return `A US ${us} boot measures about ${fixed1(sole)} mm over the sole; the ${waist} mm waist ${verdict}.`;
}

function stanceTruth(height, ref) {
  if (!(height > 0)) throw new Error("the rider height must be above zero");
  if (!(ref > 0)) throw new Error("the reference stance must be above zero");
  const rn = tenths(height * 0.29); // labeled norm: stance starts near 29% of height
  const dm = tenths(ref - rn);
  let verdict;
  if (dm > 0) verdict = `sits ${fixed1(dm)} cm wider honestly`;
  else if (dm < 0) verdict = `sits ${fixed1(-dm)} cm narrower honestly`;
  else verdict = "matches exactly honestly";
  return `At ${height} cm the stance chart reads ${rn.toFixed(1)} cm; the board's ${fixed1(ref)} cm reference ${verdict}.`;
}

if (typeof module !== "undefined") {
  module.exports = { lengthTruth, widthTruth, stanceTruth };
}
