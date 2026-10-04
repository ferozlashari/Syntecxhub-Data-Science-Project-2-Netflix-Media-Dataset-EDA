import { useEffect, useState } from "react";
import { fetchNetflixAnalysis, refreshNetflixAnalysis } from "./api/client";
import ChartGrid from "./components/ChartGrid";
import TopTenList from "./components/TopTenList";
import Loader from "./components/Loader";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const load = async (fn) => {
    try {
      setError(null);
      const result = await fn();
      setData(result);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    setLoading(true);
    load(fetchNetflixAnalysis).finally(() => setLoading(false));
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    await load(refreshNetflixAnalysis);
    setRefreshing(false);
  };

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="logo-mark">S</span>
          <div>
            <div className="brand-title">SYNTECXHUB</div>
            <div className="brand-sub">CREATE | THINK | SOLVE</div>
          </div>
        </div>
        <div className="header-text">
          <h1>Data Science — Project 2</h1>
          <p>Netflix / Media Dataset EDA, served live from a FastAPI backend</p>
        </div>
      </header>

      <main>
        {loading && <Loader message="Running EDA on the backend…" />}
        {error && <div className="error-box">Failed to load: {error}</div>}

        {data && (
          <>
            <div className="panel-header">
              <div className="meta-row">
                {data.row_count.toLocaleString()} titles in catalog
              </div>
              <button className="refresh-btn" onClick={handleRefresh} disabled={refreshing}>
                {refreshing ? "Regenerating…" : "↻ Regenerate data"}
              </button>
            </div>

            <ChartGrid filenames={data.charts} />

            <div className="top10-grid">
              <TopTenList title="Top 10 Genres" data={data.top_10_genres} />
              <TopTenList title="Top 10 Release Years" data={data.top_10_years} />
              <TopTenList title="Top 10 Countries" data={data.top_10_countries} />
            </div>

            <div className="insight-box">
              <h3>Visual Report Summary</h3>
              <p>{data.summary}</p>
            </div>
          </>
        )}
      </main>

      <footer>
        <p>Backend: FastAPI + pandas + matplotlib/seaborn &nbsp;|&nbsp; Frontend: React + Vite</p>
      </footer>
    </div>
  );
}
