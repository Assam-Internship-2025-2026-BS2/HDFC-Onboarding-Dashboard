from datetime import datetime, timedelta

def get_date_range(time_range):

    today = datetime.today().date()

    if time_range == "Today":
        return today, today

    elif time_range == "Yesterday":
        y = today - timedelta(days=1)
        return y, y

    elif time_range == "Last 7 Days":
        return today - timedelta(days=7), today

    elif time_range == "Last 30 Days":
        return today - timedelta(days=30), today

    else:
        return today.replace(day=1), today
