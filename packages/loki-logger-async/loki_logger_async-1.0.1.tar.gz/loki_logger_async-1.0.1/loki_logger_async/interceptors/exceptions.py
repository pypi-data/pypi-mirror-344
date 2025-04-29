import sys
import traceback

def intercept_exceptions(logger):
    original_hook = sys.excepthook

    def custom_hook(exc_type, exc_value, exc_traceback):
        ts = logger.options.dynamic_labels.get("timestamp", lambda: "")()
        error_message = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.log_buffer.append((ts, f"[EXCEPTION] {error_message}"))
        logger.flush_logs()
        original_hook(exc_type, exc_value, exc_traceback)

    sys.excepthook = custom_hook
