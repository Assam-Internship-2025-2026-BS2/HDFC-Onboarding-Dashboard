from datetime import date
from app.core.database import get_clickhouse_client


class MetricsRepository:

    @staticmethod
    def get_today_metrics(metric_date: date):

        client = get_clickhouse_client()

        query = """
        SELECT
            SUM(started),
            SUM(completed),
            SUM(failures)
        FROM dashboard_data
        WHERE date = {metric_date:Date}
        """

        result = client.query(
            query,
            parameters={"metric_date": metric_date}
        ).result_rows

        if not result:
            return None

        started, completed, failures = result[0]

        started = started or 0
        completed = completed or 0
        failures = failures or 0

        conversion_rate = (completed / started) * 100 if started else 0

        return {
            "started": int(started),
            "completed": int(completed),
            "failures": int(failures),
            "conversion_rate": float(conversion_rate)
        }

    @staticmethod
    def get_baseline_metrics(metric_date: date):

        client = get_clickhouse_client()

        query = """
        SELECT
            AVG(started),
            AVG(completed),
            AVG(failures)
        FROM dashboard_data
        WHERE date < {metric_date:Date}
        """

        result = client.query(
            query,
            parameters={"metric_date": metric_date}
        ).result_rows

        if not result:
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
    def get_product_metrics(metric_date: date):

        client = get_clickhouse_client()

        query = """
        SELECT
            product_name,
            SUM(started),
            SUM(completed),
            SUM(failures)
        FROM dashboard_data
        WHERE date = {metric_date:Date}
        GROUP BY product_name
        """

        result = client.query(
            query,
            parameters={"metric_date": metric_date}
        ).result_rows

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