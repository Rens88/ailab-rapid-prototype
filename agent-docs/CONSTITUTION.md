# Constitutie — AI Sparringpartner voor Talentcoaches

**Hanzehogeschool Groningen — Lectoraat Sportinnovator / AI Impact Lab**
Versie 1.0 — mei 2026

---

## Wat is dit document?

Dit document legt de niet-onderhandelbare principes vast waaraan alle features, technische keuzes en ontwerp­beslissingen van de AI Sparringpartner moeten voldoen. Het is bedoeld voor zowel stakeholders (wat mag dit product wel en niet doen?) als het development team (wat zijn de harde grenzen bij elke implementatiekeuze?).

Als een feature of technische keuze in conflict is met een principe in dit document, wint dit document. Uitzonderingen vereisen expliciete besluitvorming door de projecteigenaar.

---

## Principes

### P-01 — De coach is altijd de beslisser

De AI Sparringpartner ondersteunt het denkproces van de coach — hij vervangt het niet. Het systeem stelt vragen, deelt overwegingen en biedt perspectieven. Het stelt geen diagnoses, geeft geen behandeladviezen en doet geen uitspraken die als definitief oordeel gelezen kunnen worden.

In elke interactie blijft de menselijke coach de verantwoordelijke partij voor beslissingen over training, planning en begeleiding van sporters.

**Afdwingbaar door:**
Elke systeemprompt bevat een expliciete instructie dat de AI geen diagnoses stelt en geen beslissingen neemt namens de coach. Outputs die een harde conclusie trekken zonder nuance of doorverwijzing zijn een productdefect. Acceptatietests bevatten scenario's waarin de juiste respons "ik weet het niet" of "raadpleeg een sportwetenschapper" is.

---

### P-02 — Transparantie over mogelijkheden én beperkingen

Het systeem is open over wat het wel en niet kan. Als een vraag buiten het kennisdomein valt, buiten de MVP-scope ligt, of als het bewijs dun is, zegt het systeem dat expliciet. Een antwoord dat de schijn wekt van zekerheid terwijl die er niet is, is gevaarlijker dan geen antwoord.

De introductietekst van de chatbot maakt duidelijk: dit is een sparringpartner, geen orakel. Coaches bepalen zelf wat ze met de uitkomst doen.

**Afdwingbaar door:**
De systeemprompt bevat expliciete instructie om onzekerheid te benoemen en te verwijzen naar specialisten (sportarts, sportwetenschapper, fysiotherapeut) waar passend. Prompttests valideren dat de AI niet "doordendramt" als de vraag zijn kennisgrens bereikt.

---

### P-03 — Privacy by design: minimale verwerking van persoonsgegevens

Coaches typen namen, observaties en soms gezondheidsgerelateerde informatie over sporters in. Dit zijn persoonsgegevens — deels bijzondere persoonsgegevens in de zin van de AVG. Het systeem is zo ingericht dat de hoeveelheid verwerkte persoonsgegevens minimaal is.

Concrete maatregelen:
- Hosting op een platform dat input **niet** gebruikt voor modeltraining
- Minimale gespreksretentie — sessies worden niet langer bewaard dan technisch noodzakelijk
- Coaches worden bij onboarding geadviseerd om **geen identificeerbare persoonsgegevens** (namen, BSN, diagnoses) in te typen; zij omschrijven situaties in anonieme of geanonimiseerde termen
- Sporters worden via de coach of de betrokken organisatie geïnformeerd over het gebruik van de tool

**Afdwingbaar door:**
Platformkeuze (zie OB-01) wordt getoetst op dit principe vóór ingebruikname. Onboardingmateriaal bevat expliciete instructie over anonimiseren. Privacytoets door DPO of juridisch adviseur is een MVP-releasecriterium.

---

### P-04 — Geen verzonnen feiten: conservatief met kennisclaims

