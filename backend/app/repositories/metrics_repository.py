from typing import Dict
from app.core.database import get_clickhouse_client
from app.utils.date_utils import get_date_range

class MetricsRepository:

    @staticmethod
    def get_today_metrics(filters: Dict):

        client = get_clickhouse_client()
        from_date, to_date = get_date_range(filters.get("time_range", "This Month"))

        params = {
            "from_date": from_date,
            "to_date": to_date,
            "channel": filters.get("channel", "All Channels") or "All Channels",
            "region": filters.get("region", "All Regions") or "All Regions",
            "segment": filters.get("segment", "All Segments") or "All Segments",
        }

        query = """
        SELECT
            SUM(started),
            SUM(completed),
            SUM(failures),
            AVG(avg_time_minutes) / 60
        FROM dashboard_data
        WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        """

        result = client.query(query, parameters=params).result_rows

        if not result or not result[0]:
            return None

        started, completed, failures, avg_processing_hours = result[0]

        started = started or 0
        completed = completed or 0
        failures = failures or 0
        avg_processing_hours = avg_processing_hours or 0

        conversion_rate = (completed / started) * 100 if started else 0

        return {
            "started": int(started),
            "completed": int(completed),
            "failures": int(failures),
            "conversion_rate": float(conversion_rate),
            "avg_processing_hours": float(avg_processing_hours)
        }

    @staticmethod
    def get_baseline_metrics(filters: Dict):

        client = get_clickhouse_client()
        
        # for baseline context we compare roughly against everything strictly BEFORE from_date 
        from_date, to_date = get_date_range(filters.get("time_range", "This Month"))
        
        params = {
            "from_date": from_date,
            "channel": filters.get("channel", "All Channels") or "All Channels",
            "region": filters.get("region", "All Regions") or "All Regions",
            "segment": filters.get("segment", "All Segments") or "All Segments",
        }
        
        query = """
        SELECT
            AVG(started),
            AVG(completed),
            AVG(failures)
        FROM dashboard_data
        WHERE date < {from_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        """

        result = client.query(query, parameters=params).result_rows

        if not result or not result[0]:
            return None

        avg_started, avg_completed, avg_failures = result[0]

        avg_started = avg_started or 0
        avg_completed = avg_completed or 0
        avg_failures = avg_failures or 0

        avg_conversion = (avg_completed / avg_started) * 100 if avg_started else 0

        return {
            "avg_started": float(avg_started),
            "avg_completed": float(avg_completed),
            "avg_failures": float(avg_failures),
            "avg_conversion_rate": float(avg_conversion)
        }

    @staticmethod
    def get_product_metrics(filters: Dict):

        client = get_clickhouse_client()
        from_date, to_date = get_date_range(filters.get("time_range", "This Month"))

        params = {
            "from_date": from_date,
            "to_date": to_date,
            "channel": filters.get("channel", "All Channels") or "All Channels",
            "region": filters.get("region", "All Regions") or "All Regions",
            "segment": filters.get("segment", "All Segments") or "All Segments",
        }

        query = """
        SELECT
            product_name,
            SUM(started),
            SUM(completed),
            SUM(failures)
        FROM dashboard_data
        WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
          AND ({channel:String} = 'All Channels' OR channel = {channel:String})
          AND ({region:String} = 'All Regions' OR region = {region:String})
          AND ({segment:String} = 'All Segments' OR segment = {segment:String})
        GROUP BY product_name
        """

        result = client.query(query, parameters=params).result_rows
        products = []

        for row in result:

            product = row[0]
            started = row[1] or 0
            completed = row[2] or 0
            failures = row[3] or 0

            conversion_rate = (completed / started) * 100 if started else 0

            products.append({
                "product": product,
                "conversion_rate": conversion_rate,
                "failures": failures
            })

        return products