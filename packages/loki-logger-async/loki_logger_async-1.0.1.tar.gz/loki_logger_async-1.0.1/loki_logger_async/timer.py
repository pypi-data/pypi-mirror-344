import threading

class FlushTimer:
    def __init__(self, flush_fn, interval: int):
        self.flush_fn = flush_fn
        self.interval = interval
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def schedule(self):
        with self._lock:
            if self._timer and self._timer.is_alive():
                return
            self._timer = threading.Timer(self.interval, self.flush_fn)
            self._timer.start()
