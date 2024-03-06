import logging
from typing import Dict
from .stats_manager import StatsManager


class Lognostic:
    def __init__(self) -> None:
        self._stats_manager = StatsManager()

    def record(self, log_record: logging.LogRecord) -> None:
        logger_name: str = log_record.name
        message_size: int = len(log_record.getMessage())
        self._stats_manager.add_record(logger_name, message_size)

    def total_size(self) -> int:
        return self._stats_manager.get_total_size()

    def total_size_per_logger(self) -> Dict[str, int]:
        return self._stats_manager.get_total_size_per_logger()

    def total_logging_rate(self, lookback_period: int = 60) -> float:
        return self._stats_manager.get_total_logging_rate(lookback_period)

    def logging_rate_per_logger(self, lookback_period: int = 60) -> Dict[str, float]:
        return self._stats_manager.get_logging_rate_per_logger(lookback_period)
