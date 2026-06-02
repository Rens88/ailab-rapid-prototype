# User Stories — Team DNA
**Koninklijke Nederlandse Voetbalbond (KNVB)**
Versie 1.0 — mei 2026

---

## Actoren

| Actor | Omschrijving |
|---|---|
| **Scout (hoofd)** | Primaire gebruiker. Voert de tegenstander analyse uit, combineert tool-output met eigen video-observaties en presenteert de analyse aan de bondscoach en staf. Technisch niveau: middel-hoog. Werkt primair op laptop/desktop. |
| **Performance analist** | Secundaire gebruiker. Beheert en verrijkt de event data, ondersteunt de scout bij de interpretatie van statistieken en draagt bij aan de kwaliteitscontrole van de output. Technisch niveau: hoog. |
| **Bondscoach / staf** | Ontvanger van de output. Gebruikt de geëxporteerde PDF als voorbereiding op wedstrijdbesprekingen. Heeft geen directe toegang tot de tool. |
| **Ontwikkelaar / beheerder** | Beheert de vragenset, prompttemplates en pipeline-configuratie. Heeft volledige toegang tot de tool-infrastructuur. |

---

## Epicoverzicht

| Epic | Omschrijving | Stories |
|---|---|---|
| E-01 | Analyse starten en data selecteren | US-01, US-02 |
| E-02 | Rapport genereren | US-03, US-04, US-05 |
| E-03 | Betrouwbaarheid en traceerbaarheid | US-06, US-07, US-08 |
| E-04 | Rapport exporteren en delen | US-09 |
| E-05 | Spelersverdieping (optioneel) | US-10 |

---

## E-01 — Analyse starten en data selecteren

### US-01 — Tegenstander analyse starten

```
Als scout
wil ik een tegenstander analyse kunnen starten door een team te selecteren
zodat ik snel een gestructureerd startpunt heb voor mijn wedstrijdvoorbereiding
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout
**Context:** Reguliere voorbereiding (1–3 weken voor wedstrijd) of toernooisetting (2–5 dagen voor wedstrijd)

**Acceptatiecriteria:**
- [ ] De gebruiker kan een team selecteren uit de beschikbare tegenstanders in het datawarehouse
- [ ] Na selectie start de analysepipeline automatisch zonder verdere handmatige stappen van de gebruiker
- [ ] De tool geeft feedback aan de gebruiker dat de analyse wordt gegenereerd (voortgangsindicatie)
- [ ] Als het geselecteerde team geen of onvoldoende data heeft, meldt de tool dit expliciet vóórdat de pipeline start

---

### US-02 — Automatische wedstrijdselectie

```
Als scout
wil ik dat het systeem automatisch de meest recente wedstrijden van de tegenstander selecteert
zodat ik geen tijd kwijt ben aan handmatige dataselectie en de analyse altijd gebaseerd is op actuele data
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout / Performance analist
**Context:** Tijdskritisch bij toernooivoorbereiding

**Acceptatiecriteria:**
- [ ] Het systeem selecteert automatisch de N meest recente wedstrijden van de tegenstander (N = open besluit OB-04)
- [ ] De geselecteerde wedstrijden zijn zichtbaar in het rapport (datum, opponent, competitie)
- [ ] Als er minder dan het minimale aantal wedstrijden beschikbaar is, genereert het systeem de analyse op basis van de beschikbare wedstrijden en verlaagt het de datadekkingindicator dienovereenkomstig
- [ ] De selectie omvat zowel internationale wedstrijden (nationale team) als clubwedstrijden van de spelers, voor zover beschikbaar in het datawarehouse

---

## E-02 — Rapport genereren

### US-03 — Speelstijlsamenvatting ontvangen