Hallucinatie — het zelfverzekerd presenteren van onjuiste informatie — is het grootste kwaliteitsrisico van dit product. De AI baseert zich uitsluitend op de gecureerde kennislaag. Wanneer iets buiten die laag valt, geeft het systeem dat aan.

Waar het wetenschappelijk bewijs dun is (zie P-05), is de AI expliciet terughoudend in zijn uitspraken.

**Afdwingbaar door:**
Kennislaag is afgegrensd en gedocumenteerd (zie OB-03). Prompttests bevatten vragen waarop het juiste antwoord "dat weet ik niet zeker" is. Diepte-interviews met pilotcoaches signaleren vroegtijdig of coaches onjuiste informatie als waar aannemen.

---

### P-05 — Bias-bewustzijn: voorzichtigheid bij vrouwen en jongeren

Sportwetenschap is historisch sterk gericht op mannelijke volwassen topsporters. Voor talentontwikkeling — dat jongeren betreft, en in toenemende mate vrouwen — is het wetenschappelijk bewijs dunner en soms niet overdraagbaar. Het systeem markeert expliciet wanneer uitspraken gebaseerd zijn op bewijs dat mogelijk niet van toepassing is op de doelgroep van de coach.

**Afdwingbaar door:**
Kennislaagselectie omvat een expliciete annotatie per bron voor doelgroep (leeftijd, geslacht). Systeemprompt instrueert de AI om bij uitspraken over vrouwelijke sporters of jongeren (<18 jaar) voorzichtigheid te benoemen. Dit wordt gevalideerd in prompttests.

---

### P-06 — Niveau 2 valt buiten de MVP-scope

De AI Sparringpartner staat *naast* bestaande monitoringplatformen (Smartabase, SportDataValley) — niet erin. De MVP bevat geen directe data-integratie met externe platforms, geen automatische inlees van trainingsdata, en geen statistische analyse van sportersprestaties.

Coaches brengen zelf context in via de chat. Niveau 2 (data-integratie en patroonherkenning op sportersdata) is een bewuste volgende fase — relevant voor het CoachWell-Europese vervolg — maar maakt geen deel uit van deze spec.

**Afdwingbaar door:**
Elke feature die directe databasekoppeling vereist met externe monitoringsystemen is out of scope. Als dit in de backlog verschijnt, wordt het gelabeld als Niveau 2 en niet gebouwd zonder afzonderlijk besluit.

---

### P-07 — Platformonafhankelijkheid

De tool werkt onafhankelijk van het monitoringplatform dat een coach gebruikt. Of een coach met Smartabase, SportDataValley, Excel of een eigen vragenlijst werkt: de chatbot stelt geen eisen aan de onderliggende datawerkwijze van de coach.

**Afdwingbaar door:**
Geen enkele feature veronderstelt een specifiek monitoringsysteem. Onboardingmateriaal en systeemprompt zijn platform-neutraal geformuleerd.

---

### P-08 — Bruikbaar op zowel smartphone als laptop, met spraakondersteuning

Primaire gebruikers werken zowel onderweg (op sportlocatie) als thuis of op kantoor — met verschillende behoeften per apparaat:

- **Smartphone:** snelle vragen stellen tussen trainingen door, korte antwoorden, spraakbediening zodat typen niet nodig is
- **Laptop:** inhoudelijker gesprekken voeren, links naar literatuur lezen, langere antwoorden verwerken

Beide modaliteiten zijn volwaardig ondersteund. Daarnaast ondersteunt de tool **spraak als invoer** (coach spreekt zijn vraag in plaats van typt) en **voorlezen van antwoorden** (text-to-speech), zodat de tool ook bruikbaar is op locatie zonder dat de coach naar een scherm hoeft te kijken.

**Afdwingbaar door:**
UX-acceptatietest omvat validatie op mobiel schermformaat. Tekstvelden, knoppen en navigatie zijn toetsenbord- én touchscreen-compatibel. Spraakherkenning en TTS worden getest op gangbare smartphones (iOS en Android). Visuele QA omvat screenshots op 375px breedte (smartphone) én 1280px (laptop).

