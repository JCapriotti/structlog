# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the MIT License.  See the LICENSE file in the root of this
# repository for complete details.


from structlog.contextvars import merge_contextvars
from structlog.decorators import log_call, log_context
from structlog._loggers import PrintLogger


class TestLogContext:
    def test_adds_variable(self):
        @log_context(a=1)
        def mock_func():
            return merge_contextvars(None, None, {"b": 2})

        assert {"a": 1, "b": 2} == mock_func()

    def test_removes_variable(self):
        @log_context(a=1)
        def mock_func():
            return merge_contextvars(None, None, {"b": 2})

        def mock_func_without_var():
            return merge_contextvars(None, None, {"b": 2})

        mock_func()

        assert {"b": 2} == mock_func_without_var()

    def test_adds_multiple_variables(self):
        @log_context(a=1, c=3)
        def mock_func():
            return merge_contextvars(None, None, {"b": 2})

        assert {"a": 1, "b": 2, "c": 3} == mock_func()

    def test_no_variables(self):
        @log_context()
        def mock_func():
            return merge_contextvars(None, None, {"b": 2})

        assert {"b": 2} == mock_func()


class TestLogCall:
    def test_logs_entry_exit(self, capsys):
        @log_call(PrintLogger())
        def mock_func():
            return

        mock_func()

        out, err = capsys.readouterr()
        assert "Entered mock_func\nExited mock_func\n" == out
        assert "" == err

# This does not have context
# @log_method(logger)
# @log_context({'location': 'auth/callback', 'emr': Emr.DSSmart.value})
#
# This DOES have context
# @log_context({'location': 'auth/callback', 'emr': Emr.DSSmart.value})
# @log_method(logger)
