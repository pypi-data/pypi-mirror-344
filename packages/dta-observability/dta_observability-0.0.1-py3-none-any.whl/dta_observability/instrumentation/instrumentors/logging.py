"""
Logging-specific instrumentation for DTA Observability.
"""

import logging
import sys
from typing import Any, Optional

from opentelemetry.instrumentation.logging import LoggingInstrumentor as OTelLoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import TracerProvider

from dta_observability.instrumentation.registry import instrumentation_registry
from dta_observability.instrumentation.utils import handle_instrumentation_error
from dta_observability.logging.logger import LoggingConfigurator


class LoggingInstrumentor:
    """
    Handles logging-specific instrumentation.

    This class is standalone to avoid circular dependencies with the logging module.
    """

    _INSTRUMENTED_KEY = "_dta_logging_instrumented"

    def __init__(
        self,
        tracer_provider: Optional[TracerProvider] = None,
        logger_provider: Optional[LoggerProvider] = None,
        log_level: int = logging.INFO,
        safe_logging: bool = True,
    ):
        """
        Initialize the logging instrumentor.

        Args:
            tracer_provider: Optional tracer provider
            logger_provider: Optional logger provider
            log_level: The logging level to use
            safe_logging: Whether to enable safe logging with complex data types
        """
        self.tracer_provider = tracer_provider
        self.logger_provider = logger_provider
        self.log_level = log_level
        self.safe_logging = safe_logging
        self.logger = self._get_simple_logger()

    def _get_simple_logger(self) -> logging.Logger:
        """
        Get a simple logger that doesn't trigger instrumentation loops.

        Returns:
            A simple logger that logs to stdout
        """
        logger = logging.getLogger("dta_observability.instrumentation.logging")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
        return logger

    def _get_library_name(self) -> str:
        """Get the library name."""
        return "logging"

    def is_globally_instrumented(self) -> bool:
        """Check if already instrumented globally."""
        return instrumentation_registry.is_globally_instrumented(self._get_library_name())

    def set_globally_instrumented(self) -> None:
        """Mark as globally instrumented."""
        instrumentation_registry.set_globally_instrumented(self._get_library_name())

    def instrument_app(self, app: Any = None) -> bool:
        """
        Instrument logging system (app parameter is ignored but kept for API compatibility).

        Args:
            app: Not used for logging instrumentation, kept for API compatibility

        Returns:
            True if successful, False otherwise
        """
        if self.is_globally_instrumented():
            self.logger.debug("Logging already instrumented, skipping")
            return True

        try:
            self._apply_otel_instrumentation()
            self._apply_json_formatting()
            self.set_globally_instrumented()
            return True
        except Exception as e:
            handle_instrumentation_error(self.logger, "logging", e, "instrumentation")
            return False

    def _apply_otel_instrumentation(self) -> None:
        """Apply OpenTelemetry logging instrumentation."""
        try:
            otel_instrumentor = OTelLoggingInstrumentor()
            otel_instrumentor.instrument(
                logger_provider=self.logger_provider,
                tracer_provider=self.tracer_provider,
                log_level=self.log_level,
                set_logging_format=False,
            )
            self.logger.debug("OpenTelemetry logging instrumentation applied")
        except Exception as e:
            if "already instrumented" in str(e).lower():
                self.logger.debug("OpenTelemetry logging was already instrumented")
            else:
                raise

    def _apply_json_formatting(self) -> None:
        """Apply custom JSON formatting to all loggers."""

        log_handler = LoggingConfigurator.create_handler(
            level=self.log_level, logger_provider=self.logger_provider, safe_logging=self.safe_logging
        )

        LoggingConfigurator.configure_root_logger(self.log_level, log_handler, replace_existing=True)

        LoggingConfigurator.ensure_all_loggers_propagate()

        LoggingConfigurator.configure_library_logger(self.log_level, log_handler)

        LoggingConfigurator.configure_logger_levels(self.log_level)

        LoggingConfigurator.mark_configured()

        self.logger.debug("JSON formatting applied to logging system")
