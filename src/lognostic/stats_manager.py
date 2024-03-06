import pandas as pd
from threading import Lock


class StatsManager:
    def __init__(self):
        self._lock = Lock()
        self._records = []

    def add_record(self, logger_name, message_size):
        with self._lock:
            now = pd.Timestamp.now()
            self._records.append(
                {
                    "logger_name": logger_name,
                    "message_size": message_size,
                    "timestamp": now,
                }
            )

    def _dataframe(self):
        return pd.DataFrame(self._records)

    def _get_recent_records(self, lookback_period):
        df = self._dataframe()
        time_window = pd.Timestamp.now() - pd.Timedelta(seconds=lookback_period)
        recent = df[df["timestamp"] > time_window]
        return recent

    def get_total_size(self):
        df = self._dataframe()
        return df["message_size"].sum()

    def get_total_size_per_logger(self):
        df = self._dataframe()
        return df.groupby("logger_name")["message_size"].sum().to_dict()

    def get_total_logging_rate(self, lookback_period=60):
        recent_records = self._get_recent_records(lookback_period)
        return recent_records["message_size"].sum() / lookback_period

    def get_logging_rate_per_logger(self, lookback_period=60):
        recent_records = self._get_recent_records(lookback_period)
        return (
            recent_records.groupby("logger_name")["message_size"].sum()
            / lookback_period
        ).to_dict()
