/**
 * Stem Cell Regeneration Simulator — UI / App Controller
 * Cherry Computer Ltd. © 2026
 */

"use strict";

/* ═══════════════════════════════════════════════════════════════
   Chart.js shared defaults — dark theme
   ═══════════════════════════════════════════════════════════════ */
Chart.defaults.color           = "#8B949E";
Chart.defaults.borderColor     = "#30363D";
Chart.defaults.backgroundColor = "transparent";
Chart.defaults.font.family     = "Inter, system-ui, sans-serif";

/* ═══════════════════════════════════════════════════════════════
   State
   ═══════════════════════════════════════════════════════════════ */
let lastHistory = null;
let lastParams  = {};
const charts    = {};

/* ═══════════════════════════════════════════════════════════════
   Floating particles
   ═══════════════════════════════════════════════════════════════ */
(function spawnParticles() {
  const container = document.getElementById("particles");
  if (!container) return;
  const COLORS = ["#4FC3F7", "#69F0AE", "#FF8A65", "#E91E63", "#CE93D8"];
  const count  = window.innerWidth < 640 ? 15 : 30;
  for (let i = 0; i < count; i++) {
    const el = document.createElement("div");
    el.className = "particle";
    const size = 3 + Math.random() * 6;
    el.style.cssText = `
      width:${size}px; height:${size}px;
      left:${Math.random() * 100}vw;
      background:${COLORS[Math.floor(Math.random() * COLORS.length)]};
      animation-duration:${8 + Math.random() * 14}s;
      animation-delay:${Math.random() * -12}s;
    `;
    container.appendChild(el);
  }
})();

/* ═══════════════════════════════════════════════════════════════
   Hero canvas — animated cell network
   ═══════════════════════════════════════════════════════════════ */
(function heroCanvas() {
  const canvas = document.getElementById("heroCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;

  const TYPES = [
    { color: "#4FC3F7", label: "Stem" },
    { color: "#FF8A65", label: "Specialised" },
    { color: "#69F0AE", label: "New" },
  ];

  const nodes = Array.from({ length: 22 }, (_, i) => ({
    x:    30 + Math.random() * (W - 60),
    y:    30 + Math.random() * (H - 60),
    r:    4 + Math.random() * 7,
    vx:   (Math.random() - .5) * .55,
    vy:   (Math.random() - .5) * .55,
    type: TYPES[Math.floor(Math.random() * TYPES.length)],
    pulse: Math.random() * Math.PI * 2,
  }));

  let frame;
  function draw() {
    ctx.clearRect(0, 0, W, H);

    // connections
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.hypot(dx, dy);
        if (dist < 110) {
          ctx.save();
          ctx.globalAlpha = 0.12 + 0.10 * (1 - dist / 110);
          ctx.strokeStyle = nodes[i].type.color;
          ctx.lineWidth   = 1;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
          ctx.restore();
        }
      }
    }

    // nodes
    for (const n of nodes) {
      n.pulse += 0.045;
      const pulseFactor = 1 + 0.22 * Math.sin(n.pulse);

      // glow
      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 3.5 * pulseFactor);
      grad.addColorStop(0,   n.type.color + "55");
      grad.addColorStop(1,   n.type.color + "00");
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r * 3.5 * pulseFactor, 0, Math.PI * 2);
      ctx.fillStyle = grad;
      ctx.fill();

      // body
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r * pulseFactor, 0, Math.PI * 2);
      ctx.fillStyle = n.type.color;
      ctx.globalAlpha = 0.90;
      ctx.fill();
      ctx.globalAlpha = 1.0;

      // move
      n.x += n.vx; n.y += n.vy;
      if (n.x < n.r || n.x > W - n.r) n.vx *= -1;
      if (n.y < n.r || n.y > H - n.r) n.vy *= -1;
    }

    // watermark
    ctx.fillStyle = "#444C56";
    ctx.font      = "11px Inter";
    ctx.textAlign = "right";
    ctx.fillText("Cherry Computer Ltd.", W - 10, H - 10);

    frame = requestAnimationFrame(draw);
  }
  draw();
})();

