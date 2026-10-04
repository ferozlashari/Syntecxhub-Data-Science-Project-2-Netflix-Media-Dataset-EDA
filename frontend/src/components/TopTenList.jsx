export default function TopTenList({ title, data }) {
  const entries = Object.entries(data);
  const max = Math.max(...entries.map(([, v]) => v));

  return (
    <div className="top10-card">
      <h3>{title}</h3>
      <ol>
        {entries.map(([label, count]) => (
          <li key={label}>
            <span className="top10-label">{label}</span>
            <span className="top10-bar-wrap">
              <span
                className="top10-bar"
                style={{ width: `${(count / max) * 100}%` }}
              />
              <span className="top10-count">{count.toLocaleString()}</span>
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
}
