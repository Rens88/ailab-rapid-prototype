# Constitutie — Trainingsload Shorttrack
**NOC\*NSF / KNSB**
Versie 1.0 — 12 mei 2026

## Wat is dit document?

Dit document legt de niet-onderhandelbare principes vast waaraan alle features, technische keuzes en analyseresultaten van het project Trainingsload Shorttrack moeten voldoen. Het project bouwt een analysepipeline die externe trainingsbelasting (Kinexon) combineert met interne trainingsbelasting (RPE, hartslagdata) om de meest relevante parameters voor shorttrack-trainingsload te identificeren. Als een feature of technische keuze in conflict is met een principe in dit document, wint dit document.

---

## Principes

### P-01 — Representativiteitscheck als harde kwaliteitspoort

De analysepipeline mag geen conclusies trekken over het seizoen als de Kinexon-dataset niet representatief is. Bekend risico: de Kinexon-data dekt voornamelijk relay-trainingen. Conclusies op basis van een eenzijdige dataset zouden het vertrouwen in het systeem — en de trainingsbesluiten — schaden.

**Afdwingbaar door:**
De pipeline voert vóór elke parameteranalyse een automatische representativiteitscheck uit. Als het percentage gedekte trainingen onder een vooraf vastgestelde drempel valt, stopt de pipeline en genereert een expliciete waarschuwing met de reden. De parameteranalyse wordt pas gestart na handmatige bevestiging door Froukje.

---

### P-02 — Precisie boven volledigheid

De pipeline levert alleen parameters op waarvoor aantoonbaar statistisch bewijs bestaat in de dataset. Het is beter drie goed-onderbouwde parameters op te leveren dan acht onzekere. Dit is in het bijzonder van belang omdat Niels (coach, laag technisch niveau) de conclusies direct gebruikt voor trainingsbesluiten.

**Afdwingbaar door:**
Elke opgeleverde parameter bevat een betrouwbaarheids- of significantie-indicatie (bijv. effectgrootte, correlatiesterkte of p-waarde). Parameters zonder voldoende bewijs worden expliciet als "onvoldoende onderbouwd" gelabeld en niet als aanbeveling gepresenteerd.

---

### P-03 — Altijd redenering tonen

Iedere conclusie of aanbeveling die de pipeline produceert, is vergezeld van een uitleg: welke data is gebruikt, welke methode is toegepast, en waarom dit resultaat volgt. Geen black-box output.

**Afdwingbaar door:**
Het technische rapport (voor Froukje) bevat altijd de methodesectie en de onderliggende statistieken. Het actiegerichte overzicht (voor Niels) bevat altijd een beknopte redenering per aanbeveling, in begrijpelijk Nederlands. Een review door Froukje valideert of de uitleg klopt met haar domeinkennis vóór het overzicht aan Niels wordt gedeeld.

---

### P-04 — Transparantie bij onvoldoende data

Als de pipeline geen betrouwbare conclusie kan trekken, meldt zij dit expliciet. De pipeline produceert geen output wanneer de data onvoldoende basis biedt voor verantwoorde conclusies.

**Afdwingbaar door:**
In elk outputbestand staat een sectie "Databeperkingen" met een overzicht van ontbrekende trainingen, periodes zonder Kinexon-meting, en andere bekende gaten. Als de analyse een sectie niet kan afronden vanwege ontbrekende data, verschijnt er een gemarkeerde open post in plaats van een stilzwijgend lege sectie.

---

### P-05 — Privacy-by-design

Trainingsdata van shorttrack-sporters bevat persoonlijke gezondheidsinformatie (hartslagdata, RPE, prestatiegegevens). Sporters hebben impliciet toestemming gegeven via bestaande KNSB-overeenkomsten. Dit gebruik moet expliciet geverifieerd worden bij de DPO voordat de pipeline in productie gaat.

**Afdwingbaar door:**
De pipeline verwerkt sportersdata uitsluitend op beveiligde, toegangsgecontroleerde systemen. Froukje heeft volledige toegang. Niels ontvangt uitsluitend de geanonimiseerde of geaggregeerde teamoutput, tenzij hij als coach expliciete toegang nodig heeft tot individuele data van zijn sporters. Alle toegang wordt gelogd voor auditdoeleinden. De DPO-verificatiestap is een harde release-voorwaarde (zie MVP Releasecriteria in features.md).

---

### P-06 — Geen verkeerde data aan verkeerde sporter

Koppeling van trainingsdata aan sporters (hartslagdata, RPE, Kinexon) moet altijd correct zijn. Een verwisseling is onacceptabel: het leidt tot foutieve conclusies én tot een schending van de privacy van de betreffende sporter.

**Afdwingbaar door:**
De data-ingeststap bevat een verplichte koppelingsvalidatie: elke sessie in de gecombineerde dataset wordt voorzien van een sporterId en een datum die aantoonbaar overeenkomen over alle bronnen (Kinexon, AMS, RPE-vragenlijst). Bij mismatch wordt de sessie gemarkeerd als "niet koppelbaar" en niet meegenomen in de analyse.

---

### P-07 — Brondata is onaantastbaar

De originele bronbestanden (Kinexon-export, AMS-data, RPE-vragenlijsten) worden nooit overschreven of gewijzigd door de pipeline. Alle transformaties vinden plaats op kopieën in een aparte verwerkingslaag.

**Afdwingbaar door:**
De pipeline werkt met een onveranderlijke bronlaag (read-only input) en een aparte analyselaag. Versiebeheersoftware of bestandsdatering borgt dat de originelen intact blijven. Indien een analyse opnieuw wordt uitgevoerd, worden de originelen opnieuw ingelezen — niet de tussenresultaten.

---

