#!/usr/bin/env python3
"""
Genera privacy-policy.html e cookie-policy.html con header, footer e stile del sito.
Uso (dalla cartella del sito):  python3 .claude/genera-legali.py

⚠ I testi sono un MODELLO conforme a GDPR (Reg. UE 2016/679), D.Lgs. 196/2003 e
linee guida del Garante sui cookie (10 giugno 2021): vanno verificati da un
professionista e completati con i dati reali (sede, P.IVA, hosting) prima della
pubblicazione.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.sfmdistribuzioni.com'
AGGIORNATO = '25 ottobre 2026'

# Dati del titolare (P.IVA e hosting ancora da inserire)
TITOLARE = {
    'nome': 'S.F.M. Distribuzione',
    'indirizzo': 'Ferrara (FE)',
    'piva': '00000000000',
    'email': 'info@sfmdistribuzioni.com',
    'telefono': '+39 349 063 0846',
    'hosting': 'il fornitore del servizio di hosting del sito',
}

NAV = [('chi-siamo', 'Chi siamo'), ('servizi', 'Servizi'), ('prodotti', 'Prodotti'),
       ('eventi', 'Eventi'), ('social', 'Social'), ('contatti', 'Contatti')]


def page(slug, title, description, h1, body):
    nav = '\n'.join(f'          <li><a class="main-nav__link" href="index.html#{i}">{t}</a></li>' for i, t in NAV)
    return f'''<!DOCTYPE html>
<html lang="it" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title} | S.F.M. Distribuzione</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, follow">
  <meta name="theme-color" content="#000000">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{SITE}/{slug}">
  <link rel="icon" href="favicon.ico" sizes="48x48">
  <link rel="icon" href="assets/favicon.png" type="image/png" sizes="512x512">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="site.webmanifest">
  <script>document.documentElement.className = document.documentElement.className.replace('no-js', 'js');</script>
  <link rel="stylesheet" href="style.css">
  <script src="script.js" defer></script>
</head>

<body>
  <!-- Pagina generata da .claude/genera-legali.py: modificare lì e rilanciare.
       ⚠ MODELLO da far verificare a un professionista prima della pubblicazione. -->
  <a class="skip-link" href="#contenuto">Vai al contenuto</a>
  <div class="cursor" aria-hidden="true"></div>

  <header class="site-header">
    <div class="site-header__inner container">
      <a class="brand" href="index.html" aria-label="S.F.M. Distribuzione — torna alla home">
        <img src="assets/logo-monogramma.png" alt="S.F.M. Distribuzione — Vini d'eccellenza" width="485" height="480">
      </a>
      <button class="nav-toggle" type="button" aria-label="Apri il menu" aria-expanded="false" aria-controls="main-nav">
        <span class="nav-toggle__line"></span>
        <span class="nav-toggle__line"></span>
      </button>
      <nav class="main-nav" id="main-nav" aria-label="Navigazione principale">
        <ul class="main-nav__list">
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="contenuto" class="legal">
    <article class="container legal__inner">
      <p class="eyebrow">— Note legali</p>
      <h1>{h1}</h1>
      <p class="legal__updated">Ultimo aggiornamento: {AGGIORNATO}</p>
{body}
    </article>
  </main>

  <footer class="site-footer">
    <div class="container site-footer__inner">
      <p class="site-footer__copy">© <span id="year">2026</span> S.F.M. Distribuzione <span class="site-footer__sep" aria-hidden="true">·</span> P.IVA {TITOLARE['piva']}</p>
      <nav class="site-footer__legal" aria-label="Note legali">
        <a class="link" href="privacy-policy.html">Privacy Policy</a>
        <a class="link" href="cookie-policy.html">Cookie Policy</a>
        <button class="link site-footer__cookie" type="button" data-cookie-settings>Preferenze cookie</button>
      </nav>
      <p class="site-footer__credits">web by <a class="link" href="https://www.matteomarino.eu" target="_blank" rel="noopener">Matteo Marino</a></p>
    </div>
  </footer>
</body>
</html>
'''


T = TITOLARE

PRIVACY = f'''
      <p>La presente informativa descrive come <strong>{T['nome']}</strong> tratta i dati personali di chi visita il sito
      <a href="{SITE}">{SITE.replace('https://', '')}</a> e di chi ci contatta, ai sensi degli artt. 13 e 14 del
      Regolamento (UE) 2016/679 (“GDPR”) e del D.Lgs. 196/2003 come modificato dal D.Lgs. 101/2018.</p>

      <ol class="legal__toc">
        <li><a href="#titolare">1. Titolare del trattamento</a></li>
        <li><a href="#dati">2. Dati trattati</a></li>
        <li><a href="#finalita">3. Finalità e basi giuridiche</a></li>
        <li><a href="#conferimento">4. Natura del conferimento</a></li>
        <li><a href="#modalita">5. Modalità e sicurezza</a></li>
        <li><a href="#destinatari">6. Destinatari</a></li>
        <li><a href="#trasferimenti">7. Trasferimenti fuori dall'Unione europea</a></li>
        <li><a href="#conservazione">8. Conservazione</a></li>
        <li><a href="#diritti">9. I tuoi diritti</a></li>
        <li><a href="#minori">10. Minori e bevande alcoliche</a></li>
        <li><a href="#modifiche">11. Modifiche</a></li>
      </ol>

      <h2 id="titolare">1. Titolare del trattamento</h2>
      <p><strong>{T['nome']}</strong><br>
      {T['indirizzo']}<br>
      P.IVA {T['piva']}<br>
      Email: <a href="mailto:{T['email']}">{T['email']}</a> · Telefono: <a href="tel:{T['telefono'].replace(' ', '')}">{T['telefono']}</a></p>
      <p>Non è stato nominato un Responsabile della protezione dei dati (DPO), non essendo obbligatorio per l'attività svolta.</p>

      <h2 id="dati">2. Dati trattati</h2>
      <h3>Dati di navigazione</h3>
      <p>I sistemi informatici che fanno funzionare il sito acquisiscono, nel normale esercizio, alcuni dati la cui
      trasmissione è implicita nell'uso dei protocolli Internet: indirizzo IP, tipo di browser e dispositivo, data e ora
      della richiesta, pagine visitate. Sono usati solo per garantire il funzionamento e la sicurezza del sito.</p>
      <h3>Dati forniti volontariamente</h3>
      <ul>
        <li><strong>Modulo “Richiedi il listino”:</strong> nome e cognome, nome e tipologia del locale, città, email,
        telefono, interessi e messaggio. Il modulo <em>non invia dati ai nostri server</em>: compone un messaggio che si
        apre in WhatsApp o nel tuo programma di posta elettronica. Il trattamento inizia solo quando decidi di inviarlo.</li>
        <li><strong>Contatti diretti</strong> via email, telefono, WhatsApp o social: i dati che scegli di comunicarci.</li>
      </ul>
      <h3>Cookie e tecnologie simili</h3>
      <p>Per i cookie si rimanda alla <a href="cookie-policy.html">Cookie Policy</a>.</p>

      <h2 id="finalita">3. Finalità e basi giuridiche</h2>
      <div class="legal__table-wrap">
        <table>
          <thead><tr><th>Finalità</th><th>Base giuridica</th></tr></thead>
          <tbody>
            <tr><td>Rispondere alle richieste di informazioni e inviare il listino HORECA</td><td>Misure precontrattuali su tua richiesta (art. 6.1.b GDPR)</td></tr>
            <tr><td>Gestire forniture, consegne e rapporti commerciali con i locali clienti</td><td>Esecuzione del contratto (art. 6.1.b GDPR)</td></tr>
            <tr><td>Adempiere a obblighi di legge (fiscali, contabili)</td><td>Obbligo legale (art. 6.1.c GDPR)</td></tr>
            <tr><td>Garantire sicurezza e corretto funzionamento del sito</td><td>Legittimo interesse del Titolare (art. 6.1.f GDPR)</td></tr>
            <tr><td>Mostrare la mappa di Google nella sezione Contatti</td><td>Consenso (art. 6.1.a GDPR), revocabile in ogni momento</td></tr>
          </tbody>
        </table>
      </div>
      <p>I dati non sono usati per profilazione, decisioni automatizzate o invio di pubblicità non richiesta.</p>

      <h2 id="conferimento">4. Natura del conferimento</h2>
      <p>Il conferimento dei dati è facoltativo, ma senza i dati di contatto non possiamo rispondere alle richieste.
      I campi obbligatori del modulo sono contrassegnati con un asterisco.</p>

      <h2 id="modalita">5. Modalità e sicurezza</h2>
      <p>I dati sono trattati con strumenti elettronici e, ove necessario, cartacei, da personale autorizzato, adottando
      misure tecniche e organizzative adeguate a prevenire perdita, uso illecito e accessi non autorizzati. Il sito è
      servito tramite connessione cifrata (HTTPS).</p>

      <h2 id="destinatari">6. Destinatari</h2>
      <p>I dati possono essere comunicati, nei limiti necessari, a:</p>
      <ul>
        <li>{T['hosting']}, che ospita il sito (responsabile del trattamento);</li>
        <li>WhatsApp Ireland Ltd. (gruppo Meta), se scegli di contattarci tramite WhatsApp;</li>
        <li>il fornitore del servizio di posta elettronica del Titolare;</li>
        <li>Google Ireland Ltd., per la mappa nella sezione Contatti (solo con consenso);</li>
        <li>Cloudflare, Inc., che distribuisce tramite cdnjs la libreria grafica usata dall'animazione del sito;</li>
        <li>consulenti fiscali e legali, corrieri e autorità, quando necessario per legge o per eseguire il contratto.</li>
      </ul>
      <p>I dati non sono diffusi né venduti a terzi.</p>

      <h2 id="trasferimenti">7. Trasferimenti fuori dall'Unione europea</h2>
      <p>Alcuni fornitori (Google, Meta, Cloudflare) possono trattare dati negli Stati Uniti. Il trasferimento avviene sulla
      base della decisione di adeguatezza della Commissione europea del 10 luglio 2023 (EU-U.S. Data Privacy Framework),
      per le società aderenti, e/o delle clausole contrattuali standard approvate dalla Commissione.</p>

      <h2 id="conservazione">8. Conservazione</h2>
      <ul>
        <li><strong>Richieste di informazioni</strong> non seguite da un rapporto commerciale: fino a 24 mesi.</li>
        <li><strong>Dati dei clienti</strong>: per la durata del rapporto e, dopo, per 10 anni per gli obblighi
        di conservazione delle scritture contabili (art. 2220 c.c.).</li>
        <li><strong>Dati di navigazione</strong>: per i tempi tecnici stabiliti dal fornitore di hosting, salvo necessità
        di accertamento di reati.</li>
      </ul>

      <h2 id="diritti">9. I tuoi diritti</h2>
      <p>In ogni momento puoi chiedere al Titolare, scrivendo a <a href="mailto:{T['email']}">{T['email']}</a>:</p>
      <ul>
        <li>l'accesso ai tuoi dati e una copia (art. 15);</li>
        <li>la rettifica (art. 16) o la cancellazione (art. 17);</li>
        <li>la limitazione del trattamento (art. 18) e la portabilità (art. 20);</li>
        <li>di opporti al trattamento basato sul legittimo interesse (art. 21);</li>
        <li>di revocare il consenso, senza pregiudicare i trattamenti già effettuati (art. 7.3).</li>
      </ul>
      <p>Hai inoltre il diritto di proporre reclamo al <strong>Garante per la protezione dei dati personali</strong>
      (<a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>).</p>

      <h2 id="minori">10. Minori e bevande alcoliche</h2>
      <p>Il sito è rivolto a operatori professionali del settore HORECA e promuove bevande alcoliche: non è destinato ai
      minori di 18 anni e non raccogliamo consapevolmente dati che li riguardano. Bevi responsabilmente.</p>

      <h2 id="modifiche">11. Modifiche</h2>
      <p>La presente informativa può essere aggiornata. La versione in vigore è sempre pubblicata in questa pagina, con la
      data dell'ultimo aggiornamento indicata in alto.</p>
'''

COOKIE = f'''
      <p>Questa pagina spiega quali cookie e tecnologie simili utilizza il sito
      <a href="{SITE}">{SITE.replace('https://', '')}</a>, gestito da <strong>{T['nome']}</strong>, e come puoi gestirli,
      nel rispetto delle <em>Linee guida cookie e altri strumenti di tracciamento</em> del Garante Privacy (10 giugno 2021).</p>

      <p class="legal__note"><strong>In breve:</strong> usiamo solo strumenti tecnici e, con il tuo consenso, la mappa di
      Google. Nessun cookie di profilazione, pubblicitario o di statistica.</p>

      <ol class="legal__toc">
        <li><a href="#cosa-sono">1. Cosa sono i cookie</a></li>
        <li><a href="#elenco">2. Cookie e tecnologie usati da questo sito</a></li>
        <li><a href="#consenso">3. Come gestiamo il consenso</a></li>
        <li><a href="#browser">4. Gestire i cookie dal browser</a></li>
        <li><a href="#contatti">5. Titolare e contatti</a></li>
      </ol>

      <h2 id="cosa-sono">1. Cosa sono i cookie</h2>
      <p>I cookie sono piccoli file di testo che i siti salvano sul dispositivo dell'utente. Tecnologie simili, come il
      <em>localStorage</em> del browser, permettono di memorizzare informazioni in modo analogo. Si distinguono in:</p>
      <ul>
        <li><strong>tecnici</strong>: necessari al funzionamento del sito o a ricordare le scelte dell'utente; non richiedono consenso;</li>
        <li><strong>analitici</strong>: misurano l'uso del sito (questo sito non ne usa);</li>
        <li><strong>di profilazione e pubblicitari</strong>: tracciano l'utente per scopi commerciali (questo sito non ne usa);</li>
        <li><strong>di terze parti</strong>: impostati da servizi esterni integrati nella pagina, come le mappe.</li>
      </ul>

      <h2 id="elenco">2. Cookie e tecnologie usati da questo sito</h2>
      <div class="legal__table-wrap">
        <table>
          <thead><tr><th>Nome / servizio</th><th>Tipo</th><th>Finalità</th><th>Durata</th><th>Consenso</th></tr></thead>
          <tbody>
            <tr>
              <td><strong>sfm-consenso</strong><br>(prima parte)</td>
              <td>Tecnico — localStorage</td>
              <td>Ricorda le tue scelte sui cookie, così il banner non ricompare a ogni visita</td>
              <td>6 mesi</td>
              <td>Non necessario</td>
            </tr>
            <tr>
              <td><strong>Google Maps</strong><br>google.com</td>
              <td>Terze parti</td>
              <td>Mostra la mappa interattiva nella sezione Contatti. Google può impostare cookie propri
              (ad es. NID) secondo la sua <a href="https://policies.google.com/technologies/cookies?hl=it" target="_blank" rel="noopener">cookie policy</a></td>
              <td>Stabilita da Google</td>
              <td><strong>Sì</strong> — la mappa si carica solo dopo il consenso</td>
            </tr>
            <tr>
              <td><strong>cdnjs</strong><br>Cloudflare</td>
              <td>Servizio tecnico, nessun cookie</td>
              <td>Fornisce la libreria grafica (Three.js) dell'animazione iniziale</td>
              <td>—</td>
              <td>Non necessario</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p>I collegamenti a WhatsApp, Instagram e Facebook sono semplici link: non impostano cookie finché non li apri.
      Una volta sui loro siti si applicano le rispettive informative.</p>

      <h2 id="consenso">3. Come gestiamo il consenso</h2>
      <ul>
        <li>Al primo accesso compare un banner con i pulsanti <strong>“Rifiuta”</strong> e <strong>“Accetta”</strong>,
        di pari evidenza, e l'opzione <strong>“Personalizza”</strong> per scegliere categoria per categoria.</li>
        <li>Chiudere il banner con la <strong>X</strong> equivale a rifiutare i cookie facoltativi.</li>
        <li>Prima del consenso non viene caricato nessun contenuto che imposti cookie di terze parti.</li>
        <li>La scelta viene ricordata per <strong>6 mesi</strong>, dopo i quali ti verrà chiesta di nuovo.</li>
        <li>Puoi modificare o revocare il consenso in qualsiasi momento con il pulsante qui sotto o con il link
        “Preferenze cookie” presente in fondo a ogni pagina.</li>
      </ul>
      <button class="btn btn--outline" type="button" data-cookie-settings>Modifica le preferenze cookie</button>

      <h2 id="browser">4. Gestire i cookie dal browser</h2>
      <p>Puoi anche bloccare o cancellare i cookie dalle impostazioni del browser:</p>
      <ul>
        <li><a href="https://support.google.com/chrome/answer/95647?hl=it" target="_blank" rel="noopener">Google Chrome</a></li>
        <li><a href="https://support.apple.com/it-it/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Safari</a></li>
        <li><a href="https://support.mozilla.org/it/kb/protezione-antitracciamento-avanzata-firefox-desktop" target="_blank" rel="noopener">Mozilla Firefox</a></li>
        <li><a href="https://support.microsoft.com/it-it/microsoft-edge/eliminare-i-cookie-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener">Microsoft Edge</a></li>
      </ul>
      <p>Bloccare i cookie tecnici può impedire al sito di ricordare le tue preferenze.</p>

      <h2 id="contatti">5. Titolare e contatti</h2>
      <p><strong>{T['nome']}</strong> — {T['indirizzo']} — P.IVA {T['piva']}<br>
      Email: <a href="mailto:{T['email']}">{T['email']}</a></p>
      <p>Per tutte le informazioni sul trattamento dei dati personali consulta la <a href="privacy-policy.html">Privacy Policy</a>.</p>
'''


def main():
    (ROOT / 'privacy-policy.html').write_text(page(
        'privacy-policy.html', 'Privacy Policy',
        'Informativa sul trattamento dei dati personali di S.F.M. Distribuzione ai sensi del GDPR (Reg. UE 2016/679).',
        'Privacy <em>Policy</em>', PRIVACY), encoding='utf-8')
    (ROOT / 'cookie-policy.html').write_text(page(
        'cookie-policy.html', 'Cookie Policy',
        'Cookie Policy di S.F.M. Distribuzione: quali cookie usa il sito e come gestire il consenso.',
        'Cookie <em>Policy</em>', COOKIE), encoding='utf-8')
    print('OK: privacy-policy.html, cookie-policy.html')


if __name__ == '__main__':
    main()
