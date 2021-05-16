import pytest
import datetime
from src.frontend.callbacks import *


@pytest.fixture
def start_date() -> datetime.datetime:
    return datetime.datetime(2019, 1, 1)


@pytest.fixture
def end_date() -> datetime.datetime:
    end_date = datetime.date.today()
    return end_date


class TestCallBacks:
    def test_get_dates(self, start_date, end_date):
        assert get_start_date() == start_date
        assert get_end_date() == end_date
