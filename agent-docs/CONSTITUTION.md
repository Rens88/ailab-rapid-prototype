# Constitutie — Baseline
**KNLTB — Nationaal Tennis Centrum**
Versie 1.0 — 15 mei 2026

## Wat is dit document?

Dit document legt de niet-onderhandelbare principes vast waaraan alle features, technische keuzes en ontwerpbeslissingen van Baseline moeten voldoen. Baseline is een read-only planningsdashboard met een conversationele AI-chatbox, bedoeld voor de technische staf van het NTC. Als een feature of technische keuze in conflict is met een principe in dit document, wint dit document.

---

## Principes

### P-01 — Data-integriteit is absoluut
Geen enkele gebruiker mag ooit de planning of aanwezigheidsdata van een andere groep of persoon te zien krijgen door een fout in het systeem. Een data-mix-up — waarbij data van speler A getoond wordt onder speler B, of groep 1-data onder groep 3 — is het zwaarste technische falen dat Baseline kan vertonen.

**Afdwingbaar door:**
Elke data-ophaalactie (Graph API-aanroep, chatbox-query) is gekoppeld aan een expliciete bronidentificatie (groep-ID, persoon-ID). Integratie- en end-to-end tests valideren vóór elke release dat datasegregatie correct werkt. Een release mag niet starten zonder een geslaagde data-integriteitstest met echte of realistische testdata.

---

### P-02 — AVG-conformiteit is een harde voorwaarde, geen nagedachte
Baseline verwerkt persoonsgegevens van sporters en staf (namen, aanwezigheidsdata, planningsinformatie). De verwerking vindt uitsluitend plaats op basis van bestaande toestemmingsgronden. Alle verwerkingen blijven binnen de EU. Er worden geen persoonsgegevens verzonden naar systemen buiten de EU.

**Afdwingbaar door:**
Alle infrastructuur draait op Azure EU (West-Europe of North-Europe). Azure OpenAI EU-endpoint wordt gebruikt voor de chatbox. Data vertrekt nooit naar Azure-regio's buiten de EU. Dit wordt geverifieerd via de Azure-configuratie vóór productielancering. De DPO of juridische afdeling van KNLTB bevestigt schriftelijk dat de bestaande toestemmingsgrond de verwerking dekt.

---

### P-03 — Baseline is altijd read-only
Het dashboard en de chatbox zijn uitsluitend bedoeld voor inzage en bevraging. Baseline wijzigt, verwijdert of overschrijft nooit data in de bronbestanden op SharePoint. De verantwoordelijkheid voor datakwaliteit ligt bij de eigenaren van de Excel-bestanden, niet bij Baseline.

**Afdwingbaar door:**
De Microsoft Graph API-integratie gebruikt uitsluitend leesrechten (`Files.Read`, `Sites.Read.All`). Schrijfrechten (`Files.ReadWrite`) mogen niet worden aangevraagd of verleend. Dit wordt gecontroleerd in de Azure AD-app-registratie bij elke deployment.

---

### P-04 — Verouderde of ontbrekende data is altijd zichtbaar
Als een databron niet bereikbaar is, niet vernieuwd is, of onvolledig is, toont Baseline dit expliciet aan de gebruiker. Stille fouten — waarbij een gebruiker een leeg of verouderd dashboard ziet zonder waarschuwing — zijn niet toegestaan.

**Afdwingbaar door:**
Elke dashboardweergave toont een tijdstempel van de laatste succesvolle datasync. Ontbrekende of verouderde data (ouder dan de geconfigureerde drempelwaarde) wordt gemarkeerd met een gele vlag. Als de Graph API-verbinding faalt, toont het dashboard een expliciete foutmelding met tijdstip van de laatste bekende stand.

---

### P-05 — Laadtijd onder 3 seconden voor de gecombineerde weekweergave
Gebruikers besteden 1–3 minuten per sessie aan het dashboard. Een laadtijd boven de 3 seconden voor de hoofdweergave leidt tot afhaken en niet-gebruik. Dit is een harde prestatieeis, geen richtlijn.

**Afdwingbaar door:**
De gecombineerde weekweergave wordt getest bij elke release op laadtijd via geautomatiseerde performance-tests (bijv. Lighthouse of een equivalente tool). Een laadtijd > 3 seconden blokkeert een release. Caching van Graph API-responses is verplicht; de cachestrategie wordt vastgelegd als technische beslissing.

---

### P-06 — Responsief ontwerp: desktop én smartphone
De primaire gebruikers raadplegen Baseline zowel op laptop/desktop (kantoor, vergadering) als op smartphone (onderweg, op de baan). Alle weergaven en interacties — inclusief de chatbox — moeten volledig functioneel zijn op beide formaten.

