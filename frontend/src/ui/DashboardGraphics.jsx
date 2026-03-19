import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';

export default function DashboardGraphics({ data }) {
  if (!data || !data.kpi_cards) return null;

  // Dynamic Trend Analysis mapping from backend
  let trendData = data.trend_data || [];
  
  // If only one data point exists (e.g. for "Today"), duplicate it so the AreaChart renders an area/line instead of a single dot.
  if (trendData.length === 1) {
    trendData = [
      { ...trendData[0], day: `Start (${trendData[0].day})` },
      { ...trendData[0] },
      { ...trendData[0], day: `End (${trendData[0].day})` }
    ];
  }

  // Dynamic Channel Distribution mapping from backend
  const channelData = data.channel_distribution || [];
  const COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

      {/* Overall Trend Area Chart */}
      <div className="panel" style={{ padding: '24px' }}>
        <div className="panel-header" style={{ marginBottom: '24px', paddingBottom: 0, borderBottom: 'none' }}>
          <h3 style={{ fontSize: '1.15rem', margin: 0 }}>Onboarding Trend Analysis</h3>
        </div>
        <div style={{ height: '300px', width: '100%', minWidth: 0, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
            <AreaChart data={trendData} margin={{ top: 10, right: 10, left: 0, bottom: 15 }} minWidth={0} minHeight={0}>
              <defs>
                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorSubs" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#5cf68fff" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#5cf68fff" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis 
                dataKey="day" 
                axisLine={false} 
                tickLine={false} 
                tick={{ fontSize: 11, fill: '#64748b' }} 
                dy={10} 
                label={{ value: 'Days', position: 'insideBottom', offset: -10, fill: '#64748b', fontSize: 12, fontWeight: 500 }}
              />
              <YAxis 
                axisLine={false} 
                tickLine={false} 
                tick={{ fontSize: 11, fill: '#64748b' }} 
                width={50} 
                tickFormatter={(value) => value >= 1000 ? `${(value / 1000).toFixed(0)}k` : value}
                label={{ value: 'Volume', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 12, fontWeight: 500 }}
              />
              <Tooltip
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
              />
              <Area type="monotone" dataKey="value" name="Started" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
              <Area type="monotone" dataKey="submissions" name="Completed" stroke="#5cf68fff" strokeWidth={3} fillOpacity={1} fill="url(#colorSubs)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Channel Distribution Pie Chart */}
      <div className="panel" style={{ padding: '24px' }}>
        <div className="panel-header" style={{ marginBottom: '24px', paddingBottom: 0, borderBottom: 'none' }}>
          <h3 style={{ fontSize: '1.15rem', margin: 0 }}>Channel Origin</h3>
        </div>
        <div style={{ height: '300px', width: '100%', minWidth: 0, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%" minWidth={0} minHeight={0}>
            <PieChart minWidth={0} minHeight={0}>
              <Pie
                data={channelData}
                cx="50%"
                cy="45%"
                innerRadius={65}
                outerRadius={90}
                paddingAngle={5}
                dataKey="value"
                nameKey="name"
                stroke="none"
              >
                {channelData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value, name, props) => {
                   const total = channelData.reduce((acc, curr) => acc + curr.value, 0);
                   const percent = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                   return [`${value.toLocaleString('en-IN')} (${percent}%)`];
                }}
                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
              />
              <Legend
                verticalAlign="bottom"
                height={36}
                iconType="circle"
                formatter={(value, entry) => {
                  const dataEntry = channelData.find(d => d.name === value);
                  const val = dataEntry ? dataEntry.value : 0;
                  const total = channelData.reduce((acc, curr) => acc + curr.value, 0);
                  const percent = total > 0 ? Math.round((val / total) * 100) : 0;
                  return <span style={{ fontSize: '0.85rem', fontWeight: 500 }}>{value} - {val.toLocaleString('en-IN')} ({percent}%)</span>;
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}
