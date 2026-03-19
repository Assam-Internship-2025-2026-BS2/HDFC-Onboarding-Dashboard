from typing import Dict
from app.core.database import get_clickhouse_client
from app.schemas.products_schema import ProductsResponse, ProductKPIs, ProductMatrixRow
from app.utils.date_utils import get_date_range

class ProductsService:
    @staticmethod
    def get_products_data(filters: Dict) -> ProductsResponse:
        client = get_clickhouse_client()
        
        from_date, to_date = get_date_range(filters.get("time_range", "This Month"))
        
        params = {
            "from_date": from_date,
            "to_date": to_date,
            "channel": filters.get("channel", "All Channels") or "All Channels",
            "region": filters.get("region", "All Regions") or "All Regions",
            "segment": filters.get("segment", "All Segments") or "All Segments",
        }
        
        # 1. Fetch KPI Aggregations
        query_kpi = """
        SELECT
            SUM(started),
            SUM(approved),
            SUM(failures),
            SUM(sla_breached)
        FROM dashboard_data
        WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        """
        result_kpi = client.query(query_kpi, parameters=params).result_rows
        
        # Calculate dynamic KPIs
        total_active = 0
        total_disbursed = 0
        total_conversions = 0
        sla_breaches = 0
        
        if result_kpi and result_kpi[0]:
            total_active = result_kpi[0][0] or 0
            total_disbursed = result_kpi[0][1] or 0  # Using approved as proxy
            total_conversions = result_kpi[0][1] or 0
            sla_breaches = result_kpi[0][3] or 0
            
        # Optional: Calculate prior period for trend (Simplified)
        from datetime import timedelta
        delta = (to_date - from_date).days
        prior_to = from_date - timedelta(days=1)
        prior_from = prior_to - timedelta(days=delta)
        
        params_prior = params.copy()
        params_prior["from_date"] = prior_from
        params_prior["to_date"] = prior_to
        
        result_prior = client.query(query_kpi, parameters=params_prior).result_rows
        
        pt_active = pt_disbursed = pt_conversions = pt_sla = 0
        if result_prior and result_prior[0]:
            pt_active = result_prior[0][0] or 0
            pt_disbursed = result_prior[0][1] or 0
            pt_conversions = result_prior[0][1] or 0
            pt_sla = result_prior[0][3] or 0
            
        def calc_trend(curr, prev):
            if not prev: return "+0%", "UP"
            t = ((curr - prev) / prev) * 100
            sign = "+" if t >= 0 else ""
            return f"{sign}{t:.1f}%", "UP" if t >= 0 else "DOWN"
            
        t_act, _ = calc_trend(total_active, pt_active)
        t_dis, _ = calc_trend(total_disbursed, pt_disbursed)
        t_con, _ = calc_trend(total_conversions, pt_conversions)
        t_sla, _ = calc_trend(sla_breaches, pt_sla)
            
        kpis = ProductKPIs(
            total_active=f"{total_active:,}",
            total_active_trend=f"{t_act} vs last period",
            total_disbursed=f"{total_disbursed:,}",
            total_disbursed_trend=f"{t_dis} vs last period",
            total_conversions=f"{total_conversions:,}",
            total_conversions_trend=f"{t_con} vs last period",
            sla_breaches=f"{sla_breaches:,}",
            sla_breaches_trend=f"{t_sla} vs last period"
        )
        
        # 2. Fetch Matrix Rows
        query_matrix = """
        SELECT
            product_name,
            SUM(started),
            SUM(approved),
            AVG(avg_time_minutes)
        FROM dashboard_data
        WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        GROUP BY product_name
        """
        result_matrix = client.query(query_matrix, parameters=params).result_rows
        
        matrix_rows = []
        for row in result_matrix:
            product_name = row[0]
            started = row[1] or 0
            approved = row[2] or 0
            avg_time = row[3] or 0
            
            conv_rate = (approved / started * 100) if started > 0 else 0
            
            # Helper for formatting time
            hrs = int(avg_time // 60)
            mins = int(avg_time % 60)
            time_str = f"{hrs}h {mins}m" if hrs > 0 else f"{mins}m"
            
            # Simple status logic
            status = "Healthy"
            if conv_rate < 40:
                status = "Moderate"
            if conv_rate < 20:
                status = "Critical"
            if hrs >= 4:
                status = "SLA Breach Risk"
            
            matrix_rows.append(ProductMatrixRow(
                product_line=product_name,
                applications_started=f"{started:,}",
                approved=f"{approved:,}",
                conversion_rate=f"{conv_rate:.1f}%",
                avg_processing_time=time_str,
                status=status
            ))
            
        return ProductsResponse(kpis=kpis, matrix_rows=matrix_rows)
