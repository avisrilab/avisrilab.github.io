/* "Why we exist" figure: gene-level dots burst into the isoforms they hide.
   Scale is honest: each gray dot stands for 10 genes (2,000 dots, about 20,000 genes),
   each coloured dot for 10 isoforms (20,000 dots, about 200,000 isoforms). */
(() => {
  const cv = document.getElementById('burst');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const counter = document.getElementById('burstCount'), unit = document.getElementById('burstUnit');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const COLS = [[72, 190, 200], [96, 140, 255], [164, 120, 255], [90, 214, 140], [255, 176, 60]];
  const GENES = 2000;

  let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  // Genes sit in a soft disc; each hides a variable number of isoforms (mean 10).
  const genes = [], kids = [];
  // Five hidden 'states': each gene takes the colour of its nearest centre, so the burst resolves into regions.
  const CENTRES = [[0.34, 0.33], [0.68, 0.30], [0.74, 0.64], [0.44, 0.72], [0.24, 0.55]];
  const nearest = (x, y) => CENTRES.reduce((best, c, i) =>
    (Math.hypot(x - c[0], y - c[1]) < Math.hypot(x - CENTRES[best][0], y - CENTRES[best][1]) ? i : best), 0);
  for (let i = 0; i < GENES; i++) {
    const a = rnd() * 6.283, r = Math.sqrt(rnd()) * 0.46;
    const g = { x: 0.5 + r * Math.cos(a), y: 0.5 + r * Math.sin(a) };
    g.c = COLS[nearest(g.x, g.y)];
    genes.push(g);
    const n = Math.max(1, Math.round(-Math.log(1 - rnd() * 0.999) * 10));
    for (let k = 0; k < n && kids.length < GENES * 10; k++) {
      const b = rnd() * 6.283, d = 0.012 + rnd() * 0.05;
      kids.push({ g, dx: Math.cos(b) * d, dy: Math.sin(b) * d, c: g.c, delay: rnd() * 0.35 });
    }
  }
  while (kids.length < GENES * 10) {           // top up to exactly 10x
    const g = genes[Math.floor(rnd() * GENES)], b = rnd() * 6.283, d = 0.012 + rnd() * 0.05;
    kids.push({ g, dx: Math.cos(b) * d, dy: Math.sin(b) * d, c: g.c, delay: rnd() * 0.35 });
  }

  let W, H, S, dpr;
  function size() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight; S = Math.min(W, H);
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  const ease = t => 1 - Math.pow(1 - t, 3);
  const fmt = n => Math.round(n).toLocaleString('en-US');
  function draw(p) {                           // p: 0 = gene view, 1 = fully burst
    ctx.clearRect(0, 0, W, H);
    const ox = (W - S) / 2, oy = (H - S) / 2;
    ctx.fillStyle = `rgba(150,158,172,${0.85 - 0.6 * p})`;
    for (const g of genes) ctx.fillRect(ox + g.x * S - 1, oy + g.y * S - 1, 2, 2);
    if (p > 0) for (const k of kids) {
      const q = ease(Math.max(0, Math.min(1, (p - k.delay) / 0.65)));
      if (!q) continue;
      ctx.fillStyle = `rgba(${k.c[0]},${k.c[1]},${k.c[2]},${0.85 * q})`;
      ctx.fillRect(ox + (k.g.x + k.dx * q) * S - 0.8, oy + (k.g.y + k.dy * q) * S - 0.8, 1.6, 1.6);
    }
    const n = p < 0.02 ? 20000 : 20000 + 180000 * ease(Math.min(1, p / 0.9));
    counter.textContent = fmt(n) + (p >= 1 ? '+' : '');
    unit.textContent = p < 0.02 ? 'genes' : 'isoforms';
  }

  let t0 = null, played = false;
  function run(now) {
    if (t0 === null) t0 = now;
    const t = (now - t0) / 1000, p = Math.max(0, Math.min(1, (t - 0.8) / 2.2));
    draw(p);
    if (p < 1) requestAnimationFrame(run);
  }
  function play() { t0 = null; played = true; requestAnimationFrame(run); }

  new ResizeObserver(() => { size(); draw(played || reduce ? 1 : 0); }).observe(cv);
  size(); draw(reduce ? 1 : 0);
  if (!reduce) {
    new IntersectionObserver(([e], io) => {
      if (e.isIntersecting && e.intersectionRatio > 0.5) { io.disconnect(); play(); }
    }, { threshold: [0.5] }).observe(cv);
    cv.parentElement.querySelector('.burst__replay').addEventListener('click', play);
  }
})();
