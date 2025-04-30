"""
Celery specific helpers for DTA Observability.
"""

# type: ignore

from typing import Any

from dta_observability.core.config import get_log_level
from dta_observability.logging.logger import get_logger

logger = get_logger(__name__)


def _setup_basic_handlers(celery_app: Any) -> None:
    """Setup minimal handlers for telemetry."""
    try:

        celery_app.conf.worker_hijack_root_logger = False

        # mypy: ignore-errors
        from celery.signals import (  # type: ignore
            setup_logging,
            worker_process_init,
        )

        @setup_logging.connect(weak=False)
        def on_setup_logging(**kwargs):
            """
            Prevent Celery from setting up its own logging.
            This ensures our OpenTelemetry logging is preserved.
            """

            from dta_observability.logging.logger import LoggingConfigurator

            try:

                log_level = get_log_level()
                log_handler = LoggingConfigurator.create_handler(level=log_level, safe_logging=True)

                LoggingConfigurator.configure_root_logger(log_level, log_handler, replace_existing=True)

                print("DTA Observability: Logging reconfigured in setup_logging phase")
            except Exception as e:
                print(f"Error in setup_logging: {e}")

            return True

        @worker_process_init.connect(weak=False)
        def on_worker_process_init(**kwargs):
            """Reinitialize logging when worker process starts."""

            from dta_observability.logging.logger import LoggingConfigurator

            try:

                log_level = get_log_level()
                log_handler = LoggingConfigurator.create_handler(level=log_level, safe_logging=True)

                LoggingConfigurator.configure_root_logger(log_level, log_handler, replace_existing=True)

                LoggingConfigurator.ensure_all_loggers_propagate()

                LoggingConfigurator.mark_configured()

            except Exception as e:

                print(f"Error reinitializing logging in worker: {e}")

    except Exception as e:
        logger.error("Failed to set up Celery handlers: %s", e)


def instrument_celery(celery_app: Any) -> None:
    """
    Instrument a Celery application with DTA Observability.

    Args:
        celery_app: The Celery application instance
    """
    if not celery_app:
        return

    if getattr(celery_app, "_dta_celery_helpers_instrumented", False):
        logger.debug("Celery app already instrumented by celery_helpers, skipping")
        return

    _setup_basic_handlers(celery_app)

    setattr(celery_app, "_dta_celery_helpers_instrumented", True)

    logger.info("Celery app instrumentation completed")
