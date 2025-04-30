"""
Auto-instrumentation for DTA Observability.
"""

import importlib
import logging
from typing import Any, List, Optional

from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import TracerProvider

from dta_observability.core.config import get_boolean_config, get_log_level
from dta_observability.instrumentation.detector import InstrumentationMap, PackageDetector
from dta_observability.instrumentation.instrumentors.logging import LoggingInstrumentor
from dta_observability.instrumentation.instrumentors.system_metrics import SystemMetricsInstrumentor
from dta_observability.instrumentation.registry import instrumentation_registry
from dta_observability.instrumentation.utils import handle_instrumentation_error
from dta_observability.logging.logger import LoggingConfigurator, get_logger


def auto_patch_all() -> None:
    """
    Patch all supported frameworks for DTA Observability.

    Currently patches:
    - FastAPI
    - Uvicorn
    """
    logger = get_logger("dta_observability.instrumentation")

    try:

        _patch_fastapi()

        _patch_uvicorn()

        logger.debug("Successfully patched all supported frameworks")
    except Exception as e:
        logger.warning(f"Failed to patch all frameworks: {e}")


def auto_patch(framework_name: str) -> None:
    """
    Patch a specific framework for DTA Observability.

    Args:
        framework_name: Name of the framework to patch (fastapi, uvicorn)

    Raises:
        ValueError: If the framework is not supported
    """
    framework_name = framework_name.lower()

    if framework_name == "fastapi":
        _patch_fastapi()
    elif framework_name == "uvicorn":
        _patch_uvicorn()
    else:
        raise ValueError(f"Unsupported framework: {framework_name}. Supported frameworks: fastapi, uvicorn")


def _patch_fastapi() -> None:
    """Patch FastAPI to work with DTA Observability."""
    logger = get_logger("dta_observability.instrumentation")

    try:

        from fastapi.logger import logger as fastapi_logger

        fastapi_access_logger = logging.getLogger("dta-fastapi.access")
        werkzeug_logger = logging.getLogger("werkzeug")
        fastapi_access_logger.disabled = True
        fastapi_access_logger.propagate = False
        werkzeug_logger.disabled = True
        werkzeug_logger.propagate = False

        fastapi_logger.setLevel(logging.getLogger("dta_observability").level)
        fastapi_logger.propagate = True
        werkzeug_logger.setLevel(logging.getLogger("dta_observability").level)
        werkzeug_logger.propagate = True

        logger.debug("Configured FastAPI to use DTA Observability logging")
    except ImportError:
        logger.debug("FastAPI not installed, skipping instrumentation")
    except Exception as e:
        logger.warning(f"Failed to patch FastAPI: {e}")


def _patch_uvicorn() -> None:
    """Patch Uvicorn to work with DTA Observability."""
    logger = get_logger("dta_observability.instrumentation")

    try:

        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.disabled = True
        uvicorn_access_logger.propagate = False

        for name in ["uvicorn", "uvicorn.error"]:
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.setLevel(logging.getLogger("dta_observability").level)
            uvicorn_logger.propagate = True

            for handler in list(uvicorn_logger.handlers):
                uvicorn_logger.removeHandler(handler)

        logger.debug("Configured Uvicorn to use DTA Observability logging")
    except ImportError:
        logger.debug("Uvicorn not installed, skipping instrumentation")
    except Exception as e:
        logger.warning(f"Failed to patch Uvicorn: {e}")


class AutoInstrumentor:
    """
    Manages automatic instrumentation of libraries.
    """

    def __init__(
        self,
        tracer_provider: Optional[TracerProvider] = None,
        excluded_libraries: Optional[List[str]] = None,
        logger_provider: Optional[LoggerProvider] = None,
        log_level: Optional[int] = None,
    ):
        """
        Initialize the auto-instrumentor.

        Args:
            tracer_provider: The tracer provider to use for instrumentation
            excluded_libraries: List of library names to exclude from instrumentation
            logger_provider: The logger provider to use for instrumentation
            log_level: The log level to use for instrumentation
        """
        self.tracer_provider = tracer_provider
        self.logger_provider = logger_provider
        self.log_level = log_level
        self.excluded_libraries = set(excluded_libraries or [])
        self.instrumented_libraries: List[str] = []
        self.logger = get_logger("dta_observability.instrumentation")

    def instrument_specific_app(self, library_name: str, app: Any) -> bool:
        """
        Instrument a specific application instance.

        Args:
            library_name: The library name (e.g., "flask", "fastapi", "celery")
            app: The application instance to instrument

        Returns:
            True if instrumentation was successful, False otherwise
        """
        if library_name in self.excluded_libraries:
            return False

        instrumentor_map = {
            "flask": "dta_observability.instrumentation.instrumentors.flask.FlaskInstrumentor",
            "fastapi": "dta_observability.instrumentation.instrumentors.fastapi.FastAPIInstrumentor",
            "celery": "dta_observability.instrumentation.instrumentors.celery.CeleryInstrumentor",
        }

        if library_name not in instrumentor_map:
            self.logger.debug(f"No instrumentor found for {library_name}")
            return False

        try:
            module_path, class_name = instrumentor_map[library_name].rsplit(".", 1)
            module = importlib.import_module(module_path)
            instrumentor_class = getattr(module, class_name)

            instrumentor = instrumentor_class(
                tracer_provider=self.tracer_provider, logger_provider=self.logger_provider, log_level=self.log_level
            )

            result = instrumentor.instrument_app(app)

            if result:
                self.instrumented_libraries.append(library_name)
                self.excluded_libraries.add(library_name)

            return result

        except Exception as e:
            handle_instrumentation_error(self.logger, library_name, e, "specific app instrumentation")
            return False


