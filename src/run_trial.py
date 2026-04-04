from __future__ import annotations

from functools import partial
import random
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import (
    correct_role_for_pair,
    is_learning_pair,
    parse_pair_roles,
    sample_learning_outcome,
)


def _get_setting(settings: Any, *names: str, default: Any = None) -> Any:
    for name in names:
        if hasattr(settings, name):
            value = getattr(settings, name)
            if value is not None:
                return value
    return default


def _condition_dict(condition: Any) -> dict[str, Any]:
    if isinstance(condition, dict):
        data = dict(condition)
    else:
        pair_id = str(condition or "").strip()
        data = {"condition": pair_id, "pair_id": pair_id}

    pair_id = str(data.get("pair_id") or data.get("condition") or "").strip()
    if not pair_id:
        raise ValueError("trial condition is missing pair_id")

    if "condition" not in data:
        data["condition"] = pair_id
    data["pair_id"] = pair_id
    data.setdefault("block_kind", "learning" if is_learning_pair(pair_id) else "transfer")
    data.setdefault("pair_roles", list(parse_pair_roles(pair_id)))
    return data


def _unit_stim_id(left_symbol_id: str, right_symbol_id: str) -> str:
    return f"{left_symbol_id}+{right_symbol_id}"


def _response_side(response_key: str | None, left_key: str, right_key: str) -> str | None:
    if response_key == left_key:
        return "left"
    if response_key == right_key:
        return "right"
    return None


