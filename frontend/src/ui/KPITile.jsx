import React, { useMemo } from 'react';
import { AreaChart, Area, ResponsiveContainer } from 'recharts';

export default function KPITile({
  title, 
  value, 
  trend, 
  trendText, 
  iconColor, 
  iconSvg, 
  sparklineColor, 
  customBg, 
  customBorder, 
  footerStats
}) {

  const isPositive = trend >= 0;
  const trendColorClass = isPositive ? "green" : "red";
  const trendSign = isPositive ? "+" : "";

  // Generate dynamic array for sparkline based on the current trend
  const sparklineData = useMemo(() => {
    const data = [];
    let current = 50;
    for(let i=0; i<10; i++) {
        data.push({ uv: current });
        // Trend affects the trajectory
        const change = (Math.random() * 10) * (isPositive ? 1 : -1);
        current += change;
    }
    return data;
  }, [trend]);

  return (
    <div 
      className="kpi-card" 
      style={{
        backgroundColor: customBg || '#fff', 
        borderColor: customBorder || '#e5e7eb'
      }}
    >
      <div className="kpi-title-row">
        <div className={`kpi-icon ${iconColor}`}>
          {iconSvg}
        </div>
        {title}
      </div>

      <div className="kpi-value">{value}</div>

      <div className={`kpi-trend ${trendColorClass}`}>
        {trendSign}{trend}% <span className="kpi-trend-text">{trendText}</span>
      </div>

      <div className="kpi-sparkline">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={sparklineData}>
             <defs>
              <linearGradient id={`colorUv-${title.replace(/\s+/g, '')}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={sparklineColor} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={sparklineColor} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <Area 
                type="monotone" 
                dataKey="uv" 
                stroke={sparklineColor} 
                fill={`url(#colorUv-${title.replace(/\s+/g, '')})`} 
                strokeWidth={2}
                isAnimationActive={true}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {footerStats && (
        <div className="kpi-footer-stats">
          {footerStats.map((stat, i) => (
            <div key={i} className="kpi-stat">
              {stat.label}
              <strong style={stat.warning ? {color: '#dc2626'} : {}}>
                {stat.value} {stat.progress && <span style={{fontSize: '0.7rem', color: '#6b7280', fontWeight: 500, marginLeft: '4px'}}>{stat.progress}</span>}
              </strong>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
