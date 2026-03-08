from datetime import date
from typing import List

from app.repositories.metrics_repository import MetricsRepository

from app.constants.thresholds import (
    CONVERSION_DROP_THRESHOLD,
    FAILURE_SPIKE_THRESHOLD,
    SLA_HOURS_THRESHOLD,
    CONVERSION_DROP,
    FAILURE_SPIKE,
    SLA_BREACH,
    SEVERITY_CRITICAL,
    SEVERITY_HIGH,
    SEVERITY_MEDIUM,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_MEDIUM,
)

from app.schemas.insight_schema import InsightResponse, InsightCard


class InsightService:

    @staticmethod
    def compute_insights(metric_date: date) -> InsightResponse:

        today_data = MetricsRepository.get_today_metrics(metric_date)
        baseline_data = MetricsRepository.get_baseline_metrics(metric_date)

        insights: List[InsightCard] = []

        if not today_data or not baseline_data:
            return InsightResponse(
                date=str(metric_date),
                critical_count=0,
                insights=[]
            )

        # ------------------------------------------------
        # Extract baseline metrics
        # ------------------------------------------------

        today_processing_hours = today_data.get("avg_processing_hours") or 0
        baseline_conversion = baseline_data.get("avg_conversion_rate") or 0
        baseline_failures = baseline_data.get("avg_failed_transactions") or 0

        product_metrics = MetricsRepository.get_product_metrics(metric_date) or []

        # ------------------------------------------------
        # PRODUCT LEVEL ANALYSIS
        # ------------------------------------------------

        for product in product_metrics:

            product_name = product.get("product")

            today_conversion = product.get("conversion_rate") or 0
            today_failures = product.get("failures") or 0

            # -------------------------
            # AC1 — Conversion Drop
            # -------------------------

            if baseline_conversion > 0:

                drop_percent = round(
                    ((baseline_conversion - today_conversion) / baseline_conversion) * 100,
                    2
                )

                if drop_percent > CONVERSION_DROP_THRESHOLD:

                    if drop_percent > 40:
                        severity = SEVERITY_CRITICAL
                        priority = PRIORITY_CRITICAL
                    elif drop_percent > 25:
                        severity = SEVERITY_HIGH
                        priority = PRIORITY_HIGH
                    else:
                        severity = SEVERITY_MEDIUM
                        priority = PRIORITY_MEDIUM

                    insights.append(
                        InsightCard(
                            product=product_name,
                            type=CONVERSION_DROP,
                            severity=severity,
                            priority_score=priority,
                            metric_value=drop_percent,
                            metric_unit="%",
                            stage="Checkout",
                            impact="Revenue Impacted",
                            message=f"{product_name} conversion dropped by {drop_percent}%",
                            cta_label="View Details"
                        )
                    )

            # -------------------------
            # AC2 — Failure Spike
            # -------------------------

            if baseline_failures > 0:

                spike_percent = round(
                    ((today_failures - baseline_failures) / baseline_failures) * 100,
                    2
                )

                if spike_percent > FAILURE_SPIKE_THRESHOLD:

                    if spike_percent > 200:
                        severity = SEVERITY_CRITICAL
                        priority = PRIORITY_CRITICAL
                    elif spike_percent > 100:
                        severity = SEVERITY_HIGH
                        priority = PRIORITY_HIGH
                    else:
                        severity = SEVERITY_MEDIUM
                        priority = PRIORITY_MEDIUM

                    insights.append(
                        InsightCard(
                            product=product_name,
                            type=FAILURE_SPIKE,
                            severity=severity,
                            priority_score=priority,
                            metric_value=spike_percent,
                            metric_unit="%",
                            stage="Checkout",
                            impact="High failure rate",
                            message=f"{product_name} failures increased by {spike_percent}%",
                            cta_label="Explore Issue"
                        )
                    )

        # ------------------------------------------------
        # AC3 — SLA BREACH
        # ------------------------------------------------

        if today_processing_hours > SLA_HOURS_THRESHOLD:

            breach_hours = round(
                today_processing_hours - SLA_HOURS_THRESHOLD,
                2
            )

            if today_processing_hours > (SLA_HOURS_THRESHOLD * 3):
                severity = SEVERITY_CRITICAL
                priority = PRIORITY_CRITICAL
            elif today_processing_hours > (SLA_HOURS_THRESHOLD * 2):
                severity = SEVERITY_HIGH
                priority = PRIORITY_HIGH
            else:
                severity = SEVERITY_MEDIUM
                priority = PRIORITY_MEDIUM

            insights.append(
                InsightCard(
                    product="All Products",
                    type=SLA_BREACH,
                    severity=severity,
                    priority_score=priority,
                    metric_value=today_processing_hours,
                    metric_unit="hours",
                    stage="Verification",
                    impact="Customer onboarding delay",
                    message=f"Average processing time exceeded SLA by {breach_hours} hours",
                    cta_label="Investigate Delay"
                )
            )

        # ------------------------------------------------
        # SORT INSIGHTS BY PRIORITY
        # ------------------------------------------------

        insights.sort(
            key=lambda x: x.priority_score,
            reverse=True
        )

        # ------------------------------------------------
        # COUNT CRITICAL ALERTS
        # ------------------------------------------------

        critical_count = sum(
            1 for i in insights
            if i.severity in [SEVERITY_CRITICAL, SEVERITY_HIGH]
        )

        return InsightResponse(
            date=str(metric_date),
            critical_count=critical_count,
            insights=insights
        )