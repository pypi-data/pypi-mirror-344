import datetime
import hashlib
import typing

from apscheduler.jobstores.base import BaseJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger


class Cron:
    def __init__(
        self,
        store: BaseJobStore,
        *jobs: tuple[typing.Callable, CronTrigger | DateTrigger, dict[str, typing.Any] | None],
    ) -> None:
        self.scheduler = AsyncIOScheduler(
            timezone=datetime.UTC,
            jobstores={"default": store},
            job_defaults={
                "coalesce": False,
                "max_instances": 1,
            },
        )

        for job in jobs:
            match job:
                case (func, trigger):
                    kwargs = {}
                case (func, trigger, kwargs):
                    kwargs = kwargs or {}
                case _:
                    continue
            self.add(func, trigger, kwargs)

    def add(
        self,
        func: typing.Callable,
        trigger: CronTrigger | DateTrigger,
        kwargs: dict[str, typing.Any] | None = None,
    ) -> None:
        self.scheduler.add_job(
            func,
            trigger,
            id=hashlib.md5(f"{func.__name__}-{kwargs.__str__()}".encode()).hexdigest(),
            replace_existing=True,
            misfire_grace_time=3600,
            kwargs=kwargs,
        )

    def start(self) -> None:
        self.scheduler.start()

    def shutdown(self) -> None:
        self.scheduler.shutdown()
