# Constitutie — Team DNA
**Koninklijke Nederlandse Voetbalbond (KNVB)**
Versie 1.0 — mei 2026

---

## Wat is dit document?

Dit document legt de niet-onderhandelbare principes vast waaraan alle features, architectuurkeuzes en implementatiebeslissingen van Team DNA moeten voldoen. Als een feature, aanpassing of technische keuze in conflict is met een principe in dit document, wint dit document. De constitutie geldt voor V1 én als kader voor toekomstige versies.

---

## Principes

### P-01 — De tool is oordeelsvoeder, niet oordeelsvervanger

Team DNA ondersteunt de scout en performance analist in hun analyseproces. De tool levert een gestructureerde eerste laag van inzichten op basis van event data. Het professionele oordeel van de scout — gevormd door live observatie, video-analyse en ervaring — blijft te allen tijde leidend.

**Afdwingbaar door:**
Elke sectie van het gegenereerde rapport bevat een expliciete context-disclaimer die aangeeft dat de bevindingen zijn gebaseerd op event data en bedoeld zijn als startpunt voor verdere analyse, niet als eindconclusie. De tool stelt nooit voor wat de staf *moet* doen — alleen wat de data *laat zien*.

---

### P-02 — Elke claim is traceerbaar naar de brondata

Geen enkele conclusie of observatie mag in het rapport verschijnen zonder directe koppeling aan een concrete databron: statistieken, geaggregeerde waarden, eventpatronen of specifieke wedstrijdexempels. Een plausibel klinkende maar ongefundeerde claim is erger dan geen claim.

**Afdwingbaar door:**
Elke inhoudelijke bewering in het rapport is voorzien van een bronvermelding op claimniveau, met verwijzing naar de wedstrijd(en) waarop de bewering is gebaseerd. Ontbreekt de onderbouwing, dan genereert het systeem automatisch een "Niet onderbouwbaar"-melding (zie P-05) in plaats van een claim.

---

### P-03 — Transparantie over datakwaliteit is verplicht

De betrouwbaarheid van een analyse is direct afhankelijk van de hoeveelheid en kwaliteit van de beschikbare data. Bij minder bekende tegenstanders, spelers uit kleinere competities of beperkt beschikbare wedstrijden kan de data onvolledig of minder betrouwbaar zijn. Dit moet voor de gebruiker altijd zichtbaar zijn.

**Afdwingbaar door:**
Elke sectie van het rapport bevat een datadekkingindicator met drie niveaus:

- **Hoog** — voldoende wedstrijden en data om een onderbouwde uitspraak te doen
- **Middel** — beperkt aantal wedstrijden of gedeeltelijk ontbrekende data; conclusies zijn indicatief
- **Laag** — onvoldoende data voor een betrouwbare uitspraak; bevindingen zijn speculatief

De indicator wordt berekend op basis van het aantal beschikbare wedstrijden en de volledigheid van de eventdata, en wordt in de rapportage weergegeven als tekst-label per sectie.

---

### P-04 — Anonimisering richting de LLM is verplicht

Om reputatiebias, landenassociaties en bekendheidseffecten van spelersnamen te voorkomen, worden alle namen van spelers, teams en landen omgezet naar neutrale ID's of labels vóórdat data aan de LLM wordt aangeleverd. De LLM redeneert uitsluitend op basis van anonieme identifiers.

**Afdwingbaar door:**
De preprocessing-stap in de analysepipeline vervangt alle namen door labels (bijv. `SPELER_07`, `TEAM_A`, `LAND_X`) voordat de data en prompt naar de LLM worden gestuurd. De mapping van ID's naar echte namen wordt intern bewaard en uitsluitend in de eindrapportage voor de gebruiker teruggezet. De preprocessing is een verplichte stap — de pipeline kan niet worden uitgevoerd zonder deze stap.

---

### P-05 — Geen stille fouten of gissingen bij ontbrekende data

Wanneer de beschikbare data onvoldoende is om een sectie of claim te onderbouwen, meldt het systeem dit expliciet. Het systeem mag nooit een best-guess presenteren zonder duidelijke aanduiding dat het gaat om een redenering buiten de data, en mag nooit een sectie stilzwijgend weglaten.

**Afdwingbaar door:**
Het systeem genereert altijd alle vaste rapportsecties. Als een sectie niet onderbouwd kan worden, verschijnt daar de melding: *"Deze sectie kan niet worden onderbouwd op basis van de beschikbare data. Aanbeveling: aanvullen via video-analyse."* Deze melding telt als een geldige sectiemvulling — een lege sectie is nooit acceptabel.

---

### P-06 — Gestandaardiseerde vraagstelling per analyse

