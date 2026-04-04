# CHANGELOG

All notable development changes for `T000040-probabilistic-stimulus-selection` are documented here.

## [Unreleased] - 2026-04-04

### Added
- Added a probabilistic stimulus selection pipeline with three learning pairs, a criterion-driven transfer test, and kana role assignment.
- Added reference-curated literature files for the canonical PSS protocol and supporting reinforcement-learning variants.
- Added learning-block schedule helpers, transfer-block summary helpers, and a PSS simulation responder.

### Changed
- Replaced the previous reward-learning scaffold with a classic probabilistic stimulus selection task.
- Reworked configs to 60-trial learning blocks, 150-trial transfer blocks, 80/20 to 60/40 contingencies, and 65/60/50 acquisition criteria.
- Updated participant-facing Chinese instructions, kana stimuli, and task metadata for the new paradigm.

### Fixed
- Added the contract-required config metadata fields for validation and preview QA.
- Switched the scripted simulation config to the built-in `scripted` responder.
