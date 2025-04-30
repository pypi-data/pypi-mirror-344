"""
Telemetry initialization for DTA Observability.
"""

import logging
import os
import sys
from typing import Any, Dict, List, Literal, Optional, Union

from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.error_handler import ErrorHandler, GlobalErrorHandler
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

from dta_observability.core.config import (
    get_boolean_config,
    get_config,
    get_excluded_instrumentations,
    get_int_config,
    get_log_level,
    get_safe_logging,
)
from dta_observability.core.propagator import configure_propagation, configure_specific_propagation
from dta_observability.logging.logger import get_logger

ExporterType = Literal["otlp", "console"]


class DTAErrorHandler(ErrorHandler):
    """Custom error handler that records errors with more context."""

    def _handle(self, error: Exception, *args: Any, **kwargs: Any) -> Any:
        """Record an error with more context."""
        from dta_observability.core.span import mark_error_event
        from dta_observability.logging.logger import get_logger

        logger = get_logger("dta_observability.error")
        logger.error("Error in OpenTelemetry operation", exc_info=error)

        try:
            mark_error_event(error, True)
        except Exception:

            pass


class TelemetryInitializer:
    """
    Handles initialization of OpenTelemetry components with proper configuration.
    """

    def __init__(
        self,
        service_name: Optional[str] = None,
        service_version: Optional[str] = None,
        resource_attributes: Optional[Dict[str, str]] = None,
        log_level: int = logging.INFO,
        safe_logging: bool = True,
        otlp_endpoint: Optional[str] = None,
        otlp_insecure: Optional[bool] = None,
        batch_export_delay_ms: Optional[int] = None,
        enable_resource_detectors: bool = True,
        exporter_type: ExporterType = "otlp",
        traces_exporter_type: Optional[ExporterType] = None,
        metrics_exporter_type: Optional[ExporterType] = None,
        logs_exporter_type: Optional[ExporterType] = None,
        enable_traces: bool = True,
        enable_metrics: bool = True,
        enable_logs: bool = True,
    ):
        """
        Initialize the telemetry initializer.

        Args:
            service_name: Name of the service
            service_version: Version of the service
            resource_attributes: Additional resource attributes
            log_level: Logging level to use
            safe_logging: Whether to enable safe logging that handles complex data types
            otlp_endpoint: The OTLP exporter endpoint URL
            otlp_insecure: Whether to use insecure connection for OTLP
            batch_export_delay_ms: Delay in milliseconds between batch exports
            enable_resource_detectors: Whether to enable automatic resource detection
            exporter_type: Default type of exporter to use ("otlp" or "console")
            traces_exporter_type: Specific exporter type for traces (overrides exporter_type)
            metrics_exporter_type: Specific exporter type for metrics (overrides exporter_type)
            logs_exporter_type: Specific exporter type for logs (overrides exporter_type)
            enable_traces: Whether to enable trace collection
            enable_metrics: Whether to enable metrics collection
            enable_logs: Whether to enable logs collection
        """
        self.service_name = service_name
        self.service_version = service_version
        self.resource_attributes = resource_attributes or {}
        self.log_level = log_level
        self.safe_logging = safe_logging
        self.otlp_endpoint = otlp_endpoint
        self.otlp_insecure = otlp_insecure
        self.batch_export_delay_ms = batch_export_delay_ms
        self.enable_resource_detectors = enable_resource_detectors
        self.exporter_type = exporter_type
        self.traces_exporter_type = traces_exporter_type
        self.metrics_exporter_type = metrics_exporter_type
        self.logs_exporter_type = logs_exporter_type
        self.enable_traces = enable_traces
        self.enable_metrics = enable_metrics
        self.enable_logs = enable_logs

        self.exporter_config = self._load_exporter_config()

        self.resource = self._create_resource()

    def _load_exporter_config(self) -> Dict[str, Any]:
        """Load exporter configuration from settings or instance parameters."""

        default_exporter_type = get_config("EXPORTER_TYPE")
        if not default_exporter_type:
            default_exporter_type = self.exporter_type

        traces_type = self.traces_exporter_type or get_config("TRACES_EXPORTER_TYPE") or default_exporter_type
        metrics_type = self.metrics_exporter_type or get_config("METRICS_EXPORTER_TYPE") or default_exporter_type
        logs_type = self.logs_exporter_type or get_config("LOGS_EXPORTER_TYPE") or default_exporter_type

        return {
            "endpoint": self.otlp_endpoint or get_config("EXPORTER_OTLP_ENDPOINT") or "http://localhost:4317",
            "insecure": (
                self.otlp_insecure if self.otlp_insecure is not None else get_boolean_config("EXPORTER_OTLP_INSECURE")
            ),
            "batch_delay_ms": (
                self.batch_export_delay_ms
                if self.batch_export_delay_ms is not None
                else get_int_config("BATCH_EXPORT_SCHEDULE_DELAY", 5000)
            ),
            "exporter_type": default_exporter_type,
            "traces_exporter_type": traces_type,
            "metrics_exporter_type": metrics_type,
            "logs_exporter_type": logs_type,
            "enable_traces": (
                self.enable_traces if self.enable_traces is not None else get_boolean_config("ENABLE_TRACES", True)
            ),
            "enable_metrics": (
                self.enable_metrics if self.enable_metrics is not None else get_boolean_config("ENABLE_METRICS", True)
            ),
            "enable_logs": (
                self.enable_logs if self.enable_logs is not None else get_boolean_config("ENABLE_LOGS", True)
            ),
        }

    def _create_resource(self) -> Resource:
        """Create and configure the OpenTelemetry resource."""

        resource_attrs = self.resource_attributes.copy() if self.resource_attributes else {}

        if self.service_name:
            resource_attrs[ResourceAttributes.SERVICE_NAME] = self.service_name

        if self.service_version:
            resource_attrs[ResourceAttributes.SERVICE_VERSION] = self.service_version

        if ResourceAttributes.SERVICE_INSTANCE_ID not in resource_attrs:
            resource_attrs[ResourceAttributes.SERVICE_INSTANCE_ID] = f"process-{os.getpid()}"

        base_resource = Resource.create(resource_attrs)

        if self.enable_resource_detectors:
            from dta_observability.resources.detector import detect_resources

            auto_resource = detect_resources(resource_attrs)

            return auto_resource
        else:

            return base_resource

    def configure_tracing(self) -> Optional[TracerProvider]:
        """
        Configure and initialize the tracer provider.

        Returns:
            TracerProvider if traces are enabled, otherwise None
        """
        if not self.exporter_config["enable_traces"]:
            return None

        tracer_provider = TracerProvider(resource=self.resource)

        if self.exporter_config["traces_exporter_type"] == "console":
            console_exporter = ConsoleSpanExporter()
            exporter: Any = console_exporter
        else:
            exporter = OTLPSpanExporter(
                endpoint=self.exporter_config["endpoint"], insecure=self.exporter_config["insecure"]
            )

        span_processor = BatchSpanProcessor(exporter)
        tracer_provider.add_span_processor(span_processor)

        return tracer_provider

    def configure_metrics(self) -> Optional[MeterProvider]:
        """
        Configure and initialize the meter provider.

        Returns:
            MeterProvider if metrics are enabled, otherwise None
        """
        if not self.exporter_config["enable_metrics"]:
            return None

        if self.exporter_config["metrics_exporter_type"] == "console":
            console_exporter = ConsoleMetricExporter()
            exporter: Any = console_exporter
        else:
            exporter = OTLPMetricExporter(
                endpoint=self.exporter_config["endpoint"], insecure=self.exporter_config["insecure"]
            )

        metrics_reader = PeriodicExportingMetricReader(
            exporter, export_interval_millis=self.exporter_config["batch_delay_ms"]
        )

        meter_provider = MeterProvider(resource=self.resource, metric_readers=[metrics_reader])

        return meter_provider

    def configure_logging(self) -> Optional[LoggerProvider]:
        """
        Configure logging with trace context.

        Returns:
            LoggerProvider if logs are enabled, otherwise None
        """
        if not self.exporter_config["enable_logs"]:
            return None

        logger_provider = LoggerProvider(resource=self.resource)

        if self.exporter_config["logs_exporter_type"] == "console":
            console_exporter = ConsoleLogExporter()
            exporter: Any = console_exporter
        else:
            exporter = OTLPLogExporter(
                endpoint=self.exporter_config["endpoint"], insecure=self.exporter_config["insecure"]
            )

        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        self._apply_log_level_to_instrumented_loggers()

        return logger_provider

    def _apply_log_level_to_instrumented_loggers(self) -> None:
        """
        Apply consistent log level configuration to all loggers.
        """

        from dta_observability.logging.logger import LoggingConfigurator

        LoggingConfigurator.configure_logger_levels(self.log_level)

    def setup_exception_handling(self) -> None:
        """Configure global exception handling."""

        original_excepthook = sys.excepthook

        def global_exception_hook(exc_type, exc_value, exc_traceback):
            """Global exception hook that ensures all unhandled exceptions are properly traced."""

            with GlobalErrorHandler():
                try:

                    dta_handler = DTAErrorHandler()
                    dta_handler._handle(exc_value)
                except Exception:

                    pass

            original_excepthook(exc_type, exc_value, exc_traceback)

        sys.excepthook = global_exception_hook


