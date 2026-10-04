# Syntecxhub Data Science — Project 2: Netflix / Media Dataset EDA

Full-stack implementation: **FastAPI** (Python) backend + **React/Vite**
frontend, talking over a JSON API.

The dataset is **synthetically generated offline** (no internet or Kaggle
download needed) but shaped exactly like the real Kaggle "Netflix Titles"
dataset — same columns (`show_id, type, title, country, date_added,
release_year, rating, duration, listed_in`) — with realistic patterns:
Movies outnumbering TV Shows ~70/30, accelerating catalog growth in recent
years, skewed genre popularity, and a normally-distributed movie runtime.
6,000 titles total. Swap in the real CSV later if you want — see "Using
real data" below.

## Project structure
```
netflix_eda/
├── backend/                       # FastAPI
│   ├── app/
│   │   ├── main.py                # app entrypoint, CORS, static mount
│   │   ├── routers/netflix.py     # /api/netflix/*
│   │   ├── analysis/netflix_analysis.py
│   │   └── data/
│   │       ├── generate_netflix.py
│   │       └── netflix_titles.csv
│   ├── static/charts/netflix/     # PNGs written at runtime
│   └── requirements.txt
└── frontend/                      # React + Vite
    ├── src/
    │   ├── App.jsx                 # single-page dashboard
    │   ├── components/             # ChartGrid, TopTenList, Loader
    │   ├── api/client.js           # fetch wrapper
    │   └── styles.css
    └── package.json
```

## Run the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs
The dataset CSV and chart PNGs are generated automatically on first request.

## Run the frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://127.0.0.1:5173 — Vite proxies `/api` and `/static` calls to the
FastAPI backend on port 8000 (see `vite.config.js`), so start the backend
first.

## API reference

| Route                               | Description                                |
|---------------------------------------|---------------------------------------------|
| `GET /api/netflix/analysis`           | Netflix EDA results (cached) as JSON         |
| `GET /api/netflix/analysis/refresh`   | Regenerate data + re-run the analysis        |
| `GET /api/health`                     | Health check                                 |
| `GET /static/charts/netflix/<file>`   | Chart PNGs                                   |

## What the analysis covers (`backend/app/analysis/netflix_analysis.py`)
- Counts by content type (Movie vs TV Show) — bar chart
- Titles released per year, last 15 years — line chart
- Cumulative catalog growth over time (by date added) — filled line chart
- Top 10 genres — horizontal bar chart
- Movie runtime distribution — histogram + KDE with median marker
- Top-10 lists: genres, release years, countries (returned as JSON, shown
  as ranked bar lists in the frontend)
- Auto-generated visual report summary explaining the chart-type choices

## Using real data instead
Drop a CSV with the same columns at `backend/app/data/netflix_titles.csv`
(matching the real Kaggle "Netflix Titles" schema) and everything
downstream keeps working unchanged — no code edits needed.

## Submission notes
- Push this `netflix_eda/` folder to GitHub as `Syntecxhub_Project_Name`
  per the brief (e.g. `Syntecxhub_Netflix_EDA`).
- Share your internship status on LinkedIn and mention **@Syntecxhub**.
- Submit via the official Submission Form within the given time.
