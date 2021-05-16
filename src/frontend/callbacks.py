import datetime
from src.constants import *

__all__ = ["get_list_stocks", "get_start_date", "get_end_date"]




def get_list_stocks() -> list:
    pass


def get_start_date(
    start_date: datetime.datetime = datetime.datetime(2019, 1, 1)
) -> datetime.datetime:
    return start_date


def get_end_date(
    end_date: datetime.datetime = datetime.date.today(),
) -> datetime.datetime:
    return end_date