/* ═══════════════════════════════════════════════════════════════
   Controls — wire up sliders & toggles
   ═══════════════════════════════════════════════════════════════ */
const sliders = [
  { id: "ctrl-cycles", badge: "val-cycles", fmt: v => v },
  { id: "ctrl-init",   badge: "val-init",   fmt: v => v },
  { id: "ctrl-age",    badge: "val-age",    fmt: v => v },
  { id: "ctrl-div",    badge: "val-div",    fmt: v => `${v}%` },
  { id: "ctrl-diff",   badge: "val-diff",   fmt: v => `${v}%` },
  { id: "ctrl-death",  badge: "val-death",  fmt: v => `${v}%` },
  { id: "ctrl-gf",     badge: "val-gf",     fmt: v => `${(v / 10).toFixed(1)}×` },
  { id: "ctrl-seed",   badge: "val-seed",   fmt: v => (v == 0 ? "random" : v) },
];

sliders.forEach(({ id, badge, fmt }) => {
  const el = document.getElementById(id);
  const bd = document.getElementById(badge);
  if (!el || !bd) return;
  const update = () => {
    bd.textContent = fmt(el.value);
    // update range fill
    const pct = ((el.value - el.min) / (el.max - el.min)) * 100;
    el.style.background = `linear-gradient(to right, var(--accent-blue) ${pct}%, var(--bg-elevated) ${pct}%)`;
  };
  el.addEventListener("input", update);
  update(); // init
});

/* ── Presets ─────────────────────────────────────────────────── */
const PRESETS = {
  balanced:   { cycles: 15, init: 5,  age: 10, div: 60, diff: 50, death: 20, gf: 10, ml: false },
  aggressive: { cycles: 20, init: 8,  age: 8,  div: 80, diff: 35, death: 20, gf: 15, ml: false },
  conserve:   { cycles: 20, init: 3,  age: 15, div: 40, diff: 60, death: 15, gf: 8,  ml: false },
  treatment:  { cycles: 25, init: 6,  age: 12, div: 70, diff: 45, death: 10, gf: 18, ml: true  },
};

document.querySelectorAll(".preset-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const p = PRESETS[btn.dataset.preset];
    if (!p) return;
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) { el.value = val; el.dispatchEvent(new Event("input")); }
    };
    set("ctrl-cycles", p.cycles);
    set("ctrl-init",   p.init);
    set("ctrl-age",    p.age);
    set("ctrl-div",    p.div);
    set("ctrl-diff",   p.diff);
    set("ctrl-death",  p.death);
    set("ctrl-gf",     p.gf);
    document.getElementById("ctrl-multilineage").checked = p.ml;
  });
});

/* ── Tabs ────────────────────────────────────────────────────── */
document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b  => b.classList.remove("active"));
    document.querySelectorAll(".chart-card").forEach(c => c.classList.remove("active"));
    btn.classList.add("active");
    const card = document.getElementById(`tab-${btn.dataset.tab}`);
    if (card) card.classList.add("active");
  });
});

/* ═══════════════════════════════════════════════════════════════
   Chart factory helpers
   ═══════════════════════════════════════════════════════════════ */
const CHART_CFG = {
  animation: { duration: 600, easing: "easeInOutQuart" },
  responsive: true,
  maintainAspectRatio: false,
  interaction: { intersect: false, mode: "index" },
  plugins: {
    legend:  { display: false },
    tooltip: {
      backgroundColor: "#161B22",
      borderColor: "#30363D",
      borderWidth: 1,
      padding: 10,
      titleColor: "#E6EDF3",
      bodyColor: "#8B949E",
    },
  },
  scales: {
    x: {
      grid:  { color: "#21262D" },
      ticks: { color: "#6E7681" },
      title: { display: true, text: "Time Cycle", color: "#6E7681" },
    },
    y: {
      grid:  { color: "#21262D" },
      ticks: { color: "#6E7681" },
      title: { display: true, text: "Cell Count", color: "#6E7681" },
      beginAtZero: true,
    },
  },
};

