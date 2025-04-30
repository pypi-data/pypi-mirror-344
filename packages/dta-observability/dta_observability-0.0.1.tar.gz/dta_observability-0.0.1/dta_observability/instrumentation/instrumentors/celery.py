"""
Celery-specific instrumentation for DTA Observability.
"""

from typing import Any

from dta_observability.instrumentation.base import BaseInstrumentor
from dta_observability.instrumentation.helpers.celery import instrument_celery
from dta_observability.instrumentation.utils import (
    check_instrumentation_status,
    handle_instrumentation_error,
)


class CeleryInstrumentor(BaseInstrumentor):
    """Handles Celery-specific instrumentation."""

    _INSTRUMENTED_KEY = "_dta_observability_instrumented"

    def __init__(self, tracer_provider=None, logger_provider=None, log_level=None):
        """
        Initialize the Celery instrumentor.

        Args:
            tracer_provider: Optional tracer provider to use
            logger_provider: Optional logger provider to use
            log_level: Optional log level to use
        """
        super().__init__(tracer_provider, logger_provider, log_level)

    def _get_library_name(self) -> str:
        """Get the library name."""
        return "celery"

    def instrument_app(self, app: Any) -> bool:
        """
        Instrument a Celery application.

        Args:
            app: The Celery application to instrument

        Returns:
            True if successful, False otherwise
        """
        if not app:
            return False

        try:
            if check_instrumentation_status(app, self._get_library_name(), self._INSTRUMENTED_KEY):
                self.logger.debug("Celery app already instrumented, skipping")
                return True

            if not self.is_globally_instrumented():
                try:
                    self._apply_otel_instrumentation()
                except ImportError as err:
                    self.logger.warning("OpenTelemetry Celery instrumentation package not available: %s", err)
            else:
                self.logger.debug("OpenTelemetry Celery already globally instrumented, skipping")

            instrument_celery(app)

            setattr(app, self._INSTRUMENTED_KEY, True)
            self.register_app(app)
            self.logger.info("Celery app instrumented: %s", app)

            return True

        except Exception as e:
            handle_instrumentation_error(self.logger, "Celery", e)
            return False

    def _apply_otel_instrumentation(self) -> None:
        """Apply OpenTelemetry Celery instrumentation."""
        try:
            from opentelemetry.instrumentation.celery import CeleryInstrumentor as OTelCeleryInstrumentor

            kwargs = {"tracer_provider": self.tracer_provider}
            if hasattr(self, "logger_provider") and self.logger_provider:
                # Cast logger_provider to Any to avoid type issues
                from typing import Any, cast

                kwargs["logger_provider"] = cast(Any, self.logger_provider)

            otel_instrumentor = OTelCeleryInstrumentor(**kwargs)
            otel_instrumentor.instrument()
            self.set_globally_instrumented()
            self.logger.debug("OpenTelemetry Celery instrumentation applied")
        except Exception as e:
            if "already instrumented" in str(e).lower():
                self.set_globally_instrumented()
                self.logger.debug("OpenTelemetry Celery was already instrumented")
            else:
                handle_instrumentation_error(self.logger, "Celery", e, "OpenTelemetry instrumentation")
