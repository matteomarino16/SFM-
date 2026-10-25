#!/usr/bin/env python3
"""
Genera la <head> SEO di index.html (meta, Open Graph, geo, dati strutturati
JSON-LD) leggendo prodotti ed eventi da script.js.

Uso (dalla cartella del sito):  python3 .claude/genera-seo.py
Va rilanciato quando cambiano prodotti, eventi o i dati aziendali qui sotto.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.sfmdistribuzioni.com'
TODAY = '2026-10-25'

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
    'rossi': 'Vino rosso', 'bianchi': 'Vino bianco', 'bollicine': 'Spumante',
    'rosati': 'Vino rosato', 'distillati': 'Amaro / distillato', 'bevande': 'Bevanda',
}

FAQ = [
    ('A chi vende S.F.M. Distribuzione?',
     'Esclusivamente al settore HORECA: ristoranti, bar, enoteche, hotel, pizzerie e locali. Non vendiamo ai privati né alla grande distribuzione.'),
    ('C\'è un minimo d\'ordine?',
     'No. Non imponiamo minimi d\'ordine: acquisti solo ciò che ti serve, quando ti serve, senza immobilizzare capitale in magazzino.'),
    ('In quanto tempo consegnate?',
     'Garantiamo consegne rapide e frazionate in 48/72 ore dall\'ordine.'),
    ('Che tipo di vini distribuite?',
     'Selezioniamo etichette di cantine artigianali e micro-produzioni territoriali assenti dalla grande distribuzione, come Tenute De Giglio, Cantine De Luca e Vecchi Cantinieri (Calabria IGP), oltre ad amari artigianali.'),
    ('Offrite consulenza per la carta dei vini?',
     'Sì. Ti affianchiamo nella costruzione di una carta dei vini bilanciata con il tuo menù e il tuo target, e formiamo il personale di sala a raccontare e proporre le etichette.'),
    ('Organizzate degustazioni nel locale?',
     'Sì, con il Format "Degustazione Guidata" chiavi in mano: progettiamo e allestiamo serate come "L\'ora del calice", con postazioni dedicate, narrazione del prodotto e intrattenimento, senza gravare sul tuo staff.'),
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


def build_graph(prodotti, eventi):
    org_id = f'{SITE}/#azienda'
    a = AZIENDA
    ind = a['indirizzo']

    # Catalogo raggruppato per categoria
    gruppi = {}
    for p in prodotti:
        gruppi.setdefault(p['categoria'], []).append(p)
    catalogo = {
        '@type': 'OfferCatalog',
        'name': 'Catalogo vini e bevande HORECA',
        'itemListElement': [{
            '@type': 'OfferCatalog',
            'name': CATEGORIE.get(cat, cat).capitalize(),
            'itemListElement': [{
                '@type': 'Offer',
                'eligibleCustomerType': 'http://purl.org/goodrelations/v1#Business',
                'businessFunction': 'http://purl.org/goodrelations/v1#Sell',
                'itemOffered': {
                    '@type': 'Product',
                    'name': f"{p['nome']} – {p['cantina']}",
                    'brand': {'@type': 'Brand', 'name': p['cantina']},
                    'category': CATEGORIE.get(cat, cat),
                    'description': p.get('descrizione', ''),
                    'image': [absolute(i) for i in p.get('immagini', [])],
                    'countryOfOrigin': {'@type': 'Country', 'name': 'Italia'},
                    'additionalProperty': [{
                        '@type': 'PropertyValue', 'name': 'Zona di produzione', 'value': p.get('regione', ''),
                    }],
                },
            } for p in lista],
        } for cat, lista in gruppi.items()],
    }

    servizi = [
        ('Consegne rapide senza minimi d\'ordine', 'Consegne frazionate in 48/72 ore, senza minimi d\'ordine, per locali HORECA.'),
        ('Catalogo esclusivo HORECA', 'Etichette artigianali e micro-produzioni assenti dalla grande distribuzione.'),
        ('Consulenza carta dei vini', 'Costruzione della carta dei vini e formazione del personale di sala.'),
        ('Format Degustazione Guidata', 'Serate di degustazione chiavi in mano nel locale del cliente.'),
    ]

    graph = [
        {
            '@type': ['LocalBusiness', 'Organization'],
            '@id': org_id,
            'name': a['nome'],
            'alternateName': a['alias'],
            'slogan': a['slogan'],
            'description': 'Distributore di vini e bevande d\'eccellenza esclusivamente per il settore HORECA: '
                           'cantine artigianali assenti dalla grande distribuzione, nessun minimo d\'ordine, '
                           'consegne in 48/72 ore, consulenza sulla carta dei vini e degustazioni guidate.',
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
                {'@type': 'City', 'name': 'Ferrara'},
                {'@type': 'AdministrativeArea', 'name': 'Provincia di Ferrara'},
                {'@type': 'AdministrativeArea', 'name': 'Emilia-Romagna'},
                {'@type': 'Country', 'name': 'Italia'},
            ],
            'knowsAbout': ['Distribuzione vini HORECA', 'Vini artigianali', 'Vini calabresi IGP',
                           'Carta dei vini per ristoranti', 'Formazione personale di sala',
                           'Degustazioni guidate', 'Amari artigianali'],
            'openingHoursSpecification': [{
                '@type': 'OpeningHoursSpecification',
                'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens': '08:30', 'closes': '18:30',
            }],
            'contactPoint': [{
                '@type': 'ContactPoint', 'contactType': 'sales', 'telephone': a['telefono'], 'email': a['email'],
                'areaServed': 'IT', 'availableLanguage': ['Italian'],
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
            'inLanguage': 'it-IT',
            'publisher': {'@id': org_id},
        },
        {
            '@type': 'WebPage',
            '@id': f'{SITE}/#pagina',
            'url': f'{SITE}/',
            'name': 'Distributore vini HORECA | S.F.M. Distribuzione – Vini d\'eccellenza',
            'isPartOf': {'@id': f'{SITE}/#sito'},
            'about': {'@id': org_id},
            'primaryImageOfPage': {'@type': 'ImageObject', 'url': absolute('assets/og-image.jpg'), 'width': 1200, 'height': 630},
            'inLanguage': 'it-IT',
            'datePublished': TODAY,
            'dateModified': TODAY,
        },
        {
            '@type': 'FAQPage',
            '@id': f'{SITE}/#faq',
            'isPartOf': {'@id': f'{SITE}/#pagina'},
            'mainEntity': [{
                '@type': 'Question', 'name': q,
                'acceptedAnswer': {'@type': 'Answer', 'text': r},
            } for q, r in FAQ],
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
            'description': e.get('descrizione', ''),
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


def build_head(graph):
    a = AZIENDA
    title = 'Distributore vini HORECA | S.F.M. Distribuzione – Vini d\'eccellenza'
    desc = ('Distributore di vini d\'eccellenza solo per HORECA: cantine artigianali assenti dalla GDO, '
            'zero minimi d\'ordine, consegne in 48/72h e consulenza carta vini.')
    og_desc = ('Cantine artigianali assenti dalla grande distribuzione, nessun minimo d\'ordine, consegne in 48/72 ore '
               'e degustazioni guidate per ristoranti, bar, enoteche e hotel.')
    jsonld = json.dumps(graph, ensure_ascii=False, indent=2)
    jsonld = '\n'.join('  ' + line for line in jsonld.split('\n'))
    return f'''  <!-- ==========================================================================
       META / SEO  (generata da .claude/genera-seo.py — modificare lì e rilanciare)
       ========================================================================== -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="{a['nome']}">
  <meta name="keywords" content="distributore vini HORECA, distribuzione vini ristoranti, fornitore vini bar, vini per enoteche, vini artigianali, vini calabresi IGP, consulenza carta dei vini, degustazioni guidate, nessun minimo d'ordine, Ferrara">
  <meta name="theme-color" content="#000000">
  <meta name="color-scheme" content="dark">
  <meta name="format-detection" content="telephone=yes">
  <link rel="canonical" href="{SITE}/">
  <link rel="alternate" hreflang="it" href="{SITE}/">
  <link rel="alternate" hreflang="x-default" href="{SITE}/">

  <!-- Geo (SEO locale): Ferrara -->
  <meta name="geo.region" content="IT-{a['indirizzo']['provincia']}">
  <meta name="geo.placename" content="{a['indirizzo']['citta']}">
  <meta name="geo.position" content="{a['lat']};{a['lng']}">
  <meta name="ICBM" content="{a['lat']}, {a['lng']}">

  <!-- Open Graph / social -->
  <meta property="og:type" content="website">
  <meta property="og:locale" content="it_IT">
  <meta property="og:site_name" content="{a['nome']}">
  <meta property="og:title" content="{a['nome']} – Vini e bevande d'eccellenza per l'HORECA">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{SITE}/">
  <meta property="og:image" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:secure_url" content="{SITE}/assets/og-image.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="S.F.M. Vini d'eccellenza – Un viaggio nel mondo del vino">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{a['nome']} – Vini d'eccellenza per l'HORECA">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
  <meta name="twitter:image:alt" content="S.F.M. Vini d'eccellenza – Un viaggio nel mondo del vino">

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
'''


def main():
    js = (ROOT / 'script.js').read_text(encoding='utf-8')
    prodotti = parse_array(js, 'PRODOTTI')
    eventi = parse_array(js, 'EVENTI')
    graph = build_graph(prodotti, eventi)

    html_path = ROOT / 'index.html'
    html = html_path.read_text(encoding='utf-8')
    start = html.index('  <!-- ==========================================================================\n       META / SEO')
    end = html.index('</head>')
    html = html[:start] + build_head(graph) + html[end:]
    html_path.write_text(html, encoding='utf-8')
    print(f'OK: {len(prodotti)} prodotti, {len(eventi)} locandine eventi, {len(FAQ)} FAQ')


if __name__ == '__main__':
    main()
