#!/usr/bin/env python3
"""
Genera la <head> SEO di index.html (meta, Open Graph, geo, dati strutturati
JSON-LD) leggendo prodotti ed eventi da script.js, e la versione inglese
en/index.html (testi tradotti da traduzioni_en.py, percorsi corretti, SEO in inglese).

Uso (dalla cartella del sito):  python3 .claude/genera-seo.py
Va rilanciato quando cambiano prodotti, eventi, testi della pagina o i dati aziendali.
⚠ Modificare sempre index.html (italiano): en/index.html viene rigenerata da qui.
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import traduzioni_en as T_EN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.sfmdistribuzioni.com'
TODAY = '2026-10-28'

# ---------------------------------------------------------------------------
# DATI AZIENDALI — l'unico segnaposto rimasto è la P.IVA
# ---------------------------------------------------------------------------
AZIENDA = {
    'nome': 'S.F.M. Distribuzione',
    'alias': ['SFM Distribuzioni', 'SFM Vini d\'eccellenza', 'SFM'],
    'slogan': 'Un viaggio nel mondo del vino',
    'telefono': '+39 349 063 0846',
    'whatsapp': '+39 338 469 3769',
    'email': 'info@sfmdistribuzioni.com',
    'piva': 'IT00000000000',                  # DA INSERIRE
    'indirizzo': {                            # sede: città di Ferrara (senza via)
        'via': '',
        'cap': '',
        'citta': 'Ferrara',
        'provincia': 'FE',
    },
    # Coordinate del centro di Ferrara (località della sede)
    'lat': 44.8381,
    'lng': 11.6198,
    'instagram': 'https://www.instagram.com/sfm_distribuzioni/',
}

CATEGORIE = {
    'it': {'rossi': 'Vino rosso', 'bianchi': 'Vino bianco', 'bollicine': 'Spumante',
           'rosati': 'Vino rosato', 'distillati': 'Amaro / distillato', 'bevande': 'Bevanda'},
    'en': {'rossi': 'Red wine', 'bianchi': 'White wine', 'bollicine': 'Sparkling wine',
           'rosati': 'Rosé wine', 'distillati': 'Amaro / spirit', 'bevande': 'Soft drink'},
}

# Testi per lingua (meta, dati strutturati)
TXT = {
    'it': {
        'url': f'{SITE}/', 'lang': 'it-IT', 'og_locale': 'it_IT', 'og_alt_locale': 'en_GB',
        'title': 'Distributore vini HORECA | S.F.M. Distribuzione – Vini d\'eccellenza',
        'desc': ('Distributore di vini d\'eccellenza solo per HORECA: cantine artigianali assenti dalla GDO, '
                 'zero minimi d\'ordine, consegne in 48/72h e consulenza carta vini.'),
        'og_title': 'S.F.M. Distribuzione – Vini e bevande d\'eccellenza per l\'HORECA',
        'og_desc': ('Cantine artigianali assenti dalla grande distribuzione, nessun minimo d\'ordine, consegne in 48/72 ore '
                    'e degustazioni guidate per ristoranti, bar, enoteche e hotel.'),
        'tw_title': 'S.F.M. Distribuzione – Vini d\'eccellenza per l\'HORECA',
        'img_alt': 'S.F.M. Vini d\'eccellenza – Un viaggio nel mondo del vino',
        'keywords': ('distributore vini HORECA, distribuzione vini ristoranti, fornitore vini bar, vini per enoteche, '
                     'vini artigianali, vini calabresi IGP, consulenza carta dei vini, degustazioni guidate, '
                     'nessun minimo d\'ordine, Ferrara'),
        'org_desc': ('Distributore di vini e bevande d\'eccellenza esclusivamente per il settore HORECA: '
                     'cantine artigianali assenti dalla grande distribuzione, nessun minimo d\'ordine, '
                     'consegne in 48/72 ore, consulenza sulla carta dei vini e degustazioni guidate.'),
        'slogan': 'Un viaggio nel mondo del vino',
        'catalog': 'Catalogo vini e bevande HORECA', 'zona': 'Zona di produzione', 'italia': 'Italia',
        'area': ['Ferrara', 'Provincia di Ferrara', 'Emilia-Romagna', 'Italia'],
        'knows': ['Distribuzione vini HORECA', 'Vini artigianali', 'Vini calabresi IGP',
                  'Carta dei vini per ristoranti', 'Formazione personale di sala',
                  'Degustazioni guidate', 'Amari artigianali'],
        'servizi': [
            ('Consegne rapide senza minimi d\'ordine', 'Consegne frazionate in 48/72 ore, senza minimi d\'ordine, per locali HORECA.'),
            ('Catalogo esclusivo HORECA', 'Etichette artigianali e micro-produzioni assenti dalla grande distribuzione.'),
            ('Consulenza carta dei vini', 'Costruzione della carta dei vini e formazione del personale di sala.'),
            ('Format Degustazione Guidata', 'Serate di degustazione chiavi in mano nel locale del cliente.'),
        ],
    },
    'en': {
        'url': f'{SITE}/en/', 'lang': 'en-GB', 'og_locale': 'en_GB', 'og_alt_locale': 'it_IT',
        'title': 'Italian Fine Wine Distributor for HoReCa | S.F.M. Distribuzione',
        'desc': ('Fine Italian wines for HoReCa: artisanal wineries absent from mass retail, no minimum order, '
                 '48/72h delivery and wine list consulting. Ferrara, Italy.'),
        'og_title': 'S.F.M. Distribuzione – Fine Italian wines for the HoReCa trade',
        'og_desc': ('Artisanal wineries absent from mass retail, no minimum order, 48/72-hour delivery and guided '
                    'tastings for restaurants, bars, wine bars and hotels.'),
        'tw_title': 'S.F.M. Distribuzione – Fine Italian wines for HoReCa',
        'img_alt': 'S.F.M. Fine wines – A journey into the world of wine',
        'keywords': ('Italian wine distributor, HoReCa wine supplier, wine wholesaler Italy, wines for restaurants, '
                     'artisanal Italian wines, Calabrian IGP wines, wine list consulting, guided wine tastings, '
                     'no minimum order, Ferrara, Emilia-Romagna'),
        'org_desc': ('Distributor of fine wines and beverages exclusively for the HoReCa trade: artisanal wineries '
                     'absent from mass retail, no minimum order, 48/72-hour delivery, wine list consulting and guided tastings.'),
        'slogan': 'A journey into the world of wine',
        'catalog': 'HoReCa wine and beverage catalogue', 'zona': 'Production area', 'italia': 'Italy',
        'area': ['Ferrara', 'Province of Ferrara', 'Emilia-Romagna', 'Italy'],
        'knows': ['HoReCa wine distribution', 'Artisanal wines', 'Calabrian IGP wines',
                  'Restaurant wine lists', 'Front-of-house staff training',
                  'Guided wine tastings', 'Artisanal amari'],
        'servizi': [
            ('Fast delivery, no minimum order', 'Split deliveries within 48/72 hours with no minimum order for HoReCa venues.'),
            ('Exclusive HoReCa catalogue', 'Artisanal labels and small productions absent from mass retail.'),
            ('Wine list consulting', 'Wine list design and front-of-house staff training.'),
            ('Guided Tasting Format', 'Turnkey tasting evenings at the client\'s venue.'),
        ],
    },
}

FAQ = [
    ('A chi vende S.F.M. Distribuzione?',
     'Esclusivamente al settore HORECA: ristoranti, bar, enoteche, hotel, pizzerie e locali. Non vendiamo ai privati né alla grande distribuzione.'),
    ('C\'è un minimo d\'ordine?',
     'No. Non imponiamo minimi d\'ordine: acquisti solo ciò che ti serve, quando ti serve, senza immobilizzare capitale in magazzino.'),
    ('In quanto tempo consegnate?',
     'Garantiamo consegne rapide e frazionate in 48/72 ore dall\'ordine.'),
    ('Che tipo di vino vendete?',
     "Esclusività, fuori dai soliti circuiti. Distribuiamo etichette che non troverete mai nella grande distribuzione. La nostra ricerca si concentra esclusivamente su cantine artigianali, micro-produzioni territoriali e chicche enologiche di nicchia. Il nostro obiettivo è fornire ai professionisti dell'Ho.Re.Ca. vini unici e ricercati, capaci di distinguere e valorizzare la loro carta."),
    ('Offrite consulenza per la carta dei vini?',
     'Sì. Ti affianchiamo nella costruzione di una carta dei vini bilanciata con il tuo menù e il tuo target, e formiamo il personale di sala a raccontare e proporre le etichette.'),
    ('Organizzate degustazioni nel locale?',
     'Sì, offriamo un format "chiavi in mano". Progettiamo e allestiamo serate di degustazione guidata comprensive di postazioni dedicate, narrazione tecnica dei prodotti e intrattenimento artistico. Il tutto in totale autonomia e a costo zero, per garantirvi un evento di successo senza gravare minimamente sul vostro staff.'),
    ('Come richiedo il listino HORECA?',
     'Compila il modulo "Richiedi il listino" sul sito oppure scrivici su WhatsApp: ti inviamo il listino riservato e una proposta per il tuo locale.'),
]


def js_string(s):
    """Converte una stringa JS a singoli apici in testo semplice."""
    return s.replace("\\'", "'").replace('\\\\', '\\')


def parse_array(src, name):
    """Estrae gli oggetti { chiave: 'valore', ... } dell'array JS `name`."""
    start = src.index(f'const {name} = [')
    end = src.index('\n  ];', start)
    body = src[start:end]
    items = []
    for block in re.findall(r'\{(.*?)\n    \}', body, re.S):
        item = {}
        for key, val in re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", block):
            item.setdefault(key, js_string(val))
        lists = re.findall(r"(\w+):\s*\[(.*?)\]", block, re.S)
        for key, inner in lists:
            item[key] = [js_string(v) for v in re.findall(r"'((?:[^'\\]|\\.)*)'", inner)]
        items.append(item)
    return items


