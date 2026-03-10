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
      } catch (e) { console.error('City search error:', e); }
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !results.contains(e.target))
      results.classList.remove('open');
  });
}

// ─── Tabs ─────────────────────────────────────────────────────
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabsBar = btn.parentElement;
      const card    = tabsBar.parentElement;
      tabsBar.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      card.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(btn.dataset.tab);
      if (target) target.classList.add('active');
    });
  });
}

// ─── Aspect CSS class ─────────────────────────────────────────
function aspectClass(name) {
  const map = {
    'Conjunción': 'asp-conjuncion', 'Sextil':     'asp-sextil',
    'Trígono':    'asp-trigono',    'Cuadratura': 'asp-cuadratura',
    'Oposición':  'asp-oposicion',
  };
  return map[name] || '';
}

// ─── Dignity CSS class ────────────────────────────────────────
function dignityClass(d) {
  const map = {
    'Domicilio':  'dignity-domicilio',  'Exaltación': 'dignity-exaltacion',
    'Detrimento': 'dignity-detrimento', 'Caída':      'dignity-caida',
    'Peregrino':  'dignity-peregrino',
  };
  return map[d] || '';
}

// ─── Astrological symbols ─────────────────────────────────────
const PLANET_ABBR = {
  'Sol':'☉', 'Luna':'☽', 'Mercurio':'☿', 'Venus':'♀', 'Marte':'♂',
  'Júpiter':'♃', 'Saturno':'♄', 'Urano':'♅', 'Neptuno':'♆',
  'Plutón':'♇', 'Nodo Norte':'☊',
};
const SIGN_GLYPHS = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];
const SIGN_SYMBOLS = {
  'Aries':'♈','Tauro':'♉','Géminis':'♊','Cáncer':'♋','Leo':'♌','Virgo':'♍',
  'Libra':'♎','Escorpio':'♏','Sagitario':'♐','Capricornio':'♑','Acuario':'♒','Piscis':'♓',
};
const SIGN_ORDER = [
  'Aries','Tauro','Géminis','Cáncer','Leo','Virgo',
  'Libra','Escorpio','Sagitario','Capricornio','Acuario','Piscis',
];

// Element colors (vibrant, work on light bg)
const SIGN_COLORS_ELEMENT = {
  'Aries':      '#ef4444', 'Leo':         '#f97316', 'Sagitario':  '#eab308',
  'Tauro':      '#16a34a', 'Virgo':       '#059669', 'Capricornio':'#0d9488',
  'Géminis':    '#3b82f6', 'Libra':       '#6366f1', 'Acuario':    '#8b5cf6',
  'Cáncer':     '#0ea5e9', 'Escorpio':    '#4f46e5', 'Piscis':     '#7c3aed',
};
const ASPECT_COLORS = {
  'Conjunción': '#94a3b8', 'Sextil': '#16a34a', 'Trígono': '#3b82f6',
  'Cuadratura': '#ef4444', 'Oposición': '#7c3aed',
};
// Symbol font stack for cross-platform rendering
const SYM_FONT = "'Segoe UI Symbol','Apple Symbols','Arial Unicode MS',sans-serif";

// ─── Render planet table ──────────────────────────────────────
function renderPlanetTable(planets, containerId, getDignity) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = `
    <table class="planet-table">
      <thead>
        <tr><th>Planeta</th><th>Posición</th><th>Casa</th><th>Estado</th></tr>
      </thead>
      <tbody>
        ${planets.map(p => {
          const dignity = getDignity ? getDignity(p.name, p.sign) : '';
          const glyph = PLANET_ABBR[p.name] || '';
          const retro = p.retrograde ? ' <span class="retro">℞</span>' : '';
          return `<tr>
            <td><span style="font-family:${SYM_FONT};font-size:15px;margin-right:5px;color:var(--accent)">${glyph}</span>${p.name}${retro}</td>
            <td style="color:var(--text-dim)">${p.position_str}</td>
            <td>${p.house}</td>
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
    <div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(226,223,245,0.8)">
      <span style="min-width:70px;font-size:12px;display:flex;align-items:center;gap:4px">
        <span style="font-family:${SYM_FONT};color:var(--accent)">${PLANET_ABBR[a.planet1]||''}</span>${a.planet1}
      </span>
      <span class="aspect-badge ${aspectClass(a.aspect_name)}">${a.aspect_name}</span>
      <span style="min-width:70px;font-size:12px;display:flex;align-items:center;gap:4px">
        <span style="font-family:${SYM_FONT};color:var(--accent)">${PLANET_ABBR[a.planet2]||''}</span>${a.planet2}
      </span>
      <span style="color:var(--text-dim);font-size:11px;margin-left:auto">orb ${a.orb}°</span>
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

