/* Homepage research pillars: a step list beside one large figure. Hover, click, focus or arrow keys
   choose a pillar; otherwise the steps advance on their own while the section is in view. Any click
   stops the auto-advance; reduced motion never starts it. */
(() => {
  const root = document.querySelector('.pillars');
  if (!root) return;
  const steps = [...root.querySelectorAll('.pillars__step')];
  const panels = [...root.querySelectorAll('.pillars__panel')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let current = 0, auto = !reduce;

  function show(i, focus) {
    current = (i + steps.length) % steps.length;
    steps.forEach((s, k) => {
      const on = k === current;
      s.classList.toggle('is-on', on);
      s.setAttribute('aria-selected', on ? 'true' : 'false');
      s.tabIndex = on ? 0 : -1;
    });
    panels.forEach((p, k) => { p.hidden = k !== current; p.classList.toggle('is-on', k === current); });
    if (focus) steps[current].focus();
    restartBar();
  }

  // The active step's bar fills over the dwell time; when it finishes, move on.
  function restartBar() {
    root.classList.toggle('is-auto', auto);
    const bar = steps[current].querySelector('.pillars__bar i');
    bar.style.animation = 'none';
    void bar.offsetWidth;                                  // restart the CSS animation
    bar.style.animation = '';
  }
  steps.forEach(s => s.querySelector('.pillars__bar i').addEventListener('animationend', () => { if (auto) show(current + 1); }));

  steps.forEach((s, k) => {
    s.addEventListener('click', () => { auto = false; show(k); });
    s.addEventListener('pointerenter', () => { if (k !== current) show(k); });
    s.addEventListener('focus', () => { if (k !== current) show(k); });
    s.addEventListener('keydown', e => {
      const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
      if (d) { e.preventDefault(); auto = false; show(current + d, true); }
      if (e.key === 'Home') { e.preventDefault(); auto = false; show(0, true); }
      if (e.key === 'End') { e.preventDefault(); auto = false; show(steps.length - 1, true); }
    });
  });

  // Pause while the pointer is over the section or the section is off screen
  root.addEventListener('pointerenter', () => root.classList.add('is-paused'));
  root.addEventListener('pointerleave', () => root.classList.remove('is-paused'));
  new IntersectionObserver(([e]) => root.classList.toggle('is-offscreen', !e.isIntersecting), { threshold: 0.3 }).observe(root);

  show(0);
})();
