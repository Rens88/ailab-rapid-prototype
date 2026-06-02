# Architectuur — Team DNA
**Koninklijke Nederlandse Voetbalbond (KNVB)**
Versie 1.0 — juni 2026

---

## Overzicht

Team DNA genereert gestructureerde tegenstander-analyserapporten op basis van event data uit een intern datawarehouse. De pipeline bestaat uit een reeks verplichte verwerkingsstappen die de data klaarmaken voor de LLM, de LLM-output valideren, en het eindrapport samenstellen inclusief PDF-export.

De architectuur is bewust eenvoudig gehouden voor de pilotfase: één gebruiker tegelijk, geen authenticatielaag, geen asynchrone wachtrij.

---

## Pipeline — hoog niveau

```
Gebruiker selecteert tegenstander
         │
         ▼
┌─────────────────────────────┐
│  1. Data ophalen             │  Datawarehouse query:
│     (Data Fetcher)          │  laatste N wedstrijden + event data
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  2. Preprocessing           │  2a. Anonimisering
│     (Preprocessor)         │      namen → labels (SPELER_01, TEAM_A, …)
│                             │      sessiemapping opslaan
│                             │  2b. Tabel → tekst conversie
│                             │      event/aggregaatdata → feitelijke tekst
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  3. Datadekking berekenen   │  Per sectie: Hoog / Middel / Laag
│     (Coverage Calculator)   │  Berekend vóór LLM-aanroep
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  4. LLM aanroepen           │  OpenAI via KNVB-workspace
│     (LLM Client)            │  Systeemprompt + gestandaardiseerde vragenset
│                             │  + geanonimiseerde tekstdata
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  5. Output valideren        │  Alle secties aanwezig?
│     (Output Validator)      │  Claims voorzien van bronvermelding?
│                             │  Ontbrekende secties → onbeschikbaarheidsmelding
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  6. De-anonimiseren         │  Labels terug naar echte namen via sessiemapping
│     (De-anonymiser)         │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  7. Rapport samenstellen    │  Secties + indicatoren + bronvermeldingen
│     en tonen (UI)           │  Weergave in Streamlit of browser
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  8. PDF export (optioneel)  │  Volledige PDF inclusief koptekst,
│     (PDF Renderer)          │  indicatoren, bronvermeldingen
└─────────────────────────────┘
```

---

## Componenten

### UI Layer (Streamlit — Phase 2)

Verantwoordelijk voor:
- Tegenstander selectie (dropdown van beschikbare teams)
- Voortgangsindicatie tijdens pipelineuitvoering (statuslabels per stap)
- Weergave van het gegenereerde rapport
- PDF-exportknop

Technologie: Python / Streamlit (`app.py`). Geen externe API-aanroepen vanuit de UI-laag zelf — alle logica zit in de pipeline.

---

### Pipeline Controller

Orkestreert de volledige verwerkingsketen. Verantwoordelijk voor:
- Aanroepen van elke stap in de juiste volgorde
- Doorgeven van voortgangsstatus naar de UI
- Afbreken en foutmelding bij technische fouten in een stap
- Blokkeren van dubbele aanvragen (constitutie F-01)

---

### Data Fetcher

Haalt event data op uit het interne datawarehouse. Verantwoordelijk voor:
- Query op teamidentificatie → beschikbare wedstrijden, gesorteerd op datum
- Selectie van de N meest recente wedstrijden (N is configureerbaar door beheerder, open besluit OB-04)
- Controle op databeschikbaarheid vóór pipelinestart — pipeline start niet bij onvoldoende data
- Teruggave van: wedstrijdlijst + ruwe event- en aggregaatdata per wedstrijd

---

### Preprocessor

#### 2a — Anonimisering (verplicht, niet overslaan)

- Vervangt alle spelernamen door sequentiële labels: `SPELER_01`, `SPELER_02`, …
- Vervangt de teamnaam van de tegenstander door `TEAM_A`
- Vervangt landnamen door `LAND_X`
- Slaat de mapping (label → echte naam) op in de sessie
- De sessiemapping is het enige referentiepunt voor de latere terugmapping — verlies ervan is een fatale fout

#### 2b — Tabel → tekst conversie (methode open besluit OB-03)

- Zet event- en aggregaatdata om naar gestructureerde Nederlandstalige tekst
- Uitsluitend feitelijke statements, geen interpretaties of conclusies
- Ontbrekende kolommen worden overgeslagen en gelogd; impact is zichtbaar in de dekkingindicator
- Kandidaat-methoden (te valideren in eerste prototype):
  - Per-rij statements: elke databron wordt één tekstzin
  - Geaggregeerde beschrijvingen: statistieken worden samengevoegd per spelfase
  - Combinatie: hoog-niveau aggregaat + selectieve per-rij detail voor uitschieters

---

### Coverage Calculator

Berekent de datadekkingindicator per rapportsectie vóórdat de LLM wordt aangeroepen:

| Indicator | Criteria |
|---|---|
| **Hoog**   | ≥ N wedstrijden beschikbaar, eventdata volledig voor de betreffende spelfase |
| **Middel** | < N wedstrijden, of gedeeltelijk ontbrekende data voor de betreffende spelfase |
| **Laag**   | < 3 wedstrijden, of fundamentele datatypes ontbreken voor de betreffende spelfase |

