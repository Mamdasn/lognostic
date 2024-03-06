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

    def get_total_size(self):
        df = pd.DataFrame(self._records)
        return df["message_size"].sum()

    def get_total_size_per_logger(self):
        df = pd.DataFrame(self._records)
        return df.groupby("logger_name")["message_size"].sum().to_dict()

    def get_total_logging_rate(self, since_seconds=60):
        df = pd.DataFrame(self._records)
        time_window = pd.Timestamp.now() - pd.Timedelta(seconds=since_seconds)
        recent = df[df["timestamp"] > time_window]
        return recent["message_size"].sum() / since_seconds

    def get_logging_rate_per_logger(self, since_seconds=60):
        df = pd.DataFrame(self._records)
        time_window = pd.Timestamp.now() - pd.Timedelta(seconds=since_seconds)
        recent = df[df["timestamp"] > time_window]
        return (
            recent.groupby("logger_name")["message_size"].sum() / since_seconds
        ).to_dict()
