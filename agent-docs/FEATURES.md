# Features — Trainingsload Shorttrack
**NOC\*NSF / KNSB**
Versie 1.0 — 12 mei 2026

## Leeswijzer
Elk feature-blok is gekoppeld aan één of meer user stories en bevat: wat het systeem doet, hoe het zich gedraagt (inclusief randgevallen), acceptatiecriteria en wat expliciet buiten scope valt.

---

## F-01 — Data-ingest & structurering

**Gelinkt aan:** US-01, US-03
**Prioriteit:** Must-have (MVP)

### Beschrijving
De pipeline neemt bronbestanden in ontvangst — Kinexon-export, RPE-vragenlijsten, hartslagdata en optioneel MyLaps-data — en structureert deze in een gecombineerde analyselaag. De originele bestanden worden niet gewijzigd. De stap produceert een gecombineerde dataset per training per sporter, voorzien van koppelingsvalidatie.

### Gedrag

**Aanlevering:**
- Froukje levert bestanden aan via een vooraf afgesproken methode (handmatige upload of bestandslocatie op gedeelde schijf; zie OB-03).
- De pipeline bevestigt welke bestanden zijn ontvangen, inclusief bestandsnaam, aanleverdatum en verwacht formaat.
- De pipeline controleert op minimaal vereiste kolommen per bronbestand (bijv. sporterId, datum, sessie-ID) en meldt ontbrekende velden vóór verwerking begint.

**Koppeling internal/external load:**
- Per trainingsessie worden Kinexon-data, RPE-score en hartslagdata gekoppeld op basis van sporterId + datum (en optioneel sessie-ID).
- Sessies die over meerdere bronnen niet te matchen zijn, worden gemarkeerd als "niet koppelbaar" en opgenomen in een aparte lijst.
- De gecombineerde dataset wordt als CSV en Excel opgeslagen in de uitvoerlaag.

**Datasouvereiniteit:**
- Alle transformaties vinden plaats op kopieën. De bronbestanden zijn read-only en worden nooit overschreven.

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Bestandsformaat niet herkend | Pipeline stopt; foutmelding met verwacht formaat en instructie voor correctie |
| Ontbrekende verplichte kolom in bronbestand | Pipeline stopt; meldt welke kolom ontbreekt in welk bestand |
| Twee sessies op dezelfde datum voor dezelfde sporter | Pipeline markeert de ambiguïteit; vraagt Froukje om handmatige toewijzing |
| RPE-score ontbreekt voor een sessie | Sessie wordt opgenomen maar RPE-veld is leeg; dit wordt vermeld in "Databeperkingen" |
| Kinexon-data ontbreekt voor een sessie | Sessie wordt opgenomen maar Kinexon-velden zijn leeg; telt mee in dekkingspercentage |

### Acceptatiecriteria
- [ ] De pipeline produceert een gecombineerde dataset die per sessie ten minste bevat: sporterId, datum, trainingstype, RPE (indien beschikbaar), hartslagdata (indien beschikbaar), en Kinexon-parameters (indien beschikbaar).
- [ ] Alle gekoppelde en niet-gekoppelde sessies zijn opgesomd in het rapport, inclusief reden van niet-koppeling.
- [ ] De pipeline verwerkt de testdataset van het seizoen 2025–2026 foutloos door stap F-01 heen.
- [ ] De originele bronbestanden zijn na verwerking ongewijzigd.

### Niet in scope (MVP)
- Automatische API-koppeling met Kinexon of AMS (zie OB-03; handmatige upload is de fallback)
- Verwerking van videobeelden — videoanalyse vereist computer vision (pose estimation, actieherkenning), wat een fundamenteel andere technische investering is dan sensordataverwerking; post-MVP uitbreiding
- Verwerking van MyLaps-rondetijden: afhankelijk van OB-09; als MyLaps in scope valt voor MVP, wordt dit onderdeel van F-01 (MyLaps biedt rondetijden + rondenaantal als externe-loadproxy met waarschijnlijk hogere dekking dan Kinexon)

---

## F-02 — Representativiteitscheck

**Gelinkt aan:** US-02
**Prioriteit:** Must-have (MVP)

