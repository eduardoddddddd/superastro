/* SuperAstro — Shared utilities */

// ─── API helpers ───────────────────────────────────────────────
const API = {
  async post(path, data) {
    const res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Error del servidor');
    return json;
  },
  async get(path) {
    const res = await fetch(path);
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Error del servidor');
    return json;
  },
  async del(path) {
    const res = await fetch(path, { method: 'DELETE' });
    const json = await res.json();
    if (!res.ok) throw new Error(json.detail || 'Error del servidor');
    return json;
  },
};

// ─── City autocomplete ────────────────────────────────────────
function initCitySearch(inputId, resultsId, onSelect) {
  const input = document.getElementById(inputId);
  const results = document.getElementById(resultsId);
  let debounceTimer;

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = input.value.trim();
    if (q.length < 2) { results.classList.remove('open'); return; }
    debounceTimer = setTimeout(async () => {
      try {
        const data = await API.get(`/api/cities/search?q=${encodeURIComponent(q)}`);
        results.innerHTML = '';
        if (!data.cities.length) {
          results.innerHTML = '<div class="autocomplete-item" style="color:var(--text-dim)">Sin resultados</div>';
        } else {
          data.cities.forEach(city => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.innerHTML = `<div>${city.display}</div><div class="city-tz">${city.timezone} · ${city.lat.toFixed(2)}, ${city.lon.toFixed(2)}</div>`;
            item.addEventListener('click', () => {
              input.value = city.display;
              results.classList.remove('open');
              onSelect(city);
            });
            results.appendChild(item);
          });
        }
        results.classList.add('open');
      } catch (e) {
        console.error('City search error:', e);
      }
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.classList.remove('open');
    }
  });
}

// ─── Tabs ─────────────────────────────────────────────────────
function initTabs(containerSel) {
  const container = document.querySelector(containerSel);
  if (!container) return;
  const buttons = container.querySelectorAll('.tab-btn');
  const panels = container.querySelectorAll('.tab-panel');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');
    });
  });
}

// ─── Aspect CSS class ─────────────────────────────────────────
function aspectClass(name) {
  const map = {
    'Conjunción': 'asp-conjuncion',
    'Sextil':     'asp-sextil',
    'Trígono':    'asp-trigono',
    'Cuadratura': 'asp-cuadratura',
    'Oposición':  'asp-oposicion',
  };
  return map[name] || '';
}

// ─── Dignity CSS class ────────────────────────────────────────
function dignityClass(d) {
  const map = {
    'Domicilio': 'dignity-domicilio',
    'Exaltación': 'dignity-exaltacion',
    'Detrimento': 'dignity-detrimento',
    'Caída': 'dignity-caida',
    'Peregrino': 'dignity-peregrino',
  };
  return map[d] || '';
}

// ─── Planet glyph fallbacks ───────────────────────────────────
const PLANET_SYMBOLS = {
  'Sol': '☉', 'Luna': '☽', 'Mercurio': '☿', 'Venus': '♀', 'Marte': '♂',
  'Júpiter': '♃', 'Saturno': '♄', 'Urano': '⛢', 'Neptuno': '♆',
  'Plutón': '♇', 'Nodo Norte': '☊',
};
const SIGN_SYMBOLS = {
  'Aries': '♈', 'Tauro': '♉', 'Géminis': '♊', 'Cáncer': '♋',
  'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Escorpio': '♏',
  'Sagitario': '♐', 'Capricornio': '♑', 'Acuario': '♒', 'Piscis': '♓',
};

// ─── Render planet table ──────────────────────────────────────
function renderPlanetTable(planets, containerId, getDignity) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = `
    <table class="planet-table">
      <thead>
        <tr>
          <th>Planeta</th>
          <th>Posición</th>
          <th>Casa</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody>
        ${planets.map(p => {
          const dignity = getDignity ? getDignity(p.name, p.sign) : '';
          const retro = p.retrograde ? ' <span class="retro">℞</span>' : '';
          return `<tr>
            <td>${p.name}${retro}</td>
            <td style="color:var(--text-dim)">${p.position_str}</td>
            <td>Casa ${p.house}</td>
            <td class="${dignityClass(dignity)}">${dignity}</td>
          </tr>`;
        }).join('')}
      </tbody>
    </table>
  `;
}

// ─── Render aspects list ──────────────────────────────────────
function renderAspects(aspects, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (!aspects.length) {
    container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">✦</div><p>Sin aspectos principales</p></div>';
    return;
  }
  container.innerHTML = aspects.map(a => `
    <div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid rgba(42,42,85,0.5)">
      <span style="min-width:80px;font-size:13px">${a.planet1}</span>
      <span class="aspect-badge ${aspectClass(a.aspect_name)}">${a.aspect_name}</span>
      <span style="min-width:80px;font-size:13px">${a.planet2}</span>
      <span style="color:var(--text-dim);font-size:12px;margin-left:auto">orb ${a.orb}°</span>
    </div>
  `).join('');
}

