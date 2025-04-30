try:
    from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
except ImportError as exc:  # pragma: nocover
    ...


class Sqlalchemy:
    def __init__(self, dsn: str) -> None:
        self.store = SQLAlchemyJobStore(dsn)