### Beschrijving
Vóór elke parameteranalyse berekent de pipeline automatisch in hoeverre de Kinexon-dataset het seizoen dekt. Als de dekking onder een configureerbare drempel valt, stopt de pipeline en geeft een expliciete waarschuwing. Froukje kan bewust kiezen toch door te gaan — deze keuze wordt gelogd.

### Gedrag

**Dekkingsberekening:**
- De pipeline berekent: aantal unieke trainingssessies met Kinexon-meting ÷ totaal aantal trainingssessies in de aangeleverde dataset × 100%.
- **Trainingstype-verdeling (zie OB-10):** Als trainingstypelabels beschikbaar zijn, berekent de pipeline ook de dekking per trainingstype (relay, individueel, techniek, etc.). Een hoog totaal-dekkingspercentage maar uitsluitend relay-sessies is onvoldoende — het bekende risico is dat de Kinexon-database overwegend relay-trainingen dekt, waardoor gevonden parameters relay-belasting meten in plaats van algemene shorttrack-trainingsbelasting.

**Drempellogica:**
- Drempelwaarde is configureerbaar (zie OB-06; standaardvoorstel: 60%).
- Bij dekking ≥ drempel: analyse gaat automatisch door; dekkingspercentage wordt vermeld in het rapport.
- Bij dekking < drempel: pipeline stopt; waarschuwing toont dekkingspercentage, periode(s) zonder meting, en de implicatie voor de betrouwbaarheid. Froukje moet actief bevestigen om door te gaan.

**Logging:**
- Elke run legt vast: timestamp, inputbestanden, dekkingspercentage, en of Froukje een drempelwaarschuwing heeft overschreven.

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Geen Kinexon-data aanwezig | Pipeline stopt direct; meldt dat Kinexon-data vereist is voor de analyse |
| Dekking exact op de drempel | Pipeline gaat door; meldt dit expliciet in het rapport |
| Froukje overschrijft de drempelwaarschuwing | Analyse wordt gestart; rapport bevat een prominente disclaimer over beperkte betrouwbaarheid |
| Trainingsschema ontbreekt (geen referentie voor totaal) | Dekking kan niet berekend worden; pipeline vraagt Froukje om trainingsschema aan te leveren of om handmatig het totaal aantal trainingen in te vullen |

### Acceptatiecriteria
- [ ] De pipeline berekent het dekkingspercentage correct voor de testdataset (geverifieerd door Froukje).
- [ ] Bij dekking onder de drempel verschijnt een waarschuwing vóórdat enige parameteranalyse plaatsvindt.
- [ ] Het dekkingspercentage is altijd zichtbaar in het rapport, ook als de analyse gewoon is doorgegaan.
- [ ] Een door Froukje overschreven drempelwaarschuwing resulteert in een zichtbare disclaimer in het rapport.

### Niet in scope (MVP)
- Automatische aanvulling van ontbrekende Kinexon-data
- Statistische imputation van ontbrekende sessies

---

## F-03 — AI-parameteranalyse

**Gelinkt aan:** US-04, US-05
**Prioriteit:** Must-have (MVP)

### Beschrijving
De kern van de pipeline: een analysemodule die de Kinexon-parameters onderzoekt op hun relatie met interne trainingsbelasting (RPE, hartslagdata) en met de geplande trainingsintensiteit. De module identificeert de meest relevante parameters, rangschikt ze op statistische onderbouwing, en produceert een verklaring per parameter in shorttrack-terminologie. Precisie gaat boven volledigheid (zie P-02).

### Gedrag

**Parameteranalyse:**
- De module berekent per Kinexon-parameter de statistische relatie met: RPE-score (of sRPE indien sessieduur beschikbaar, zie OB-13), hartslagintensiteit, en geplande trainingsintensiteit (zwaar/medium/licht).
- Analysemethode wordt bepaald op basis van OB-02; bij voorkeur een interpretatieve methode (bijv. correlatie, feature importance, of regressie) die uitlegbaar is voor Froukje.
- Parameters worden gerangschikt op statistische relevantie (bijv. correlatiesterkte of feature importance-score).
- **Kinexon-validiteitsvoorbehoud:** Kinexon-parameters (bijv. PlayerLoad, acceleratiecount) zijn primair gevalideerd voor teamsport op gras/parket, niet voor schaatsen op ijs. Shorttrack heeft een ander bewegingsprofiel (glijden, bochttechniek, geen voetcontact). Froukje's domeinvalidatie is daarom essentieel: een parameter met sterke statistische correlatie die sportspecifiek niet logisch is, wordt niet als aanbeveling opgenomen. Dit wordt expliciet benoemd in het rapport.
- **Trainingstype als confoundevariabele (zie OB-14):** Als trainingstypelabels beschikbaar zijn, voert de module de analyse stratified uit per trainingstype. Dit voorkomt schijnverbanden veroorzaakt door het verschil in belastingsprofiel tussen relay en individuele trainingen.

