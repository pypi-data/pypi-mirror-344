"""
Logging instrumentation for DTA Observability.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from opentelemetry import trace
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from pythonjsonlogger.json import JsonFormatter as PythonJsonFormatter


class LogFieldMap:
    """Constants for log field mapping."""

    TIMESTAMP = "timestamp"
    SEVERITY = "severity"
    LOGGER = "logger"
    MESSAGE = "message"

    TRACE_ID = "logging.googleapis.com/trace"
    SPAN_ID = "logging.googleapis.com/spanId"
    TRACE_SAMPLED = "logging.googleapis.com/trace_sampled"

    OTEL_TRACE_ID = "otelTraceID"
    OTEL_SPAN_ID = "otelSpanID"
    OTEL_TRACE_SAMPLED = "otelTraceSampled"

    ERROR_TYPE = "error_type"
    ERROR_MESSAGE = "error_message"


class JsonFormatter(PythonJsonFormatter):
    """JSON formatter with proper RFC 3339 timestamps and GCP field mapping."""

    def __init__(self, *args, safe_logging: bool = True, **kwargs):
        """
        Initialize the JSON formatter.

        Args:
            safe_logging: Whether to enable extra handling for complex data types
            *args: Arguments for the parent class
            **kwargs: Keyword arguments for the parent class
        """
        super().__init__(*args, **kwargs)
        self.safe_logging = safe_logging

    def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
        """Format timestamp in RFC 3339 format with Z suffix."""

        isoformat = datetime.fromtimestamp(record.created).isoformat()
        return f"{isoformat}Z"

    def format(self, record: logging.LogRecord) -> str:
        """Format the record with complex type handling."""
        if not self.safe_logging:

            return super().format(record)

        original_msg = record.msg
        original_args = record.args
        original_extra = getattr(record, "extra", None)

        try:

            if hasattr(record, "extra") and isinstance(record.extra, dict):
                extra_copy = record.extra.copy()
                for key, value in list(extra_copy.items()):

                    if not isinstance(value, (str, int, float, bool, type(None))):
                        extra_copy[key] = self._serialize_value(value)
                record.extra = extra_copy

            if isinstance(record.args, dict):

                record.args = {k: self._serialize_value(v) for k, v in record.args.items()}
            elif isinstance(record.args, tuple):

                record.args = tuple(self._serialize_value(arg) for arg in record.args)
            elif record.args:

                record.args = self._serialize_value(record.args)
            else:

                record.args = ()

            if not isinstance(record.msg, str):
                record.msg = str(record.msg)

            return super().format(record)
        except Exception:

            record.msg = original_msg
            record.args = original_args
            if original_extra is not None:
                record.extra = original_extra

            try:

                if not isinstance(record.msg, str):
                    record.msg = str(record.msg)

                if isinstance(record.args, dict):
                    record.args = {k: str(v) for k, v in record.args.items()}
                elif isinstance(record.args, tuple):
                    record.args = tuple(str(arg) for arg in record.args)
                elif record.args is not None:
                    record.args = (str(record.args),)
                else:
                    record.args = ()

                if hasattr(record, "extra") and isinstance(record.extra, dict):
                    record.extra = {k: str(v) for k, v in record.extra.items()}

                return super().format(record)
            except Exception:

                return super().format(
                    logging.LogRecord(
                        name=record.name,
                        level=record.levelno,
                        pathname=record.pathname,
                        lineno=record.lineno,
                        msg=str(record.msg) if record.msg is not None else "",
                        args=(),
                        exc_info=record.exc_info,
                    )
                )

    def _serialize_value(self, value: Any) -> Any:
        """Serialize complex types to simpler format."""
        if value is None:
            return ""

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, (list, tuple)):
            if not value:
                return []

            if len(value) < 100:
                return [self._serialize_value(item) for item in value]

            try:
                return json.dumps(value)
            except (TypeError, ValueError):
                return str(value)

        if isinstance(value, dict):
            if not value:
                return {}

            if len(value) < 50:
                return {str(k): self._serialize_value(v) for k, v in value.items()}

            try:
                return json.dumps(value)
            except (TypeError, ValueError):
                return str(value)

        try:
            return json.dumps(value)
        except (TypeError, ValueError):
            try:
                return str(value)
            except Exception:
                return "[Unconvertible Object]"


class ComplexLogger(logging.Logger):
    """Logger that handles complex types automatically."""

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """Override _log to ensure complex types are handled consistently."""

        if extra is None:
            extra = {}
        elif not isinstance(extra, dict):

            try:
                extra = {"extra": str(extra)}
            except Exception:
                extra = {"extra": "[Unconvertible Object]"}

        safe_extra = {}
        for key, value in extra.items():
            if isinstance(value, (dict, list, tuple)):
                try:

                    safe_extra[key] = json.dumps(value)
                except (TypeError, ValueError):

                    safe_extra[key] = str(value)
            else:
                safe_extra[key] = value

        super()._log(level, msg, args, exc_info, safe_extra, stack_info, stacklevel)


logging.setLoggerClass(ComplexLogger)


class LogRecordFilter(logging.Filter):
    """Filter that ensures all log records have necessary attributes for JSON formatting."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Ensure records have required OTEL attributes.

        Args:
            record: The log record to filter

        Returns:
            True to include the record (always)
        """

        if not hasattr(record, "otelTraceID"):
            record.otelTraceID = ""
        if not hasattr(record, "otelSpanID"):
            record.otelSpanID = ""
        if not hasattr(record, "otelTraceSampled"):
            record.otelTraceSampled = ""
        return True


class LoggingConfigurator:
    """Manages logging configuration."""

    _configured = False

    @classmethod
    def is_configured(cls) -> bool:
        """Check if logging has been configured."""
        return cls._configured

    @classmethod
    def mark_configured(cls) -> None:
        """Mark logging as configured."""
        cls._configured = True

    @staticmethod
    def reset_instrumented_logger_levels(level: int) -> None:
        """
        Reset all logger levels according to the configured policy.

        Args:
            level: The application log level to apply
        """

        LoggingConfigurator.configure_logger_levels(level)

    @staticmethod
    def create_formatter(safe_logging: bool = True) -> JsonFormatter:
        """
        Create a JSON formatter with proper field mapping.

        Args:
            safe_logging: Whether to enable safe logging
        """
        return JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(otelTraceID)s %(otelSpanID)s %(otelTraceSampled)s",
            safe_logging=safe_logging,
            rename_fields={
                "levelname": LogFieldMap.SEVERITY,
                "asctime": LogFieldMap.TIMESTAMP,
                "name": LogFieldMap.LOGGER,
                LogFieldMap.OTEL_TRACE_ID: LogFieldMap.TRACE_ID,
                LogFieldMap.OTEL_SPAN_ID: LogFieldMap.SPAN_ID,
                LogFieldMap.OTEL_TRACE_SAMPLED: LogFieldMap.TRACE_SAMPLED,
            },
        )

    @staticmethod
    def create_handler(
        level: int, logger_provider: Optional[LoggerProvider] = None, safe_logging: bool = True
    ) -> LoggingHandler:
        """
        Create a logging handler with proper formatting.

        Args:
            level: The logging level
            logger_provider: Optional logger provider
            safe_logging: Whether to enable safe logging
        """
        handler = LoggingHandler(level=level, logger_provider=logger_provider)
        handler.setFormatter(LoggingConfigurator.create_formatter(safe_logging=safe_logging))

        setattr(handler, "_dta_otel_handler", True)

        return handler

    @staticmethod
    def configure_root_logger(level: int, handler: logging.Handler, replace_existing: bool) -> None:
        """Configure the root logger."""
        root_logger = logging.getLogger()
        root_logger.setLevel(level)

        if replace_existing or not root_logger.handlers:

            for existing_handler in root_logger.handlers[:]:
                root_logger.removeHandler(existing_handler)
            root_logger.addHandler(handler)

        special_loggers = ["fastapi.access", "werkzeug", "uvicorn", "uvicorn.access", "uvicorn.error"]

        for logger_name in special_loggers:
            special_logger = logging.getLogger(logger_name)
            special_logger.setLevel(level)

            special_logger.propagate = True

            for handler in list(special_logger.handlers):
                if not hasattr(handler, "_dta_otel_handler"):
                    special_logger.removeHandler(handler)

    @staticmethod
    def ensure_all_loggers_propagate() -> None:
        """Ensure all loggers propagate to the root logger."""
        for name in logging.root.manager.loggerDict:
            logger = logging.getLogger(name)
            logger.propagate = True

    @staticmethod
    def configure_logger_levels(app_level: int) -> None:
        """
        Configure all logger levels based on a consistent policy:
        - DTA and framework loggers: Use application log level
        - Third-party loggers: ERROR, unless app_level is DEBUG (then DEBUG)

        Args:
            app_level: The application log level
        """

        third_party_level = logging.ERROR
        if app_level <= logging.DEBUG:
            third_party_level = logging.DEBUG

        framework_loggers = {"werkzeug", "flask.access", "fastapi.access", "uvicorn", "uvicorn.access", "uvicorn.error"}

        for name in logging.root.manager.loggerDict:
            logger = logging.getLogger(name)

            if name in framework_loggers:
                logger.setLevel(app_level)
                logger.propagate = True
                continue

            if hasattr(logger, "_dta_instrumented_logger"):
                logger.setLevel(app_level)
                logger.propagate = True
                continue

            logger.setLevel(third_party_level)
            logger.propagate = True

    @staticmethod
    def configure_library_logger(level: int, handler: logging.Handler) -> None:
        """Configure the DTA Observability library logger."""
        lib_logger = logging.getLogger("dta_observability")
        lib_logger.setLevel(level)

        for existing_handler in lib_logger.handlers[:]:
            lib_logger.removeHandler(existing_handler)

        lib_logger.addHandler(handler)
        lib_logger.propagate = True


class DTAErrorHandler:
    """Custom error handler for DTA Observability."""

    def handle(self, error: Exception) -> None:
        """
        Handle errors by logging them with trace context.

        Args:
            error: The exception to handle
        """
        logger = get_logger("dta_observability.error")

        current_span = trace.get_current_span()
        span_context = current_span.get_span_context() if current_span else None

        error_context: Dict[str, Any] = {
            LogFieldMap.ERROR_TYPE: error.__class__.__name__,
            LogFieldMap.ERROR_MESSAGE: str(error),
        }

        if span_context:
            error_context.update(
                {
                    "trace_id": span_context.trace_id,
                    "span_id": span_context.span_id,
                }
            )

        logger.error(
            "Error caught by DTA error handler",
            extra=error_context,
            exc_info=error,
        )


def get_logger(name: str) -> logging.Logger:
    """
    Get an instrumented logger with the given name.

    The logger will respect the log level set in init_telemetry.
    All instrumented loggers will have their log level set
    based on the app log level, while third-party loggers
    will be restricted to ERROR (or DEBUG if app is in DEBUG mode).

    Args:
        name: Name for the logger, typically the module name

    Returns:
        A configured Logger instance with JSON formatting and trace context
    """
    logger = logging.getLogger(name)

    logger.propagate = True

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    setattr(logger, "_dta_instrumented_logger", True)

    return logger
