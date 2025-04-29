import logging


class LokiHandler(logging.Handler):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def emit(self, record):
        try:
            ts = self.logger.options.dynamic_labels.get("timestamp", lambda: "")()
            msg = self.format(record)
            self.logger.log_buffer.append((ts, f"[{record.levelname}] {msg}"))
            self.logger.flush_manager.check_and_flush()
        except Exception:
            pass

def intercept_logging(logger):
    handler = LokiHandler(logger)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
