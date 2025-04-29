from pymongo import MongoClient
import os
import logging
import datetime as dt

logger = logging.getLogger(__name__)

class MongoLogger(logging.Handler):
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern: ensures only one MongoLogger instance is created."""
        if cls._instance is None:
            cls._instance = super(MongoLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, mongo_uri=None, db_name=None, collection_name="logs"):
        """
        Initialize the MongoLogger.

        Args:
            mongo_uri (str): MongoDB URI'
            db_name (str): Database name to log into.
            collection_name (str): Collection name for logs.
        """
        super().__init__()

        if not mongo_uri or not db_name:
            raise ValueError("You must provide both 'mongo_uri' and 'db_name'.")

        if MongoLogger._client is None:
            MongoLogger._client = MongoClient(mongo_uri)

        self.db = MongoLogger._client[db_name]
        self.collection = self.db[collection_name]

    def emit(self, record):
        """Emit log record to MongoDB."""
        log_entry = self.format(record)
        container_name = os.getenv("HOSTNAME", "unknown_container")
        log_doc = {
            "message": log_entry,
            "level": record.levelname,
            "container": container_name,
            "func": record.funcName,
            "line": record.lineno,
            "timestamp": dt.datetime.utcnow(),  # Use UTC time
        }

        try:
            self.collection.insert_one(log_doc)
        except Exception as e:
            print(f"Failed to write log to MongoDB: {e}")
