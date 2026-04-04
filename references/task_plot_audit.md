# Task Plot Audit

- generated_at: 2026-04-04T10:30:51.4006617+08:00
- mode: existing
- task_path: E:\Taskbeacon\T000040-probabilistic-stimulus-selection

## 1. Inputs and provenance

- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\README.md
- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\config\config.yaml
- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | Block ready | A centered ready screen appears for `3.0 s` before each block. |
- | Choice screen | Two kana symbols appear left and right; the participant responds with the left or right key within `4.0 s`. |
- | Feedback, learning only | A probabilistic `正确` or `错误` screen appears for `1.0 s` based on the chosen role's reward probability. |
- | No-feedback transfer | Transfer trials skip feedback and go straight to the inter-trial interval. |
- | Inter-trial interval | A fixation `+` appears for `1.0 s` before the next trial. |

## 3. Evidence extracted from config/source

- train_ab: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- train_ab: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- train_ab: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- train_cd: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- train_cd: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- train_cd: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- train_ef: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- train_ef: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- train_ef: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ab: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ab: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ab: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ac: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ac: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ac: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ad: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ad: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ad: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ae: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ae: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ae: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_af: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_af: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_af: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_bc: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_bc: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_bc: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_bd: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_bd: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_bd: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_be: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_be: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_be: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_bf: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_bf: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_bf: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_cd: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_cd: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_cd: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ce: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ce: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ce: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_cf: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_cf: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_cf: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_de: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_de: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_de: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_df: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_df: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_df: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'
- test_ef: phase=choice phase, deadline_expr=response_timeout, response_expr=response_timeout, stim_expr=_unit_stim_id(left_symbol_id, right_symbol_id)
- test_ef: phase=feedback phase, deadline_expr=feedback_duration, response_expr=n/a, stim_expr=feedback_stim_id
- test_ef: phase=iti phase, deadline_expr=iti_duration, response_expr=n/a, stim_expr='iti_fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 1
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.018, right=0.032, blank=0.123
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0177, 'right_ratio': 0.032, 'blank_ratio': 0.1235}

## 7. Output files and checksums

- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\references\task_plot_spec.yaml: sha256=a373cb5f8ce30f082096193eebc1eabd225fcd98f44df1d91acac9ce431704a2
- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\references\task_plot_spec.json: sha256=ab23131e39a9a663cb2e6e5f307a3fca6de999292aeb4a158fbde42b28cd817d
- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\references\task_plot_source_excerpt.md: sha256=50ab77e24bbf0ce1a7b59a5aa570eb9416e194155479e6f291495e003a8389f3
- E:\Taskbeacon\T000040-probabilistic-stimulus-selection\task_flow.png: sha256=db8628bb73be0056d3462b8abd61362dd105283766fe0ebbb4c8e45a882812627

## 8. Inferred/uncertain items

- train_ab:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- train_ab:choice phase:stimulus unresolved, used textual fallback
- train_ab:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- train_ab:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- train_cd:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- train_cd:choice phase:stimulus unresolved, used textual fallback
- train_cd:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- train_cd:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- train_ef:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- train_ef:choice phase:stimulus unresolved, used textual fallback
- train_ef:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- train_ef:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ab:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ab:choice phase:stimulus unresolved, used textual fallback
- test_ab:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ab:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ac:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ac:choice phase:stimulus unresolved, used textual fallback
- test_ac:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ac:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ad:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ad:choice phase:stimulus unresolved, used textual fallback
- test_ad:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ad:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ae:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ae:choice phase:stimulus unresolved, used textual fallback
- test_ae:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ae:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_af:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_af:choice phase:stimulus unresolved, used textual fallback
- test_af:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_af:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_bc:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_bc:choice phase:stimulus unresolved, used textual fallback
- test_bc:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_bc:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_bd:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_bd:choice phase:stimulus unresolved, used textual fallback
- test_bd:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_bd:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_be:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_be:choice phase:stimulus unresolved, used textual fallback
- test_be:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_be:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_bf:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_bf:choice phase:stimulus unresolved, used textual fallback
- test_bf:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_bf:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_cd:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_cd:choice phase:stimulus unresolved, used textual fallback
- test_cd:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_cd:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ce:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ce:choice phase:stimulus unresolved, used textual fallback
- test_ce:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ce:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_cf:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_cf:choice phase:stimulus unresolved, used textual fallback
- test_cf:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_cf:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_de:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_de:choice phase:stimulus unresolved, used textual fallback
- test_de:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_de:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_df:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_df:choice phase:stimulus unresolved, used textual fallback
- test_df:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_df:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- test_ef:choice phase:heuristic numeric parse from 'float(_get_setting(settings, 'response_timeout', default=4.0))'
- test_ef:choice phase:stimulus unresolved, used textual fallback
- test_ef:feedback phase:heuristic numeric parse from 'float(_get_setting(settings, 'feedback_duration', default=1.0))'
- test_ef:iti phase:heuristic numeric parse from 'float(_get_setting(settings, 'iti_duration', default=1.0))'
- collapsed equivalent condition logic into representative timeline: train_ab, train_cd, train_ef, test_ab, test_ac, test_ad, test_ae, test_af, test_bc, test_bd, test_be, test_bf, test_cd, test_ce, test_cf, test_de, test_df, test_ef
- unparsed if-tests defaulted to condition-agnostic applicability: correct_role is None; block_kind == 'learning'; learning_phase; learning_phase; correct_role is not None; not left_symbol_id; not right_symbol_id; selected_role is not None
- manual layout fix applied after render: shortened `display_condition_note` and set `meta.task_id` to `T000040` to keep the condition label column readable
