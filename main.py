from contextlib import nullcontext
from pathlib import Path
from typing import Any

import pandas as pd
from psychopy import core

from psyflow import (
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
    set_trial_context,
)

from src import (
    RoleAssignment,
    build_learning_block_schedule,
    build_role_assignment,
    build_transfer_block_schedule,
    coerce_subject_id,
    evaluate_learning_block,
    format_phase_label,
    resolve_block_seed,
    run_trial,
    summarize_transfer_block,
)

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}
def _get_response_key_labels(settings: TaskSettings) -> tuple[str, str]:
    key_labels = dict(getattr(settings, "response_key_labels", {}) or {})
    left_label = str(key_labels.get("left", str(getattr(settings, "response_key_left", "a")).upper()))
    right_label = str(key_labels.get("right", str(getattr(settings, "response_key_right", "l")).upper()))
    return left_label, right_label


def _make_instruction_unit(win, kb, stim_bank, settings, trigger_runtime):
    left_label, right_label = _get_response_key_labels(settings)
    unit = StimUnit("instructions", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format(
            "instruction_text",
            left_key_label=left_label,
            right_key_label=right_label,
        )
    )
    set_trial_context(
        unit,
        trial_id="instructions",
        phase="instructions",
        deadline_s=None,
        valid_keys=["space"],
        block_id="instructions",
        condition_id="instructions",
        task_factors={
            "stage": "instructions",
            "left_key": str(getattr(settings, "response_key_left", "a")),
            "right_key": str(getattr(settings, "response_key_right", "l")),
        },
        stim_id="instruction_text",
    )
    return unit


def _make_block_ready_unit(
    win,
    kb,
    stim_bank,
    trigger_runtime,
    *,
    phase: str,
    phase_label: str,
    block_id: str,
    block_num: int,
):
    unit = StimUnit("block_ready", win, kb, runtime=trigger_runtime).add_stim(
        stim_bank.get_and_format("block_ready", phase_label=phase_label)
    )
    set_trial_context(
        unit,
        trial_id=f"{phase}_ready_{block_num:02d}",
        phase=f"{phase}_ready",
        deadline_s=None,
        valid_keys=[],
        block_id=block_id,
        condition_id=block_id,
        task_factors={
            "stage": f"{phase}_ready",
            "phase_label": phase_label,
            "block_id": block_id,
            "block_num": block_num,
        },
        stim_id="block_ready",
    )
    return unit


def _run_block_trials(
    *,
    win,
    kb,
    settings: TaskSettings,
    stim_bank: StimBank,
    trigger_runtime,
    schedule: list[dict[str, Any]],
    block_id: str,
    block_idx: int,
    score_total: int,
) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    for condition in schedule:
        row = run_trial(
            win=win,
            kb=kb,
            settings=settings,
            condition=condition,
            stim_bank=stim_bank,
            trigger_runtime=trigger_runtime,
            block_id=block_id,
            block_idx=block_idx,
            score_total=score_total,
        )
        rows.append(row)
        score_total = int(row.get("score_total", score_total))
    return rows, score_total


def _make_role_assignment(settings: TaskSettings, subject_id: int) -> RoleAssignment:
    symbol_ids = [f"kana_{idx}" for idx in range(1, 7)]
    return build_role_assignment(
        subject_id=subject_id,
        seed_base=int(getattr(settings, "overall_seed", 40040)),
        symbol_ids=symbol_ids,
        policy=str(getattr(settings, "symbol_role_shuffle_policy", "random_per_subject")),
    )


