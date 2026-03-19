from typing import Dict
from app.core.database import get_clickhouse_client
from app.schemas.analysis_schema import AnalysisResponse, FunnelStep, TrendPoint, ChannelPoint
from app.utils.date_utils import get_date_range

class AnalysisService:
    @staticmethod
    def get_analysis_data(filters: Dict) -> AnalysisResponse:
        client = get_clickhouse_client()
        from_date, to_date = get_date_range(filters.get("time_range", "This Month"))
        
        product_name = filters.get("product", "Credit Card")
        
        params = {
            "from_date": from_date,
            "to_date": to_date,
            "product_name": product_name,
            "channel": filters.get("channel", "All Channels") or "All Channels",
            "region": filters.get("region", "All Regions") or "All Regions",
            "segment": filters.get("segment", "All Segments") or "All Segments",
        }
        
        # 1. Fetch Funnel Data
        query_funnel = """
        SELECT
            SUM(started),
            SUM(submitted),
            SUM(in_progress),
            SUM(completed),
            SUM(approved)
        FROM dashboard_data
        WHERE product_name = {product_name:String}
          AND date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        """
        result_funnel = client.query(query_funnel, parameters=params).result_rows
        
        funnel = []
        if result_funnel and result_funnel[0]:
            r = result_funnel[0]
            funnel.append(FunnelStep(name="Traffic Hit", count=int(r[0] or 0)))
            funnel.append(FunnelStep(name="Eligibility", count=int(r[1] or 0)))
            funnel.append(FunnelStep(name="V-KYC", count=int(r[2] or 0)))
            funnel.append(FunnelStep(name="Underwriting", count=int(r[3] or 0)))
            funnel.append(FunnelStep(name="Approval", count=int(r[4] or 0)))
        
        # 2. Fetch Trend Data dynamically
        query_trend = """
        SELECT
            date,
            SUM(started),
            SUM(approved)
        FROM dashboard_data
        WHERE product_name = {product_name:String}
          AND date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        GROUP BY date
        ORDER BY date ASC
        """
        result_trend = client.query(query_trend, parameters=params).result_rows
        
        trend = []
        for r in result_trend:
            dt_str = r[0].strftime("%b %d") if hasattr(r[0], "strftime") else str(r[0])
            started = r[1] or 0
            approved = r[2] or 0
            
            conv_rate = int((approved / started) * 100) if started > 0 else 0
            dropoff_rate = 100 - conv_rate if started > 0 else 0
            
            trend.append(TrendPoint(month=dt_str, Conversion=conv_rate, Dropoff=dropoff_rate))
            
        # Optional: Limit to recent points if too dense (e.g. 15 max)
        if len(trend) > 15:
            trend = trend[-15:]
        
        # 3. Fetch Channel Distribution Data
        query_channels = """
        SELECT
            channel,
            SUM(started)
        FROM dashboard_data
        WHERE product_name = {product_name:String}
          AND date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        GROUP BY channel
        """
        result_channels = client.query(query_channels, parameters=params).result_rows
        
        channels = []
        total_started_all_channels = sum((r[1] or 0) for r in result_channels)
        
        for row in result_channels:
            channel_name = row[0]
            count = row[1] or 0
            pct = int((count / total_started_all_channels) * 100) if total_started_all_channels else 0
            if pct > 0:
                channels.append(ChannelPoint(name=channel_name, value=pct))
                
        return AnalysisResponse(funnel=funnel, trend=trend, channels=channels)
