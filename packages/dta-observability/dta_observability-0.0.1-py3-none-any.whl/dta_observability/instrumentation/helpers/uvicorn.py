from typing import Optional

from dta_observability.logging.logger import get_logger

logger = get_logger(__name__)


def configure_uvicorn_for_otel(log_level: Optional[int] = None) -> None:
    """
    Configure uvicorn to use OpenTelemetry logging handlers.

    This function should be called before starting uvicorn to ensure
    that it uses our OpenTelemetry instrumented logging instead of
    its default configuration.

    Args:
        log_level: Optional log level to set for uvicorn loggers
    """
    try:

        import uvicorn.config

        uvicorn.config.LOGGING_CONFIG = {}

        uvicorn_logger = get_logger("uvicorn")
        uvicorn_access = get_logger("uvicorn.access")
        uvicorn_error = get_logger("uvicorn.error")

        if log_level is not None:
            uvicorn_logger.setLevel(log_level)
            uvicorn_access.setLevel(log_level)
            uvicorn_error.setLevel(log_level)

        uvicorn_access.disabled = True
        uvicorn_access.propagate = False

        for uvicorn_log in [uvicorn_logger, uvicorn_access, uvicorn_error]:
            for handler in list(uvicorn_log.handlers):
                uvicorn_log.removeHandler(handler)

        uvicorn.config.Config.configure_logging

        def patched_configure_logging(self):
            """Patched method to skip uvicorn's default logging configuration."""
            uvicorn_logger.info("Intercepted uvicorn logging setup - using DTA Observability handlers")

            self.access_log = False
            self.log_config = None

            self.use_colors = False

            return None

        setattr(uvicorn.config.Config, "configure_logging", patched_configure_logging)

        original_run = uvicorn.run

        def patched_run(app, **kwargs):

            kwargs["access_log"] = False

            kwargs["log_config"] = None

            if "use_colors" not in kwargs:
                kwargs["use_colors"] = False

            return original_run(app, **kwargs)

        uvicorn.run = patched_run

        logger.info("Configured uvicorn to use DTA Observability logging")
    except Exception as e:
        logger.warning(f"Failed to configure uvicorn logging: {e}", exc_info=True)
