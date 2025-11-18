import time
from functools import wraps

def retry(retries=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        raise last_error
        return wrapper
    return decorator
