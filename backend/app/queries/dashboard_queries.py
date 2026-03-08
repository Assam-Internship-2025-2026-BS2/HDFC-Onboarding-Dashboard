def executive_aggregate_query():
    
    return """
    SELECT
        SUM(started) AS total_started,
        SUM(submitted) AS total_submitted,
        SUM(in_progress) AS total_in_progress,
        SUM(completed) AS total_completed,
        SUM(approved) AS total_approved,
        SUM(failures) AS total_failures,

        AVG(avg_time_minutes) AS avg_completion_time,
        AVG(sla_target_minutes) AS avg_sla_target,

        SUM(pipeline_total_cr) AS pipeline_total_cr,
        SUM(pipeline_risk_cr) AS pipeline_risk_cr,

        SUM(sla_breached) AS total_sla_breached,
        SUM(stuck_24h) AS stuck_24h

    FROM dashboard_data

    WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
      AND ({channel:String} = 'All Channels' OR channel = {channel:String})
      AND ({region:String} = 'All Regions' OR region = {region:String})
      AND ({segment:String} = 'All Segments' OR segment = {segment:String})
    """
    
def max_product_time_query():

    return """
    SELECT
        product_name,
        MAX(avg_time_minutes) AS max_time

    FROM dashboard_data

    WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
      AND ({channel:String} = 'All Channels' OR channel = {channel:String})
      AND ({region:String} = 'All Regions' OR region = {region:String})
      AND ({segment:String} = 'All Segments' OR segment = {segment:String})

    GROUP BY product_name
    ORDER BY max_time DESC
    LIMIT 1
    """
    
def product_alerts_query():

    return """
    SELECT
        product_name,

        SUM(started) AS started,
        SUM(completed) AS completed,
        SUM(approved) AS approved,
        SUM(failures) AS failures,
        SUM(sla_breached) AS sla_breached

    FROM dashboard_data

    WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
      AND ({channel:String} = 'All Channels' OR channel = {channel:String})
      AND ({region:String} = 'All Regions' OR region = {region:String})
      AND ({segment:String} = 'All Segments' OR segment = {segment:String})

    GROUP BY product_name
    """

def channel_distribution_query():
    
    return """
    SELECT
        channel,
        SUM(submitted) as total_submitted
    FROM dashboard_data
    WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
      AND ({channel:String} = 'All Channels' OR channel = {channel:String})
      AND ({region:String} = 'All Regions' OR region = {region:String})
      AND ({segment:String} = 'All Segments' OR segment = {segment:String})
    GROUP BY channel
    """


def trend_analysis_query():
    
    return """
    SELECT
        date,
        SUM(started) as total_started,
        SUM(completed) as total_completed
    FROM dashboard_data
    WHERE date BETWEEN {from_date:Date} AND {to_date:Date}
      AND ({channel:String} = 'All Channels' OR channel = {channel:String})
      AND ({region:String} = 'All Regions' OR region = {region:String})
      AND ({segment:String} = 'All Segments' OR segment = {segment:String})
    GROUP BY date
    ORDER BY date ASC
    """