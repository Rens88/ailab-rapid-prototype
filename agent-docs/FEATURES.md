# Features — Baseline
**KNLTB — Nationaal Tennis Centrum**
Versie 1.0 — 15 mei 2026

## Leeswijzer
Elk feature-blok is gekoppeld aan één of meer user stories en bevat: wat het systeem doet, hoe het zich gedraagt (inclusief randgevallen), acceptatiecriteria en wat expliciet buiten scope valt voor de MVP.

---

## F-01 — Gecombineerde weekweergave (startscherm)

**Gelinkt aan:** US-01, US-02
**Prioriteit:** Must-have (MVP)

### Beschrijving
Het startscherm van Baseline toont na inloggen direct een gecombineerde weekweergave met twee secties naast of onder elkaar: groepsplanning en aanwezigheid staf & spelers. De huidige week is standaard geselecteerd. Gebruikers kunnen navigeren naar vorige of volgende weken. Het scherm laadt binnen 3 seconden.

### Gedrag

**Initieel laden:**
- Na succesvolle Azure AD-authenticatie wordt de gecombineerde weekweergave geladen voor de huidige ISO-week
- Alle drie de datasecties worden parallel opgehaald via de Graph API (of cache)
- Een laadspinner is zichtbaar zolang data nog wordt opgehaald
- Zodra alle secties geladen zijn, verdwijnt de spinner en is de volledige weergave zichtbaar

**Weeknavigatie:**
- Links/rechts pijlknoppen en/of swipe-gebaar (mobiel) navigeren naar de vorige/volgende week
- Bij elke weekwisseling worden de drie secties opnieuw geladen (vanuit cache indien beschikbaar)
- Een "deze week"-knop brengt de gebruiker altijd terug naar de huidige week
- Het weeknummer en de datumrange (bijv. "Week 21 — 18–24 mei 2026") zijn zichtbaar in de header

**Tijdstempel:**
- Onder of naast de weekheader is zichtbaar wanneer de data voor het laats is gesynchroniseerd ("Laatste update: [datum] om [tijd]")
- Als de laatste succesvolle sync meer dan [drempelwaarde, zie OB-06] geleden was, kleurt het tijdstempel oranje/rood

**Responsiviteit:**
- Op desktop (≥ 1280px): twee secties naast elkaar in een twee-kolomslayout
- Op tablet (768–1279px): twee kolommen of gestapeld afhankelijk van schermruimte
- Op smartphone (≤ 390px): gestapelde weergave, elke sectie als inklapbaar blok

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Graph API niet bereikbaar bij laden | Foutmelding per sectie: "Kon data niet ophalen. Laatste bekende stand: [tijdstempel]." Overige secties laden normaal. |
| Eén van de drie bronbestanden ontbreekt of is leeg | Betreffende sectie toont gele vlag met bericht "Geen data beschikbaar voor deze periode" |
| Gebruiker navigeert naar een week meer dan 52 weken in het verleden | Systeem toont beschikbare data; als bronbestand die periode niet dekt, gele vlag met melding |
| Gebruiker opent Baseline op een langzame verbinding (> 3 sec laadtijd) | Laadspinner blijft zichtbaar; na 10 seconden verschijnt een melding "Het laden duurt langer dan verwacht" |
| Sessie verlopen (Azure AD token verlopen) | Gebruiker wordt doorgestuurd naar Azure AD-inlogscherm; na inloggen teruggeleid naar dezelfde weekweergave |

### Acceptatiecriteria
- [ ] Startscherm toont beide secties (groepsplanning en aanwezigheid) na inloggen zonder extra klik
- [ ] Laadtijd ≤ 3 seconden op een standaard kantoorverbinding (gemeten via performance-test bij elke release)
- [ ] Weeknavigatie werkt op desktop (klik) én smartphone (klik of swipe)
- [ ] Tijdstempel is zichtbaar op elke weergave
- [ ] Responsieve layout is gevalideerd op viewport 1280px en 390px

