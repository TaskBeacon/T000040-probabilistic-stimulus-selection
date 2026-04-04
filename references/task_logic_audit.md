# Task Logic Audit

## 1. Paradigm Intent

- Task: Probabilistic Stimulus Selection
- Primary construct: probabilistic reinforcement learning, positive-vs-negative feedback sensitivity, and transfer choice bias
- Manipulated factors:
  - training pair contingencies: AB 80/20, CD 70/30, EF 60/40
  - learning versus transfer phase
  - pair order within each block
  - left/right placement of the role-bearing symbol within each pair
- Dependent measures:
  - training accuracy by pair
  - learning-block criterion attainment
  - transfer choice proportions, especially A-choice and B-avoidance
  - choice latency
  - timeout / omission rate
- Key citations:
  - `W2014979870` - classic open-access PSS structure and transfer test
  - `W2125735154` - open-access task implementation with 60-trial learning blocks, 65/60/50 criteria, 150-trial test default, and left/right balance
  - `W2170143116` - open-access PSS variant with explicit 4 s stimulus display and no-feedback performance phase
  - `W2419503723` - open-access supporting paper that includes the PSS transfer phase inside a broader reinforcement-learning battery

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: learning blocks repeat until criteria are met; one transfer block follows. Use `max_learning_blocks=6` as a safety cap for automation.
- Trials per block: learning blocks run 60 trials each; transfer runs 150 trials by default.
- Randomization/counterbalancing:
  - six Hiragana symbols are randomly assigned to the roles A-F at runtime
  - within each block, each pair is balanced 50/50 for left/right placement
  - trial order is shuffled within the block while preserving the exact pair counts
- Condition generation method:
  - custom generator
  - built-in `BlockUnit.generate_conditions(...)` is not sufficient because the task needs exact pair counts, left/right balance, and criterion-driven repetition
  - generated condition data shape: list of dictionaries with `phase`, `pair_id`, `left_role`, `right_role`, `correct_role`, `feedback_prob`, `feedback_enabled`, `block_idx`, and `trial_idx`
- Runtime-generated trial values:
  - role-to-symbol assignment is sampled deterministically from the subject seed
  - per-trial left/right placement is sampled with exact within-block balance
  - learning feedback is sampled from the role-specific win probability
  - block repetition depends on whether the learning criteria are met
  - transfer trials are generated without feedback but retain the same pair metadata for analysis

### Trial State Machine

List each state in order with entry/exit conditions:

1. State name: `instructions`
   - Onset trigger: none
   - Stimuli shown: `instruction_text`
   - Valid keys: `space`
   - Timeout behavior: wait until participant continues
   - Next state: `learning_ready`
2. State name: `learning_ready`
   - Onset trigger: `block_onset`
   - Stimuli shown: `block_ready`
   - Valid keys: none
   - Timeout behavior: fixed 3000 ms
   - Next state: `learning_choice`
3. State name: `learning_choice`
   - Onset trigger: `trial_onset`
   - Stimuli shown: two Hiragana symbols, one on the left and one on the right
   - Valid keys: left key and right key
   - Timeout behavior: response window capped at 4000 ms
   - Next state: `learning_feedback`
4. State name: `learning_feedback`
   - Onset trigger: `feedback_onset`
   - Stimuli shown: `feedback_correct` or `feedback_incorrect`
   - Valid keys: none
   - Timeout behavior: fixed 1000 ms
   - Next state: `learning_iti`
5. State name: `learning_iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `iti_fixation`
   - Valid keys: none
   - Timeout behavior: fixed 1000 ms
   - Next state: next learning trial or `learning_block_check`
6. State name: `learning_block_check`
   - Onset trigger: none
   - Stimuli shown: none
   - Valid keys: none
   - Timeout behavior: instant block criterion evaluation
   - Next state: another learning block if criteria are not met, otherwise `transfer_ready`
7. State name: `transfer_ready`
   - Onset trigger: `block_onset`
   - Stimuli shown: `block_ready`
   - Valid keys: none
   - Timeout behavior: fixed 3000 ms
   - Next state: `transfer_choice`
8. State name: `transfer_choice`
   - Onset trigger: `trial_onset`
   - Stimuli shown: two Hiragana symbols, one on the left and one on the right
   - Valid keys: left key and right key
   - Timeout behavior: response window capped at 4000 ms
   - Next state: `transfer_iti`
9. State name: `transfer_iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `iti_fixation`
   - Valid keys: none
   - Timeout behavior: fixed 1000 ms
   - Next state: next transfer trial