```
Als scout
wil ik een Nederlandse samenvatting van de speelstijl van de tegenstander ontvangen
zodat ik snel een kwalitatief beeld krijg van hoe de tegenstander speelt
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] Het rapport bevat een speelstijlsamenvatting die de aanvallende organisatie beschrijft (bijv. opbouwwijze, aanvalspatronen, dieptespel)
- [ ] Het rapport beschrijft de verdedigende organisatie (bijv. pressing, verdedigende linie, omschakelmoment)
- [ ] De samenvatting is geschreven in begrijpelijk Nederlands, met gebruik van gangbare voetbalterminologie
- [ ] De samenvatting bevat geen conclusies die niet teruggevonden kunnen worden in de onderliggende data
- [ ] De sectie heeft een datadekkingindicator (Hoog / Middel / Laag)

---

### US-04 — Sterktes en zwaktes per spelfase ontvangen

```
Als scout
wil ik een overzicht van sterktes en zwaktes per spelfase van de tegenstander
zodat ik gerichte aandachtspunten heb die ik kan toetsen en verdiepen via video-analyse
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] Het rapport bevat sterktes en zwaktes voor minimaal de volgende spelfasen: aanvallende opbouw, verdedigende organisatie, omschakeling aanval→verdediging, omschakeling verdediging→aanval
- [ ] Per fase worden maximaal 3–5 bevindingen gepresenteerd (geen uitputtende lijst)
- [ ] Elke bevinding is voorzien van een zekerheidsaanduiding (datadekkingindicator) en bronverwijzing (zie US-06 en US-07)
- [ ] De sectie maakt onderscheid tussen bevindingen die sterk onderbouwd zijn en bevindingen die indicatief zijn
- [ ] Ontbreekt voldoende data voor een spelfase, dan wordt dit expliciet gemeld (zie US-08)

---

### US-05 — Rapport bevat contextuele aandachtspunten voor de eigen ploeg

```
Als analist
wil ik dat het rapport relevante tactische aandachtspunten benoemt die kunnen worden benut door onze ploeg
zodat de scout en coach gerichte vragen kunnen formuleren voor de wedstrijdbespreking
```

**Prioriteit:** Should-have (MVP als tijd het toelaat)
**Primaire actor:** Performance analist / Scout

**Acceptatiecriteria:**
- [ ] Het rapport bevat een sectie met suggesties voor exploiteerbare patronen of aandachtspunten op basis van de geïdentificeerde zwaktes van de tegenstander
- [ ] Suggesties zijn altijd gekoppeld aan specifieke bevindingen uit de sterktes/zwaktes-sectie en de onderliggende data
- [ ] Suggesties zijn geformuleerd als aandachtspunten ("Uit de data blijkt dat de tegenstander kwetsbaar is voor..."), niet als tactische adviezen ("De ploeg moet...")
- [ ] De sectie heeft een datadekkingindicator

---

## E-03 — Betrouwbaarheid en traceerbaarheid

### US-06 — Bronvermelding per claim

```
Als scout
wil ik dat elke conclusie in het rapport gekoppeld is aan de wedstrijden waarop die conclusie is gebaseerd
zodat ik claims kan terugvinden, zelf kan verifiëren en desgewenst kan opzoeken in videobeelden
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] Elke inhoudelijke bewering in het rapport is voorzien van een verwijzing naar de specifieke wedstrijd(en) waarop zij is gebaseerd (bijv. datum + opponent)
- [ ] De bronvermelding is compact en staat direct bij de claim (niet alleen in een voetnoot of bijlage)
- [ ] Als een claim is gebaseerd op een patroon over meerdere wedstrijden, worden alle betrokken wedstrijden vermeld
- [ ] De wedstrijdreferenties in het rapport komen overeen met de wedstrijden die zijn opgenomen in de automatische selectie (US-02)

---

### US-07 — Datadekkingindicator per sectie

```
Als scout
wil ik per sectie van het rapport kunnen zien hoe sterk de conclusies zijn onderbouwd
zodat ik weet waar ik extra kritisch moet zijn en de output niet overinterpreteer
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout / Performance analist

