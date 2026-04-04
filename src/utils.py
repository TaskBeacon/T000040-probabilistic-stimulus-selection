from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
import math
import random
from typing import Any, Mapping, Sequence


ROLE_ORDER = ("A", "B", "C", "D", "E", "F")
LEARNING_PAIR_ORDER = ("train_ab", "train_cd", "train_ef")
TRANSFER_PAIR_ORDER = tuple(f"test_{left.lower()}{right.lower()}" for left, right in combinations(ROLE_ORDER, 2))
PAIR_ROLE_MAP: dict[str, tuple[str, str]] = {
    "train_ab": ("A", "B"),
    "train_cd": ("C", "D"),
    "train_ef": ("E", "F"),
}
PAIR_ROLE_MAP.update({pair_id: (left, right) for pair_id, (left, right) in zip(TRANSFER_PAIR_ORDER, combinations(ROLE_ORDER, 2))})

DEFAULT_LEARNING_PROBABILITIES: dict[str, dict[str, float]] = {
    "train_ab": {"A": 0.80, "B": 0.20},
    "train_cd": {"C": 0.70, "D": 0.30},
    "train_ef": {"E": 0.60, "F": 0.40},
}

DEFAULT_LEARNING_CRITERIA: dict[str, float] = {
    "train_ab": 0.65,
    "train_cd": 0.60,
    "train_ef": 0.50,
}

DEFAULT_SYMBOL_IDS = ("kana_1", "kana_2", "kana_3", "kana_4", "kana_5", "kana_6")


@dataclass(frozen=True)
class RoleAssignment:
    subject_id: int
    seed: int
    role_to_symbol_id: dict[str, str]
    symbol_id_to_role: dict[str, str]
    symbol_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "seed": self.seed,
            "role_to_symbol_id": dict(self.role_to_symbol_id),
            "symbol_id_to_role": dict(self.symbol_id_to_role),
            "symbol_ids": list(self.symbol_ids),
        }


def coerce_subject_id(value: Any, fallback: int = 101) -> int:
    digits = "".join(ch for ch in str(value) if ch.isdigit())
    if not digits:
        return int(fallback)
    return int(digits)


def parse_pair_roles(pair_id: Any) -> tuple[str, str]:
    token = str(pair_id or "").strip().lower()
    if not token:
        raise ValueError("pair_id is empty")
    suffix = token.split("_")[-1]
    if len(suffix) != 2:
        raise ValueError(f"pair_id {pair_id!r} does not end with a two-role token")
    left, right = suffix[0].upper(), suffix[1].upper()
    if left not in ROLE_ORDER or right not in ROLE_ORDER:
        raise ValueError(f"Unsupported pair_id roles in {pair_id!r}")
    return left, right


def correct_role_for_pair(pair_id: Any) -> str:
    left, _ = parse_pair_roles(pair_id)
    return left


def build_role_assignment(
    *,
    subject_id: int,
    seed_base: int,
    symbol_ids: Sequence[str] = DEFAULT_SYMBOL_IDS,
    policy: str = "random_per_subject",
) -> RoleAssignment:
    symbols = tuple(str(symbol) for symbol in symbol_ids)
    if len(symbols) != len(ROLE_ORDER):
        raise ValueError(f"Expected {len(ROLE_ORDER)} symbol ids, got {len(symbols)}")

    shuffled = list(symbols)
    normalized_policy = str(policy or "").strip().lower()
    if normalized_policy == "random_per_subject":
        rng = random.Random(int(seed_base) * 1009 + int(subject_id) * 37)
        rng.shuffle(shuffled)

    role_to_symbol_id = {role: symbol for role, symbol in zip(ROLE_ORDER, shuffled)}
    symbol_id_to_role = {symbol: role for role, symbol in role_to_symbol_id.items()}
    return RoleAssignment(
        subject_id=int(subject_id),
        seed=int(seed_base),
        role_to_symbol_id=role_to_symbol_id,
        symbol_id_to_role=symbol_id_to_role,
        symbol_ids=symbols,
    )


def resolve_block_seed(settings: Any, block_idx: int) -> int:
    seeds = list(getattr(settings, "block_seed", []) or [])
    if 0 <= int(block_idx) < len(seeds):
        candidate = seeds[int(block_idx)]
        if candidate is not None and str(candidate).strip() != "":
            return int(candidate)
    base = int(getattr(settings, "overall_seed", 0) or 0)
    return base + int(block_idx) * 10007


