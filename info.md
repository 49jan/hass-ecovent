# EcoVent

## Configuration

Add the following to your `configuration.yaml`

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

Reload Home Assistant

## Services

The component uses most services from the fan component:
- [Turn on](https://developers.home-assistant.io/docs/core/entity/fan/#turn-on)
- [Turn off](https://developers.home-assistant.io/docs/core/entity/fan/#turn-off)
- [Set preset mode](https://developers.home-assistant.io/docs/core/entity/fan/#set-preset-mode)
- [Set speed percentage](https://developers.home-assistant.io/docs/core/entity/fan/#set-speed-percentage)


### Set airflow
The ecovent component also adds a service to control airflow modes.

Service name: `ecovent.set_airflow`

This service accepts the following input values:

```yaml
target:
  entity_id: "your fan entity id"
data:
  airflow: ventilation

Allowed airflow values are:
  - "ventilation"
  - "heat_recovery"
  - "air_supply"
```

Example service call yaml:

```yaml
service: ecovent.set_airflow
data:
  airflow: ventilation
target:
  entity_id: fan.basement_fan  
```

The 'airflow mode' is shown as a state attribute on the fan component and can be used in automations.

### Set humidity sensor ON
The ecovent component also adds a service to control humidity sensor.

Service name: `ecovent.humidity_sensor_turn_on`

This service accepts the following input values:

```yaml
target:
  entity_id: "your fan entity id"
```

Example service call yaml:

```yaml
service: ecovent.humidity_sensor_turn_on
target:
  entity_id: fan.basement_fan  
```

### Set humidity sensor OFF
The ecovent component also adds a service to control humidity sensor.

Service name: `ecovent.humidity_sensor_turn_off`

This service accepts the following input values:

```yaml
target:
  entity_id: "your fan entity id"
```

Example service call yaml:

```yaml
service: ecovent.humidity_sensor_turn_off
target:
  entity_id: fan.basement_fan  
```

### Treshold of humidity sensor
Set the humidity threshold when the fan turns on automatically.

Service name: `ecovent.set_humidity_sensor_treshold_percentage`

This service accepts the following input values:

```yaml
data:
  percentage: "Humidity treshold in percentage. Allowed values are between 40 and 80."
target:
  entity_id: "your fan entity id"
```

Example service call yaml:

```yaml
service: ecovent.set_humidity_sensor_treshold_percentage
data:
  percentage: 70
target:
  entity_id: fan.basement_fan  
```

### Treshold of humidity sensor
Clears the filter replacement warning.

Service name: `ecovent.clear_filter_reminder`

This service accepts the following input values:

```yaml
target:
  entity_id: "your fan entity id"
```

Example service call yaml:

```yaml
service: ecovent.clear_filter_reminder
target:
  entity_id: fan.basement_fan  
```