**Drempellogica voor aanbevelingen:**
- Alleen parameters met een statistisch bewijs boven een vooraf vastgestelde drempel worden als "relevant" gepresenteerd.
- Parameters onder de drempel worden vermeld als "onderzocht maar onvoldoende onderbouwd" — ze verdwijnen niet stil uit de output.

**Seizoensvergelijking:**
- De module produceert een overzicht: voor elk trainingstype (gepland als zwaar/medium/licht) de gemiddelde interne en externe load, plus afwijkingen van de verwachting.
- **Optioneel — seizoensfase als dimensie:** Als het trainingsschema seizoensfasen bevat (opbouw, competitie, herstel), kan de vergelijking ook per fase worden uitgesplitst. Dit geeft inzicht in of de belasting op de juiste momenten in het seizoen piekt. Afhankelijk van beschikbaarheid trainingsschema (zie OB-14).

**Uitlegbaarheid:**
- Elke aanbevolen parameter bevat: de parameternaam in shorttrack-terminologie, de statistische maatstaf (bijv. r = 0.72, p < 0.01), en een begrijpelijke uitleg van wat de parameter meet en waarom hij relevant is.

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Geen enkele parameter haalt de drempel | Pipeline geeft transparante melding: "Op basis van de beschikbare data kan geen betrouwbare parameteraanbeveling worden gedaan." Geen lege of foutieve output. |
| Twee parameters zijn statistisch even sterk | Beide worden gerapporteerd; de uitleg benoemt dat de keuze verder domeinkennis vereist |
| Kinexon-parameter is in alle sessies gelijk (geen variatie) | Parameter wordt automatisch uitgesloten van analyse; dit wordt gemeld in "Databeperkingen" |
| Analyse duurt langer dan verwacht | Geen tijdseis voor de pilot (zie Ronde 9); verwerking mag op de achtergrond plaatsvinden |

### Acceptatiecriteria
- [ ] De pipeline levert minimaal 1 en maximaal 5 parameters op, voorzien van statistisch bewijs en uitleg.
- [ ] Parameters zonder voldoende bewijs zijn zichtbaar in de output maar duidelijk gelabeld als "onvoldoende onderbouwd".
- [ ] Als geen enkele parameter de drempel haalt, verschijnt een transparante melding in plaats van lege output.
- [ ] De seizoensvergelijking toont per trainingstype de gemiddelde load en markeert afwijkingen.
- [ ] Froukje kan de analyse-uitkomsten valideren aan de hand van haar domeinkennis (shorttrack-terminologie is correct gebruikt).

### Niet in scope (MVP)
- Voorspellende modellering (bijv. blessurerisico, prestatieprognose) — dit is post-MVP; de canvas noemt dit als mogelijke richting na de analysiefase
- Real-time analyse tijdens of direct na een training
- Vergelijking met andere sporten of andere seizoenen (vereist uitbreiding van de dataset)
- Wedstrijddata als vergelijkingsbenchmark — afhankelijk van OB-11; als wedstrijddata (Kinexon of MyLaps tijdens wedstrijden) beschikbaar is, kan de kernvraag "trainen wij wat we in de wedstrijd nodig hebben?" direct empirisch worden beantwoord in plaats van alleen via trainingsschema-vergelijking

---

## F-04 — Technisch rapport (voor Froukje)

**Gelinkt aan:** US-06
**Prioriteit:** Must-have (MVP)

### Beschrijving
Na een succesvolle analyse-run genereert de pipeline automatisch een gestructureerd technisch rapport voor Froukje. Het rapport dekt alle stappen van de analyse, is reproduceerbaar en bevat een sectie "Databeperkingen" die altijd aanwezig is, ook als er geen beperkingen zijn.

