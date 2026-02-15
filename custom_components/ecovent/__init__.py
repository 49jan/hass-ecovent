"""Eco Ventilation Fan Control for Home Assistant."""

from __future__ import annotations

import logging

from homeassistant.components.fan import DOMAIN as FAN_DOMAIN
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
)
from homeassistant.core import HomeAssistant

from .const import (
    CONF_DEFAULT_DEVICE_ID,
    CONF_DEFAULT_NAME,
    CONF_DEFAULT_PASSWORD,
    CONF_DEFAULT_PORT,
    DOMAIN,
)

LOG = logging.getLogger(__name__)

PLATFORMS: list[str] = ["fan", "sensor", "binary_sensor", "select"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up EcoVent and import legacy YAML fan configs into config entries."""
    fan_configs = config.get(FAN_DOMAIN, [])
    for fan_conf in fan_configs:
        if fan_conf.get("platform") != DOMAIN:
            continue

        import_data = {
            CONF_NAME: fan_conf.get(CONF_NAME, CONF_DEFAULT_NAME),
            CONF_IP_ADDRESS: str(fan_conf[CONF_IP_ADDRESS]),
            CONF_DEVICE_ID: fan_conf.get(CONF_DEVICE_ID, CONF_DEFAULT_DEVICE_ID),
            CONF_PORT: fan_conf.get(CONF_PORT, CONF_DEFAULT_PORT),
            CONF_PASSWORD: fan_conf.get(CONF_PASSWORD, CONF_DEFAULT_PASSWORD),
        }

        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data=import_data,
            )
        )
        LOG.warning(
            "Legacy YAML configuration for ecovent was detected and imported. "
            "Please remove ecovent entries from configuration.yaml after confirming entities exist."
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up EcoVent from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload an EcoVent config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return unload_ok
