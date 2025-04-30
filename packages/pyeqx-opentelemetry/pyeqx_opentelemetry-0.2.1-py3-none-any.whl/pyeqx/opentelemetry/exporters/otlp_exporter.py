from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as OTLPHttpSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
    OTLPMetricExporter as OTLPHttpMetricExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPGrpcSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter as OTLPGrpcMetricExporter,
)

from pyeqx.opentelemetry.constants import DEFAULT_OTLP_PROTOCOL


def create_otlp_exporter(endpoint: str, protocol: str = DEFAULT_OTLP_PROTOCOL):
    if protocol == "grpc":
        return (
            OTLPGrpcSpanExporter(endpoint=endpoint),
            OTLPGrpcMetricExporter(endpoint=endpoint),
        )
    elif protocol == "http":
        return (
            OTLPHttpSpanExporter(endpoint=endpoint),
            OTLPHttpMetricExporter(endpoint=endpoint),
        )
    else:
        raise ValueError(f"Unsupported OTLP protocol: {protocol}")
