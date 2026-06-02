# User Stories — AI Sparringpartner voor Talentcoaches

**Hanzehogeschool Groningen — Lectoraat Sportinnovator / AI Impact Lab**
Versie 1.0 — mei 2026

---

## Actoren

| Actor | Omschrijving |
|---|---|
| **Talentcoach** | Coacht 10–20 sporters in een RTC, talentteam of opleidingsploeg richting (sub)topniveau. Heeft domeinkennis en motivatie, maar geen data-analist of sportwetenschapper beschikbaar. Gebruikt de tool ad-hoc op smartphone én laptop. Laag tot middel technisch niveau. |
| **Sporter** | Vult dagelijks monitoring in (welzijn, RPE, slaap). Ontvangt via de coach terugkoppeling op basis van de tool. Heeft geen directe toegang tot de chatbot in de MVP. |
| **Projectteam / lectoraat** | Beheert de kennislaag, evalueert gesprekslogs, voert diepte-interviews uit. Heeft geen actieve rol in de chatbot zelf, maar is eigenaar van kwaliteit en doorontwikkeling. |

---

## Epicoverzicht

| Epic | Omschrijving | Stories |
|---|---|---|
| E-01 | Sparringpartner-gesprek | US-01, US-02, US-03 |
| E-02 | Kennislaag & antwoordkwaliteit | US-04, US-05 |
| E-03 | Privacy & verantwoord gebruik | US-06, US-07 |
| E-04 | Onboarding & adoptie | US-08, US-09 |
| E-05 | Spraak & multimodaliteit | US-10, US-11 |

---

## E-01 — Sparringpartner-gesprek

### US-01 — Een vrije vraag stellen in gewone taal

```
Als talentcoach
wil ik in gewone taal een vraag kunnen stellen over een situatie met een sporter
zodat ik een doordacht perspectief krijg dat mij helpt verder te denken
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Ad-hoc gebruik, voor/na training of bij voorbereiding van een 1-op-1 gesprek. Sessie duurt typisch 3–10 minuten.

**Acceptatiecriteria:**
- [ ] Coach kan een vraag invoeren als vrije tekst zonder structuur of formatvereiste
- [ ] Systeem geeft een antwoord binnen 10 seconden
- [ ] Antwoord is geformuleerd als perspectief, overweging of vervolgvraag — niet als definitieve conclusie
- [ ] Antwoord bevat minimaal één concrete vervolgstap of vervolgvraag voor de coach
- [ ] Systeem stelt geen diagnose en schrijft geen behandeling voor

---

### US-02 — Context opbouwen binnen een sessie

```
Als talentcoach
wil ik tijdens een gesprek context kunnen toevoegen (sport, ploeg, situatie)
zodat het systeem steeds relevantere en meer toegespitste antwoorden geeft naarmate het gesprek vordert
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Geldt voor de volledige sessieduur; context is vluchtig en verdwijnt na afsluiting van de sessie.

**Acceptatiecriteria:**
- [ ] Systeem gebruikt eerder gedeelde context (bijv. sport, leeftijdscategorie, beschreven situatie) in latere antwoorden binnen dezelfde sessie
- [ ] Coach hoeft context niet te herhalen zolang de sessie actief is
- [ ] Na afsluiting van de sessie wordt geen context bewaard (geen persistente geheugen in MVP)
- [ ] Systeem maakt duidelijk wanneer het terugverwijst naar eerder gedeelde informatie

---

### US-03 — Een gesprek afsluiten met een concrete actie of vraag

```
Als talentcoach
wil ik aan het einde van een gesprek weten wat mijn volgende stap is
zodat ik het gesprek met de tool omzet in iets wat ik daadwerkelijk doe in mijn coachpraktijk
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Laatste fase van een sessie; output moet bruikbaar zijn als notitie voor een 1-op-1 of trainingsmoment.

**Acceptatiecriteria:**
- [ ] Systeem biedt aan het einde van een gesprek (of op verzoek) een samenvatting van besproken punten en concrete vervolgacties of -vragen
- [ ] Samenvatting is in maximaal 5 punten en past op één scherm op een smartphone
- [ ] "Nog niet weten" of "pas op de plaats" is een expliciete en geldige uitkomst — systeem dringt geen kunstmatige conclusie op
- [ ] Coach kan de samenvatting kopiëren (tekst selecteerbaar)

---

## E-02 — Kennislaag & antwoordkwaliteit

### US-04 — Antwoord gebaseerd op relevante vakkennis

```
Als talentcoach
wil ik dat antwoorden zijn gebaseerd op sportwetenschap en monitoringmethodologie
zodat ik erop kan vertrouwen dat wat ik lees inhoudelijk verantwoord is
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Geldt voor elke interactie.

