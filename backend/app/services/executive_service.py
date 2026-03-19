from datetime import datetime, timedelta

from app.services.insight_service import InsightService
from app.constants.thresholds import (
    SEVERITY_CRITICAL,
    ALERT_CONVERSION_THRESHOLD,
    ALERT_FAILURE_THRESHOLD,
    ALERT_SLA_BREACH_THRESHOLD,
    SEVERITY_HIGH
)

from app.core.database import get_clickhouse_client

from app.queries.dashboard_queries import (
    executive_aggregate_query,
    max_product_time_query,
    product_alerts_query,
    channel_distribution_query,
    trend_analysis_query
)


from app.utils.date_utils import get_date_range


def get_comparison_range(comparison):

    today = datetime.today().date()

    if comparison is None:
        return None, None

    if comparison == "V/S Last Week":
        return today - timedelta(days=14), today - timedelta(days=7)

    elif comparison == "V/S Previous Period":
        return today - timedelta(days=60), today - timedelta(days=30)

    elif comparison == "V/S Last Month":

        first_day_this_month = today.replace(day=1)
        last_month_end = first_day_this_month - timedelta(days=1)

        return last_month_end.replace(day=1), last_month_end

    elif comparison == "V/S Yesterday":
        yday = today - timedelta(days=1)
        return yday, yday

    return None, None


def calculate_trend(current, previous):

    if not previous:
        return 0, "UP"

    trend = ((current - previous) / previous) * 100

    direction = "UP" if trend >= 0 else "DOWN"

    return round(abs(trend), 2), direction


def generate_alerts(client, params):

    alerts = []
    seen_products = set()

    result = client.query(
        product_alerts_query(),
        parameters=params
    )

    rows = result.result_rows

    for row in rows:

        product = row[0]
        started = row[1] or 0
        completed = row[2] or 0
        approved = row[3] or 0
        failures = row[4] or 0
        sla_breached = row[5] or 0

        conversion = (completed / started) * 100 if started else 0

        if product in seen_products:
            continue

        if conversion < ALERT_CONVERSION_THRESHOLD:

            alerts.append({
                "text": f"{product} conversion dropped below threshold ({round(conversion,1)}%)",
                "severity": SEVERITY_CRITICAL
            })

            seen_products.add(product)

        elif failures > ALERT_FAILURE_THRESHOLD:

            alerts.append({
                "text": f"{product} failures increased significantly",
                "severity": SEVERITY_CRITICAL
            })

            seen_products.add(product)

        elif sla_breached > ALERT_SLA_BREACH_THRESHOLD:

            alerts.append({
                "text": f"{product} SLA breached — {sla_breached} cases",
                "severity": SEVERITY_HIGH
            })

            seen_products.add(product)

    return alerts