### Niet in scope (MVP)
- Aanpasbare dashboardlayout (gebruiker kan secties herordenen)
- Exporteren of printen van de weekweergave
- Pushmeldingen bij wijzigingen in de data
- Integratie met Outlook-agenda

---

## F-02 — Groepsplanning dashboard

**Gelinkt aan:** US-03, US-04
**Prioriteit:** Must-have (MVP)

### Beschrijving
De groepsplanningsectie toont per week de activiteiten van alle vijf groepen (Groep 1, 2, 3, 4, Rolstoeltennis). Activiteiten worden geclassificeerd als toernooi, event, testdag, bijeenkomst of vakantie/vrij, en zijn kleurgecodeerd. De sectie is filterbaar op groep. Ontbrekende planning wordt gesignaleerd met een gele vlag.

### Gedrag

**Weergave:**
- Per groep wordt een rij of blok getoond met de activiteiten van de geselecteerde week
- Activiteitstypes zijn kleurgecodeerd (kleuren worden bepaald in het ontwerp; dit is een Open Besluit voor de UI-fase)
- Groepen zonder activiteiten in de geselecteerde week tonen "Geen activiteiten gepland" — dit is neutraal, geen gele vlag
- Groepen waarvan de brondata voor die week ontbreekt of ouder is dan de drempelwaarde tonen een gele vlag

**Filteren:**
- Een filtercomponent (dropdown of chips) boven de sectie laat toe om één of meerdere groepen te selecteren
- "Alle groepen" is de standaardinstelling bij elke sessie
- De filterinstelling blijft actief bij navigatie tussen weken binnen dezelfde sessie

**Datahiërarchie:**
- Groep 1 en 2 leveren planningsdata op jaarniveau (volledige jaarplanning verwacht)
- Groep 3, 4 en Rolstoeltennis leveren planningsdata per speler en per coach
- De weergave aggregeert per groep, niet per individuele speler (individuele drill-down is onderdeel van F-03)

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Bronbestand voor één groep ontbreekt op SharePoint | Gele vlag voor die groep; overige groepen worden normaal getoond |
| Activiteit zonder type-classificatie in het bronbestand | Activiteit wordt weergegeven als "Overig" met neutrale kleur |
| Activiteit met overlappende datums (bijv. een toernooi + vakantie op dezelfde dag) | Beide activiteiten worden getoond; geen automatische conflictresolutie |
| Filter geselecteerd op groep die geen data heeft | Gele vlag zichtbaar; geen leeg scherm of foutmelding |

### Acceptatiecriteria
- [ ] Alle vijf groepen zijn zichtbaar in de standaardweergave
- [ ] Minimaal vijf activiteitstypes worden onderscheiden en kleurgecodeerd weergegeven
- [ ] Filter op groep werkt correct en blijft actief bij weeknavigatie
- [ ] Gele vlag verschijnt als brondata ontbreekt of ouder is dan de drempelwaarde
- [ ] "Geen activiteiten gepland" wordt neutraal weergegeven (geen vlag, geen foutmelding)

### Niet in scope (MVP)
- Activiteiten bewerken of toevoegen vanuit het dashboard
- Conflictdetectie tussen groepen
- Exporteren naar kalenderformaat
- Historische trendanalyse over meerdere seizoenen

---

## F-03 — Aanwezigheid staf & spelers

**Gelinkt aan:** US-05, US-06
**Prioriteit:** Must-have (MVP)

### Beschrijving
De aanwezigheidssectie toont per week voor elk staflid en elke speler hun status: aanwezig NTC, extern (toernooi, reis, vrij) of onbekend/niet ingevuld. Staf en spelers zijn gescheiden weergegeven. De sectie is doorzoekbaar op naam. Klikken op een persoon opent een drill-down met de aanwezigheid voor de komende vier weken.

### Gedrag