**Acceptatiecriteria:**
- [ ] Antwoorden zijn aantoonbaar gebaseerd op de gecureerde kennislaag (trainingsbelasting, welzijn, RPE, talentontwikkeling, vragenlijstmethodologie)
- [ ] Systeem geeft bij een antwoord de bron of het type redenering aan (bijv. "op basis van onderzoek naar trainingsbelasting bij jongeren")
- [ ] Systeem zegt expliciet wanneer het bewijs dun is of niet direct van toepassing op de doelgroep (vrouwen, jongeren)
- [ ] Systeem verzint geen feiten: als het antwoord buiten de kennislaag valt, geeft het dat aan

---

### US-05 — Doorverwijzing naar een specialist

```
Als talentcoach
wil ik dat het systeem mij doorverwijst als een vraag buiten zijn competentie valt
zodat ik weet wanneer ik een sportarts, fysiotherapeut of sportwetenschapper moet raadplegen
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach

**Acceptatiecriteria:**
- [ ] Bij vragen over blessures, medische symptomen of behandeling verwijst het systeem expliciet door naar een sportarts of fysiotherapeut
- [ ] Bij vragen die Niveau 2-data vereisen (bijv. "analyseer mijn Smartabase-data") legt het systeem uit dat dit buiten de MVP-scope valt
- [ ] Doorverwijzing is altijd vriendelijk en niet-beschuldigend geformuleerd
- [ ] Systeem stopt niet simpelweg — het geeft altijd een reden en een alternatief pad

---

## E-03 — Privacy & verantwoord gebruik

### US-06 — Geïnformeerd gebruik zonder persoonsgegevens

```
Als talentcoach
wil ik weten hoe ik de tool verantwoord gebruik met betrekking tot privacy van mijn sporters
zodat ik geen regels overtreedt en mijn sporters bescherm
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach

**Acceptatiecriteria:**
- [ ] Bij onboarding wordt expliciet uitgelegd dat coaches geen identificeerbare persoonsgegevens (namen, diagnoses, BSN) moeten invoeren
- [ ] Systeem toont bij eerste gebruik een beknopte privacytoelichting: welk model wordt gebruikt, waar data heen gaat, wat de retentietermijn is
- [ ] Systeemprompt instrueert de AI om coaches te attenderen op anonimisering als ze (vermoedelijk) persoonsgegevens invoeren
- [ ] Privacytoelichting is in begrijpelijke taal — geen juridisch jargon

---

### US-07 — Gesprekslogs voor kwaliteitsverbetering

```
Als projectteam
willen we gesprekslogs kunnen analyseren op gebruikspatronen en inhoudskwaliteit
zodat we de kennislaag en systeemprompt gericht kunnen verbeteren na de pilot
```

**Prioriteit:** Should-have (MVP indien OB-06 is besloten)
**Primaire actor:** Projectteam / lectoraat
**Afhankelijkheid:** OB-06 (logbeleid vastgesteld vóór pilot)

**Acceptatiecriteria:**
- [ ] Gesprekslogs worden opgeslagen met minimale metadata (tijdstip, sessieduur, gespreksonderwerpen — geen identificerende data)
- [ ] Coaches zijn bij onboarding geïnformeerd over het feit dat sessies worden gelogd voor kwaliteitsverbetering
- [ ] Toegang tot logs is beperkt tot geautoriseerde projectteamleden
- [ ] Logs worden niet langer bewaard dan de evaluatieperiode, conform OB-06

---

## E-04 — Onboarding & adoptie

### US-08 — Eerste gebruik zonder handleiding

```
Als talentcoach
wil ik de tool kunnen gebruiken zonder uitgebreide instructies
zodat de drempel om ermee te starten zo laag mogelijk is
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach

**Acceptatiecriteria:**
- [ ] Interface bevat een korte introductietekst (max. 3 zinnen) die uitlegt wat de tool doet en wat het niet doet
- [ ] Interface bevat 2–4 voorbeeldvragen waarmee een coach direct kan starten
- [ ] Coach kan binnen 60 seconden na inloggen een eerste vraag stellen
- [ ] Er is geen uitgebreide registratie of configuratie vereist vóór eerste gebruik

---

### US-09 — Demo-sessie als startpunt voor pilotcoaches

```
Als pilotcoach
wil ik een korte introductiesessie van ~30 minuten krijgen
zodat ik begrijp hoe ik de tool het beste kan inzetten in mijn coachpraktijk
```

**Prioriteit:** Should-have (MVP)
**Primaire actor:** Talentcoach (pilotgroep)

**Acceptatiecriteria:**
- [ ] Er is een demo-sessieformat beschikbaar (agenda, voorbeeldvragen, uitleg MVP-scope)
- [ ] Pilotcoaches weten na de sessie wat de tool wel en niet kan
- [ ] Pilotcoaches hebben na de sessie inloggegevens en kunnen zelfstandig verder
- [ ] Contactpersoon voor vragen tijdens de pilot is bekend bij elke pilotcoach

---

## E-05 — Spraak & multimodaliteit

### US-10 — Vraag stellen via spraak

```
Als talentcoach op een sportlocatie
wil ik een vraag kunnen inspreken in plaats van typen
zodat ik de tool kan gebruiken terwijl ik onderweg ben of mijn handen niet vrij zijn
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Gebruik op smartphone, op locatie, typisch < 2 minuten.

