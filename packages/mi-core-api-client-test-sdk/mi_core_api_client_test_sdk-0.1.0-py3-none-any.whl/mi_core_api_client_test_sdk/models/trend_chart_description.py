from enum import Enum


class TrendChartDescription(str, Enum):
    DECLINING_TREND = "Declining trend"
    STEADY_GROWTH = "Steady growth"

    def __str__(self) -> str:
        return str(self.value)
