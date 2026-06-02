# Features — Team DNA
**Koninklijke Nederlandse Voetbalbond (KNVB)**
Versie 1.0 — mei 2026

---

## Leeswijzer

Elk feature-blok is gekoppeld aan één of meer user stories en beschrijft wat het systeem doet, hoe het zich gedraagt (inclusief randgevallen), toetsbare acceptatiecriteria en wat expliciet buiten scope valt voor V1. De volgorde weerspiegelt de volgorde in de analysepipeline.

---

## F-01 — Tegenstander selectie en pipeline-start

**Gelinkt aan:** US-01
**Prioriteit:** Must-have (MVP)

### Beschrijving

De gebruiker start de analysepipeline door een tegenstander te selecteren. Het systeem haalt vervolgens automatisch de benodigde data op uit het datawarehouse en start de verwerkingsketen. De gebruiker hoeft na de selectie geen handmatige stappen meer te nemen totdat het rapport beschikbaar is.

### Gedrag

**Normale flow:**
- Gebruiker selecteert een team uit een lijst van beschikbare tegenstanders
- Het systeem controleert de beschikbaarheid van eventdata voor dit team in het datawarehouse
- Het systeem start automatisch de preprocessing- en anonimiseringsstap (zie F-03)
- De gebruiker ontvangt een bevestiging dat de analyse wordt gegenereerd, met een indicatie van de verwachte duur
- Na voltooiing is het rapport beschikbaar voor weergave en export

**Voortgangsindicatie:**
- Het systeem toont in ieder geval de statussen: *Bezig met ophalen van data*, *Bezig met verwerken*, *Rapport wordt gegenereerd*, *Rapport gereed*

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Geen eventdata beschikbaar voor het geselecteerde team | Systeem meldt dit vóór het starten: "Geen data beschikbaar voor [teamnaam]. Analyse kan niet worden gegenereerd." Pipeline start niet. |
| Minder wedstrijden beschikbaar dan de ingestelde N | Systeem start de analyse op basis van beschikbare wedstrijden en verlaagt de datadekkingindicatoren dienovereenkomstig. Melding in het rapport: "Analyse gebaseerd op X wedstrijden (minder dan standaard)." |
| Pipeline mislukt halverwege (technische fout) | Systeem meldt de fout aan de gebruiker met de suggestie om opnieuw te proberen. Geen gedeeltelijk rapport wordt getoond. |
| Gebruiker start dezelfde analyse opnieuw terwijl een analyse loopt | Systeem blokkeert de tweede aanvraag en informeert dat een analyse al in uitvoering is |

### Acceptatiecriteria
- [ ] Gebruiker kan een team selecteren en de pipeline starten in maximaal 3 handelingen
- [ ] Bij onvoldoende data wordt de pipeline niet gestart en de gebruiker geïnformeerd vóór aanvang
- [ ] Bij een technische fout krijgt de gebruiker een begrijpelijke foutmelding; het systeem toont nooit een gedeeltelijk rapport
- [ ] Het systeem toont voortgangsfeedback gedurende de volledige generatieduur

### Niet in scope (V1)
- Handmatige selectie of aanpassing van individuele wedstrijden door de gebruiker
- Parallelle analyses voor meerdere tegenstanders tegelijk
- Opslaan of beheren van eerder gegenereerde analyses in een historisch overzicht

---

## F-02 — Automatische wedstrijdselectie

**Gelinkt aan:** US-02
**Prioriteit:** Must-have (MVP)

### Beschrijving

Het systeem selecteert automatisch de N meest recente wedstrijden van de geselecteerde tegenstander op basis van datum. De selectie omvat beschikbare wedstrijden uit zowel internationale als clubcompetities, afhankelijk van wat aanwezig is in het datawarehouse.

### Gedrag

**Selectielogica:**
- Het systeem haalt alle beschikbare wedstrijden op voor het geselecteerde team, gesorteerd op datum (meest recent eerst)
- De standaardwaarde van N is nog een open besluit (OB-04); de feature is ontworpen zodat N configureerbaar is door een beheerder
- De geselecteerde wedstrijden worden opgeslagen als de bronset die door de hele analysepipeline wordt gebruikt

