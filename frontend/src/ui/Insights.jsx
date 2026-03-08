export default function Insights({items}) {

  return (
    <div className="insights-panel panel" style={{ padding: '24px' }}>
      <div className="panel-header" style={{ marginBottom: '24px', paddingBottom: 0, borderBottom: 'none' }}>
        <h3 style={{ fontSize: '1.35rem', color: '#0f172a' }}>Today's Key Insights</h3>
        <span className="critical-count" style={{backgroundColor: '#fce7f3', color: '#e11d48', border: '1px solid #fbcfe8', borderRadius: '16px', padding: '4px 12px', fontWeight: 500}}>2 Critical</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
        
        {/* Card 1 */}
        <div className="insight-card red">
          <div className="insight-card-header">
            <span className="insight-title" style={{ fontSize: '1.05rem', color: '#0f172a' }}>Credit Card</span>
            <span className="insight-tag" style={{backgroundColor: '#fce7f3', color: '#e11d48', border: 'none', padding: '4px 10px', borderRadius: '12px', fontWeight: 600}}>
              Conversion Drop
            </span>
          </div>
          <div className="insight-value" style={{color: '#dc2626'}}>
            -6.2%
          </div>
          <div className="insight-desc" style={{ color: '#475569', fontSize: '0.875rem' }}>
            Drop concentrated at Video KYC stage · Android devices
          </div>
          <div className="insight-subtext" style={{ color: '#64748b' }}>
            ₹4.2 Cr at risk · West Zone primary · 8,420 users
          </div>
          <a href="#" className="insight-link" style={{color: '#2563eb'}}>View Details →</a>
        </div>

        {/* Card 2 */}
        <div className="insight-card pink">
          <div className="insight-card-header">
            <span className="insight-title" style={{ fontSize: '1.05rem', color: '#0f172a' }}>Video KYC</span>
            <span className="insight-tag" style={{backgroundColor: '#fce7f3', color: '#e11d48', border: 'none', padding: '4px 10px', borderRadius: '12px', fontWeight: 600}}>
              Failure Spike
            </span>
          </div>
          <div className="insight-value" style={{color: '#db2777'}}>
            14.8%
          </div>
          <div className="insight-desc" style={{ color: '#475569', fontSize: '0.875rem' }}>
            Agent unavailable + timeout errors · +18% since yesterday
          </div>
          <div className="insight-subtext" style={{ color: '#64748b' }}>
            8,420 users affected · Peak 11:30–12:15 PM
          </div>
          <a href="#" className="insight-link" style={{color: '#2563eb'}}>Explore Issue →</a>
        </div>

        {/* Card 3 */}
        <div className="insight-card orange">
          <div className="insight-card-header">
            <span className="insight-title" style={{ fontSize: '1.05rem', color: '#0f172a' }}>Personal Loan</span>
            <span className="insight-tag" style={{backgroundColor: '#ffedd5', color: '#f59e0b', border: 'none', padding: '4px 10px', borderRadius: '12px', fontWeight: 600}}>
              SLA Breach
            </span>
          </div>
          <div className="insight-value" style={{color: '#ea580c'}}>
            2,180
          </div>
          <div className="insight-desc" style={{ color: '#475569', fontSize: '0.875rem' }}>
            Cases delayed at Underwriting · Avg delay 6 hrs
          </div>
          <div className="insight-subtext" style={{ color: '#64748b' }}>
            South Zone · Manual review bottleneck
          </div>
          <a href="#" className="insight-link" style={{color: '#2563eb'}}>Check SLA →</a>
        </div>

      </div>
    </div>
  )
}