def _resolve_log_level(log_level: Optional[Union[int, str]]) -> int:
    """
    Resolve the log level from the provided value or config.

    Args:
        log_level: Log level as int, string, or None to use config

    Returns:
        Resolved log level as int
    """
    if log_level is None:
        return get_log_level()
    elif isinstance(log_level, str):
        try:
            return int(log_level)
        except ValueError:

            level_map = {
                "debug": logging.DEBUG,
                "info": logging.INFO,
                "warning": logging.WARNING,
                "error": logging.ERROR,
                "critical": logging.CRITICAL,
            }
            return level_map.get(log_level.lower(), logging.INFO)
    return log_level


def init_telemetry(
    service_name: Optional[str] = None,
    service_version: Optional[str] = None,
    service_instance_id: Optional[str] = None,
    resource_attributes: Optional[Dict[str, str]] = None,
    configure_auto_instrumentation: Optional[bool] = None,
    log_level: Optional[Union[int, str]] = None,
    flask_app: Optional[Any] = None,
    fastapi_app: Optional[Any] = None,
    celery_app: Optional[Any] = None,
    safe_logging: Optional[bool] = None,
    excluded_instrumentations: Optional[List[str]] = None,
    otlp_endpoint: Optional[str] = None,
    otlp_insecure: Optional[bool] = None,
    batch_export_delay_ms: Optional[int] = None,
    enable_resource_detectors: Optional[bool] = None,
    enable_logging_instrumentation: Optional[bool] = None,
    propagators: Optional[str] = None,
    exporter_type: Optional[ExporterType] = None,
    traces_exporter_type: Optional[ExporterType] = None,
    metrics_exporter_type: Optional[ExporterType] = None,
    logs_exporter_type: Optional[ExporterType] = None,
    enable_traces: Optional[bool] = None,
    enable_metrics: Optional[bool] = None,
    enable_logs: Optional[bool] = None,
) -> None:
    """
    Initialize telemetry with sensible defaults.

    Args:
        service_name: Name of the service.
        service_version: Version of the service.
        service_instance_id: Unique instance ID for this service instance.
        resource_attributes: Additional resource attributes.
        configure_auto_instrumentation: Whether to configure auto-instrumentation.
        log_level: Logging level to use.
        flask_app: Optional Flask application instance to instrument directly.
        fastapi_app: Optional FastAPI application instance to instrument directly.
        celery_app: Optional Celery application instance to instrument directly.
        safe_logging: Whether to enable safe logging with complex data type handling.
        excluded_instrumentations: List of instrumentation names to exclude.
        otlp_endpoint: The OTLP exporter endpoint (e.g., "http://localhost:4317").
        otlp_insecure: Whether to use insecure connections for OTLP exporter.
        batch_export_delay_ms: Delay in milliseconds between batch exports.
        enable_resource_detectors: Whether to enable automatic resource detection.
        enable_logging_instrumentation: Whether to enable logging instrumentation.
        propagators: Comma-separated list of context propagators to use (e.g., "w3c,gcp").
        exporter_type: Default type of exporter to use for all signal types.
        traces_exporter_type: Specific exporter type to use for traces.
        metrics_exporter_type: Specific exporter type to use for metrics.
        logs_exporter_type: Specific exporter type to use for logs.
        enable_traces: Whether to enable trace collection.
        enable_metrics: Whether to enable metrics collection.
        enable_logs: Whether to enable logs collection.
    """

    configure_propagation()

    actual_log_level = _resolve_log_level(log_level)
    actual_safe_logging = safe_logging if safe_logging is not None else get_safe_logging()
    actual_configure_auto_instrumentation = (
        configure_auto_instrumentation
        if configure_auto_instrumentation is not None
        else get_boolean_config("AUTO_INSTRUMENTATION_ENABLED")
    )
    actual_excluded_instrumentations = (
        excluded_instrumentations if excluded_instrumentations is not None else get_excluded_instrumentations()
    )
    actual_service_name = service_name if service_name is not None else get_config("SERVICE_NAME")
    actual_service_version = service_version if service_version is not None else get_config("SERVICE_VERSION")
    actual_service_instance_id = (
        service_instance_id if service_instance_id is not None else get_config("SERVICE_INSTANCE_ID")
    )
    actual_otlp_endpoint = otlp_endpoint if otlp_endpoint is not None else get_config("EXPORTER_OTLP_ENDPOINT")
    actual_otlp_insecure = otlp_insecure if otlp_insecure is not None else get_boolean_config("EXPORTER_OTLP_INSECURE")
    actual_batch_export_delay_ms = (
        batch_export_delay_ms
        if batch_export_delay_ms is not None
        else get_int_config("BATCH_EXPORT_SCHEDULE_DELAY", 5000)
    )
    actual_enable_resource_detectors = (
        enable_resource_detectors
        if enable_resource_detectors is not None
        else get_boolean_config("RESOURCE_DETECTORS_ENABLED")
    )
    actual_enable_logging_instrumentation = (
        enable_logging_instrumentation
        if enable_logging_instrumentation is not None
        else get_boolean_config("LOGGING_INSTRUMENTATION_ENABLED")
    )
    actual_propagators = propagators if propagators is not None else get_config("OTEL_PROPAGATORS")

    default_exporter_type = exporter_type
    if default_exporter_type is None:
        default_exporter_type = get_config("EXPORTER_TYPE")
        if not default_exporter_type:
            default_exporter_type = "otlp"

    if default_exporter_type not in ["otlp", "console"]:
        logger = get_logger("dta_observability.telemetry")
        logger.warning(f"Invalid exporter type '{default_exporter_type}', defaulting to 'otlp'")
        default_exporter_type = "otlp"

    if actual_propagators:
        configure_specific_propagation(actual_propagators.split(","))

    combined_resource_attributes = {}

    combined_resource_attributes[ResourceAttributes.SERVICE_NAME] = actual_service_name

    if actual_service_version:
        combined_resource_attributes[ResourceAttributes.SERVICE_VERSION] = actual_service_version

    if actual_service_instance_id:
        combined_resource_attributes[ResourceAttributes.SERVICE_INSTANCE_ID] = actual_service_instance_id

    if resource_attributes:
        combined_resource_attributes.update(resource_attributes)

    from dta_observability.logging.logger import LoggingConfigurator

    try:
        from dta_observability.instrumentation.helpers.uvicorn import configure_uvicorn_for_otel

        configure_uvicorn_for_otel(log_level=actual_log_level)
    except Exception:

        pass

    initializer = TelemetryInitializer(
        service_name=actual_service_name,
        service_version=actual_service_version,
        resource_attributes=combined_resource_attributes,
        log_level=actual_log_level,
        safe_logging=actual_safe_logging,
        otlp_endpoint=actual_otlp_endpoint,
        otlp_insecure=actual_otlp_insecure,
        batch_export_delay_ms=actual_batch_export_delay_ms,
        enable_resource_detectors=actual_enable_resource_detectors,
        exporter_type=default_exporter_type,
        traces_exporter_type=traces_exporter_type,
        metrics_exporter_type=metrics_exporter_type,
        logs_exporter_type=logs_exporter_type,
        enable_traces=bool(enable_traces) if enable_traces is not None else True,
        enable_metrics=bool(enable_metrics) if enable_metrics is not None else True,
        enable_logs=bool(enable_logs) if enable_logs is not None else True,
    )

    tracer_provider = initializer.configure_tracing()
    meter_provider = initializer.configure_metrics()
    logger_provider = initializer.configure_logging()

    if logger_provider:
        _logs.set_logger_provider(logger_provider)
    if tracer_provider:
        trace.set_tracer_provider(tracer_provider)
    if meter_provider:
        metrics.set_meter_provider(meter_provider)

    initializer.setup_exception_handling()

    if celery_app:

        celery_app.conf.worker_hijack_root_logger = False

    if actual_configure_auto_instrumentation:
        from dta_observability.instrumentation.auto import configure_instrumentation

        configure_instrumentation(
            tracer_provider=tracer_provider,
            logger_provider=logger_provider,
            flask_app=flask_app,
            fastapi_app=fastapi_app,
            celery_app=celery_app,
            log_level=actual_log_level,
            safe_logging=actual_safe_logging,
            excluded_instrumentations=actual_excluded_instrumentations,
            enable_logging_instrumentation=actual_enable_logging_instrumentation,
        )

    LoggingConfigurator.reset_instrumented_logger_levels(actual_log_level)

    trace_status = "enabled" if tracer_provider else "disabled"
    metrics_status = "enabled" if meter_provider else "disabled"
    logs_status = "enabled" if logger_provider else "disabled"

    logger = get_logger("dta_observability.telemetry")
    logger.info(
        f"Telemetry initialized for service: {actual_service_name} - "
        + f"traces: {trace_status}/{initializer.exporter_config.get('traces_exporter_type')}, "
        + f"metrics: {metrics_status}/{initializer.exporter_config.get('metrics_exporter_type')}, "
        + f"logs: {logs_status}/{initializer.exporter_config.get('logs_exporter_type')}"
    )