**Weergave in rapport:**
- Het rapport bevat een overzichtslijst van de geselecteerde wedstrijden: datum, opponent en competitie/toernooi
- Deze lijst fungeert als context voor de gebruiker en als validatiepunt ("zijn dit de wedstrijden die ik verwacht?")

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Minder wedstrijden beschikbaar dan N | Analyse gebruikt alle beschikbare wedstrijden; rapport vermeldt "gebaseerd op X wedstrijden" en datadekking wordt dienovereenkomstig aangepast |
| Alleen internationale wedstrijden beschikbaar (geen clubdata) | Analyse wordt gegenereerd op internationale wedstrijden; rapport vermeldt dat clubdata ontbreekt |
| Data van een wedstrijd is incompleet (ontbrekende eventtypes) | De wedstrijd wordt wel meegenomen in de selectie; de impact op datakwaliteit wordt gereflecteerd in de datadekkingindicator van de betrokken secties |

### Acceptatiecriteria
- [ ] Het systeem selecteert automatisch de N meest recente wedstrijden zonder tussenkomst van de gebruiker
- [ ] De geselecteerde wedstrijden zijn zichtbaar in het rapport met datum, opponent en competitie
- [ ] N is configureerbaar door een beheerder (niet door eindgebruikers in V1)
- [ ] Bij minder dan N beschikbare wedstrijden genereert het systeem een analyse en past de datadekkingindicatoren aan

### Niet in scope (V1)
- Handmatige aanpassing van de wedstrijdselectie door de gebruiker
- Filtering op competitietype (bijv. alleen kwalificatiewedstrijden)

---

## F-03 — Preprocessing: anonimisering en tabel→tekst conversie

**Gelinkt aan:** US-01, US-02, constitutie P-04
**Prioriteit:** Must-have (MVP)

### Beschrijving

Vóórdat event data aan de LLM wordt aangeleverd, doorloopt de data twee verplichte verwerkingsstappen: (1) anonimisering van namen en (2) conversie van tabeldata naar tekstuele beschrijving. Dit zijn infrastructurele functies die de gebruiker niet direct ziet, maar die essentieel zijn voor de betrouwbaarheid en compliance van de output.

### Gedrag

**Stap 1 — Anonimisering:**
- Alle spelernamen worden vervangen door labels: `SPELER_01`, `SPELER_02`, etc.
- De teamnaam van de tegenstander wordt vervangen door `TEAM_A`
- Landnamen worden vervangen door `LAND_X`
- De mapping (echte naam → label) wordt opgeslagen in een sessiesleutel die uitsluitend intern beschikbaar is
- Na rapportgeneratie worden de labels in de eindtekst teruggezet naar echte namen via de sessiesleutel

**Stap 2 — Tabel→tekst conversie:**
- De event- en aggregaatdata uit het datawarehouse worden omgezet naar een gestructureerde tekstuele beschrijving die de LLM als input ontvangt
- De exacte methode (per-rij statements, geaggregeerde beschrijvingen of een combinatie) is een open besluit (OB-03) dat in de eerste prototypefase wordt bepaald
- De gegenereerde tekst bevat uitsluitend feiten, statistieken en patronen die herleidbaar zijn naar de brondata — geen interpretaties

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Twee spelers hebben hetzelfde label na initialisatie (edge case bij grote selecties) | Labelnummering wordt uniek gehouden via incrementele toewijzing; mapping-tabel borgt uniciteit |
| Conversie mislukt voor een datakolom (ontbrekend veld) | Conversie slaat het ontbrekende veld over en logt dit intern; het rapport vermeldt via de datadekkingindicator dat niet alle data beschikbaar was |
| Sessiesleutel gaat verloren vóór terugmapping | Rapport kan niet worden afgerond met echte namen; systeem geeft foutmelding en vraagt de analyse opnieuw te starten |

