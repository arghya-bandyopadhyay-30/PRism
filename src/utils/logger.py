import os
import sys
import json
from loguru import logger
from threading import Lock

class PrismLogger:
    _instance = None
    _lock = Lock()
    _env = os.environ.get("PRISM_ENV", "dev").lower()

    def __init__(self):
        raise RuntimeError("Use get_instance() to access the logger.")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls.__new__(cls)
                    cls._instance._setup(logger)
        return cls._instance._logger

    def _setup(self, loguru_logger):
        loguru_logger.remove()

        if self._env == "dev":
            loguru_logger.add(
                sys.stdout,
                format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                colorize=True
            )
        else:
            patched_logger = loguru_logger.patch(PrismLogger._patch_record)
            patched_logger.add(sys.stdout, format="{extra[serialized]}")
            self._logger = patched_logger
            return

        self._logger = loguru_logger

    @staticmethod
    def _patch_record(record):
        record["extra"]["serialized"] = PrismLogger._serialize(record)

    @staticmethod
    def _serialize(record):
        return json.dumps({
            "timestamp": str(record["time"]),
            "level": record["level"].name,
            "message": record["message"],
            "file": record["file"].path,
            "function": record["function"],
            "line": record["line"],
            **record["extra"]
        })
