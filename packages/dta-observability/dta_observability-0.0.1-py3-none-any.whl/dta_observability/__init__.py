"""
DTA Observability - A lightweight wrapper around OpenTelemetry core APIs.
"""

__version__ = "0.1.0"

from dta_observability.core.span import (
    SpanAttribute,
    SpanAttributeValue,
    add_span_attribute,
    add_span_attributes,
    create_span,
    get_current_span,
    mark_error_event,
    set_span_status,
    traced,
)
from dta_observability.core.telemetry import init_telemetry
from dta_observability.logging.logger import get_logger

__all__ = [
    "init_telemetry",
    "get_logger",
    "traced",
    "create_span",
    "mark_error_event",
    "add_span_attribute",
    "add_span_attributes",
    "set_span_status",
    "set_log_level",
    "get_current_span",
    "SpanAttribute",
    "SpanAttributeValue",
]


def set_log_level(level: int) -> None:
    """
    Set the log level for all loggers using the consistent policy:
    - DTA and framework loggers: Use the provided log level
    - Third-party loggers: ERROR, unless level is DEBUG (then DEBUG)

    This allows changing the log level after initialization, which can be
    useful for debugging or temporarily adjusting verbosity.

    Args:
        level: The log level to set (e.g., logging.DEBUG, logging.INFO)
    """
    from dta_observability.logging.logger import LoggingConfigurator

    LoggingConfigurator.configure_logger_levels(level)

    get_logger("dta_observability").info(f"Log level updated to {level}")
