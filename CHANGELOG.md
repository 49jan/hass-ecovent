# Changelog

All notable changes to this project will be documented in this file.

## [1.5] - 2025-10-22

### Fixed
- Fixed AttributeError for '_unit_type' object when accessing unknown device models (closes #5)
- Fixed AttributeError for '_device_search' object when device ID cannot be retrieved (closes #5)
- Fixed AttributeError for '_state' object during initialization (closes #5)
- Added proper initialization of critical attributes to prevent runtime errors
- Added support for additional device models (TwinFresh, Winzel, Flexit)
- Made extra_state_attributes method more robust with safe attribute access
- Improved error handling for unknown unit types with better logging
- Fixed device ID auto-detection logic that never worked due to initialization order
- Added graceful fallback when device ID cannot be auto-detected
- Fixed services.yaml airflow selector with empty option that broke HA UI (closes #11)

### Added
- Support for Winzel Expert WiFi RW1-50 P model
- Support for TwinFresh Expert RW1-50 model
- Support for Flexit Roomie Dual model
- Better logging for unknown device types to help with future support

## [1.4] - 2025-07-29

### Fixed
- Fixed "Entity does not support action fan.turn_on" error for newer Home Assistant versions (2024.5+)
- Added missing FanEntityFeature.TURN_ON and FanEntityFeature.TURN_OFF to supported_features
- Added required is_on and percentage properties for fan entity compliance
- Fixed async_turn_off method to accept **kwargs parameter
- Fixed sync turn_on/turn_off methods to avoid calling async methods directly
- Ensured _speed is properly initialized in constructor

### Changed
- Updated fan entity implementation to comply with latest Home Assistant requirements
- Improved compatibility with Home Assistant 2024.5.0 and newer versions

## [1.3] - Previous version
- Previous functionality (details from original repository)
