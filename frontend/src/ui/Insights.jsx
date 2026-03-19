export default function Insights({items}) {

  // Default mock items if none provided
  const displayItems = items && items.length > 0 ? items : [
    "No insights currently available based on the selected filters."
  ];

  const colors = ["red", "pink", "orange"];
  const colorHexes = ["#dc2626", "#db2777", "#ea580c"];
  const bgColors = ["#fce7f3", "#fce7f3", "#ffedd5"];
  const textColors = ["#e11d48", "#e11d48", "#f59e0b"];

  return (
    <div className="insights-panel panel" style={{ padding: '24px' }}>
      <div className="panel-header" style={{ marginBottom: '24px', paddingBottom: 0, borderBottom: 'none' }}>
        <h3 style={{ fontSize: '1.35rem' }}>Today's Key Insights</h3>
        {displayItems.length > 0 && items && items.length > 0 && (
           <span className="critical-count" style={{backgroundColor: '#fce7f3', color: '#e11d48', border: '1px solid #fbcfe8', borderRadius: '16px', padding: '4px 12px', fontWeight: 500}}>{displayItems.length} Insight{displayItems.length > 1 ? 's' : ''}</span>
        )}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
        {displayItems.map((insight, index) => {
          // If the backend insight is plain string:
          const text = typeof insight === 'string' ? insight : insight.message || insight.text || 'Insight';
          const title = typeof insight === 'string' ? `Insight ${index + 1}` : `${insight.product || 'System'} ${insight.impact ? '- ' + insight.impact : 'Update'}`;
          
          return (
            <div key={index} className={`insight-card ${colors[index % colors.length]}`}>
              <div className="insight-card-header" style={{ marginBottom: "12px" }}>
                <span className="insight-title" style={{ fontSize: '1.05rem' }}>{title}</span>
                <span className="insight-tag" style={{backgroundColor: bgColors[index % bgColors.length], color: textColors[index % textColors.length], border: 'none', padding: '4px 10px', borderRadius: '12px', fontWeight: 600}}>
                  Automated
                </span>
              </div>
              
              <div className="insight-desc" style={{ fontSize: '0.95rem', lineHeight: '1.5', marginBottom: '16px' }}>
                {text}
              </div>
              
            </div>
          );
        })}
      </div>
    </div>
  )
}