### Acceptatiecriteria
- [ ] Alle namen van spelers, teams en landen zijn vervangen door anonieme labels vóórdat data de LLM bereikt
- [ ] De mapping is volledig en reproduceerbaar: elk label in de LLM-output kan worden teruggezet naar de juiste echte naam
- [ ] De eindrapportage toont uitsluitend echte namen (geen labels)
- [ ] De tabel→tekst conversie levert alleen feitelijke, herleidbare statements op — geen geïnterpreteerde conclusies
- [ ] De preprocessing-stap kan niet worden omzeild; de pipeline weigert te starten zonder deze stap

### Niet in scope (V1)
- Configureerbare anonimiseringsregels door de gebruiker
- Logging of audit trail van de anonimiseringsmapping

---

## F-04 — Rapportgeneratie via LLM

**Gelinkt aan:** US-03, US-04, US-05
**Prioriteit:** Must-have (MVP)

### Beschrijving

De kern van de analysepipeline. Het systeem stuurt de verwerkte, geanonimiseerde data samen met een gestandaardiseerde vragenset naar de LLM. De LLM genereert per sectie een gestructureerde Nederlandstalige analyse. De maximale responstijd voor het genereren van een volledig rapport is niet kritisch voor V1 — een wachttijd van meer dan 5 minuten is acceptabel in de pilotfase.

### Gedrag

**Promptstructuur:**
- De systeemprompt instrueert de LLM om uitsluitend te redeneren op basis van de aangeleverde feiten, statistieken en eventpatronen
- De LLM wordt expliciet geïnstrueerd dat iedere claim moet worden onderbouwd met een verwijzing naar de aangeleverde data, en dat de claim *niet mag worden gemaakt* als de onderbouwing ontbreekt
- De vragenset is gestandaardiseerd en wordt niet aangepast per analyse (constitutie P-06)

**Gegenereerde secties (vaste volgorde):**
1. Wedstrijdoverzicht (gebruikte wedstrijden als bronset)
2. Speelstijlsamenvatting (aanvallend, verdedigend, pressing/omschakeling)
3. Sterktes per spelfase
4. Zwaktes per spelfase
5. Tactische aandachtspunten (should-have — US-05)
6. Datalimitaties en aanbevelingen voor aanvullende analyse

**Per sectie genereert de LLM:**
- Inhoudelijke tekst (2–5 bevindingen per sectie)
- Datadekkingindicator: Hoog / Middel / Laag
- Bronvermelding: welke wedstrijden liggen ten grondslag aan de claims in deze sectie

### Randgevallen

| Situatie | Gedrag |
|---|---|
| LLM kan een sectie niet onderbouwen | LLM genereert de standaard onbeschikbaarheidsmelding (F-06) voor die sectie; overige secties worden wel gegenereerd |
| LLM-respons is incompleet (niet alle secties aanwezig) | Systeem detecteert ontbrekende secties en vervangt deze door de onbeschikbaarheidsmelding (F-06) |
| LLM-respons bevat een claim zonder bronvermelding | Systeem-validatiestap markeert de claim als "niet geverifieerd" en voegt een waarschuwing toe; de claim wordt niet stilzwijgend overgenomen |
| LLM-respons overschrijdt de maximale tokenlimiet | Systeem splitst de aanvraag per sectie en combineert de resultaten; gebruiker merkt hier niets van |

### Acceptatiecriteria
- [ ] Het rapport bevat altijd alle vaste secties (lege of niet-onderbouwbare secties tonen de standaard onbeschikbaarheidsmelding)
- [ ] Elke inhoudelijke claim is voorzien van een bronvermelding die verwijst naar de aangeleverde wedstrijddata
- [ ] Het systeem gebruikt een identieke vragenset voor elke analyse (geen variatie per tegenstander of gebruiker)
- [ ] Het rapport is volledig in het Nederlands, inclusief alle koppen, labels en conclusies
- [ ] De LLM-output wordt gevalideerd op volledigheid vóórdat het rapport aan de gebruiker wordt getoond

