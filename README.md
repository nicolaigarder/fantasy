# Fyntasy League – overblik

Hjemmeside med stilling, pointudvikling og bødekasse for vores FPL Draft-liga (liga 29277).
Data hentes automatisk fra `draft.premierleague.com/api` hver time af en GitHub Action.

## Sådan sætter du den op (én gang)

1. Opret et nyt **public** repo på GitHub, fx `fantasy`.
2. Upload alle filerne i denne mappe (inkl. den skjulte mappe `.github/`).
   - Uploader du via github.com og kommer `.github` ikke med: vælg *Add file → Create new file*,
     skriv navnet `.github/workflows/update.yml` og indsæt indholdet fra filen.
3. **Settings → Actions → General → Workflow permissions** → vælg *Read and write permissions* → Save.
4. **Settings → Pages** → *Deploy from a branch* → `main` / `(root)` → Save.
5. **Actions → Opdater fantasy-data → Run workflow** for at hente data første gang.

Siden ligger derefter på `https://nicolaigarder.github.io/fantasy/`.

## Det du selv skal opdatere

**Betalinger** – `data/payments.json`: skriv de gameweeks hver person har betalt bøde for.
Rediger direkte på github.com (blyant-ikonet) – siden opdaterer sig selv efter ca. et minut.

```json
"Kaj": [1, 2, 3, 4, 5, 6, 7, 8]
```

**Kælenavne / bødesatser** – `config.json`.

## Filer

| Fil | Hvad |
|---|---|
| `index.html` | Selve siden |
| `config.json` | Liga-ID, kælenavne (entry-ID → navn), bødesatser |
| `data/league.json` | Data fra FPL – skrives automatisk, rør den ikke |
| `data/payments.json` | Hvem har betalt for hvilke gameweeks |
| `scripts/fetch_data.py` | Henter data fra API'et |
| `.github/workflows/update.yml` | Kører scriptet hver time |

## API-endpoints der bruges

- `/api/game` – aktuel gameweek og om den er afsluttet
- `/api/bootstrap-static` – alle gameweeks
- `/api/league/29277/details` – hold, navne og stilling
- `/api/entry/{entry_id}/history` – point pr. gameweek pr. hold

Bøderegel (samme som Excel-arket): alle med laveste score betaler 30 kr. Har kun én laveste score,
betaler den/de med næstlaveste 20 kr. Kun afsluttede gameweeks tæller.
