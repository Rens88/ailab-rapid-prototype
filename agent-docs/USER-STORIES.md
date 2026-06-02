# User Stories — Baseline
**KNLTB — Nationaal Tennis Centrum**
Versie 1.0 — 15 mei 2026

---

## Actoren

| Actor | Omschrijving |
|---|---|
| **Stafmedewerker** | Primaire gebruiker. Omvat alle rollen op het NTC: tenniscoach, S&C-coach, bondsarts, fysio, sport scientist, expert prestatiegedrag, expert voeding, data scientist, stagiaires en de KNLTB-buddy. Werkt op laptop/desktop (kantoor, vergadering) én smartphone (onderweg, op de baan). Medium tech-niveau: comfortabel met spreadsheets en basistools. Raadpleegt het dashboard in sessies van 1–3 minuten. |
| **Topsportmanager** | Eindverantwoordelijke en beslisser. Heeft volledig overzicht nodig over alle groepen, staf en banen. Raadpleegt het dashboard voor strategische afstemming en voortgangsbewaking. |
| **Systeem (Baseline)** | Het dashboard zelf als actor in automatische processen: data ophalen, verversing signaleren, yellow flags tonen. |

---

## Epicoverzicht

| Epic | Omschrijving | Stories |
|---|---|---|
| E-01 | Gecombineerde weekweergave | US-01, US-02 |
| E-02 | Groepsplanning dashboard | US-03, US-04 |
| E-03 | Aanwezigheid staf & spelers | US-05, US-06 |
| E-04 | Chatbox — planningsvragen | US-07, US-08, US-09 |
| E-05 | Datakwaliteit & transparantie | US-10, US-11 |
| E-06 | Toegang & authenticatie | US-12 |

---

## E-01 — Gecombineerde weekweergave

### US-01 — Startscherm met gecombineerde weekweergave
```
Als stafmedewerker
wil ik bij het openen van Baseline direct een gecombineerde weekweergave zien
van de groepsplanning, aanwezigheid staf/spelers én het baanschema NTC,
zodat ik in één oogopslag de situatie van deze week begrijp zonder door meerdere schermen te navigeren.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Openingsscherm — moet in < 3 seconden laden; gebruiker heeft 1–3 minuten

**Acceptatiecriteria:**
- [ ] Het startscherm toont alle drie de dashboards (groepsplanning, aanwezigheid, baanschema) zichtbaar na het inloggen, zonder extra klik
- [ ] Het startscherm laadt volledig binnen 3 seconden op een standaard kantoorverbinding
- [ ] De huidige week is standaard geselecteerd bij het openen
- [ ] Het startscherm is volledig bruikbaar op desktop (≥ 1280px) én smartphone (≤ 390px)
- [ ] Een tijdstempel toont wanneer de data voor het laatst succesvol is gesynchroniseerd

---

### US-02 — Navigeren naar vorige en volgende week
```
Als stafmedewerker
wil ik vanuit het startscherm eenvoudig naar de vorige of volgende week kunnen navigeren,
zodat ik snel kan controleren wat er komende week gepland staat of terugkijken op vorige week.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Snelle navigatie — maximaal 2 klikken om 2 weken vooruit/achteruit te gaan

**Acceptatiecriteria:**
- [ ] Navigatiepijlen (vorige week / volgende week) zijn zichtbaar op het startscherm
- [ ] Na klik op een navigatiepijl laadt de nieuwe weekweergave binnen 3 seconden
- [ ] De geselecteerde week is duidelijk zichtbaar (weeknummer + datumrange)
- [ ] Er is een "terug naar huidige week"-knop beschikbaar

---

## E-02 — Groepsplanning dashboard

### US-03 — Overzicht groepsplanning per week bekijken
```
Als stafmedewerker
wil ik per week de planningen zien van Groep 1, 2, 3, 4 en Rolstoeltennis,
inclusief toernooien, events, testdagen, bijeenkomsten en vakanties,
zodat ik weet wat er per groep gepland staat en ik mijn eigen agenda daarop kan afstemmen.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker, Topsportmanager
**Context / tijdsbudget:** Onderdeel van gecombineerde weekweergave; ook als zelfstandig tabblad/sectie beschikbaar

**Acceptatiecriteria:**
- [ ] Alle vijf groepen (Groep 1, 2, 3, 4, Rolstoeltennis) zijn zichtbaar in de planningsweergave
- [ ] Per groep worden de volgende typen activiteiten onderscheiden: toernooi, event, testdag, bijeenkomst, vakantie/vrij
- [ ] Activiteiten zijn kleurgecodeerd per type
- [ ] Groepen zonder ingevulde planning voor de geselecteerde week tonen een gele vlag
- [ ] De weergave is filterbaar op groep (één of meerdere groepen selecteerbaar)

---

### US-04 — Filteren op specifieke groep
```
Als stafmedewerker die verantwoordelijk is voor één groep
wil ik de weergave kunnen filteren op mijn eigen groep,
zodat ik niet afgeleid word door planningen van andere groepen.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Filter instelbaar in < 2 klikken; instelling blijft actief tijdens de sessie

