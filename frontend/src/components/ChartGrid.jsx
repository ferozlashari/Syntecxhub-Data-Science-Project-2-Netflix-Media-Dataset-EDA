import { chartUrl } from "../api/client";

export default function ChartGrid({ filenames }) {
  return (
    <div className="chart-grid">
      {filenames.map((name) => (
        <img key={name} src={`${chartUrl(name)}?t=${Date.now()}`} alt={name} />
      ))}
    </div>
  );
}
