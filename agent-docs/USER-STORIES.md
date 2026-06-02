# User Stories — Trainingsload Shorttrack
**NOC\*NSF / KNSB**
Versie 1.0 — 12 mei 2026

## Actoren

| Actor | Omschrijving |
|---|---|
| **Froukje** | Embedded scientist shorttrack bij KNSB. Technisch niveau: medium (werkt met spreadsheets en AMS, geen programmeerervaring). Primaire gebruiker van de pipeline. Gebruikt de tool op laptop/desktop. Valideert analyseresultaten op basis van domeinkennis. |
| **Niels** | Hoofdcoach shorttrack bij KNSB. Technisch niveau: laag. Ontvangt het actiegerichte outputrapport van Froukje. Neemt op basis van de bevindingen trainingsbesluiten. |
| **DSA-team** | Data Science & Analytics-team van NOC\*NSF. Technisch niveau: hoog. Bouwt en beheert de pipeline. Heeft technische toegang voor ontwikkeling en kwaliteitscontrole. |

---

## Epicoverzicht

| Epic | Omschrijving | Stories |
|---|---|---|
| E-01 | Data-voorbereiding | US-01, US-02, US-03 |
| E-02 | Parameteranalyse | US-04, US-05 |
| E-03 | Outputgeneratie | US-06, US-07 |
| E-04 | Reproduceerbaarheid | US-08 |

---

## E-01 — Data-voorbereiding

### US-01 — Brondata aanleveren aan de pipeline

```
Als Froukje
wil ik de beschikbare data (Kinexon-export, RPE-vragenlijsten, hartslagdata) kunnen aanleveren aan de pipeline
zodat de analyse kan starten zonder dat ik afhankelijk ben van technische ondersteuning van het DSA-team
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje
**Context / tijdsbudget:** Eenmalig per analyse-run; Froukje werkt op laptop/desktop.

**Acceptatiecriteria:**
- [ ] Froukje kan databestanden aanleveren via een duidelijk gedefinieerde methode (CSV-upload of bestandslocatie) zonder code te schrijven.
- [ ] De pipeline bevestigt na aanlevering welke bestanden zijn ontvangen en wat het verwachte formaat is.
- [ ] Bij een onleesbaar of onverwacht bestandsformaat geeft de pipeline een begrijpelijke foutmelding met instructies voor correctie.
- [ ] De originele bronbestanden worden niet gewijzigd door de pipeline (zie P-07).

---

### US-02 — Kwaliteits- en representativiteitscheck uitvoeren

```
Als Froukje
wil ik dat de pipeline automatisch controleert of de Kinexon-dataset representatief genoeg is voor het seizoen
zodat ik geen conclusies trek op basis van een eenzijdige dataset (bijv. alleen relay-trainingen)
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje
**Context / tijdsbudget:** Automatisch vóór elke parameteranalyse; resultaat zichtbaar in het rapport.

**Acceptatiecriteria:**
- [ ] De pipeline berekent het percentage van het seizoen dat gedekt wordt door Kinexon-metingen.
- [ ] Als het dekkingspercentage onder de vastgestelde drempel valt (zie OB-06), stopt de pipeline en geeft een expliciete waarschuwing met: het dekkingspercentage, welke periodes ontbreken, en wat dit betekent voor de betrouwbaarheid van de analyse.
- [ ] Froukje kan na de waarschuwing bewust kiezen om toch door te gaan — dit keuze wordt gelogd.
- [ ] Het rapport vermeldt altijd het dekkingspercentage, ongeacht of de drempel gehaald is.

---

### US-03 — Internal en external load koppelen

```
Als Froukje
wil ik dat de pipeline de Kinexon-data (externe load) automatisch koppelt aan de RPE- en hartslagdata (interne load) per training en per sporter
zodat ik een gecombineerd beeld heb van de totale trainingsbelasting
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje
**Context / tijdsbudget:** Automatische stap in de pipeline; Froukje verifieert de koppeling via het technische rapport.

**Acceptatiecriteria:**
- [ ] Elke training in de gecombineerde dataset is voorzien van een sporterId en datum die aantoonbaar overeenkomen over alle bronnen.
- [ ] Sessies die niet gekoppeld kunnen worden (bijv. geen overeenkomende datum of sporterId in Kinexon én AMS) worden gemarkeerd als "niet koppelbaar" en opgenomen in een aparte lijst in het rapport.
- [ ] De gecombineerde dataset is beschikbaar als CSV/Excel-exportbestand.
- [ ] Het totaal aantal gekoppelde versus niet-gekoppelde sessies is zichtbaar in het rapport.

---

## E-02 — Parameteranalyse

### US-04 — Meest relevante externe-load-parameters identificeren

```
Als Froukje
wil ik dat de pipeline de Kinexon-parameters analyseert en de meest relevante voor shorttrack-trainingsbelasting identificeert
zodat ik weet welke parameters het beste de externe load weergeven en hoe die zich verhoudt tot de interne load
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje
**Context / tijdsbudget:** Kern van de analyse; output wordt door Froukje gevalideerd voor gebruik.

**Acceptatiecriteria:**
- [ ] De pipeline levert minimaal 1 en maximaal de top 5 meest relevante Kinexon-parameters op, gerangschikt op statistische relevantie.
- [ ] Elke parameter is voorzien van: de naam in shorttrack-terminologie, de statistische onderbouwing (bijv. correlatiesterkte, effectgrootte), en een begrijpelijke uitleg van wat de parameter meet.
- [ ] Parameters zonder voldoende statistisch bewijs (onder de vastgestelde drempel) worden expliciet gelabeld als "onvoldoende onderbouwd" en niet als aanbeveling gepresenteerd.
- [ ] Als de dataset onvoldoende basis biedt voor enige aanbeveling, geeft de pipeline een transparante melding (zie P-04) in plaats van een lege of onjuiste output.

