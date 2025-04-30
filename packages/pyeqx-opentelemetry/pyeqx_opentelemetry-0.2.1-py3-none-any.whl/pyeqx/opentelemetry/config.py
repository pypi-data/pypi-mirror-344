from dataclasses import dataclass
from enum import Enum

from pyeqx.opentelemetry.constants import (
    DEFAULT_OTLP_ENDPOINT,
    DEFAULT_OTLP_PROTOCOL,
)


class TelemetryType(str, Enum):
    OTLP = "otlp"
    AZURE_MONITOR = "azuremonitor"


@dataclass
class TelemetryConfiguration:
    service_name: str
    type: TelemetryType
    endpoint: str
    protocol: str

    def __init__(
        self,
        service_name: str,
        type: TelemetryType = TelemetryType.OTLP,
        endpoint: str = None,
        protocol: str = None,
    ):
        self.service_name = service_name
        self.type = type

        if type == TelemetryType.OTLP:
            self.endpoint = endpoint or DEFAULT_OTLP_ENDPOINT
            self.protocol = protocol or DEFAULT_OTLP_PROTOCOL
        else:
            self.endpoint = endpoint
            self.protocol = None
