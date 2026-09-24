/* Homepage dot-field hero: one dot per simulated cell, gene-level vs isoform-level. */
(() => {
  if (!document.getElementById('dotfield')) return;
  const cv = document.getElementById('dotfield');
  const ctx = cv.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const N = innerWidth < 760 ? 1600 : 3200;

  // Box-Muller gaussian
  const g = () => { let u = 0, v = 0; while (!u) u = Math.random(); while (!v) v = Math.random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };

  // Isoform-level clusters in unit space: [cx, cy, sx, sy, rotation, share, colour]
  const CL = [
    [ 0.00, -0.30, 0.16, 0.07,  0.4, 0.22, [ 72, 190, 200]],  // teal
    [-0.42,  0.02, 0.09, 0.15, -0.3, 0.18, [ 96, 140, 255]],  // blue
    [ 0.40,  0.10, 0.13, 0.08,  0.9, 0.17, [164, 120, 255]],  // violet
    [-0.10,  0.34, 0.14, 0.06, -0.2, 0.16, [ 90, 214, 140]],  // green
    [ 0.22, -0.02, 0.06, 0.06,  0.0, 0.15, [ 96, 140, 255]],  // blue twin of cluster 1 by gene counts
    [ 0.30,  0.38, 0.05, 0.05,  0.0, 0.12, [255, 176,  60]],  // amber: the hidden state
  ];
  const AMBER = 5;

  const dots = [];
  let acc = 0; const cum = CL.map(c => (acc += c[5]));
  for (let i = 0; i < N; i++) {
    const r = Math.random() * acc; const k = cum.findIndex(c => r <= c);
    const [cx, cy, sx, sy, rot] = CL[k];
    const a = g() * sx, b = g() * sy;
    dots.push({
      k,
      // gene-level: one broad, slightly lumpy cloud
      gx: g() * 0.17 + (k === AMBER ? 0.03 : 0), gy: g() * 0.13,
      ix: cx + a * Math.cos(rot) - b * Math.sin(rot),
      iy: cy + a * Math.sin(rot) + b * Math.cos(rot),
      delay: Math.random() * 0.35, ph: Math.random() * 6.283, sz: 0.8 + Math.random() * 1.1,
    });
  }

  let W, H, dpr, cx0, cy0, S;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // Must match the CSS query that stacks the hero.
    const stacked = matchMedia('(max-width: 699px), (orientation: portrait)').matches;
    // Stacked: the cloud lives in the space above the text block.
    if (!cv.isConnected) return;
    const copy = cv.parentElement.querySelector('.dotfield__copy');
    const free = stacked && copy ? Math.max(copy.offsetTop, H * 0.3) : H;
    if (stacked) {
      cx0 = W * 0.5; cy0 = free * 0.5; S = Math.min(W * 0.66, free * 0.85);
    } else {
      // Side by side: the cloud fills the space right of the paragraph, never behind it.
      const lead = cv.parentElement.querySelector('.dotfield__lead');
      const left = (lead ? lead.getBoundingClientRect().right - cv.getBoundingClientRect().left : W * 0.52) + 48;
      const right = W - 32;
      cx0 = (left + right) / 2; cy0 = H * 0.5; S = Math.max(120, Math.min((right - left) / 1.1, H * 0.78));
    }
  }
  size();

  // Timeline: target 0 = gene, 1 = isoform. Auto-cycles until the visitor picks one.
  let target = 1, mix = reduce ? 1 : 0, auto = !reduce, last = performance.now(), hold = 0;
  const bGene = document.getElementById('dfGene'), bIso = document.getElementById('dfIso'), note = document.getElementById('dfNote');
  const NOTES = ['One population by gene counts.', 'Isoform counts split it into states.'];
  function ui() { bGene.classList.toggle('on', target === 0); bIso.classList.toggle('on', target === 1); note.textContent = NOTES[target]; }
  bGene.onclick = () => { auto = false; target = 0; ui(); };
  bIso.onclick  = () => { auto = false; target = 1; ui(); };
  target = reduce ? 1 : 0; ui();

  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  let grey = [150, 158, 172];
  const VARS = ['--c-teal', '--c-blue', '--c-violet', '--c-green', '--c-blue', '--c-amber'];
  const rgb = v => { const m = v.trim().match(/^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i); return m ? m.slice(1).map(x => parseInt(x, 16)) : null; };
  const readTheme = () => {
    const cs = getComputedStyle(cv.parentElement);          // the hero may carry its own palette
    grey = cs.getPropertyValue('--dot-grey').split(',').map(Number);
    VARS.forEach((v, i) => { const c = rgb(cs.getPropertyValue(v)); if (c) CL[i][6] = c; });
  };
  readTheme(); new MutationObserver(readTheme).observe(document.documentElement, { attributes: true });

  function frame(now) {
    const dt = Math.min((now - last) / 1000, 0.05); last = now;
    if (auto) { hold += dt; if (hold > (target ? 5.5 : 3)) { hold = 0; target = 1 - target; ui(); } }
    mix += (target - mix) * (reduce ? 1 : Math.min(dt * 0.9, 1));
    const t = now / 1000;

    ctx.clearRect(0, 0, W, H);
    for (const d of dots) {
      const m = ease(Math.max(0, Math.min(1, (mix * 1.35 - d.delay))));
      const x = d.gx + (d.ix - d.gx) * m, y = d.gy + (d.iy - d.gy) * m;
      const jx = reduce ? 0 : Math.sin(t * 0.6 + d.ph) * 0.0035, jy = reduce ? 0 : Math.cos(t * 0.5 + d.ph) * 0.0035;
      const c = CL[d.k][6];
      const r = grey[0] + (c[0] - grey[0]) * m, gg = grey[1] + (c[1] - grey[1]) * m, b = grey[2] + (c[2] - grey[2]) * m;
      const alpha = 0.55 + 0.35 * m * (d.k === AMBER ? 1.2 : 1);
      ctx.fillStyle = `rgba(${r|0},${gg|0},${b|0},${Math.min(alpha, 1)})`;
      const px = cx0 + (x + jx) * S, py = cy0 + (y + jy) * S, s = d.sz * (d.k === AMBER ? 1 + 0.4 * m : 1);
      ctx.beginPath(); ctx.arc(px, py, s, 0, 6.283); ctx.fill();
    }
    // Keep animating only while visible; reduced motion draws a single still frame.
    if (!reduce && onScreen && !document.hidden) requestAnimationFrame(frame); else running = false;
  }

  // Pause when the hero is scrolled away or the tab is hidden, so the page costs nothing in the background.
  let running = false, onScreen = true;
  function start() {
    if (running || !onScreen || document.hidden) return;
    running = true; last = performance.now(); requestAnimationFrame(frame);
  }
  new IntersectionObserver(([e]) => { onScreen = e.isIntersecting; start(); }).observe(cv);
  document.addEventListener('visibilitychange', start);
  bGene.addEventListener('click', start); bIso.addEventListener('click', start);
  new MutationObserver(start).observe(document.documentElement, { attributes: true });
  // Repaint whenever the canvas changes size (window resize, zoom, layout shift), even while paused,
  // and always paint one frame at load so the hero is never blank or stretched.
  function paint() { size(); if (!running) { running = true; last = performance.now(); frame(last); } }
  new ResizeObserver(paint).observe(cv);
  paint();
})();
