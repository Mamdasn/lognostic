import logging
import unittest
from datetime import datetime
from threading import Thread
from unittest.mock import Mock, patch

import pandas as pd

from lognostic import Lognostic


class TestLognostic(unittest.TestCase):

    def setUp(self) -> None:
        """Create a Lognostic instance before each test."""
        self.lognostic = Lognostic()

    @patch("pandas.Timestamp.now")
    def test_record(self, now_mock: Mock) -> None:
        """Test that log records are correctly recorded."""
        now_mock.return_value = pd.Timestamp(datetime(2024, 3, 6, 12))
        log_record = logging.LogRecord(
            "test_logger", logging.INFO, "", 0, "test message", args=(), exc_info=None
        )
        self.lognostic.record(log_record)

        self.assertEqual(len(self.lognostic._records), 1)
        self.assertEqual(self.lognostic._records[0]["logger_name"], "test_logger")
        self.assertEqual(
            self.lognostic._records[0]["message_size"], len("test message")
        )
        self.assertEqual(
            self.lognostic._records[0]["timestamp"],
            pd.Timestamp(datetime(2024, 3, 6, 12)),
        )

    def test_total_size(self) -> None:
        """Test calculation of the total size of logged messages."""
        self.lognostic._records = [
            {
                "logger_name": "logger1",
                "message_size": 10,
                "timestamp": pd.Timestamp.now(),
            },
            {
                "logger_name": "logger2",
                "message_size": 20,
                "timestamp": pd.Timestamp.now(),
            },
        ]
        self.assertEqual(self.lognostic.total_size(), 30)

    def test_total_size_per_logger(self) -> None:
        """Test calculation of the total size of logged messages per logger."""
        self.lognostic._records = [
            {
                "logger_name": "logger1",
                "message_size": 10,
                "timestamp": pd.Timestamp.now(),
            },
            {
                "logger_name": "logger1",
                "message_size": 15,
                "timestamp": pd.Timestamp.now(),
            },
            {
                "logger_name": "logger2",
                "message_size": 20,
                "timestamp": pd.Timestamp.now(),
            },
        ]
        expected = {"logger1": 25, "logger2": 20}
        self.assertEqual(self.lognostic.total_size_per_logger(), expected)

    @patch("pandas.Timestamp.now")
    def test_total_logging_rate(self, now_mock: Mock) -> None:
        """Test calculation of the total logging rate over a specified period."""
        now_mock.return_value = pd.Timestamp(datetime(2024, 3, 6, 12))
        self.lognostic._records = [
            {
                "logger_name": "logger",
                "message_size": 60,
                "timestamp": pd.Timestamp(datetime(2024, 3, 6, 12)),
            },
        ]
        self.assertAlmostEqual(self.lognostic.total_logging_rate(lookback_period=1), 60)

    @patch("pandas.Timestamp.now")
    def test_logging_rate_per_logger(self, now_mock: Mock) -> None:
        """Test calculation of the logging rate per logger over a specified period."""
        now_mock.return_value = pd.Timestamp(datetime(2024, 3, 6, 12))
        self.lognostic._records = [
            {
                "logger_name": "logger1",
                "message_size": 30,
                "timestamp": pd.Timestamp(datetime(2024, 3, 6, 12)),
            },
            {
                "logger_name": "logger2",
                "message_size": 60,
                "timestamp": pd.Timestamp(datetime(2024, 3, 6, 12)),
            },
        ]
        expected = {"logger1": 0.5, "logger2": 1.0}
        self.assertEqual(
            self.lognostic.logging_rate_per_logger(lookback_period=60), expected
        )

    def test_thread_safety(self) -> None:
        """Test that the Lognostic record method is thread-safe."""
        logging.getLogger("TestLogger")
        log_record1 = logging.LogRecord(
            "logger-1", logging.INFO, "", 0, "test message 1", args=(), exc_info=None
        )
        log_record2 = logging.LogRecord(
            "logger-2",
            logging.INFO,
            "",
            0,
            "test message 2",
            args=(),
            exc_info=None,
        )

        def target1() -> None:
            for _ in range(50):
                self.lognostic.record(log_record1)

        def target2() -> None:
            for _ in range(50):
                self.lognostic.record(log_record2)

        thread1 = Thread(target=target1)
        thread2 = Thread(target=target2)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Check if all records are added
        df = pd.DataFrame(self.lognostic._records)
        logger1_count = len(df[df["logger_name"] == "logger-1"])
        logger2_count = len(df[df["logger_name"] == "logger-2"])

        self.assertEqual(logger1_count, 50, "Logger1 did not log 100 messages.")
        self.assertEqual(logger2_count, 50, "Logger2 did not log 100 messages.")
