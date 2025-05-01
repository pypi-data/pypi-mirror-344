from enum import Enum


class TimeFilter(str, Enum):
    TOP_HOUR = "top_hour"
    TOP_NOW = "top_now"
    TOP_THIS_MONTH = "top_this_month"
    TOP_THIS_WEEK = "top_this_week"
    TOP_THIS_YEAR = "top_this_year"
    TOP_TODAY = "top_today"

    def __str__(self) -> str:
        return str(self.value)
