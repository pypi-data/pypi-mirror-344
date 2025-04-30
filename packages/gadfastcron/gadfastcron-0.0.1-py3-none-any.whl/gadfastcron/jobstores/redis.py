import urllib.parse

from gadfastcron import const

try:
    from apscheduler.jobstores.redis import RedisJobStore
except ImportError as exc:  # pragma: nocover
    ...


class Redis:
    def __init__(self, dsn: str, jobs_key: str = "cron.jobs", run_times_key: str = "cron.run_times") -> None:
        parsed = urllib.parse.urlparse(dsn)
        db = parsed.path.lstrip(const.SYMBOL_FORWARD_SLASH)
        self.store = RedisJobStore(
            host=parsed.hostname,
            port=parsed.port,
            db=int(db),
            password=parsed.password,
            jobs_key=jobs_key,
            run_times_key=run_times_key,
        )
