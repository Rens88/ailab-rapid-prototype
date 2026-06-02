# Rapport: AI Casus Canvas - LA-agent WSV
**Sportinnovator AI Impact Lab**

|  |  |
| ------ | ------ |
| **Project / Casus** | LA-agent WSV |
| **Organisatie** | Sailing Innovation Centre Den Haag |
| **Datum** | 28 mei 2026 |

---

## 1. GEBRUIKERSPROFIEL

**Gebruiker & Context**
Het project speelt binnen de topsport in de watersport (zoals zeilen of roeien), waar factoren zoals wind, water en weer een grote invloed hebben op prestaties [1]. De eindgebruikers zijn topsportcoaches binnen het Watersportverbond (WSV) [1]. Zij gaan dit systeem gebruiken om alle informatie rondom de Olympische locatie in Los Angeles op te slaan en snel te kunnen reproduceren [1].

**Taken & Doelen**
De gebruiker wil beter onderbouwde inzichten verkrijgen in wedstrijdlocaties [2]. Dit gebeurt nu vaak op basis van niet-gedeelde persoonlijke ervaring [2]. Het doel is om vóór juli 2026 een prototype te hebben dat gecombineerde kennis gebruikt voor een eerste locatie-analyse, resulterend in een onderbouwd en praktisch advies [3].

**Huidig Proces**
Locatie-analyses worden nu gedaan op basis van intuïtie, notities en eerdere observaties [3]. De tools zijn beperkt en versnipperd (weerapps, losse data) en er is geen centraal systeem waarin data en expertise samenkomen [4].

**Pijnpunten & Frustraties**
Waardevolle kennis over wedstrijdlocaties raakt verspreid en is niet systematisch vastgelegd, waardoor belangrijke ervaring verloren gaat [4]. Beslissingen worden genomen op basis van persoonlijke intuïtie en beperkte datasets [5]. Daarnaast willen coaches niet alle tactieken delen vanwege concurrentie binnen de bond [6].

---

## 2. AI & WAARDEAANBOD

**AI-mogelijkheden**
AI combineert data en ervaringskennis tot praktische adviezen. Er wordt een bot ontwikkeld met *speech-to-text* functionaliteit, waarmee coaches observaties inspreken [6]. Analyserende AI herkent patronen in de data, terwijl generatieve AI zorgt voor duidelijke, onderbouwde adviezen [7].

**Databronnen**
Externe bronnen zijn weer- en waterdata rondom Los Angeles [7]. Dit wordt aangevuld met speech-to-text observaties van coaches [7].

**Datakwaliteit & -beheer**
- **Kwaliteit:** Data van lokale weerstations is momenteel voldoende; dit wordt later in LA aangevuld met coachboten met windpalen. 
- **Eigenaarschap:** De bond is eigenaar van het concept. Coaches blijven eigenaar van hun data, maar moeten data aanleveren om het systeem te mogen gebruiken.
- **Techniek:** Het speech-to-text systeem moet specifiek zeiljargon en terminologie foutloos herkennen en in staat zijn om sprekers te onderscheiden in teammeetings.

**Product / Dienst (MVP)**
- **Wat bouwen we:** Een web- of tablet-app voor gebruik aan wal. Coaches kunnen data laagdrempelig invoeren via een spraakbericht naar een centraal WhatsApp-nummer van het SIC.
- **Eerste versie:** Een vraag-en-antwoord app. De coach vraagt een situatie uit (bijv. *"Ik ben klasse X, vaar straks op baan Y en zie nu Z... Wat kan ik verwachten?"*) en krijgt direct waardevol advies.
- **Workflow:** De app wordt voorafgaand aan de race (avond of ochtend) gebruikt, niet op het water.

**Waardecreatie**
- **Concrete verbetering:** Voorkomt het verlies van waardevolle kennis. De kwaliteit van locatiekennis neemt drastisch toe, wat essentieel is voor detailwerk in LA.
- **Superkracht:** In een handomdraai advies krijgen van een bot op basis van gecombineerde locatiekennis, zonder zelf urenlang logboeken te hoeven doorzoeken.

