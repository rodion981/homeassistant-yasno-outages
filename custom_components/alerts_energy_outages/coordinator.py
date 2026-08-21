"""Data coordinator and schedule helpers."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import AlertsEnergyApi, AlertsEnergyApiError
from .const import CONF_OPERATOR, DEFAULT_OPERATOR, DOMAIN, SCAN_INTERVAL_SECONDS

type OutagePeriod = tuple[int, int]


def outage_periods(hours: list[int]) -> list[OutagePeriod]:
    """Convert 24 hourly codes to half-hour boundaries in the range 0..48."""
    halves: list[bool] = []
    for value in hours:
        halves.extend((value in (1, 2), value in (1, 3)))

    periods: list[OutagePeriod] = []
    start: int | None = None
    for index, is_outage in enumerate(halves):
        if is_outage and start is None:
            start = index
        elif not is_outage and start is not None:
            periods.append((start, index))
            start = None
    if start is not None:
        periods.append((start, 48))
    return periods


def format_boundary(boundary: int) -> str:
    """Format a half-hour boundary as HH:MM."""
    return f"{boundary // 2:02d}:{(boundary % 2) * 30:02d}"


def format_periods(periods: list[OutagePeriod]) -> str:
    """Format all outage periods for a sensor state."""
    if not periods:
        return "Без відключень"
    return "; ".join(
        f"{format_boundary(start)}–{format_boundary(end)}"
        for start, end in periods
    )


class AlertsEnergyCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Poll Alerts Energy and share the selected schedule with entities."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: AlertsEnergyApi,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self._api = api
        self._operator = entry.data.get(CONF_OPERATOR, DEFAULT_OPERATOR)
        self._queue = entry.data["queue"]

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self._api.async_get_schedule(self._operator, self._queue)
        except AlertsEnergyApiError as err:
            raise UpdateFailed(str(err)) from err

