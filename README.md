# EcoVent Home Assistant Integration

[![HACS Badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/49jan/hass-ecovent)

Home Assistant custom component for heat recovery ventilation units.
See below sections for details about 'supported' ventilation units.

## Installation

### HACS

The recommended way of installing this component is using the [Home Assistant Community Store](https://hacs.xyz).
To install the integration follow these steps:

1. Go to the HACS Settings and add the custom repository `49jan/hass-ecovent` with category "Integration".
2. Open the "Integrations" tab and search for "EcoVent".
3. Follow the instructions on the page to set the integration up.

### Manual installation

Copy the contents of the [custom_components](custom_components) folder to the `custom_components` folder in your Home Assistant config directory.
You may need to create the `custom_components` folder if this is the first integration you're installing.
It should look something like this:

```
├── custom_components
│   └── ecovent
│       ├── __init__.py
│       ├── configuration.yaml
│       ├── const.py
│       ├── fan.py
│       ├── manifest.json
│       └── services.yaml
```

Follow the instructions in the [info.md](info.md) file for the configuration and usage documentation.

### Configure Home Assistant
The device must be pre-connected to the network and in the same LAN as home-assistant.

#### Configuration Variables

- **name** (*Optional*): Friendly name for this fan
- **ip_address** (*Required*): IP address of this fan
- **port** (*Optional*): Port of device. Need to be set if you have changed port or your device has a different port than the default value. The default port is 4000
- **device_id** (*Optional*): Id of device.
- **password** (*Optional*): Password of the fan. Necessary to set if you have changed password or your device has a different password than the default. The default pass is 1111

#### Configuration Example

This example configuration assumes that the relay switches are already setup in Home Assistant, since that setup differs
substantially depending on the type of relay hardware being used (e.g. Tasmota MQTT vs WeMo Maker).

```yaml
fan:
  - platform: ecovent
    ip_address: "192.168.1.200"

  - platform: ecovent
    name: Kitchen fan
    ip_address: "192.168.1.205"
    device_id: "85481285"
    port: 4000
    password: !secret blauberg_pass
```

### Add Lovelace Card

The following is a basic Lovelace card using the [fan-control-entity-row](https://community.home-assistant.io/t/lovelace-fan-control-entity-row/102952) customization:

![Blauberg Simple Example](https://github.com/49jan/hass-ecovent/blob/88124903f6bcde9aff00267a47db16804d6bef8a/img/blauberg-fan-control-example.png?raw=true)

```yaml
- entity: fan.basement_fan 
  type: custom:fan-control-entity-row
```
And another example with multiple Blauberg ventilation fans and ability to turn on/off the entire house:

![Blauberg Simple Example](https://github.com/49jan/hass-ecovent/blob/88124903f6bcde9aff00267a47db16804d6bef8a/img/blauberg-fan-control-example-2.png?raw=true)

```yaml
type: entities
title: Blauberg Ventilation
entities:
  - entity: fan.basement_fan 
    name: Basement
    type: 'custom:fan-control-entity-row'
  - entity: fan.bedrooms_fan
    name: Bedrooms
    type: 'custom:fan-control-entity-row'
  - entity: fan.bathroom_fan
    name: Master Bathroom
    type: 'custom:fan-control-entity-row'
```

## Tested fans

This component has only been tested on two [Blauberg Vento Expert A50-1 W](https://blaubergventilatoren.de/en/product/vento-expert-a50-1-w) which are configured as master.

There are fans from Blauberg and Flexit that are identical and should work, but I have not verified that.

- [Blauberg Vento Expert Duo A30-1 W V.2](https://blaubergventilatoren.de/en/series/vento-expert-duo-a30-1-s10-w-v2)
- Blauberg Vento Expert A30 W V.2
- [Twinfresh Expert RW1-50](http://vents-us.com/item/5262/VENTS_TwinFresh_Expert_RW1-50-2_Wi-Fi/)
- [Single room ventilator Roomie Dual](https://www.flexit.no/en/products/single_room_ventilator/single_room_ventilator_roomie_dual/single_room_ventilator_roomie_dual/)
