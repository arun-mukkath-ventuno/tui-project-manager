# TUI Project Manager - First Pass Design Guideline

This is a first-pass visual guideline for the terminal UI.
The goal is to make the app feel intentional, calm, and information-dense
without turning it into a generic admin table.

## Design Goals

- Make the UI easy to scan in under a second
- Keep project state obvious at all times
- Use visual hierarchy to separate dashboard, drilldown, and task detail
- Avoid noisy decoration
- Keep the interface readable in small terminals as well as wide ones

## Overall Feel

The app should feel like a project control room, not a spreadsheet.
That means:

- strong hierarchy
- compact but legible data presentation
- calm dark surfaces
- restrained use of accent color
- clear separation between sections

## Visual Principles

### 1. Hierarchy First

- Project name should be the strongest text on the screen
- Status counts should be secondary but highly visible
- Metadata like source paths and timestamps should be dimmer
- Task rows should not compete with the main header or summary

### 2. Consistent Status Language

Use the same visual treatment everywhere for the same status:

- `open` = neutral or muted
- `wip` = attention color
- `dev-complete` = positive accent
- `qa-complete` = stronger positive accent
- `in-production` = stable success state
- blockers or risks = warning accent

### 3. Density Without Clutter

- Favor compact cards and grouped panels
- Avoid large empty spaces that make the UI feel unfinished
- Use section headers and panel borders to create structure
- Keep rows tight, but add enough padding that the screen does not feel cramped

### 4. Restraint

- Use one primary accent color
- Use a second accent only for warnings or blocker states
- Avoid rainbow UI patterns
- Avoid over-styled tables with too many competing effects

## Palette Direction

Suggested direction:

- background: very dark navy or charcoal
- primary text: near-white
- secondary text: muted blue-gray
- accent: blue or cyan
- positive: green
- warning: amber
- danger: red

Keep contrast strong enough for terminal readability.
Do not rely on color alone for meaning.

## Typography Direction

Textual is fixed-width, so typography here means emphasis and hierarchy:

- bold for titles and active labels
- dim for timestamps, source paths, and metadata
- uppercase only for small section labels if needed
- avoid shouting with all caps for long content
- keep titles and counts short and visually distinct

## Layout Direction

### Dashboard

Recommended structure:

- hero band at the top
- compact status cards beneath it
- project list or project cards below
- clear refresh and sync state messaging

The dashboard should answer:

- what projects exist
- what state they are in
- what changed recently
- what needs attention

### Project Drilldown

Recommended structure:

- top summary band with project name and counts
- summary panel or insight panel
- task table underneath
- phase grouping separators if space allows

The drilldown should answer:

- where work sits by phase
- which tasks are active
- what the project owner needs to focus on next

### Task Detail

Recommended structure:

- prominent task title
- status and owner at the top
- phase and project information beneath
- source metadata secondary
- notes or history area reserved for later growth

## Component Style

### Cards and Panels

- use bordered panels for major regions
- use cards for summary metrics and highlighted states
- keep panel corners consistent across the app

### Badges

- use small status badges for counts and task states
- keep badge text short
- use color sparingly

### Tables

- keep tables clean and readable
- avoid too many columns on smaller terminals
- prioritize project/task identity over raw metadata
- if a table gets too wide, split the layout instead of shrinking everything

## State Styling

### Selected State

- make the selected row obvious with background and text emphasis
- do not rely on subtle contrast differences

### Loading State

- show a clear loading message
- keep it calm and intentional

### Empty State

- explain what is missing
- tell the user what action to take next
- make the empty state feel designed, not broken

### Error State

- keep errors short and readable
- state the cause first
- avoid stack traces in the main UI

## Motion and Feedback

- use very light transitions only
- refresh should feel immediate and explicit
- summary generation should have a visible loading state
- avoid flashy motion that slows the workflow down

## Visual Guardrails

- no purple default theme
- no generic IDE-style default layout
- no flat white-background admin look
- no excessive animation
- no decorative clutter that hides data

## First Screens to Polish

1. Dashboard
2. Project drilldown
3. Task detail
4. Summary panel

## Guideline Status

This is the first pass only.
It should evolve after the UI is seen in terminal and refined with real usage.

