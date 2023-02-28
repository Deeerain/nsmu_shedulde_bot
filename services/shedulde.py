from datetime import date
from calendar import monthrange

from nsmu_parser.parser import get_list


def shedulde_by_group(link: str, shedulde_time: str):
    today_date = date.today()
    tomorow_date = get_tomorrow_date(today_date)

    if shedulde_time == 'today':
        return get_list(today_date, link)

    if shedulde_time == 'tomorrow':
        return get_list(tomorow_date, link)


def get_tomorrow_date(today: date) -> date:
    weekday, days_in_month = monthrange(today.year, today.month)

    tomorrow_day: int = today.day + 1
    month: int = today.month

    if tomorrow_day > days_in_month:
        tomorrow_day = 1
        month += 1

    return date(today.year, month, tomorrow_day)
