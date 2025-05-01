'''
Logging handler
'''
from typing import Iterable
import logging
import tqdm


class Color:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class Formatter(logging.Formatter):
    datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        timestamp = self.formatTime(record, self.datefmt)

        # Format the message
        levelcolor = Color.fg.lightblue
        if record.levelname == 'INFO':
            levelcolor = Color.fg.green
        elif record.levelname == 'WARNING':
            levelcolor = Color.fg.yellow
        elif record.levelname == 'ERROR':
            levelcolor = Color.fg.red
        log_message = f"{Color.bold}{timestamp}{Color.reset} | {levelcolor}{record.levelname:<8}{Color.reset} | {record.getMessage()}"
        return log_message


class Logger:
    def __init__(self, name=__name__, log_file: str = None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        # Formatter
        formatter = Formatter()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def __call__(self, *args, **kwds):
        self.debug(*args, **kwds)

    def debug(self, *args, **kwds):
        self.logger.debug(*args, **kwds)

    def info(self, *args, **kwds):
        self.logger.info(*args, **kwds)

    def warning(self, *args, **kwds):
        self.logger.warning(*args, **kwds)

    def error(self, *args, **kwds):
        self.logger.error(*args, **kwds)

    def progress(self, iterator: Iterable, total: int = None, desc: str = None):
        timestamp = Formatter().formatTime(logging.makeLogRecord({}))
        return tqdm.tqdm(iterator, total=total, desc=f"{Color.bold}{timestamp}{Color.reset}{f'| {desc}' if desc else ''}", file=self.logger.handlers[0].stream)


log = Logger()
