def calculate_dropoff(previous: int, current: int) -> float:
    
    previous = previous or 0
    current = current or 0

    if previous == 0:
        return 0.0

    drop = ((previous - current) / previous) * 100

    return round(drop, 2)