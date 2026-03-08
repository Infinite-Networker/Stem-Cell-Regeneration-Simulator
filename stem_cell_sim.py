"""
Stem Cell Regeneration Simulator
=================================
A Python-based simulation that models stem cell regeneration dynamics,
including self-renewal, differentiation, and cell aging.

Author : Dr. Ahmad Mateen Ishanzai
License: MIT
"""

import random
import matplotlib.pyplot as plt
from typing import List, Dict


# ---------------------------------------------------------------------------
# Cell Model
# ---------------------------------------------------------------------------

class Cell:
    """Represents a single biological cell (stem or specialized)."""

    def __init__(self, cell_type: str = "Stem", max_age: int = 10):
        """
        Parameters
        ----------
        cell_type : str
            Either ``"Stem"`` or ``"Specialized"``.
        max_age : int
            Maximum number of cycles the cell can survive.
        """
        if cell_type not in ("Stem", "Specialized"):
            raise ValueError(f"Unknown cell_type '{cell_type}'. Choose 'Stem' or 'Specialized'.")

        self.cell_type: str = cell_type
        self.max_age: int = max_age
        self.age: int = 0
        self.alive: bool = True

    # ------------------------------------------------------------------
    def update(self) -> None:
        """Advance the cell by one time cycle and apply aging / death rules."""
        if not self.alive:
            return

        self.age += 1

        # Natural lifespan exceeded → apoptosis (programmed cell death)
        if self.age >= self.max_age:
            self.alive = False
            return

        # Specialized cells have an additional stochastic death rate (~20 % / cycle)
        if self.cell_type == "Specialized" and random.random() < 0.20:
            self.alive = False

    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        status = "alive" if self.alive else "dead"
        return f"Cell(type={self.cell_type}, age={self.age}, status={status})"


# ---------------------------------------------------------------------------
# Simulation Engine
# ---------------------------------------------------------------------------

def simulate_regeneration(
    cycles: int = 15,
    initial_stem_cells: int = 5,
    max_cell_age: int = 10,
    differentiation_prob: float = 0.50,
    division_prob: float = 0.60,
    specialized_death_rate: float = 0.20,
    seed: int | None = None,
) -> Dict[str, List[int]]:
    """
    Run a stem-cell regeneration simulation.

    Parameters
    ----------
    cycles : int
        Number of time cycles to simulate.
    initial_stem_cells : int
        Number of stem cells at t = 0.
    max_cell_age : int
        Maximum age (in cycles) before a cell dies of old age.
    differentiation_prob : float
        Probability that a dividing stem cell produces a specialized cell.
    division_prob : float
        Probability that a stem cell attempts to divide in a given cycle.
    specialized_death_rate : float
        Per-cycle probability that a specialized cell dies (used inside Cell.update).
    seed : int or None
        Optional random seed for reproducibility.

    Returns
    -------
    dict
        ``{"Stem": [...], "Specialized": [...]}`` — population counts per cycle.
    """
    if seed is not None:
        random.seed(seed)

    # Validate parameters
    if cycles < 1:
        raise ValueError("cycles must be >= 1.")
    if initial_stem_cells < 1:
        raise ValueError("initial_stem_cells must be >= 1.")
    if not 0.0 <= differentiation_prob <= 1.0:
        raise ValueError("differentiation_prob must be between 0 and 1.")
    if not 0.0 <= division_prob <= 1.0:
        raise ValueError("division_prob must be between 0 and 1.")

    # Initialise population
    population: List[Cell] = [
        Cell(cell_type="Stem", max_age=max_cell_age)
        for _ in range(initial_stem_cells)
    ]

    history: Dict[str, List[int]] = {"Stem": [], "Specialized": []}

    for _cycle in range(cycles):
        new_cells: List[Cell] = []

        for cell in population:
            if not cell.alive:
                continue

            cell.update()  # age / natural death

            if not cell.alive:
                continue

            # Only stem cells divide
            if cell.cell_type == "Stem" and random.random() < division_prob:
                # Determine daughter-cell type
                if random.random() < differentiation_prob:
                    daughter_type = "Specialized"
                else:
                    daughter_type = "Stem"
                new_cells.append(Cell(cell_type=daughter_type, max_age=max_cell_age))

        population.extend(new_cells)

        # Remove dead cells (keeps memory tidy in long simulations)
        population = [c for c in population if c.alive]

        # Record current counts
        stem_count = sum(1 for c in population if c.cell_type == "Stem")
        spec_count = sum(1 for c in population if c.cell_type == "Specialized")
        history["Stem"].append(stem_count)
        history["Specialized"].append(spec_count)

    return history


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def plot_results(history: Dict[str, List[int]], save_path: str | None = None) -> None:
    """
    Plot stem-cell and specialized-cell populations over time.

    Parameters
    ----------
    history : dict
        Output from :func:`simulate_regeneration`.
    save_path : str or None
        If given, the figure is saved to this file path instead of displayed.
    """
    cycles = list(range(1, len(history["Stem"]) + 1))

    plt.figure(figsize=(10, 5))
    plt.plot(cycles, history["Stem"], label="Stem Cells", marker="o", color="steelblue")
    plt.plot(cycles, history["Specialized"], label="Specialized Cells", marker="s", color="coral")
    plt.xlabel("Time Cycle")
    plt.ylabel("Cell Count")
    plt.title("Stem Cell Regeneration Simulation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Figure saved to '{save_path}'.")
    else:
        plt.show()

    plt.close()


def plot_detailed_results(
    history: Dict[str, List[int]], save_path: str | None = None
) -> None:
    """
    Create a two-panel figure: population over time *and* differentiation ratio.

    Parameters
    ----------
    history : dict
        Output from :func:`simulate_regeneration`.
    save_path : str or None
        If given, the figure is saved to this file path instead of displayed.
    """
    cycles = list(range(1, len(history["Stem"]) + 1))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # --- Panel 1: population counts ---
    ax1.plot(cycles, history["Stem"], label="Stem Cells", marker="o", color="steelblue")
    ax1.plot(cycles, history["Specialized"], label="Specialized Cells", marker="s", color="coral")
    ax1.set_xlabel("Time Cycle")
    ax1.set_ylabel("Cell Count")
    ax1.set_title("Cell Populations Over Time")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # --- Panel 2: differentiation ratio ---
    stem_counts = history["Stem"]
    spec_counts = history["Specialized"]
    ratio = [
        s / (st + s) if (st + s) > 0 else 0.0
        for st, s in zip(stem_counts, spec_counts)
    ]
    ax2.plot(cycles, ratio, color="green", linewidth=2)
    ax2.set_xlabel("Time Cycle")
    ax2.set_ylabel("Specialized Cell Ratio")
    ax2.set_title("Differentiation Ratio Over Time")
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Detailed figure saved to '{save_path}'.")
    else:
        plt.show()

    plt.close()


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Stem Cell Regeneration Simulator ===\n")

    # Default run (15 cycles)
    results = simulate_regeneration(cycles=15, seed=42)

    print(f"{'Cycle':<8} {'Stem':>8} {'Specialized':>14}")
    print("-" * 32)
    for i, (s, sp) in enumerate(zip(results["Stem"], results["Specialized"]), start=1):
        print(f"{i:<8} {s:>8} {sp:>14}")

    print(f"\nFinal stem cells     : {results['Stem'][-1]}")
    print(f"Final specialized    : {results['Specialized'][-1]}")
    total_final = results["Stem"][-1] + results["Specialized"][-1]
    print(f"Total cells at end   : {total_final}\n")

    plot_detailed_results(results)