function makeLabels(n) {
  return Array.from({ length: n }, (_, i) => `Cycle ${i + 1}`);
}

function destroyChart(key) {
  if (charts[key]) { charts[key].destroy(); delete charts[key]; }
}

function buildPopulationChart(history) {
  destroyChart("pop");
  const n   = history.Stem.length;
  const ctx = document.getElementById("chartPopulation").getContext("2d");
  charts["pop"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: makeLabels(n),
      datasets: [
        {
          label: "Stem Cells",
          data: history.Stem,
          borderColor: "#4FC3F7",
          backgroundColor: "rgba(79,195,247,.10)",
          fill: true, tension: 0.38, pointRadius: 4,
          borderWidth: 2.2,
        },
        {
          label: "Specialised",
          data: history.Specialized,
          borderColor: "#FF8A65",
          backgroundColor: "rgba(255,138,101,.10)",
          fill: true, tension: 0.38, pointRadius: 4,
          borderWidth: 2.2,
        },
        ...(history.Hematopoietic.some(v => v > 0) ? [
          { label: "Hematopoietic", data: history.Hematopoietic, borderColor: "#EF5350", tension: 0.38, borderWidth: 1.8, pointRadius: 3 },
          { label: "Neural",        data: history.Neural,        borderColor: "#CE93D8", tension: 0.38, borderWidth: 1.8, pointRadius: 3 },
          { label: "Mesenchymal",   data: history.Mesenchymal,   borderColor: "#66BB6A", tension: 0.38, borderWidth: 1.8, pointRadius: 3 },
        ] : []),
      ],
    },
    options: { ...CHART_CFG, plugins: { ...CHART_CFG.plugins, legend: { display: true, labels: { color: "#8B949E", boxWidth: 12 } } } },
  });
}

function buildRatioChart(history) {
  destroyChart("ratio");
  const n     = history.Stem.length;
  const ratio = history.Stem.map((s, i) => {
    const tot = s + history.Specialized[i];
    return tot > 0 ? +(history.Specialized[i] / tot * 100).toFixed(1) : 0;
  });
  const ctx = document.getElementById("chartRatio").getContext("2d");
  charts["ratio"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: makeLabels(n),
      datasets: [{
        label: "Specialised %",
        data: ratio,
        borderColor: "#69F0AE",
        backgroundColor: "rgba(105,240,174,.12)",
        fill: true, tension: 0.42, pointRadius: 4, borderWidth: 2.5,
      }],
    },
    options: {
      ...CHART_CFG,
      scales: {
        ...CHART_CFG.scales,
        y: {
          ...CHART_CFG.scales.y,
          min: 0, max: 100,
          title: { display: true, text: "Specialised (%)", color: "#6E7681" },
        },
      },
    },
  });
}

function buildStackedChart(history) {
  destroyChart("stacked");
  const n   = history.Stem.length;
  const ctx = document.getElementById("chartStacked").getContext("2d");
  charts["stacked"] = new Chart(ctx, {
    type: "line",
    data: {
      labels: makeLabels(n),
      datasets: [
        { label: "Stem",       data: history.Stem,       borderColor: "#4FC3F7", backgroundColor: "rgba(79,195,247,.55)",  fill: true, tension: 0.38, borderWidth: 1.8, pointRadius: 0 },
        { label: "Specialised",data: history.Specialized,borderColor: "#FF8A65", backgroundColor: "rgba(255,138,101,.50)", fill: true, tension: 0.38, borderWidth: 1.8, pointRadius: 0 },
      ],
    },
    options: {
      ...CHART_CFG,
      plugins: { ...CHART_CFG.plugins, legend: { display: true, labels: { color: "#8B949E", boxWidth: 12 } } },
    },
  });
}

