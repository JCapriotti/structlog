# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the MIT License.  See the LICENSE file in the root of this
# repository for complete details.


from functools import partial, wraps

from structlog.contextvars import bind_contextvars, unbind_contextvars


def log_context(func=None, /, **contextvars):
    if func is None:
        return partial(log_context, contextvars)

    @wraps(func)
    def wrapped_func(*args, **kwargs):
        bind_contextvars(**contextvars)
        func_ret = func(*args, **kwargs)
        unbind_contextvars(*contextvars.keys())
        return func_ret
    return wrapped_func


def log_call(logger):
    def wrap(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            logger.info("Entered " + func.__name__)
            func_ret = func(*args, **kwargs)
            logger.info("Exited " + func.__name__)
            return func_ret
        return wrapped_func
    return wrap
