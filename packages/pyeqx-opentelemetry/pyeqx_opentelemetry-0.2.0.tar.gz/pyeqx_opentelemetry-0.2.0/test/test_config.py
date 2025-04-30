from unittest import TestCase

from pyeqx.opentelemetry.config import TelemetryType
from pyeqx.opentelemetry.constants import DEFAULT_OTLP_ENDPOINT, DEFAULT_OTLP_PROTOCOL


class TestConfig(TestCase):
    def test_instantiate_should_success(self):
        from pyeqx.opentelemetry.config import TelemetryConfiguration

        # act
        config = TelemetryConfiguration(
            service_name="test-service",
        )

        # assert
        self.assertIsNotNone(config)
        self.assertEqual(config.service_name, "test-service")
        self.assertEqual(config.type, TelemetryType.OTLP)
        self.assertEqual(config.endpoint, DEFAULT_OTLP_ENDPOINT)
        self.assertEqual(config.protocol, DEFAULT_OTLP_PROTOCOL)