// ─── Chart geometry helpers ───────────────────────────────────
function lonToAngle(lon, asc) {
  // ASC queda a la izquierda (270°), convención estándar occidental
  return (270 - (lon - asc) + 360) % 360;
}
function polarToXY(cx, cy, r, angleDeg) {
  const rad = (angleDeg - 90) * Math.PI / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}
function midAngle(a, b) {
  // Toma siempre el arco más corto entre dos ángulos
  const diff = (b - a + 360) % 360;
  if (diff <= 180) {
    return (a + diff / 2) % 360;
  } else {
    return (a - (360 - diff) / 2 + 360) % 360;
  }
}
function placePlanets(planets, asc) {
  const MIN_GAP = 22;
  const placed = planets.map(p => ({
    planet: p,
    exactAngle: lonToAngle(p.longitude, asc),
    displayAngle: lonToAngle(p.longitude, asc),
    tier: 0, // 0 = anillo exterior, 1 = anillo interior
  }));
  placed.sort((a, b) => a.exactAngle - b.exactAngle);

  // Separar planetas en el mismo arco
  let changed = true;
  for (let iter = 0; iter < 50 && changed; iter++) {
    changed = false;
    for (let i = 0; i < placed.length; i++) {
      const next = placed[(i + 1) % placed.length];
      let diff = (next.displayAngle - placed[i].displayAngle + 360) % 360;
      if (diff < MIN_GAP && diff !== 0) {
        const push = (MIN_GAP - diff) / 2;
        placed[i].displayAngle  = (placed[i].displayAngle - push + 360) % 360;
        next.displayAngle = (next.displayAngle + push) % 360;
        changed = true;
      }
    }
  }

  // Asignar tier: planetas desplazados >9° de su posición exacta van al anillo interior
  for (const p of placed) {
    const drift = Math.abs((p.displayAngle - p.exactAngle + 540) % 360 - 180);
    p.tier = drift > 9 ? 1 : 0;
  }

  return placed;
}

