"""Config flow for EcoVent."""

from __future__ import annotations

import ipaddress

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_DEFAULT_DEVICE_ID,
    CONF_DEFAULT_NAME,
    CONF_DEFAULT_PASSWORD,
    CONF_DEFAULT_PORT,
    DOMAIN,
)
from .fan import EcoVentFan


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidHost(Exception):
    """Error to indicate host input is invalid."""


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=CONF_DEFAULT_NAME): str,
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Optional(CONF_DEVICE_ID, default=CONF_DEFAULT_DEVICE_ID): str,
        vol.Optional(CONF_PORT, default=CONF_DEFAULT_PORT): int,
        vol.Optional(CONF_PASSWORD, default=CONF_DEFAULT_PASSWORD): str,
    }
)


async def _async_validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Validate user input by connecting to the target device."""
    try:
        ipaddress.ip_address(data[CONF_IP_ADDRESS])
    except ValueError as err:
        raise InvalidHost from err

    def _probe() -> tuple[str, str]:
        device = EcoVentFan(
            hass,
            {},
            str(data[CONF_IP_ADDRESS]),
            data.get(CONF_PASSWORD, CONF_DEFAULT_PASSWORD),
            data.get(CONF_DEVICE_ID, CONF_DEFAULT_DEVICE_ID),
            data.get(CONF_NAME, CONF_DEFAULT_NAME),
            data.get(CONF_PORT, CONF_DEFAULT_PORT),
        )
        unique = device.id if device.id and device.id != CONF_DEFAULT_DEVICE_ID else str(data[CONF_IP_ADDRESS])
        title = data.get(CONF_NAME) or str(data[CONF_IP_ADDRESS])
        return unique, title

    try:
        unique_id, title = await hass.async_add_executor_job(_probe)
    except Exception as err:  # pylint: disable=broad-except
        raise CannotConnect from err

    return {
        "title": title,
        "unique_id": unique_id,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EcoVent."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        """Handle the user step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await _async_validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["base"] = "invalid_host"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["unique_id"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_import(self, import_data: dict) -> FlowResult:
        """Handle import from YAML configuration."""
        try:
            info = await _async_validate_input(self.hass, import_data)
        except (CannotConnect, InvalidHost):
            return self.async_abort(reason="cannot_connect")

        await self.async_set_unique_id(info["unique_id"])
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=info["title"], data=import_data)