**Weekoverzicht:**
- Stafleden en spelers worden in twee gescheiden blokken getoond
- Per persoon is de aanwezigheidsstatus voor de geselecteerde week zichtbaar als een pictogram of label: ✅ Aanwezig NTC / 🌍 Extern / ❓ Onbekend
- "Onbekend" (niet ingevuld) wordt weergegeven als gele vlag per persoon
- Personen zijn sorteerbaar op naam (alfabetisch, standaard)

**Zoeken en filteren:**
- Een zoekveld laat toe om op naam te filteren (stafleden en spelers)
- Zoekresultaten verschijnen direct bij het typen (geen confirmatiestap nodig)

**Drill-down:**
- Klikken op een naam opent een detailpaneel of -pagina voor die persoon
- Het detailpaneel toont de aanwezigheidsstatus voor de huidige week + 3 opvolgende weken (4 weken totaal)
- Weken zonder ingevulde data tonen een gele vlag in het detailpaneel
- Terugknop of swipe-gebaar brengt terug naar het weekoverzicht

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Aanwezigheidsdata van een staflid ontbreekt volledig | Staflid zichtbaar in lijst met gele vlag; geen verborgen records |
| Speler is niet ingedeeld in een groep (tijdelijk) | Speler zichtbaar in de spelerslijst; groepskolom leeg of "n.v.t." |
| Drill-down van persoon zonder data voor komende 4 weken | Alle weken tonen gele vlag; melding "Geen aanwezigheidsdata beschikbaar voor deze periode" |
| Zoekopdracht levert geen resultaten op | Lege staat met melding "Geen resultaten voor '[zoekopdracht]'" |
| Gebruiker bekijkt drill-down op smartphone | Detailpaneel opent als volledig scherm (niet als zijpaneel); terugknop prominent in header |

### Acceptatiecriteria
- [ ] Alle stafleden en spelers zijn zichtbaar in het overzicht, gescheiden per categorie
- [ ] Drie aanwezigheidsstatussen zijn onderscheidbaar weergegeven
- [ ] Gele vlag verschijnt per persoon als aanwezigheidsdata ontbreekt
- [ ] Zoekopdracht op naam filtert het overzicht in real-time
- [ ] Drill-down toont minimaal 4 weken; laadt binnen 2 seconden
- [ ] Drill-down is volledig bruikbaar op smartphone

### Niet in scope (MVP)
- Aanwezigheid bewerken vanuit het dashboard
- Pushmeldingen als iemand zijn aanwezigheid niet heeft ingevuld
- Integratie met persoonlijke Outlook-agenda's
- Automatische aanwezigheidstracking (bijv. via badge of locatiedata)

---

## F-04 — Chatbox: planningsvragen

**Gelinkt aan:** US-07, US-08, US-09
**Prioriteit:** Must-have (MVP)

### Beschrijving
Een conversationele chatbox stelt gebruikers in staat om in gewone Nederlandse taal vragen te stellen over de groepsplanning en aanwezigheid van staf en spelers. De chatbox is aangedreven door Azure OpenAI (EU-endpoint) en beantwoordt uitsluitend vragen die beantwoord kunnen worden met de live dashboarddata. Vragen buiten deze domeinen worden expliciet geweigerd. De chatbox is beschikbaar op alle pagina's en werkt op desktop én smartphone.

### Gedrag

**Invoer en antwoord:**
- Een persistente chatbox-knop of -balk is zichtbaar op elke dashboardpagina
- Gebruiker typt een vraag in gewone taal (bijv. "Wie is er volgende week dinsdag aanwezig?")
- De chatbox haalt de relevante data op uit de actuele dashboarddata (via Graph API / cache)
- Het antwoord verschijnt als leesbare tekst binnen 5 seconden
- De chatbox toont een laadanimatie zolang het antwoord wordt opgebouwd