---

## Technische Beslissingen (vastgesteld)

| Beslissing | Keuze | Reden |
|---|---|---|
| MVP-scope | Niveau 1: conversatie + kennislaag | Niveau 2 (data-integratie) is bewust buiten scope — haalbaarheid binnen 12-weken lab-cyclus |
| AI-type | Generatieve AI (LLM) met domein-gerichte kennislaag | Geen voorspellend of statistisch model — gesprekskwaliteit staat centraal |
| Reactietijd | < 10 seconden voor standaard antwoorden | Acceptabel voor doordachte antwoorden op zowel mobiel als desktop |
| Consent sporters | Via coach en betrokken organisatie | Coaches worden geadviseerd geen identificeerbare persoonsgegevens in te voeren |
| Kwaliteitsmonitoring | Diepte-interviews met pilotcoaches na 8–12 weken + gesprekslogs | Kwalitatieve evaluatie is primaire succesmeting |
| Pilotomvang | 5–10 talentcoaches via bestaand netwerk | RTC's, bonden, opleidingsteams — netwerk is beschikbaar |
| Tijdlijn | 12-weken lab-cyclus | Week 1–3 kennislaag, Week 4–6 prototype, Week 7–10 pilot, Week 11–12 evaluatie |

---

## Open Besluiten (nog te nemen)

| # | Besluit | Eigenaar | Deadline |
|---|---|---|---|
| OB-01 | Keuze LLM-platform en hostinglocatie. Afwegingscriteria: (1) AVG-conform hosting zonder training op input; (2) dataveiligheid bij doorontwikkeling naar Niveau 2 — Mistral (EU, open source) is door adviseurs genoemd als veilige optie voor gevoelige sportersdata; (3) compatibiliteit met AI-partners zoals Researchable; (4) Microsoft Copilot is beschikbaar via Fontys/Hanze én KNSB, maar de Niveau 2-roadmap vraagt mogelijk een ander platform. Besluit vereist afstemming met DPO én een blik op de Niveau 2-strategie. | Projecteigenaar + DPO | Vóór start Week 1 |
| OB-02 | Authenticatiemethode (Microsoft SSO via Fontys/Hanze vs. standalone login vs. andere SSO) | Projecteigenaar + IT | Vóór start Week 1 |
| OB-03 | Samenstelling en onderhoud kennislaag. Vereiste domeinen (gebaseerd op WP2-veldonderzoek): (1) monitoring-methodologie incl. Saw et al. 2017, SRPE, TQR, wellness-schalen; (2) compliance en sporter-commitment incl. onboarding-aanpak, sporter-archetypes en peer accountability; (3) feedbackstrategieën coach-sporter incl. frequentie, rode-vlaggen-redenering en het voorkomen van de "politieagent"-rol; (4) periodisering en belasting-belastbaarheid; (5) coachpedagogie, autonomie en mentor mindset. Ankerpunten: eigen onderzoekstraditie Sportmonitor op Maat / Coach in Control, interviews coaches/experts 2024–2026 (WP2-aantekeningen), relevante wetenschappelijke literatuur. Te besluiten: welke bronnen wegen mee, annotatie per bron op doelgroep (leeftijd/geslacht), wie onderhoudt de laag na de pilot. | Lectoraat + domeinexperts | Vóór start Week 4 |
| OB-04 | Privacytoets door DPO of juridisch adviseur: AVG-conformiteit bevestigd | DPO / juridisch adviseur | Vóór start pilot (Week 7) |
| OB-05 | Evaluatiestrategie pilot: groepsgrootte, selectiebias, evt. sporter-feedback | Lectoraat + onderzoeksbegeleiders | Vóór start Week 7 |
| OB-06 | Gesprekslogbeleid: retentietermijn, wie heeft toegang, hoe worden logs gebruikt voor kwaliteitsverbetering | Projecteigenaar + DPO | Vóór start pilot (Week 7) |
