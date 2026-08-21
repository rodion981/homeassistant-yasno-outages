"""Constants for the Alerts Energy Outages integration."""

from typing import Final

DOMAIN: Final = "yasno_outages"
PLATFORMS: Final = ["sensor", "binary_sensor"]

CONF_OPERATOR: Final = "operator"
DEFAULT_OPERATOR: Final = "kyiv_oblenergo"
DEFAULT_QUEUE: Final = "2.2"

API_URL: Final = (
    "https://alerts.energy/api/v1/source-registry/areas/kyiv/shutdowns"
)
SCAN_INTERVAL_SECONDS: Final = 60