function buildDeathsChart(history) {
  destroyChart("deaths");
  const n         = history.Dead.length;
  const perCycle  = history.Dead.map((d, i) => i === 0 ? d : d - history.Dead[i - 1]);
  const ctx = document.getElementById("chartDeaths").getContext("2d");
  charts["deaths"] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: makeLabels(n),
      datasets: [{
        label: "Deaths",
        data: perCycle,
        backgroundColor: perCycle.map(v => v > 0 ? "rgba(239,83,80,.70)" : "rgba(176,190,197,.25)"),
        borderColor: perCycle.map(v => v > 0 ? "#EF5350" : "#8B949E"),
        borderWidth: 1,
        borderRadius: 3,
      }],
    },
    options: {
      ...CHART_CFG,
      scales: { ...CHART_CFG.scales, y: { ...CHART_CFG.scales.y, title: { display: true, text: "Deaths", color: "#6E7681" } } },
    },
  });
}

/* ═══════════════════════════════════════════════════════════════
   Table builder
   ═══════════════════════════════════════════════════════════════ */
function buildTable(history) {
  const body = document.getElementById("tableBody");
  if (!body) return;
  const n = history.Stem.length;
  const rows = [];
  for (let i = 0; i < n; i++) {
    const s   = history.Stem[i];
    const sp  = history.Specialized[i];
    const tot = history.Total[i];
    const d   = history.Dead[i];
    const prevDead = i === 0 ? 0 : history.Dead[i - 1];
    const thisDead = d - prevDead;
    const ratio = tot > 0 ? ((sp / tot) * 100).toFixed(1) + "%" : "—";
    rows.push(`<tr>
      <td>${i + 1}</td>
      <td>${s}</td>
      <td>${sp}</td>
      <td>${tot}</td>
      <td>${thisDead}</td>
      <td>${ratio}</td>
    </tr>`);
  }
  body.innerHTML = rows.join("");
}

/* ═══════════════════════════════════════════════════════════════
   Stats bar updater
   ═══════════════════════════════════════════════════════════════ */
