import builtins

def intercept_print(logger):
    original_print = builtins.print

    def custom_print(*args, **kwargs):
        ts = logger.options.dynamic_labels.get("timestamp", lambda: "")()
        message = " ".join(str(a) for a in args)
        logger.log_buffer.append((ts, f"[PRINT] {message}"))
        logger._check_flush()
        original_print(*args, **kwargs)

    builtins.print = custom_print