### Niet in scope (V1)
- Aanpasbare vragensets door eindgebruikers
- Meerdere LLM-runs ter vergelijking of kwaliteitsverbetering
- Geautomatiseerde factcheck van LLM-output tegen brondata

---

## F-05 — Datadekkingindicator

**Gelinkt aan:** US-07, constitutie P-03
**Prioriteit:** Must-have (MVP)

### Beschrijving

Elke sectie van het rapport toont een datadekkingindicator die de gebruiker informeert over de betrouwbaarheid van de bevindingen in die sectie. De indicator wordt berekend vóórdat de LLM wordt aangeroepen, op basis van objectieve datakenmerken.

### Gedrag

**Berekeningslogica (indicatief — exact algoritme is OB-03/OB-04):**
- **Hoog:** Voldoende wedstrijden (≥ N) met volledige eventdata voor de betreffende spelfase
- **Middel:** Minder dan N wedstrijden beschikbaar, of gedeeltelijk ontbrekende data voor de betreffende spelfase
- **Laag:** Minder dan 3 wedstrijden beschikbaar, of fundamentele datatypes ontbreken voor de betreffende spelfase; of de sectie bevat een onbeschikbaarheidsmelding

**Weergave:**
- Tekst-label direct zichtbaar per sectie-kop: `[Hoog]`, `[Middel]` of `[Laag]`
- Eenmalige legenda in de inleiding van het rapport:
  - *Hoog: voldoende data voor een onderbouwde uitspraak*
  - *Middel: beperkte data; conclusies zijn indicatief*
  - *Laag: onvoldoende data; bevindingen zijn speculatief of ontbreken*

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Sectie bevat onbeschikbaarheidsmelding (F-06) | Indicator is altijd Laag |
| Data voor de ene spelfase is volledig, voor de andere beperkt | Elke sectie krijgt een eigen indicator op basis van de relevante data voor die fase |
| Alle beschikbare wedstrijden zijn van lage datakwaliteit | Indicator is Middel of Laag afhankelijk van de impact op de betreffende sectie |

### Acceptatiecriteria
- [ ] Elke sectie van het rapport toont een datadekkingindicator
- [ ] De legenda is aanwezig in de rapportinleiding
- [ ] Een sectie met een onbeschikbaarheidsmelding heeft altijd indicator Laag
- [ ] Dezelfde databeschikbaarheid levert altijd hetzelfde label op (deterministische berekening)
- [ ] De indicator is zichtbaar in de PDF-export

### Niet in scope (V1)
- Kwantitatieve dekking (bijv. percentages of scores)
- Historische vergelijking van datadekking over meerdere analyses

---

## F-06 — Expliciete onbeschikbaarheidsmelding

**Gelinkt aan:** US-08, constitutie P-05
**Prioriteit:** Must-have (MVP)

### Beschrijving

Als het systeem een sectie of claim niet kan onderbouwen vanuit de beschikbare data, toont het een vaste, expliciete melding. Het systeem mag nooit een aannemelijk klinkende tekst genereren als vervanging voor ontbrekende data.

### Gedrag

**Standaard melding (per sectie):**
> *"Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse."*

**Wanneer de melding verschijnt:**
- De LLM geeft aan geen claim te kunnen onderbouwen voor een sectie
- De systeem-validatiestap detecteert dat een sectie ontbreekt in de LLM-output
- De datadekkingindicator voor een sectie is Laag én de LLM heeft geen bruikbare output gegenereerd

**Structuur:**
- De sectie-kop blijft aanwezig in het rapport (duidelijk welk onderdeel ontbreekt)
- De melding vervangt de inhoud van de sectie
- De indicator van de sectie is altijd **[Laag]**

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Alle secties ontvangen een onbeschikbaarheidsmelding | Rapport wordt gegenereerd met alle meldingen; gebruiker wordt geïnformeerd dat de analyse geen bruikbare output heeft opgeleverd en wordt aangeraden de datasituatie te controleren |
| Slechts één claim binnen een sectie is niet onderbouwbaar | De melding wordt inline toegevoegd bij die specifieke claim, niet voor de hele sectie |

