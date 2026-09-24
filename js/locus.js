/* Research page, "One gene, many RNAs": a schematic locus drawn as genome-browser tracks.
   Strand-split nascent RNA, spliced RNA with junction arcs, small-RNA and 3' end tracks, then one
   annotation row per RNA class. Hover, focus or tap a row to highlight its region and show what it is,
   with the paper it comes from. Coverage is schematic, not data. */
(() => {
  const svg = document.getElementById('locusSvg');
  if (!svg) return;
  const fig = svg.closest('.locus');
  const card = document.getElementById('locusCard');

  // Genomic frame (kb from the TSS) mapped onto the plot area of the 1120-wide viewBox
  const K0 = -24, K1 = 80, PX0 = 150, PX1 = 1100, W = 1120, H = 592;
  const X = k => PX0 + (k - K0) / (K1 - K0) * (PX1 - PX0);
  const f1 = v => v.toFixed(1);

  // Gene model in kb; exon 2 is the alternative exon
  const EX = [[0, 1.5], [12, 13], [22, 23], [34, 36]];
  const UTR_END = 40, PA = [37.5, 40], SNO = 6, ENH = [-21, -19];

  // Smooth deterministic wobble so the tracks look measured rather than drawn
  const wob = k => 1 + 0.05 * Math.sin(k * 2.1) + 0.035 * Math.sin(k * 5.3 + 1) + 0.015 * Math.sin(k * 11.7);
  const bump = (k, c, w) => Math.exp(-(((k - c) / w) ** 2));
  const inExon = k => EX.findIndex(([a, b]) => k >= a && k <= b);

  const nascentPlus = k => (0.3 * bump(k, -20, 0.5)
    + (k >= 0 && k <= 40 ? 0.62 - 0.004 * k : 0)
    + (k > 40 ? 0.36 * Math.exp(-(k - 40) / 13) : 0)) * wob(k);
  const nascentMinus = k => (0.25 * bump(k, -20, 0.5) + 0.38 * bump(k, -1.5, 0.45)) * wob(k + 3);
  const spliced = k => {
    const e = inExon(k);
    let v = e >= 0 ? [0.72, 0.36, 0.74, 0.82][e] : 0;
    if (k > 36 && k <= 37.5) v = 0.86;
    else if (k > 37.5 && k <= 40) v = 0.42;
    if (k > 23 && k < 34) v = 0.07;               // the retained intron
    return v * wob(k * 1.7);
  };
  const smallRna = k => bump(k, SNO, 0.12);
  const ends = k => 0.9 * bump(k, PA[0], 0.22) + 0.55 * bump(k, PA[1], 0.22);

  const area = (f, base, h, dir, step) => {
    let d = `M${f1(X(K0))} ${base}`;
    for (let k = K0; k <= K1 + 1e-9; k += step) d += ` L${f1(X(k))} ${f1(base - dir * h * Math.min(f(k), 1.1))}`;
    return `${d} L${f1(X(K1))} ${base} Z`;
  };
  const arcUp = (k1, y1, k2, y2, h) => {
    const top = Math.min(y1, y2) - h;
    return `M${f1(X(k1))} ${y1} C${f1(X(k1))} ${top} ${f1(X(k2))} ${top} ${f1(X(k2))} ${y2}`;
  };
  const arcDown = (k1, k2, y, h) => `M${f1(X(k1))} ${y} C${f1(X(k1))} ${y + h} ${f1(X(k2))} ${y + h} ${f1(X(k2))} ${y}`;
  const box = (a, b, y, h, cls) =>
    `<rect class="${cls}" x="${f1(X(a))}" y="${f1(y - h / 2)}" width="${f1(Math.max(2.5, X(b) - X(a)))}" height="${h}" rx="1"/>`;
  const hline = (a, b, y, cls) => `<line class="${cls}" x1="${f1(X(a))}" y1="${y}" x2="${f1(X(b))}" y2="${y}"/>`;
  const chev = (k, y, dir, cls) => {
    const x = X(k);
    return `<path class="${cls}" d="M${f1(x - 3 * dir)} ${y - 3} L${f1(x)} ${y} L${f1(x - 3 * dir)} ${y + 3}"/>`;
  };
  const label = (y, text, cls = 'lx-label') => `<text class="${cls}" x="${PX0 - 14}" y="${y}" text-anchor="end">${text}</text>`;

  // A transcript model: exons thick, 3' UTR thin, introns as a hairline
  const model = (exons, utrEnd, y, cls, extra = '') => {
    let s = hline(exons[0][0], utrEnd, y, `${cls} lx-hair`);
    exons.forEach(ex => { s += box(ex[0], ex[1], y, 9, EX.indexOf(ex) === 1 ? `${cls} lx-alt` : cls); });
    return s + box(36, utrEnd, y, 5, cls) + extra;
  };

  // ── Track geometry (viewBox units) ──
  const RULER = 26, GENE = 70, NAS = 150, NAS_H = 44, SPL = 270, SPL_H = 46, SMALL = 334, END = 378, TRK_H = 30;
  const ROW0 = 418, ROW = 17;

  let out = `<defs>
    <clipPath id="lxReveal"><rect id="lxRevealRect" x="0" y="0" width="${W}" height="${H}"/></clipPath>
    <linearGradient id="lxDogFade" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="var(--c-violet)" stop-opacity=".9"/><stop offset="1" stop-color="var(--c-violet)" stop-opacity="0"/>
    </linearGradient></defs>`;
  out += '<g id="lxBands"></g>';

  // Ruler
  out += `<line class="lx-axis" x1="${PX0}" y1="${RULER}" x2="${PX1}" y2="${RULER}"/>`;
  for (let k = -20; k <= 80; k += 10) {
    out += `<line class="lx-axis" x1="${f1(X(k))}" y1="${RULER - 4}" x2="${f1(X(k))}" y2="${RULER}"/>`;
    out += `<text class="lx-tick" x="${f1(X(k))}" y="${RULER - 8}" text-anchor="middle">${k === 0 ? 'TSS' : (k > 0 ? '+' : '') + k}</text>`;
  }
  out += label(RULER + 3, 'kb, schematic');

  // Gene model with enhancer, TSS, intronic snoRNA and two poly(A) sites
  out += label(GENE + 4, 'gene');
  out += `<line class="lx-dna" x1="${PX0}" y1="${GENE}" x2="${PX1}" y2="${GENE}"/>`;
  out += `<rect class="gm-enh" x="${f1(X(ENH[0]))}" y="${GENE - 5}" width="${f1(X(ENH[1]) - X(ENH[0]))}" height="10" rx="1"/>`;
  out += `<text class="lx-tick" x="${f1(X(-20))}" y="${GENE - 10}" text-anchor="middle">enhancer</text>`;
  out += `<path class="gm-tss" d="M${f1(X(0))} ${GENE} V${GENE - 14} H${f1(X(0) + 12)} M${f1(X(0) + 8)} ${GENE - 17} L${f1(X(0) + 12)} ${GENE - 14} L${f1(X(0) + 8)} ${GENE - 11}"/>`;
  out += hline(0, UTR_END, GENE, 'gm-intron');
  for (let k = 4; k < 34; k += 4) if (inExon(k) < 0) out += chev(k, GENE, 1, 'gm-chev');
  EX.forEach(([a, b], i) => { out += box(a, b, GENE, 12, i === 1 ? 'gm-alt' : 'gm-exon'); });
  out += box(36, UTR_END, GENE, 7, 'gm-exon');
  out += box(SNO - 0.2, SNO + 0.2, GENE, 8, 'gm-sno');
  PA.forEach(k => { out += `<line class="gm-pa" x1="${f1(X(k))}" y1="${GENE + 6}" x2="${f1(X(k))}" y2="${GENE + 14}"/>`; });
  out += `<text class="lx-tick" x="${f1(X(PA[0]))}" y="${GENE + 25}" text-anchor="middle">pA</text>`;
  out += `<text class="lx-tick" x="${f1(X(PA[1]))}" y="${GENE + 25}" text-anchor="middle">pA</text>`;

  // Coverage tracks (revealed left to right on first view)
  out += '<g clip-path="url(#lxReveal)">';
  out += label(NAS - 4, 'nascent RNA') + label(NAS + 10, '+ / − strand', 'lx-tick lx-sub');
  out += `<line class="lx-base" x1="${PX0}" y1="${NAS}" x2="${PX1}" y2="${NAS}"/>`;
  out += `<path class="cov-plus" d="${area(nascentPlus, NAS, NAS_H, 1, 0.1)}"/>`;
  out += `<path class="cov-minus" d="${area(nascentMinus, NAS, NAS_H, -1, 0.1)}"/>`;

  out += label(SPL - 12, 'spliced RNA');
  out += `<line class="lx-base" x1="${PX0}" y1="${SPL}" x2="${PX1}" y2="${SPL}"/>`;
  out += `<path class="cov-spl" d="${area(spliced, SPL, SPL_H, 1, 0.1)}"/>`;
  const top = i => SPL - SPL_H * [0.72, 0.36, 0.74, 0.82][i];
  out += `<path class="arc" d="${arcUp(1.5, f1(top(0)), 12, f1(top(1)), 22)}"/>`;
  out += `<path class="arc" d="${arcUp(13, f1(top(1)), 22, f1(top(2)), 20)}"/>`;
  out += `<path class="arc arc--main" d="${arcUp(23, f1(top(2)), 34, f1(top(3)), 22)}"/>`;
  out += `<path class="arc" d="${arcDown(1.5, 22, SPL + 2, 28)}"/>`;                     // exon skipping
  out += `<path class="arc arc--circ" d="${arcDown(12, 23, SPL + 2, 15)}"/>`;             // circRNA junction

  out += label(SMALL - 6, 'small RNA');
  out += `<line class="lx-base" x1="${PX0}" y1="${SMALL}" x2="${PX1}" y2="${SMALL}"/>`;
  out += `<path class="cov-small" d="${area(smallRna, SMALL, TRK_H, 1, 0.04)}"/>`;

  out += label(END - 6, '3′ ends');
  out += `<line class="lx-base" x1="${PX0}" y1="${END}" x2="${PX1}" y2="${END}"/>`;
  out += `<path class="cov-end" d="${area(ends, END, TRK_H, 1, 0.04)}"/>`;
  out += '</g>';

  // One annotation row per RNA class
  const e1 = EX[0], e2 = EX[1], e3 = EX[2], e4 = EX[3];
  const ROWS = [
    ['erna', 'eRNA', y => box(-20.5, -19.1, y - 3, 3, 'f-erna') + chev(-19.1, y - 3, 1, 'f-erna-l')
                        + box(-20.9, -19.5, y + 3, 3, 'f-erna') + chev(-20.9, y + 3, -1, 'f-erna-l')],
    ['prompt', 'PROMPT', y => box(-2.5, -0.6, y, 4, 'f-prompt') + chev(-2.5, y, -1, 'f-prompt-l')],
    ['premrna', 'pre-mRNA', y => box(0, UTR_END, y, 3, 'f-pre') + EX.map(([a, b]) => box(a, b, y, 8, 'f-pre')).join('')],
    ['snorna', 'snoRNA', y => box(SNO - 0.18, SNO + 0.18, y, 9, 'f-sno')],
    ['alt', 'mRNA, exon in', y => model([e1, e2, e3, e4], UTR_END, y, 'f-mrna')],
    ['alt', 'mRNA, exon out', y => model([e1, e3, e4], UTR_END, y, 'f-mrna')],
    ['apa', 'mRNA, short 3′ end', y => model([e1, e2, e3, e4], PA[0], y, 'f-mrna')],
    ['ri', 'retained intron', y => box(23, 34, y, 6, 'f-ri') + model([e1, e2, e3, e4], UTR_END, y, 'f-mrna')],
    ['circ', 'circRNA', y => box(e2[0], e2[1], y, 8, 'f-circ') + hline(e2[1], e3[0], y, 'f-circ-l') + box(e3[0], e3[1], y, 8, 'f-circ')
                            + `<path class="f-circ-l" d="${arcUp(e3[1], y - 4, e2[0], y - 4, 5)}"/>`],
    ['dog', 'DoG RNA', y => `<rect x="${f1(X(PA[1]))}" y="${y - 2}" width="${f1(X(78) - X(PA[1]))}" height="4" rx="1" fill="url(#lxDogFade)"/>`],
  ];
  ROWS.forEach(([key, name, draw], i) => {
    const y = ROW0 + i * ROW;
    out += `<g class="lx-row" data-key="${key}" tabindex="0" role="button" aria-label="${name}">`
      + `<rect class="lx-hit" x="0" y="${y - ROW / 2}" width="${W}" height="${ROW}"/>`
      + `<text class="lx-name" x="${PX0 - 14}" y="${y + 4}" text-anchor="end">${name}</text>${draw(y)}</g>`;
  });
  svg.innerHTML = out;

  // ── What each class is, with the paper it comes from ──
  const REF = {
    kim: ['Kim et al. 2010, Nature', 'https://doi.org/10.1038/nature09033'],
    preker: ['Preker et al. 2008, Science', 'https://doi.org/10.1126/science.1164096'],
    matera: ['Matera & Wang 2014, Nat Rev Mol Cell Biol', 'https://doi.org/10.1038/nrm3742'],
    bach: ['Bachellerie et al. 1995, Biochem Cell Biol', 'https://doi.org/10.1139/o95-091'],
    yin: ['Yin et al. 2012, Mol Cell', 'https://doi.org/10.1016/j.molcel.2012.07.033'],
    ober: ['Oberdoerffer et al. 2008, Science', 'https://doi.org/10.1126/science.1157610'],
    domin: ['Dominski & Marzluff 2007, Gene', 'https://doi.org/10.1016/j.gene.2007.04.021'],
    tian: ['Tian & Manley 2016, Nat Rev Mol Cell Biol', 'https://doi.org/10.1038/nrm.2016.116'],
    sand: ['Sandberg et al. 2008, Science', 'https://doi.org/10.1126/science.1155390'],
    braun: ['Braunschweig et al. 2014, Genome Res', 'https://doi.org/10.1101/gr.177790.114'],
    krist: ['Kristensen et al. 2019, Nat Rev Genet', 'https://doi.org/10.1038/s41576-019-0158-7'],
    vil: ['Vilborg et al. 2015, Mol Cell', 'https://doi.org/10.1016/j.molcel.2015.06.016'],
    obsch: ['Oberbauer & Schaefer 2018, Genes', 'https://doi.org/10.3390/genes9120607'],
    lerner79: ['Lerner & Steitz 1979, PNAS', 'https://doi.org/10.1073/pnas.76.11.5495'],
    darz: ['Darzacq et al. 2002, EMBO J', 'https://doi.org/10.1093/emboj/21.11.2746'],
    nguyen: ['Nguyen et al. 2001, Nature', 'https://doi.org/10.1038/35104581'],
    lerner81: ['Lerner et al. 1981, PNAS', 'https://doi.org/10.1073/pnas.78.2.805'],
  };
  const CL = {
    erna: { name: 'Enhancer RNA (eRNA)', band: [[-21, -19]], poly: 'not established',
      text: 'RNA polymerase II transcribes active enhancers in both directions. eRNA levels track mRNA synthesis at nearby genes.', src: ['kim'] },
    prompt: { name: 'Promoter upstream transcript (PROMPT)', band: [[-2.6, -0.4]], poly: 'yes',
      text: 'Short, unstable RNAs made 0.5 to 2.5 kb upstream of active promoters, in both directions. They become visible when the RNA exosome that degrades them is removed.', src: ['preker'] },
    premrna: { name: 'Nascent pre-mRNA', band: [[0, UTR_END]],
      text: 'The first copy of the gene still carries its introns. The spliceosome, assembled on small nuclear RNAs, removes them.', src: ['matera'] },
    snorna: { name: 'Small nucleolar RNA (snoRNA)', band: [[SNO - 0.4, SNO + 0.4]],
      text: 'Many snoRNAs sit inside introns of host genes and are processed out of the intron. Some pair with ribosomal RNA precursors and are needed to make mature ribosomal RNA. When two snoRNAs share an intron, the RNA between them can survive as a sno-lncRNA, with no cap and no poly(A) tail.', src: ['bach', 'yin'] },
    alt: { name: 'Alternative exon', band: [e2], poly: 'yes',
      text: 'The same pre-mRNA can keep or skip an exon, so one gene makes mRNAs with different sequences. In T cells, splicing of CD45 changes as cells move from naive to activated.', src: ['ober', 'domin'] },
    apa: { name: 'Alternative 3′ end', band: [[36, UTR_END]], poly: 'yes',
      text: 'One gene can end at more than one poly(A) site, giving mRNAs with shorter or longer 3′ ends. The choice is widespread and tied to proliferation and differentiation. Activated T cells shift toward the shorter ends.', src: ['tian', 'sand'] },
    ri: { name: 'Retained intron', band: [[e3[1], e4[0]]], poly: 'yes, found in poly(A)+ RNA',
      text: 'Some transcripts keep an intron. In mammals this affects transcripts from up to three-quarters of multi-exon genes and lowers their levels through decay or retention in the nucleus.', src: ['braun'] },
    circ: { name: 'Circular RNA (circRNA)', band: [[e2[0], e3[1]]], poly: 'no free 3′ end',
      text: 'Covalently closed RNAs with cell- and tissue-specific expression. Some act as microRNA or protein sponges, and some are translated.', src: ['krist'] },
    dog: { name: 'Downstream-of-gene RNA (DoG)', band: [[PA[1], 78]], poly: 'not established',
      text: 'When termination at the gene end fails, for example under osmotic stress, the polymerase keeps going. The resulting RNAs cover long non-coding stretches, often over 45 kb, and stay bound to chromatin. Thousands exist genome-wide.', src: ['vil'] },
    trna: { name: 'tRNAs and tRNA fragments', band: [],
      text: 'tRNAs decode mRNA during translation and are the most heavily modified RNAs in the cell. They are also cut into small tRNA-derived RNAs, whose functions are still being worked out.', src: ['obsch'] },
    snrna: { name: 'Spliceosomal snRNAs', band: [],
      text: 'U1, U2, U4, U5 and U6 form the RNA core of the spliceosome. Their RNA-protein particles were first defined as the targets of antibodies made by patients with lupus.', src: ['matera', 'lerner79'] },
    scarna: { name: 'scaRNAs', band: [],
      text: 'Small Cajal body-specific RNAs guide chemical modification of the spliceosomal snRNAs.', src: ['darz'] },
    sk7: { name: '7SK RNA', band: [],
      text: 'An abundant small nuclear RNA that holds more than half of the P-TEFb elongation factor in a low-activity complex, a brake on RNA polymerase II.', src: ['nguyen'] },
    eber: { name: 'EBV EBERs', band: [], poly: 'no',
      text: 'Epstein-Barr virus makes large amounts of two small non-coding RNAs, EBER1 and EBER2, in the cells it infects. They are bound by La, a protein targeted by lupus autoantibodies.', src: ['lerner81'] },
  };

  const DEFAULT = '<p class="locus__text">Hover, focus or tap a track to see what it is and where the evidence comes from.</p>';
  const bands = svg.querySelector('#lxBands');
  const rows = [...svg.querySelectorAll('.lx-row')];
  const chips = [...fig.querySelectorAll('.locus__chip')];

  function activate(key) {
    const c = CL[key];
    rows.forEach(r => { r.classList.toggle('is-on', r.dataset.key === key); r.classList.toggle('is-dim', !!c && c.band.length > 0 && r.dataset.key !== key); });
    chips.forEach(b => b.classList.toggle('is-on', b.dataset.key === key));
    bands.innerHTML = c ? c.band.map(([a, b]) => {
      const x = X(a), w = Math.max(8, X(b) - x);
      return `<rect class="lx-band" x="${f1(x - (w === 8 ? 4 : 0))}" y="${RULER + 8}" width="${f1(w)}" height="${H - RULER - 12}" rx="2"/>`;
    }).join('') : '';
    if (!c) { card.innerHTML = DEFAULT; return; }
    const refs = c.src.map(r => `<a href="${REF[r][1]}" target="_blank" rel="noopener">${REF[r][0]}</a>`).join(' · ');
    card.innerHTML = `<p class="locus__name">${c.name}</p><p class="locus__text">${c.text}</p>`
      + `<p class="locus__meta">${c.poly ? `Poly(A) tail: ${c.poly} · ` : ''}${refs}</p>`;
  }
  rows.forEach(r => {
    const on = () => activate(r.dataset.key);
    r.addEventListener('pointerenter', on); r.addEventListener('focus', on); r.addEventListener('click', on);
    r.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); on(); } });
  });
  chips.forEach(b => { const on = () => activate(b.dataset.key); b.addEventListener('pointerenter', on); b.addEventListener('focus', on); b.addEventListener('click', on); });
  activate(null);

  // Reveal the coverage tracks left to right the first time the figure scrolls into view
  const rect = svg.querySelector('#lxRevealRect');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    rect.setAttribute('width', '0');
    new IntersectionObserver(([e], io) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      const t0 = performance.now(), dur = 1600;
      const step = now => {
        const p = Math.min(1, (now - t0) / dur), q = 1 - Math.pow(1 - p, 3);
        rect.setAttribute('width', f1(W * q));
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }, { threshold: 0.25 }).observe(svg);
  }
})();
