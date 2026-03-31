# Stem Cell Regeneration Simulator — Parameter Reference
# Cherry Computer Ltd. © 2026

## `simulate_regeneration()` Parameters

### `cycles` (int, default: 15)
The total number of time steps (cycles) to run the simulation.
Each cycle represents one unit of biological time (e.g., one cell generation).
- Minimum: 1
- Recommended range: 10 – 50 for meaningful population dynamics

---

### `initial_stem_cells` (int, default: 5)
The number of stem cells present at the start of the simulation (t = 0).
- Minimum: 1
- Higher values produce more stable and diverse populations

---

### `max_cell_age` (int, default: 10)
The maximum number of cycles a cell can survive before undergoing apoptosis (programmed cell death).
This models the Hayflick limit — the number of times a normal cell can divide before it stops.
- Minimum: 1
- Typical biological values: 5 – 20 cycles

---

### `differentiation_prob` (float, default: 0.50)
The probability (0.0 – 1.0) that when a stem cell divides, the daughter cell becomes a specialised cell rather than another stem cell.
- 0.0 = all divisions produce stem cells (no differentiation)
- 1.0 = all divisions produce specialised cells (rapid depletion of stem pool)
- Biological range: 0.30 – 0.70

---

### `division_prob` (float, default: 0.60)
The probability (0.0 – 1.0) that a stem cell will attempt to divide in a given cycle.
- 0.0 = no divisions (population will die out)
- 1.0 = every stem cell divides every cycle (rapid expansion)
- Modulated by `growth_factor` during treatment simulation

---

### `specialized_death_rate` (float, default: 0.20)
The per-cycle probability that a specialised (differentiated) cell will undergo stochastic death.
This models normal tissue cell turnover.
- 0.0 = specialised cells are immortal
- 0.20 = 20% of specialised cells die each cycle (default — physiologically realistic)
- 0.50+ = aggressive turnover (models tissue injury)

---

### `growth_factor` (float, default: 1.0)
A multiplier applied to `division_prob` to simulate the effect of therapeutic growth factors
(e.g., G-CSF, EGF, FGF). The effective division probability is:

    eff_prob = min(1.0, division_prob × growth_factor)

- 1.0 = baseline (no treatment)
- 1.5 = moderate growth-factor stimulation
- 2.0 = strong treatment response
- Range: 0.1 – 3.0

---

### `multi_lineage` (bool, default: False)
When True, stem cells can differentiate into one of three lineage types:
- **Hematopoietic** — blood cell precursors
- **Neural** — nervous system precursors  
- **Mesenchymal** — connective tissue precursors

This models the multipotency of adult stem cells found in bone marrow and other tissues.

---

### `seed` (int or None, default: None)
An optional integer random seed for fully reproducible simulations.
- `None` = new random result every run
- Any integer = deterministic, reproducible output

---

### `verbose` (bool, default: False)
If True, prints a colour-coded per-cycle statistics table to stdout as the simulation runs.

---

## Return Value

`simulate_regeneration()` returns a `dict` with these keys:

| Key | Type | Description |
|---|---|---|
| `"Stem"` | `List[int]` | Stem cell count per cycle |
| `"Specialized"` | `List[int]` | Specialised cell count per cycle |
| `"Hematopoietic"` | `List[int]` | Hematopoietic count (0 unless `multi_lineage=True`) |
| `"Neural"` | `List[int]` | Neural count (0 unless `multi_lineage=True`) |
| `"Mesenchymal"` | `List[int]` | Mesenchymal count (0 unless `multi_lineage=True`) |
| `"Damaged"` | `List[int]` | Cells with ≥3 mutations per cycle |
| `"Total"` | `List[int]` | Total living cell count per cycle |
| `"Dead"` | `List[int]` | Cumulative death count per cycle |

---

*Cherry Computer Ltd. © 2026 — Building Tomorrow's Scientific Tools Today.*