def absolute(path):
    return f'{SITE}/{path}'


def build_graph(prodotti, eventi, lang='it'):
    org_id = f'{SITE}/#azienda'
    a = AZIENDA
    ind = a['indirizzo']
    t = TXT[lang]
    cats = CATEGORIE[lang]
    en = lang == 'en'
    loc = lambda obj, key: (obj.get(key + 'En') if en else None) or obj.get(key, '')

    # Catalogo raggruppato per categoria
    gruppi = {}
    for p in prodotti:
        gruppi.setdefault(p['categoria'], []).append(p)
    catalogo = {
        '@type': 'OfferCatalog',
        'name': t['catalog'],
        'itemListElement': [{
            '@type': 'OfferCatalog',
            'name': cats.get(cat, cat).capitalize(),
            'itemListElement': [{
                '@type': 'Offer',
                'eligibleCustomerType': 'http://purl.org/goodrelations/v1#Business',
                'businessFunction': 'http://purl.org/goodrelations/v1#Sell',
                'itemOffered': {
                    '@type': 'Product',
                    'name': f"{p['nome']} – {loc(p, 'cantina')}",
                    'brand': {'@type': 'Brand', 'name': loc(p, 'cantina')},
                    'category': cats.get(cat, cat),
                    'description': loc(p, 'descrizione'),
                    'image': [absolute(i) for i in p.get('immagini', [])],
                    'countryOfOrigin': {'@type': 'Country', 'name': t['italia']},
                    'additionalProperty': [{
                        '@type': 'PropertyValue', 'name': t['zona'], 'value': p.get('regione', ''),
                    }],
                },
            } for p in lista],
        } for cat, lista in gruppi.items()],
    }

    servizi = t['servizi']

    graph = [
        {
            '@type': ['LocalBusiness', 'Organization'],
            '@id': org_id,
            'name': a['nome'],
            'alternateName': a['alias'],
            'slogan': t['slogan'],
            'description': t['org_desc'],
            'url': f'{SITE}/',
            'logo': {'@type': 'ImageObject', '@id': f'{SITE}/#logo', 'url': absolute('assets/logo-sfm.png'),
                     'width': 404, 'height': 480, 'caption': a['nome']},
            'image': [absolute('assets/og-image.jpg'), absolute('assets/chi-siamo.jpg')],
            'telephone': a['telefono'],
            'email': a['email'],
            'vatID': a['piva'],
            'address': {k: v for k, v in {
                '@type': 'PostalAddress', 'streetAddress': ind['via'], 'postalCode': ind['cap'],
                'addressLocality': ind['citta'], 'addressRegion': ind['provincia'], 'addressCountry': 'IT',
            }.items() if v},
            'geo': {'@type': 'GeoCoordinates', 'latitude': a['lat'], 'longitude': a['lng']},
            'hasMap': f"https://www.google.com/maps/search/?api=1&query={a['lat']},{a['lng']}",
            'areaServed': [
                {'@type': 'City', 'name': t['area'][0]},
                {'@type': 'AdministrativeArea', 'name': t['area'][1]},
                {'@type': 'AdministrativeArea', 'name': t['area'][2]},
                {'@type': 'Country', 'name': t['area'][3]},
            ],
            'knowsAbout': t['knows'],
            'openingHoursSpecification': [{
                '@type': 'OpeningHoursSpecification',
                'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens': '08:30', 'closes': '18:30',
            }],
            'contactPoint': [{
                '@type': 'ContactPoint', 'contactType': 'sales', 'telephone': a['telefono'], 'email': a['email'],
                'areaServed': 'IT', 'availableLanguage': ['Italian', 'English'],
            }],
            'makesOffer': [{
                '@type': 'Offer',
                'eligibleCustomerType': 'http://purl.org/goodrelations/v1#Business',
                'itemOffered': {'@type': 'Service', 'name': n, 'description': d, 'provider': {'@id': org_id}},
            } for n, d in servizi],
            'hasOfferCatalog': catalogo,
            'sameAs': [a['instagram'], f"https://wa.me/{a['whatsapp'].replace('+', '').replace(' ', '')}"],
        },
        {
            '@type': 'WebSite',
            '@id': f'{SITE}/#sito',
            'url': f'{SITE}/',
            'name': a['nome'],
            'alternateName': a['alias'],
            'inLanguage': ['it-IT', 'en-GB'],
            'publisher': {'@id': org_id},
        },
        {
            '@type': 'WebPage',
            '@id': f"{t['url']}#pagina",
            'url': t['url'],
            'name': t['title'],
            'isPartOf': {'@id': f'{SITE}/#sito'},
            'about': {'@id': org_id},
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': absolute('assets/og-image.jpg'), 'width': 1200, 'height': 630},
            'inLanguage': t['lang'],
            'datePublished': TODAY,
            'dateModified': TODAY,
        },
        {
            '@type': 'FAQPage',
            '@id': f"{t['url']}#faq",
            'isPartOf': {'@id': f"{t['url']}#pagina"},
            'inLanguage': t['lang'],
            'mainEntity': [{
                '@type': 'Question', 'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': r},
            } for q, r in (faq_en() if en else FAQ)],
        },
    ]

    # Eventi (raggruppati per data + luogo: più locandine = più immagini)
    visti = {}
    for e in eventi:
        key = (e.get('data'), e.get('luogo'))
        if key in visti:
            visti[key]['image'] += [absolute(i) for i in e.get('locandine', [])]
            continue
        luogo_nome, _, luogo_ind = (e.get('luogo') or '').partition(' · ')
        node = {
            '@type': 'Event',
            'name': f"{e['titolo']} – {luogo_nome}",
            'description': loc(e, 'descrizione'),
            'startDate': f"{e['data']}T{e.get('ora', '19:00')}:00+02:00",
            'eventStatus': 'https://schema.org/EventScheduled',
            'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
            'location': {
                '@type': 'Place', 'name': luogo_nome,
                'address': {'@type': 'PostalAddress', 'streetAddress': luogo_ind.split(',')[0].strip(),
                            'addressLocality': 'Ferrara', 'addressRegion': 'FE', 'addressCountry': 'IT'},
            },
            'image': [absolute(i) for i in e.get('locandine', [])],
            'organizer': {'@id': org_id},
        }
        visti[key] = node
        graph.append(node)

    return {'@context': 'https://schema.org', '@graph': graph}