// ─── Draw empty wheel (placeholder) ──────────────────────────
function drawEmptyWheel(svgEl) {
  const size = svgEl.viewBox ? (svgEl.viewBox.baseVal.width || 600) : 600;
  const cx = size / 2, cy = size / 2;
  const R = size * 0.46;
  const R_SIGN_IN = R * 0.83;
  const R_INNER   = R * 0.63;
  const R_CENTER  = R * 0.43;

  svgEl.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, text) {
    const e = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (text !== undefined) e.textContent = text;
    return e;
  }

  // Background
  svgEl.appendChild(el('circle', { cx, cy, r: R, fill: '#f8f6ff', stroke: '#ddd9f5', 'stroke-width': '1.5' }));

  // 12 sign sectors (Aries at top, clockwise)
  for (let i = 0; i < 12; i++) {
    const startA = i * 30;
    const endA   = (i + 1) * 30;
    const color  = SIGN_COLORS_ELEMENT[SIGN_ORDER[i]];
    const s1 = polarToXY(cx, cy, R,        startA);
    const s2 = polarToXY(cx, cy, R,        endA);
    const s3 = polarToXY(cx, cy, R_SIGN_IN, endA);
    const s4 = polarToXY(cx, cy, R_SIGN_IN, startA);
    svgEl.appendChild(el('path', {
      d: `M ${s1.x} ${s1.y} A ${R} ${R} 0 0 1 ${s2.x} ${s2.y} L ${s3.x} ${s3.y} A ${R_SIGN_IN} ${R_SIGN_IN} 0 0 0 ${s4.x} ${s4.y} Z`,
      fill: color + '22', stroke: '#ece8f8', 'stroke-width': '0.5',
    }));
    // Glyph
    const midA = (startA + endA) / 2;
    const mp   = polarToXY(cx, cy, (R + R_SIGN_IN) / 2, midA);
    svgEl.appendChild(el('text', {
      x: mp.x, y: mp.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
      fill: color, 'font-size': size * 0.036, 'font-family': SYM_FONT,
    }, SIGN_GLYPHS[i]));
  }

  // Ring borders
  svgEl.appendChild(el('circle', { cx, cy, r: R,        fill: 'none', stroke: '#cec9ec', 'stroke-width': '1.5' }));
  svgEl.appendChild(el('circle', { cx, cy, r: R_SIGN_IN, fill: 'none', stroke: '#ddd9f2', 'stroke-width': '1' }));
  // Inner zone
  svgEl.appendChild(el('circle', { cx, cy, r: R_INNER,  fill: '#ffffff', stroke: '#e8e4f5', 'stroke-width': '1' }));
  svgEl.appendChild(el('circle', { cx, cy, r: R_CENTER, fill: '#f8f6ff', stroke: '#e0dbf5', 'stroke-width': '1' }));
  // Center text
  svgEl.appendChild(el('text', {
    x: cx, y: cy - 10, 'text-anchor': 'middle', 'dominant-baseline': 'central',
    fill: '#c4bfe0', 'font-size': size * 0.028, 'font-family': "'Inter',sans-serif", 'font-weight': '700',
  }, '✦ SuperAstro'));
  svgEl.appendChild(el('text', {
    x: cx, y: cy + 14, 'text-anchor': 'middle', 'dominant-baseline': 'central',
    fill: '#d0cae8', 'font-size': size * 0.018, 'font-family': "'Inter',sans-serif",
  }, 'Calcula para ver la rueda'));
}