def run(options: TaskRunOptions):
    """Run the probabilistic stimulus selection task in human/qa/sim mode."""

    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path), extra_keys=["condition_generation"])

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "qa":
            subject_data = {"subject_id": "101"}
        elif options.mode == "sim":
            participant_id = "sim001"
            if runtime_ctx is not None and getattr(runtime_ctx, "session", None) is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim001")
            subject_data = {"subject_id": participant_id}
        else:
            subform = SubInfo(cfg["subform_config"])
            subject_data = subform.collect()

        subject_id = coerce_subject_id(subject_data["subject_id"])

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)
        settings.triggers = cfg["trigger_config"]

        role_assignment = _make_role_assignment(settings, subject_id)
        settings.role_assignment = role_assignment.to_dict()
        settings.role_assignment_policy = str(getattr(settings, "symbol_role_shuffle_policy", "random_per_subject"))
        settings.symbol_pool = list(role_assignment.symbol_ids)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.save_to_json()

        trigger_runtime = initialize_triggers(mock=options.mode in ("qa", "sim")) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        win, kb = initialize_exp(settings)
        stim_bank = StimBank(win, cfg["stim_config"])
        stim_bank = stim_bank.preload_all()

        learning_conditions = list(getattr(settings, "learning_conditions", []) or [])
        transfer_conditions = list(getattr(settings, "transfer_conditions", []) or [])
        learning_probabilities = dict(getattr(settings, "learning_probabilities", {}) or {})
        learning_criteria = dict(getattr(settings, "learning_criteria", {}) or {})
        max_learning_blocks = int(getattr(settings, "max_learning_blocks", 6) or 6)
        learning_trials_per_pair = int(getattr(settings, "learning_trials_per_pair", 20) or 20)
        transfer_trials_per_pair = int(getattr(settings, "transfer_trials_per_pair", 10) or 10)
        left_right_balance_policy = str(getattr(settings, "left_right_balance_policy", "exact_within_block"))

        ready_duration = float(getattr(settings, "ready_duration", getattr(settings, "timing", {}).get("ready_duration", 3.0)) or 3.0)
        response_timeout = float(getattr(settings, "response_timeout", getattr(settings, "timing", {}).get("response_timeout", 4.0)) or 4.0)
        feedback_duration = float(getattr(settings, "feedback_duration", getattr(settings, "timing", {}).get("feedback_duration", 1.0)) or 1.0)
        iti_duration = float(getattr(settings, "iti_duration", getattr(settings, "timing", {}).get("iti_duration", 1.0)) or 1.0)

        score_total = 0
        all_rows: list[dict[str, Any]] = []

        trigger_runtime.send(settings.triggers.get("exp_onset"))

        instruction = _make_instruction_unit(win, kb, stim_bank, settings, trigger_runtime)
        if getattr(settings, "voice_enabled", False):
            try:
                instruction.add_stim(stim_bank.get("instruction_text_voice"))
            except Exception:
                pass
        instruction.wait_and_continue()

        learning_passed = False
        learning_blocks_completed = 0
        for block_idx in range(max_learning_blocks):
            block_num = block_idx + 1
            block_id = f"learning_block_{block_num:02d}"
            learning_ready = _make_block_ready_unit(
                win,
                kb,
                stim_bank,
                trigger_runtime,
                phase="learning",
                phase_label=format_phase_label("learning", block_num),
                block_id=block_id,
                block_num=block_num,
            )
            learning_ready.show(duration=ready_duration, onset_trigger=settings.triggers.get("block_onset"))

            block_seed = resolve_block_seed(settings, block_idx)
            learning_schedule = build_learning_block_schedule(
                block_idx=block_idx,
                block_seed=block_seed,
                pair_order=learning_conditions,
                trials_per_pair=learning_trials_per_pair,
                role_assignment=role_assignment,
                learning_probabilities=learning_probabilities,
                left_right_balance_policy=left_right_balance_policy,
            )
            block_rows, score_total = _run_block_trials(
                win=win,
                kb=kb,
                settings=settings,
                stim_bank=stim_bank,
                trigger_runtime=trigger_runtime,
                schedule=learning_schedule,
                block_id=block_id,
                block_idx=block_idx,
                score_total=score_total,
            )
            all_rows.extend(block_rows)
            learning_blocks_completed += 1
            summary = evaluate_learning_block(block_rows, learning_criteria)
            print(
                f"[pss] learning block {block_num}: overall={summary['overall_accuracy']:.1%} "
                f"passed={summary['passed']} pair={summary['pair_accuracy']}"
            )
            trigger_runtime.send(settings.triggers.get("block_end"))
            if summary["passed"]:
                learning_passed = True
                break

        if not learning_passed:
            print(f"[pss] learning criterion was not met within {max_learning_blocks} block(s); proceeding to transfer.")

        transfer_block_idx = learning_blocks_completed
        transfer_block_id = "transfer_block"
        transfer_ready = _make_block_ready_unit(
            win,
            kb,
            stim_bank,
            trigger_runtime,
            phase="transfer",
            phase_label=format_phase_label("transfer", 1),
            block_id=transfer_block_id,
            block_num=1,
        )
        transfer_ready.show(duration=ready_duration, onset_trigger=settings.triggers.get("block_onset"))

        transfer_seed = resolve_block_seed(settings, transfer_block_idx)
        transfer_schedule = build_transfer_block_schedule(
            block_idx=transfer_block_idx,
            block_seed=transfer_seed,
            pair_order=transfer_conditions,
            trials_per_pair=transfer_trials_per_pair,
            role_assignment=role_assignment,
            left_right_balance_policy=left_right_balance_policy,
        )
        transfer_rows, score_total = _run_block_trials(
            win=win,
            kb=kb,
            settings=settings,
            stim_bank=stim_bank,
            trigger_runtime=trigger_runtime,
            schedule=transfer_schedule,
            block_id=transfer_block_id,
            block_idx=transfer_block_idx,
            score_total=score_total,
        )
        all_rows.extend(transfer_rows)
        transfer_summary = summarize_transfer_block(transfer_rows)
        print(
            f"[pss] transfer: role_rates={transfer_summary['role_choice_rate']} "
            f"timeouts={transfer_summary['timeouts']}"
        )
        trigger_runtime.send(settings.triggers.get("block_end"))

        goodbye = StimUnit("good_bye", win, kb, runtime=trigger_runtime).add_stim(stim_bank.get("good_bye"))
        set_trial_context(
            goodbye,
            trial_id="good_bye",
            phase="good_bye",
            deadline_s=None,
            valid_keys=["space"],
            block_id="good_bye",
            condition_id="good_bye",
            task_factors={
                "stage": "good_bye",
                "learning_passed": learning_passed,
                "total_trials": len(all_rows),
                "score_total": score_total,
            },
            stim_id="good_bye",
        )
        goodbye.wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))

        df = pd.DataFrame(all_rows)
        if not df.empty:
            df.to_csv(settings.res_file, index=False)
        else:
            pd.DataFrame().to_csv(settings.res_file, index=False)

        if hasattr(trigger_runtime, "close"):
            try:
                trigger_runtime.close()
            except Exception:
                pass
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run Probabilistic Stimulus Selection in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
