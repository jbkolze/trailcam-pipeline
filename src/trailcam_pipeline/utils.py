from datetime import date, timedelta


def get_date_list(start_date: date, end_date: date) -> list[date]:
    dates: list[date] = []

    cur_date = start_date
    while cur_date <= end_date:
        dates.append(cur_date)
        cur_date = cur_date + timedelta(days=1)

    return dates
