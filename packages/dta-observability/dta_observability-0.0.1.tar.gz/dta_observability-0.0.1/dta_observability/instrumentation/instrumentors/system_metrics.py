"""
System metrics instrumentation using OpenTelemetry.
"""

from typing import Any, Dict, List, Optional, Union

from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider

from dta_observability.core.config import get_boolean_config
from dta_observability.instrumentation.base import BaseInstrumentor


class SystemMetricsInstrumentor(BaseInstrumentor):
    """
    Instrumentor for system metrics collection.

    Collects system (CPU, memory, network) and process metrics using OpenTelemetry.
    """

    DEFAULT_CONFIG = {
        "system.cpu.time": ["idle", "user", "system", "irq"],
        "system.cpu.utilization": ["idle", "user", "system", "irq"],
        "system.memory.usage": ["used", "free", "cached"],
        "system.memory.utilization": ["used", "free", "cached"],
        "system.disk.io": ["read", "write"],
        "system.disk.operations": ["read", "write"],
        "system.disk.time": ["read", "write"],
        "system.network.io": ["transmit", "receive"],
        "system.network.packets": ["transmit", "receive"],
        "system.network.errors": ["transmit", "receive"],
        "system.network.connections": ["family", "type"],
        "process.cpu.time": ["user", "system"],
        "process.memory.usage": None,
        "process.memory.virtual": None,
        "process.runtime.memory": ["rss", "vms"],
    }

    def __init__(
        self,
        tracer_provider: Optional[TracerProvider] = None,
        meter_provider: Optional[MeterProvider] = None,
        config: Optional[Dict[str, Union[List[str], None]]] = None,
    ):
        """
        Initialize the system metrics instrumentor.

        Args:
            tracer_provider: Optional tracer provider for trace context
            meter_provider: Optional meter provider for metrics
            config: Optional configuration to specify which metrics to collect
        """
        super().__init__(tracer_provider)
        self.meter_provider = meter_provider
        self.config = config or self.DEFAULT_CONFIG
        self._instrumentor: Any = None

    def _get_library_name(self) -> str:
        """Get the name of the library being instrumented."""
        return "system_metrics"

    def _import_instrumentor(self) -> bool:
        """
        Import the OpenTelemetry system metrics instrumentor.

        Returns:
            True if import was successful, False otherwise
        """
        try:
            from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

            self._instrumentor = SystemMetricsInstrumentor(config=self.config)
            return True
        except ImportError:
            self.logger.warning(
                "opentelemetry-instrumentation-system-metrics package not found. "
                "Install it with: pip install opentelemetry-instrumentation-system-metrics"
            )
            return False

    def instrument(self) -> bool:
        """
        Instrument system metrics collection.

        Returns:
            True if instrumentation was successful, False otherwise
        """
        if not get_boolean_config("SYSTEM_METRICS_ENABLED", default=True):
            self.logger.debug("System metrics collection disabled by configuration")
            return False

        if not self._instrumentor and not self._import_instrumentor():
            return False

        try:
            if self.meter_provider:
                set_meter_provider(self.meter_provider)

            self._instrumentor.instrument()
            self.logger.info("System metrics instrumentation enabled")
            return True
        except Exception as e:
            self.logger.error(f"Failed to instrument system metrics: {e}")
            return False

    def instrument_app(self, app: Any = None) -> bool:
        """
        Instrument system metrics (app parameter is ignored but kept for API compatibility).

        Args:
            app: Ignored parameter, kept for API compatibility

        Returns:
            True if instrumentation was successful, False otherwise
        """
        return self.instrument()
