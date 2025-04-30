"""
Resource detection for DTA Observability.
"""

import os
import platform
import socket
import sys
from typing import Any, Dict, Optional

from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from dta_observability.core.config import ConfigValueType, get_boolean_config, get_typed_config


class CloudPlatformDetector:
    """Detects cloud platform information."""

    @staticmethod
    def detect() -> Optional[str]:
        """
        Detect the cloud platform the application is running on.

        Returns:
            String identifying the cloud platform or None if not detected.
        """

        if os.environ.get("KUBERNETES_SERVICE_HOST"):
            return "kubernetes"

        if os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT"):
            return "gcp"

        if os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"):
            return "aws"

        if os.environ.get("AZURE_REGION") or os.environ.get("AZURE_LOCATION"):
            return "azure"

        return None


class ProcessInfoDetector:
    """Detects process information."""

    @staticmethod
    def detect() -> Dict[str, str]:
        """
        Get resource attributes for the current process.

        Returns:
            Dictionary of process resource attributes.
        """
        return {
            ResourceAttributes.PROCESS_PID: str(os.getpid()),
            ResourceAttributes.PROCESS_RUNTIME_NAME: "CPython",
            ResourceAttributes.PROCESS_RUNTIME_VERSION: platform.python_version(),
            ResourceAttributes.PROCESS_EXECUTABLE_PATH: sys.executable,
        }


def detect_resources(override_attrs: Optional[Dict[str, Any]] = None) -> Resource:
    """
    Detect resources from the environment.

    Args:
        override_attrs: Optional dictionary of attributes that override detected ones

    Returns:
        OpenTelemetry Resource with detected attributes.
    """

    enabled = get_boolean_config("RESOURCE_DETECTORS_ENABLED")
    if not enabled:

        return Resource(override_attrs or {})

    attributes = {}

    service_name = get_typed_config("SERVICE_NAME", ConfigValueType.STRING, "unnamed-service")
    service_version = get_typed_config("SERVICE_VERSION", ConfigValueType.STRING, "0.0.0")
    service_instance_id = get_typed_config("SERVICE_INSTANCE_ID", ConfigValueType.STRING, socket.gethostname())

    attributes.update(
        {
            ResourceAttributes.SERVICE_NAME: service_name,
            ResourceAttributes.SERVICE_VERSION: service_version,
            ResourceAttributes.SERVICE_INSTANCE_ID: service_instance_id,
        }
    )

    cloud_platform = CloudPlatformDetector.detect()
    if cloud_platform:
        attributes["cloud.provider"] = cloud_platform

    attributes.update(ProcessInfoDetector.detect())

    if override_attrs:
        for key, value in override_attrs.items():
            if value is not None:
                attributes[key] = value

    return Resource(attributes)
