from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


ROLE_SCORES = {
    "A": 0.80,
    "B": 0.20,
    "C": 0.70,
    "D": 0.30,
    "E": 0.60,
    "F": 0.40,
}


def _sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, float(value)))
    return 1.0 / (1.0 + math.exp(-value))


def _extract_phase(obs: Observation | dict[str, Any]) -> str:
    if isinstance(obs, dict):
        phase = obs.get("phase") or obs.get("stage") or ""
    else:
        phase = obs.phase or obs.task_factors.get("stage") or ""
    return str(phase).strip().lower()


def _extract_valid_keys(obs: Observation | dict[str, Any]) -> list[str]:
    if isinstance(obs, dict):
        return [str(key) for key in list(obs.get("valid_keys") or [])]
    return [str(key) for key in list(obs.valid_keys or [])]


def _extract_factors(obs: Observation | dict[str, Any]) -> dict[str, Any]:
    if isinstance(obs, dict):
        return dict(obs.get("task_factors") or {})
    return dict(obs.task_factors or {})


@dataclass
class TaskSamplerResponder:
    """Simple choice responder for the probabilistic stimulus selection task."""

    mode: str = "sampled"
    left_key: str = "a"
    right_key: str = "l"
    space_key: str = "space"
    evidence_strength: float = 2.0
    rt_mean_s: float = 0.42
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.15
    no_response_rate: float = 0.0
    role_scores: dict[str, float] = field(default_factory=lambda: dict(ROLE_SCORES))

    def __post_init__(self) -> None:
        self.mode = str(self.mode or "sampled").strip().lower()
        if self.mode not in {"scripted", "sampled", "sampler"}:
            self.mode = "sampled"
        if self.mode == "sampler":
            self.mode = "sampled"
        self.left_key = str(self.left_key or "a").strip().lower()
        self.right_key = str(self.right_key or "l").strip().lower()
        self.space_key = str(self.space_key or "space").strip().lower()
        self.evidence_strength = float(self.evidence_strength)
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self.no_response_rate = min(1.0, max(0.0, float(self.no_response_rate)))
        self.role_scores = {str(role).upper(): float(score) for role, score in dict(self.role_scores).items()}
        self._rng: Any = None
        self._session: SessionInfo | None = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._session = session
        self._rng = rng

    def end_session(self) -> None:
        self._session = None
        self._rng = None

    def on_feedback(self, fb: Feedback) -> None:
        # The task is fully driven by the current choice context, so the
        # feedback hook remains intentionally light-weight.
        return None

    def _random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return random.random()

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        if hasattr(rng, "gauss"):
            return float(rng.gauss(mean, sd))
        return float(random.gauss(mean, sd))

    def _sample_rt(self) -> float:
        rt = self._normal(self.rt_mean_s, self.rt_sd_s)
        return max(self.rt_min_s, rt)

    def _choose_space(self, valid_keys: list[str], phase: str) -> Action:
        key = self.space_key if self.space_key in valid_keys else (valid_keys[0] if valid_keys else None)
        return Action(key=key, rt_s=self._sample_rt(), meta={"source": "task_sampler", "phase": phase, "kind": "continue"})

    def _choose_choice(self, valid_keys: list[str], factors: dict[str, Any], phase: str) -> Action:
        left_role = str(factors.get("left_role") or factors.get("left_symbol_role") or "").upper()
        right_role = str(factors.get("right_role") or factors.get("right_symbol_role") or "").upper()
        left_score = float(self.role_scores.get(left_role, 0.5))
        right_score = float(self.role_scores.get(right_role, 0.5))

        if self.mode == "scripted":
            choose_left = left_score >= right_score
        else:
            p_left = _sigmoid(self.evidence_strength * (left_score - right_score))
            choose_left = self._random() < p_left

        if self._random() < self.no_response_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase, "kind": "timeout_bias"})

        key = self.left_key if choose_left else self.right_key
        if key not in valid_keys:
            key = valid_keys[0] if valid_keys else None
        chosen_role = left_role if choose_left else right_role
        chosen_side = "left" if choose_left else "right"
        p_left = _sigmoid(self.evidence_strength * (left_score - right_score))
        return Action(
            key=key,
            rt_s=self._sample_rt(),
            meta={
                "source": "task_sampler",
                "phase": phase,
                "kind": "choice",
                "left_role": left_role,
                "right_role": right_role,
                "chosen_role": chosen_role,
                "chosen_side": chosen_side,
                "left_score": left_score,
                "right_score": right_score,
                "p_left": p_left,
            },
        )

    def act(self, obs: Observation | dict[str, Any]) -> Action:
        valid_keys = _extract_valid_keys(obs)
        phase = _extract_phase(obs)
        factors = _extract_factors(obs)

        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase, "kind": "no_valid_keys"})

        continue_phases = {
            "instructions",
            "instruction_text",
            "learning_ready",
            "transfer_ready",
            "block_ready",
            "good_bye",
            "goodbye",
        }
        if phase in continue_phases or phase.endswith("ready") or phase.endswith("instructions"):
            return self._choose_space(valid_keys, phase)

        if "choice" in phase:
            return self._choose_choice(valid_keys, factors, phase)

        if self.space_key in valid_keys:
            return self._choose_space(valid_keys, phase)

        return Action(key=valid_keys[0], rt_s=self._sample_rt(), meta={"source": "task_sampler", "phase": phase, "kind": "fallback"})