def faq_en():
    return [(q, f'{lead} {r}'.strip()) for q, lead, r in T_EN.FAQ_EN]


def build_head(graph, lang='it'):
    a = AZIENDA
    t = TXT[lang]
    jsonld = json.dumps(graph, ensure_ascii=False, indent=2)
    jsonld = '\n'.join('  ' + line for line in jsonld.split('\n'))
    return f"""  <!-- ==========================================================================
       META / SEO  (generata da .claude/genera-seo.py — modificare lì e rilanciare)
       ========================================================================== -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{t['title']}</title>
  <meta name="description" content="{t['desc']}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="{a['nome']}">
  <meta name="keywords" content="{t['keywords']}">
  <meta name="theme-color" content="#000000">
  <meta name="color-scheme" content="dark">
  <meta name="format-detection" content="telephone=yes">
  <link rel="canonical" href="{t['url']}">
  <link rel="alternate" hreflang="it" href="{SITE}/">
  <link rel="alternate" hreflang="en" href="{SITE}/en/">
  <link rel="alternate" hreflang="x-default" href="{SITE}/">

  <!-- Geo (SEO locale): Ferrara -->
  <meta name="geo.region" content="IT-{a['indirizzo']['provincia']}">
  <meta name="geo.placename" content="{a['indirizzo']['citta']}">
  <meta name="geo.position" content="{a['lat']};{a['lng']}">
  <meta name="ICBM" content="{a['lat']}, {a['lng']}">

  <!-- Open Graph / social -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{t['og_locale']}">
  <meta property="og:locale:alternate" content="{t['og_alt_locale']}">
  <meta property="og:site_name" content="{a['nome']}">
  <meta property="og:title" content="{t['og_title']}">
  <meta property="og:description" content="{t['og_desc']}">
  <meta property="og:url" content="{t['url']}">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:secure_url" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{t['img_alt']}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{t['tw_title']}">
  <meta name="twitter:description" content="{t['og_desc']}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
  <meta name="twitter:image:alt" content="{t['img_alt']}">

  <!-- Icone e manifest -->
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" href="assets/favicon.png" type="image/png" sizes="512x512">
  <link rel="icon" href="assets/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="site.webmanifest">
  <meta name="apple-mobile-web-app-title" content="SFM">
  <meta name="application-name" content="S.F.M. Distribuzione">

  <!-- Segnala subito che JS è attivo (evita il "flash" delle animazioni di comparsa) -->
  <script>document.documentElement.className = document.documentElement.className.replace('no-js', 'js');</script>

  <!-- Prestazioni: connessione anticipata e logo d'apertura (elemento più grande) -->
  <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
  <link rel="preload" as="image" href="assets/logo-monogramma.png" fetchpriority="high">

  <!-- Font: Helvetica di sistema (nessun font esterno da scaricare) -->
  <link rel="stylesheet" href="style.css">

  <!-- Three.js (versione fissata r128) + script del sito, entrambi in defer -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
          integrity="sha512-dLxUelApnYxpLt6K2iomGngnHO83iUvZytA3YjDUCjT0HDOHKXnVYdf3hU4JjM8uEhxf9nD1/ey98U3t2vZ0qQ=="
          crossorigin="anonymous" referrerpolicy="no-referrer" defer></script>
  <script src="script.js" defer></script>

  <!-- Dati strutturati (azienda, sito, pagina, catalogo, servizi, FAQ, eventi) -->
  <script type="application/ld+json">
{jsonld}
  </script>
"""


