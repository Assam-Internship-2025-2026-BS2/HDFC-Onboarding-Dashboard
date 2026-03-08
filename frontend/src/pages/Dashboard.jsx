import {useEffect, useState} from "react";
import {getDashboard, getMatrix} from "../services/api";
import KPIStrip from "../ui/KPIStrip";
import Matrix from "../ui/Matrix";
import Insights from "../ui/Insights";
import Filters from "../ui/Filters";
import DashboardGraphics from "../ui/DashboardGraphics";

export default function Dashboard() {
  const [filters, setFilters] = useState({
    time_range: "This Month",
    channel: "All Channels",
    region: "All Regions",
    segment: "All Segments"
  });

  const [data, setData] = useState(null);
  const [matrix, setMatrix] = useState([]);

  useEffect(() => { load() }, [filters]);

  const load = async () => {
    let comp = "V/S Last Month";
    if (filters.time_range === "Last 7 Days") comp = "V/S Last Week";
    if (filters.time_range === "Last 30 Days") comp = "V/S Previous Period";
    if (filters.time_range === "Today") comp = "V/S Yesterday"; // Even if backend lacks this, it's safer.

    const payload = { ...filters, comparison: comp };

    const d = await getDashboard(payload);
    const m = await getMatrix(payload);
    setData(d);
    setMatrix(m);
  }

  if (!data) return <div className="loading">Loading dashboard...</div>;

  return (
    <>
      <div className="dashboard-header-container" style={{ backgroundColor: '#0b0f19', padding: '24px 24px 0 24px', color: '#f8fafc' }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600, letterSpacing: '-0.5px' }}>Digital Onboarding Dashboard</h1>
      </div>
      {/* Sub Navigation */}
      <Filters filters={filters} setFilters={setFilters} />

      <div className="content">
        {/* Alert Banner */}
        <div className="alert-banner">
          <div className="alert-left">
            <div className="alert-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
              Overall Health: {data.overall_health.status}
            </div>
            <div className="alert-subtitle">
              {data.overall_health.message}
            </div>
            <div className="alert-tags">
              {data.overall_health.alerts && data.overall_health.alerts.length > 0 ? (
                data.overall_health.alerts.map((alert, idx) => {
                  let colorClass = "orange"; // default
                  if (alert.severity === "CRITICAL") colorClass = "red";
                  if (alert.severity === "HIGH") colorClass = "pink";
                  return (
                    <span key={idx} className={`alert-tag ${colorClass}`}>
                      ● {alert.text}
                    </span>
                  );
                })
              ) : (
                <span className="alert-tag green">● All systems normal. No alerts triggered.</span>
              )}
            </div>
          </div>
          <button className="view-alerts-btn">View All Alerts →</button>
        </div>

        <KPIStrip cards={data.kpi_cards} />

        <div className="lower">
          <DashboardGraphics data={data} />
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <Matrix matrix={matrix} />
            <Insights items={data.insights} />
          </div>
        </div>
      </div>
    </>
  );
}
