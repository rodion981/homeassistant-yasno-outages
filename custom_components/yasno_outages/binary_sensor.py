"""Binary sensors for Alerts Energy outages."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import AlertsEnergyCoordinator, outage_periods


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the current-outage sensor."""
    coordinator: AlertsEnergyCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AlertsEnergyOutageNow(coordinator, entry)])


class AlertsEnergyOutageNow(
    CoordinatorEntity[AlertsEnergyCoordinator],
    BinarySensorEntity,
):
    """Whether the selected queue is currently scheduled off."""

    _attr_device_class = BinarySensorDeviceClass.POWER
    _attr_has_entity_name = True
    _attr_icon = "mdi:power-plug-off"
    _attr_translation_key = "outage_now"

    def __init__(
        self,
        coordinator: AlertsEnergyCoordinator,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id}_outage_now"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.unique_id or entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Alerts Energy",
            "configuration_url": "https://alerts.energy/kyiv",
        }

    @property
    def is_on(self) -> bool:
        """Return true when the current half hour is an outage."""
        now = dt_util.now()
        boundary = now.hour * 2 + (1 if now.minute >= 30 else 0)
        return any(
            start <= boundary < end
            for start, end in outage_periods(self.coordinator.data["today"])
        )
