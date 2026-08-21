"""Client for the public Alerts Energy schedule endpoint."""

from __future__ import annotations

from typing import Any

from aiohttp import ClientError, ClientSession

from .const import API_URL


class AlertsEnergyApiError(Exception):
    """Raised when Alerts Energy cannot provide a valid schedule."""


class AlertsEnergyApi:
    """Small async client for Alerts Energy."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def async_get_schedule(self, operator: str, queue: str) -> dict[str, Any]:
        """Return the schedule for one operator and queue."""
        try:
            async with self._session.get(
                API_URL,
                headers={
                    "Accept": "application/json",
                    "Referer": "https://alerts.energy/kyiv",
                },
                timeout=30,
            ) as response:
                response.raise_for_status()
                payload = await response.json()
        except (ClientError, TimeoutError, ValueError) as err:
            raise AlertsEnergyApiError(str(err)) from err

        if not isinstance(payload, list):
            raise AlertsEnergyApiError("Unexpected response format")

        row = next(
            (
                item
                for item in payload
                if item.get("initiator") == operator and item.get("queue") == queue
            ),
            None,
        )
        if row is None:
            raise AlertsEnergyApiError(
                f"Schedule not found for operator {operator}, queue {queue}"
            )

        for day in ("today", "tomorrow"):
            if not isinstance(row.get(day), list) or len(row[day]) != 24:
                raise AlertsEnergyApiError(f"Invalid {day} schedule")
        return row

