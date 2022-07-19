import os
import datetime
from rich.console import Console
import threading 

LOCK = threading.Lock()
console = Console(highlight=False)

COLORS = {
    'warning': 'yellow',
    'error': 'red',
    'info': 'green',
    'debug': 'blue'
}


class Logger:
    """
    
    THREAD UNSAFE LOGGER

    """

    def __init__(
        self,
        module_name: str = __name__,
        log_file: str = 'app.log',
        show_module: bool = True,
        show_time: bool = True
    ):

        self.log_file = open(log_file, 'a', encoding='utf-8')
        self.module_name = module_name
        self.show_module = show_module
        self.show_time = show_time

        self.console = Console(highlight=False, file=self.log_file)

    def info(self, *args, **kwargs):
        level = 'info'
        self._print(level, *args, **kwargs)

    def warn(self, *args, **kwargs):
        level = 'warning'
        self._print(level, *args, **kwargs)

    def error(self, *args, **kwargs):
        level = 'error'
        self._print(level, *args, **kwargs)

    def debug(self, *args, **kwargs):
        level = 'debug'
        self._print(level, *args, **kwargs)

    def _print(
        self,
        level: str,
        *args,
        **kwargs
    ):

        color = COLORS.get(level)
        time = '[' + datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p') + ']'
        module = '[' + self.module_name
        pid = str(os.getpid()).ljust(5) + ']'
        log_level = f'[{level.upper()}'.ljust(8) + ']'

        LOCK.acquire()

        try:
            # terminal printing
            console.print(time, module, pid, log_level, *
                        args, **kwargs, style=f"{color}")
        except:
            pass

        LOCK.release()

        try:
            # file printing
            self.console.print(time, module, pid, log_level, *
                            args, **kwargs, style=f"{color}")
        except:
            pass
        finally:
            self.log_file.flush()