def fetch_executive_dashboard(time_range, comparison, channel, region, segment):

    if time_range == "Today":
        return {
            "overall_health": {
                "status": "STABLE",
                "critical_products": 0,
                "message": "Live production data unavailable for today in mock environment",
                "alerts": []
            },
            "insights": [],
            "kpi_cards": {
                "onboarding_started": {
                    "value": 0,
                    "trend_percentage": 0,
                    "trend_direction": "UP",
                    "submitted": 0,
                    "in_progress": 0
                },
                "onboarding_completed": {
                    "value": 0,
                    "trend_percentage": 0,
                    "trend_direction": "UP",
                    "conversion_rate": 0,
                    "approval_rate": 0
                },
                "avg_completion_time": {
                    "value_minutes": 0,
                    "trend_minutes": 0,
                    "trend_direction": "UP",
                    "sla_target_minutes": 0,
                    "max_product_time_minutes": 0,
                    "max_product_name": "N/A"
                },
                "pipeline_at_risk": {
                    "amount_cr": 0,
                    "trend_cr": 0,
                    "trend_direction": "UP",
                    "percentage_of_total_pipeline": 0,
                    "sla_breached": 0,
                    "stuck_over_24h": 0
                }
            },
            "filters_applied": {
                "time_range": time_range,
                "comparison": comparison,
                "channel": channel,
                "region": region,
                "segment": segment
            },
            "channel_distribution": [],
            "trend_data": [],
            "data_as_of_timestamp": datetime.utcnow()
        }

    client = get_clickhouse_client()

    from_date, to_date = get_date_range(time_range)

    params = {
        "from_date": from_date,
        "to_date": to_date,
        "channel": channel,
        "region": region,
        "segment": segment
    }

    result = client.query(
        executive_aggregate_query(),
        parameters=params
    )

    row = result.result_rows[0] if result.result_rows else [0] * 12

    started = row[0] or 0
    submitted = row[1] or 0
    in_progress = row[2] or 0
    completed = row[3] or 0
    approved = row[4] or 0
    failures = row[5] or 0
    avg_time = row[6] or 0
    sla_target = row[7] or 0
    pipeline_total = row[8] or 0
    pipeline_risk = row[9] or 0
    sla_breached = row[10] or 0
    stuck = row[11] or 0

    conversion = (completed / started) * 100 if started else 0
    approval = (approved / completed) * 100 if completed else 0

    pipeline_percentage = (pipeline_risk / pipeline_total) * 100 if pipeline_total else 0

    comp_from, comp_to = get_comparison_range(comparison)

    prev_started = prev_completed = prev_avg_time = prev_pipeline = 0

    if comp_from and comp_to:

        comp_params = {
            "from_date": comp_from,
            "to_date": comp_to,
            "channel": channel,
            "region": region,
            "segment": segment
        }

        comp_result = client.query(
            executive_aggregate_query(),
            parameters=comp_params
        )

        comp_row = comp_result.result_rows[0] if comp_result.result_rows else [0] * 12

        prev_started = comp_row[0] or 0
        prev_completed = comp_row[3] or 0
        prev_avg_time = comp_row[6] or 0
        prev_pipeline = comp_row[9] or 0

    started_trend, started_dir = calculate_trend(started, prev_started)
    completed_trend, completed_dir = calculate_trend(completed, prev_completed)
    time_trend, time_dir = calculate_trend(avg_time, prev_avg_time)
    pipeline_trend, pipeline_dir = calculate_trend(pipeline_risk, prev_pipeline)

    max_product_result = client.query(
        max_product_time_query(),
        parameters=params
    )

    max_product_row = max_product_result.result_rows[0] if max_product_result.result_rows else ["N/A", 0]

    alerts = generate_alerts(client, params)

    filters = {
        "time_range": time_range,
        "channel": channel,
        "region": region,
        "segment": segment
    }
    insight_response = InsightService.compute_insights(filters)

    channel_res = client.query(channel_distribution_query(), parameters=params)
    channel_data = [{"name": r[0], "value": r[1]} for r in channel_res.result_rows] if channel_res.result_rows else []

    trend_res = client.query(trend_analysis_query(), parameters=params)
    trend_data = [{"day": r[0].strftime("%b %d") if hasattr(r[0], "strftime") else str(r[0]), "value": r[1] or 0, "submissions": r[2] or 0} for r in trend_res.result_rows] if trend_res.result_rows else []

    return {

        "overall_health": {
            "status": "WATCH" if alerts else "STABLE",
            "critical_products": len(alerts),
            "message": f"{len(alerts)} products showing risk signals",
            "alerts": alerts
        },

        "insights": insight_response.insights,

        "kpi_cards": {

            "onboarding_started": {
                "value": started,
                "trend_percentage": started_trend,
                "trend_direction": started_dir,
                "submitted": submitted,
                "in_progress": in_progress
            },

            "onboarding_completed": {
                "value": completed,
                "trend_percentage": completed_trend,
                "trend_direction": completed_dir,
                "conversion_rate": round(conversion, 2),
                "approval_rate": round(approval, 2)
            },

            "avg_completion_time": {
                "value_minutes": round(avg_time, 2) if avg_time else 0,
                "trend_minutes": time_trend,
                "trend_direction": time_dir,
                "sla_target_minutes": round(sla_target, 2) if sla_target else 0,
                "max_product_time_minutes": round(max_product_row[1], 2),
                "max_product_name": max_product_row[0]
            },

            "pipeline_at_risk": {
                "amount_cr": round(pipeline_risk, 2),
                "trend_cr": pipeline_trend,
                "trend_direction": pipeline_dir,
                "percentage_of_total_pipeline": round(pipeline_percentage, 2),
                "sla_breached": sla_breached,
                "stuck_over_24h": stuck
            }
        },

        "filters_applied": {
            "time_range": time_range,
            "comparison": comparison,
            "channel": channel,
            "region": region,
            "segment": segment
        },

        "channel_distribution": channel_data,
        "trend_data": trend_data,

        "data_as_of_timestamp": datetime.utcnow()
    }