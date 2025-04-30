import datetime

from apscheduler.triggers.date import DateTrigger


def time(date: datetime.datetime) -> DateTrigger:
    return DateTrigger(run_date=date)
