# Task Plot Review

## Evidence Match

- Pass: title and construct match Probabilistic Stimulus Selection.
- Pass: rows match Train AB, Train CD, Train EF, and no-feedback Transfer contexts.
- Pass: phase order matches README and `src/run_trial.py`: Block ready -> Choice screen -> Feedback or No feedback -> ITI.
- Pass: timing labels match config: 3000 ms ready, 4000 ms response window, 1000 ms learning feedback, 1000 ms ITI.
- Pass: response mapping shows A=left and L=right.
- Pass: learning probabilities preserve AB 80/20, CD 70/30, and EF 60/40.
- Pass: transfer row explicitly skips feedback and does not expose hidden score.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
