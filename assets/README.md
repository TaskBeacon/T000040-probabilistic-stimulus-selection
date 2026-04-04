# Assets for Probabilistic Stimulus Selection

This task is intentionally asset-light.

- The participant-visible symbols are six kana text stimuli defined in `config/config.yaml`.
- The instructions, feedback, and fixation screens are also config-defined text stimuli.
- The optional `instruction_text_voice.mp3` file may be used when `voice_enabled` is enabled, but the default human/QA/sim configs keep voice playback off.

If a future protocol revision needs new media, add only reference-aligned assets and update `references/stimulus_mapping.md` accordingly.