### P-08 — Herhaalbaar instrument, niet eenmalige analyse

De pipeline is ontworpen om volgend shorttrack-seizoen opnieuw te kunnen worden ingezet. Alle stappen, parameters en drempelwaarden zijn gedocumenteerd zodat een nieuw DSA-teamlid de analyse kan reproduceren zonder dat Froukje of het huidige team aanwezig is.

**Afdwingbaar door:**
De pipeline wordt gedocumenteerd in een technische handleiding die als onderdeel van de oplevering wordt meegeleverd. De handleiding bevat: instructies voor data-aanlevering, uitleg van de analysestappen, beschrijving van configureerbare parameters (bijv. drempel voor representativiteitscheck), en een beschrijving van de verwachte outputstructuur.

---

## Technische Beslissingen (vastgesteld)

| Beslissing | Keuze | Reden |
|---|---|---|
| Doeldomein | Shorttrack (KNSB) | Scope van de pilot; andere sporten zijn post-MVP |
| Outputformaten | Rapport (PDF/Word) + grafieken (PNG/SVG) + dataset (CSV/Excel) | Verschillende behoeften: Froukje analyseert, Niels leest, AMS ontvangt data |
| Outputtaal | Nederlands | Beide eindgebruikers zijn Nederlandstalig; shorttrack-terminologie is Nederlandstalig |
| Authenticatie | Niet van toepassing | Geen front-end gebruikersinterface in de pilot |
| Toegangsmodel | Froukje: volledige toegang; Niels: alleen actiegericht outputrapport | Gebaseerd op rol en technisch niveau |
| Auditlogging | Ja — voor kwaliteitsverbetering | Elke analyse-run wordt gelogd met timestamp, inputbestanden en versie-informatie |
| Analysemethode | Precisie boven volledigheid | Zie P-02; 3 goed-onderbouwde parameters > 8 onzekere |
| Deadline | Vóór start nieuw shorttrack-seizoen (augustus/september 2026) | Inzichten moeten beschikbaar zijn voor de trainingsplanning van het nieuwe seizoen |

---

## Open Besluiten (nog te nemen)

| # | Besluit | Eigenaar | Deadline |
|---|---|---|---|
| OB-01 | Hostingplatform: EU-cloud (Azure/AWS Frankfurt) of on-premise bij NOC\*NSF | DSA-team + NOC\*NSF IT | Vóór start technische bouw |
| OB-02 | AI/analyse-platform: Azure OpenAI, open source, of traditionele statistiek (correlatie, feature importance) | DSA-team | Vóór start technische bouw |
| OB-03 | Data-integratiewijze: handmatige CSV-upload of API-koppeling met Kinexon/AMS | DSA-team + KNSB (Froukje) | Vóór start data-sprint |
| OB-04 | Dataretentiebeleid: hoe lang mag sportersdata bewaard worden na de pilot? | DPO NOC\*NSF | Vóór go-live |
| OB-05 | AVG/GDPR-verificatie: dekt de bestaande KNSB-toestemming ook gebruik van Kinexon-data voor AI-analyse? | DPO NOC\*NSF | Vóór start data-sprint |
| OB-06 | Drempelwaarde representativiteitscheck: welk percentage gedekte trainingen is minimaal vereist? | Froukje + DSA-team | Vóór start analyse-sprint |
| OB-07 | Gedrag pipeline bij ontbrekende data: expliciet melden, stil doorwerken, of als signaal beschouwen? | Froukje + DSA-team | Vóór start analyse-sprint |
| OB-08 | Toegang Niels tot individuele sportersdata: heeft de coach inzage nodig in data per sporter, of alleen op teamniveau? | Niels + DPO | Vóór go-live |
| OB-09 | MyLaps-data (rondetijden, rondenaantal) in of buiten de MVP-scope? MyLaps heeft waarschijnlijk hogere dekking dan Kinexon en biedt een alternatieve externe-loadproxy. | Froukje + DSA-team | Vóór start data-sprint |
| OB-10 | Minimale verdeling over trainingstypes in de representativiteitscheck: niet alleen dekkingspercentage totaal, maar ook minimale vertegenwoordiging van individuele trainingen (naast relay). Drempelwaarden bepalen. | Froukje + DSA-team | Vóór start analyse-sprint |
| OB-11 | Wedstrijddata als benchmark: is er Kinexon- of MyLaps-data beschikbaar van wedstrijden? Zo ja, dan kan de kernvraag "trainen wij wat we in de wedstrijd nodig hebben?" direct empirisch worden beantwoord. | Froukje + KNSB | Vóór start analyse-sprint |
| OB-12 | Aggregatiemethode per databron: hoe worden RPE (sessieniveau), hartslagdata (tijdreeks) en Kinexon (hoge frequentie) naar een vergelijkbaar sessiemaatstaf gebracht? Keuze voor gemiddelde, piek, tijd-in-zone of som heeft directe invloed op correlaties. | DSA-team + Froukje | Vóór start analyse-sprint |
| OB-13 | sRPE vs. ruwe RPE: is sessieduur beschikbaar per training? Zo ja, dan is sRPE (RPE × sessieduur) de aanbevolen loadmaatstaf (gevalideerd; Foster et al.). Zo nee, dan wordt ruwe RPE gebruikt met bijbehorende beperking. | Froukje + DSA-team | Vóór start data-sprint |
| OB-14 | Trainingstypelabels: zijn er labels per sessie beschikbaar (bijv. snelheid, uithoudingsvermogen, techniek, relay)? Zonder trainingstype kunnen correlaties tussen Kinexon en RPE/hartslag vertekend zijn door sessietypeeffecten. | Froukje + KNSB | Vóór start data-sprint |
