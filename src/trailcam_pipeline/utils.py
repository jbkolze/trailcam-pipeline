from datetime import date, datetime, timedelta


def get_date_list(start_date: date, end_date: date) -> list[date]:
    dates: list[date] = []

    cur_date = start_date
    while cur_date <= end_date:
        dates.append(cur_date)
        cur_date = cur_date + timedelta(days=1)

    return dates


def get_datetimes_midpoint(start_dt: datetime, end_dt: datetime):
    if start_dt == end_dt:
        return start_dt
    time_diff = end_dt - start_dt
    half_diff = time_diff / 2
    midpoint = start_dt + half_diff
    return midpoint


def normalize_list(data: list[float]):
    total = sum(data)
    normal_data = [datum / total for datum in data]
    return normal_data


def smooth_circular_list(data: list[int], window: int = 4):
    n = len(data)
    smoothed: list[float] = []

    for i in range(n):
        total = 0
        count = 0
        for k in range(-window, window + 1):
            total += data[(i + k) % n]
            count += 1
        smoothed.append(total / count)

    return smoothed