// ─── Render interpretations ───────────────────────────────────
function renderInterpretations(interpretations, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (!interpretations || !interpretations.length) {
    container.innerHTML = '<div class="empty-state"><p>Sin interpretaciones disponibles</p></div>';
    return;
  }
  container.innerHTML = interpretations.map((item, i) => `
    <div class="interp-section ${i < 2 ? 'highlight' : ''}">
      <div class="interp-title">${item[0]}</div>
      <div class="interp-body">${item[1]}</div>
    </div>
  `).join('');
}

// ─── SVG Chart Wheel ─────────────────────────────────────────
const SIGN_COLORS_ELEMENT = {
  'Aries':      '#ff6b4a', 'Leo':       '#ff9f1c', 'Sagitario': '#ffcf3d',  // Fuego
  'Tauro':      '#7ec850', 'Virgo':     '#4ade80', 'Capricornio':'#34d399', // Tierra
  'Géminis':    '#60a5fa', 'Libra':     '#818cf8', 'Acuario':   '#a78bfa',  // Aire
  'Cáncer':     '#38bdf8', 'Escorpio':  '#6366f1', 'Piscis':    '#8b5cf6',  // Agua
};
const SIGN_ORDER = ['Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
                    'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis'];
const ASPECT_COLORS = {
  'Conjunción': '#94a3b8', 'Sextil': '#34d399', 'Trígono': '#60a5fa',
  'Cuadratura': '#f87171', 'Oposición': '#f472b6',
};
const PLANET_ABBR = {
  'Sol':'Sol', 'Luna':'Lun', 'Mercurio':'Mer', 'Venus':'Ven', 'Marte':'Mar',
  'Júpiter':'Jup', 'Saturno':'Sat', 'Urano':'Ura', 'Neptuno':'Nep',
  'Plutón':'Plu', 'Nodo Norte':'NN',
};

function lonToAngle(lon, asc) {
  // ASC en izquierda (180°), avanza antihorario en SVG = horario en cielo
  return (180 - (lon - asc) + 360) % 360;
}

