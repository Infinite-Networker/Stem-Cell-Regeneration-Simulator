"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          STEM CELL REGENERATION SIMULATOR  ·  v2.0                          ║
║          Created by Cherry Computer Ltd.                                    ║
║          © 2026 Cherry Computer Ltd. All rights reserved.                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

A Python-based simulation that models stem cell regeneration dynamics,
including self-renewal, differentiation, apoptosis, and cell aging.

Features
--------
- Stochastic stem-cell division / differentiation model
- Extended cell-type hierarchy (Hematopoietic, Neural, Mesenchymal)
- Mutation & damage tracking
- Export to CSV / JSON
- Rich CLI output with colour via ANSI codes
- Matplotlib visualisations (basic & detailed)

Author  : Dr. Ahmad Mateen Ishanzai
Company : Cherry Computer Ltd.
License : MIT
"""

from __future__ import annotations

import csv
import json
import math
import random
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# ANSI colour helpers
# ─────────────────────────────────────────────────────────────────────────────

_USE_COLOUR = sys.stdout.isatty()


def _c(code: str, text: str) -> str:
    """Wrap *text* in an ANSI colour code (no-op if not a TTY)."""
    if not _USE_COLOUR:
        return text
    return f"\033[{code}m{text}\033[0m"


def cyan(t: str)    -> str: return _c("96", t)
def green(t: str)   -> str: return _c("92", t)
def yellow(t: str)  -> str: return _c("93", t)
def red(t: str)     -> str: return _c("91", t)
def bold(t: str)    -> str: return _c("1",  t)
def magenta(t: str) -> str: return _c("95", t)
def blue(t: str)    -> str: return _c("94", t)
def dim(t: str)     -> str: return _c("2",  t)


# ─────────────────────────────────────────────────────────────────────────────
# Cell Model
# ─────────────────────────────────────────────────────────────────────────────

CELL_TYPES = {
    "Stem":           {"colour": "steelblue",  "marker": "o", "emoji": "🔵"},
    "Specialized":    {"colour": "coral",       "marker": "s", "emoji": "🟠"},
    "Hematopoietic":  {"colour": "crimson",     "marker": "^", "emoji": "🔴"},
    "Neural":         {"colour": "mediumpurple","marker": "D", "emoji": "🟣"},
    "Mesenchymal":    {"colour": "seagreen",    "marker": "P", "emoji": "🟢"},
    "Damaged":        {"colour": "dimgray",     "marker": "x", "emoji": "⚫"},
}


@dataclass
class Cell:
    """Represents a single biological cell."""

    cell_type: str = "Stem"
    max_age:   int = 10
    age:       int = field(default=0, init=False)
    alive:     bool = field(default=True, init=False)
    mutations: int = field(default=0, init=False)
    energy:    float = field(default=1.0, init=False)   # 0.0 – 1.0

    def __post_init__(self) -> None:
        if self.cell_type not in CELL_TYPES:
            raise ValueError(
                f"Unknown cell_type '{self.cell_type}'. "
                f"Valid types: {list(CELL_TYPES)}"
            )

    # ------------------------------------------------------------------ #
    def update(self, specialized_death_rate: float = 0.20) -> None:
        """Advance the cell by one time cycle."""
        if not self.alive:
            return

        self.age    += 1
        self.energy  = max(0.0, self.energy - random.uniform(0.03, 0.12))

        # Natural lifespan exceeded → apoptosis
        if self.age >= self.max_age:
            self.alive = False
            return

        # Energy depletion → death
        if self.energy <= 0.0:
            self.alive = False
            return

        # Stochastic death for non-stem cells
        if self.cell_type != "Stem" and random.random() < specialized_death_rate:
            self.alive = False
            return

        # Random mutation accumulation (rare)
        if random.random() < 0.02:
            self.mutations += 1
            # Too many mutations → damaged / death
            if self.mutations >= 3:
                self.cell_type = "Damaged"
            if self.mutations >= 5:
                self.alive = False

    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:
        status = "alive" if self.alive else "dead"
        return (
            f"Cell(type={self.cell_type}, age={self.age}, "
            f"energy={self.energy:.2f}, mutations={self.mutations}, status={status})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Simulation Engine
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class SimulationConfig:
    """All tunable parameters for one simulation run."""

    cycles:                int   = 15
    initial_stem_cells:    int   = 5
    max_cell_age:          int   = 10
    differentiation_prob:  float = 0.50
    division_prob:         float = 0.60
    specialized_death_rate:float = 0.20
    multi_lineage:         bool  = False   # enable Hematopoietic / Neural / Mesenchymal
    growth_factor:         float = 1.0     # multiplier on division probability (0.5 – 2.0)
    seed:        Optional[int]   = None


def simulate_regeneration(
    cycles:                int   = 15,
    initial_stem_cells:    int   = 5,
    max_cell_age:          int   = 10,
    differentiation_prob:  float = 0.50,
    division_prob:         float = 0.60,
    specialized_death_rate:float = 0.20,
    multi_lineage:         bool  = False,
    growth_factor:         float = 1.0,
    seed:        Optional[int]   = None,
    verbose:               bool  = False,
) -> Dict[str, List[int]]:
    """
    Run a complete stem-cell regeneration simulation.

    Parameters
    ----------
    cycles                : Number of time cycles to simulate.
    initial_stem_cells    : Starting stem-cell population.
    max_cell_age          : Maximum cycles a cell can survive.
    differentiation_prob  : Probability a dividing stem cell specialises.
    division_prob         : Probability a stem cell divides per cycle.
    specialized_death_rate: Per-cycle death probability for non-stem cells.
    multi_lineage         : If True, daughter cells may become Hematopoietic,
                            Neural, or Mesenchymal instead of generic Specialized.
    growth_factor         : Scales effective division probability (simulate
                            growth-factor treatment; 1.0 = baseline).
    seed                  : Optional random seed for reproducibility.
    verbose               : Print per-cycle statistics to stdout.

    Returns
    -------
    dict  – keys = cell-type names, values = list of counts per cycle.
            Also includes "Total", "Dead", and "Damaged" series.
    """
    if seed is not None:
        random.seed(seed)

    # ── validation ──────────────────────────────────────────────────────
    if cycles < 1:
        raise ValueError("cycles must be >= 1.")
    if initial_stem_cells < 1:
        raise ValueError("initial_stem_cells must be >= 1.")
    for name, val in [("differentiation_prob", differentiation_prob),
                      ("division_prob",         division_prob),
                      ("specialized_death_rate",specialized_death_rate)]:
        if not 0.0 <= val <= 1.0:
            raise ValueError(f"{name} must be in [0, 1].")
    growth_factor = max(0.1, min(3.0, growth_factor))

    # ── initial population ───────────────────────────────────────────────
    population: List[Cell] = [
        Cell(cell_type="Stem", max_age=max_cell_age)
        for _ in range(initial_stem_cells)
    ]

    lineage_types = ["Hematopoietic", "Neural", "Mesenchymal"]
    type_keys     = list(CELL_TYPES.keys())
    history: Dict[str, List[int]] = {k: [] for k in type_keys + ["Total", "Dead", "Damaged"]}
    dead_count = 0

    for cycle_idx in range(cycles):
        new_cells: List[Cell] = []
        cycle_dead = 0

        for cell in population:
            if not cell.alive:
                continue

            was_alive = cell.alive
            cell.update(specialized_death_rate=specialized_death_rate)

            if was_alive and not cell.alive:
                cycle_dead += 1
                continue

            # ── stem-cell division logic ─────────────────────────────────
            if cell.cell_type == "Stem":
                eff_prob = min(1.0, division_prob * growth_factor)
                if random.random() < eff_prob:
                    if random.random() < differentiation_prob:
                        if multi_lineage:
                            dtype = random.choice(lineage_types)
                        else:
                            dtype = "Specialized"
                    else:
                        dtype = "Stem"
                    new_cells.append(Cell(cell_type=dtype, max_age=max_cell_age))

        dead_count += cycle_dead
        population.extend(new_cells)
        population = [c for c in population if c.alive]

        # ── record counts ────────────────────────────────────────────────
        counts = {k: 0 for k in type_keys}
        for c in population:
            counts[c.cell_type] = counts.get(c.cell_type, 0) + 1

        for k in type_keys:
            history[k].append(counts.get(k, 0))

        total = sum(counts.values())
        history["Total"].append(total)
        history["Dead"].append(dead_count)
        history["Damaged"].append(counts.get("Damaged", 0))

        if verbose:
            _print_cycle_stats(cycle_idx + 1, counts, total, dead_count)

    return history


# ─────────────────────────────────────────────────────────────────────────────
# CLI helpers
# ─────────────────────────────────────────────────────────────────────────────

def _print_header() -> None:
    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║   🧬  STEM CELL REGENERATION SIMULATOR  ·  v2.0             ║",
        "║   Created by Cherry Computer Ltd.                           ║",
        "║   © 2026 Cherry Computer Ltd. All rights reserved.          ║",
        "╚══════════════════════════════════════════════════════════════╝",
    ]
    for line in lines:
        print(cyan(line))
    print()


def _print_cycle_stats(
    cycle: int,
    counts: Dict[str, int],
    total: int,
    dead: int,
) -> None:
    bar_len  = 30
    stem_cnt = counts.get("Stem", 0)
    bar_fill = int(bar_len * stem_cnt / max(total, 1))
    bar      = green("█" * bar_fill) + dim("░" * (bar_len - bar_fill))

    parts = []
    for k, v in counts.items():
        if v > 0:
            parts.append(f"{CELL_TYPES[k]['emoji']} {k}: {v}")

    print(
        f"  {bold(f'Cycle {cycle:>3}')}  [{bar}]  "
        + "  ".join(parts)
        + dim(f"  (dead so far: {dead})")
    )


def _print_summary(history: Dict[str, List[int]]) -> None:
    print()
    print(cyan("─" * 64))
    print(bold("  SIMULATION SUMMARY"))
    print(cyan("─" * 64))
    cycles = len(history["Stem"])
    print(f"  Cycles run       : {bold(str(cycles))}")
    print(f"  Final stem cells : {bold(green(str(history['Stem'][-1])))}")
    print(f"  Final specialised: {bold(yellow(str(history['Specialized'][-1])))}")
    print(f"  Total cells (end): {bold(str(history['Total'][-1]))}")
    print(f"  Cumulative deaths: {bold(red(str(history['Dead'][-1])))}")
    if sum(history["Hematopoietic"]) > 0:
        print(f"  Hematopoietic    : {bold(str(history['Hematopoietic'][-1]))}")
        print(f"  Neural           : {bold(str(history['Neural'][-1]))}")
        print(f"  Mesenchymal      : {bold(str(history['Mesenchymal'][-1]))}")
    peak_total = max(history["Total"])
    peak_cycle = history["Total"].index(peak_total) + 1
    print(f"  Peak population  : {bold(str(peak_total))} at cycle {peak_cycle}")
    print(cyan("─" * 64))
    print()


def print_table(history: Dict[str, List[int]]) -> None:
    """Print a formatted cycle-by-cycle table to stdout."""
    cols = ["Stem", "Specialized", "Total", "Dead"]
    header = f"  {'Cycle':<8}" + "".join(f"{c:>14}" for c in cols)
    print(cyan(header))
    print(cyan("  " + "─" * (8 + 14 * len(cols))))
    for i, stem in enumerate(history["Stem"]):
        row = (
            f"  {i+1:<8}"
            f"{green(str(stem)):>14}"
            f"{yellow(str(history['Specialized'][i])):>14}"
            f"{str(history['Total'][i]):>14}"
            f"{red(str(history['Dead'][i])):>14}"
        )
        print(row)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# Visualisation
# ─────────────────────────────────────────────────────────────────────────────

def _check_mpl() -> None:
    if not _MPL_AVAILABLE:
        raise ImportError(
            "matplotlib is required for visualisation.\n"
            "Install it with:  pip install matplotlib"
        )


def plot_results(
    history: Dict[str, List[int]],
    save_path: Optional[str] = None,
    title: str = "Stem Cell Regeneration Simulation",
) -> None:
    """Single-panel population plot with Cherry Computer Ltd. styling."""
    _check_mpl()
    cycles = list(range(1, len(history["Stem"]) + 1))

    fig, ax = plt.subplots(figsize=(11, 5))
    _apply_cherry_style(fig, ax)

    ax.plot(cycles, history["Stem"],
            label="Stem Cells", marker="o", color="#2196F3", linewidth=2.2,
            markersize=6, zorder=3)
    ax.plot(cycles, history["Specialized"],
            label="Specialized Cells", marker="s", color="#FF5722", linewidth=2.2,
            markersize=6, zorder=3)
    ax.fill_between(cycles, history["Stem"],       alpha=0.15, color="#2196F3")
    ax.fill_between(cycles, history["Specialized"],alpha=0.15, color="#FF5722")

    ax.set_xlabel("Time Cycle", fontsize=12)
    ax.set_ylabel("Cell Count",  fontsize=12)
    ax.set_title(title, fontsize=15, fontweight="bold", pad=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.25, linestyle="--")

    _add_watermark(fig)
    plt.tight_layout()
    _save_or_show(fig, save_path, "Figure")


def plot_detailed_results(
    history: Dict[str, List[int]],
    save_path: Optional[str] = None,
) -> None:
    """Four-panel dashboard plot with Cherry Computer Ltd. branding."""
    _check_mpl()
    cycles = list(range(1, len(history["Stem"]) + 1))

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor("#0D1117")
    gs = GridSpec(2, 2, figure=fig, hspace=0.40, wspace=0.32)

    axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(2)]
    for ax in axes:
        _apply_cherry_style(fig, ax)

    # ── panel 0: population ──────────────────────────────────────────────
    ax0 = axes[0]
    ax0.plot(cycles, history["Stem"], label="Stem",
             color="#4FC3F7", marker="o", linewidth=2, markersize=5)
    ax0.plot(cycles, history["Specialized"], label="Specialized",
             color="#FF8A65", marker="s", linewidth=2, markersize=5)
    if sum(history.get("Hematopoietic", [])) > 0:
        ax0.plot(cycles, history["Hematopoietic"], label="Hematopoietic",
                 color="#EF5350", marker="^", linewidth=1.8, markersize=5)
        ax0.plot(cycles, history["Neural"], label="Neural",
                 color="#CE93D8", marker="D", linewidth=1.8, markersize=5)
        ax0.plot(cycles, history["Mesenchymal"], label="Mesenchymal",
                 color="#66BB6A", marker="P", linewidth=1.8, markersize=5)
    ax0.fill_between(cycles, history["Stem"],        alpha=0.12, color="#4FC3F7")
    ax0.fill_between(cycles, history["Specialized"], alpha=0.12, color="#FF8A65")
    ax0.set_title("Cell Population Dynamics", color="white", fontsize=12, fontweight="bold")
    ax0.set_xlabel("Time Cycle", color="#B0BEC5", fontsize=10)
    ax0.set_ylabel("Cell Count",  color="#B0BEC5", fontsize=10)
    ax0.legend(fontsize=9, facecolor="#161B22", edgecolor="#30363D", labelcolor="white")

    # ── panel 1: differentiation ratio ──────────────────────────────────
    ax1 = axes[1]
    stem_c = history["Stem"]
    spec_c = history["Specialized"]
    ratio  = [
        sp / (st + sp) if (st + sp) > 0 else 0.0
        for st, sp in zip(stem_c, spec_c)
    ]
    ax1.plot(cycles, ratio, color="#69F0AE", linewidth=2.5)
    ax1.fill_between(cycles, ratio, alpha=0.20, color="#69F0AE")
    ax1.axhline(0.5, color="#FFD54F", linewidth=1.2, linestyle="--",
                label="50 % threshold")
    ax1.set_ylim(0, 1)
    ax1.set_title("Differentiation Ratio", color="white", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Time Cycle",      color="#B0BEC5", fontsize=10)
    ax1.set_ylabel("Specialised / Total", color="#B0BEC5", fontsize=10)
    ax1.legend(fontsize=9, facecolor="#161B22", edgecolor="#30363D", labelcolor="white")

    # ── panel 2: stacked-area ────────────────────────────────────────────
    ax2 = axes[2]
    ax2.stackplot(
        cycles,
        history["Stem"],
        history["Specialized"],
        labels=["Stem", "Specialized"],
        colors=["#4FC3F7", "#FF8A65"],
        alpha=0.75,
    )
    ax2.set_title("Stacked Population", color="white", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Time Cycle", color="#B0BEC5", fontsize=10)
    ax2.set_ylabel("Cell Count",  color="#B0BEC5", fontsize=10)
    ax2.legend(fontsize=9, facecolor="#161B22", edgecolor="#30363D", labelcolor="white")

    # ── panel 3: cumulative deaths bar ──────────────────────────────────
    ax3 = axes[3]
    dead = history["Dead"]
    per_cycle_dead = [dead[0]] + [dead[i] - dead[i-1] for i in range(1, len(dead))]
    colours = ["#EF5350" if d > 0 else "#B0BEC5" for d in per_cycle_dead]
    ax3.bar(cycles, per_cycle_dead, color=colours, alpha=0.85, edgecolor="#0D1117")
    ax3.set_title("Deaths per Cycle", color="white", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Time Cycle",  color="#B0BEC5", fontsize=10)
    ax3.set_ylabel("Deaths",      color="#B0BEC5", fontsize=10)

    # ── figure title ─────────────────────────────────────────────────────
    fig.suptitle(
        "🧬  Stem Cell Regeneration Simulator  ·  Cherry Computer Ltd.",
        color="white", fontsize=14, fontweight="bold", y=0.98,
    )
    _add_watermark(fig)
    plt.tight_layout(rect=[0, 0.0, 1, 0.96])
    _save_or_show(fig, save_path, "Detailed figure")


def _apply_cherry_style(fig: "plt.Figure", ax: "plt.Axes") -> None:
    """Apply the Cherry Computer Ltd. dark theme to an axes object."""
    ax.set_facecolor("#161B22")
    ax.tick_params(colors="#B0BEC5", labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor("#30363D")
    ax.xaxis.label.set_color("#B0BEC5")
    ax.yaxis.label.set_color("#B0BEC5")
    ax.title.set_color("white")
    ax.grid(True, alpha=0.18, linestyle="--", color="#444C56")


def _add_watermark(fig: "plt.Figure") -> None:
    """Add a subtle Cherry Computer Ltd. watermark."""
    fig.text(
        0.99, 0.01,
        "© 2026 Cherry Computer Ltd.",
        ha="right", va="bottom", fontsize=7.5,
        color="#555E6B", style="italic",
        transform=fig.transFigure,
    )


def _save_or_show(fig: "plt.Figure", save_path: Optional[str], label: str) -> None:
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(green(f"  ✔  {label} saved to '{save_path}'."))
    else:
        plt.show()
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Export helpers
# ─────────────────────────────────────────────────────────────────────────────

def export_csv(history: Dict[str, List[int]], filepath: str = "simulation_results.csv") -> None:
    """Export simulation history to a CSV file."""
    keys   = list(history.keys())
    cycles = len(history[keys[0]])
    with open(filepath, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["cycle"] + keys)
        writer.writeheader()
        for i in range(cycles):
            row = {"cycle": i + 1}
            row.update({k: history[k][i] for k in keys})
            writer.writerow(row)
    print(green(f"  ✔  CSV exported to '{filepath}'."))


def export_json(
    history: Dict[str, List[int]],
    filepath: str = "simulation_results.json",
    config:   Optional[SimulationConfig] = None,
) -> None:
    """Export simulation history (and optional config) to JSON."""
    payload: Dict = {
        "meta": {
            "tool":    "Stem Cell Regeneration Simulator v2.0",
            "creator": "Cherry Computer Ltd.",
            "year":    2026,
        },
        "history": history,
    }
    if config:
        payload["config"] = config.__dict__
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(green(f"  ✔  JSON exported to '{filepath}'."))


# ─────────────────────────────────────────────────────────────────────────────
# Scenario runner (multi-run comparison)
# ─────────────────────────────────────────────────────────────────────────────

def run_scenario_comparison(
    scenarios: List[Tuple[str, SimulationConfig]],
    save_path: Optional[str] = None,
) -> None:
    """
    Run multiple named scenarios and produce a comparison plot.

    Parameters
    ----------
    scenarios  : list of (label, SimulationConfig) tuples.
    save_path  : optional file path to save the figure.
    """
    _check_mpl()

    colours = ["#4FC3F7", "#FF8A65", "#69F0AE", "#FFD54F",
               "#CE93D8", "#EF5350", "#4DB6AC", "#FF8F00"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor("#0D1117")
    for ax in axes:
        _apply_cherry_style(fig, ax)

    for idx, (label, cfg) in enumerate(scenarios):
        col = colours[idx % len(colours)]
        h   = simulate_regeneration(
            cycles=cfg.cycles,
            initial_stem_cells=cfg.initial_stem_cells,
            max_cell_age=cfg.max_cell_age,
            differentiation_prob=cfg.differentiation_prob,
            division_prob=cfg.division_prob,
            specialized_death_rate=cfg.specialized_death_rate,
            growth_factor=cfg.growth_factor,
            seed=cfg.seed,
        )
        cyc = list(range(1, cfg.cycles + 1))
        axes[0].plot(cyc, h["Stem"],       label=f"{label} – Stem",        color=col,
                     linewidth=2, linestyle="-")
        axes[1].plot(cyc, h["Specialized"],label=f"{label} – Specialised", color=col,
                     linewidth=2, linestyle="--")

    for ax, ylabel, title in zip(
        axes,
        ["Stem Cell Count", "Specialised Cell Count"],
        ["Stem Cell Dynamics (Scenarios)", "Specialised Cell Dynamics (Scenarios)"],
    ):
        ax.set_xlabel("Time Cycle", color="#B0BEC5")
        ax.set_ylabel(ylabel,       color="#B0BEC5")
        ax.set_title(title, color="white", fontweight="bold")
        ax.legend(fontsize=8, facecolor="#161B22", edgecolor="#30363D", labelcolor="white")

    fig.suptitle(
        "🧬  Scenario Comparison  ·  Cherry Computer Ltd.",
        color="white", fontsize=13, fontweight="bold",
    )
    _add_watermark(fig)
    plt.tight_layout()
    _save_or_show(fig, save_path, "Scenario comparison figure")


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry-point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _print_header()

    # ── Run 1: default single-lineage simulation ─────────────────────────
    print(bold(cyan("  ► Running default simulation (15 cycles, seed=42)…\n")))
    t0      = time.perf_counter()
    results = simulate_regeneration(cycles=15, seed=42, verbose=True)
    elapsed = time.perf_counter() - t0

    print()
    print_table(results)
    _print_summary(results)
    print(dim(f"  Completed in {elapsed*1000:.1f} ms\n"))

    # ── Run 2: multi-lineage demo ────────────────────────────────────────
    print(bold(cyan("  ► Running multi-lineage simulation (20 cycles)…\n")))
    ml_results = simulate_regeneration(
        cycles=20, initial_stem_cells=8,
        multi_lineage=True, growth_factor=1.3,
        seed=7, verbose=True,
    )
    print()
    _print_summary(ml_results)

    # ── Exports ──────────────────────────────────────────────────────────
    export_csv(results,    "simulation_results.csv")
    export_json(results,   "simulation_results.json")

    # ── Scenario comparison ───────────────────────────────────────────────
    scenarios = [
        ("Baseline",      SimulationConfig(cycles=20, seed=1)),
        ("High Division", SimulationConfig(cycles=20, division_prob=0.80, seed=1)),
        ("High Diff.",    SimulationConfig(cycles=20, differentiation_prob=0.80, seed=1)),
        ("Growth Factor", SimulationConfig(cycles=20, growth_factor=1.8, seed=1)),
    ]
    print(bold(cyan("  ► Generating scenario comparison plot…")))
    run_scenario_comparison(scenarios, save_path="scenario_comparison.png")

    # ── Detailed plot ─────────────────────────────────────────────────────
    print(bold(cyan("  ► Generating detailed dashboard plot…")))
    plot_detailed_results(results, save_path="stem_cell_dashboard.png")

    print(cyan("\n  🧬 All done! Cherry Computer Ltd. — Happy Simulating!\n"))