### Gedrag

**Structuur van het rapport:**
1. Samenvatting (max. 1 pagina): dekkingspercentage, aantal geanalyseerde sessies, top-parameters
2. Representativiteitscheck: dekkingspercentage, periodes zonder meting, drempeluitkomst
3. Koppelingsvalidatie: aantal gekoppelde/niet-gekoppelde sessies, reden niet-koppeling
4. Parameteranalyse: gerangschikte parameters met statistieken en uitleg
5. Seizoensvergelijking: trainingstype vs. gemeten load, afwijkingen
6. Methode: gebruikte analyseplatform, methode, versie-informatie
7. Databeperkingen: alle bekende gaten, ontbrekende sessies, beperkingen van de conclusies

**Formaat:**
- Beschikbaar als Word (.docx) én PDF
- Alle grafieken ook los exporteerbaar als PNG of SVG

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Analyse gedeeltelijk mislukt (bijv. één stap gefaald) | Rapport wordt gegenereerd met beschikbare resultaten; mislukte stap is duidelijk gemarkeerd als "niet beschikbaar" met reden |
| Geen aanbevelingen beschikbaar | Rapport bevat expliciet de melding en redenering; overige secties worden normaal gevuld |
| Froukje wil het rapport opnieuw genereren na een correctie | Rapport wordt opnieuw gegenereerd met de gecorrigeerde input; versienummer wordt verhoogd |

### Acceptatiecriteria
- [ ] Het rapport bevat alle zeven secties, ook als sommige secties "geen bevindingen" rapporteren.
- [ ] Het rapport is beschikbaar als zowel .docx als .pdf na elke succesvolle run.
- [ ] Alle grafieken zijn los exporteerbaar.
- [ ] De methodesectie is voldoende gedetailleerd om de analyse te reproduceren (zie US-08).

### Niet in scope (MVP)
- Interactief rapport of dashboard
- Automatische e-mailverzending van het rapport

---

## F-05 — Actiegericht overzicht (voor Niels)

**Gelinkt aan:** US-07
**Prioriteit:** Must-have (MVP)

### Beschrijving
Op basis van het technisch rapport genereert de pipeline een beknopt actiegericht overzicht voor Niels. Dit overzicht bevat de twee à drie meest relevante bevindingen in begrijpelijk Nederlands, zonder statistische termen. Froukje keurt het overzicht goed vóór het gedeeld wordt.

### Gedrag

**Structuur van het overzicht:**
1. Kernvraag en antwoord: "Trainen wij wat we in de wedstrijd nodig hebben?" — ja/nee/gedeeltelijk, met redenering in één alinea
2. Top-bevindingen (2–3 punten): elke bevinding in 2–4 zinnen, zonder statistische termen, met een concrete implicatie voor de training
3. Aanbevelingen voor het komende seizoen: maximaal 3 concrete suggesties

**Goedkeuringsflow:**
- Het overzicht wordt eerst aan Froukje aangeboden voor validatie.
- Froukje kan inhoudelijke correcties doorgeven voordat het aan Niels gaat.

**Formaat:**
- Maximaal 1 A4 / 2 schermen
- Beschikbaar als PDF of Word

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Technisch rapport bevat geen aanbevelingen | Overzicht vermeldt expliciet: "Op basis van de beschikbare data kunnen geen betrouwbare aanbevelingen worden gedaan voor het komende seizoen." Geen lege pagina. |
| Froukje keurt het overzicht niet goed | Overzicht wordt niet vrijgegeven; Froukje geeft correcties door en het overzicht wordt bijgewerkt |

### Acceptatiecriteria
- [ ] Het overzicht bevat geen statistische termen (r-waarde, p-waarde, feature importance etc.).
- [ ] Het bevat altijd een antwoord op de kernvraag "trainen wij wat we nodig hebben?".
- [ ] Het overzicht is door Froukje goedgekeurd vóór het aan Niels wordt gedeeld.
- [ ] Het past op maximaal 1 A4 / 2 schermen.

### Niet in scope (MVP)
- Automatische verzending naar Niels
- Gepersonaliseerde versie per sporter voor Niels

---

## F-06 — Auditlog & reproduceerbaarheidsondersteuning

**Gelinkt aan:** US-08
**Prioriteit:** Must-have (MVP)