# ---------------------------------------------------------------------------
# Versione inglese: traduzione del corpo della pagina e correzione dei percorsi
# ---------------------------------------------------------------------------
def _forms(text):
    """Le possibili forme di un testo nel sorgente HTML (con e senza entità)."""
    esc = htmllib.escape(text, quote=False)
    return [text] if esc == text else [text, esc]


def translate_body(body):
    missing = []
    # Domande frequenti: blocco rigenerato dalle traduzioni
    items = ''.join(
        '          <details class="service faq__item reveal">\n'
        '            <summary class="service__head faq__q">\n'
        f'              <span class="service__titles"><span class="service__title">{htmllib.escape(q, quote=False)}</span></span>\n'
        '              <span class="service__toggle" aria-hidden="true"></span>\n'
        '            </summary>\n'
        '            <div class="service__body"><p>'
        + (f'<strong class="faq__lead">{htmllib.escape(lead, quote=False)}</strong> ' if lead else '')
        + f'{htmllib.escape(r, quote=False)}</p></div>\n'
        '          </details>\n'
        for q, lead, r in T_EN.FAQ_EN)
    m = re.search(r'(<section class="section faq".*?<div class="services__list">\n)(.*?)(        </div>\n      </div>\n    </section>)', body, re.S)
    body = body[:m.start(2)] + items + body[m.end(2):]

    # Testi visibili: si sostituisce solo il contenuto intero di un nodo di testo
    for it, en in sorted(T_EN.TESTI, key=lambda x: -len(x[0])):
        done = False
        for form in _forms(it):
            pat = re.compile(r'(>\s*)' + re.escape(form).replace(r'\ ', r'\s+') + r'(\s*<)')
            body, n = pat.subn(lambda mm: mm.group(1) + htmllib.escape(en, quote=False) + mm.group(2), body)
            done = done or n > 0
        if not done:
            missing.append(it)
    # Attributi
    for it, en in T_EN.ATTRIBUTI:
        done = False
        for form in {it, htmllib.escape(it, quote=True)}:
            for attr in ('alt', 'aria-label', 'title', 'data-wa-text'):
                old = f'{attr}="{form}"'
                if old in body:
                    body = body.replace(old, f'{attr}="{htmllib.escape(en, quote=True)}"')
                    done = True
        if not done:
            missing.append('[attr] ' + it)
    # Valori del form
    for it, en in T_EN.VALORI:
        body = body.replace(f'value="{it}"', f'value="{en}"')
    if missing:
        print('⚠ Testi non trovati (aggiornare traduzioni_en.py):')
        for x in missing:
            print('   -', x)
    return body