**Scope-bewaking:**
- De chatbox beantwoordt uitsluitend vragen over: groepsplanning en aanwezigheid staf/spelers
- Vragen over andere onderwerpen (bijv. voedingsadvies, externe toernooiuitslagen, algemene kennis) worden geweigerd met de melding: "Dit valt buiten wat ik kan opzoeken — ik kan alleen vragen beantwoorden over de groepsplanning en aanwezigheid."
- De chatbox verzint nooit data: als informatie ontbreekt, zegt hij dat expliciet

**Geheugenbeheer:**
- De chatbox heeft geen geheugen over sessies heen (elke sessie begint blanco)
- Binnen een sessie kan de chatbox verwijzen naar de vorige vraag in hetzelfde gesprek (bijv. "En voor die persoon — volgende week?")

**Smartphone-gebruik:**
- De chatbox opent als een volledig scherm of een groot panel op smartphone
- Invoer via touchtoetsenbord; antwoord leesbaar zonder horizontaal scrollen of inzoomen

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Gevraagde data ontbreekt in de bronbestanden | Chatbox antwoordt: "De [aanwezigheids/plannings/baanschema]data voor [periode] is niet (volledig) ingevuld." Geen geraden antwoord. |
| Azure OpenAI-service niet bereikbaar | Chatbox toont melding: "De chatbox is momenteel niet beschikbaar. Gebruik het dashboard om de informatie op te zoeken." |
| Vraag bevat een naam die niet voorkomt in de data | Chatbox antwoordt: "Ik ken geen [naam] in de aanwezigheidsdata. Controleer de schrijfwijze of kies een naam uit het overzicht." |
| Gebruiker stelt een vraag in het Engels | Chatbox antwoordt in het Engels als de vraag in het Engels is gesteld (taal volgt de gebruiker) |
| Vraag is ambigu (bijv. "Wie is er dinsdag?") | Chatbox vraagt om verduidelijking: "Bedoel je aanstaande dinsdag [datum]?" |
| Lange aanwezigheidslijst als antwoord | Antwoord toont de eerste 10 namen + "en [X] anderen" met optie om alles te tonen |

### Acceptatiecriteria
- [ ] Chatbox is bereikbaar op elke dashboardpagina zonder navigatie
- [ ] Antwoord verschijnt binnen 5 seconden voor een gemiddelde vraag
- [ ] Chatbox weigert vragen buiten groepsplanning en aanwezigheid met een begrijpelijke melding
- [ ] Chatbox verzint nooit data; bij ontbrekende data volgt een expliciete melding
- [ ] Chatbox werkt volledig op smartphone: invoer, antwoord en weigering leesbaar zonder zoomen
- [ ] Bij onbeschikbaarheid van Azure OpenAI toont chatbox een begrijpelijke foutmelding

### Niet in scope (MVP)
- Chatbox-geheugen over sessies heen
- Spraakinvoer of spraakuitvoer
- Chatbox die planning kan wijzigen of acties kan uitvoeren
- Logging van chatbox-vragen of -antwoorden (zie P-08)

---

## F-05 — Gele vlag & datakwaliteitsindicatoren

**Gelinkt aan:** US-10, US-11
**Prioriteit:** Must-have (MVP)

### Beschrijving
Baseline signaleert proactief wanneer data ontbreekt, verouderd is of niet is bijgewerkt, via een gele vlag-systeem. Elke datasectie en elke individuele record (groep, persoon, baan) kan een gele vlag tonen. Een globale tijdstempel toont wanneer de laatste datasync succesvol was.

### Gedrag

**Gele vlag — triggers:**
- Datasectie van een groep: bronbestand ontbreekt op SharePoint, of data is ouder dan de drempelwaarde (OB-05)
- Individueel staflid of speler: aanwezigheidsdata voor komende week ontbreekt
- Chatbox-antwoord: chatbox markeert welke specifieke data ontbreekt in zijn antwoord

**Gele vlag — weergave:**
- Een geel vlagicoon (⚑ of equivalente visuele indicator) verschijnt bij het betreffende blok
- Bij aanwijzen of klikken op de vlag verschijnt een tooltip of uitlegpaneel met: "Geen data beschikbaar" of "Niet bijgewerkt sinds [datum]"
- Vlaggen verdwijnen automatisch zodra de brondata is bijgewerkt en Baseline nieuwe data heeft opgehaald

