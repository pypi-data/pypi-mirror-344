"""
FastAPI-specific instrumentation for DTA Observability.
"""

import logging
import time
import weakref
from typing import Any, Dict

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor as OTelFastAPIInstrumentor
from opentelemetry.sdk.trace import Span
from opentelemetry.trace import SpanKind

from dta_observability.core.span import set_span_attribute_safely
from dta_observability.instrumentation.base import BaseInstrumentor
from dta_observability.instrumentation.utils import check_instrumentation_status, handle_instrumentation_error
from dta_observability.logging.logger import get_logger


class FastAPIInstrumentor(BaseInstrumentor):
    """Handles FastAPI-specific instrumentation."""

    _INSTRUMENTED_KEY = "_dta_fastapi_instrumented"

    def __init__(self, tracer_provider=None, logger_provider=None, log_level=None):
        """
        Initialize the FastAPI instrumentor.

        Args:
            tracer_provider: Optional tracer provider to use
            logger_provider: Optional logger provider to use
            log_level: Optional log level to use for access logs
        """
        super().__init__(tracer_provider, logger_provider, log_level)

    def _get_library_name(self) -> str:
        """Get the library name."""
        return "fastapi"

    def instrument_app(self, app: Any) -> bool:
        """
        Instrument a FastAPI application.

        Args:
            app: The FastAPI application to instrument

        Returns:
            True if successful, False otherwise
        """
        if not app:
            return False

        try:
            if check_instrumentation_status(app, self._get_library_name(), self._INSTRUMENTED_KEY):
                self.logger.debug("FastAPI app already instrumented, skipping")
                return True

            self._instrument_app(app)

            setattr(app, self._INSTRUMENTED_KEY, True)
            self.register_app(app)
            self.logger.info("FastAPI app instrumented: %s", app)
            return True

        except Exception as e:
            handle_instrumentation_error(self.logger, "FastAPI", e)
            return False

    def _instrument_app(self, app: Any) -> None:
        """
        Apply OpenTelemetry instrumentation to a FastAPI app.

        This method uses the official OpenTelemetry FastAPI instrumentation
        which handles ASGI middleware internally.

        Args:
            app: The FastAPI application to instrument
        """
        try:
            access_logger = get_logger("fastapi.logs")

            if hasattr(self, "log_level"):
                access_logger.setLevel(self.log_level if isinstance(self.log_level, (int, str)) else logging.INFO)

            self._configure_uvicorn_logging()

            logged_spans: weakref.WeakSet[Any] = weakref.WeakSet()

            def server_request_hook(span: Span, scope: Dict[str, Any]) -> None:
                if not span or not span.is_recording():
                    return

                span._kind = SpanKind.SERVER

                method = scope.get("method", "")
                path = scope.get("path", "")
                route = scope.get("route", "")

                if hasattr(route, "path") and route.path:
                    path = route.path

                if method and path:
                    set_span_attribute_safely(span, "http.route", path)
                    set_span_attribute_safely(span, "http.method", method)

                if hasattr(span, "set_attribute"):
                    span.set_attribute("http.request_start_time", time.time())

            def client_response_hook(span: Span, scope: Dict[str, Any], message: Dict[str, Any]) -> None:
                if not span or not span.is_recording():
                    return

                if message.get("type") != "http.response.start":
                    return

                status_code = message.get("status", 0)
                if status_code == 0:
                    return

                span_id = getattr(span, "span_id", None)
                if span_id in logged_spans:
                    return

                try:
                    method = scope.get("method", "")
                    path = scope.get("path", "")
                    route = scope.get("route", "")

                    normalized_path = path
                    if hasattr(route, "path") and route.path:
                        normalized_path = route.path

                    headers = scope.get("headers", [])
                    headers_dict = {k.decode("utf-8"): v.decode("utf-8") for k, v in headers if k and v}

                    client_ip = scope.get("client", ("unknown", 0))[0]
                    forwarded_for = headers_dict.get("x-forwarded-for", "")
                    if forwarded_for:
                        client_ip = forwarded_for.split(",")[0].strip()

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

                    access_logger.info(
                        f"{method} {normalized_path} {status_code}",
                        extra={
                            "http_client_ip": client_ip,
                            "http_method": method,
                            "http_path": normalized_path,
                            "http_query": scope.get("query_string", b"").decode("utf-8"),
                            "http_version": scope.get("http_version", ""),
                            "http_status_code": status_code,
                            "http_request_time": request_time,
                            "http_user_agent": headers_dict.get("user-agent", ""),
                            "http_referer": headers_dict.get("referer", ""),
                        },
                    )
                except Exception as e:
                    logging.getLogger("dta_observability").error(
                        f"Error in FastAPI access log hook: {e}", exc_info=True
                    )

            from opentelemetry.trace.span import Span as OTelSpan

            # Type adaptation for the hooks
            def server_hook_adapter(span: OTelSpan, scope: Dict[str, Any]) -> None:
                from opentelemetry.sdk.trace import Span as SDKSpan

                if isinstance(span, SDKSpan):
                    server_request_hook(span, scope)

            def client_hook_adapter(span: OTelSpan, scope: Dict[str, Any], message: Dict[str, Any]) -> None:
                from opentelemetry.sdk.trace import Span as SDKSpan

                if isinstance(span, SDKSpan):
                    client_response_hook(span, scope, message)

            OTelFastAPIInstrumentor.instrument_app(
                app,
                tracer_provider=self.tracer_provider,
                server_request_hook=server_hook_adapter,
                client_response_hook=client_hook_adapter,
                exclude_spans=None,
            )

            self.logger.info("FastAPI app instrumented with JSON access logging")

        except ImportError:
            self.logger.warning(
                "OpenTelemetry FastAPI instrumentation not available. "
                "Install with: pip install opentelemetry-instrumentation-fastapi"
            )
            raise

    def _configure_uvicorn_logging(self) -> None:
        """
        Configure uvicorn to use our logging setup instead of its default.

        This is needed because uvicorn sets up its own logging config by default,
        which can bypass our OpenTelemetry instrumentation.
        """
        try:

            from dta_observability.instrumentation.helpers.uvicorn import configure_uvicorn_for_otel

            log_level = getattr(self, "log_level", None)
            configure_uvicorn_for_otel(log_level=log_level)

            for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
                logger = logging.getLogger(logger_name)

                for handler in list(logger.handlers):
                    if not hasattr(handler, "_dta_otel_handler"):
                        logger.removeHandler(handler)

            self.logger.info("Configured uvicorn to use DTA Observability logging handlers")
        except Exception as e:
            self.logger.warning(f"Failed to configure uvicorn logging: {e}", exc_info=True)