---

### US-05 — Vergelijken of zware trainingen ook zwaar zijn

```
Als Froukje en Niels
willen wij kunnen zien of trainingen die in het trainingsschema als 'zwaar' zijn gemarkeerd, ook daadwerkelijk zwaar waren volgens zowel de interne als externe loadmeting
zodat wij kunnen beoordelen of de training bereikt wat het moet bereiken
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje (analyse), Niels (besluit)
**Context / tijdsbudget:** Froukje analyseert technisch; Niels ontvangt het actiegerichte overzicht.

**Acceptatiecriteria:**
- [ ] De pipeline produceert een overzicht per trainingstype (bijv. zwaar / medium / licht) met de gemiddelde internal en external load per categorie.
- [ ] Afwijkingen tussen geplande intensiteit en gemeten belasting zijn visueel gemarkeerd (bijv. een training gepland als zwaar maar met lage external load).
- [ ] Het overzicht gebruikt shorttrack-terminologie die herkenbaar is voor Froukje en Niels.
- [ ] Het overzicht is beschikbaar als grafiek (exporteerbaar) én als tabel in het rapport.

---

## E-03 — Outputgeneratie

### US-06 — Technisch rapport voor Froukje ontvangen

```
Als Froukje
wil ik na afloop van de analyse een gestructureerd technisch rapport ontvangen
zodat ik de methodiek kan controleren, de resultaten kan valideren en ze indien nodig kan aanpassen of aanvullen
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Froukje
**Context / tijdsbudget:** Nawerk na een analyse-run; Froukje heeft ruim de tijd.

**Acceptatiecriteria:**
- [ ] Het rapport bevat: de representativiteitscheck-uitkomst, de koppelingsvalidatie (percentage gekoppeld/niet-gekoppeld), de top-parameters met statistieken, de seizoensvergelijking (gepland vs. gemeten), en een sectie "Databeperkingen".
- [ ] De methode-sectie beschrijft welk analyseplatform en welke methode gebruikt zijn, zodat de analyse reproduceerbaar is.
- [ ] Het rapport is beschikbaar als Word (.docx) én PDF.
- [ ] Alle grafieken in het rapport zijn ook los exporteerbaar als afbeeldingsbestanden (PNG of SVG).

---

### US-07 — Actiegericht overzicht voor Niels ontvangen

```
Als Niels
wil ik een beknopt overzicht ontvangen van de belangrijkste bevindingen in begrijpelijk Nederlands, zonder technisch jargon
zodat ik zonder data-expertise besluiten kan nemen over de trainingsopbouw voor het komende seizoen
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Niels
**Context / tijdsbudget:** Niels leest het overzicht op laptop; tijdsbesteding naar verwachting 10–15 minuten.

**Acceptatiecriteria:**
- [ ] Het overzicht bevat maximaal 1 A4 / 2 schermen met: de 2–3 meest relevante bevindingen, een antwoord op "trainen wij wat we in de wedstrijd nodig hebben?", en concrete aanbevelingen voor de trainingsplanning.
- [ ] Elke bevinding bevat een beknopte redenering in begrijpelijk Nederlands (geen statistische termen).
- [ ] Het overzicht is goedgekeurd door Froukje voordat het aan Niels wordt gedeeld.
- [ ] Het overzicht is beschikbaar als PDF of Word-document.

---

## E-04 — Reproduceerbaarheid

### US-08 — Pipeline herhalen voor volgend seizoen

```
Als DSA-team en Froukje
willen wij de analysepipeline het volgende shorttrack-seizoen opnieuw kunnen inzetten
zodat de bevindingen van dit seizoen vergeleken kunnen worden met toekomstige seizoenen en de investering herhaalbaar is
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** DSA-team, Froukje
**Context / tijdsbudget:** Technische documentatie bij oplevering; geen tijdsdruk.

**Acceptatiecriteria:**
- [ ] Een technische handleiding beschrijft alle stappen van de pipeline: data-aanlevering, verwerkingsstappen, analyse-instellingen en outputgeneratie.
- [ ] De configureerbare parameters (bijv. drempel representativiteitscheck, analysemethode) zijn gedocumenteerd en aanpasbaar zonder code te herschrijven.
- [ ] Een nieuw DSA-teamlid kan de analyse reproduceren met behulp van de handleiding zonder ondersteuning van het huidige team.
- [ ] De pipeline is voorzien van een versienummer en wijzigingslog.

---

## Prioriteitenmatrix

| Story | Epic | Prioriteit | MVP? |
|---|---|---|---|
| US-01 | E-01 Data-voorbereiding | Must-have | ✅ |
| US-02 | E-01 Data-voorbereiding | Must-have | ✅ |
| US-03 | E-01 Data-voorbereiding | Must-have | ✅ |
| US-04 | E-02 Parameteranalyse | Must-have | ✅ |
| US-05 | E-02 Parameteranalyse | Must-have | ✅ |
| US-06 | E-03 Outputgeneratie | Must-have | ✅ |
| US-07 | E-03 Outputgeneratie | Must-have | ✅ |
| US-08 | E-04 Reproduceerbaarheid | Must-have | ✅ |
