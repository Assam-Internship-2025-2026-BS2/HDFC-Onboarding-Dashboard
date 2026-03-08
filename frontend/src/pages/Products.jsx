import React from "react";

export default function Products() {
  return (
    <div className="content">
      <h2 style={{ marginBottom: "20px" }}>Products Overview</h2>
      
      <div className="kpi-strip">
        <div className="kpi-card" style={{ borderTop: "4px solid #3b82f6" }}>
          <div className="kpi-title-row">Total Active Products</div>
          <div className="kpi-value">4.2M</div>
          <div className="kpi-trend green">+2.4% vs last quarter</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #f97316" }}>
          <div className="kpi-title-row">Total Disbursed (PL)</div>
          <div className="kpi-value">₹8,450 Cr</div>
          <div className="kpi-trend green">+11% vs last year</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #22c55e" }}>
          <div className="kpi-title-row">New Credit Cards</div>
          <div className="kpi-value">124K</div>
          <div className="kpi-trend red">-4.1% vs last month</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #db2777" }}>
          <div className="kpi-title-row">Product SLA Breaches</div>
          <div className="kpi-value" style={{color: '#dc2626'}}>1,420</div>
          <div className="kpi-trend red">+18% vs last month</div>
        </div>
      </div>

      <div className="lower" style={{ marginTop: "24px", gridTemplateColumns: "1fr" }}>
        <div className="matrix-panel">
          <div className="matrix-header">
            <h3>Product Performance Matrix</h3>
            <button className="export-btn" style={{padding: '4px 12px'}}>Download Report</button>
          </div>
          <p className="matrix-subtitle">Conversion and Drop-off analysis by major product line.</p>
          
          <table className="matrix-table">
            <thead>
              <tr>
                <th>Product Line</th>
                <th>Applications Started</th>
                <th>Approved</th>
                <th>Conversion Rate</th>
                <th>Avg. Processing Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style={{fontWeight: 600}}>Credit Cards</td>
                <td>145,200</td>
                <td>68,500</td>
                <td><span className="pill yellow">47.1%</span></td>
                <td>18m 40s</td>
                <td style={{color: '#059669'}}>Healthy</td>
              </tr>
              <tr>
                <td style={{fontWeight: 600}}>Personal Loan</td>
                <td>84,100</td>
                <td>12,400</td>
                <td><span className="pill red">14.7%</span></td>
                <td>4h 15m</td>
                <td style={{color: '#dc2626'}}>SLA Breach Risk</td>
              </tr>
              <tr>
                <td style={{fontWeight: 600}}>Savings Account</td>
                <td>210,000</td>
                <td>189,400</td>
                <td><span className="pill green">90.1%</span></td>
                <td>5m 12s</td>
                <td style={{color: '#059669'}}>Healthy</td>
              </tr>
              <tr>
                <td style={{fontWeight: 600}}>Auto Loan</td>
                <td>45,300</td>
                <td>18,000</td>
                <td><span className="pill yellow">39.7%</span></td>
                <td>2h 45m</td>
                <td style={{color: '#d97706'}}>Warning</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
