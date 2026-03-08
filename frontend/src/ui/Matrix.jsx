export default function Matrix({matrix}) {
  if (!matrix.length) return null;

  const stages = Object.keys(matrix[0]).filter(k => k !== "product");

  const getPillColor = (v) => {
    if (v >= 25) return "red";
    if (v >= 20) return "pink";
    if (v >= 10) return "yellow";
    return "green"; // < 10%
  };

  return (
    <div className="matrix-panel">
      <div className="matrix-header">
        <h3>Stage Drop-off Matrix</h3>
        <span style={{fontSize:'0.75rem', padding:'4px 10px', borderRadius:'12px', backgroundColor:'#fff7ed', color:'#ea580c', fontWeight: 600}}>
          1 Critical Stage
        </span>
      </div>
      <div className="matrix-subtitle">
        Drop rate at each onboarding stage per product · Click any cell to drill down
      </div>

      <table className="matrix-table">
        <thead>
          <tr>
            <th>Stage</th>
            {matrix.map((p, i) => (<th key={i}>{p.product}</th>))}
          </tr>
        </thead>
        <tbody>
          {stages.map(s => (
            <tr key={s}>
              <td>{s}</td>
              {matrix.map((p, i) => {
                const val = p[s];
                const colorClass = getPillColor(val);
                return (
                  <td key={i}>
                    <div className={`pill ${colorClass}`}>
                      {val}%
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="legend">
        <div className="legend-item">
          <div className="legend-dot green"></div> &lt;10% Healthy
        </div>
        <div className="legend-item">
          <div className="legend-dot yellow"></div> 10-20% Watch
        </div>
        <div className="legend-item">
          <div className="legend-dot pink"></div> 20%+ Critical
        </div>
        <div className="legend-item">
          <div className="legend-dot red"></div> 25%+ Severe
        </div>
      </div>
    </div>
  );
}
