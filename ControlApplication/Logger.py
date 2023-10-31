import datetime
from enum import Enum

class Logger:

    class LogLevel(Enum):
        ERROR = 1,
        INFO = 2

    DELIMITER = "-" * 60

    def __init__(self, log_filename):
        self.log_filename = log_filename

    def logMessage(self, message, level = None, use_delimiter = False, timestamp = False):
        log_message = message

        if timestamp:
            log_message = f"[{datetime.datetime.now()}] " + log_message
        if level:
            log_message = f"[{level.name}] " + log_message
        if use_delimiter:
            log_message = f"{self.DELIMITER}\n" + log_message + f"\n{self.DELIMITER}"

        with open(self.log_filename, "a") as file:
            file.write(f"{log_message}\n")