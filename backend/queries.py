def onboarding_started_query():

    return """
    SELECT count()
    FROM onboarding
    WHERE status='started'
    """


def onboarding_completed_query():

    return """
    SELECT count()
    FROM onboarding
    WHERE status='completed'
    """


def dropoff_query():

    return """
    SELECT count()
    FROM onboarding
    WHERE status='dropoff'
    """


def avg_time_query():

    return """
    SELECT avg(processing_time)
    FROM onboarding
    """