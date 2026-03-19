import Card from "./KPITile";

export default function KPIStrip({cards}) {
  return (
    <div className="kpi-strip">
      <Card 
        title="Onboarding Started" 
        value={cards.onboarding_started.value.toLocaleString()} 
        trend={cards.onboarding_started.trend_percentage}
        trendText="vs previous period"
        iconColor="blue"
        iconSvg={<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>}
        sparklineColor="#3b82f6"
        footerStats={[
          { label: "Submitted", value: cards.onboarding_started.submitted.toLocaleString(), progress: " " },
          { label: "In Progress", value: cards.onboarding_started.in_progress.toLocaleString() }
        ]}
      />

      <Card 
        title="Onboarding Completed" 
        value={cards.onboarding_completed.value.toLocaleString()} 
        trend={cards.onboarding_completed.trend_percentage}
        trendText="vs previous period"
        iconColor="green"
        iconSvg={<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>}
        sparklineColor="#22c55e"
        footerStats={[
          { label: "Conversion Rate", value: `${cards.onboarding_completed.conversion_rate}%` },
          { label: "Approval Rate", value: `${cards.onboarding_completed.approval_rate}%` }
        ]}
      />

      <Card 
        title="Avg Completion Time" 
        value={`${Math.floor(cards.avg_completion_time.value_minutes)}m ${Math.round((cards.avg_completion_time.value_minutes % 1) * 60)}s`} 
        trend={cards.avg_completion_time.trend_minutes}
        trendText="slower vs previous period"
        iconColor="orange"
        iconSvg={<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>}
        sparklineColor="#f97316"
        footerStats={[
          { label: "SLA Target", value: `${Math.floor(cards.avg_completion_time.sla_target_minutes)}m 00s` },
          { label: `Max (${cards.avg_completion_time.max_product_name || 'N/A'})`, value: `${Math.floor(cards.avg_completion_time.max_product_time_minutes || 0)}m` }
        ]}
      />

      <Card 
        title="Pipeline At Risk" 
        value={`₹${cards.pipeline_at_risk.amount_cr.toFixed(1)} Cr`} 
        trend={cards.pipeline_at_risk.trend_cr}
        trendText={`Cr ${cards.pipeline_at_risk.percentage_of_total_pipeline}% of total pipeline`}
        iconColor="red"
        iconSvg={<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>}
        sparklineColor="#ef4444"
        footerStats={[
          { label: "SLA Breached", value: cards.pipeline_at_risk.sla_breached.toLocaleString(), warning: true },
          { label: "Stuck >24h", value: cards.pipeline_at_risk.stuck_over_24h.toLocaleString(), warning: true }
        ]}
      />
    </div>
  )
}
