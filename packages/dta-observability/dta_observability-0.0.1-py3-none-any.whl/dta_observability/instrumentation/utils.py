"""
Instrumentation utilities for DTA Observability.
"""

import logging
from typing import Any


def handle_instrumentation_error(
    logger: logging.Logger, library_name: str, error: Exception, context: str = "instrumentation"
) -> None:
    """
    Handle instrumentation errors consistently.

    Args:
        logger: Logger to use for recording errors
        library_name: The name of the library that failed to instrument
        error: The exception that was raised
        context: Context where the error occurred (default: "instrumentation")
    """
    logger.warning("Failed to instrument %s (%s): %s - %s", library_name, context, error.__class__.__name__, str(error))
    logger.debug("Instrumentation error details", exc_info=error)


def check_instrumentation_status(object_to_check: Any, library_name: str, attr_name: str) -> bool:
    """
    Check if an object has already been instrumented.

    Args:
        object_to_check: The object to check for instrumentation status
        library_name: The name of the library being instrumented (for logging)
        attr_name: The attribute name that marks the object as instrumented

    Returns:
        True if the object is already instrumented, False otherwise
    """
    return hasattr(object_to_check, attr_name) and bool(getattr(object_to_check, attr_name))


def mark_as_instrumented(object_to_mark: Any, attr_name: str, instrumented: bool = True) -> None:
    """
    Mark an object as instrumented.

    Args:
        object_to_mark: The object to mark as instrumented
        attr_name: The attribute name to use as marker
        instrumented: The value to set (default: True)
    """
    setattr(object_to_mark, attr_name, instrumented)
