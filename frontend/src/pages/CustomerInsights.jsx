import React from "react";

export default function CustomerInsights() {
  return (
    <div className="content">
      <h2 style={{ marginBottom: "20px" }}>Customer Insights</h2>
      
      <div className="kpi-strip" style={{ gridTemplateColumns: "repeat(3, 1fr)" }}>
        <div className="kpi-card">
          <div className="kpi-title-row">Total Reachable Base</div>
          <div className="kpi-value">12.4M</div>
          <div className="kpi-trend green">+4% since last quarter</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title-row">Avg. Engagement Score</div>
          <div className="kpi-value">78.4 / 100</div>
          <div className="kpi-trend green">+2.1 points</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title-row">Overall NPS</div>
          <div className="kpi-value" style={{color: '#059669'}}>64</div>
          <div className="kpi-trend green">+4 since last survey</div>
        </div>
      </div>

      <div className="lower" style={{ marginTop: "24px", gridTemplateColumns: "1fr 1fr" }}>
        <div className="panel">
          <h3>Customer Demographics</h3>
          <p style={{ color: "#6b7280", marginTop: "10px", marginBottom: "20px", fontSize: "0.85rem" }}>
            Age and income bracket distribution across active product users.
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>18-25 Years</span>
                <span style={{fontWeight: 600}}>14%</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: '14%', backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>26-35 Years</span>
                <span style={{fontWeight: 600}}>42%</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: '42%', backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>36-50 Years</span>
                <span style={{fontWeight: 600}}>28%</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: '28%', backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>50+ Years</span>
                <span style={{fontWeight: 600}}>16%</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: '16%', backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="panel">
          <h3>Channel Preference</h3>
          <p style={{ color: "#6b7280", marginTop: "10px", marginBottom: "20px", fontSize: "0.85rem" }}>
            Where customers are initiating their onboarding journeys.
          </p>
          
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", height: "160px" }}>
            <div style={{ width: "160px", height: "160px", borderRadius: "50%", background: "conic-gradient(#3b82f6 0% 64%, #10b981 64% 88%, #f59e0b 88% 100%)", position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ width: "100px", height: "100px", backgroundColor: "#fff", borderRadius: "50%", position: "absolute" }}></div>
            </div>
          </div>
          
          <div style={{ display: "flex", justifyContent: "space-around", marginTop: "24px", fontSize: "0.85rem", fontWeight: 500 }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#3b82f6', borderRadius:'50%'}}></div> Mobile App (64%)</div>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#10b981', borderRadius:'50%'}}></div> Website (24%)</div>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#f59e0b', borderRadius:'50%'}}></div> Branch (12%)</div>
          </div>

        </div>
      </div>
    </div>
  );
}
