# 🧬 Stem Cell Regeneration Simulator

<p align="center">
  <img src="logo.png" alt="Stem Cell Regeneration Simulator Logo" width="260"/>
</p>

<p align="center">
  <strong>Created by <a href="https://github.com/Infinite-Networker">Cherry Computer Ltd.</a></strong><br/>
  © 2026 Cherry Computer Ltd. All Rights Reserved.
</p>

<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-2.0-E91E63?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg=="/>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-4FC3F7?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="License" src="https://img.shields.io/badge/License-MIT-69F0AE?style=for-the-badge"/>
  <img alt="Web UI" src="https://img.shields.io/badge/Web_UI-Included-FF8A65?style=for-the-badge"/>
  [![Made by](https://img.shields.io/badge/Made%20by-Cherry%20Computer%20Ltd.-e8003d?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+&logoColor=white)](#-cherry-computer-ltd)
</p>

---

> A Python-based simulation (with an interactive browser-based UI) that models stem cell regeneration dynamics — including self-renewal, differentiation, apoptosis, multi-lineage commitment, mutation accumulation, and cellular energy. Built and maintained by **Cherry Computer Ltd.**

---

## ✨ What's New in v2.0

| Feature | Description |
|---|---|
| 🌐 **Interactive Web UI** | Full browser-based simulator with real-time Chart.js visualisations |
| 🧬 **Multi-Lineage Mode** | Stem cells differentiate into Hematopoietic, Neural & Mesenchymal lineages |
| 💊 **Growth-Factor Simulation** | Model therapeutic growth-factor treatment (0.1× – 3.0× multiplier) |
| ⚡ **Cellular Energy** | Cells track metabolic energy; depletion triggers apoptosis |
| 🔬 **Mutation Tracking** | Stochastic mutation accumulation → cell damage → death |
| 📦 **CSV & JSON Export** | Export simulation data from both the Python CLI and the web UI |
| 🎨 **Cherry Computer Branding** | Dark-theme dashboard with Cherry Computer Ltd. signature styling |
| 📊 **4-Panel Dashboard Plot** | Population, differentiation ratio, stacked area, deaths-per-cycle |
| 🔁 **Scenario Comparison** | Run multiple parameter sets and compare on a single figure |
| 🎯 **Animated Web Runner** | Step-by-step animated visualisation in the browser |

---

## Overview

This simulation models the fundamental behaviour of stem cells in tissue regeneration:

- **Self-renewal** — Stem cells divide to produce more stem cells
- **Differentiation** — Stem cells specialise into functional cells (or multi-lineage types)
- **Aging & Apoptosis** — Cells have lifespans and undergo programmed cell death
- **Metabolic Energy** — Energy depletion independently triggers cell death
- **Mutation Accumulation** — Rare mutations degrade cells and cause damage/death
- **Growth-Factor Modelling** — Simulate clinical intervention scenarios
- **Population Dynamics** — Visualise how cell populations evolve over time

---

## Project Structure

```
Stem-Cell-Regeneration-Simulator/
├── stem_cell_sim.py          # Core Python simulation engine (v2.0)
├── requirements.txt          # Python dependencies
├── web/                      # Interactive browser UI
│   ├── index.html            # Main HTML page
│   ├── css/
│   │   └── style.css         # Cherry Computer dark-theme stylesheet
│   └── js/
│       ├── simulation.js     # JS port of the simulation engine
│       └── app.js            # UI controller & Chart.js integration
├── docs/
│   └── parameters.md         # Detailed parameter documentation
├── logo.png
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator.git
cd Stem-Cell-Regeneration-Simulator
```

**Install Python dependencies:**

```bash
pip install -r requirements.txt
```

---

## Usage

### Python CLI

```bash
python stem_cell_sim.py
```

The CLI will:
1. Print a colour-coded header with Cherry Computer Ltd. branding
2. Run a default 15-cycle simulation (seed = 42)
3. Display a live per-cycle progress table
4. Print a summary panel
5. Run a multi-lineage demo (20 cycles)
6. Export `simulation_results.csv` and `simulation_results.json`
7. Generate `scenario_comparison.png` and `stem_cell_dashboard.png`

---

### Web UI

Open `web/index.html` in any modern browser — no server required:

```bash
open web/index.html         # macOS
xdg-open web/index.html     # Linux
start web/index.html        # Windows
```

Or serve it locally:

```bash
python -m http.server 8080
# then visit http://localhost:8080/web/
```

---

### Python API

**Basic example:**

```python
from stem_cell_sim import simulate_regeneration

results = simulate_regeneration(cycles=15, seed=42)
print(results["Stem"])
print(results["Specialized"])
```

**Advanced — multi-lineage + growth factor:**

```python
from stem_cell_sim import simulate_regeneration, plot_detailed_results, export_csv

results = simulate_regeneration(
    cycles=25,
    initial_stem_cells=8,
    division_prob=0.65,
    differentiation_prob=0.45,
    growth_factor=1.4,
    multi_lineage=True,
    seed=7,
    verbose=True,
)

plot_detailed_results(results, save_path="dashboard.png")
export_csv(results, "results.csv")
```

**Scenario comparison:**

```python
from stem_cell_sim import SimulationConfig, run_scenario_comparison

scenarios = [
    ("Baseline",       SimulationConfig(cycles=20, seed=1)),
    ("High Division",  SimulationConfig(cycles=20, division_prob=0.80, seed=1)),
    ("Growth Factor",  SimulationConfig(cycles=20, growth_factor=1.8, seed=1)),
]

run_scenario_comparison(scenarios, save_path="comparison.png")
```

---

## Simulation Parameters

| Parameter | Default | Range | Description |
|---|---|---|---|
| `cycles` | `15` | 1 – ∞ | Number of time cycles |
| `initial_stem_cells` | `5` | ≥ 1 | Starting stem-cell population |
| `max_cell_age` | `10` | ≥ 1 | Cycles before natural apoptosis |
| `differentiation_prob` | `0.50` | 0 – 1 | Probability a division yields a specialised cell |
| `division_prob` | `0.60` | 0 – 1 | Probability a stem cell divides per cycle |
| `specialized_death_rate` | `0.20` | 0 – 1 | Per-cycle stochastic death for specialised cells |
| `growth_factor` | `1.0` | 0.1 – 3.0 | Multiplier on division probability |
| `multi_lineage` | `False` | bool | Enable Hematopoietic / Neural / Mesenchymal lineages |
| `seed` | `None` | int | Random seed (None = non-reproducible) |
| `verbose` | `False` | bool | Print per-cycle stats to stdout |

---

## Biological Basis

| Concept | Simulation Representation |
|---|---|
| Stem cell self-renewal | Symmetric division → two Stem daughters |
| Asymmetric division | One Stem + one Specialised daughter |
| Multipotency | Multi-lineage mode (Hematopoietic / Neural / Mesenchymal) |
| Hayflick limit | `max_cell_age` triggers apoptosis |
| Metabolic stress | Energy depletion triggers cell death |
| Oncogenesis | Mutation accumulation → Damaged cell type |
| Growth-factor therapy | `growth_factor` multiplier on division probability |
| Tissue homeostasis | Balance between production and turnover |

---

## Output Files

| File | Description |
|---|---|
| `simulation_results.csv` | Cycle-by-cycle population counts |
| `simulation_results.json` | Full results + metadata + config |
| `stem_cell_dashboard.png` | 4-panel matplotlib dashboard |
| `scenario_comparison.png` | Multi-scenario comparison plot |

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ideas for future enhancements:
- Spatial cell organisation (grid-based model)
- Environmental nutrient / oxygen gradients
- Cancer stem-cell subpopulations
- Immune system interactions
- Real clinical data integration
- Streamlit / Flask web backend
- Unit & integration test suite

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## About Cherry Computer Ltd.

**Cherry Computer Ltd.** builds advanced scientific computing tools for researchers, educators, and clinicians worldwide. Our mission is to make cutting-edge computational biology accessible to everyone.

> "Building Tomorrow's Scientific Tools Today."
> — Cherry Computer Ltd.

---

## Citation

If you use this simulation in research or teaching, please cite:

```text
@software{stem_cell_sim_2026,
  author  = {Cherry Computer Ltd.},
  title   = {Stem Cell Regeneration Simulator v2.0},
  year    = {2026},
  url     = {https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator}
}
```

---

## Contact

For questions or feedback, open an [issue on GitHub](https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator/issues).

---

<p align="center">
  🍒 <strong>Cherry Computer Ltd.</strong> — Happy Simulating! 🧬🔬
</p>