---

## 3. IMPLEMENTATIE & HAALBAARHEID

**Ethiek & Privacy**
- Er worden geen persoonsgegevens opgeslagen, maar de data is zeer strategisch richting de Spelen van 2028. Toegang is strikt beperkt via een WSV-inlog. 
- **Informed Consent:** Coaches tekenen een overeenkomst waarin staat dat data niet met externe landen gedeeld mag worden. Om geheime tactieken af te schermen, is dit gekoppeld aan een boeteclausule bij schending.

**Kritische Aannames**
- De grootste aanname is dat de *speech-to-text* technologie het complexe zeiljargon accuraat verstaat. 
- Sprekerherkenning in teammeetings is essentieel om input aan de juiste persoon of zeilklasse te kunnen labelen.

**Succes-metrics**
- Het MVP is in juli 2026 een succes wanneer coaches daadwerkelijk berichten inspreken en kwalitatieve feedback geven dat de app waardevolle inzichten oplevert. 
- Het SIC-team moet de gegenereerde output intern eerst met succes kunnen valideren.

**Tijdlijn & Team**
- **Rollen:** Een expert voor de speech-to-text implementatie, Yazemin voor de opslag in de eigen Azure-database, en inrichting van een centraal WhatsApp-telefoonnummer bij het SIC.
- **Eerste stappen:** Voorbeeld-voiceberichten verzamelen en testen, input ophalen rondom het zeiljargon, en bepalen of coaches een vaste spreekstructuur moeten aanhouden.

--------------------------------------------------------------------------------
2. Markdown (.md) voor het Slide Deck
# Slide Deck: AI Casus Canvas - LA-agent WSV

## Slide 1: Introductie & Gebruikersprofiel
* **Project:** LA-agent WSV (Sailing Innovation Centre)
* **Doelgroep:** Topsportcoaches binnen het Watersportverbond (WSV).
* **Doel:** Voor juli 2026 een prototype (bot) ontwikkelen dat locatiekennis combineert voor onderbouwde locatie-analyses richting de Olympische Spelen in Los Angeles.
* **Probleem:** Kennis zit in hoofden van coaches of losse notities. Versnippering van data, verlies van inzicht en interne concurrentie belemmeren kennisdeling.

---

## Slide 2: AI & Waardepropositie
* **De Oplossing (MVP):** Een web/tablet-app (aan wal) die acteert als bot.
* **Functionaliteit:** Coaches sturen spraakberichten (bijv. via WhatsApp) naar het SIC. De AI zet dit om in tekst en combineert dit met actuele weer- en waterdata.
* **Vraag & Antwoord:** Coaches vragen de bot om situatie-specifiek advies ("Ik ben klasse X, vaar op baan Y..."). 
* **Superkracht:** In een handomdraai waardevolle, gebundelde inzichten ophalen zonder handmatig logboeken door te zoeken. 

---

## Slide 3: Databeheer, Kwaliteit & Privacy
* **Databronnen:** Weer/wind-data van lokale stations en coachboten (windpalen), gecombineerd met ervaringsdata van coaches.
* **Eigenaarschap:** Coaches blijven eigenaar van hun data, maar aanleveren is verplicht om toegang tot het platform te krijgen.
* **Privacy & Concurrentie:** Om tactieken af te schermen geldt een verplicht *informed consent* (geen externe deling) met een boeteclausule. Toegang uitsluitend via WSV-login.

---

## Slide 4: Aannames, Metrics & Actieplan
* **Grootste aanname:** De speech-to-text software begrijpt het complexe zeiljargon en kan verschillende sprekers feilloos onderscheiden.
* **Succes (juli 2026):** Coaches sturen actief berichten in en leveren kwalitatieve feedback over de meerwaarde van de adviezen, na een eerste interne validatie door het SIC.
* **Team:** Speech-to-text expert, Azure-database expert (Yazemin), inrichting SIC-telefoonnummer.
* **Directe vervolgstap:** Voorbeeld-voiceberichten testen, jargon verzamelen en spreekstructuur voor coaches bepalen.