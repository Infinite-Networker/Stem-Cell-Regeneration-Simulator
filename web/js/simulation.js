/**
 * Stem Cell Regeneration Simulator — Core Simulation Engine (JavaScript)
 * Cherry Computer Ltd. © 2026
 *
 * Pure JavaScript port of the Python simulation logic.
 * Runs entirely in the browser — no server required.
 */

"use strict";

/* ═══════════════════════════════════════════════════════════════
   Seeded pseudo-random number generator (Mulberry32)
   Ensures reproducibility when a seed is given.
   ═══════════════════════════════════════════════════════════════ */
function createRNG(seed) {
  let s = seed >>> 0;
  return function () {
    s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

/* ═══════════════════════════════════════════════════════════════
   Cell class
   ═══════════════════════════════════════════════════════════════ */
class Cell {
  constructor(cellType = "Stem", maxAge = 10, rng) {
    this.cellType  = cellType;
    this.maxAge    = maxAge;
    this.age       = 0;
    this.alive     = true;
    this.mutations = 0;
    this.energy    = 1.0;
    this._rng      = rng;
  }

  update(specializedDeathRate = 0.20) {
    if (!this.alive) return;

    this.age   += 1;
    this.energy = Math.max(0, this.energy - (0.03 + this._rng() * 0.09));

    // Natural lifespan → apoptosis
    if (this.age >= this.maxAge) { this.alive = false; return; }

    // Energy depleted
    if (this.energy <= 0) { this.alive = false; return; }

    // Stochastic death for non-stem cells
    if (this.cellType !== "Stem" && this._rng() < specializedDeathRate) {
      this.alive = false; return;
    }

    // Rare mutation
    if (this._rng() < 0.02) {
      this.mutations++;
      if (this.mutations >= 3) this.cellType = "Damaged";
      if (this.mutations >= 5) { this.alive = false; }
    }
  }
}

/* ═══════════════════════════════════════════════════════════════
   simulateRegeneration
   ═══════════════════════════════════════════════════════════════ */
function simulateRegeneration({
  cycles                = 15,
  initialStemCells      = 5,
  maxCellAge            = 10,
  differentiationProb   = 0.50,
  divisionProb          = 0.60,
  specializedDeathRate  = 0.20,
  multiLineage          = false,
  growthFactor          = 1.0,
  seed                  = 42,
} = {}) {

  // clamp
  growthFactor = Math.max(0.1, Math.min(3.0, growthFactor));

  const rng = seed === 0 ? createRNG(Date.now() & 0xFFFFFFFF) : createRNG(seed);

  const LINEAGE = ["Hematopoietic", "Neural", "Mesenchymal"];

  const keys = ["Stem", "Specialized", "Hematopoietic", "Neural", "Mesenchymal", "Damaged", "Total", "Dead"];
  const history = {};
  keys.forEach(k => (history[k] = []));

  let population = Array.from({ length: initialStemCells }, () =>
    new Cell("Stem", maxCellAge, rng)
  );

  let deadCount = 0;

  for (let cycle = 0; cycle < cycles; cycle++) {
    const newCells = [];
    let cycleDead  = 0;

    for (const cell of population) {
      if (!cell.alive) continue;
      const wasAlive = cell.alive;
      cell.update(specializedDeathRate);

      if (wasAlive && !cell.alive) { cycleDead++; continue; }
      if (!cell.alive) continue;

      if (cell.cellType === "Stem") {
        const effProb = Math.min(1.0, divisionProb * growthFactor);
        if (rng() < effProb) {
          let dtype;
          if (rng() < differentiationProb) {
            dtype = multiLineage
              ? LINEAGE[Math.floor(rng() * LINEAGE.length)]
              : "Specialized";
          } else {
            dtype = "Stem";
          }
          newCells.push(new Cell(dtype, maxCellAge, rng));
        }
      }
    }

    deadCount += cycleDead;
    population = population.filter(c => c.alive).concat(newCells);

    // count
    const counts = { Stem: 0, Specialized: 0, Hematopoietic: 0, Neural: 0, Mesenchymal: 0, Damaged: 0 };
    for (const c of population) {
      if (counts[c.cellType] !== undefined) counts[c.cellType]++;
    }

    const total = Object.values(counts).reduce((a, b) => a + b, 0);
    for (const k of Object.keys(counts)) history[k].push(counts[k]);
    history["Total"].push(total);
    history["Dead"].push(deadCount);
  }

  return history;
}

/* ═══════════════════════════════════════════════════════════════
   Export helpers
   ═══════════════════════════════════════════════════════════════ */
function exportCSV(history) {
  const keys   = Object.keys(history);
  const cycles = history[keys[0]].length;
  const rows   = [["cycle", ...keys].join(",")];
  for (let i = 0; i < cycles; i++) {
    rows.push([i + 1, ...keys.map(k => history[k][i])].join(","));
  }
  return rows.join("\n");
}

function exportJSON(history, params = {}) {
  return JSON.stringify({
    meta: {
      tool:    "Stem Cell Regeneration Simulator v2.0",
      creator: "Cherry Computer Ltd.",
      year:    2026,
    },
    params,
    history,
  }, null, 2);
}

function downloadFile(content, filename, mime = "text/plain") {
  const blob = new Blob([content], { type: mime });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement("a");
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