10. State name: `good_bye`
    - Onset trigger: none
    - Stimuli shown: `good_bye`
    - Valid keys: `space`
    - Timeout behavior: wait until participant continues
    - Next state: experiment end

## 3. Condition Semantics

For each condition token in `task.conditions`:

- Condition ID: `train_ab`
  - Participant-facing meaning: a learning trial with the role-A and role-B symbols, where A is correct 80% of the time and B is correct 20% of the time.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: learning feedback is probabilistic and only the role with the higher win probability counts as correct.
- Condition ID: `train_cd`
  - Participant-facing meaning: a learning trial with the role-C and role-D symbols, where C is correct 70% of the time and D is correct 30% of the time.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: learning feedback is probabilistic and only the role with the higher win probability counts as correct.
- Condition ID: `train_ef`
  - Participant-facing meaning: a learning trial with the role-E and role-F symbols, where E is correct 60% of the time and F is correct 40% of the time.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: learning feedback is probabilistic and only the role with the higher win probability counts as correct.
- Condition ID: `test_ab`
  - Participant-facing meaning: a transfer trial with the role-A and role-B symbols, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_ac`
  - Participant-facing meaning: transfer pair A versus C, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_ad`
  - Participant-facing meaning: transfer pair A versus D, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_ae`
  - Participant-facing meaning: transfer pair A versus E, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_af`
  - Participant-facing meaning: transfer pair A versus F, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_bc`
  - Participant-facing meaning: transfer pair B versus C, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_bd`
  - Participant-facing meaning: transfer pair B versus D, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_be`
  - Participant-facing meaning: transfer pair B versus E, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_bf`
  - Participant-facing meaning: transfer pair B versus F, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_cd`
  - Participant-facing meaning: transfer pair C versus D, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_ce`
  - Participant-facing meaning: transfer pair C versus E, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_cf`
  - Participant-facing meaning: transfer pair C versus F, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_de`
  - Participant-facing meaning: transfer pair D versus E, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_df`
  - Participant-facing meaning: transfer pair D versus F, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.
- Condition ID: `test_ef`
  - Participant-facing meaning: transfer pair E versus F, no feedback.
  - Concrete stimulus realization: two Hiragana symbols shown side-by-side with randomized left/right placement.
  - Outcome rules: choice is logged for transfer analysis; no feedback is shown.

Also document where participant-facing text/stimuli are defined:

- Participant-facing text source: config stimuli in `config/config.yaml`, especially `instruction_text`, `block_ready`, `feedback_correct`, `feedback_incorrect`, `iti_fixation`, and `good_bye`.
- Why this source is appropriate for auditability: the task wording stays localized in YAML, while the pair logic remains in code; this makes it easy to review or translate the participant text without touching the state machine.
- Localization strategy: Chinese instructions and feedback live in config, while the Hiragana symbol pool is rendered by a kana-capable font selected in config; changing language or symbol styling should not require edits to `src/run_trial.py`.

## 4. Response and Scoring Rules

- Response mapping: left key selects the left symbol; right key selects the right symbol.
- Response key source: config fields `task.response_key_left` and `task.response_key_right`.
- If code-defined, why config-driven mapping is not sufficient: config-driven mapping is sufficient; code only needs to resolve the pair-specific left/right placement.
- Missing-response policy: if no response is made before the response timeout, the trial is logged as a timeout and treated as non-winning on learning trials; on transfer trials it is excluded from preference metrics but still logged.
- Correctness logic: on learning trials, the role with the higher win probability is correct; on transfer trials there is no correctness score because feedback is withheld.
- Reward/penalty updates:
  - correct learning responses increment a hidden cumulative score by 1
  - incorrect or timed-out learning responses increment 0
  - no negative penalty is shown to participants
- Running metrics:
  - learning accuracy by pair and by block
  - block criterion attainment
  - transfer choice proportions, including A-choice and B-avoidance style indices
  - response latency
  - omission rate

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: instruction
  - Stimulus IDs shown together: `instruction_text`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): height 28-32, `wrapWidth` around 980-1000
  - Readability/overlap checks: single centered text block only
  - Rationale: Chinese instructions should be easy to read before the first choice trial
- Screen name: block ready
  - Stimulus IDs shown together: `block_ready`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): height 28-32, `wrapWidth` around 980
  - Readability/overlap checks: single centered text block only
  - Rationale: brief block transition screen keeps the phase structure visible
- Screen name: learning choice / transfer choice
  - Stimulus IDs shown together: left role symbol, right role symbol
  - Layout anchors (`pos`): left symbol around `(-220, 0)`, right symbol around `(220, 0)`
  - Size/spacing (`height`, width, wrap): symbol height around 180-200 px; no wrap
  - Readability/overlap checks: two large kana symbols remain separated on a 1280 x 720 window
  - Rationale: the pair must be easy to discriminate while keeping the left/right decision explicit
- Screen name: feedback
  - Stimulus IDs shown together: `feedback_correct` or `feedback_incorrect`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): height 36-40, `wrapWidth` around 980
  - Readability/overlap checks: one text block only
  - Rationale: feedback should be legible and unambiguous
- Screen name: ITI / fixation
  - Stimulus IDs shown together: `iti_fixation`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): single symbol, no wrap
  - Readability/overlap checks: neutral fixation prevents accidental overlap with the next pair
  - Rationale: a simple fixation anchor is enough between trials
- Screen name: goodbye
  - Stimulus IDs shown together: `good_bye`
  - Layout anchors (`pos`): centered
  - Size/spacing (`height`, width, wrap): height 28-32, `wrapWidth` around 980
  - Readability/overlap checks: single centered text block only
  - Rationale: exit screen should be calm and easy to dismiss

## 6. Trigger Plan

Map each phase/state to trigger code and semantics.

| Phase/State | Trigger | Semantics |
|---|---:|---|
| `instructions` | none | Instruction screen is shown before the task begins. |
| `exp_onset` | `1` | Experiment begins. |
| `block_onset` | `10` | A learning or transfer block begins. |
| `block_end` | `11` | A learning or transfer block ends. |
| `trial_onset` | `20` | A choice trial begins. |
| `response_onset` | `30` | Response window opens. |
| `left_response` | `31` | The left key was pressed. |
| `right_response` | `32` | The right key was pressed. |
| `timeout` | `33` | The response window expired without a choice. |
| `feedback_onset` | `40` | Learning feedback is shown. |
| `no_feedback_onset` | `41` | Transfer trial shows no feedback. |
| `iti_onset` | `50` | Inter-trial interval begins. |
| `exp_end` | `2` | Experiment closes after the goodbye screen. |

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: simple mode-aware single flow with explicit `human`, `qa`, and `sim` branches.
- `utils.py` used? yes
- If yes, exact purpose: phase-specific schedule generation, role randomization, criterion checks, and transfer-metric helpers.
- Custom controller used? yes
- If yes, why PsyFlow-native path is insufficient: the task needs exact pair counts, left/right balance, probabilistic feedback, and criterion-driven repetition before the transfer block.
- Legacy/backward-compatibility fallback logic required? no

## 8. Inference Log

List any inferred decisions not directly specified by references:

- Decision: the exact six Hiragana glyphs are centralized in config and randomized across the A-F roles.
  - Why inference was required: the papers and manual specify the symbol class, but not the literal glyph identities in accessible text.
  - Citation-supported rationale: the task logic depends on six Hiragana symbols with random role assignment, not on a fixed glyph identity.
- Decision: response timeout is set to 4000 ms.
  - Why inference was required: the open papers give the task structure and response-latency reporting but do not define a universal timeout for the non-scanner implementation.
  - Citation-supported rationale: the timing is consistent with the open-access Parkinson's disease variant that used a 4 s stimulus window and with the need to keep QA/simulation bounded.
- Decision: ITI is set to 1000 ms.
  - Why inference was required: the manual gives feedback duration and block timing but does not spell out an inter-trial gap in the excerpted parameters.
  - Citation-supported rationale: a 1 s ITI preserves the published short trial structure while keeping the block duration close to the software manual.
- Decision: `max_learning_blocks=6`.
  - Why inference was required: the literature says repeat until criteria are met, but a finite cap is needed for runtime safety and QA.
  - Citation-supported rationale: the cap is a framework safeguard and does not change the criterion rule itself.
- Decision: Chinese instruction copy and block/goodbye screens are localized framework text.
  - Why inference was required: the papers do not prescribe the exact participant-facing language.
  - Citation-supported rationale: the protocol specifies the task logic; language should remain editable in config.

## Contract Note

- Participant-facing labels/instructions/options should be config-defined whenever possible.
- `src/run_trial.py` should not hardcode participant-facing text that would require code edits for localization.
