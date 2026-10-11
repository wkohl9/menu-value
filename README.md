# Menu Value

The goal of this project is to compare a dish's price with similar dishes nearby. Give the app a picture of the restaurant's menu, and for every dish it tells you whether the price is good
value, typical, or pricey compared with comparable dishes in the same neighborhood (or citywide when the neighborhood is thin on data).

## How it works

```
menu photo / text
      │
      ▼
 ocr.py ──► parse.py ──► categorize.py ──► pricing.py ──► JSON to the website
 (week 4)   lines→dishes   dish→category    vs. similar dishes nearby
```

| Folder | What's in it |
|---|---|
| `backend/` | Python API (FastAPI). All the parsing, categorizing and pricing. |
| `backend/app/pipeline/` | One file per pipeline step. Start reading at `analyze.py`. |
| `backend/tests/` | Tests. Skipped tests are your TODOs. |
| `frontend/` | React website (Vite). Calls the backend through `src/api.js`. |
| `data/` | `menus.csv` = your real data. `sample_menus.csv` = synthetic placeholder. |
| `scripts/` | Helper scripts (regenerating sample data, later your collectors). |

## Run it locally

You need Python 3.11+ and Node.js 20+.

**Terminal 1 - backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate       
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs to try the API directly.

## Tests

```bash
cd backend && pytest         
cd frontend && npm run lint  
```

## Finding your work

Every task left for you is marked in the code:

```bash
grep -rn "TODO (week" backend
```

Skipped tests (`@pytest.mark.skip`) describe the behavior you're building -
remove the skip, watch it fail, make it pass.

## Data

- `data/menus.csv` - **real** menus you collect. As soon as it has rows, the
  app uses it instead of the sample set automatically.
- `data/sample_menus.csv` - **synthetic** prices from
  `scripts/make_sample_data.py`, so the app works on day one. Every response
  says `using_sample_data: true` while it's in use, and the website shows a
  notice.

Collect menus from restaurants' own websites or by photographing physical
menus. Avoid scraping delivery apps: it usually breaks their terms, and their
prices are often marked up over in-store prices.
