# Fahrpreisrechner (DB-Regeln) — QS-Projekt (Blackbox-Tests & CI/CD)

Dieses Repository enthält einen **Fahrpreisrechner** (DB-inspiriert), der den Ticket-Endpreis auf Basis von:
- **Distanz** in km (`distance_km`)
- **Alter** in Jahren (`age`)
- **BahnCard** (`bahncard` ∈ {0, 25, 50})

berechnet.

Der Fokus liegt auf **Qualitätssicherung (QS)**: Anforderungen → Testdesign (EK/GW) → automatisierte Tests im CI → Merge nur bei grün.

---

## Projektziele

### Fachliches Ziel
Implementierung einer Python-Funktion:

`compute_fare(distance_km, age, bahncard)`

Sie liefert den Endpreis (Euro) oder wirft bei ungültigen Eingaben einen Fehler.

### QS-Ziel (Qualitätssicherung)
Nachweis, dass die Anforderungen **vor dem Merge in `main`** abgesichert werden durch:
- Ableitung von Testfällen direkt aus den Anforderungen
- Blackbox-Testdesign mit **Äquivalenzklassenbildung (EK)** und **Grenzwertanalyse (GW)**
- **automatisierte Testausführung über CI (GitHub Actions)** bei jedem `push` und jeder `pull_request`
- **Merge-Blockierung** via Branch Protection (Quality Gate), falls Checks fehlschlagen

> Kernaussage: **Qualität wird automatisiert vor der Integration überprüft.**

---

## Geschäftsregeln (Kurzfassung)

### R1 Distanz (degressiver Tarif)
- ungültig: `distance_km < 1`
- 1–50 km (Kurz): `5.00 + 0.20 * km`
- 51–200 km (Mittel): `8.00 + 0.14 * km`
- >200 km (Lang): `12.00 + 0.09 * km`

### R2 Alter (Altersrabatt)
- ungültig: `age < 0` oder `age > 120`
- 0–5: 100% Rabatt (gratis)
- 6–14: 50% Rabatt
- 15–64: 0% Rabatt
- 65–120: 25% Rabatt

### R3 BahnCard (zusätzlicher Rabatt)
- 0 → 0%
- 25 → 25%
- 50 → 50%
- sonst ungültig

### Endformel
`Preis = (Grundpreis + km * Preis/km) * (1 - Altersrabatt) * (1 - BahnCard-Rabatt)`

---

## Teststrategie (Blackbox)

### Äquivalenzklassen (EK)
Partitionierung des Eingaberaums in Klassen mit gleichem Verhalten.  
→ **13 EK-Testfälle** (Distanz, Alter, BahnCard inkl. ungültige Klassen)

### Grenzwertanalyse (GW)
Tests an Übergängen zwischen Klassen (typische Fehler: `<` statt `<=`).  
→ **16 GW-Testfälle**:
- Distanz: 0/1, 50/51, 200/201
- Alter: -1/0, 5/6, 14/15, 64/65, 120/121

Die konkreten Testfälle inkl. Erwartungswerten (Oracles) sind in `docs/Projekt_Q.tex` dokumentiert.

---

## Repository-Struktur (empfohlen)
