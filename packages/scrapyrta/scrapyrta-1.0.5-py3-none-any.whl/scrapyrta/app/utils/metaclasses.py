import threading
from typing import ClassVar


class Singleton(type):
    _instances: ClassVar[dict] = {}
    _lock = threading.Lock()  # to synchronize threads (if we had any)

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