function polarToXY(cx, cy, r, angleDeg) {
  const rad = (angleDeg - 90) * Math.PI / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

function svgArc(cx, cy, r, startAngle, endAngle) {
  const s = polarToXY(cx, cy, r, startAngle);
  const e = polarToXY(cx, cy, r, endAngle);
  const large = (endAngle - startAngle + 360) % 360 > 180 ? 1 : 0;
  return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
}

function drawChartWheel(svgEl, chartData, transitData = null) {
  const size = svgEl.viewBox.baseVal.width || 600;
  const cx = size / 2, cy = size / 2;
  const R = size * 0.46;  // outer ring

  const R_SIGN_IN  = R * 0.86;
  const R_HOUSE    = R * 0.80;
  const R_PLANET   = R * 0.70;
  const R_TRANSIT  = R * 0.55;
  const R_ASPECT   = R * 0.48;
  const R_CENTER   = R * 0.48;

  const asc = chartData.ascendant;
  const cusps = chartData.cusps;

  // clear
  svgEl.innerHTML = '';

  const ns = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, text) {
    const e = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (text !== undefined) e.textContent = text;
    return e;
  }

  // ── Background
  svgEl.appendChild(el('circle', { cx, cy, r: R, fill: '#0d0d1e', stroke: '#2a2a55', 'stroke-width': '1' }));

  // ── Sign ring sectors (R → R_SIGN_IN)
  for (let i = 0; i < 12; i++) {
    const signLon = i * 30;
    const startA = lonToAngle(signLon, asc);
    const endA   = lonToAngle(signLon + 30, asc);
    const color  = SIGN_COLORS_ELEMENT[SIGN_ORDER[i]];

    // Pie sector using path
    const s1 = polarToXY(cx, cy, R, startA);
    const s2 = polarToXY(cx, cy, R, endA);
    const s3 = polarToXY(cx, cy, R_SIGN_IN, endA);
    const s4 = polarToXY(cx, cy, R_SIGN_IN, startA);
    const large = 0; // each sector is 30°
    const path = `M ${cx} ${cy} L ${s1.x} ${s1.y} A ${R} ${R} 0 0 1 ${s2.x} ${s2.y} L ${cx} ${cy}`;
    // Better: proper annular sector
    const sector = el('path', {
      d: `M ${s1.x} ${s1.y} A ${R} ${R} 0 0 1 ${s2.x} ${s2.y} L ${s3.x} ${s3.y} A ${R_SIGN_IN} ${R_SIGN_IN} 0 0 0 ${s4.x} ${s4.y} Z`,
      fill: color + '33',
      stroke: '#1a1a35',
      'stroke-width': '0.5',
    });
    svgEl.appendChild(sector);

    // Sign abbreviation at middle of sector
    const midA = (startA + endA) / 2;
    const midR = (R + R_SIGN_IN) / 2;
    const mp   = polarToXY(cx, cy, midR, midA);
    const abbr = SIGN_ORDER[i].slice(0, 2).toUpperCase();
    svgEl.appendChild(el('text', {
      x: mp.x, y: mp.y + 4,
      'text-anchor': 'middle', fill: color, 'font-size': size * 0.022,
      'font-weight': '600', 'font-family': 'Inter, sans-serif',
    }, abbr));
  }

  // ── Sign ring border circles
  svgEl.appendChild(el('circle', { cx, cy, r: R, fill: 'none', stroke: '#3a3a66', 'stroke-width': '1.5' }));
  svgEl.appendChild(el('circle', { cx, cy, r: R_SIGN_IN, fill: 'none', stroke: '#2a2a55', 'stroke-width': '1' }));

  // ── House cusps lines + numbers
  for (let i = 0; i < 12; i++) {
    const a = lonToAngle(cusps[i], asc);
    const pOuter = polarToXY(cx, cy, R_SIGN_IN, a);
    const pInner = polarToXY(cx, cy, R_CENTER + 4, a);

    const isAngular = [0, 3, 6, 9].includes(i);
    svgEl.appendChild(el('line', {
      x1: pInner.x, y1: pInner.y,
      x2: pOuter.x, y2: pOuter.y,
      stroke: isAngular ? '#a78bfa' : '#2a2a55',
      'stroke-width': isAngular ? '1.5' : '0.8',
      'stroke-dasharray': isAngular ? '' : '3,4',
    }));

    // House number between cusps
    const nextA  = lonToAngle(cusps[(i + 1) % 12], asc);
    const midA2  = midAngle(a, nextA);
    const numPt  = polarToXY(cx, cy, R_HOUSE, midA2);
    svgEl.appendChild(el('text', {
      x: numPt.x, y: numPt.y + 4,
      'text-anchor': 'middle', fill: '#4a4a7a', 'font-size': size * 0.018,
      'font-family': 'Inter, sans-serif',
    }, String(i + 1)));
  }

  // ── Inner fill circle
  svgEl.appendChild(el('circle', { cx, cy, r: R_CENTER, fill: '#0a0a14', stroke: '#2a2a55', 'stroke-width': '1' }));

  // ── Aspect lines (inside R_CENTER)
  for (const asp of (chartData.aspects || [])) {
    const p1 = chartData.planets.find(p => p.name === asp.planet1);
    const p2 = chartData.planets.find(p => p.name === asp.planet2);
    if (!p1 || !p2) continue;
    const a1 = lonToAngle(p1.longitude, asc);
    const a2 = lonToAngle(p2.longitude, asc);
    const pt1 = polarToXY(cx, cy, R_ASPECT, a1);
    const pt2 = polarToXY(cx, cy, R_ASPECT, a2);
    const color = ASPECT_COLORS[asp.aspect_name] || '#555';
    svgEl.appendChild(el('line', {
      x1: pt1.x, y1: pt1.y,
      x2: pt2.x, y2: pt2.y,
      stroke: color, 'stroke-width': '0.8', 'stroke-opacity': '0.5',
    }));
  }

  // ── Natal planets
  const natalPlaced = placePlanets(chartData.planets, asc);
  for (const { planet, displayAngle } of natalPlaced) {
    const pt = polarToXY(cx, cy, R_PLANET, displayAngle);
    const abbr = PLANET_ABBR[planet.name] || planet.name.slice(0, 3);
    const retro = planet.retrograde ? '℞' : '';

    // small dot on exact position
    const exactPt = polarToXY(cx, cy, R_PLANET - 8, lonToAngle(planet.longitude, asc));
    svgEl.appendChild(el('circle', { cx: exactPt.x, cy: exactPt.y, r: 2, fill: '#a78bfa' }));

    // line from dot to label if spread
    const labelPt = polarToXY(cx, cy, R_PLANET, displayAngle);
    svgEl.appendChild(el('line', {
      x1: exactPt.x, y1: exactPt.y,
      x2: labelPt.x, y2: labelPt.y,
      stroke: '#3a3a66', 'stroke-width': '0.5',
    }));

    // label background
    const bg = el('rect', {
      x: labelPt.x - 14, y: labelPt.y - 8,
      width: 28, height: 16, rx: 4,
      fill: '#12122a', stroke: '#3a3a66', 'stroke-width': '0.5',
    });
    svgEl.appendChild(bg);
    svgEl.appendChild(el('text', {
      x: labelPt.x, y: labelPt.y + 4,
      'text-anchor': 'middle', fill: planet.retrograde ? '#f87171' : '#e2e8f0',
      'font-size': size * 0.022, 'font-family': 'Inter, sans-serif', 'font-weight': '600',
    }, abbr + retro));
  }

  // ── Transit planets (if any)
  if (transitData) {
    const transitPlaced = placePlanets(transitData.transit_planets, asc);
    for (const { planet, displayAngle } of transitPlaced) {
      const pt = polarToXY(cx, cy, R_TRANSIT, displayAngle);
      const abbr = PLANET_ABBR[planet.name] || planet.name.slice(0, 3);
      svgEl.appendChild(el('circle', { cx: pt.x, cy: pt.y, r: 2, fill: '#34d399' }));
      const bg = el('rect', {
        x: pt.x - 13, y: pt.y - 7, width: 26, height: 14, rx: 3,
        fill: '#0a2818', stroke: '#1a5c38', 'stroke-width': '0.5',
      });
      svgEl.appendChild(bg);
      svgEl.appendChild(el('text', {
        x: pt.x, y: pt.y + 4,
        'text-anchor': 'middle', fill: '#34d399',
        'font-size': size * 0.020, 'font-family': 'Inter, sans-serif', 'font-weight': '600',
      }, abbr));
    }
  }

  // ── ASC label
  const ascPt = polarToXY(cx, cy, R + 16, lonToAngle(asc, asc));
  svgEl.appendChild(el('text', {
    x: ascPt.x, y: ascPt.y + 4,
    'text-anchor': 'middle', fill: '#a78bfa', 'font-size': size * 0.022,
    'font-family': 'Inter, sans-serif', 'font-weight': '700',
  }, 'ASC'));

  // ── MC label
  const mcPt = polarToXY(cx, cy, R + 16, lonToAngle(chartData.mc, asc));
  svgEl.appendChild(el('text', {
    x: mcPt.x, y: mcPt.y + 4,
    'text-anchor': 'middle', fill: '#fbbf24', 'font-size': size * 0.022,
    'font-family': 'Inter, sans-serif', 'font-weight': '700',
  }, 'MC'));
}

