Use case: infographic-diagram
Asset type: TaskBeacon task flow diagram
Primary request: Create a clean, publication-ready task flow diagram as a timeline collection for the behavioral task described below.

Task: Probabilistic Stimulus Selection
Construct: reinforcement learning / probabilistic feedback learning / transfer bias
Rows/conditions:
- Train AB: A 0.80, B 0.20.
- Train CD: C 0.70, D 0.30.
- Train EF: E 0.60, F 0.40.
- Transfer: 15 pairings, no feedback.

Timeline phases:
- Train AB: Block ready (3000 ms; no response) -> Choice screen (4000 ms; press A=left / L=right; pair AB) -> Feedback (1000 ms; no response; correct / incorrect; A 0.80 B 0.20) -> ITI (1000 ms; no response; +)
- Train CD: Block ready (3000 ms; no response) -> Choice screen (4000 ms; press A=left / L=right; pair CD) -> Feedback (1000 ms; no response; correct / incorrect; C 0.70 D 0.30) -> ITI (1000 ms; no response; +)
- Train EF: Block ready (3000 ms; no response) -> Choice screen (4000 ms; press A=left / L=right; pair EF) -> Feedback (1000 ms; no response; correct / incorrect; E 0.60 F 0.40) -> ITI (1000 ms; no response; +)
- Transfer: Block ready (3000 ms; no response) -> Choice screen (4000 ms; press A=left / L=right; any of 15 pairings) -> No feedback (0 ms; skip feedback) -> ITI (1000 ms; no response; +)

Visual requirements:
- White background, landscape orientation, crisp dark text, restrained condition accent colors.
- One horizontal row per learning/transfer context.
- Each row contains 4 participant-screen snapshots connected by a subtle arrow.
- Each screen snapshot shows participant-visible screen content only.
- Use simple kana-like symbol cards or role letters, not images.
- Use gray participant-screen boxes, thin black arrows, consistent row spacing, and subtle row separators.
- Place timing labels under each screen in compact text.
- Place row labels at the left of each row.
- Use short labels only; avoid paragraphs inside the image.
- Make all text legible at normal document preview size.
- Leave a clean blank header band across the top 18-20% of the image.

Accuracy constraints:
- Do not invent phases, stimuli, condition names, keys, rewards, or timings.
- Do not reveal hidden score to participants.
- Do not add people, lab equipment, decorative scenes, logos, or unrelated icons.
- Do not draw the task title, construct subtitle, any logo, watermark, brand mark, or `TaskBeacon` text inside the generated image.
- Draw only the timeline content below the blank header band.
- Preserve these exact terms where used: Train AB, Train CD, Train EF, Transfer, A=left, L=right, A 0.80, B 0.20, C 0.70, D 0.30, E 0.60, F 0.40, 3000 ms, 4000 ms, 1000 ms, No feedback.

Style:
TaskBeacon scientific infographic style: clean vector-like raster image, organized spacing, gray screen boxes, restrained color accents, and a blank header-safe area.
