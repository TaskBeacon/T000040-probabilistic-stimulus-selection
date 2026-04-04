# Probabilistic Stimulus Selection

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Probabilistic Stimulus Selection |
| Version | v0.1.0-dev |
| URL / Repository | E:/Taskbeacon/T000040-probabilistic-stimulus-selection |
| Short Description | Chinese probabilistic reinforcement-learning task with three learning pairs, 15 transfer pairings, and kana stimuli. |
| Created By | TaskBeacon |
| Date Updated | 2026-04-04 |
| PsyFlow Version | 0.1.12 |
| PsychoPy Version | 2025.2.4 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural |

## 1. Task Overview

This task reproduces the classic probabilistic stimulus selection paradigm in a Chinese-localized PsyFlow implementation. Participants learn three two-option pairings, `AB`, `CD`, and `EF`, where the higher-probability role is rewarded at 80/20, 70/30, and 60/40, respectively. After learning reaches criterion, the task presents all 15 possible pairings without feedback to measure transfer bias and learned preference.

The six visible symbols are Japanese kana glyphs rendered from PsychoPy text stimuli. Their mapping to roles `A-F` is randomized per participant, so the same learning structure is preserved while the concrete symbols vary across runs.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Parse mode/config | `main.py` loads `human`, `qa`, or `sim` mode and the matching YAML config. |
| 2. Initialize runtime | Window, keyboard, triggers, and stimulus bank are initialized. |
| 3. Assign roles | Six kana symbols are shuffled into roles `A-F` deterministically from the subject seed. |
| 4. Run instructions | The participant reads the Chinese instruction page and presses space to start. |
| 5. Run learning blocks | Learning blocks repeat until all pair criteria are met or `max_learning_blocks` is reached. |
| 6. Run transfer block | One transfer block presents all 15 pairings with no feedback. |
| 7. Finish | The goodbye screen appears and all trial data are saved. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Block ready | A centered ready screen appears for `3.0 s` before each block. |
| Choice screen | Two kana symbols appear left and right; the participant responds with the left or right key within `4.0 s`. |
| Feedback, learning only | A probabilistic `正确` or `错误` screen appears for `1.0 s` based on the chosen role's reward probability. |
| No-feedback transfer | Transfer trials skip feedback and go straight to the inter-trial interval. |
| Inter-trial interval | A fixation `+` appears for `1.0 s` before the next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Role assignment | `build_role_assignment(...)` shuffles the six kana stimuli into roles `A-F` per participant. |
| Learning schedule | `build_learning_block_schedule(...)` creates exactly 20 trials per learning pair with exact within-block left/right balance. |
| Transfer schedule | `build_transfer_block_schedule(...)` creates exactly 10 trials per transfer pair across all 15 pairings. |
| Probabilistic feedback | On learning trials, the chosen role is sampled against its pair-specific win probability. |
| Criterion check | `evaluate_learning_block(...)` requires `AB >= 0.65`, `CD >= 0.60`, and `EF >= 0.50`. |
| Transfer summary | `summarize_transfer_block(...)` reports role choice rates and timeout counts for audit logs. |

### Other Logic

| Component | Description |
|---|---|
| Hidden score | A hidden cumulative score is tracked from learning feedback outcomes, but it is not shown to participants. |
| No-response policy | Learning timeouts count as incorrect; transfer omissions are logged but do not create feedback. |
| QA and sim modes | `config/config_qa.yaml`, `config/config_scripted_sim.yaml`, and `config/config_sampler_sim.yaml` reuse the same task logic with shorter smoke-test schedules. |
| Stimulus rendering | All participant-facing text and symbols are PsychoPy text stimuli defined in YAML; no external media is required. |

## 3. Configuration Summary

All human settings are defined in `config/config.yaml`. QA and smoke-test overrides live in `config/config_qa.yaml`, `config/config_scripted_sim.yaml`, and `config/config_sampler_sim.yaml`.

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier used to seed the kana role assignment. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `black` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `instruction_text` | text | Chinese instruction page with left/right key labels injected at runtime. |
| `block_ready` | text | Ready screen for learning or transfer blocks. |
| `iti_fixation` | text | Centered `+` used during the inter-trial interval. |
| `feedback_correct` | text | Green Chinese correctness cue `正确`. |
| `feedback_incorrect` | text | Orange Chinese error cue `错误`. |
| `good_bye` | text | Final exit screen. |
| `kana_1` to `kana_6` | text | Six kana glyphs (`あ`, `い`, `う`, `え`, `お`, `か`) that are randomly assigned to roles `A-F` per participant. |

### d. Timing

| Phase | Duration |
|---|---|
| Block ready | `3.0 s` |
| Response window | `4.0 s` |
| Learning feedback | `1.0 s` |
| Inter-trial interval | `1.0 s` |

### e. Triggers

| Event | Code |
|---|---:|
| Experiment onset | `1` |
| Experiment end | `2` |
| Block onset | `10` |
| Block end | `11` |
| Trial onset | `20` |
| Left response | `31` |
| Right response | `32` |
| Timeout | `33` |
| Feedback onset | `40` |
| No-feedback onset | `41` |
| ITI onset | `50` |

### f. Adaptive Controller

| Parameter | Value |
|---|---|
| `phase_order` | `learning -> transfer` |
| `learning_conditions` | `train_ab`, `train_cd`, `train_ef` |
| `learning_probabilities` | `AB 80/20`, `CD 70/30`, `EF 60/40` |
| `learning_trials_per_block` | `60` |
| `learning_trials_per_pair` | `20` |
| `learning_criteria` | `AB >= 0.65`, `CD >= 0.60`, `EF >= 0.50` |
| `max_learning_blocks` | `6` |
| `transfer_conditions` | 15 pairings: `AB`, `AC`, `AD`, `AE`, `AF`, `BC`, `BD`, `BE`, `BF`, `CD`, `CE`, `CF`, `DE`, `DF`, `EF` |
| `transfer_trials_total` | `150` |
| `transfer_trials_per_pair` | `10` |
| `response_key_left` / `response_key_right` | `a` / `l` |
| `response_key_labels.left` / `response_key_labels.right` | `A` / `L` |
| `left_right_balance_policy` | `exact_within_block` |
| `symbol_role_shuffle_policy` | `random_per_subject` |
| `no_response_policy` | `timeout_counts_as_incorrect_on_learning` |
| `correct_score_delta` / `incorrect_score_delta` | `1` / `0` |

## 4. Methods (for academic publication)

Probabilistic stimulus selection is a classic reinforcement-learning paradigm used to measure reward sensitivity, choice bias, and transfer from learned feedback contingencies. The canonical structure contains three acquisition pairs with progressively weaker reward contingencies and a transfer test that presents all pairwise combinations without feedback.

This implementation preserves that structure while using six kana text stimuli and Chinese participant instructions. The learning phase uses probabilistic feedback, exact within-block left/right balance, and criterion-driven repetition. The transfer phase keeps the same symbols but removes feedback, allowing the analysis of learned preferences rather than immediate reinforcement.