def _apply_celery_helpers(celery_app: Any) -> None:
    """
    Apply Celery-specific logging helpers.

    Args:
        celery_app: The Celery application to instrument
    """
    try:

        if hasattr(celery_app, "conf"):
            celery_app.conf.worker_hijack_root_logger = False

        from dta_observability.instrumentation.helpers.celery import instrument_celery

        instrument_celery(celery_app)
    except Exception as e:
        logger = get_logger("dta_observability.instrumentation")
        handle_instrumentation_error(logger, "Celery", e, "helper instrumentation")


def _instrument_library(instrumentor: AutoInstrumentor, library_name: str) -> bool:
    """
    Instrument a specific library by name.

    Args:
        instrumentor: The AutoInstrumentor instance
        library_name: The name of the library to instrument

    Returns:
        True if instrumentation was successful, False otherwise
    """
    logger = get_logger("dta_observability.instrumentation")

    if instrumentation_registry.is_globally_instrumented(library_name):
        logger.debug(f"Library {library_name} already globally instrumented, skipping")
        if library_name not in instrumentor.instrumented_libraries:
            instrumentor.instrumented_libraries.append(library_name)
        return True

    module_path = InstrumentationMap.get_module_path(library_name)
    if not module_path or not (
        PackageDetector.is_available(library_name) and PackageDetector.is_available(module_path)
    ):
        logger.debug(f"Library {library_name} or its instrumentation is not available, skipping")
        return False

    try:

        otel_instrumentor = _create_otel_instrumentor(library_name)
        if not otel_instrumentor:
            return False

        kwargs = {}
        if instrumentor.tracer_provider:
            from opentelemetry.sdk.trace import TracerProvider

            if isinstance(instrumentor.tracer_provider, TracerProvider):
                kwargs["tracer_provider"] = instrumentor.tracer_provider
        if instrumentor.log_level is not None:
            # Use int casting to avoid type errors
            if isinstance(instrumentor.log_level, int):
                from typing import Any, cast

                kwargs["log_level"] = cast(Any, instrumentor.log_level)

        try:
            otel_instrumentor.instrument(**kwargs)
            instrumentation_registry.set_globally_instrumented(library_name)
            instrumentor.instrumented_libraries.append(library_name)
            return True
        except Exception as e:

            if "already instrumented" in str(e).lower():
                instrumentation_registry.set_globally_instrumented(library_name)
                instrumentor.instrumented_libraries.append(library_name)
                logger.debug(f"Library {library_name} was already instrumented")
                return True
            raise

    except Exception as e:
        handle_instrumentation_error(logger, library_name, e, "auto-instrumentation")
        return False


def _create_otel_instrumentor(library_name: str) -> Optional[Any]:
    """
    Create an OpenTelemetry instrumentor instance dynamically.

    Args:
        library_name: The name of the library to create an instrumentor for

    Returns:
        An instrumentor instance or None if creation failed
    """
    try:
        module_path = InstrumentationMap.get_module_path(library_name)
        if not module_path:
            return None

        module = importlib.import_module(module_path)
        class_name = InstrumentationMap.get_instrumentor_class_name(library_name)
        return getattr(module, class_name)()
    except (ImportError, AttributeError) as e:
        logger = get_logger("dta_observability.instrumentation")
        logger.debug(f"Could not create instrumentor for {library_name}: {e}")
        return None