function animateNumber(el, target, duration = 700) {
  const start    = parseInt(el.textContent) || 0;
  const startT   = performance.now();
  function step(now) {
    const p   = Math.min((now - startT) / duration, 1);
    const cur = Math.round(start + (target - start) * (1 - Math.pow(1 - p, 3)));
    el.textContent = cur;
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function updateStatsBar(history) {
  const n    = history.Stem.length;
  const stem = history.Stem[n - 1];
  const spec = history.Specialized[n - 1];
  const tot  = history.Total[n - 1];
  const dead = history.Dead[n - 1];
  const ratio = tot > 0 ? ((spec / tot) * 100).toFixed(1) + "%" : "—";

  animateNumber(document.getElementById("stat-cycles"), n);
  animateNumber(document.getElementById("stat-stem"),   stem);
  animateNumber(document.getElementById("stat-spec"),   spec);
  animateNumber(document.getElementById("stat-dead"),   dead);
  document.getElementById("stat-ratio").textContent = ratio;
}

/* ═══════════════════════════════════════════════════════════════
   Animated simulation runner (step-by-step visual)
   ═══════════════════════════════════════════════════════════════ */
function runWithAnimation(params) {
  // Run full simulation first for full results
  const full = simulateRegeneration(params);
  const n    = full.Stem.length;

  let step = 0;
  const partial = {};
  Object.keys(full).forEach(k => (partial[k] = []));

  function advance() {
    if (step >= n) {
      lastHistory = full;
      buildTable(full);
      updateStatsBar(full);
      return;
    }
    Object.keys(full).forEach(k => partial[k].push(full[k][step]));
    step++;

    // refresh charts incrementally
    if (charts["pop"]) {
      const ds = charts["pop"].data.datasets;
      ds[0].data = partial.Stem;
      ds[1].data = partial.Specialized;
      charts["pop"].data.labels = makeLabels(step);
      charts["pop"].update("none");
    }

    updateStatsBar(partial);
    setTimeout(advance, 90);
  }

  // initialise charts with empty data before animating
  buildPopulationChart({ Stem: [], Specialized: [], Hematopoietic: [], Neural: [], Mesenchymal: [] });
  buildRatioChart(full);
  buildStackedChart(full);
  buildDeathsChart(full);
  advance();
}

/* ═══════════════════════════════════════════════════════════════
   Main run function
   ═══════════════════════════════════════════════════════════════ */
function getParams() {
  const g  = id => document.getElementById(id);
  const iv = id => parseInt(g(id).value, 10);
  const fv = id => parseFloat(g(id).value);

  return {
    cycles:               iv("ctrl-cycles"),
    initialStemCells:     iv("ctrl-init"),
    maxCellAge:           iv("ctrl-age"),
    divisionProb:         fv("ctrl-div")    / 100,
    differentiationProb:  fv("ctrl-diff")   / 100,
    specializedDeathRate: fv("ctrl-death")  / 100,
    growthFactor:         fv("ctrl-gf")     / 10,
    multiLineage:         g("ctrl-multilineage").checked,
    seed:                 iv("ctrl-seed"),
  };
}

function runSimulation() {
  const params  = getParams();
  lastParams    = params;
  const animate = document.getElementById("ctrl-animate").checked;

  if (animate) {
    runWithAnimation(params);
  } else {
    lastHistory = simulateRegeneration(params);
    buildPopulationChart(lastHistory);
    buildRatioChart(lastHistory);
    buildStackedChart(lastHistory);
    buildDeathsChart(lastHistory);
    buildTable(lastHistory);
    updateStatsBar(lastHistory);
  }
}

function resetAll() {
  // Reset sliders to defaults
  const defaults = { "ctrl-cycles": 15, "ctrl-init": 5, "ctrl-age": 10,
                     "ctrl-div": 60, "ctrl-diff": 50, "ctrl-death": 20,
                     "ctrl-gf": 10, "ctrl-seed": 42 };
  for (const [id, val] of Object.entries(defaults)) {
    const el = document.getElementById(id);
    if (el) { el.value = val; el.dispatchEvent(new Event("input")); }
  }
  document.getElementById("ctrl-multilineage").checked = false;
  document.getElementById("ctrl-animate").checked      = true;

  // Clear charts & table
  ["pop","ratio","stacked","deaths"].forEach(k => destroyChart(k));
  document.getElementById("tableBody").innerHTML =
    '<tr><td colspan="6" class="empty-row">Run the simulation to see data.</td></tr>';

  // Reset stats
  ["stat-cycles","stat-stem","stat-spec","stat-dead"].forEach(id => {
    document.getElementById(id).textContent = "0";
  });
  document.getElementById("stat-ratio").textContent = "—";

  lastHistory = null;
}

/* ═══════════════════════════════════════════════════════════════
   Event listeners
   ═══════════════════════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {

  document.getElementById("btn-run").addEventListener("click", runSimulation);
  document.getElementById("btn-reset").addEventListener("click", resetAll);

  document.getElementById("btn-csv").addEventListener("click", () => {
    if (!lastHistory) return alert("Run the simulation first.");
    downloadFile(exportCSV(lastHistory), "stem_cell_results.csv", "text/csv");
  });

  document.getElementById("btn-json").addEventListener("click", () => {
    if (!lastHistory) return alert("Run the simulation first.");
    downloadFile(exportJSON(lastHistory, lastParams), "stem_cell_results.json", "application/json");
  });

  // Auto-run on page load with default parameters
  setTimeout(runSimulation, 400);
});
