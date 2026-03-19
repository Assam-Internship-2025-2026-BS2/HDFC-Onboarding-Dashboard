import React, { useState, useEffect } from "react";
import { getAnalysis } from "../services/api";
import Filters from "../ui/Filters";
import { 
  BarChart, Bar, 
  LineChart, Line, 
  PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area 
} from "recharts";

export default function Analysis() {
  const [filters, setFilters] = useState({
    time_range: "This Month",
    channel: "All Channels",
    region: "All Regions",
    segment: "All Segments",
    product: "Credit Card"
  });

  const [activeData, setActiveData] = useState(null);

  useEffect(() => {
    async function loadData() {
      const response = await getAnalysis(filters);
      setActiveData(response);
    }
    loadData();
  }, [filters]);

  const pieColors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"];

  if (!activeData) return <div className="loading">Loading analysis data...</div>;

  return (
    <>
    <div className="dashboard-header-container" style={{ backgroundColor: '#0b0f19', padding: '24px 24px 0 24px', color: '#f8fafc' }}>
      <h1 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 600, letterSpacing: '-0.5px' }}>Advanced Intelligence & Analytics</h1>
    </div>
    <Filters filters={filters} setFilters={setFilters} />

    <div className="content">

      
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", paddingBottom: "40px" }}>
        
        {/* Funnel Bar Chart */}
        <div className="panel" style={{ height: "400px" }}>
          <div className="panel-header" style={{marginBottom: "20px"}}>
            <h3>Funnel Drop-off Volume</h3>
          </div>
          <ResponsiveContainer width="100%" height="85%" minWidth={0} minHeight={0}>
            <BarChart data={activeData.funnel} margin={{ top: 20, right: 30, left: 20, bottom: 5 }} minWidth={0} minHeight={0}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip cursor={{fill: '#f3f4f6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'}} />
              <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Trend Area Chart */}
        <div className="panel" style={{ height: "400px" }}>
          <div className="panel-header" style={{marginBottom: "20px"}}>
            <h3>6-Month Performance Trend</h3>
          </div>
          <ResponsiveContainer width="100%" height="85%" minWidth={0} minHeight={0}>
            <AreaChart data={activeData.trend} margin={{ top: 20, right: 30, left: 0, bottom: 5 }} minWidth={0} minHeight={0}>
              <defs>
                <linearGradient id="colorConv" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorDrop" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
              <XAxis dataKey="month" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'}} />
              <Legend verticalAlign="top" height={36}/>
              <Area type="monotone" dataKey="Conversion" stroke="#10b981" fillOpacity={1} fill="url(#colorConv)" />
              <Area type="monotone" dataKey="Dropoff" stroke="#ef4444" fillOpacity={1} fill="url(#colorDrop)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Channel Pie Chart */}
        <div className="panel" style={{ height: "350px", gridColumn: "1 / -1" }}>
          <div className="panel-header" style={{marginBottom: "10px"}}>
            <h3>Acquisition Channel Distribution</h3>
          </div>
          <div style={{display: 'flex', width: '100%', height: '80%'}}>
            <ResponsiveContainer width="50%" height="100%" minWidth={0} minHeight={0}>
              <PieChart minWidth={0} minHeight={0}>
                <Pie
                  data={activeData.channels}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {activeData.channels.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)'}} />
              </PieChart>
            </ResponsiveContainer>
            
            <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '20px', width: '50%'}}>
              {activeData.channels.map((entry, index) => (
                <div key={index} style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
                  <div style={{width: '16px', height: '16px', borderRadius: '4px', backgroundColor: pieColors[index]}}></div>
                  <div style={{fontSize: '1.1rem', fontWeight: 500}}>{entry.name}</div>
                  <div style={{fontSize: '1.1rem', fontWeight: 700, marginLeft: 'auto'}}>{entry.value}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
    </>
  );
}
