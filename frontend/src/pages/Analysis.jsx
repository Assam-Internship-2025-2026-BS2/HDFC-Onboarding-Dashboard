import React, { useState } from "react";
import { 
  BarChart, Bar, 
  LineChart, Line, 
  PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area 
} from "recharts";

export default function Analysis() {
  const [product, setProduct] = useState("Credit Card");

  // Dictionary mapping product to distinct mock data sets
  // This allows the UI to change upon selecting the filter
  const productData = {
    "Credit Card": {
      funnel: [
        { name: "Traffic Hit", count: 145200 },
        { name: "Eligibility", count: 121968 },
        { name: "V-KYC", count: 104544 },
        { name: "Underwriting", count: 78408 },
        { name: "Approval", count: 68500 }
      ],
      trend: [
        { month: "Jan", Conversion: 42, Dropoff: 18 },
        { month: "Feb", Conversion: 45, Dropoff: 15 },
        { month: "Mar", Conversion: 44, Dropoff: 16 },
        { month: "Apr", Conversion: 49, Dropoff: 12 },
        { month: "May", Conversion: 54, Dropoff: 9 },
        { month: "Jun", Conversion: 52, Dropoff: 11 },
      ],
      channels: [
        { name: "Mobile App", value: 65 },
        { name: "Web Portal", value: 25 },
        { name: "Branch/Offline", value: 10 },
      ]
    },
    "Personal Loan": {
      funnel: [
        { name: "Traffic Hit", count: 84100 },
        { name: "Eligibility", count: 52000 },
        { name: "V-KYC", count: 48000 },
        { name: "Underwriting", count: 21000 },
        { name: "Approval", count: 12400 }
      ],
      trend: [
        { month: "Jan", Conversion: 12, Dropoff: 44 },
        { month: "Feb", Conversion: 14, Dropoff: 41 },
        { month: "Mar", Conversion: 13, Dropoff: 45 },
        { month: "Apr", Conversion: 15, Dropoff: 39 },
        { month: "May", Conversion: 14, Dropoff: 42 },
        { month: "Jun", Conversion: 16, Dropoff: 38 },
      ],
      channels: [
        { name: "Mobile App", value: 45 },
        { name: "Web Portal", value: 35 },
        { name: "Branch/Offline", value: 20 },
      ]
    },
    "Auto Loan": {
      funnel: [
        { name: "Traffic Hit", count: 45300 },
        { name: "Eligibility", count: 39000 },
        { name: "V-KYC", count: 32000 },
        { name: "Underwriting", count: 24000 },
        { name: "Approval", count: 18000 }
      ],
      trend: [
        { month: "Jan", Conversion: 34, Dropoff: 22 },
        { month: "Feb", Conversion: 37, Dropoff: 19 },
        { month: "Mar", Conversion: 35, Dropoff: 21 },
        { month: "Apr", Conversion: 39, Dropoff: 18 },
        { month: "May", Conversion: 41, Dropoff: 15 },
        { month: "Jun", Conversion: 40, Dropoff: 16 },
      ],
      channels: [
        { name: "Mobile App", value: 30 },
        { name: "Web Portal", value: 20 },
        { name: "Branch/Offline", value: 50 },
      ]
    },
    "Gold Loan": {
      funnel: [
        { name: "Traffic Hit", count: 22000 },
        { name: "Eligibility", count: 21500 },
        { name: "V-KYC", count: 21000 },
        { name: "Underwriting", count: 19800 },
        { name: "Approval", count: 18900 }
      ],
      trend: [
        { month: "Jan", Conversion: 82, Dropoff: 5 },
        { month: "Feb", Conversion: 84, Dropoff: 4 },
        { month: "Mar", Conversion: 85, Dropoff: 3 },
        { month: "Apr", Conversion: 81, Dropoff: 6 },
        { month: "May", Conversion: 88, Dropoff: 2 },
        { month: "Jun", Conversion: 86, Dropoff: 4 },
      ],
      channels: [
        { name: "Mobile App", value: 15 },
        { name: "Web Portal", value: 10 },
        { name: "Branch/Offline", value: 75 },
      ]
    }
  };

  const activeData = productData[product];
  const pieColors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"];

  return (
    <div className="content">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: "20px"}}>
        <h2 style={{ margin: 0 }}>Advanced Intelligence & Analytics</h2>
        <select 
          className="filter-select" 
          style={{ color: "#111827", backgroundColor: "#fff", border: "1px solid #d1d5db" }}
          value={product}
          onChange={(e) => setProduct(e.target.value)}
        >
          <option value="Credit Card">Credit Card</option>
          <option value="Personal Loan">Personal Loan</option>
          <option value="Auto Loan">Auto Loan</option>
          <option value="Gold Loan">Gold Loan</option>
        </select>
      </div>
      
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", paddingBottom: "40px" }}>
        
        {/* Funnel Bar Chart */}
        <div className="panel" style={{ height: "400px" }}>
          <div className="panel-header" style={{marginBottom: "20px"}}>
            <h3>Funnel Drop-off Volume ({product})</h3>
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
                  <div style={{fontSize: '1.1rem', fontWeight: 500, color: '#374151'}}>{entry.name}</div>
                  <div style={{fontSize: '1.1rem', fontWeight: 700, marginLeft: 'auto', color: '#111827'}}>{entry.value}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