### Beschrijving
Elke analyse-run wordt automatisch gelogd. De logs stellen het DSA-team en Froukje in staat om eerdere analyses te reproduceren, de pipeline te debuggen en de kwaliteit over tijd te monitoren.

### Gedrag

**Loginhoud per run:**
- Timestamp van de run
- Versie van de pipeline
- Lijst van inputbestanden (naam + hash of wijzigingsdatum)
- Dekkingspercentage en drempeluitkomst
- Versienummer van het outputrapport
- Of een drempelwaarschuwing is overschreven (ja/nee)

**Technische handleiding:**
- Geleverd als onderdeel van de MVP-oplevering
- Bevat: installatie-instructies, beschrijving van alle configureerbare parameters, stapsgewijze beschrijving van de pipeline, en de verwachte outputstructuur

### Acceptatiecriteria
- [ ] Elke run produceert een logbestand met de hierboven genoemde velden.
- [ ] De technische handleiding is aanwezig bij oplevering en is door een nieuw DSA-teamlid getest op reproduceerbaarheid.
- [ ] De pipeline is voorzien van een versienummer in de outputbestanden en de log.

### Niet in scope (MVP)
- Automatische kwaliteitsalerts op basis van logdata
- Vergelijking van resultaten over meerdere runs of seizoenen

---

## Technische Afhankelijkheden

| Feature | Afhankelijkheid | Risico | Mitigatie |
|---|---|---|---|
| F-01 | Kinexon-exportformaat beschikbaar en stabiel | Hoog | KNSB/Froukje bevestigt exportformaat vóór bouwsprint; DSA maakt conversiescripts per formaat |
| F-01 | AMS-exportformaat beschikbaar | Middel | Alternatief: Froukje levert CSV handmatig aan; API-koppeling is post-MVP |
| F-02 | Trainingsschema van KNSB beschikbaar als referentie | Middel | Fallback: Froukje vult handmatig totaal aantal trainingen in |
| F-03 | Keuze analyseplatform (OB-02) | Middel | Analysemethode (correlatie/regressie) kan met standaard Python/R-libraries zonder cloudplatform |
| F-03 | Voldoende gekoppelde sessies voor statistische analyse | Hoog | Representativiteitscheck (F-02) blokkeert analyse als dataset te klein is |
| F-04 | Rapportgenerator compatibel met Word/PDF | Laag | Python-libraries (python-docx, reportlab) zijn beschikbaar en bewezen |
| F-05 | Froukje beschikbaar voor goedkeuringsronde | Middel | Goedkeuringsproces wordt ingepland als onderdeel van de analyse-sprint |
| Alle | AVG/GDPR-verificatie (OB-05) | Hoog | DPO-check is harde release-voorwaarde; zie MVP Releasecriteria |
| Alle | Hostingplatform besloten (OB-01) | Middel | Analyse kan lokaal draaien als interim-oplossing; cloud-migratie later |

---

## MVP Releasecriteria

De pilot mag niet starten totdat aan het volgende is voldaan:

- [ ] AVG/GDPR-verificatie: DPO heeft bevestigd dat bestaande KNSB-toestemming het gebruik van Kinexon-data voor AI-analyse dekt (OB-05)
- [ ] Dataretentiebeleid vastgesteld: DPO heeft bepaald hoe lang sportersdata bewaard mag worden (OB-04)
- [ ] Drempelwaarde representativiteitscheck bepaald: Froukje en DSA-team zijn het eens over het minimale dekkingspercentage (OB-06)
- [ ] Analysemethode gekozen en gedocumenteerd: DSA-team heeft de AI/analyse-aanpak vastgesteld (OB-02)
- [ ] Kinexon-exportformaat bevestigd: KNSB heeft het beschikbare exportformaat geleverd aan DSA
- [ ] Data-ingest getest: F-01 is succesvol getest met een subset van de echte seizoensdata
- [ ] Koppelingsvalidatie geslaagd: F-01 koppelt internal en external load correct voor minimaal 80% van de testdataset
- [ ] End-to-end test geslaagd: de pipeline is van input tot output doorgelopen met echte data en het resultaat is door Froukje inhoudelijk gevalideerd
- [ ] Technische handleiding aanwezig en getest op reproduceerbaarheid
