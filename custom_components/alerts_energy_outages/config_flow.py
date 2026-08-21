"""Config flow for Alerts Energy Outages."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import CONF_OPERATOR, DEFAULT_OPERATOR, DEFAULT_QUEUE, DOMAIN

QUEUES = [f"{group}.{subgroup}" for group in range(1, 7) for subgroup in (1, 2)]


class AlertsEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle an Alerts Energy config flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """Create an entry for a Kyiv DTEK queue."""
        if user_input is not None:
            queue = user_input["queue"]
            await self.async_set_unique_id(f"{DEFAULT_OPERATOR}_{queue}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=user_input.get(CONF_NAME) or f"Київ, черга {queue}",
                data={
                    CONF_OPERATOR: DEFAULT_OPERATOR,
                    "queue": queue,
                },
            )

        schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default="Alerts Energy"): str,
                vol.Required("queue", default=DEFAULT_QUEUE): vol.In(QUEUES),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