**Acceptatiecriteria:**
- [ ] Een filtercomponent laat toe om één of meerdere groepen te selecteren
- [ ] Filterinstelling blijft actief bij navigatie tussen weken
- [ ] Een "toon alle groepen"-optie reset de filter snel
- [ ] Het actieve filter is altijd zichtbaar in de interface

---

## E-03 — Aanwezigheid staf & spelers

### US-05 — Aanwezigheidsoverzicht staf en spelers per week
```
Als stafmedewerker
wil ik per week zien wie van de staf en welke spelers aanwezig zijn op het NTC en wie extern is (toernooi, vrij, ziek),
zodat ik weet met wie ik die week kan samenwerken en geen afspraken plan met mensen die er niet zijn.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker, Topsportmanager
**Context / tijdsbudget:** Onderdeel gecombineerde weekweergave; snel scanbaar op weekniveau

**Acceptatiecriteria:**
- [ ] Per week toont het dashboard voor elk staflid en elke speler: aanwezig NTC / extern / onbekend
- [ ] Staf en spelers zijn gescheiden weergegeven in het overzicht
- [ ] "Onbekend / niet ingevuld" is zichtbaar als gele vlag per persoon
- [ ] De weergave is filterbaar op staflid of speler (zoek op naam)

---

### US-06 — Drill-down naar individueel staflid of speler
```
Als stafmedewerker
wil ik op een individueel staflid of speler kunnen klikken om hun volledige weekplanning te zien,
zodat ik snel kan controleren wanneer iemand beschikbaar is over een langere periode.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Drill-down opent in < 2 seconden; gebruiker scant 2–4 weken vooruit

**Acceptatiecriteria:**
- [ ] Klikken op een naam opent een detailweergave van die persoon
- [ ] De detailweergave toont de aanwezigheid van de geselecteerde persoon voor minimaal 4 weken (huidige + 3 toekomstige)
- [ ] De detailweergave is ook bereikbaar via de chatbox ("Toon de planning van [naam]")
- [ ] Terugnavigeren naar het overzicht is mogelijk met één klik of gebaar

---

## E-04 — Chatbox: planningsvragen

### US-07 — Eenvoudige planningsvraag stellen
```
Als stafmedewerker
wil ik in de chatbox een vraag kunnen typen over de planningsdata,
zodat ik snel een antwoord krijg zonder zelf door filters en weergaven te hoeven navigeren.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Vraag stellen en antwoord lezen in < 30 seconden; bruikbaar op smartphone

**Acceptatiecriteria:**
- [ ] Er is een chatbox-invoerveld beschikbaar op elke dashboardpagina (of als persistent element)
- [ ] De chatbox beantwoordt vragen over groepsplanning en aanwezigheid staf/spelers
- [ ] Het antwoord verschijnt binnen 5 seconden na het insturen van de vraag
- [ ] De chatbox werkt volledig op smartphone (invoer via touchtoetsenbord, antwoord leesbaar zonder zoomen)

---

### US-08 — Antwoord op aanwezigheidsvraag
```
Als stafmedewerker
wil ik kunnen vragen "Wie is er volgende week dinsdag aanwezig op het NTC?"
en een direct antwoord krijgen op basis van de actuele aanwezigheidsdata,
zodat ik snel kan plannen zonder het aanwezigheidsoverzicht handmatig te doorzoeken.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** 1–2 vragen per sessie; antwoord in < 5 seconden

**Acceptatiecriteria:**
- [ ] De chatbox begrijpt aanwezigheidsvragen in gewone Nederlandse taal
- [ ] Het antwoord noemt namen van aanwezige stafleden/spelers voor de gevraagde dag
- [ ] Als de aanwezigheidsdata voor die dag niet (volledig) is ingevuld, meldt de chatbox dit expliciet
- [ ] Het antwoord verwijst niet naar informatie buiten de groepsplanning en aanwezigheidsdata

---