function midAngle(a, b) {
  // Returns midpoint angle handling wraparound
  if (b < a) b += 360;
  const mid = (a + b) / 2;
  return mid % 360;
}

function placePlanets(planets, asc) {
  const MIN_GAP = 14;
  const placed = planets.map(p => ({
    planet: p,
    exactAngle: lonToAngle(p.longitude, asc),
    displayAngle: lonToAngle(p.longitude, asc),
  }));

  // Simple spread: sort by exact angle, then push apart if too close
  placed.sort((a, b) => a.exactAngle - b.exactAngle);
  let changed = true;
  for (let iter = 0; iter < 20 && changed; iter++) {
    changed = false;
    for (let i = 0; i < placed.length; i++) {
      const next = placed[(i + 1) % placed.length];
      let diff = (next.displayAngle - placed[i].displayAngle + 360) % 360;
      if (diff < MIN_GAP && diff !== 0) {
        const push = (MIN_GAP - diff) / 2;
        placed[i].displayAngle = (placed[i].displayAngle - push + 360) % 360;
        next.displayAngle = (next.displayAngle + push) % 360;
        changed = true;
      }
    }
  }
  return placed;
}

// ─── Date helpers ─────────────────────────────────────────────
function fillDateTimeNow() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  document.getElementById('year').value  = now.getFullYear();
  document.getElementById('month').value = pad(now.getMonth() + 1);
  document.getElementById('day').value   = pad(now.getDate());
  document.getElementById('hour').value  = pad(now.getHours());
  document.getElementById('minute').value = pad(now.getMinutes());
}

// Expose globally
window.API = API;
window.initCitySearch = initCitySearch;
window.initTabs = initTabs;
window.renderPlanetTable = renderPlanetTable;
window.renderAspects = renderAspects;
window.renderInterpretations = renderInterpretations;
window.drawChartWheel = drawChartWheel;
window.aspectClass = aspectClass;
window.fillDateTimeNow = fillDateTimeNow;
window.PLANET_ABBR = PLANET_ABBR;
window.SIGN_SYMBOLS = SIGN_SYMBOLS;
