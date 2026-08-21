"""Sensors for Alerts Energy outage schedules."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AlertsEnergyCoordinator, format_periods, outage_periods


@dataclass(frozen=True, kw_only=True)
class AlertsEnergySensorDescription(SensorEntityDescription):
    """Describe an Alerts Energy sensor."""

    value_fn: Callable[[dict[str, Any]], str]


DESCRIPTIONS = (
    AlertsEnergySensorDescription(
        key="today",
        translation_key="today",
        icon="mdi:calendar-today",
        value_fn=lambda data: format_periods(outage_periods(data["today"])),
    ),
    AlertsEnergySensorDescription(
        key="tomorrow",
        translation_key="tomorrow",
        icon="mdi:calendar-clock",
        value_fn=lambda data: format_periods(outage_periods(data["tomorrow"])),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up schedule sensors."""
    coordinator: AlertsEnergyCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        AlertsEnergySensor(coordinator, entry, description)
        for description in DESCRIPTIONS
    )


class AlertsEnergySensor(
    CoordinatorEntity[AlertsEnergyCoordinator],
    SensorEntity,
):
    """Representation of an Alerts Energy schedule."""

    entity_description: AlertsEnergySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AlertsEnergyCoordinator,
        entry: ConfigEntry,
        description: AlertsEnergySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.unique_id or entry.entry_id)},
            "name": entry.title,
            "manufacturer": "Alerts Energy",
            "configuration_url": "https://alerts.energy/kyiv",
        }

    @property
    def native_value(self) -> str:
        """Return the formatted schedule."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose source data for dashboards and automations."""
        day = self.entity_description.key
        hours = self.coordinator.data[day]
        return {
            "queue": self.coordinator.data["queue"],
            "operator": self.coordinator.data["initiator"],
            "updated": self.coordinator.data.get("updated"),
            "hours": hours,
            "periods": [
                {
                    "start": f"{start // 2:02d}:{(start % 2) * 30:02d}",
                    "end": f"{end // 2:02d}:{(end % 2) * 30:02d}",
                }
                for start, end in outage_periods(hours)
            ],
        }