def _pair_trials_for_block(
    *,
    block_idx: int,
    block_kind: str,
    block_seed: int,
    pair_order: Sequence[str],
    trials_per_pair: int,
    role_assignment: RoleAssignment,
    learning_probabilities: Mapping[str, Mapping[str, float]] | None = None,
    left_right_balance_policy: str = "exact_within_block",
) -> list[dict[str, Any]]:
    rng = random.Random(int(block_seed) * 7919 + int(block_idx) * 104729)
    trials: list[dict[str, Any]] = []

    if int(trials_per_pair) <= 0:
        return trials

    exact_balance = str(left_right_balance_policy or "").strip().lower() == "exact_within_block"
    for pair_index, pair_id in enumerate(pair_order):
        pair_id = str(pair_id)
        canonical_left, canonical_right = parse_pair_roles(pair_id)
        if exact_balance and int(trials_per_pair) % 2 != 0:
            raise ValueError(
                f"{pair_id} requires an even number of trials when left/right balance is exact."
            )

        orientations = [False] * max(0, int(trials_per_pair) // 2)
        orientations += [True] * max(0, int(trials_per_pair) - len(orientations))
        if exact_balance:
            orientations = [False] * (int(trials_per_pair) // 2) + [True] * (int(trials_per_pair) // 2)
        rng.shuffle(orientations)

        for pair_trial_idx, swapped in enumerate(orientations, start=1):
            left_role = canonical_right if swapped else canonical_left
            right_role = canonical_left if swapped else canonical_right
            left_symbol_id = role_assignment.role_to_symbol_id[left_role]
            right_symbol_id = role_assignment.role_to_symbol_id[right_role]
            left_prob = None
            right_prob = None
            if learning_probabilities is not None:
                pair_probs = learning_probabilities.get(pair_id, {})
                left_prob = pair_probs.get(left_role)
                right_prob = pair_probs.get(right_role)

            trials.append(
                {
                    "block_idx": int(block_idx),
                    "block_num": int(block_idx) + 1,
                    "block_kind": str(block_kind),
                    "trial_idx": 0,
                    "pair_trial_idx": int(pair_trial_idx),
                    "pair_index": int(pair_index),
                    "pair_id": pair_id,
                    "condition": pair_id,
                    "pair_roles": [canonical_left, canonical_right],
                    "left_role": left_role,
                    "right_role": right_role,
                    "correct_role": canonical_left if str(block_kind).lower() == "learning" else None,
                    "left_symbol_id": left_symbol_id,
                    "right_symbol_id": right_symbol_id,
                    "left_reward_probability": left_prob,
                    "right_reward_probability": right_prob,
                    "feedback_enabled": str(block_kind).lower() == "learning",
                    "orientation": "swapped" if swapped else "canonical",
                    "role_assignment_seed": int(block_seed),
                }
            )

    rng.shuffle(trials)
    for trial_idx, trial in enumerate(trials, start=1):
        trial["trial_idx"] = int(trial_idx)
        trial["trial_order"] = int(trial_idx)
    return trials


def build_learning_block_schedule(
    *,
    block_idx: int,
    block_seed: int,
    pair_order: Sequence[str] = LEARNING_PAIR_ORDER,
    trials_per_pair: int = 20,
    role_assignment: RoleAssignment,
    learning_probabilities: Mapping[str, Mapping[str, float]] | None = None,
    left_right_balance_policy: str = "exact_within_block",
) -> list[dict[str, Any]]:
    return _pair_trials_for_block(
        block_idx=block_idx,
        block_kind="learning",
        block_seed=block_seed,
        pair_order=pair_order,
        trials_per_pair=trials_per_pair,
        role_assignment=role_assignment,
        learning_probabilities=learning_probabilities or DEFAULT_LEARNING_PROBABILITIES,
        left_right_balance_policy=left_right_balance_policy,
    )


def build_transfer_block_schedule(
    *,
    block_idx: int,
    block_seed: int,
    pair_order: Sequence[str] = TRANSFER_PAIR_ORDER,
    trials_per_pair: int = 10,
    role_assignment: RoleAssignment,
    left_right_balance_policy: str = "exact_within_block",
) -> list[dict[str, Any]]:
    return _pair_trials_for_block(
        block_idx=block_idx,
        block_kind="transfer",
        block_seed=block_seed,
        pair_order=pair_order,
        trials_per_pair=trials_per_pair,
        role_assignment=role_assignment,
        learning_probabilities=None,
        left_right_balance_policy=left_right_balance_policy,
    )


def sample_learning_outcome(
    pair_id: Any,
    chosen_role: Any,
    learning_probabilities: Mapping[str, Mapping[str, float]] | None,
    rng: random.Random,
) -> tuple[bool, float]:
    probs = learning_probabilities or DEFAULT_LEARNING_PROBABILITIES
    pair_key = str(pair_id)
    role_key = str(chosen_role).upper()
    pair_probs = probs.get(pair_key, {})
    probability = float(pair_probs.get(role_key, 0.5))
    return rng.random() < probability, probability


def format_phase_label(block_kind: str, block_num: int | None = None) -> str:
    kind = str(block_kind or "").strip().lower()
    if kind == "learning":
        if block_num is None:
            return "学习阶段"
        return f"学习阶段（第{int(block_num)}轮）"
    if kind == "transfer":
        return "转移测验"
    return str(block_kind)


def evaluate_learning_block(
    trials: Sequence[Mapping[str, Any]],
    criteria: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    thresholds = dict(criteria or DEFAULT_LEARNING_CRITERIA)
    pair_accuracy: dict[str, float] = {}
    pair_counts: dict[str, dict[str, int]] = {}
    pair_passed: dict[str, bool] = {}
    total = 0
    correct_total = 0

    for pair_id, threshold in thresholds.items():
        rows = [row for row in trials if str(row.get("pair_id", row.get("condition", ""))) == pair_id]
        n_rows = len(rows)
        n_correct = sum(1 for row in rows if bool(row.get("response_correct", False)))
        acc = (n_correct / n_rows) if n_rows else 0.0
        pair_accuracy[pair_id] = acc
        pair_counts[pair_id] = {"n": n_rows, "correct": n_correct, "threshold": float(threshold)}
        pair_passed[pair_id] = acc >= float(threshold)
        total += n_rows
        correct_total += n_correct

    mean_rt_values = [
        float(row["response_rt"])
        for row in trials
        if isinstance(row.get("response_rt"), (int, float))
    ]
    mean_rt = (sum(mean_rt_values) / len(mean_rt_values)) if mean_rt_values else None

    return {
        "pair_accuracy": pair_accuracy,
        "pair_counts": pair_counts,
        "pair_passed": pair_passed,
        "overall_accuracy": (correct_total / total) if total else 0.0,
        "total_trials": total,
        "total_correct": correct_total,
        "mean_rt": mean_rt,
        "passed": all(pair_passed.values()) if pair_passed else False,
        "thresholds": thresholds,
    }


def summarize_transfer_block(trials: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    role_counts = Counter()
    pair_counts: dict[str, Counter[str]] = {}
    rts: list[float] = []
    timeouts = 0

    for row in trials:
        chosen_role = str(row.get("chosen_role") or row.get("selected_role") or "").upper()
        if chosen_role in ROLE_ORDER:
            role_counts[chosen_role] += 1

        pair_id = str(row.get("pair_id") or row.get("condition") or "")
        if pair_id not in pair_counts:
            pair_counts[pair_id] = Counter()
        if chosen_role:
            pair_counts[pair_id][chosen_role] += 1

        if bool(row.get("choice_timeout", False)):
            timeouts += 1

        rt = row.get("response_rt")
        if isinstance(rt, (int, float)):
            rts.append(float(rt))

    total = len(trials)
    role_choice_rate = {
        role: (role_counts[role] / total if total else 0.0)
        for role in ROLE_ORDER
    }
    pair_choice_rate = {
        pair_id: {role: count / sum(counter.values()) if sum(counter.values()) else 0.0 for role, count in counter.items()}
        for pair_id, counter in pair_counts.items()
    }

    return {
        "total_trials": total,
        "timeouts": timeouts,
        "role_counts": dict(role_counts),
        "role_choice_rate": role_choice_rate,
        "pair_choice_rate": pair_choice_rate,
        "mean_rt": (sum(rts) / len(rts)) if rts else None,
    }


def left_right_pair_summary(trials: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    left_count = sum(1 for row in trials if str(row.get("response_side") or "").lower() == "left")
    right_count = sum(1 for row in trials if str(row.get("response_side") or "").lower() == "right")
    total = left_count + right_count
    return {
        "left_count": left_count,
        "right_count": right_count,
        "left_rate": (left_count / total) if total else 0.0,
        "right_rate": (right_count / total) if total else 0.0,
    }


def is_learning_pair(pair_id: Any) -> bool:
    return str(pair_id).strip().lower().startswith("train_")


def is_transfer_pair(pair_id: Any) -> bool:
    return str(pair_id).strip().lower().startswith("test_")


__all__ = [
    "DEFAULT_LEARNING_CRITERIA",
    "DEFAULT_LEARNING_PROBABILITIES",
    "DEFAULT_SYMBOL_IDS",
    "LEARNING_PAIR_ORDER",
    "PAIR_ROLE_MAP",
    "ROLE_ORDER",
    "RoleAssignment",
    "TRANSFER_PAIR_ORDER",
    "build_learning_block_schedule",
    "build_role_assignment",
    "build_transfer_block_schedule",
    "coerce_subject_id",
    "correct_role_for_pair",
    "evaluate_learning_block",
    "format_phase_label",
    "is_learning_pair",
    "is_transfer_pair",
    "left_right_pair_summary",
    "parse_pair_roles",
    "resolve_block_seed",
    "sample_learning_outcome",
    "summarize_transfer_block",
]