def _choice_unit(
    *,
    win,
    kb,
    trigger_runtime,
    stim_bank,
    unit_label: str,
    left_symbol_id: str,
    right_symbol_id: str,
    left_x: float,
    right_x: float,
):
    unit = StimUnit(unit_label, win, kb, runtime=trigger_runtime)
    unit.add_stim(
        stim_bank.rebuild(left_symbol_id, pos=(left_x, 0)),
        stim_bank.rebuild(right_symbol_id, pos=(right_x, 0)),
    )
    return unit


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
    score_total: int = 0,
):
    """Run one probabilistic stimulus selection trial."""

    trial_id = int(next_trial_id())
    trial = _condition_dict(condition)
    block_kind = str(trial.get("block_kind") or ("learning" if is_learning_pair(trial["pair_id"]) else "transfer")).strip().lower()
    pair_id = str(trial["pair_id"])
    pair_left_role, pair_right_role = parse_pair_roles(pair_id)
    left_role = str(trial.get("left_role") or pair_left_role).upper()
    right_role = str(trial.get("right_role") or pair_right_role).upper()
    correct_role = trial.get("correct_role")
    if correct_role is None and block_kind == "learning":
        correct_role = correct_role_for_pair(pair_id)
    correct_role = str(correct_role).upper() if correct_role is not None else None

    left_symbol_id = str(trial.get("left_symbol_id") or "")
    right_symbol_id = str(trial.get("right_symbol_id") or "")
    if not left_symbol_id or not right_symbol_id:
        raise ValueError(f"Trial condition {pair_id!r} is missing symbol ids.")

    block_idx_value = int(block_idx if block_idx is not None else trial.get("block_idx", 0) or 0)
    block_num_value = int(trial.get("block_num", block_idx_value + 1) or (block_idx_value + 1))
    pair_trial_idx = int(trial.get("pair_trial_idx", 0) or 0)
    trial_idx = int(trial.get("trial_idx", trial_id) or trial_id)
    block_id_value = str(block_id if block_id is not None else trial.get("block_id", f"{block_kind}_block_{block_num_value:02d}"))

    left_key = str(_get_setting(settings, "response_key_left", default="a")).strip().lower()
    right_key = str(_get_setting(settings, "response_key_right", default="l")).strip().lower()

    left_x = float(_get_setting(settings, "symbol_x_left_px", default=-220))
    right_x = float(_get_setting(settings, "symbol_x_right_px", default=220))
    response_timeout = float(_get_setting(settings, "response_timeout", default=4.0))
    feedback_duration = float(_get_setting(settings, "feedback_duration", default=1.0))
    iti_duration = float(_get_setting(settings, "iti_duration", default=1.0))
    correct_score_delta = int(_get_setting(settings, "correct_score_delta", default=1))
    incorrect_score_delta = int(_get_setting(settings, "incorrect_score_delta", default=0))
    learning_probabilities = dict(_get_setting(settings, "learning_probabilities", default={}) or {})
    response_triggers = {
        left_key: settings.triggers.get("left_response"),
        right_key: settings.triggers.get("right_response"),
    }

    trial_seed = int(trial.get("role_assignment_seed", 0) or 0) * 1009 + block_idx_value * 97 + trial_idx * 53
    trial_rng = random.Random(trial_seed)

    learning_phase = block_kind == "learning"
    choice_phase = f"{block_kind}_choice"
    feedback_phase = f"{block_kind}_feedback"
    iti_phase = f"{block_kind}_iti"
    condition_id = pair_id

    trial_data: dict[str, Any] = {
        "trial_id": trial_id,
        "block_id": block_id_value,
        "block_idx": block_idx_value,
        "block_num": block_num_value,
        "block_kind": block_kind,
        "phase": block_kind,
        "phase_kind": block_kind,
        "condition": pair_id,
        "condition_id": condition_id,
        "pair_id": pair_id,
        "pair_roles": list(trial.get("pair_roles") or [pair_left_role, pair_right_role]),
        "left_role": left_role,
        "right_role": right_role,
        "correct_role": correct_role,
        "left_symbol_id": left_symbol_id,
        "right_symbol_id": right_symbol_id,
        "pair_trial_idx": pair_trial_idx,
        "trial_idx": trial_idx,
        "feedback_enabled": bool(trial.get("feedback_enabled", learning_phase)),
        "score_total_before": int(score_total),
        "score_total": int(score_total),
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    # Choice window.
    choice_unit = _choice_unit(
        win=win,
        kb=kb,
        trigger_runtime=trigger_runtime,
        stim_bank=stim_bank,
        unit_label=choice_phase,
        left_symbol_id=left_symbol_id,
        right_symbol_id=right_symbol_id,
        left_x=left_x,
        right_x=right_x,
    )
    correct_key = None
    if learning_phase and correct_role is not None:
        correct_key = left_key if left_role == correct_role else right_key

    set_trial_context(
        choice_unit,
        trial_id=trial_id,
        phase=choice_phase,
        deadline_s=response_timeout,
        valid_keys=[left_key, right_key],
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors={
            "stage": choice_phase,
            "block_kind": block_kind,
            "block_idx": block_idx_value,
            "block_num": block_num_value,
            "trial_idx": trial_idx,
            "pair_id": pair_id,
            "left_role": left_role,
            "right_role": right_role,
            "correct_role": correct_role,
            "feedback_enabled": learning_phase,
            "left_symbol_id": left_symbol_id,
            "right_symbol_id": right_symbol_id,
            "response_timeout": response_timeout,
        },
        stim_id=_unit_stim_id(left_symbol_id, right_symbol_id),
    )
    choice_unit.capture_response(
        keys=[left_key, right_key],
        correct_keys=[correct_key] if correct_key is not None else [],
        duration=response_timeout,
        onset_trigger=settings.triggers.get("trial_onset"),
        response_trigger=response_triggers,
        timeout_trigger=settings.triggers.get("timeout"),
        terminate_on_response=True,
    ).to_dict(trial_data)

    response_key = choice_unit.get_state("response", None)
    response_key = str(response_key).strip().lower() if response_key is not None else None
    response_rt = choice_unit.get_state("rt", None)
    response_rt_value = float(response_rt) if isinstance(response_rt, (int, float)) else None
    response_side = _response_side(response_key, left_key, right_key)
    selected_role = left_role if response_side == "left" else right_role if response_side == "right" else None
    choice_timeout = response_side is None
    response_correct = bool(choice_unit.get_state("hit", False)) if learning_phase else None

    trial_data.update(
        {
            "response_key": response_key or "",
            "response_side": response_side,
            "selected_role": selected_role,
            "chosen_role": selected_role,
            "choice_timeout": choice_timeout,
            "choice_forced": choice_timeout,
            "response_rt": response_rt_value,
            "choice_rt": response_rt_value,
            "response_correct": response_correct,
            "choice_correct": response_correct,
        }
    )

    feedback_win = None
    reward_probability = None
    score_delta = 0
    feedback_stim_id = None
    score_total_after = int(score_total)

    if learning_phase:
        if selected_role is not None:
            feedback_win, reward_probability = sample_learning_outcome(
                pair_id,
                selected_role,
                learning_probabilities,
                trial_rng,
            )
        else:
            feedback_win = False
            reward_probability = 0.0

        score_delta = correct_score_delta if feedback_win else incorrect_score_delta
        score_total_after = int(score_total) + int(score_delta)
        feedback_stim_id = "feedback_correct" if feedback_win else "feedback_incorrect"
        feedback_unit = make_unit(feedback_phase).add_stim(stim_bank.get(feedback_stim_id))
        set_trial_context(
            feedback_unit,
            trial_id=trial_id,
            phase=feedback_phase,
            deadline_s=feedback_duration,
            valid_keys=[],
            block_id=block_id_value,
            condition_id=condition_id,
            task_factors={
                "stage": feedback_phase,
                "block_kind": block_kind,
                "block_idx": block_idx_value,
                "block_num": block_num_value,
                "trial_idx": trial_idx,
                "pair_id": pair_id,
                "selected_role": selected_role,
                "correct_role": correct_role,
                "choice_correct": response_correct,
                "feedback_win": feedback_win,
                "reward_probability": reward_probability,
                "score_delta": score_delta,
                "score_total": score_total_after,
            },
            stim_id=feedback_stim_id,
        )
        feedback_unit.show(duration=feedback_duration, onset_trigger=settings.triggers.get("feedback_onset")).to_dict(trial_data)
    else:
        trial_data.update(
            {
                "feedback_win": None,
                "reward_probability": None,
                "score_delta": 0,
                "feedback_stim_id": None,
            }
        )

    trial_data.update(
        {
            "feedback_win": feedback_win,
            "reward_probability": reward_probability,
            "score_delta": int(score_delta),
            "feedback_stim_id": feedback_stim_id,
            "score_total": int(score_total_after),
        }
    )

    iti = make_unit(iti_phase).add_stim(stim_bank.get("iti_fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase=iti_phase,
        deadline_s=iti_duration,
        valid_keys=[],
        block_id=block_id_value,
        condition_id=condition_id,
        task_factors={
            "stage": iti_phase,
            "block_kind": block_kind,
            "block_idx": block_idx_value,
            "block_num": block_num_value,
            "trial_idx": trial_idx,
            "pair_id": pair_id,
            "score_total": score_total_after,
        },
        stim_id="iti_fixation",
    )
    iti.show(duration=iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    return trial_data


__all__ = ["run_trial"]