### Acceptatiecriteria
- [ ] De standaard melding is gestandaardiseerd en identiek voor alle secties
- [ ] Het systeem genereert nooit een best-guess tekst als vervanging voor ontbrekende data
- [ ] De sectiekop is altijd aanwezig, ook als de inhoud een melding is
- [ ] De melding is leesbaar in de PDF-export

### Niet in scope (V1)
- Suggesties voor alternatieve databronnen of zoekopdrachten
- Automatische notificatie aan de analist als data ontbreekt

---

## F-07 — PDF-export

**Gelinkt aan:** US-09
**Prioriteit:** Must-have (MVP)

### Beschrijving

De gebruiker kan het volledig gegenereerde rapport exporteren als PDF. De PDF is zelfstandig leesbaar, offline bruikbaar en deelbaar met staf die geen toegang heeft tot de tool.

### Gedrag

**Exportflow:**
- Gebruiker activeert de export via één knop of actie
- Het systeem genereert de PDF inclusief alle rapportonderdelen: wedstrijdoverzicht, alle secties, datadekkingindicatoren, bronvermeldingen en eventuele visualisaties
- De PDF wordt direct aangeboden als download

**Koptekst van de PDF:**
- Naam van de tegenstander (echte naam na terugmapping)
- Datum en tijd van genereren
- Projectnaam (Team DNA) of KNVB-identifier

**Inhoud:**
- Alle secties in vaste volgorde
- Datadekkingindicatoren als tekst-labels
- Bronvermeldingen per claim
- Legenda voor de datadekkingindicatoren
- Eventuele visualisaties (statistieken, grafieken) als statische afbeeldingen

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Rapport bevat alleen onbeschikbaarheidsmeldingen | PDF wordt gegenereerd met alle meldingen; rapport is nog steeds exporteerbaar |
| Visualisaties konden niet worden gegenereerd | PDF wordt gegenereerd zonder visualisaties; tekst-rapport blijft beschikbaar |
| PDF-generatie mislukt technisch | Gebruiker ontvangt een foutmelding met de suggestie opnieuw te proberen; geen gedeeltelijke PDF |

### Acceptatiecriteria
- [ ] De gebruiker kan met één actie een volledige PDF genereren
- [ ] De PDF bevat alle secties, indicatoren, bronvermeldingen en visualisaties
- [ ] De PDF is offline leesbaar zonder externe afhankelijkheden
- [ ] De koptekst bevat: teamnaam, datum van genereren en projectidentificatie
- [ ] De PDF-naam volgt een herkenbare conventie, bijv. `TeamDNA_[Tegenstander]_[Datum].pdf`

### Niet in scope (V1)
- Export naar Word (.docx) of andere formaten
- Directe verzending van de PDF via e-mail vanuit de tool
- Aanpassen van de PDF-lay-out of branding door de gebruiker

---

## F-08 — Spelersprofiel op positie (optionele verdieping)

**Gelinkt aan:** US-10
**Prioriteit:** Should-have (MVP als tijd het toelaat, anders V2)

### Beschrijving

Na het genereren van het teamrapport kan de gebruiker optioneel een verdiepingsprofiel opvragen voor een specifieke positie. Het spelersprofiel wordt gegenereerd op dezelfde anonimiserings- en traceerbaarheidsnormen als het teamrapport.

### Gedrag

**Aanvraagflow:**
- Gebruiker selecteert een positie (bijv. centrale verdediger, spits) vanuit het teamrapport
- Het systeem haalt spelersdata op voor spelers die op die positie hebben gespeeld in de geselecteerde wedstrijden
- LLM genereert een profiel met positierelevante statistieken, patronen en aandachtspunten
- Profiel wordt toegevoegd aan het rapport als bijlage of aparte sectie

