"""Binary sensor platform for EcoVent warnings/status."""

from __future__ import annotations

import ipaddress
import logging
import time
from dataclasses import dataclass
from typing import Callable

import voluptuous as vol
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
    PLATFORM_SCHEMA,
)
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers import entity_registry as er

from .const import (
    CONF_DEFAULT_DEVICE_ID,
    CONF_DEFAULT_NAME,
    CONF_DEFAULT_PASSWORD,
    CONF_DEFAULT_PORT,
    DOMAIN,
)
from .fan import EcoVentFan

LOG = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=CONF_DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_ID, default=CONF_DEFAULT_DEVICE_ID): cv.string,
        vol.Required(CONF_IP_ADDRESS): vol.All(ipaddress.ip_address, cv.string),
        vol.Optional(CONF_PORT, default=CONF_DEFAULT_PORT): cv.port,
        vol.Optional(CONF_PASSWORD, default=CONF_DEFAULT_PASSWORD): cv.string,
    }
)

_MIN_UPDATE_INTERVAL_SECONDS = 20


@dataclass(frozen=True, kw_only=True)
class EcoVentBinaryDescription(BinarySensorEntityDescription):
    is_on_fn: Callable[[EcoVentFan], bool]


BINARY_DESCRIPTIONS: tuple[EcoVentBinaryDescription, ...] = (
    EcoVentBinaryDescription(
        key="filter_replacement_required",
        name="Filter replacement required",
        is_on_fn=lambda dev: getattr(dev, "filter_replacement_status", "off") == "on",
    ),
    EcoVentBinaryDescription(
        key="alarm_active",
        name="Alarm active",
        is_on_fn=lambda dev: getattr(dev, "alarm_status", "no") != "no",
    ),
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up EcoVent warning/status binary sensors from YAML config."""
    device = _create_device(hass, config)

    entities = []
    for description in BINARY_DESCRIPTIONS:
        entity = EcoVentStatusBinarySensor(device, description)
        desired_entity_id = async_generate_entity_id(
            "binary_sensor.{}",
            f"{device.name}_{description.key}",
            hass=hass,
        )
        _async_migrate_binary_entity_id(hass, entity.unique_id, desired_entity_id)
        entity.entity_id = desired_entity_id
        entities.append(entity)
    async_add_entities(entities, update_before_add=True)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up EcoVent warning/status binary sensors from config entry."""
    device = _create_device(hass, entry.data)
    entities = []
    for description in BINARY_DESCRIPTIONS:
        entity = EcoVentStatusBinarySensor(device, description)
        desired_entity_id = async_generate_entity_id(
            "binary_sensor.{}",
            f"{device.name}_{description.key}",
            hass=hass,
        )
        _async_migrate_binary_entity_id(hass, entity.unique_id, desired_entity_id)
        entity.entity_id = desired_entity_id
        entities.append(entity)
    async_add_entities(entities, update_before_add=True)


def _create_device(hass, cfg) -> EcoVentFan:
    return EcoVentFan(
        hass,
        cfg,
        cfg.get(CONF_IP_ADDRESS),
        cfg.get(CONF_PASSWORD),
        cfg.get(CONF_DEVICE_ID),
        cfg.get(CONF_NAME),
        cfg.get(CONF_PORT),
    )


def _async_migrate_binary_entity_id(
    hass, unique_id: str | None, desired_entity_id: str
) -> None:
    """Rename existing binary sensor entity ID to the desired name-based ID."""
    if not unique_id:
        return
    registry = er.async_get(hass)
    current_entity_id = registry.async_get_entity_id(
        "binary_sensor", DOMAIN, unique_id
    )
    if not current_entity_id or current_entity_id == desired_entity_id:
        return
    try:
        registry.async_update_entity(current_entity_id, new_entity_id=desired_entity_id)
    except ValueError:
        LOG.debug(
            "Cannot migrate binary_sensor entity_id from %s to %s because target is in use",
            current_entity_id,
            desired_entity_id,
        )


class EcoVentStatusBinarySensor(BinarySensorEntity):
    """Status binary sensor bound to a shared EcoVent device session."""

    _attr_has_entity_name = False

    def __init__(self, device: EcoVentFan, description: EcoVentBinaryDescription) -> None:
        self._device = device
        self.entity_description = description
        self._attr_name = description.name
        self._attr_translation_key = description.key
        self._attr_unique_id = f"{device.id}_{description.key}"
        self._attr_suggested_object_id = f"{device.name}_{description.key}"
        self._attr_is_on = False

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(DOMAIN, self._device.id)},
            "name": self._device.name,
            "manufacturer": "EcoVent/Blauberg",
            "model": getattr(self._device, "unit_type", None),
        }

    def _refresh_device_if_needed(self) -> None:
        now = time.monotonic()
        last_update_ts = getattr(self._device, "_ecovent_diag_last_update", 0.0)
        if now - last_update_ts >= _MIN_UPDATE_INTERVAL_SECONDS:
            try:
                self._device.update()
            except Exception as err:  # pylint: disable=broad-except
                LOG.error("Failed to refresh EcoVent status: %s", err)
            setattr(self._device, "_ecovent_diag_last_update", now)

    def update(self) -> None:
        self._refresh_device_if_needed()
        self._attr_is_on = self.entity_description.is_on_fn(self._device)