**Tijdstempel globale sync:**
- Een tijdstempel ("Laatste update: [datum] om [tijd]") is zichtbaar in de header van elke pagina
- Bij een succesvolle Graph API-sync wordt de tijdstempel bijgewerkt
- Bij een mislukte sync meer dan [drempelwaarde] geleden kleurt de tijdstempel oranje/rood

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Drempelwaarde OB-05 nog niet bepaald | Systeem gebruikt een standaardwaarde van 48 uur tot OB-05 is besloten; dit is zichtbaar in de systeeminstellingen |
| Meerdere vlaggen tegelijkertijd zichtbaar | Elke vlag staat op zijn eigen record; geen aggregatie of "totaal X vlaggen" teller in de MVP |
| Brondata wordt bijgewerkt terwijl gebruiker het dashboard open heeft | Vlag verdwijnt bij de eerstvolgende datasync-cyclus, niet real-time mid-sessie |

### Acceptatiecriteria
- [ ] Gele vlag verschijnt bij ontbrekende of verouderde data op groeps-, persoons- en baanniveau
- [ ] Tooltip of uitleg bij de vlag is leesbaar op zowel desktop als smartphone
- [ ] Vlaggen verdwijnen automatisch na een succesvolle datasync
- [ ] Tijdstempel is zichtbaar op elke pagina en kleurt bij verouderde sync
- [ ] Standaarddrempelwaarde van 48 uur is geconfigureerd als fallback voor OB-05

### Niet in scope (MVP)
- E-mailalerts of pushmeldingen op basis van gele vlaggen
- Aggregatieteller ("X items vereisen aandacht")
- Dashboard-brede kwaliteitsscore of rapportage

---

## F-06 — Authenticatie via Azure AD SSO

**Gelinkt aan:** US-12
**Prioriteit:** Must-have (MVP)

### Beschrijving
Baseline gebruikt Azure Active Directory Single Sign-On (SSO) via de KNLTB Microsoft-tenant voor authenticatie. Gebruikers loggen in met hun bestaande KNLTB-Microsoft account. Er zijn geen aparte credentials voor Baseline. Gebruikers zonder geldig KNLTB-account hebben geen toegang.

### Gedrag

**Inlogstroom:**
- Bij het openen van Baseline wordt de gebruiker doorgestuurd naar de Azure AD-inlogpagina als er geen actieve sessie is
- Een gebruiker die al is ingelogd op hun Microsoft-account (bijv. Outlook) wordt via SSO automatisch herkend en doorgeleid naar het dashboard
- Na succesvolle authenticatie wordt de gecombineerde weekweergave getoond

**Sessiebeheer:**
- Sessieduur volgt het KNLTB IT-beleid voor Azure AD-tokenverloop
- Na verloop van de sessie wordt de gebruiker opnieuw gevraagd in te loggen; na hernieuwde login wordt teruggekeerd naar de pagina die de gebruiker aan het bekijken was

**Toegangsbeheer:**
- Alle geauthenticeerde KNLTB-stafleden zien dezelfde data (geen rolscheiding in MVP)
- Accounts buiten de KNLTB-tenant worden geweigerd met een begrijpelijke melding

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Gebruiker heeft geen KNLTB Microsoft-account | Inlogpagina toont melding "Toegang vereist een KNLTB-account. Neem contact op met IT." |
| Azure AD-service niet bereikbaar | Baseline toont: "Inloggen is momenteel niet mogelijk. Probeer het later opnieuw." |
| Token verlopen mid-sessie | Gebruiker wordt stil doorgestuurd naar inlogscherm; na herlogin teruggeleid naar vorige pagina |
| Gebruiker opent Baseline op smartphone in een app-browser (bijv. Teams) | SSO-stroom werkt via in-app browser; indien niet ondersteund, wordt externe browser-redirect aangeboden |

