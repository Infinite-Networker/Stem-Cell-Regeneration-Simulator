# 🧬 Stem Cell Regeneration Simulator

> A Python-based simulation that models stem cell regeneration dynamics, including self-renewal, differentiation, and cell aging. This educational tool visualizes how stem cell populations maintain and regenerate specialized cell types over time.

---

## Overview

This simulation models the fundamental behavior of stem cells in tissue regeneration:

- **Self-renewal:** Stem cells can divide to produce more stem cells
- **Differentiation:** Stem cells can specialize into functional cells
- **Aging & Death:** Cells have lifespans and can undergo programmed cell death
- **Population Dynamics:** Visualize how cell populations change over time

---

## Features

- 🧬 Simple object-oriented cell model
- 📊 Real-time population tracking and visualization
- 🎲 Stochastic elements for realistic biological variation
- 📈 Clear visual output with matplotlib
- ⚙️ Easily customizable parameters

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator.git
cd Stem-Cell-Regeneration-Simulator
```

**Install required dependencies:**

```bash
pip install matplotlib
```

---

## Usage

**Run the basic simulation:**

```bash
python stem_cell_sim.py
```

### Basic Example

```python
from stem_cell_sim import simulate_regeneration

# Run simulation with default parameters (15 cycles)
results = simulate_regeneration()

# Access the results
stem_counts = results["Stem"]
specialized_counts = results["Specialized"]
```

### Custom Simulation

```python
# Run with custom number of cycles
results = simulate_regeneration(cycles=25)

# Run with a fixed seed for reproducibility
results = simulate_regeneration(cycles=20, seed=42)
```

---

## Simulation Parameters

The simulation includes several key parameters that can be modified:

| Parameter | Default | Description |
|---|---|---|
| `cycles` | `15` | Number of time cycles to simulate |
| `initial_stem_cells` | `5` | Starting population size |
| `max_cell_age` | `10` cycles | Maximum age before death |
| `differentiation_prob` | `0.50` (50%) | Chance a stem cell becomes specialized |
| `division_prob` | `0.60` (60%) | Chance a stem cell divides |
| `specialized_death_rate` | `0.20` (20% per cycle) | Probability of death for specialized cells |
| `seed` | `None` | Optional random seed for reproducibility |

---

## Biological Basis

This simulation is based on key principles of stem cell biology:

- **Stem Cells:** Undifferentiated cells capable of self-renewal and differentiation
- **Specialized Cells:** Differentiated cells with specific functions (limited lifespan)
- **Asymmetric Division:** Stem cells can produce both stem and specialized cells
- **Homeostasis:** Balance between cell production and loss

---

## Customization

### Modifying Cell Behavior

You can easily modify the `Cell` class to change aging and death probabilities:

```python
class Cell:
    def update(self):
        self.age += 1
        # Customize aging and death rules here
        if self.age > 15:  # Longer lifespan
            self.alive = False
```

### Adjusting Stem Cell Logic

Modify the regeneration probabilities via `simulate_regeneration` parameters:

```python
# 70% division rate, 30% differentiation probability
results = simulate_regeneration(
    cycles=20,
    division_prob=0.70,
    differentiation_prob=0.30,
)
```

### Enhanced Visualization

Create more detailed plots using the built-in helper:

```python
from stem_cell_sim import simulate_regeneration, plot_detailed_results

results = simulate_regeneration(cycles=20, seed=0)

plot_detailed_results(results)
```

Or build your own:

```python
import matplotlib.pyplot as plt

def plot_detailed_results(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Population over time
    ax1.plot(history["Stem"], label="Stem Cells", marker='o')
    ax1.plot(history["Specialized"], label="Specialized Cells", marker='s')
    ax1.set_xlabel("Time Cycle")
    ax1.set_ylabel("Cell Count")
    ax1.set_title("Cell Populations Over Time")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Ratio plot
    stem_counts = history["Stem"]
    spec_counts = history["Specialized"]
    ratio = [
        s / (st + s) if (st + s) > 0 else 0
        for st, s in zip(stem_counts, spec_counts)
    ]
    ax2.plot(ratio, color='green', linewidth=2)
    ax2.set_xlabel("Time Cycle")
    ax2.set_ylabel("Specialized Cell Ratio")
    ax2.set_title("Differentiation Ratio")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
```

---

## Contributing

Contributions are welcome! Here are some ideas for enhancements:

- Add multiple stem cell types
- Implement spatial organization
- Add environmental factors (growth factors, nutrients)
- Create interactive parameter sliders
- Export simulation data to CSV
- Add unit tests
- Create web-based version with Streamlit

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by stem cell biology and regenerative medicine concepts
- Built with Python's scientific computing ecosystem
- Educational tool for computational biology students

---

## Citation

If you use this simulation in your research or teaching, please cite:

```text
@software{stem_cell_sim_2026,
  author = {Dr. Ahmad Mateen Ishanzai},
  title  = {Stem Cell Regeneration Simulator},
  year   = {2026},
  url    = {https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator}
}
```

---

## Contact

For questions or feedback, please open an [issue on GitHub](https://github.com/Infinite-Networker/Stem-Cell-Regeneration-Simulator/issues).

---

*Happy Simulating! 🧬🔬*
