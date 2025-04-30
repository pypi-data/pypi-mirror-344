"""
Flask-specific instrumentation for DTA Observability.
"""

import logging
import time
import weakref
from typing import Any, Dict

from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import SpanKind

from dta_observability.core.span import set_span_attribute_safely
from dta_observability.instrumentation.base import BaseInstrumentor
from dta_observability.instrumentation.utils import check_instrumentation_status, handle_instrumentation_error
from dta_observability.logging.logger import get_logger


class FlaskInstrumentor(BaseInstrumentor):
    """Handles Flask-specific instrumentation."""

    _INSTRUMENTED_KEY = "_dta_flask_instrumented"

    def __init__(self, tracer_provider=None, logger_provider=None, log_level=None):
        """
        Initialize the Flask instrumentor.

        Args:
            tracer_provider: Optional tracer provider to use
            logger_provider: Optional logger provider to use
            log_level: Optional log level to use for access logs
        """
        super().__init__(tracer_provider, logger_provider, log_level)

    def _get_library_name(self) -> str:
        """Get the library name."""
        return "flask"

    def instrument_app(self, app: Any) -> bool:
        """
        Instrument a Flask application.

        Args:
            app: The Flask application to instrument

        Returns:
            True if successful, False otherwise
        """
        if not app:
            return False

        try:
            if check_instrumentation_status(app, self._get_library_name(), self._INSTRUMENTED_KEY):
                self.logger.debug("Flask app already instrumented, skipping")
                return True

            self._apply_wsgi_middleware(app)

            if hasattr(app, "config") and app.config.get("ENABLE_FORK_HOOKS", False):
                self._add_gunicorn_fork_hooks(app)

            setattr(app, self._INSTRUMENTED_KEY, True)
            self.register_app(app)
            self.logger.info("Flask app WSGI middleware instrumented with JSON access logging: %s", app)
            return True

        except Exception as e:
            handle_instrumentation_error(self.logger, "Flask", e)
            return False

    def _apply_wsgi_middleware(self, app: Any) -> None:
        """
        Apply OpenTelemetry WSGI middleware to Flask app.

        Args:
            app: The Flask application
        """
        access_logger = get_logger("flask.logs")

        if hasattr(self, "log_level"):
            access_logger.setLevel(self.log_level if isinstance(self.log_level, (int, str)) else logging.INFO)

        logged_spans: weakref.WeakSet[Any] = weakref.WeakSet()

        def request_hook(span: Span, environ: Dict[str, Any]) -> None:
            if not span or not span.is_recording():
                return

            span._kind = SpanKind.SERVER

            method = environ.get("REQUEST_METHOD", "")
            path = environ.get("PATH_INFO", "")
            if method and path:
                set_span_attribute_safely(span, "http.route", path)
                set_span_attribute_safely(span, "http.method", method)

            if hasattr(span, "set_attribute"):
                span.set_attribute("http.request_start_time", time.time())

        def response_hook(span: Span, environ: Dict[str, Any], status: str, headers: Dict[str, Any]) -> None:
            if not span or not span.is_recording() or not status:
                return

            span_id = getattr(span, "span_id", None)
            if span_id in logged_spans:
                return

            try:
                method = environ.get("REQUEST_METHOD", "")
                path = environ.get("PATH_INFO", "")
                query = environ.get("QUERY_STRING", "")
                client_ip = environ.get("REMOTE_ADDR", "unknown")

                forwarded_for = environ.get("HTTP_X_FORWARDED_FOR", "")
                if forwarded_for:
                    client_ip = forwarded_for.split(",")[0].strip()

                status_code = int(status.split(" ")[0]) if status else 0

                request_time = "unknown"
                if (
                    hasattr(span, "attributes")
                    and span.attributes is not None
                    and "http.request_start_time" in span.attributes
                ):
                    start_time = span.attributes.get("http.request_start_time")
                    if start_time:
                        if isinstance(start_time, (int, float)):
                            request_time = f"{time.time() - start_time:.4f}s"

                if span_id:
                    logged_spans.add(span_id)

                if status_code > 0:
                    access_logger.info(
                        f"{method} {path} {status_code}",
                        extra={
                            "http_client_ip": client_ip,
                            "http_method": method,
                            "http_path": path,
                            "http_query": query,
                            "http_version": environ.get("SERVER_PROTOCOL", ""),
                            "http_status_code": status_code,
                            "http_request_time": request_time,
                            "http_user_agent": environ.get("HTTP_USER_AGENT", ""),
                            "http_referer": environ.get("HTTP_REFERER", ""),
                        },
                    )
            except Exception as e:
                logging.getLogger("dta_observability").error(f"Error in Flask access log hook: {e}", exc_info=True)

        from typing import List

        from opentelemetry.trace.span import Span as OTelSpan

        # Type adaptation for the hooks
        def request_hook_adapter(span: OTelSpan, environ: Dict[str, Any]) -> None:
            from opentelemetry.sdk.trace import Span as SDKSpan

            if isinstance(span, SDKSpan):
                request_hook(span, environ)

        def response_hook_adapter(
            span: OTelSpan, environ: Dict[str, Any], status: str, response_headers: List[tuple[str, str]]
        ) -> None:
            from opentelemetry.sdk.trace import Span as SDKSpan

            if isinstance(span, SDKSpan):
                # Convert response_headers to dict for type compatibility
                headers_dict = {k: v for k, v in response_headers} if response_headers else {}
                response_hook(span, environ, status, headers_dict)

        app.wsgi_app = OpenTelemetryMiddleware(
            app.wsgi_app,
            request_hook=request_hook_adapter,
            response_hook=response_hook_adapter,
            tracer_provider=self.tracer_provider,
        )

    def _add_gunicorn_fork_hooks(self, app: Any) -> None:
        """
        Add post-fork hooks for Gunicorn workers.

        This helps handle the issue where BatchSpanProcessor is not fork-safe.

        Args:
            app: The Flask application
        """
        if hasattr(app, "dta_observability_post_fork"):
            return

        def post_fork(server, worker):
            """
            Re-initialize telemetry in forked worker processes.

            This fixes the issue with BatchSpanProcessor not being fork-safe.
            """
            import logging

            from dta_observability.logging.logger import get_logger

            root_logger = logging.getLogger()
            if not root_logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                handler.setFormatter(formatter)
                root_logger.addHandler(handler)
                root_logger.setLevel(logging.INFO)

            worker_logger = get_logger("dta_observability.worker")
            worker_logger.info("Worker spawned (pid: %s) - Reinitializing telemetry", worker.pid)
            log_level = app.config.get("DTA_LOG_LEVEL")
            if log_level is not None and isinstance(log_level, str):
                try:
                    log_level = int(log_level)
                except ValueError:
                    log_level = logging.INFO

            exporter_type = app.config.get("EXPORTER_TYPE", "otlp")

            worker_logger.info(f"Telemetry reinitialized in worker process with {exporter_type} exporter")

        app.dta_observability_post_fork = post_fork
        self.logger.info("Gunicorn post_fork hooks registered for fork-safe BatchSpanProcessor")
