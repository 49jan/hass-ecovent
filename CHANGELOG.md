# Changelog

All notable changes to this project will be documented in this file.

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
