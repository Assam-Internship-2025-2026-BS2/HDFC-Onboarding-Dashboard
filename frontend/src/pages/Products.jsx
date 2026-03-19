import React, { useState, useEffect } from "react";
import { getProducts } from "../services/api";
import Filters from "../ui/Filters";

export default function Products() {
  const [filters, setFilters] = useState({
    time_range: "This Month",
    channel: "All Channels",
    region: "All Regions",
    segment: "All Segments"
  });

  const [data, setData] = useState(null);

  useEffect(() => {
    async function loadData() {
      const response = await getProducts(filters);
      setData(response);
    }
    loadData();
  }, [filters]);

  if (!data) return <div className="loading">Loading products data...</div>;

  return (
    <>
    <div className="dashboard-header-container" style={{ backgroundColor: '#0b0f19', padding: '24px 24px 0 24px', color: '#f8fafc' }}>
      <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600, letterSpacing: '-0.5px' }}>Products Overview</h1>
    </div>
    <Filters filters={filters} setFilters={setFilters} />

    <div className="content">
      
      <div className="kpi-strip">
        <div className="kpi-card" style={{ borderTop: "4px solid #3b82f6" }}>
          <div className="kpi-title-row">Total Active Products</div>
          <div className="kpi-value">{data.kpis.total_active}</div>
          <div className="kpi-trend green">{data.kpis.total_active_trend}</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #f97316" }}>
          <div className="kpi-title-row">Total Disbursed (PL)</div>
          <div className="kpi-value">₹{data.kpis.total_disbursed}</div>
          <div className="kpi-trend green">{data.kpis.total_disbursed_trend}</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #22c55e" }}>
          <div className="kpi-title-row">Total Conversions</div>
          <div className="kpi-value">{data.kpis.total_conversions}</div>
          <div className="kpi-trend green">{data.kpis.total_conversions_trend}</div>
        </div>
        <div className="kpi-card" style={{ borderTop: "4px solid #db2777" }}>
          <div className="kpi-title-row">Product SLA Breaches</div>
          <div className="kpi-value" style={{color: '#dc2626'}}>{data.kpis.sla_breaches}</div>
          <div className="kpi-trend red">{data.kpis.sla_breaches_trend}</div>
        </div>
      </div>

      <div className="lower" style={{ marginTop: "24px", gridTemplateColumns: "1fr" }}>
        <div className="matrix-panel">
          <div className="matrix-header">
            <h3>Product Performance Matrix</h3>
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
              {data.matrix_rows.map((row, idx) => {
                let pillClass = "pill green";
                if (row.status === "Moderate") pillClass = "pill yellow";
                if (row.status === "Critical" || row.status === "SLA Breach Risk") pillClass = "pill red";
                
                let conversionClass = "pill green";
                const convVal = parseFloat(row.conversion_rate);
                if (convVal < 40) conversionClass = "pill yellow";
                if (convVal < 20) conversionClass = "pill red";
                
                let statusColor = "#059669";
                if (row.status === "Moderate") statusColor = "#d97706";
                if (row.status === "Critical" || row.status === "SLA Breach Risk") statusColor = "#dc2626";

                return (
                  <tr key={idx}>
                    <td style={{fontWeight: 600}}>{row.product_line}</td>
                    <td>{row.applications_started}</td>
                    <td>{row.approved}</td>
                    <td><span className={conversionClass}>{row.conversion_rate}</span></td>
                    <td>{row.avg_processing_time}</td>
                    <td style={{color: statusColor}}>{row.status}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    </>
  );
}