**Acceptatiecriteria:**
- [ ] Interface biedt een microfoonknop waarmee de coach een vraag kan inspreken
- [ ] Gesproken invoer wordt correct omgezet naar tekst (spraakherkenning in het Nederlands)
- [ ] Coach kan de herkende tekst controleren en corrigeren vóór verzending
- [ ] Functionaliteit werkt op gangbare iOS- en Android-smartphones
- [ ] Bij ontbrekende microfoontoegang toont de interface een heldere foutmelding

---

### US-11 — Antwoord laten voorlezen

```
Als talentcoach op locatie
wil ik dat het antwoord van de tool hardop wordt voorgelezen
zodat ik het kan beluisteren zonder naar mijn scherm te kijken
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Talentcoach
**Context / tijdsbudget:** Gebruik op smartphone, bijv. tijdens rijden naar locatie of tussen trainingsonderdelen.

**Acceptatiecriteria:**
- [ ] Elk antwoord heeft een "Voorlezen"-knop die text-to-speech activeert
- [ ] Voorgelezen tekst is in het Nederlands met een begrijpelijke spreeksnelheid
- [ ] Coach kan het voorlezen pauzeren of stoppen
- [ ] Functionaliteit werkt op gangbare iOS- en Android-smartphones zonder extra app-installatie

---

### US-12 — Gesprekgeschiedenis bewaren (post-MVP)

```
Als talentcoach
wil ik eerdere gesprekken met de tool kunnen terugvinden
zodat ik kan voortbouwen op eerdere inzichten en actiepunten
```

**Prioriteit:** Nice-to-have — **post-MVP**
**Primaire actor:** Talentcoach
**Toelichting:** Persistente gespreksgeschiedenis is inhoudelijk zeer wenselijk — coaches bouwen over meerdere sessies context op over individuele sporters. Het is echter bewust buiten de MVP gehouden vanwege hogere infrastructuurkosten (opslag, toegangscontrole per coach) en aanvullende AVG-overwegingen (langere retentie van mogelijk persoonsgegevens). Dit wordt beschouwd als een prioriteit voor fase 2, direct na een positief geëvalueerde pilot.

**Acceptatiecriteria (fase 2):**
- [ ] Coach kan vorige sessies terugvinden gesorteerd op datum
- [ ] Opgeslagen sessies zijn uitsluitend zichtbaar voor de coach die ze heeft gevoerd
- [ ] Coach kan een sessie verwijderen
- [ ] Retentiebeleid en toegangscontrole zijn AVG-conform vastgesteld

---

## Prioriteitenmatrix

| Story | Epic | Prioriteit | MVP? |
|---|---|---|---|
| US-01 — Vrije vraag stellen | E-01 | Must-have | ✅ |
| US-02 — Context opbouwen in sessie | E-01 | Must-have | ✅ |
| US-03 — Afsluiten met concrete actie | E-01 | Must-have | ✅ |
| US-04 — Antwoord op basis van vakkennis | E-02 | Must-have | ✅ |
| US-05 — Doorverwijzing naar specialist | E-02 | Must-have | ✅ |
| US-06 — Privacyinstructie bij onboarding | E-03 | Must-have | ✅ |
| US-07 — Gesprekslogs voor kwaliteitsverbetering | E-03 | Should-have | ⚠️ (afhankelijk van OB-06) |
| US-08 — Eerste gebruik zonder handleiding | E-04 | Must-have | ✅ |
| US-09 — Demo-sessie pilotcoaches | E-04 | Should-have | ✅ |
| US-10 — Vraag stellen via spraak | E-05 | Must-have | ✅ |
| US-11 — Antwoord laten voorlezen | E-05 | Must-have | ✅ |
| US-12 — Gesprekgeschiedenis bewaren | E-05 | Nice-to-have | ❌ (fase 2) |
