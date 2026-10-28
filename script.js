/* ==========================================================================
   S.F.M. Distribuzione — Script del sito
   Indice:
   01. Configurazione (numero WhatsApp, endpoint form, prodotti)
   02. Utilità
   03. Header, menu mobile e link attivi
   04. Animazioni di comparsa
   05. Prodotti (griglia + filtri) · 05b. Eventi
   06. Link WhatsApp e recensioni Google
   07. Form richieste
   08. Cursore personalizzato
   09. Hero 3D (Three.js)
   10. Avvio
   ========================================================================== */
(function () {
  'use strict';

  /* ========================================================================
     01. CONFIGURAZIONE
     ======================================================================== */

  /** Numero WhatsApp in formato internazionale, senza "+" né spazi (es. 393331234567). */
  const WHATSAPP_NUMBER = '393384693769';

  /**
   * Endpoint alternativo per il form (es. Formspree: 'https://formspree.io/f/xxxxxxx').
   * Lasciare vuoto per usare WhatsApp come canale principale.
   * Per attivarlo vedere la funzione "inviaAEndpoint" nella sezione 07.
   */
  const FORM_ENDPOINT = '';

  /** Email per l'invio alternativo del form (mailto). */
  const CONTACT_EMAIL = 'info@sfmdistribuzioni.com';

  /**
   * Recensioni Google (SEGNAPOSTO: da compilare con i dati reali della scheda).
   * voto / totale: voto medio e numero di recensioni (null = non mostrati).
   * link: pagina con le recensioni; linkScrivi: link "lascia una recensione"
   * (dalla scheda Google Business: "Chiedi recensioni" → https://g.page/r/…/review).
   * recensioni: facoltativo, alcune recensioni REALI copiate da Google, es.
   *   { autore: 'Mario R.', voto: 5, testo: 'Servizio impeccabile…' }
   */
  const GOOGLE_REVIEWS = {
    voto: null,
    totale: null,
    link: 'https://www.google.com/maps/search/?api=1&query=S.F.M.%20Distribuzione',
    linkScrivi: '',
    recensioni: []
  };

  /** Etichette leggibili delle categorie (la chiave corrisponde a data-filter nell'HTML). */
  const CATEGORIE = {
    rossi: 'Vino Rosso',
    bianchi: 'Vino Bianco',
    bollicine: 'Bollicine',
    rosati: 'Rosato',
    distillati: 'Amaro / Distillato',
    bevande: 'Bevanda'
  };

  /**
   * Catalogo prodotti.
   * categoria: una delle chiavi di CATEGORIE (rossi, bianchi, bollicine, rosati, distillati, bevande).
   * immagini: una o più foto (fronte, retro…): nella card si scorrono e al clic
   *           si ingrandiscono. Le foto ottimizzate stanno in assets/prodotti/web/
   *           (gli originali ad alta risoluzione restano in assets/prodotti/vino/).
   * Se l'immagine manca viene mostrato un segnaposto grafico.
   */
  const PRODOTTI = [
    // ---- Vini rossi --------------------------------------------------------
    {
      nome: 'Vasia',
      cantina: 'Tenute De Giglio',
      categoria: 'rossi',
      regione: 'Calabria IGP',
      descrizione: 'Calabrese e Sangiovese. Rosso intenso con riflessi violacei, frutti rossi e finale persistente: ideale con carni e formaggi stagionati.',
      immagini: [
        'assets/prodotti/web/vasia-rosso.jpg',
        'assets/prodotti/web/vasia-rosso-retro.jpg'
      ]
    },
    {
      nome: 'Kalanero',
      cantina: 'Vecchi Cantinieri',
      categoria: 'rossi',
      regione: 'Calabria',
      descrizione: 'Rosso calabrese dal carattere deciso, pensato per accompagnare la cucina di terra e i piatti più strutturati.',
      immagini: ['assets/prodotti/web/kalanero.jpg']
    },
    {
      nome: 'Primula Rosso',
      cantina: 'Cantine De Luca',
      categoria: 'rossi',
      regione: 'Calabria IGP',
      descrizione: 'Dalla linea dedicata al fiore simbolo della primavera: profumi intensi e delicati, gusto vivace e sorprendente.',
      immagini: [
        'assets/prodotti/web/primula-rosso.jpg',
        'assets/prodotti/web/primula-rosso-retro.jpg'
      ]
    },
    {
      nome: 'Dalia Rosso',
      cantina: 'Vecchi Cantinieri',
      categoria: 'rossi',
      regione: 'Calabria',
      descrizione: 'Rosso dall\'etichetta d\'autore, morbido e conviviale: un compagno versatile per tutta la tavola.',
      immagini: [
        'assets/prodotti/web/dalia-rosso.jpg',
        'assets/prodotti/web/dalia-rosso-retro.jpg'
      ]
    },
    {
      nome: 'Calasulu Rosso',
      cantina: 'Vecchi Cantinieri',
      categoria: 'rossi',
      regione: 'Calabria',
      descrizione: '"Si canusci du culuri, d\'a scumma e du sapuri." Rosso schietto e territoriale, da tutti i giorni.',
      immagini: [
        'assets/prodotti/web/calasulu-rosso.jpg',
        'assets/prodotti/web/calasulu-rosso-retro.jpg'
      ]
    },

    // ---- Vini bianchi ------------------------------------------------------
    {
      nome: 'Maremè',
      cantina: 'Tenute De Giglio',
      categoria: 'bianchi',
      regione: 'Calabria IGP',
      descrizione: 'Insolia. Giallo paglierino, note agrumate, finale fresco e persistente. Perfetto con pesce e cucina mediterranea.',
      immagini: [
        'assets/prodotti/web/mareme-bianco.jpg',
        'assets/prodotti/web/mareme-bianco-retro.jpg'
      ]
    },
    {
      nome: 'Primula Bianco',
      cantina: 'Cantine De Luca',
      categoria: 'bianchi',
      regione: 'Calabria IGP',
      descrizione: 'Bianco giovane e luminoso: profumi intensi e delicati, sorso vivace. Ottimo con antipasti e crudi.',
      immagini: [
        'assets/prodotti/web/primula-bianco.jpg',
        'assets/prodotti/web/primula-bianco-retro.jpg'
      ]
    },
    {
      nome: 'Dalia Bianco',
      cantina: 'Vecchi Cantinieri',
      categoria: 'bianchi',
      regione: 'Calabria',
      descrizione: 'Bianco fresco e beverino, ideale per aperitivi e piatti di mare.',
      immagini: [
        'assets/prodotti/web/dalia-bianco.jpg',
        'assets/prodotti/web/dalia-bianco-retro.jpg'
      ]
    },
    {
      nome: 'Calasulu Bianco',
      cantina: 'Vecchi Cantinieri',
      categoria: 'bianchi',
      regione: 'Calabria',
      descrizione: 'Bianco calabrese semplice e sincero, da servire fresco con la cucina quotidiana.',
      immagini: [
        'assets/prodotti/web/calasulu-bianco.jpg',
        'assets/prodotti/web/calasulu-bianco-retro.jpg'
      ]
    },

    // ---- Rosati ------------------------------------------------------------
    {
      nome: 'Mùrmuro',
      cantina: 'Tenute De Giglio',
      categoria: 'rosati',
      regione: 'Calabria IGP',
      descrizione: 'Calabrese e Sangiovese. Rosa cerasuolo, naso fruttato, finale fresco e persistente. Da servire a 10–12 °C.',
      immagini: [
        'assets/prodotti/web/murmuro-rosato.jpg',
        'assets/prodotti/web/murmuro-rosato-retro.jpg'
      ]
    },
    {
      nome: 'Primula Rosato',
      cantina: 'Cantine De Luca',
      categoria: 'rosati',
      regione: 'Calabria IGP',
      descrizione: 'Rosato delicato e floreale, dalla linea Primula: freschezza e piacevolezza per la bella stagione.',
      immagini: [
        'assets/prodotti/web/primula-rosato.jpg',
        'assets/prodotti/web/primula-rosato-retro.jpg'
      ]
    },
    {
      nome: 'Dalia Rosato',
      cantina: 'Vecchi Cantinieri',
      categoria: 'rosati',
      regione: 'Calabria',
      descrizione: 'Rosato brillante e fragrante, perfetto per aperitivi, pizza e cucina estiva.',
      immagini: [
        'assets/prodotti/web/dalia-rosato.jpg',
        'assets/prodotti/web/dalia-rosato-retro.jpg'
      ]
    },
    {
      nome: 'Calasulu Rosato',
      cantina: 'Vecchi Cantinieri',
      categoria: 'rosati',
      regione: 'Calabria',
      descrizione: 'Rosato fresco e immediato, dal colore vivace: un jolly per la carta al calice.',
      immagini: [
        'assets/prodotti/web/calasulu-rosato.jpg',
        'assets/prodotti/web/calasulu-rosato-retro.jpg'
      ]
    },

    // ---- Amari e distillati ------------------------------------------------
    {
      nome: 'Amaro Korva',
      cantina: 'Produzione artigianale',
      categoria: 'distillati',
      regione: 'Calabria · 30% vol.',
      descrizione: 'Amaro artigianale ottenuto dall\'infusione di erbe aromatiche e agrumi. Il fine pasto che mancava in carta.',
      immagini: [
        'assets/prodotti/web/amaro-korva.jpg',
        'assets/prodotti/web/amaro-korva-retro-1.jpg',
        'assets/prodotti/web/amaro-korva-retro-2.jpg'
      ]
    }
  ];


  /**
   * Eventi (locandine). Prima i prossimi eventi (con "Prenota"), poi quelli
   * conclusi in archivio, dal più recente.
   * data: 'AAAA-MM-GG' · ora: facoltativa
   * locandine: una o più immagini in assets/eventi/ (formato verticale);
   *   con più locandine, nell'ingrandimento si sfogliano.
   * prenotazione: facoltativo, numero per prenotare il tavolo (altrimenti
   *   si prenota tramite il WhatsApp di S.F.M.).
   */
  const EVENTI = [
    {
      titolo: 'L\'ora del calice',
      data: '2026-10-09',
      ora: '19:00',
      luogo: 'Lo Sbagliato · Via Gandini 24, Ferrara',
      descrizione: 'Mostra d\'arte contemporanea e degustazione guidata, con le violiniste Cristina Direnzo e Sara Suci.',
      locandine: ['assets/eventi/2026-10-09-ora-del-calice-lo-sbagliato.jpg']
    },
    {
      titolo: 'L\'ora del calice',
      data: '2026-10-09',
      ora: '19:00',
      luogo: 'Lo Sbagliato · Via Gandini 24, Ferrara',
      descrizione: 'Mostra d\'arte contemporanea, degustazione guidata e musica live.',
      locandine: ['assets/eventi/2026-10-09-ora-del-calice-lo-sbagliato-b.jpg'],
      prenotazione: '+393339532029'
    },
    {
      titolo: 'L\'ora del calice',
      data: '2026-09-11',
      ora: '19:00',
      luogo: 'La Bode Ristobar · Via Boccacanale di S. Stefano 36, Ferrara',
      descrizione: 'Degustazione guidata con musica jazz country e un menu di sfiziosità e cucina tipica.',
      locandine: ['assets/eventi/2026-09-11-ora-del-calice-la-bode.jpg']
    }
  ];

  /** Quanti eventi conclusi mostrare al massimo in archivio. */
  const EVENTI_CONCLUSI_MAX = 8;


  /* ========================================================================
     02. UTILITÀ
     ======================================================================== */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));

  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const prefersReducedMotion = () => motionQuery.matches;

  /** Costruisce un link wa.me con testo precompilato e codificato. */
  function buildWhatsAppUrl(text) {
    const base = `https://wa.me/${WHATSAPP_NUMBER}`;
    return text ? `${base}?text=${encodeURIComponent(text)}` : base;
  }

  /** Apre un URL in una nuova scheda; se il popup è bloccato usa la scheda corrente. */
  function openExternal(url) {
    const win = window.open(url, '_blank');
    if (win) {
      win.opener = null;
    } else {
      window.location.href = url;
    }
  }

  /** Escape dei caratteri HTML per i contenuti inseriti via template. */
  function escapeHTML(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  const clamp = (v, min, max) => Math.min(Math.max(v, min), max);
  const lerp = (a, b, t) => a + (b - a) * t;
  /** Transizione morbida da 0 a 1 quando x passa da a a b. */
  const smoothstep = (a, b, x) => {
    const t = clamp((x - a) / (b - a), 0, 1);
    return t * t * (3 - 2 * t);
  };


  /**
   * Visualizzatore a tutto schermo condiviso (foto prodotti e locandine).
   * openViewer(['a.jpg', 'b.jpg'], indiceIniziale, 'Titolo')
   * Con più immagini: frecce, tasti ← → e scorrimento col dito.
   */
  const openViewer = (() => {
    let viewer, img, vPrev, vNext, vCount;
    let images = [];
    let title = '';
    let index = 0;

    const show = (i) => {
      const n = images.length;
      index = (i + n) % n;
      img.src = images[index];
      img.alt = n > 1 ? `${title} (${index + 1} di ${n})` : title;
      [vPrev, vNext, vCount].forEach((el) => { if (el) el.hidden = n < 2; });
      if (vCount) vCount.textContent = `${index + 1} / ${n}`;
    };

    const setup = () => {
      viewer = $('#image-viewer');
      if (!viewer) return false;
      img = $('.poster-viewer__img', viewer);
      vPrev = $('[data-viewer-prev]', viewer);
      vNext = $('[data-viewer-next]', viewer);
      vCount = $('.poster-viewer__count', viewer);

      viewer.addEventListener('click', (ev) => {
        if (ev.target === viewer || ev.target.closest('[data-close]')) viewer.close();
      });
      vPrev.addEventListener('click', () => show(index - 1));
      vNext.addEventListener('click', () => show(index + 1));
      viewer.addEventListener('keydown', (ev) => {
        if (images.length < 2) return;
        if (ev.key === 'ArrowLeft') show(index - 1);
        if (ev.key === 'ArrowRight') show(index + 1);
      });
      // Scorrimento col dito
      let startX = null;
      img.addEventListener('pointerdown', (ev) => { startX = ev.clientX; });
      img.addEventListener('pointerup', (ev) => {
        if (startX === null || images.length < 2) return;
        const dx = ev.clientX - startX;
        if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
        startX = null;
      });
      return true;
    };

    return (list, start = 0, label = '') => {
      if (!viewer && !setup()) return;
      images = list;
      title = label;
      show(start);
      if (typeof viewer.showModal === 'function') viewer.showModal();
      else window.open(list[start], '_blank');
    };
  })();


  /* ========================================================================
     02b. CONSENSO COOKIE (GDPR / linee guida Garante Privacy 2021)
     - Al primo accesso compare il banner con "Rifiuta" e "Accetta" di pari
       evidenza e "Personalizza"; chiudere con la X equivale a rifiutare.
     - Il sito usa solo: archiviazione tecnica della scelta (localStorage) e,
       previo consenso, la mappa di Google (cookie di terze parti).
     - La scelta dura 6 mesi, poi viene richiesta di nuovo.
     - window.SFMConsent: get() / open() / on(categoria, callback)
     ======================================================================== */
  const CONSENT_KEY = 'sfm-consenso';
  const CONSENT_VERSION = 1;
  const CONSENT_MAX_DAYS = 180;
  const CONSENT_CATEGORIES = [
    {
      id: 'necessari',
      nome: 'Tecnici e necessari',
      testo: 'Salvano le tue preferenze sui cookie. Sempre attivi: senza questi il sito non può ricordare la tua scelta.',
      fisso: true
    },
    {
      id: 'mappe',
      nome: 'Contenuti di terze parti (Google Maps)',
      testo: 'Mostrano la mappa interattiva di Google nella sezione Contatti. Google può impostare cookie propri.'
    }
  ];

  const SFMConsent = (() => {
    const listeners = {};
    let state = null;

    const read = () => {
      try {
        const raw = JSON.parse(localStorage.getItem(CONSENT_KEY));
        if (!raw || raw.v !== CONSENT_VERSION) return null;
        const ageDays = (Date.now() - new Date(raw.data).getTime()) / 86400000;
        return ageDays > CONSENT_MAX_DAYS ? null : raw;
      } catch (err) {
        return null;
      }
    };

    const save = (choices) => {
      state = { v: CONSENT_VERSION, data: new Date().toISOString(), ...choices, necessari: true };
      try { localStorage.setItem(CONSENT_KEY, JSON.stringify(state)); } catch (err) { /* archiviazione non disponibile */ }
      CONSENT_CATEGORIES.forEach((c) => {
        if (state[c.id]) (listeners[c.id] || []).forEach((fn) => fn());
      });
      document.dispatchEvent(new CustomEvent('sfm:consenso', { detail: state }));
    };

    const allowed = (id) => !!(state && state[id]);

    const on = (id, fn) => {
      (listeners[id] = listeners[id] || []).push(fn);
      if (allowed(id)) fn();
    };

    // --- Banner ---------------------------------------------------------------
    let banner = null;
    let lastFocus = null;

    const build = () => {
      banner = document.createElement('div');
      banner.className = 'cookie-banner';
      banner.setAttribute('role', 'dialog');
      banner.setAttribute('aria-modal', 'false');
      banner.setAttribute('aria-labelledby', 'cookie-title');
      banner.setAttribute('aria-describedby', 'cookie-desc');
      banner.innerHTML = `
        <button class="cookie-banner__close" type="button" data-cookie="rifiuta" aria-label="Chiudi e rifiuta i cookie facoltativi">
          <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M6 6l12 12M18 6L6 18"/></svg>
        </button>
        <p class="cookie-banner__title" id="cookie-title">Rispettiamo la tua privacy</p>
        <p class="cookie-banner__text" id="cookie-desc">
          Usiamo solo cookie tecnici e, con il tuo consenso, contenuti di terze parti come la mappa di Google.
          Nessun cookie di profilazione o pubblicità. Puoi cambiare idea in qualsiasi momento da
          «Preferenze cookie» in fondo alla pagina. Dettagli nella <a class="link" href="cookie-policy.html">Cookie Policy</a>.
        </p>
        <div class="cookie-banner__prefs" hidden>
          ${CONSENT_CATEGORIES.map((c) => `
            <label class="cookie-pref">
              <span class="cookie-pref__text">
                <span class="cookie-pref__name">${c.nome}</span>
                <span class="cookie-pref__desc">${c.testo}</span>
              </span>
              <span class="switch">
                <input type="checkbox" data-cat="${c.id}" ${c.fisso ? 'checked disabled' : ''}>
                <span class="switch__track" aria-hidden="true"></span>
              </span>
            </label>`).join('')}
        </div>
        <div class="cookie-banner__actions">
          <button class="btn btn--outline" type="button" data-cookie="rifiuta">Rifiuta</button>
          <button class="btn btn--solid" type="button" data-cookie="accetta">Accetta</button>
          <button class="cookie-banner__more link" type="button" data-cookie="personalizza">Personalizza</button>
          <button class="btn btn--solid" type="button" data-cookie="salva" hidden>Salva le scelte</button>
        </div>`;
      document.body.appendChild(banner);

      const prefs = $('.cookie-banner__prefs', banner);
      const showPrefs = (open) => {
        prefs.hidden = !open;
        $('[data-cookie="personalizza"]', banner).hidden = open;
        $('[data-cookie="salva"]', banner).hidden = !open;
        $('[data-cookie="accetta"]', banner).hidden = open;
      };

      banner.addEventListener('click', (ev) => {
        const btn = ev.target.closest('[data-cookie]');
        if (!btn) return;
        const action = btn.dataset.cookie;
        if (action === 'personalizza') {
          showPrefs(true);
          return;
        }
        const choices = {};
        CONSENT_CATEGORIES.forEach((c) => {
          if (c.fisso) return;
          if (action === 'accetta') choices[c.id] = true;
          else if (action === 'rifiuta') choices[c.id] = false;
          else choices[c.id] = $(`input[data-cat="${c.id}"]`, banner).checked;
        });
        save(choices);
        close();
      });

      banner.addEventListener('keydown', (ev) => {
        if (ev.key === 'Escape' && state) close();
      });
      banner._showPrefs = showPrefs;
    };

    const open = (withPrefs = false) => {
      if (!banner) build();
      lastFocus = document.activeElement;
      CONSENT_CATEGORIES.forEach((c) => {
        const box = $(`input[data-cat="${c.id}"]`, banner);
        if (box && !c.fisso) box.checked = allowed(c.id);
      });
      banner._showPrefs(withPrefs);
      banner.hidden = false;
      requestAnimationFrame(() => banner.classList.add('is-open'));
      const first = $(withPrefs ? 'input:not([disabled])' : '[data-cookie="accetta"]', banner);
      if (first) setTimeout(() => first.focus({ preventScroll: true }), 50);
    };

    const close = () => {
      if (!banner) return;
      banner.classList.remove('is-open');
      setTimeout(() => { banner.hidden = true; }, 400);
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    };

    const init = () => {
      state = read();
      if (!state) open(false);
      document.addEventListener('click', (ev) => {
        if (ev.target.closest('[data-cookie-settings]')) {
          ev.preventDefault();
          open(true);
        }
      });
    };

    return { init, on, open, get: () => state, accept: (id) => save({ ...(state || {}), [id]: true }) };
  })();
  window.SFMConsent = SFMConsent;

  /** Mappa di Google: caricata solo con il consenso "mappe". */
  function initConsentMap() {
    const box = $('[data-consent-map]');
    if (!box) return;
    const iframe = $('iframe', box);
    const load = () => {
      if (!iframe.getAttribute('src')) iframe.src = iframe.dataset.src;
      iframe.hidden = false;
      box.classList.add('is-loaded');
    };
    SFMConsent.on('mappe', load);
    const btn = $('[data-accept-maps]', box);
    if (btn) btn.addEventListener('click', () => SFMConsent.accept('mappe'));
  }


  /* ========================================================================
     03. HEADER, MENU MOBILE E LINK ATTIVI
     ======================================================================== */
  function initHeader() {
    const header = $('.site-header');
    if (!header) return;

    // Header trasparente sopra l'hero, nero con blur dopo lo scroll
    let ticking = false;
    const update = () => {
      header.classList.toggle('is-scrolled', window.scrollY > 40);
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }, { passive: true });
    update();
  }

  function initMobileNav() {
    const header = $('.site-header');
    const toggle = $('.nav-toggle');
    const nav = $('#main-nav');
    if (!toggle || !nav) return;

    const desktopQuery = window.matchMedia('(min-width: 960px)');

    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
      nav.classList.toggle('is-open', open);
      header.classList.toggle('is-menu-open', open);
      document.body.classList.toggle('is-locked', open);
      if (open) {
        const first = $('a', nav);
        if (first) window.setTimeout(() => first.focus(), 50);
      }
    };

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    // Chiude il menu al click su una voce (lo scroll fluido è gestito via CSS)
    $$('a', nav).forEach((link) => {
      link.addEventListener('click', () => setOpen(false));
    });

    // Esc per chiudere e restituire il focus al pulsante
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    // Se si passa a desktop con il menu aperto, lo si chiude
    desktopQuery.addEventListener('change', (e) => {
      if (e.matches) setOpen(false);
    });
  }

  /** Evidenzia nel menu la sezione attualmente visibile. */
  function initActiveLinks() {
    const links = $$('.main-nav__link');
    if (!links.length || !('IntersectionObserver' in window)) return;

    const byId = new Map(links.map((l) => [l.getAttribute('href').slice(1), l]));
    // La sezione "richieste" appartiene all'area Contatti
    const alias = { richieste: 'contatti' };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const id = alias[entry.target.id] || entry.target.id;
        links.forEach((l) => l.classList.remove('is-active'));
        const active = byId.get(id);
        if (active) active.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    $$('main section[id]').forEach((s) => observer.observe(s));
  }


  /* ========================================================================
     04. ANIMAZIONI DI COMPARSA
     ======================================================================== */
  function initReveal() {
    const items = $$('.reveal');
    if (!items.length) return;

    // Ritardo sfalsato per gli elementi fratelli (griglie, liste)
    items.forEach((el) => {
      const siblings = Array.from(el.parentElement.children).filter((c) => c.classList.contains('reveal'));
      const index = siblings.indexOf(el);
      if (index > 0) el.style.setProperty('--reveal-delay', `${Math.min(index, 6) * 90}ms`);
    });

    if (prefersReducedMotion() || !('IntersectionObserver' in window)) {
      items.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    items.forEach((el) => observer.observe(el));
  }

  /* ========================================================================
     05. PRODOTTI (GRIGLIA + FILTRI)
     ======================================================================== */

  /** Segnaposto grafico (bottiglia a linea) per prodotti senza immagine. */
  const PLACEHOLDER_SVG = `
    <svg viewBox="0 0 60 160" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M25 6h10v4H25zM25.5 10v30c0 6-13.5 12-13.5 26v84c0 2.2 1.8 4 4 4h28c2.2 0 4-1.8 4-4V66c0-14-13.5-20-13.5-26V10"/>
      <path d="M12 86h36M12 124h36" opacity=".6"/>
      <path d="M20 100h20M23 108h14" opacity=".6"/>
    </svg>`;

  function productMessage(p) {
    return `Buongiorno, vorrei informazioni sul prodotto: ${p.nome} – ${p.cantina}`;
  }

  function showProductPlaceholder(media) {
    $$('.product__slides, .product__nav, .product__dots', media).forEach((el) => el.remove());
    if ($('.product__placeholder', media)) return;
    const ph = document.createElement('div');
    ph.className = 'product__placeholder';
    ph.innerHTML = PLACEHOLDER_SVG;
    media.appendChild(ph);
  }

  /** Card prodotto: galleria di foto scorrevole + link "Richiedi info". */
  function createProductItem(p, index) {
    const li = document.createElement('li');
    li.className = 'product-item';
    li.style.setProperty('--i', index);

    const categoria = CATEGORIE[p.categoria] || '';
    const nomeCompleto = `${p.nome} – ${p.cantina}`;
    let images = (p.immagini || (p.immagine ? [p.immagine] : [])).slice();
    const n = images.length;
    const multi = n > 1;

    li.innerHTML = `
      <article class="product">
        <div class="product__media">
          <span class="product__badge">${escapeHTML(categoria)}</span>
          ${n ? `<div class="product__slides">
            ${images.map((src, i) => `
              <button class="product__slide" type="button" data-i="${i}" aria-label="Ingrandisci la foto ${i + 1} di ${n}: ${escapeHTML(nomeCompleto)}">
                <img src="${escapeHTML(src)}" alt="${escapeHTML(nomeCompleto)}${multi ? ` (foto ${i + 1})` : ''}" loading="lazy" decoding="async" width="750" height="1000">
              </button>`).join('')}
          </div>` : ''}
          ${multi ? `
            <button class="product__nav product__nav--prev" type="button" aria-label="Foto precedente" disabled>
              <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 5l-7 7 7 7"/></svg>
            </button>
            <button class="product__nav product__nav--next" type="button" aria-label="Foto successiva">
              <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5l7 7-7 7"/></svg>
            </button>
            <div class="product__dots" aria-hidden="true">${images.map((_, i) => `<span class="product__dot${i === 0 ? ' is-active' : ''}"></span>`).join('')}</div>` : ''}
        </div>
        <div class="product__body">
          <span class="product__region">${escapeHTML(p.regione)}</span>
          <h3 class="product__name">${escapeHTML(p.nome)}</h3>
          <p class="product__winery">${escapeHTML(p.cantina)}</p>
          <p class="product__desc">${escapeHTML(p.descrizione)}</p>
          <a class="product__cta" href="${buildWhatsAppUrl(productMessage(p))}" target="_blank" rel="noopener"
             aria-label="Richiedi informazioni: ${escapeHTML(nomeCompleto)}">
            <span>Richiedi info</span>
            <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
        </div>
      </article>`;

    const media = $('.product__media', li);
    if (!n) {
      showProductPlaceholder(media);
      return li;
    }

    const slides = $('.product__slides', media);
    const prev = $('.product__nav--prev', media);
    const next = $('.product__nav--next', media);
    const dots = $$('.product__dot', media);

    // Foto che non si caricano: tolte dalla galleria (se nessuna resta → segnaposto)
    $$('.product__slide img', media).forEach((img) => {
      img.addEventListener('error', () => {
        const slide = img.closest('.product__slide');
        images = images.filter((src) => src !== img.getAttribute('src'));
        slide.remove();
        if (!images.length) showProductPlaceholder(media);
      }, { once: true });
    });

    // Clic sulla foto → visualizzatore a tutto schermo, dalla foto cliccata
    slides.addEventListener('click', (ev) => {
      const slide = ev.target.closest('.product__slide');
      if (!slide) return;
      const src = $('img', slide).getAttribute('src');
      openViewer(images, Math.max(0, images.indexOf(src)), nomeCompleto);
    });

    if (multi) {
      const current = () => Math.round(slides.scrollLeft / slides.clientWidth);
      const go = (i) => slides.scrollTo({ left: i * slides.clientWidth, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
      const update = () => {
        const i = current();
        const count = $$('.product__slide', slides).length;
        dots.forEach((d, k) => d.classList.toggle('is-active', k === i));
        if (prev) prev.disabled = i <= 0;
        if (next) next.disabled = i >= count - 1;
      };
      prev.addEventListener('click', () => go(current() - 1));
      next.addEventListener('click', () => go(current() + 1));
      slides.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    }

    return li;
  }

  function initProducts() {
    const grid = $('#products-grid');
    if (!grid) return;
    const filters = $$('.filter');

    // Nasconde i filtri delle categorie che non hanno (ancora) prodotti:
    // ricompaiono da soli quando si aggiunge un prodotto di quella categoria.
    filters.forEach((btn) => {
      const cat = btn.dataset.filter;
      if (cat !== 'tutti' && !PRODOTTI.some((p) => p.categoria === cat)) btn.hidden = true;
    });

    const render = (filter) => {
      const list = filter === 'tutti' ? PRODOTTI : PRODOTTI.filter((p) => p.categoria === filter);
      const fragment = document.createDocumentFragment();

      if (!list.length) {
        const empty = document.createElement('li');
        empty.className = 'products__empty';
        empty.textContent = 'Nessun prodotto in questa categoria al momento. Contattaci per conoscere le novità.';
        fragment.appendChild(empty);
      } else {
        list.forEach((p, i) => fragment.appendChild(createProductItem(p, i)));
      }

      grid.replaceChildren(fragment);
    };

    filters.forEach((btn) => {
      btn.addEventListener('click', () => {
        if (btn.classList.contains('is-active')) return;
        filters.forEach((b) => {
          const active = b === btn;
          b.classList.toggle('is-active', active);
          b.setAttribute('aria-pressed', String(active));
        });
        render(btn.dataset.filter);
      });
    });

    render('tutti');
  }


  /* ========================================================================
     05b. EVENTI (LOCANDINE)
     ======================================================================== */
  function initEvents() {
    const track = $('#events-track');
    if (!track) return;
    const empty = $('#events-empty');
    const prev = $('[data-events-prev]');
    const next = $('[data-events-next]');

    // 'AAAA-MM-GG' → data locale (evita lo slittamento di fuso orario)
    const parseDate = (str) => {
      const [y, m, d] = str.split('-').map(Number);
      return new Date(y, m - 1, d);
    };
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const all = EVENTI.map((e) => ({
      ...e,
      date: parseDate(e.data),
      locandine: e.locandine || (e.locandina ? [e.locandina] : [])
    }));
    const upcoming = all.filter((e) => e.date >= today).sort((a, b) => a.date - b.date);
    const past = all.filter((e) => e.date < today).sort((a, b) => b.date - a.date).slice(0, EVENTI_CONCLUSI_MAX);
    const list = [...upcoming, ...past];

    if (!list.length) {
      track.hidden = true;
      if (empty) empty.hidden = false;
      $$('.events__nav').forEach((n) => (n.hidden = true));
      return;
    }

    const fmtDay = new Intl.DateTimeFormat('it-IT', { day: '2-digit' });
    const fmtMonth = new Intl.DateTimeFormat('it-IT', { month: 'short' });
    const fmtLong = new Intl.DateTimeFormat('it-IT', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

    const fallbackPoster = (e) => `
      <span class="event__fallback" aria-hidden="true">
        <span class="event__fallback-kicker">Serata evento</span>
        <span class="event__fallback-title">${escapeHTML(e.titolo)}</span>
        <span class="event__fallback-brand">S.F.M. Distribuzione</span>
      </span>`;

    track.innerHTML = list.map((e, i) => {
      const concluso = e.date < today;
      const quando = `${fmtLong.format(e.date)}${e.ora ? `, ore ${e.ora}` : ''}`;
      const msg = `Buongiorno, vorrei prenotare per l'evento "${e.titolo}" di ${quando}.`;
      const prenota = e.prenotazione
        ? `<a class="event__cta link" href="tel:${escapeHTML(e.prenotazione)}">Prenota il tavolo</a>`
        : `<a class="event__cta link" href="${buildWhatsAppUrl(msg)}" target="_blank" rel="noopener">
             <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#icon-whatsapp"/></svg>
             Prenota su WhatsApp
           </a>`;
      const piu = e.locandine.length > 1 ? `<span class="event__count" aria-hidden="true">1 / ${e.locandine.length}</span>` : '';
      return `
        <li class="event${concluso ? ' is-past' : ''}">
          <button class="event__poster" type="button" data-index="${i}" aria-label="Ingrandisci la locandina: ${escapeHTML(e.titolo)}, ${quando}">
            <span class="event__date" aria-hidden="true">
              <span class="event__day">${fmtDay.format(e.date)}</span>
              <span class="event__month">${fmtMonth.format(e.date).replace('.', '')}</span>
            </span>
            ${concluso ? '<span class="event__status">Concluso</span>' : ''}
            ${piu}
            ${fallbackPoster(e)}
          </button>
          <div class="event__info">
            <h3 class="event__title">${escapeHTML(e.titolo)}</h3>
            <p class="event__meta"><time datetime="${e.data}${e.ora ? `T${e.ora}` : ''}">${quando}</time></p>
            ${e.luogo ? `<p class="event__meta">${escapeHTML(e.luogo)}</p>` : ''}
            ${e.descrizione ? `<p class="event__desc">${escapeHTML(e.descrizione)}</p>` : ''}
            ${concluso ? '' : prenota}
          </div>
        </li>`;
    }).join('');

    // Locandina in copertina: copre la grafica di riserva solo se si carica
    $$('.event__poster', track).forEach((btn) => {
      const e = list[Number(btn.dataset.index)];
      const disable = () => {
        btn.disabled = true; // niente da ingrandire: resta la locandina grafica
        btn.style.cursor = 'default';
      };
      if (!e.locandine.length) return disable();

      const img = new Image();
      img.className = 'event__img';
      img.alt = `Locandina: ${e.titolo}`;
      img.loading = 'lazy';
      img.decoding = 'async';
      img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true });
      img.addEventListener('error', () => { img.remove(); disable(); }, { once: true });
      img.src = e.locandine[0];
      btn.appendChild(img); // inserita subito: il caricamento "lazy" parte solo nel DOM

      btn.addEventListener('click', () => openViewer(e.locandine, 0, `Locandina: ${e.titolo}`));
    });

    // --- Frecce della fila: scorrono di una locandina alla volta ---
    const step = () => {
      const first = track.querySelector('.event');
      return first ? first.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0) : track.clientWidth;
    };
    const updateArrows = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    };
    const behavior = prefersReducedMotion() ? 'auto' : 'smooth';
    if (prev) prev.addEventListener('click', () => track.scrollBy({ left: -step(), behavior }));
    if (next) next.addEventListener('click', () => track.scrollBy({ left: step(), behavior }));
    track.addEventListener('scroll', updateArrows, { passive: true });
    window.addEventListener('resize', updateArrows);
    updateArrows();
  }


  /* ========================================================================
     06. LINK WHATSAPP E RECENSIONI GOOGLE
     ======================================================================== */

  /** Aggiorna tutti i link [data-wa] con il numero definito in WHATSAPP_NUMBER. */
  function initWhatsAppLinks() {
    $$('[data-wa]').forEach((a) => {
      a.href = buildWhatsAppUrl(a.dataset.waText || '');
    });
  }

  /** Sezione recensioni: voto, stelle, link e schede (da GOOGLE_REVIEWS). */
  function initReviews() {
    const section = $('#recensioni');
    if (!section) return;
    const { voto, totale, link, linkScrivi, recensioni } = GOOGLE_REVIEWS;

    const stars = $('[data-reviews-stars]', section);
    if (stars) stars.style.setProperty('--fill', `${voto ? (voto / 5) * 100 : 100}%`);

    const rating = $('[data-reviews-rating]', section);
    if (rating && voto) {
      rating.textContent = voto.toLocaleString('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
      rating.hidden = false;
    }

    const count = $('[data-reviews-count]', section);
    if (count) {
      count.textContent = totale
        ? `${totale} recensioni su Google`
        : 'Le opinioni dei ristoratori che lavorano con noi, su Google.';
    }

    const read = $('[data-reviews-read]', section);
    const write = $('[data-reviews-write]', section);
    if (read) read.href = link;
    if (write) write.href = linkScrivi || link;

    const list = $('#reviews-list');
    if (list && recensioni.length) {
      list.innerHTML = recensioni.map((r) => `
        <li class="review reveal">
          <span class="stars" style="--fill:${(r.voto / 5) * 100}%" role="img" aria-label="${r.voto} stelle su 5"></span>
          <p class="review__text">“${escapeHTML(r.testo)}”</p>
          <p class="review__author">${escapeHTML(r.autore)}</p>
        </li>`).join('');
      list.hidden = false;
    }
  }


  /** Chi siamo: mostra la foto se esiste, altrimenti resta il calice disegnato. */
  function initAboutPhoto() {
    const img = $('.about__photo');
    if (!img) return;
    const figure = img.closest('.about__visual');
    const ok = () => figure.classList.add('has-photo');
    const fail = () => img.remove();
    if (img.complete) {
      img.naturalWidth ? ok() : fail();
    } else {
      img.addEventListener('load', ok, { once: true });
      img.addEventListener('error', fail, { once: true });
    }
  }

  /** Immagine di chiusura: se il file manca la sezione viene nascosta. */
  function initStatement() {
    const section = $('#frase');
    const img = section ? $('.statement__img', section) : null;
    if (!img) return;
    const fail = () => section.classList.add('no-image');
    if (img.complete && img.naturalWidth === 0) fail();
    else img.addEventListener('error', fail, { once: true });
  }


  /* ========================================================================
     07. FORM RICHIESTE
     ======================================================================== */
  function initForm() {
    const form = $('#request-form');
    if (!form) return;
    const success = $('#form-success');

    // Regole di validazione: ritornano il messaggio d'errore oppure ''
    const rules = {
      nome: (v) => {
        if (!v) return 'Inserisci il tuo nome e cognome.';
        if (v.length < 3) return 'Il nome sembra troppo corto.';
        return '';
      },
      locale: (v) => (v ? '' : 'Inserisci il nome del tuo locale.'),
      citta: (v) => (v ? '' : 'Indica la città in cui si trova il locale.'),
      tipologia: (v) => (v ? '' : 'Scegli la tipologia del tuo locale.'),
      email: (v) => {
        if (!v) return 'Inserisci il tuo indirizzo email.';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return 'Indirizzo email non valido (es. nome@dominio.it).';
        return '';
      },
      telefono: (v) => {
        if (!v) return 'Inserisci un numero di telefono.';
        const digits = v.replace(/\D/g, '');
        if (!/^[+\d\s().\-/]+$/.test(v) || digits.length < 6 || digits.length > 15) {
          return 'Numero di telefono non valido (solo cifre, spazi e +).';
        }
        return '';
      },
      messaggio: (v) => (v.length > 1000 ? 'Il messaggio può contenere al massimo 1000 caratteri.' : ''),
      privacy: (v) => (v ? '' : 'Per inviare la richiesta è necessario accettare l\'informativa privacy.')
    };

    const tipologiaGroup = $('.chips-field[role="radiogroup"]', form);

    /** Valore di un campo (gestisce gruppi radio e checkbox singola). */
    const valueOf = (name) => {
      const el = form.elements[name];
      if (name === 'privacy') return el.checked;
      return (el.value || '').trim(); // RadioNodeList.value = radio selezionato
    };

    /** Elemento su cui segnalare l'errore (il gruppo per le "pillole"). */
    const targetOf = (name) => (name === 'tipologia' ? tipologiaGroup : form.elements[name]);

    const validateField = (name) => {
      const message = rules[name](valueOf(name));
      const errorEl = $(`#e-${name}`);
      if (errorEl) errorEl.textContent = message;
      const target = targetOf(name);
      if (target) target.setAttribute('aria-invalid', message ? 'true' : 'false');
      return !message;
    };

    // Validazione "gentile": al blur, poi in tempo reale sui campi già segnalati
    ['nome', 'locale', 'citta', 'email', 'telefono', 'messaggio'].forEach((name) => {
      const el = form.elements[name];
      el.addEventListener('blur', () => {
        if (el.value || el.dataset.touched) validateField(name);
        el.dataset.touched = '1';
      });
      el.addEventListener('input', () => {
        if (el.getAttribute('aria-invalid') === 'true') validateField(name);
      });
    });
    form.addEventListener('change', (e) => {
      if (e.target.name === 'tipologia' && tipologiaGroup.getAttribute('aria-invalid') === 'true') validateField('tipologia');
      if (e.target.name === 'privacy' && e.target.getAttribute('aria-invalid') === 'true') validateField('privacy');
    });

    /** Compone il messaggio con tutti i dati del form. */
    const composeMessage = (d, bold) => {
      const b = (t) => (bold ? `*${t}*` : t);
      return [
        b('Richiesta listino HORECA — S.F.M. Distribuzione'),
        '',
        `Nome: ${d.nome}`,
        `Locale: ${d.locale} (${d.tipologia})`,
        `Città: ${d.citta}`,
        `Email: ${d.email}`,
        `Telefono: ${d.telefono}`,
        ...(d.interessi.length ? [`Interessi: ${d.interessi.join(', ')}`] : []),
        ...(d.messaggio ? ['', 'Messaggio:', d.messaggio] : [])
      ].join('\n');
    };

    /*
     * ALTERNATIVA: invio a un endpoint (es. Formspree) tramite fetch.
     * Per usarla: impostare FORM_ENDPOINT in cima al file e, nel gestore "submit"
     * qui sotto, sostituire l'apertura di WhatsApp/email con:
     *
     *   inviaAEndpoint(data)
     *     .then(() => mostraConferma())
     *     .catch(() => alert('Si è verificato un errore. Riprova o scrivici su WhatsApp.'));
     *
     * async function inviaAEndpoint(data) {
     *   const res = await fetch(FORM_ENDPOINT, {
     *     method: 'POST',
     *     headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
     *     body: JSON.stringify(data)
     *   });
     *   if (!res.ok) throw new Error('Invio non riuscito');
     *   return res.json();
     * }
     */
    void FORM_ENDPOINT; // mantenuta per l'alternativa commentata qui sopra

    const mostraConferma = () => {
      form.reset();
      Object.keys(rules).forEach((name) => {
        const target = targetOf(name);
        if (target) target.removeAttribute('aria-invalid');
        const el = form.elements[name];
        if (el && el.dataset) delete el.dataset.touched;
      });
      success.hidden = false;
      success.focus({ preventScroll: true });
      success.scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth', block: 'center' });
    };

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      success.hidden = true;

      const invalid = Object.keys(rules).filter((name) => !validateField(name));
      if (invalid.length) {
        const first = invalid[0];
        const focusEl = first === 'tipologia' ? $('input[name="tipologia"]', form) : form.elements[first];
        if (focusEl) focusEl.focus();
        return;
      }

      const data = {
        nome: valueOf('nome'),
        locale: valueOf('locale'),
        tipologia: valueOf('tipologia'),
        citta: valueOf('citta'),
        email: valueOf('email'),
        telefono: valueOf('telefono'),
        interessi: $$('input[name="interessi"]:checked', form).map((i) => i.value),
        messaggio: valueOf('messaggio')
      };

      // Canale scelto dal pulsante premuto: WhatsApp (principale) o email
      const channel = (e.submitter && e.submitter.dataset.channel) || 'whatsapp';
      if (channel === 'email') {
        const subject = `Richiesta listino HORECA — ${data.locale}`;
        window.location.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(composeMessage(data, false))}`;
      } else {
        openExternal(buildWhatsAppUrl(composeMessage(data, true)));
      }
      mostraConferma();
    });
  }


  /* ========================================================================
     08. CURSORE PERSONALIZZATO
     ======================================================================== */
  function initCursor() {
    const cursor = $('.cursor');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (!cursor || !finePointer || prefersReducedMotion()) return;

    const pos = { x: -100, y: -100 };
    const target = { x: -100, y: -100 };
    let rafId = null;

    const loop = () => {
      pos.x = lerp(pos.x, target.x, 0.2);
      pos.y = lerp(pos.y, target.y, 0.2);
      cursor.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0)`;
      if (Math.abs(pos.x - target.x) > 0.1 || Math.abs(pos.y - target.y) > 0.1) {
        rafId = requestAnimationFrame(loop);
      } else {
        rafId = null;
      }
    };

    window.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      target.x = e.clientX;
      target.y = e.clientY;
      cursor.classList.add('is-visible');
      if (!rafId) rafId = requestAnimationFrame(loop);
    }, { passive: true });

    document.addEventListener('mouseleave', () => cursor.classList.remove('is-visible'));

    const interactive = 'a, button, select, label, summary, .filter';
    document.addEventListener('mouseover', (e) => {
      cursor.classList.toggle('is-hover', !!e.target.closest(interactive));
    });
  }


  /* ========================================================================
     09. HERO 3D (THREE.JS)
     Bottiglia di Vasia (Tenute De Giglio) ricostruita in 3D: vetro scuro
     (LatheGeometry), capsula, etichette fronte/retro reali come texture,
     particelle fluttuanti, luci drammatiche e parallasse mouse/giroscopio.
     Per cambiare vino basta modificare HERO_BOTTLE qui sotto.
     ======================================================================== */

  /**
   * Stato condiviso dello scroll dell'hero: "target" è la posizione reale
   * (0 = inizio sezione, 1 = fine), "progress" la versione ammorbidita
   * usata sia dai testi sia dalla scena 3D, così restano sincronizzati.
   */
  const heroScroll = { enabled: false, target: 0, progress: 0 };

  /** Momento (0–1) in cui il monogramma "atterra" nell'header. */
  const BRAND_DOCK = 0.14;

  function initHeroScroll() {
    const section = $('#hero');
    if (!section || prefersReducedMotion()) return;

    section.classList.add('is-scrolly');
    heroScroll.enabled = true;

    const header = $('.site-header');
    const headerLogo = $('.brand img');
    const mono = $('.hero__mono', section);
    const rest = $('.hero__brand-rest', section);
    const indicator = $('.scroll-indicator', section);
    const bar = $('.hero__progress-bar', section);
    const chapters = $$('.hero-chapter', section).map((el) => ({
      el,
      from: parseFloat(el.dataset.from),
      to: parseFloat(el.dataset.to)
    }));
    const FADE = 0.05; // durata delle dissolvenze (in frazione di scroll)
    const isTouch = window.matchMedia('(pointer: coarse)').matches;

    // --- Geometria in cache: durante lo scroll si legge solo window.scrollY,
    //     così il browser non deve ricalcolare l'impaginazione a ogni evento.
    let sectionTop = 0;
    let sectionH = 0;
    const measureGeometry = () => {
      sectionTop = section.getBoundingClientRect().top + window.scrollY;
      sectionH = section.offsetHeight;
    };
    const measure = () => {
      const total = sectionH - window.innerHeight;
      heroScroll.target = total > 0 ? clamp((window.scrollY - sectionTop) / total, 0, 1) : 0;
    };

    // "Volo" del logo (tecnica FLIP): si misura la posizione del monogramma
    // nell'hero e quella del logo nell'header, poi lo scroll interpola tra
    // le due con translate + scale.
    let flip = { dx: 0, dy: 0, s: 1 };
    const measureFlip = () => {
      if (!mono || !headerLogo) return;
      const prev = mono.style.transform;
      mono.style.transform = 'none';
      const a = mono.getBoundingClientRect();
      const b = headerLogo.getBoundingClientRect();
      mono.style.transform = prev;
      if (!a.height) return;
      flip = { dx: b.left - a.left, dy: b.top - a.top, s: b.height / a.height };
    };

    // --- Scritture di stile solo quando il valore cambia davvero
    const set = (el, prop, value) => {
      const cache = el._sfm || (el._sfm = {});
      if (cache[prop] === value) return;
      cache[prop] = value;
      el.style[prop] = value;
    };
    const setVisible = (el, a) => {
      set(el, 'opacity', a.toFixed(3));
      set(el, 'visibility', a < 0.01 ? 'hidden' : 'visible');
    };
    let monoAnimating = !!(mono && mono.classList.contains('hero-in'));
    let brandHidden = null;

    const apply = (p) => {
      // 1. Logo: la scritta sfuma, il monogramma vola nell'header
      const k = smoothstep(0.01, BRAND_DOCK, p);
      if (mono) {
        set(mono, 'transform', `translate3d(${(flip.dx * k).toFixed(1)}px, ${(flip.dy * k).toFixed(1)}px, 0) scale(${lerp(1, flip.s, k).toFixed(4)})`);
        if (!monoAnimating) setVisible(mono, 1 - smoothstep(BRAND_DOCK - 0.008, BRAND_DOCK, p));
      }
      if (rest) {
        setVisible(rest, 1 - smoothstep(0, 0.05, p));
        set(rest, 'translate', `0 ${(smoothstep(0, 0.06, p) * 40).toFixed(1)}px`);
      }
      const hide = p < BRAND_DOCK - 0.004;
      if (header && hide !== brandHidden) {
        brandHidden = hide;
        header.classList.toggle('hide-brand', hide);
      }
      if (indicator) set(indicator, 'opacity', (1 - smoothstep(0, 0.04, p)).toFixed(3));

      // 2. Capitoli: dissolvenza in entrata e in uscita nel proprio intervallo
      chapters.forEach((c) => {
        const a = smoothstep(c.from, c.from + FADE, p) * (1 - smoothstep(c.to - FADE, c.to, p));
        setVisible(c.el, a);
        set(c.el, 'translate', `0 ${((1 - a) * 28).toFixed(1)}px`);
        const active = a > 0.5;
        if (c.active !== active) {
          c.active = active;
          c.el.classList.toggle('is-active', active);
        }
      });

      if (bar) set(bar, 'transform', `scaleX(${p.toFixed(4)})`);
    };

    // --- Inseguimento morbido dello scroll, indipendente dalla frequenza dello
    //     schermo (60/90/120 Hz): più reattivo su touch, più fluido col mouse.
    const FOLLOW = isTouch ? 16 : 10;
    let rafId = null;
    let lastT = 0;
    const tick = (now) => {
      const dt = lastT ? Math.min((now - lastT) / 1000, 0.1) : 1 / 60;
      lastT = now;
      heroScroll.progress += (heroScroll.target - heroScroll.progress) * (1 - Math.exp(-FOLLOW * dt));
      if (Math.abs(heroScroll.progress - heroScroll.target) < 0.0003) heroScroll.progress = heroScroll.target;
      apply(heroScroll.progress);
      if (heroScroll.progress !== heroScroll.target) {
        rafId = requestAnimationFrame(tick);
      } else {
        rafId = null;
        lastT = 0;
      }
    };
    const kick = () => {
      measure();
      if (!rafId) rafId = requestAnimationFrame(tick);
    };

    window.addEventListener('scroll', kick, { passive: true });

    // Resize: su telefono la barra degli indirizzi cambia solo l'altezza della
    // finestra; la geometria si rimisura solo quando cambia la larghezza.
    let lastW = window.innerWidth;
    window.addEventListener('resize', () => {
      if (window.innerWidth !== lastW) {
        lastW = window.innerWidth;
        measureGeometry();
        measureFlip();
        apply(heroScroll.progress);
      }
      kick();
    });
    window.addEventListener('load', () => { measureGeometry(); kick(); }, { once: true });

    // L'animazione d'ingresso del monogramma controlla la sua opacità:
    // finita quella, il controllo passa allo scroll.
    if (mono) {
      mono.addEventListener('animationend', () => {
        mono.classList.remove('hero-in');
        monoAnimating = false;
        measureFlip();
        apply(heroScroll.progress);
      }, { once: true });
      if (!mono.complete) mono.addEventListener('load', () => { measureFlip(); apply(heroScroll.progress); }, { once: true });
    }

    measureGeometry();
    measure();
    measureFlip();
    heroScroll.progress = heroScroll.target;
    apply(heroScroll.progress);
  }

  /** Vino mostrato nell'hero: texture delle etichette e colore del vetro. */
  const HERO_BOTTLE = {
    fronte: 'assets/hero/vasia-fronte.jpg',
    retro: 'assets/hero/vasia-retro.jpg',
    inline: 'assets/hero/etichette-inline.js', // copia per l'apertura da file://
    vetro: 0x000000,       // vetro scuro: solo riflessi, nessuna luce diffusa
    controluce: 0x5c0812,  // colore del vino sui bordi in controluce
    capsula: 0x0b0b0b,
    scrittaCapsula: 'TENUTE DE GIGLIO'
  };

  /** Stessa media query del CSS: testo a sinistra e bottiglia a destra. */
  const HERO_SIDE_QUERY = '(min-width: 560px) and (min-aspect-ratio: 1/1)';

  function initHero3D() {
    const section = $('#hero');          // sezione alta (scroll)
    if (!section) return;                // pagine senza hero (es. pagine legali)
    const hero = $('.hero', section);    // contenitore fisso con il canvas
    const canvas = $('#hero-canvas');
    if (!section || !hero || !canvas) return;

    if (typeof window.THREE === 'undefined') {
      hero.classList.add('no-webgl');
      return;
    }
    const THREE = window.THREE;

    // --- Profilo prestazioni -------------------------------------------------
    // Su telefoni, tablet e dispositivi con poca CPU/RAM si usa una versione
    // più leggera della scena (risoluzione, materiali, geometrie, particelle).
    const isMobile = window.matchMedia('(max-width: 767px)').matches;
    const lowPower = isMobile
      || window.matchMedia('(pointer: coarse)').matches
      || (navigator.hardwareConcurrency || 8) <= 4
      || (navigator.deviceMemory || 8) <= 4;
    const MAX_DPR = lowPower ? 1.5 : 2;          // densità massima dei pixel
    let dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);

    // --- Renderer -----------------------------------------------------------
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
    } catch (err) {
      hero.classList.add('no-webgl');
      return;
    }
    renderer.setClearColor(0x000000, 1);
    renderer.outputEncoding = THREE.sRGBEncoding;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;

    const sideQuery = window.matchMedia(HERO_SIDE_QUERY);

    // --- Scena e camera -----------------------------------------------------
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.035);

    const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
    const cameraBase = new THREE.Vector3(0, 0, 12);
    camera.position.copy(cameraBase);

    // --- Mappa d'ambiente "studio fotografico" ------------------------------
    // Una piccola scena con softbox luminosi viene convertita (PMREM) in mappa
    // di riflessione: sono i riflessi lunghi e morbidi tipici del packshot.
    const pmrem = new THREE.PMREMGenerator(renderer);
    const envScene = new THREE.Scene();
    envScene.background = new THREE.Color(0x000000);
    const envMats = [];
    const softbox = (w, h, intensity, x, y, z, ry = 0, rx = 0) => {
      const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(1, 1, 1).multiplyScalar(intensity), side: THREE.DoubleSide });
      envMats.push(mat);
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
      m.position.set(x, y, z);
      m.rotation.set(rx, ry, 0);
      envScene.add(m);
    };
    softbox(2.6, 12, 4, -6, 0, 2, Math.PI / 2);     // softbox grande a sinistra (key)
    softbox(0.35, 12, 7, 6, 0, 0.5, -Math.PI / 2);  // striscia netta a destra (rim)
    softbox(1.2, 12, 3, 3.5, 0, -6);                // striscia posteriore
    softbox(5, 5, 2, 0, 7, 0, 0, Math.PI / 2);       // softbox dall'alto
    softbox(9, 6, 0.05, 0, 0, 9);                   // riempimento frontale tenue
    const envMap = pmrem.fromScene(envScene, 0.035).texture;
    envMats.forEach((m) => m.dispose());
    pmrem.dispose();

    // --- Luci: key laterale forte + rim posteriore --------------------------
    scene.add(new THREE.AmbientLight(0xffffff, 0.12));

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
    keyLight.position.set(-5, 3, 5);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xffffff, 2.5);
    rimLight.position.set(5, 2, -6);
    scene.add(rimLight);

    const fillLight = new THREE.DirectionalLight(0xffffff, 0.6);
    fillLight.position.set(3, -1, 6);
    scene.add(fillLight);

    // --- Bottiglia bordolese (profilo ruotato con LatheGeometry) ------------
    // Coordinate: x = raggio, y = altezza (bottiglia alta 6, centrata sull'origine).
    // Fondo con rientranza, spalla morbida (curva di Bézier), collo e cercine.
    const BODY_R = 0.92;
    const WINE_LEVEL = 1.3; // altezza del vino (coordinate centrate)
    const profile = [];
    const add = (x, y) => profile.push(new THREE.Vector2(x, y - 3));
    [[0, 0.16], [0.4, 0.11], [0.68, 0.03], [0.8, 0], [0.875, 0.015], [0.908, 0.06], [BODY_R, 0.15], [BODY_R, 3.3]]
      .forEach(([x, y]) => add(x, y));
    new THREE.CubicBezierCurve(
      new THREE.Vector2(BODY_R, 3.3), new THREE.Vector2(BODY_R, 3.98),
      new THREE.Vector2(0.36, 4.12), new THREE.Vector2(0.305, 4.75)
    ).getPoints(20).slice(1).forEach((v) => add(v.x, v.y));
    [[0.29, 5.15], [0.285, 5.6], [0.33, 5.64], [0.345, 5.72], [0.345, 5.9], [0.33, 5.97], [0.3, 6.0], [0, 6.0]]
      .forEach(([x, y]) => add(x, y));

    const segments = lowPower ? 56 : 144;
    const bottle = new THREE.Group();
    const bodyGeo = new THREE.LatheGeometry(profile, segments);

    // Vetro scuro lucido
    const glassMat = new (lowPower ? THREE.MeshStandardMaterial : THREE.MeshPhysicalMaterial)({
      color: HERO_BOTTLE.vetro,
      metalness: 0,
      roughness: 0.05,
      ...(lowPower ? {} : { clearcoat: 1, clearcoatRoughness: 0.02, reflectivity: 0.7 }),
      envMap,
      envMapIntensity: 1.9
    });
    bottle.add(new THREE.Mesh(bodyGeo, glassMat));

    // "Controluce": guscio con effetto Fresnel che illumina i bordi della
    // bottiglia di rosso vino (sotto il livello del vino) e di grigio vetro
    // sopra, come quando la luce attraversa il vetro sui contorni.
    const rimMat = new THREE.ShaderMaterial({
      uniforms: {
        uWine: { value: new THREE.Color(HERO_BOTTLE.controluce) },
        uGlass: { value: new THREE.Color(0x3a3a3a) },
        uLevel: { value: WINE_LEVEL },
        uPower: { value: 4.2 }
      },
      vertexShader: `
        varying vec3 vN;
        varying vec3 vV;
        varying float vY;
        void main() {
          vY = position.y;
          vN = normalize(normalMatrix * normal);
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          vV = normalize(-mv.xyz);
          gl_Position = projectionMatrix * mv;
        }`,
      fragmentShader: `
        uniform vec3 uWine;
        uniform vec3 uGlass;
        uniform float uLevel;
        uniform float uPower;
        varying vec3 vN;
        varying vec3 vV;
        varying float vY;
        void main() {
          float f = pow(1.0 - clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0), uPower);
          vec3 c = mix(uWine, uGlass, smoothstep(uLevel - 0.06, uLevel + 0.06, vY));
          gl_FragColor = vec4(c * f, 1.0);
        }`,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    const rim = new THREE.Mesh(bodyGeo, rimMat);
    rim.scale.set(1.004, 1, 1.004);
    bottle.add(rim);

    // Capsula sul collo, con piccolo bordino in basso
    const capsuleProfile = [
      [0.318, 1.78], [0.31, 1.8], [0.304, 2.0], [0.298, 2.6], [0.338, 2.64], [0.352, 2.72],
      [0.352, 2.9], [0.336, 2.975], [0.305, 3.008], [0, 3.008]
    ].map(([x, y]) => new THREE.Vector2(x, y));
    const capsuleMat = new THREE.MeshStandardMaterial({ color: HERO_BOTTLE.capsula, roughness: 0.38, metalness: 0.45, envMap, envMapIntensity: 0.9 });
    bottle.add(new THREE.Mesh(new THREE.LatheGeometry(capsuleProfile, segments), capsuleMat));

    // Scritta stampata sulla capsula (come sulla bottiglia vera)
    if (HERO_BOTTLE.scrittaCapsula) {
      const capCanvas = document.createElement('canvas');
      capCanvas.width = 1024;
      capCanvas.height = 96;
      const capTex = new THREE.CanvasTexture(capCanvas);
      capTex.encoding = THREE.sRGBEncoding;
      const drawCapsuleText = () => {
        const c = capCanvas.getContext('2d');
        c.clearRect(0, 0, 1024, 96);
        c.fillStyle = '#e8e8e8';
        c.font = '600 46px "Helvetica Neue", Helvetica, Arial, sans-serif';
        c.textAlign = 'center';
        c.textBaseline = 'middle';
        if ('letterSpacing' in c) c.letterSpacing = '6px';
        [256, 768].forEach((x) => c.fillText(HERO_BOTTLE.scrittaCapsula, x, 50));
        capTex.needsUpdate = true;
      };
      drawCapsuleText();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawCapsuleText);
      const capBand = new THREE.Mesh(
        new THREE.CylinderGeometry(0.3035, 0.3035, 0.16, segments, 1, true),
        new THREE.MeshStandardMaterial({ map: capTex, transparent: true, roughness: 0.35, metalness: 0.5, envMap, envMapIntensity: 0.6, depthWrite: false })
      );
      capBand.position.y = 2.32;
      bottle.add(capBand);
    }

    // Etichette: porzioni di cilindro con la foto dell'etichetta come texture.
    // In CylinderGeometry theta = 0 punta verso +z (la camera), quindi la
    // fronte è centrata su 0 e il retro su PI.
    const loader = new THREE.TextureLoader();
    const maxAniso = Math.min(renderer.capabilities.getMaxAnisotropy(), lowPower ? 4 : 8);
    // Texture provvisoria (1 pixel scuro) con le stesse impostazioni di quella
    // vera: quando la foto arriva si scambia solo l'immagine, senza ricompilare
    // gli shader a metà animazione (causa di scatti).
    const placeholderTex = new THREE.DataTexture(new Uint8Array([12, 10, 10, 255]), 1, 1, THREE.RGBAFormat);
    placeholderTex.encoding = THREE.sRGBEncoding;
    placeholderTex.needsUpdate = true;

    const addLabel = (url, { height, arc, centerY, facing }) => {
      const thetaLength = arc / BODY_R;
      const geo = new THREE.CylinderGeometry(BODY_R + 0.006, BODY_R + 0.006, height, segments, 1, true, facing - thetaLength / 2, thetaLength);
      // La foto contiene già la luce: una quota "emissiva" mantiene i colori
      // reali dell'etichetta, mentre le luci aggiungono il volume sui lati.
      const mat = new THREE.MeshStandardMaterial({
        color: 0x3a3a3a,
        map: placeholderTex,
        emissive: 0xffffff,
        emissiveMap: placeholderTex,
        emissiveIntensity: 0.55,
        roughness: 0.8,
        metalness: 0,
        toneMapped: false
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.y = centerY;
      bottle.add(mesh);

      loader.load(url, (tex) => {
        tex.encoding = THREE.sRGBEncoding;
        tex.anisotropy = maxAniso;
        mat.map = tex;          // stesso tipo di texture: nessuna ricompilazione
        mat.emissiveMap = tex;
        if (!running) renderFrame(0); // aggiorna il frame statico (movimento ridotto)
      });
    };
    // Proporzioni ricavate dalla foto della bottiglia reale.
    // Aperto da file:// (doppio clic su index.html) il browser blocca le
    // texture WebGL caricate da file: in quel caso si usano le etichette
    // incorporate in HERO_BOTTLE.inline (data URI).
    const placeLabels = (urls) => {
      addLabel(urls.fronte, { height: 2.15, arc: 1.68, centerY: -0.75, facing: 0 });
      addLabel(urls.retro, { height: 1.84, arc: 1.48, centerY: -0.62, facing: Math.PI });
    };
    if (window.location.protocol === 'file:' && HERO_BOTTLE.inline) {
      const script = document.createElement('script');
      script.src = HERO_BOTTLE.inline;
      script.onload = () => placeLabels(window.SFM_HERO_LABELS || HERO_BOTTLE);
      script.onerror = () => placeLabels(HERO_BOTTLE);
      document.head.appendChild(script);
    } else {
      placeLabels(HERO_BOTTLE);
    }

    scene.add(bottle);

    // Riflesso morbido sotto la bottiglia
    const glowCanvas = document.createElement('canvas');
    glowCanvas.width = glowCanvas.height = 128;
    const gctx = glowCanvas.getContext('2d');
    const glowGrad = gctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    glowGrad.addColorStop(0, 'rgba(255,255,255,.35)');
    glowGrad.addColorStop(1, 'rgba(255,255,255,0)');
    gctx.fillStyle = glowGrad;
    gctx.fillRect(0, 0, 128, 128);
    const shadow = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 3.4),
      new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(glowCanvas), transparent: true, depthWrite: false, opacity: 0.5 })
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = -3.25;
    scene.add(shadow);

    // --- Particelle ---------------------------------------------------------
    const PARTICLES = lowPower ? 140 : 700;
    const AREA = { x: 14, y: 9, zMin: -10, zMax: 6 };
    const positions = new Float32Array(PARTICLES * 3);
    const speeds = new Float32Array(PARTICLES);
    const phases = new Float32Array(PARTICLES);

    for (let i = 0; i < PARTICLES; i++) {
      positions[i * 3] = (Math.random() * 2 - 1) * AREA.x;
      positions[i * 3 + 1] = (Math.random() * 2 - 1) * AREA.y;
      positions[i * 3 + 2] = AREA.zMin + Math.random() * (AREA.zMax - AREA.zMin);
      speeds[i] = 0.08 + Math.random() * 0.25;
      phases[i] = Math.random() * Math.PI * 2;
    }

    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    // Texture circolare morbida generata su canvas
    const dot = document.createElement('canvas');
    dot.width = dot.height = 64;
    const ctx = dot.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.35, 'rgba(255,255,255,.45)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);

    const particleMat = new THREE.PointsMaterial({
      size: isMobile ? 0.07 : 0.06,
      map: new THREE.CanvasTexture(dot),
      transparent: true,
      opacity: 0.6,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      sizeAttenuation: true
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // --- Parallasse: mouse e giroscopio -------------------------------------
    const pointer = { x: 0, y: 0 };   // valore obiettivo (-1..1)
    const smooth = { x: 0, y: 0 };    // valore interpolato

    window.addEventListener('pointermove', (e) => {
      if (e.pointerType !== 'mouse') return;
      pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
      pointer.y = (e.clientY / window.innerHeight) * 2 - 1;
    }, { passive: true });

    let betaBase = null;
    const onOrientation = (e) => {
      if (e.gamma == null || e.beta == null) return;
      if (betaBase === null) betaBase = e.beta;
      pointer.x = clamp(e.gamma / 25, -1, 1);
      pointer.y = clamp((e.beta - betaBase) / 25, -1, 1);
    };

    if ('DeviceOrientationEvent' in window && window.matchMedia('(pointer: coarse)').matches) {
      if (typeof DeviceOrientationEvent.requestPermission === 'function') {
        // iOS 13+: il permesso va chiesto in risposta a un gesto dell'utente
        const ask = () => {
          DeviceOrientationEvent.requestPermission()
            .then((state) => { if (state === 'granted') window.addEventListener('deviceorientation', onOrientation); })
            .catch(() => {});
        };
        window.addEventListener('touchend', ask, { once: true });
      } else {
        window.addEventListener('deviceorientation', onOrientation);
      }
    }

    // --- Regia allo scroll: pose chiave della bottiglia --------------------
    // Ogni posa: posizione (x, y), scala (s) e rotazioni. Le pose vengono
    // ricalcolate a ogni resize perché dipendono dal formato dello schermo.
    //   0.00–0.12 fuori scena (c'è il logo) · 0.30 entrata dal basso
    //   0.50–0.62 primo piano fronte · 0.70–0.82 retro · 0.96 "versata"
    let keyframes = [];

    const pose = (x, y, s, rotY, rotZ = 0, rotX = 0) => ({ x, y, s, rotY, rotZ, rotX });

    let lastW = 0;
    let lastH = 0;
    const resize = (force) => {
      const w = hero.clientWidth;
      const h = hero.clientHeight;
      // Su telefono la barra degli indirizzi genera continui "resize" senza che
      // l'hero (alto 100svh) cambi davvero: in quel caso non si ricalcola nulla.
      if (force !== true && w === lastW && h === lastH) return;
      lastW = w;
      lastH = h;
      renderer.setPixelRatio(dpr);
      renderer.setSize(w, h, false);
      camera.aspect = w / h;

      const halfH = (z) => z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
      let open, front, back, pour, offY;

      if (sideQuery.matches) {
        // Desktop: bottiglia a destra, testi a sinistra
        cameraBase.z = 12.5;
        const halfW = halfH(cameraBase.z) * camera.aspect;
        open = pose(halfW * 0.44, 0.15, 1, 0, -0.06);
        front = pose(halfW * 0.36, 0.95, 1.45, 0, 0, 0.04);
        back = pose(halfW * 0.36, 0.95, 1.45, Math.PI, 0.03, 0.04);
        pour = pose(halfW * 0.4, 0.5, 1.05, Math.PI * 2, 0.42);
        offY = -(halfH(cameraBase.z) + 3.6);
      } else {
        // Mobile/verticale: la bottiglia occupa lo spazio libero tra l'header
        // e il capitolo di testo corrispondente (misurato davvero a schermo),
        // così bottiglia e testi non si sovrappongono su nessun telefono.
        cameraBase.z = 15;
        const hh = halfH(cameraBase.z);
        const pxToWorld = (2 * hh) / h;
        const heroTop = hero.getBoundingClientRect().top;
        const headerH = ($('.site-header') || {}).offsetHeight || 72;
        const chapterTop = (sel) => {
          const el = $(sel, hero);
          return el ? el.getBoundingClientRect().top - heroTop : h * 0.55;
        };
        const fit = (topPx, zoom = 1) => {
          const regionTop = headerH + 8;
          const regionPx = Math.max(120, topPx - 12 - regionTop);
          const s = Math.min(0.62 * zoom, ((regionPx * pxToWorld) / 6.2) * zoom);
          const centerPx = regionTop + regionPx / 2;
          return { s, y: hh - centerPx * pxToWorld };
        };
        const chapters = $$('.hero-chapter', hero);
        const fOpen = fit(chapterTop('.hero-chapter--intro'));
        const fFront = fit(chapters[1] ? chapters[1].getBoundingClientRect().top - heroTop : h * 0.6, 1.08);
        const fBack = fit(chapters[2] ? chapters[2].getBoundingClientRect().top - heroTop : h * 0.6, 1.08);
        const fPour = fit(chapters[3] ? chapters[3].getBoundingClientRect().top - heroTop : h * 0.6);
        open = pose(0, fOpen.y, fOpen.s, 0, -0.06);
        front = pose(0, fFront.y, fFront.s, 0, 0, 0.04);
        back = pose(0, fBack.y, fBack.s, Math.PI, 0.03, 0.04);
        pour = pose(0, fPour.y, fPour.s * 0.95, Math.PI * 2, 0.3);
        offY = -(hh + 3.6 * open.s);
      }
      // Fuori scena: sotto l'inquadratura, ruotata, pronta a entrare
      const hidden = pose(open.x, offY, open.s, -Math.PI * 0.9, -0.25);

      keyframes = [
        [0, hidden], [0.12, hidden], [0.3, open], [0.42, open],
        [0.5, front], [0.62, front], [0.7, back], [0.82, back],
        [0.96, pour], [1, pour]
      ];
      camera.updateProjectionMatrix();
      if (!running) renderFrame(0);
    };

    /** Interpola la posa corrispondente alla posizione di scroll q (0–1). */
    const sample = (q) => {
      for (let i = 0; i < keyframes.length - 1; i++) {
        const [q0, a] = keyframes[i];
        const [q1, b] = keyframes[i + 1];
        if (q <= q1 || i === keyframes.length - 2) {
          const k = smoothstep(q0, q1, q);
          return {
            x: lerp(a.x, b.x, k), y: lerp(a.y, b.y, k), s: lerp(a.s, b.s, k),
            rotY: lerp(a.rotY, b.rotY, k), rotZ: lerp(a.rotZ, b.rotZ, k), rotX: lerp(a.rotX, b.rotX, k)
          };
        }
      }
      return keyframes[0][1];
    };

    // --- Loop di animazione -------------------------------------------------
    const clock = new THREE.Clock();
    let running = false;
    let rafId = null;
    let heroVisible = true;
    let elapsed = 0;

    function renderFrame(dt) {
      elapsed += dt;
      const t = elapsed;

      // Parallasse ammorbidita
      smooth.x = lerp(smooth.x, pointer.x, 0.045);
      smooth.y = lerp(smooth.y, pointer.y, 0.045);

      camera.position.x = cameraBase.x + smooth.x * 0.8;
      camera.position.y = cameraBase.y - smooth.y * 0.5;
      camera.position.z = cameraBase.z;
      camera.lookAt(0, 0, 0);

      // Posa guidata dallo scroll + movimento "a riposo" che si spegne scorrendo
      const q = heroScroll.enabled ? heroScroll.progress : 0;
      const p = sample(q);
      // oscillazione "a riposo" solo mentre la bottiglia è nella posa d'apertura
      const idle = smoothstep(0.24, 0.3, q) * (1 - smoothstep(0.42, 0.5, q));

      bottle.position.set(p.x, p.y + Math.sin(t * 0.6) * 0.08, 0);
      bottle.scale.setScalar(p.s);
      bottle.rotation.y = p.rotY + Math.sin(t * 0.4) * 0.6 * idle + smooth.x * 0.3;
      bottle.rotation.x = p.rotX + smooth.y * 0.08;
      bottle.rotation.z = p.rotZ + Math.sin(t * 0.5) * 0.02;

      // Riflesso a terra: segue la bottiglia e sparisce quando si inclina
      shadow.position.set(p.x, p.y - 3.25 * p.s, 0);
      shadow.scale.setScalar(p.s);
      shadow.material.opacity = 0.5 * smoothstep(0.22, 0.3, q) * (1 - smoothstep(0.84, 0.95, q));

      // Particelle: salgono lentamente con lieve oscillazione
      if (dt > 0) {
        const pos = particleGeo.attributes.position.array;
        for (let i = 0; i < PARTICLES; i++) {
          const iy = i * 3 + 1;
          pos[iy] += speeds[i] * dt;
          pos[i * 3] += Math.sin(t * 0.4 + phases[i]) * 0.0025;
          if (pos[iy] > AREA.y) pos[iy] = -AREA.y;
        }
        particleGeo.attributes.position.needsUpdate = true;
      }
      particles.rotation.y = smooth.x * 0.08;
      particles.rotation.x = smooth.y * 0.05;

      renderer.render(scene, camera);
    }

    // Qualità adattiva: ogni 90 fotogrammi si misura la media; sotto i ~45 fps
    // si riduce la densità dei pixel (fino a 1) e, se non basta, le particelle.
    let frames = 0;
    let frameTime = 0;
    let lastStamp = 0;
    const adapt = (now) => {
      if (lastStamp) {
        const ft = now - lastStamp;
        if (ft < 250) { frameTime += ft; frames++; } // ignora le pause (scheda in background)
      }
      lastStamp = now;
      if (frames < 90) return;
      const avg = frameTime / frames;
      frames = 0;
      frameTime = 0;
      if (avg <= 22) return;
      if (dpr > 1) {
        dpr = Math.max(1, Math.round((dpr - 0.25) * 100) / 100);
        renderer.setPixelRatio(dpr);
        renderer.setSize(lastW, lastH, false);
      } else if (particles.visible) {
        particles.visible = false;
      }
    };

    function loop(now) {
      if (!running) return;
      rafId = requestAnimationFrame(loop);
      adapt(now);
      renderFrame(Math.min(clock.getDelta(), 0.05));
    }

    function start() {
      if (running || prefersReducedMotion() || !heroVisible || document.hidden) return;
      running = true;
      lastStamp = 0;
      clock.getDelta(); // azzera il delta accumulato durante la pausa
      rafId = requestAnimationFrame(loop);
    }

    function stop() {
      running = false;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    }

    // Ferma il loop quando l'hero non è visibile o la scheda è in background
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([entry]) => {
        heroVisible = entry.isIntersecting;
        heroVisible ? start() : stop();
      }).observe(section);
    }
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));

    // Preferenza di movimento ridotto: un solo frame statico
    motionQuery.addEventListener('change', () => {
      if (prefersReducedMotion()) {
        stop();
        renderFrame(0);
      } else {
        start();
      }
    });

    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(resize, 120);
    });

    // Contesto WebGL perso: si passa allo sfondo di fallback
    canvas.addEventListener('webglcontextlost', (e) => {
      e.preventDefault();
      stop();
      hero.classList.add('no-webgl');
    });

    // Fase iniziale dell'oscillazione: etichetta leggermente di tre quarti
    elapsed = -0.9;
    resize(true);
    // Compila subito tutti gli shader della scena, prima che parta l'animazione
    try { renderer.compile(scene, camera); } catch (err) { /* facoltativo */ }
    // I capitoli cambiano altezza quando arrivano i font: si ricalcola la posa
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => resize(true));
    renderFrame(0);
    start();
  }


  /* ========================================================================
     10. AVVIO
     ======================================================================== */
  function init() {
    SFMConsent.init();
    initConsentMap();
    const year = $('#year');
    if (year) year.textContent = String(new Date().getFullYear());

    initHeader();
    initMobileNav();
    initActiveLinks();
    initWhatsAppLinks();
    initProducts();
    initEvents();
    initReviews();
    initStatement();
    initAboutPhoto();
    initReveal();
    initForm();
    initCursor();
    initHeroScroll();
    initHero3D();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