def configure_instrumentation(
    tracer_provider: Optional[TracerProvider] = None,
    excluded_instrumentations: Optional[List[str]] = None,
    flask_app: Optional[Any] = None,
    fastapi_app: Optional[Any] = None,
    celery_app: Optional[Any] = None,
    logger_provider: Optional[LoggerProvider] = None,
    meter_provider: Optional[Any] = None,
    log_level: Optional[int] = None,
    safe_logging: bool = True,
    enable_logging_instrumentation: Optional[bool] = None,
    enable_system_metrics: Optional[bool] = None,
    system_metrics_config: Optional[dict] = None,
) -> None:
    """
    Configure auto-instrumentation for common libraries.

    Args:
        tracer_provider: The tracer provider to use for instrumentation.
        excluded_instrumentations: List of instrumentation names to exclude.
        flask_app: Optional Flask application instance to instrument directly.
        fastapi_app: Optional FastAPI application instance to instrument directly.
        celery_app: Optional Celery application instance to instrument directly.
        logger_provider: Optional logger provider for logging instrumentation.
        meter_provider: Optional meter provider for metrics instrumentation.
        log_level: The log level to use for instrumentation.
        safe_logging: Whether to enable safe logging with complex data type handling.
        enable_logging_instrumentation: Whether to enable logging instrumentation.
        enable_system_metrics: Whether to enable system metrics collection.
        system_metrics_config: Optional configuration for system metrics collection.
    """
    if not get_boolean_config("AUTO_INSTRUMENTATION_ENABLED"):
        return

    excluded_instrumentations = excluded_instrumentations or []
    actual_log_level = log_level if log_level is not None else get_log_level()
    actual_enable_logging = (
        enable_logging_instrumentation
        if enable_logging_instrumentation is not None
        else get_boolean_config("LOGGING_INSTRUMENTATION_ENABLED")
    )
    actual_enable_system_metrics = (
        enable_system_metrics
        if enable_system_metrics is not None
        else get_boolean_config("SYSTEM_METRICS_ENABLED", default=True)
    )

    logger = get_logger("dta_observability.instrumentation")

    LoggingConfigurator.configure_logger_levels(actual_log_level)

    if "fastapi" not in excluded_instrumentations and "uvicorn" not in excluded_instrumentations:
        try:
            auto_patch_all()
        except Exception as e:
            logger.warning(f"Failed to patch FastAPI and Uvicorn: {e}")
    elif "fastapi" not in excluded_instrumentations:
        try:
            auto_patch("fastapi")
        except Exception as e:
            logger.warning(f"Failed to patch FastAPI: {e}")
    elif "uvicorn" not in excluded_instrumentations:
        try:
            auto_patch("uvicorn")
        except Exception as e:
            logger.warning(f"Failed to patch Uvicorn: {e}")

    if actual_enable_logging:
        _instrument_logging(tracer_provider, actual_log_level, safe_logging, logger)

        LoggingConfigurator.configure_logger_levels(actual_log_level)

    if actual_enable_system_metrics:
        _instrument_system_metrics(tracer_provider, meter_provider, system_metrics_config, logger)

    instrumentor = AutoInstrumentor(
        tracer_provider=tracer_provider,
        excluded_libraries=excluded_instrumentations,
        logger_provider=logger_provider,
        log_level=actual_log_level,
    )

    _instrument_specific_apps(instrumentor, flask_app, fastapi_app, celery_app)

    for library_name in InstrumentationMap.LIBRARIES:
        if library_name not in instrumentor.excluded_libraries:
            _instrument_library(instrumentor, library_name)

    if instrumentor.instrumented_libraries:
        logger.info(f"Auto-instrumented libraries: {', '.join(instrumentor.instrumented_libraries)}")
    else:
        logger.info("No libraries were auto-instrumented")


def _instrument_logging(
    tracer_provider: Optional[TracerProvider], log_level: int, safe_logging: bool, logger: Any
) -> None:
    """Instrument logging."""
    try:
        logging_instrumentor = LoggingInstrumentor(
            tracer_provider=tracer_provider, log_level=log_level, safe_logging=safe_logging
        )
        logging_instrumentor.instrument_app()
        logger.debug("Logging instrumentation enabled")
    except Exception as e:
        logger.warning(f"Failed to instrument logging: {e}")


def _instrument_system_metrics(
    tracer_provider: Optional[TracerProvider],
    meter_provider: Optional[Any],
    system_metrics_config: Optional[dict],
    logger: Any,
) -> None:
    """Instrument system metrics."""
    try:
        system_metrics_instrumentor = SystemMetricsInstrumentor(
            tracer_provider=tracer_provider, meter_provider=meter_provider, config=system_metrics_config
        )
        if system_metrics_instrumentor.instrument():
            logger.debug("System metrics instrumentation enabled")
    except Exception as e:
        logger.warning(f"Failed to instrument system metrics: {e}")


def _instrument_specific_apps(
    instrumentor: AutoInstrumentor, flask_app: Optional[Any], fastapi_app: Optional[Any], celery_app: Optional[Any]
) -> None:
    """Instrument specific app instances."""
    if flask_app:
        instrumentor.instrument_specific_app("flask", flask_app)

    if fastapi_app:
        instrumentor.instrument_specific_app("fastapi", fastapi_app)

    if celery_app:
        _apply_celery_helpers(celery_app)
        instrumentor.instrument_specific_app("celery", celery_app)
