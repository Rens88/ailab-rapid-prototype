# Example Data

This folder contains synthetic example data. All data is fictitious — generated for demo and development purposes only. No real athletes, no real measurements. This folder is tracked by git and must be treated as fully public.

---

## Files

### trainingsschema_KNSB_2526.csv

38 planned training sessions, seizoen 2025–2026.

| Kolom | Beschrijving |
| --- | --- |
| sessie_id | Uniek ID (S001–S038) |
| datum | ISO 8601 (YYYY-MM-DD) |
| trainingstype | relay / individueel / techniek / uithoudingsvermogen |
| geplande_intensiteit | zwaar / medium / licht |

---

### kinexon_export_2526.csv

External load data (Kinexon device). 29 of 38 sessions measured (76% coverage).

Coverage per trainingstype: relay 89%, individueel 64%, techniek 60%, uithoudingsvermogen 75%.

| Kolom | Beschrijving |
| --- | --- |
| sessie_id | Matches trainingsschema |
| sporterId | SPORTER_01 – SPORTER_06 (geanonimiseerd) |
| datum | ISO 8601 |
| trainingstype | relay / individueel / techniek / uithoudingsvermogen |
| geplande_intensiteit | zwaar / medium / licht |
| player_load | Totale mechanische belasting (arbitrary units) |
| acceleratiecount | Aantal acceleraties boven drempelwaarde |
| afstand_per_minuut_m | Gemiddelde rijafstand per trainingsminuut (m/min) |
| max_snelheid_kmh | Gemeten topsnelheid per sessie (km/h) |
| sprint_intensiteit_pct | % van sessietijd boven 85% maximale snelheid |

---

### rpe_vragenlijsten_2526.csv

Internal load data (RPE questionnaire). 38 sessions × 6 athletes = 228 entries; 3 missing (athletes did not complete).

| Kolom | Beschrijving |
| --- | --- |
| sessie_id | Matches trainingsschema |
| sporterId | SPORTER_01 – SPORTER_06 |
| datum | ISO 8601 |
| trainingstype | relay / individueel / techniek / uithoudingsvermogen |
| geplande_intensiteit | zwaar / medium / licht |
| rpe_score | Rate of Perceived Exertion (1–10 Borg-schaal) |
| sessieduur_min | Sessieduur in minuten |
| srpe | Sessie-RPE = rpe_score × sessieduur_min (Foster et al.) |

---

### hartslagdata_2526.csv

Internal load via heart rate monitor. 38 sessions × 6 athletes; 6 sessions missing due to HR monitor not worn.

| Kolom | Beschrijving |
| --- | --- |
| sessie_id | Matches trainingsschema |
| sporterId | SPORTER_01 – SPORTER_06 |
| datum | ISO 8601 |
| trainingstype | relay / individueel / techniek / uithoudingsvermogen |
| geplande_intensiteit | zwaar / medium / licht |
| gem_hartslag_bpm | Gemiddelde hartslag over de sessie (bpm) |
| max_hartslag_bpm | Maximale hartslag in de sessie (bpm) |
| tijd_zone4_min | Minuten in hartslagzone 4 (80–89% HRmax) |
| tijd_zone5_min | Minuten in hartslagzone 5 (≥90% HRmax) |

---

## Koppeling

Bestanden koppelen op: `sessie_id` + `sporterId`. Datum is redundant maar bruikbaar als validatiecheck. Sessies in trainingsschema zonder Kinexon-meting zijn de ontbrekende rijen in kinexon_export_2526.csv.

## Noot over correlaties

In deze synthetische dataset is de overall PlayerLoad–RPE correlatie r ≈ 0.88, hoger dan in echte trainingsdata (typisch r ≈ 0.65–0.75). Dit komt doordat de drie intensiteitsniveaus (zwaar/medium/licht) in de synthetische data schoner gescheiden zijn dan in de praktijk. De Phase 1 prototype-interface toont r = 0.71 als indicatie voor realistischere ruwe data.