De indicator is deterministisch: dezelfde inputdata levert altijd hetzelfde label op.

---

### LLM Client

- Platform: OpenAI API via de KNVB enterprise workspace (no-train garantie)
- Aanroep: één aanroep per rapport met de volledige geanonimiseerde dataset en vragenset
- Bij overschrijding van tokenlimiet: opsplitsing per sectie, resultaten samengevoegd
- De vragenset is vastgelegd in de systeemprompt-template (zie `PROMPTS.md`) en wordt niet per analyse aangepast

---

### Output Validator

Valideert de LLM-respons vóórdat die aan de gebruiker wordt getoond:

| Controle | Actie bij fout |
|---|---|
| Sectie ontbreekt in respons | Sectie vervangen door standaard onbeschikbaarheidsmelding |
| Claim zonder bronvermelding | Claim gemarkeerd als "niet geverifieerd" + waarschuwing toegevoegd |
| Sectie bevat onbeschikbaarheidsmelding | Dekkingindicator geforceerd naar Laag |
| Respons is leeg of onparseerbaar | Pipeline stopt, foutmelding naar gebruiker |

Het systeem toont nooit een gedeeltelijk rapport. Bij een technische fout in de validatiestap krijgt de gebruiker een begrijpelijke foutmelding met het verzoek opnieuw te proberen.

---

### De-anonymiser

- Leest de sessiemapping
- Vervangt alle labels in de gevalideerde LLM-output terug naar echte namen
- Als de sessiemapping niet meer beschikbaar is: rapport kan niet worden afgerond, foutmelding naar gebruiker

---

### PDF Renderer

- Genereert een PDF van het volledig samengestelde rapport
- Koptekst: teamnaam (echte naam), datum van genereren, projectidentificatie (Team DNA / KNVB)
- Bestandsnaamconventie: `TeamDNA_[Tegenstander]_[YYYY-MM-DD].pdf`
- Inhoud: alle secties in vaste volgorde, datadekkingindicatoren, bronvermeldingen, visualisaties als statische afbeeldingen (indien aanwezig), legenda
- PDF is offline leesbaar zonder externe afhankelijkheden
- Bibliotheek (nog te bepalen — zie technische afhankelijkheden): kandidaten zijn `weasyprint`, `reportlab`, of Streamlit-native print-naar-PDF

---

## Datastroom samengevat

```
Datawarehouse
    → ruwe event data (tabel)
    → Preprocessor (anonimisering + tabel→tekst)
    → geanonimiseerde tekstbeschrijving
    → LLM Client (systeemprompt + vragenset + tekstdata)
    → LLM-respons (secties in labels)
    → Output Validator (volledigheid + bronvermelding)
    → De-anonymiser (labels → echte namen)
    → Coverage Calculator (indicatoren per sectie)
    → Rapport (secties + indicatoren + bronvermeldingen)
    → PDF export
```

---

## Technische keuzes (vastgesteld in constitutie)

| Beslissing | Keuze |
|---|---|
| LLM-platform | OpenAI API via KNVB enterprise workspace |
| Data-input V1 | Intern datawarehouse — event data staat klaar |
| Data-formaat voor LLM | Tabeldata omgezet naar tekstuele beschrijving (methode: OB-03) |
| Anonimiseringsmethode | Preprocessing ID-mapping vóór LLM-aanlevering |
| Authenticatie (V1) | Geen — intern gebruik, max. 2–3 gebruikers |
| Rapporttaal | Altijd Nederlands |
| Zekerheidsweergave | Tekst-label per sectie (Hoog / Middel / Laag) |
| Outputformaat | PDF-export |
| Wedstrijdselectie | Automatisch op datum (laatste N wedstrijden) |
| Chatbot / verdieping | Niet in V1 — gepland voor V2 |
| Spelersprofielen | Optioneel in V1 (F-08), niet verplicht |
| UI-framework | Streamlit (`app.py`) |

---

## Open besluiten met architectuurimpact

| # | Besluit | Impact |
|---|---|---|
| OB-03 | Methode tabel→tekst conversie | Bepaalt datadichtheid en LLM-inputkwaliteit; vroeg prototypen aanbevolen |
| OB-04 | Waarde van N (wedstrijdselectie) | Bepaalt drempel voor dekkingindicatoren; configureerbaar maken |
| OB-05 | Visualisatieformaat in rapport | Bepaalt hoe grafieken worden gegenereerd en in PDF worden opgenomen |
| OB-01 | Retentiebeleid gegenereerde rapporten | Bepaalt of en hoe rapporten worden opgeslagen na generatie |
| OB-02 | Logging LLM-prompts en -outputs | Bepaalt audit trail en foutopsporingsmogelijkheden |

---

## Bekende beperkingen (V1)

- Geen parallelle analyses voor meerdere tegenstanders
- Geen historisch overzicht van eerder gegenereerde analyses
- Geen authenticatie of rolgebaseerde toegangscontrole
- Sessiemapping is in-memory — verlies bij herstart of crash vereist herstart van de analyse
- PDF-rendering is nog niet gevalideerd voor alle visualisatieformaten
