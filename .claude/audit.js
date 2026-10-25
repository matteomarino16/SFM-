// Verifica responsive (strumento di sviluppo, non fa parte del sito)
(async () => {
  document.documentElement.style.scrollBehavior = 'auto';
  document.querySelectorAll('.reveal').forEach((e) => e.classList.add('is-visible'));
  await new Promise((r) => setTimeout(r, 700));
  const W = innerWidth, H = innerHeight;
  const ov = [];
  document.querySelectorAll('body *').forEach((el) => {
    if (el.closest('.events__track, .filters, .product__slides, .main-nav:not(.is-open), dialog, .hero__canvas, .cursor, .skip-link, .sr-only')) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.position === 'fixed' || cs.visibility === 'hidden') return;
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > W + 1 || r.left < -1)) ov.push(String(el.className).slice(0, 36) + ' ' + Math.round(r.left) + '→' + Math.round(r.right));
  });
  const brand = document.querySelector('.hero__brand-rest').getBoundingClientRect();
  const mono = document.querySelector('.hero__mono').getBoundingClientRect();
  const chapters = [...document.querySelectorAll('.hero-chapter')].map((c) => { const r = c.getBoundingClientRect(); return Math.round(r.top) + '-' + Math.round(r.bottom) + (r.bottom > H ? '!' : ''); });
  const nav = document.querySelector('.main-nav__list').getBoundingClientRect(), b = document.querySelector('.brand').getBoundingClientRect();
  const desktopNav = getComputedStyle(document.querySelector('.nav-toggle')).display === 'none';
  const cta = document.querySelector('.product__cta').getBoundingClientRect().height;
  return {
    vw: W + 'x' + H,
    sw: document.documentElement.scrollWidth,
    ov: [...new Set(ov)].slice(0, 6),
    logo: Math.round(mono.top) + '-' + Math.round(brand.bottom) + (brand.bottom > H ? '!' : ''),
    chapters: chapters.join(' '),
    nav: desktopNav ? (nav.left < b.right + 8 ? 'SOVRAPPOSTO!' : 'ok') : 'hamburger',
    cta: Math.round(cta)
  };
})()
