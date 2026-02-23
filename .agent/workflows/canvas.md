---
description: Visualize current project architecture or UI mocks in a live browser canvas.
---

# Workflow: /canvas

This workflow opens the current Live Canvas state in the browser.

## Steps

1. **Verify State**: Check if `.agent/canvas/state.html` exists.
2. **Generate (if missing)**: If it doesn't exist, create a default "Antigravity Dashboard" page.
// turbo
3. **Open Browser**: Use `Start-Process .agent/canvas/state.html` (Windows) or open via tool.
4. **Report**: Confirm to the user that the canvas is active.

## Triggering

Invoke this command whenever you need a visual representation of the progress.