**Acceptatiecriteria:**
- [ ] Elke sectie van het rapport toont een datadekkingindicator: **Hoog**, **Middel** of **Laag**
- [ ] De indicator wordt berekend op basis van het aantal beschikbare wedstrijden en de volledigheid van de eventdata voor die spelfase
- [ ] De betekenis van de drie niveaus is uitgelegd in het rapport (eenmalig, bijv. in een legenda of inleiding)
- [ ] De indicator is consistent: dezelfde databeschikbaarheid levert altijd hetzelfde label op

---

### US-08 — Expliciete melding bij onvoldoende data

```
Als scout
wil ik dat het systeem expliciet meldt wanneer een sectie niet onderbouwd kan worden vanuit de beschikbare data
zodat ik nooit per ongeluk een ongefundeerde conclusie als vastgesteld feit behandel
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] Als de beschikbare data onvoldoende is om een sectie te genereren, verschijnt de tekst: *"Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse."*
- [ ] De melding vervangt de sectie-inhoud — de sectiekop blijft aanwezig zodat duidelijk is welk onderdeel ontbreekt
- [ ] De tool genereert nooit een best-guess of aannemelijk klinkende tekst als vervanging voor ontbrekende data
- [ ] De datadekkingindicator voor een sectie met deze melding is altijd **Laag**

---

## E-04 — Rapport exporteren en delen

### US-09 — Rapport exporteren als PDF

```
Als scout
wil ik het gegenereerde rapport kunnen exporteren als PDF
zodat ik het kan delen met de bondscoach en staf zonder dat zij toegang tot de tool nodig hebben
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] De gebruiker kan het rapport met één actie exporteren als PDF
- [ ] De PDF bevat alle secties van het rapport, inclusief datadekkingindicatoren, bronvermeldingen en eventuele visualisaties
- [ ] De PDF is in het Nederlands en leesbaar zonder toegang tot de tool
- [ ] De PDF bevat een koptekst met: naam tegenstander (na mapping terug naar echte naam), datum van genereren en het KNVB-logo of projectnaam
- [ ] De gegenereerde PDF is offline leesbaar (geen externe afhankelijkheden in het bestand)

---

## E-05 — Spelersverdieping (optioneel)

### US-10 — Spelersprofiel op specifieke positie opvragen

```
Als scout
wil ik optioneel een spelersprofiel kunnen opvragen voor een specifieke positie of speler van de tegenstander
zodat ik gerichter kan kijken naar individuele spelers die relevant zijn voor onze wedstrijdvoorbereiding
```

**Prioriteit:** Should-have (MVP als tijd het toelaat, anders V2)
**Primaire actor:** Scout

**Acceptatiecriteria:**
- [ ] De gebruiker kan na het genereren van het teamrapport een verdiepingsprofiel opvragen voor een specifieke positie (bijv. centrale verdediger, aanvallende middenvelder)
- [ ] Het spelersprofiel bevat: relevante statistieken voor die positie, datadekkingindicator en bronvermelding naar wedstrijden
- [ ] Als data voor een specifieke speler beperkt is (bijv. speler uit kleinere competitie), wordt dit expliciet gemeld met een **Laag**-indicator
- [ ] Spelersprofielen worden gegenereerd op dezelfde anonimiserings- en traceerbaarheidsnormen als het teamrapport

---

## Prioriteitenmatrix

| Story | Epic | Prioriteit | MVP? |
|---|---|---|---|
| US-01 | E-01 | Must-have | ✅ |
| US-02 | E-01 | Must-have | ✅ |
| US-03 | E-02 | Must-have | ✅ |
| US-04 | E-02 | Must-have | ✅ |
| US-05 | E-02 | Should-have | ⚠️ Als tijd het toelaat |
| US-06 | E-03 | Must-have | ✅ |
| US-07 | E-03 | Must-have | ✅ |
| US-08 | E-03 | Must-have | ✅ |
| US-09 | E-04 | Must-have | ✅ |
| US-10 | E-05 | Should-have | ⚠️ Als tijd het toelaat, anders V2 |