**Inhoud spelersprofiel:**
- Relevante statistieken voor de betreffende positie
- Datadekkingindicator (Hoog / Middel / Laag) — extra aandacht bij spelers uit kleinere competities
- Bronvermelding naar wedstrijden
- Expliciete melding als data beperkt is: *"Beperkte data beschikbaar voor deze speler. Profiel is indicatief."*

### Randgevallen

| Situatie | Gedrag |
|---|---|
| Speler heeft minder dan 3 wedstrijden in de dataselectie | Indicator Laag + melding dat profiel indicatief is |
| Meerdere spelers op dezelfde positie | Systeem genereert een vergelijkend overzicht of vraagt de gebruiker een specifieke speler te selecteren (OB: nog te bepalen) |

### Acceptatiecriteria
- [ ] Gebruiker kan na het teamrapport een positieselectie maken voor verdiepingsanalyse
- [ ] Het spelersprofiel volgt dezelfde anonimiserings- en traceerbaarheidsnormen als het teamrapport
- [ ] Bij beperkte spelersdata is de indicator Laag en is er een expliciete melding
- [ ] Het profiel is opgenomen in de PDF-export

### Niet in scope (V1)
- Vergelijking van spelers over meerdere tegenstanders
- Automatische highlight van de meest relevante spelers zonder gebruikerselectie

---

## Technische Afhankelijkheden

| Feature | Afhankelijkheid | Risico | Mitigatie |
|---|---|---|---|
| F-01 t/m F-04 | Beschikbaarheid van event data in intern datawarehouse | Middel | Data staat klaar maar vereist nog voorbereiding; valideer vóór eerste prototyperun |
| F-03 | Tabel→tekst conversiemethode (OB-03) | Hoog | Vroeg prototype van conversiemethode testen met representatieve dataset |
| F-04 | OpenAI KNVB-workspace toegang en API-limieten | Middel | Toegang bevestigd; tokenlimiet per aanvraag testen bij volledige rapportgeneratie |
| F-04 | Gestandaardiseerde vragenset (kwaliteit van de prompts) | Hoog | Iteratief ontwikkelen en valideren tegen eigen elftal (zie validatiestrategie) |
| F-05 | Definitie van N (OB-04) | Laag | Configureerbaar maken; standaardwaarde kan later worden aangepast |
| F-07 | PDF-renderingbibliotheek | Laag | Standaard libraries beschikbaar; vroeg integreren om lay-out te valideren |
| F-08 | Spelersdata beschikbaar per positie | Middel | Testen welke posities voldoende data hebben in huidige warehouse |

---

## MVP Releasecriteria

De pilot mag niet starten totdat aan het volgende is voldaan:

- [ ] **F-01 t/m F-07 zijn geïmplementeerd en getest** op representatieve data uit het datawarehouse
- [ ] **Anonimiseringspreprocessing (F-03) werkt correct**: labels worden consistent teruggezet naar echte namen in het eindrapport
- [ ] **Tabel→tekst conversiemethode (OB-03) is vastgesteld** en gevalideerd op een set van minimaal 3 wedstrijden
- [ ] **Waarde van N (OB-04) is bepaald** en geconfigureerd in de pipeline
- [ ] **Interne validatie geslaagd**: analyse gegenereerd op het eigen elftal, gelegd naast bestaande rapporten van scouts en analisten; patronen zijn herkenbaar en claims zijn traceerbaar
- [ ] **Geen ongefundeerde claims** in de output van de validatierun (nulmeting hallucinations)
- [ ] **OpenAI KNVB-workspace is actief** en data processing agreement is bevestigd voor productiegebruik
- [ ] **PDF-export werkt correct** inclusief koptekst, indicatoren en bronvermeldingen
- [ ] **Retentie- en loggingbeleid (OB-01, OB-02) is besloten** vóór eerste gebruik met echte tegenstander data
- [ ] **Onboarding met scout en analist afgerond**: begeleide eerste sessie heeft plaatsgevonden