def fix_paths(html):
    """Da /en/ i percorsi relativi salgono di un livello (../)."""
    def repl(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|data:|#|/|\.\./)', val) or val == '':
            return m.group(0)
        return f'{attr}="../{val}"'
    return re.sub(r'\b(href|src)="([^"]*)"', repl, html)


def build_en(html_it, graph_en):
    head_start = html_it.index('  <!-- ==========================================================================\n       META / SEO')
    head_end = html_it.index('</head>')
    body = translate_body(html_it[head_end:])
    html = html_it[:head_start] + build_head(graph_en, 'en') + body
    html = html.replace('<html lang="it" class="no-js">', '<html lang="en" class="no-js">', 1)
    html = fix_paths(html)
    # Selettore di lingua: IT torna alla radice, EN è la pagina corrente
    html = re.sub(
        r'<nav class="lang-switch".*?</nav>',
        '<nav class="lang-switch" aria-label="Language / Lingua">\n'
        '        <a class="lang-switch__link" href="../" hreflang="it" lang="it" data-lang-link>IT</a>\n'
        '        <span class="lang-switch__sep" aria-hidden="true">/</span>\n'
        '        <a class="lang-switch__link is-current" href="./" hreflang="en" lang="en" aria-current="page" data-lang-link>EN</a>\n'
        '      </nav>', html, count=1, flags=re.S)
    html = html.replace('<!-- Pagina generata', '<!-- Pagina generata', 1)
    banner = ('<!-- ⚠ FILE GENERATO da .claude/genera-seo.py partendo da index.html:\n'
              '     non modificarlo a mano (le modifiche andrebbero perse). -->\n')
    return html.replace('<body>', '<body>\n  ' + banner, 1)


def main():
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    prodotti = parse_array(js, 'PRODOTTI')
    eventi = parse_array(js, 'EVENTI')

    # Italiano
    html_path = ROOT / 'index.html'
    html = html_path.read_text(encoding='utf-8')
    start = html.index('  <!-- ==========================================================================\n       META / SEO')
    end = html.index('</head>')
    html = html[:start] + build_head(build_graph(prodotti, eventi, 'it'), 'it') + html[end:]
    html_path.write_text(html, encoding='utf-8')

    # Inglese
    (ROOT / 'en').mkdir(exist_ok=True)
    (ROOT / 'en' / 'index.html').write_text(build_en(html, build_graph(prodotti, eventi, 'en')), encoding='utf-8')
    print(f'OK: index.html + en/index.html · {len(prodotti)} prodotti, {len(eventi)} locandine eventi, {len(FAQ)} FAQ')


if __name__ == '__main__':
    main()
