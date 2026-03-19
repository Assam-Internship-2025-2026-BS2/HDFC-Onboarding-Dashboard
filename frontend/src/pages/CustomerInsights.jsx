import React, { useState, useEffect } from "react";
import { getInsights } from "../services/api";
import Filters from "../ui/Filters";

export default function CustomerInsights() {
  const [filters, setFilters] = useState({
    time_range: "This Month",
    channel: "All Channels",
    region: "All Regions",
    segment: "All Segments"
  });

  const [data, setData] = useState(null);

  useEffect(() => {
    async function loadData() {
      const response = await getInsights(filters);
      setData(response);
    }
    loadData();
  }, [filters]);

  if (!data) return <div className="loading">Loading insights data...</div>;

  return (
    <>
    <div className="dashboard-header-container" style={{ backgroundColor: '#0b0f19', padding: '24px 24px 0 24px', color: '#f8fafc' }}>
      <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600, letterSpacing: '-0.5px' }}>Customer Insights</h1>
    </div>
    <Filters filters={filters} setFilters={setFilters} />

    <div className="content">
      
      <div className="kpi-strip" style={{ gridTemplateColumns: "repeat(3, 1fr)" }}>
        <div className="kpi-card">
          <div className="kpi-title-row">Total Reachable Base</div>
          <div className="kpi-value">{data.reachable_base}</div>
          <div className="kpi-trend green">{data.reachable_base_trend}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title-row">Avg. Engagement Score</div>
          <div className="kpi-value">{data.engagement_score}</div>
          <div className="kpi-trend green">{data.engagement_score_trend}</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-title-row">Overall NPS</div>
          <div className="kpi-value" style={{color: '#059669'}}>{data.overall_nps}</div>
          <div className="kpi-trend green">{data.overall_nps_trend}</div>
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
                <span style={{fontWeight: 600}}>{data.demographics.age_18_25}</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: data.demographics.age_18_25, backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>26-35 Years</span>
                <span style={{fontWeight: 600}}>{data.demographics.age_26_35}</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: data.demographics.age_26_35, backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>36-50 Years</span>
                <span style={{fontWeight: 600}}>{data.demographics.age_36_50}</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: data.demographics.age_36_50, backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
              </div>
            </div>
            <div>
              <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px'}}>
                <span>50+ Years</span>
                <span style={{fontWeight: 600}}>{data.demographics.age_50_plus}</span>
              </div>
              <div style={{width: '100%', backgroundColor: '#f3f4f6', height: '8px', borderRadius: '4px'}}>
                <div style={{width: data.demographics.age_50_plus, backgroundColor: '#3b82f6', height: '100%', borderRadius: '4px'}}></div>
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
            <div style={{ width: "160px", height: "160px", borderRadius: "50%", background: `conic-gradient(#3b82f6 0% ${data.channel_preference.mobile_app}, #10b981 ${data.channel_preference.mobile_app} calc(${data.channel_preference.mobile_app} + ${data.channel_preference.website}), #f59e0b calc(${data.channel_preference.mobile_app} + ${data.channel_preference.website}) 100%)`, position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ width: "100px", height: "100px", backgroundColor: "#fff", borderRadius: "50%", position: "absolute" }}></div>
            </div>
          </div>
          
          <div style={{ display: "flex", justifyContent: "space-around", marginTop: "24px", fontSize: "0.85rem", fontWeight: 500 }}>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#3b82f6', borderRadius:'50%'}}></div> Mobile App ({data.channel_preference.mobile_app})</div>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#10b981', borderRadius:'50%'}}></div> Website ({data.channel_preference.website})</div>
            <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}><div style={{width:'10px', height:'10px', backgroundColor:'#f59e0b', borderRadius:'50%'}}></div> Branch ({data.channel_preference.branch})</div>
          </div>

        </div>
      </div>
    </div>
    </>
  );
}