### Acceptatiecriteria
- [ ] Gebruikers loggen in met bestaand KNLTB Microsoft-account via Azure AD SSO
- [ ] Gebruikers met een actieve Microsoft-sessie worden automatisch ingelogd (SSO, geen extra stap)
- [ ] Gebruikers buiten de KNLTB-tenant worden geweigerd met een begrijpelijke melding
- [ ] Na sessieverloop wordt de gebruiker teruggeleid naar de oorspronkelijke pagina na herlogin
- [ ] Graph API-rechten zijn beperkt tot lezen (geen schrijfrechten aangevraagd)

### Niet in scope (MVP)
- Rolgebaseerde toegangsniveaus (fase 2, zie OB-04)
- Gastaccounts of externe toegang voor niet-KNLTB-gebruikers
- Multi-factor authenticatie (volgt KNLTB IT-beleid; niet apart te configureren door Baseline)

---

## Technische Afhankelijkheden

| Feature | Afhankelijkheid | Risico | Mitigatie |
|---|---|---|---|
| F-01 t/m F-03 | Microsoft Graph API — leesbevoegdheden op SharePoint-bestanden | **Hoog** — kern van de architectuur; als Graph API-integratie faalt, heeft het dashboard geen data | Vroeg in development integratie bouwen en testen; fallback naar handmatige CSV-upload als noodoptie voor pilot |
| F-04 (Chatbox) | Azure OpenAI EU-endpoint beschikbaarheid en latency | **Middel** — als Azure OpenAI latency > 5 sec is, voldoet chatbox niet aan acceptatiecriterium | Streaming responses implementeren zodat gebruiker direct ziet dat antwoord wordt opgebouwd; timeout na 10 sec |
| F-04 (Chatbox) | Standaardisering Excel-invoerformaten — OB-02 | **Hoog** — als bronbestanden inconsistente structuur hebben, kan chatbox data niet betrouwbaar interpreteren | OB-02 oplossen vóór chatbox in productie gaat; chatbox laten testen met alle bronbestandsformaten |
| F-06 (Auth) | Azure AD app-registratie in KNLTB-tenant | **Laag** — standaard configuratie; afhankelijk van medewerking KNLTB IT | Vroeg in project aanvragen; doorlooptijd IT-afdeling inplannen |
| Alle features | Datakwaliteit bronbestanden — gebruikers vullen Excels correct in | **Hoog** — het grootste pilotrisico; slechte invoer = onbetrouwbaar dashboard | Afspraken over invoerstandaard (OB-02) + begeleide onboarding eerste weken |

---

## MVP Releasecriteria

De pilot mag niet starten totdat aan het volgende is voldaan:

- [ ] **F-01 t/m F-03**: Gecombineerde weekweergave laadt correct met echte data uit SharePoint (end-to-end test geslaagd)
- [ ] **F-04**: Chatbox beantwoordt minimaal 10 testscenario's correct (inclusief weigering buiten-scope-vragen) met echte data
- [ ] **F-06**: Azure AD SSO werkt voor alle KNLTB-stafleden; toegang buiten tenant geweigerd
- [ ] **P-01 / P-02**: Data-integriteitstest geslaagd (geen data-mix-up); AVG-beoordeling door DPO / juridisch KNLTB afgerond
- [ ] **OB-02**: Invoerstandaard voor alle Excel-bronbestanden vastgesteld en gecommuniceerd aan alle groepen
- [ ] **OB-05**: Drempelwaarde voor gele vlag bepaald en geconfigureerd
- [ ] Performance-test: laadtijd gecombineerde weekweergave ≤ 3 seconden onder realistische testomstandigheden
- [ ] Responsiviteitstest: alle weergaven gevalideerd op desktop (1280px) en smartphone (390px)
- [ ] Begeleide onboardingsessie gepland voor de eerste gebruikersweek
- [ ] In-product feedbackmechanisme (duim omhoog/omlaag) actief op het dashboard
