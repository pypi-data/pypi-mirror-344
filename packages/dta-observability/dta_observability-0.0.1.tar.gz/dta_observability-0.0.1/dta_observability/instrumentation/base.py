"""
Base classes for instrumentation.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import TracerProvider

from dta_observability.instrumentation.registry import instrumentation_registry
from dta_observability.logging.logger import get_logger


class BaseInstrumentor(ABC):
    """
    Base class for all instrumentors.

    Provides common functionality and enforces a consistent interface.
    """

    def __init__(
        self,
        tracer_provider: Optional[TracerProvider] = None,
        logger_provider: Optional[LoggerProvider] = None,
        log_level: Optional[int] = None,
    ):
        """
        Initialize the instrumentor.

        Args:
            tracer_provider: Optional tracer provider to use
            logger_provider: Optional logger provider to use
            log_level: Optional log level to use for this instrumentor
        """
        self.tracer_provider = tracer_provider
        self.logger_provider = logger_provider
        self.log_level = log_level
        self.logger = get_logger(f"dta_observability.instrumentation.{self._get_library_name()}")

    @abstractmethod
    def _get_library_name(self) -> str:
        """
        Get the name of the library being instrumented.

        Returns:
            The library name as a string
        """
        pass

    @abstractmethod
    def instrument_app(self, app: Any) -> bool:
        """
        Instrument a specific application instance.

        Args:
            app: The application instance to instrument

        Returns:
            True if successful, False otherwise
        """
        pass

    def is_globally_instrumented(self) -> bool:
        """
        Check if the library is already globally instrumented.

        Returns:
            True if globally instrumented, False otherwise
        """
        return instrumentation_registry.is_globally_instrumented(self._get_library_name())

    def set_globally_instrumented(self) -> None:
        """Mark the library as globally instrumented."""
        instrumentation_registry.set_globally_instrumented(self._get_library_name())

    def is_app_instrumented(self, app: Any) -> bool:
        """
        Check if a specific app is already instrumented.

        Args:
            app: The application instance to check

        Returns:
            True if already instrumented, False otherwise
        """
        return instrumentation_registry.is_app_instrumented(self._get_library_name(), app)

    def register_app(self, app: Any) -> None:
        """
        Register an app as instrumented.

        Args:
            app: The application instance to register
        """
        instrumentation_registry.register_app(self._get_library_name(), app)