Elke tegenstander analyse wordt gegenereerd op basis van dezelfde gestandaardiseerde vragenset. Dit borgt consistentie tussen analyses, vermindert afhankelijkheid van individuele voorkeuren van scouts, en maakt vergelijking tussen tegenstanders over tijd mogelijk.

**Afdwingbaar door:**
De vragenset is vastgelegd in de systeemprompt-template en wordt niet aangepast per analyse. Uitbreiding of aanpassing van de vragenset vindt alleen plaats via een beheerder en wordt geversied. Individuele gebruikers kunnen de vragenset niet overschrijven in V1.

---

### P-07 — Data wordt niet gebruikt buiten de analysedoeleinden

De event data die wordt ingekocht van dataproviders is gelicentieerd voor intern analysegebruik. Gebruik voor commerciële, publieke of andere doeleinden is niet toegestaan. De KNVB OpenAI-workspace borgt dat de aangeleverde data niet wordt gebruikt voor het trainen van modellen.

**Afdwingbaar door:**
De tool gebruikt uitsluitend de KNVB OpenAI-workspace voor alle LLM-interacties. Gebruik van andere OpenAI-toegangspaden (API keys buiten de workspace) is niet toegestaan. Datacontracten met externe providers worden gerespecteerd: gegenereerde analyses zijn uitsluitend bestemd voor intern gebruik door de nationale elftallenstaf.

---

## Technische Beslissingen (vastgesteld)

| Beslissing | Keuze | Reden |
|---|---|---|
| LLM-platform | OpenAI API via KNVB-workspace | No-train garantie via bestaande enterprise overeenkomst |
| Data-input V1 | Intern datawarehouse / database | Event data is beschikbaar; geen externe API-integratie nodig voor V1 |
| Data-formaat voor LLM | Tabeldata omgezet naar tekstuele beschrijving | LLM verwerkt tekst effectiever dan ruwe tabelrijen |
| Anonimiseringsmethode | Preprocessing ID-mapping (vóór LLM-aanlevering) | Voorkomt reputatie- en herkomstbias in LLM-redenering |
| Authenticatie (V1) | Geen — intern gebruik, max. 2–3 gebruikers | Pilot is te klein voor SSO-integratie; V2 heroverweegt dit |
| Rapporttaal | Altijd Nederlands | Primaire gebruikerstaal |
| Zekerheidsweergave | Tekst-label per sectie (Hoog / Middel / Laag) | Eenvoudig leesbaar, geen visuele complexiteit nodig |
| Outputformaat | PDF-export | Apparaat-agnostisch, deelbaar met staf zonder tooltoegang |
| Wedstrijdselectie | Automatisch op basis van datum (laatste N wedstrijden) | Minimaliseert handmatig werk bij toernooivoorbereiding |
| Chatbot / verdiepende vragen | Niet in V1 — gepland voor V2 | Scopekeuze: eerst rapportkwaliteit valideren |
| Spelersprofielen | Optionele verdieping, niet verplicht in V1 | Team-eersts als kernfocus; spelersdata als drilldown |
| Beschikbaarheid pilot | Best-effort | Pilotfase is exploratief; SLA-vereisten komen bij productierelease |
| Offline gebruik | PDF-export dekt de offlinebehoefte af | Gegenereerde rapporten zijn als PDF offline leesbaar |

---

## Open Besluiten (nog te nemen)

| # | Besluit | Eigenaar | Deadline |
|---|---|---|---|
| OB-01 | Retentiebeleid: hoe lang worden gegenereerde analyses bewaard en waar? | Performance / Legal | Vóór productierelease |
| OB-02 | Logging-beleid: worden LLM-prompts en outputs opgeslagen, en zo ja door wie raadpleegbaar? | Performance / Legal | Vóór productierelease |
| OB-03 | Exacte methode voor tabel→tekst omzetting: per-rij statements, geaggregeerde beschrijvingen of een combinatie? | Ontwikkelteam | Eerste prototype |
| OB-04 | Waarde van N bij automatische wedstrijdselectie: hoeveel recente wedstrijden worden standaard meegenomen? | Performance + Scout | Eerste prototype |
| OB-05 | Visualisatieformaat in het rapport: welke statistieken worden als grafiek getoond en in welke vorm? | Performance + Ontwikkelteam | V1 rapportontwerp |
| OB-06 | Toegangscontrole voor V2: welke rollen (coaches, bredere staf) krijgen leestoegang en via welk mechanisme? | Performance / IT | V2 scope |
| OB-07 | Validatiemethodiek: hoe wordt de kwaliteit van de output formeel gemeten zodra de pilotfase voorbij is? | Performance + Scout | Post-pilot evaluatie |
