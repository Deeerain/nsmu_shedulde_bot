from datetime import date

from nsmu_parser.parser import get_list


def shedulde_by_group(link: str, shedulde_time: str):
    today_date = date.today()
    tomoroww_date = date(today_date.year, today_date.month, today_date.day + 1)

    if shedulde_time == 'today':
        return get_list(today_date, link)

    if shedulde_time == 'tomorrow':
        return get_list(tomoroww_date, link)