### US-09 — Chatbox weigert vragen buiten de planningsdomeinen
```
Als stafmedewerker
wil ik een duidelijke melding zien als ik een vraag stel die de chatbox niet kan beantwoorden,
zodat ik weet dat ik de vraag ergens anders moet stellen en ik geen onbetrouwbaar antwoord krijg.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Foutmelding verschijnt direct; gebruiker begrijpt meteen waarom

**Acceptatiecriteria:**
- [ ] Als een vraag buiten de drie planningsdomeinen valt, antwoordt de chatbox met een begrijpelijke weigering (bijv. "Dit valt buiten wat ik kan opzoeken — ik kan alleen vragen beantwoorden over de groepsplanning, aanwezigheid en het baanschema.")
- [ ] De chatbox verzint nooit een antwoord als de data ontbreekt of onvolledig is
- [ ] Bij ontbrekende data geeft de chatbox aan welke data mist en voor welke periode

---

## E-05 — Datakwaliteit & transparantie

### US-10 — Gele vlag voor ontbrekende of verouderde data
```
Als stafmedewerker
wil ik direct zien welke groepen, personen of banen hun data niet hebben ingevuld of al lang niet hebben bijgewerkt,
zodat ik weet welk deel van het overzicht onbetrouwbaar is en waar actie nodig is.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker, Topsportmanager
**Context / tijdsbudget:** Zichtbaar in de gecombineerde weekweergave zonder extra klik

**Acceptatiecriteria:**
- [ ] Elke datasectie (groepsplanning per groep, aanwezigheid per persoon, baanschema) toont een gele vlag als de data ontbreekt of ouder is dan de geconfigureerde drempelwaarde (zie OB-06)
- [ ] De gele vlag toont bij aanwijzen/klikken een tooltip of bericht met een uitleg ("Geen data beschikbaar" of "Laatst bijgewerkt op [datum]")
- [ ] Gele vlaggen verdwijnen automatisch zodra de brondata is bijgewerkt en opgehaald

---

### US-11 — Tijdstempel laatste datasync zichtbaar
```
Als stafmedewerker
wil ik altijd kunnen zien wanneer de data in Baseline voor het laast is vernieuwd,
zodat ik weet of ik naar de meest actuele situatie kijk.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker
**Context / tijdsbudget:** Altijd zichtbaar, geen klik vereist

**Acceptatiecriteria:**
- [ ] Een tijdstempel ("Laatste update: [datum en tijd]") is zichtbaar op elke dashboardpagina
- [ ] Als de Graph API-verbinding meer dan X minuten geleden voor het laast succesvol was, verandert het tijdstempel naar een waarschuwing (rood of oranje)
- [ ] De tijdstempel wordt automatisch bijgewerkt na een succesvolle datasync

---

## E-06 — Toegang & authenticatie

### US-12 — Inloggen met KNLTB-Microsoft account
```
Als stafmedewerker of topsportmanager
wil ik inloggen op Baseline met mijn bestaande KNLTB-Microsoft account,
zodat ik geen apart wachtwoord hoef te onthouden en de toegang beheerd wordt via het bestaande KNLTB-IT-beleid.
```

**Prioriteit:** Must-have (MVP)
**Primaire actor:** Stafmedewerker, Topsportmanager
**Context / tijdsbudget:** Inloggen via Azure AD SSO — maximaal 2 klikken voor een gebruiker die al ingelogd is op hun Microsoft-account

**Acceptatiecriteria:**
- [ ] Baseline gebruikt Azure AD SSO via de bestaande KNLTB Microsoft-tenant
- [ ] Een gebruiker die al ingelogd is op hun Microsoft-account wordt automatisch herkend (single sign-on)
- [ ] Gebruikers zonder KNLTB-Microsoft account kunnen niet inloggen
- [ ] Na een inactieve sessie van [X uur] wordt de gebruiker opnieuw gevraagd in te loggen (time-out conform KNLTB IT-beleid)

---

## Prioriteitenmatrix

| Story | Epic | Prioriteit | MVP? |
|---|---|---|---|
| US-01 | E-01 Gecombineerde weekweergave | Must-have | ✅ |
| US-02 | E-01 Gecombineerde weekweergave | Must-have | ✅ |
| US-03 | E-02 Groepsplanning | Must-have | ✅ |
| US-04 | E-02 Groepsplanning | Must-have | ✅ |
| US-05 | E-03 Aanwezigheid | Must-have | ✅ |
| US-06 | E-03 Aanwezigheid | Must-have | ✅ |
| US-07 | E-04 Chatbox | Must-have | ✅ |
| US-08 | E-04 Chatbox | Must-have | ✅ |
| US-09 | E-04 Chatbox | Must-have | ✅ |
| US-10 | E-05 Datakwaliteit | Must-have | ✅ |
| US-11 | E-05 Datakwaliteit | Must-have | ✅ |
| US-12 | E-06 Authenticatie | Must-have | ✅ |