**Afdwingbaar door:**
Elke UI-component wordt getest op minimaal twee viewports: desktop (≥ 1280px breed) en mobiel (≤ 390px breed). De chatbox is toegankelijk en bruikbaar op smartphone zonder horizontaal scrollen. Dit wordt gevalideerd via handmatige of geautomatiseerde viewport-tests vóór elke release.

---

### P-07 — De chatbox antwoordt alleen op basis van brondata, nooit op basis van aannames
De AI-chatbox beantwoordt uitsluitend vragen die beantwoord kunnen worden met de planningsdata of aanwezigheidsdata uit de gekoppelde bronbestanden. De chatbox verzint geen antwoorden, vult geen ontbrekende data aan met aannames, en geeft bij onzekerheid of ontbrekende data een expliciete melding terug.

**Afdwingbaar door:**
De systeemprompt van de Azure OpenAI-integratie bevat een expliciete instructie om geen informatie te genereren die niet aantoonbaar afkomstig is uit de opgehaalde brondata. Antwoorden die buiten de planningsdomeinen vallen worden geweigerd met een duidelijke melding ("Dit valt buiten wat ik kan opzoeken in de planningsdata").

---

### P-08 — Geen gebruikslogboeken opgeslagen
Baseline slaat geen logboeken op van wie het dashboard heeft geraadpleegd, welke vragen aan de chatbox zijn gesteld, of welke filters zijn toegepast. Privacy van gebruikers is ook intern gewaarborgd.

**Afdwingbaar door:**
De applicatie configureert geen telemetrie of gebruikslogging naar externe diensten. Azure Application Insights (of equivalent) mag uitsluitend worden ingezet voor technische foutmeldingen en prestatiemonitoring — niet voor gebruikersgedrag of chatbox-inhoud. Dit wordt geverifieerd in de privacybeoordeling vóór de lancering.

---

### P-09 — De Topsportmanager is eindverantwoordelijke en beslisser
Alle features, prioriteitswijzigingen en afwijkingen van deze constitutie vereisen goedkeuring van de Topsportmanager. Het ontwikkelteam adviseert; de Topsportmanager besluit.

**Afdwingbaar door:**
Open Besluiten (zie sectie hieronder) worden niet eenzijdig opgelost door het ontwikkelteam. Elk Open Besluit heeft een eigenaar en een deadline. Besluiten worden schriftelijk vastgelegd voordat de bijbehorende feature in ontwikkeling gaat.

---

## Technische Beslissingen (vastgesteld)

| Beslissing | Keuze | Reden |
|---|---|---|
| Cloudplatform | Microsoft Azure EU (West-Europe) | AVG-conformiteit, bestaande Microsoft-omgeving KNLTB |
| Authenticatie | Azure AD SSO (KNLTB-account) | Gebruikers hoeven geen apart wachtwoord; bestaande identiteiten |
| Data-integratie | Microsoft Graph API (read-only) | Real-time koppeling met SharePoint-bestanden zonder handmatige export |
| Cachestrategie | Server-side caching van Graph API-responses | Laadtijd < 3 sec haalbaar maken ondanks real-time brondata |
| AI-platform (chatbox) | Azure OpenAI (EU-endpoint) | AVG-conform, data blijft in EU, past in Microsoft-stack |
| Toegangsniveaus MVP | Geen rolscheiding — alle stafleden zien alles | Vereenvoudigt MVP; rolscheiding wordt heroverwogen in fase 2 |
| Gebruikslogging | Geen gebruikslogboeken | Privacy-first conform P-08 |
| Beschikbaarheidsniveau pilot | Best-effort | Occasionele uitval acceptabel tijdens testfase |

---

## Open Besluiten (nog te nemen)

| # | Besluit | Eigenaar | Deadline |
|---|---|---|---|
| OB-01 | Exacte MVP-deadline: vóór zomerstop 2026 — welke specifieke datum is de go/no-go? | Topsportmanager | Z.s.m. |
| OB-02 | Standaardisering Excel-invoerformat: welk format geldt als bronstandaard voor alle groepen? | Staf per groep + Topsportmanager | Vóór technische integratie |
| OB-03 | Rolscheiding fase 2: welke rollen mogen wat zien als de pilot opschaalt (bijv. Padel)? | Topsportmanager | Na pilotevaluatie |
| OB-04 | Bewaartermijn planningsdata: hoelang bewaren we historische data conform de toestemmingsverklaring? | DPO / juridisch KNLTB | Vóór lancering |
| OB-05 | Drempelwaarde gele vlag: na hoeveel uur/dagen zonder update wordt data als verouderd gemarkeerd? | Topsportmanager + staf | Vóór start UI-ontwikkeling |
