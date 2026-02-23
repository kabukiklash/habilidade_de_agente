---
name: canvas
description: Visual workspace orchestration. Allows the agent to generate and update real-time visual dashboards, diagrams, and UI mocks.
tools: Write, Read, Browser
---

# Canvas Skill (Live Canvas)

Inspired by Clawdbot's Live Canvas/A2UI, this skill enables a visual layer for AI-human collaboration.

## Features

- **Diagramming**: Generate Mermaid or SVG diagrams and render them in a local HTML dashboard.
- **UI Mocks**: Create interactive prototypes using Vanilla CSS/JS.
- **Real-time Updates**: Overwrite the `canvas_state.html` to push changes to the user's browser.

## Protocol

1. **State Update**: Write the visual state to `.agent/canvas/state.html`.
2. **Persistence**: Maintain old states in `.agent/canvas/history/`.
3. **Trigger**: Use the `/canvas` workflow to automatically open the state in the default browser.

## Styling Guidelines

- Use a premium dark theme.
- Glassmorphism effects for cards.
- Smooth CSS transitions for state updates.