// ─── Draw full chart wheel ────────────────────────────────────
function drawChartWheel(svgEl, chartData, transitData = null) {
  const size = svgEl.viewBox ? (svgEl.viewBox.baseVal.width || 600) : 600;
  const cx = size / 2, cy = size / 2;
  const R          = size * 0.46;
  const R_SIGN_IN  = R * 0.83;
  const R_HOUSE    = R * 0.73;
  const R_TRANSIT  = R * 0.51;
  const R_ASPECT   = R * 0.42;
  const R_CENTER   = R * 0.40;

  const asc   = chartData.ascendant;
  const cusps = chartData.cusps;

  svgEl.innerHTML = '';
  const ns = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, text) {
    const e = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (text !== undefined) e.textContent = text;
    return e;
  }

  // ── Background
  svgEl.appendChild(el('circle', { cx, cy, r: R, fill: '#f8f6ff', stroke: '#ddd9f5', 'stroke-width': '1.5' }));

  // ── Sign ring sectors
  for (let i = 0; i < 12; i++) {
    const signLon = i * 30;
    const startA  = lonToAngle(signLon, asc);
    const endA    = lonToAngle(signLon + 30, asc);
    const color   = SIGN_COLORS_ELEMENT[SIGN_ORDER[i]];
    const s1 = polarToXY(cx, cy, R,        startA);
    const s2 = polarToXY(cx, cy, R,        endA);
    const s3 = polarToXY(cx, cy, R_SIGN_IN, endA);
    const s4 = polarToXY(cx, cy, R_SIGN_IN, startA);
    svgEl.appendChild(el('path', {
      d: `M ${s1.x} ${s1.y} A ${R} ${R} 0 0 1 ${s2.x} ${s2.y} L ${s3.x} ${s3.y} A ${R_SIGN_IN} ${R_SIGN_IN} 0 0 0 ${s4.x} ${s4.y} Z`,
      fill: color + '28', stroke: '#eae6f8', 'stroke-width': '0.5',
    }));
    // Unicode sign glyph
    const midA = midAngle(startA, endA);
    const mp   = polarToXY(cx, cy, (R + R_SIGN_IN) / 2, midA);
    svgEl.appendChild(el('text', {
      x: mp.x, y: mp.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
      fill: color, 'font-size': size * 0.034, 'font-family': SYM_FONT,
    }, SIGN_GLYPHS[i]));
  }

  // ── Ring borders
  svgEl.appendChild(el('circle', { cx, cy, r: R,        fill: 'none', stroke: '#cec9ec', 'stroke-width': '1.5' }));
  svgEl.appendChild(el('circle', { cx, cy, r: R_SIGN_IN, fill: 'none', stroke: '#dcd8f0', 'stroke-width': '1' }));

  // ── House cusp lines + numbers
  for (let i = 0; i < 12; i++) {
    const a      = lonToAngle(cusps[i], asc);
    const pOuter = polarToXY(cx, cy, R_SIGN_IN, a);
    const pInner = polarToXY(cx, cy, R_CENTER + 4, a);
    const isAngular = [0, 3, 6, 9].includes(i);
    svgEl.appendChild(el('line', {
      x1: pInner.x, y1: pInner.y, x2: pOuter.x, y2: pOuter.y,
      stroke: isAngular ? '#6d28d9' : '#d8d4ee',
      'stroke-width': isAngular ? '1.5' : '0.8',
      'stroke-dasharray': isAngular ? '' : '3,4',
    }));
    // House number at midpoint between cusps
    const nextA = lonToAngle(cusps[(i + 1) % 12], asc);
    const midA2 = midAngle(a, nextA);
    const numPt = polarToXY(cx, cy, R_HOUSE, midA2);
    svgEl.appendChild(el('text', {
      x: numPt.x, y: numPt.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
      fill: '#b0acd0', 'font-size': size * 0.017, 'font-family': "'Inter',sans-serif",
    }, String(i + 1)));
  }

  // ── Inner fill
  svgEl.appendChild(el('circle', { cx, cy, r: R_CENTER, fill: '#ffffff', stroke: '#e4e0f5', 'stroke-width': '1' }));

  // ── Aspect lines
  for (const asp of (chartData.aspects || [])) {
    const p1 = chartData.planets.find(p => p.name === asp.planet1);
    const p2 = chartData.planets.find(p => p.name === asp.planet2);
    if (!p1 || !p2) continue;
    const pt1   = polarToXY(cx, cy, R_ASPECT, lonToAngle(p1.longitude, asc));
    const pt2   = polarToXY(cx, cy, R_ASPECT, lonToAngle(p2.longitude, asc));
    const color = ASPECT_COLORS[asp.aspect_name] || '#aaa';
    svgEl.appendChild(el('line', {
      x1: pt1.x, y1: pt1.y, x2: pt2.x, y2: pt2.y,
      stroke: color, 'stroke-width': '0.9', 'stroke-opacity': '0.55',
    }));
  }

  // ── Natal planets (dos anillos: exterior e interior para evitar amontonamiento)
  const R_PLANET_A = R * 0.70;        // anillo exterior (tier 0)
  const R_PLANET_B = R * 0.58;        // anillo interior (tier 1)
  const R_EXACT    = R_SIGN_IN - 10;  // punto exacto eclíptico (justo dentro del anillo de signos)

  const natalPlaced = placePlanets(chartData.planets, asc);
  for (const { planet, displayAngle, tier } of natalPlaced) {
    const exactPt  = polarToXY(cx, cy, R_EXACT, lonToAngle(planet.longitude, asc));
    const R_LBL_R  = tier === 0 ? R_PLANET_A : R_PLANET_B;
    const R_CIRCLE = tier === 0 ? 11 : 9;
    const labelPt  = polarToXY(cx, cy, R_LBL_R, displayAngle);
    const glyph    = PLANET_ABBR[planet.name] || planet.name[0];

    // Punto en posición eclíptica exacta
    svgEl.appendChild(el('circle', { cx: exactPt.x, cy: exactPt.y, r: 2.5, fill: '#7c3aed' }));
    // Línea conectora
    svgEl.appendChild(el('line', {
      x1: exactPt.x, y1: exactPt.y, x2: labelPt.x, y2: labelPt.y,
      stroke: '#d4d0ee', 'stroke-width': '0.7',
    }));
    // Círculo fondo (ligeramente distinto para anillo interior)
    svgEl.appendChild(el('circle', {
      cx: labelPt.x, cy: labelPt.y, r: R_CIRCLE,
      fill: tier === 0 ? '#ffffff' : '#f5f3ff',
      stroke: planet.retrograde ? '#b91c1c' : '#ccc8e8',
      'stroke-width': planet.retrograde ? '1.8' : '1.2',
    }));
    // Glifo Unicode
    svgEl.appendChild(el('text', {
      x: labelPt.x, y: labelPt.y,
      'text-anchor': 'middle', 'dominant-baseline': 'central',
      fill: planet.retrograde ? '#b91c1c' : '#3b1d8c',
      'font-size': size * (tier === 0 ? 0.027 : 0.023), 'font-family': SYM_FONT,
    }, glyph));
  }

  // ── Transit planets
  if (transitData) {
    const transitPlaced = placePlanets(transitData.transit_planets, asc);
    for (const { planet, displayAngle } of transitPlaced) {
      const pt    = polarToXY(cx, cy, R_TRANSIT, displayAngle);
      const glyph = PLANET_ABBR[planet.name] || planet.name[0];
      svgEl.appendChild(el('circle', { cx: pt.x, cy: pt.y, r: 11, fill: '#f0fdf4', stroke: '#16a34a', 'stroke-width': '1.2' }));
      svgEl.appendChild(el('text', {
        x: pt.x, y: pt.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
        fill: '#15803d', 'font-size': size * 0.024, 'font-family': SYM_FONT,
      }, glyph));
    }
  }

  // ── ASC / MC labels (outside ring)
  const ascPt = polarToXY(cx, cy, R + 16, lonToAngle(asc, asc));
  svgEl.appendChild(el('text', {
    x: ascPt.x, y: ascPt.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
    fill: '#6d28d9', 'font-size': size * 0.022, 'font-family': "'Inter',sans-serif", 'font-weight': '800',
  }, 'ASC'));

  const mcPt = polarToXY(cx, cy, R + 16, lonToAngle(chartData.mc, asc));
  svgEl.appendChild(el('text', {
    x: mcPt.x, y: mcPt.y, 'text-anchor': 'middle', 'dominant-baseline': 'central',
    fill: '#d97706', 'font-size': size * 0.022, 'font-family': "'Inter',sans-serif", 'font-weight': '800',
  }, 'MC'));
}

// ─── Date helpers ─────────────────────────────────────────────
function fillDateTimeNow() {
  const now = new Date();
  const pad = n => String(n).padStart(2, '0');
  document.getElementById('year').value   = now.getFullYear();
  document.getElementById('month').value  = pad(now.getMonth() + 1);
  document.getElementById('day').value    = pad(now.getDate());
  document.getElementById('hour').value   = pad(now.getHours());
  document.getElementById('minute').value = pad(now.getMinutes());
}

// ─── Expose globally ──────────────────────────────────────────
window.API                  = API;
window.initCitySearch       = initCitySearch;
window.initTabs             = initTabs;
window.renderPlanetTable    = renderPlanetTable;
window.renderAspects        = renderAspects;
window.renderInterpretations= renderInterpretations;
window.drawChartWheel       = drawChartWheel;
window.drawEmptyWheel       = drawEmptyWheel;
window.aspectClass          = aspectClass;
window.fillDateTimeNow      = fillDateTimeNow;
window.PLANET_ABBR          = PLANET_ABBR;
window.SIGN_SYMBOLS         = SIGN_SYMBOLS;
window.lonToAngle           = lonToAngle;
window.polarToXY            = polarToXY;
