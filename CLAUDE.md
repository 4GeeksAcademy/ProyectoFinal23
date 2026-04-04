# CLAUDE.md — Python / Streamlit Practical Rules

## Core
1. Think before acting.
2. Keep solutions simple, direct, and practical.
3. User instructions always override this file.
4. Do not add complexity unless clearly necessary.

## Context & Files
5. Read only the files relevant to the task.
6. Read before writing.
7. Do not re-read files unless they may have changed.
8. Ask for more context only if truly necessary.
9. Work from the smallest relevant code block whenever possible.

## Editing
10. Prefer editing over rewriting.
11. Return only the necessary changes whenever possible.
12. Prefer targeted patches, diffs, or exact replacements over full rewrites.
13. Do not modify unrelated code, formatting, naming, or structure.
14. Do not refactor unless explicitly asked.
15. Do not rewrite working code.

## Python
16. Prefer standard library or existing dependencies first.
17. Keep logic readable over clever.
18. Do not overengineer simple problems.
19. Do not add abstractions unless they clearly reduce complexity.
20. Preserve compatibility with the current codebase.

## Streamlit
21. Keep Streamlit code simple and idiomatic.
22. Do not redesign the UI unless requested.
23. Preserve current layout, widgets, and flow unless a fix requires changes.
24. Be careful with session_state, forms, caching, reruns, and widget keys.
25. Do not move chart or UI logic unless necessary.

## Data & Charts
26. Preserve existing data logic unless the task requires changing it.
27. Do not silently change schemas, column names, data types, filters, joins, or aggregations.
28. If a chart is broken, fix only the issue causing the break first.
29. Keep outputs readable and executive-friendly.

## Debugging
30. Identify the root cause before making broad changes.
31. Fix the smallest thing that solves the problem.
32. Choose the least disruptive valid solution first.
33. If assumptions are required, state them briefly.

## Output
34. Keep visible output concise.
35. Do not explain obvious code unless asked.
36. Do not repeat the user's code or context unnecessarily.
37. Prioritize showing only what changed.
38. If useful, structure output as:
   - Problem
   - Cause
   - Fix

## Validation
39. Validate the logic before declaring done.
40. If relevant, provide a short "how to verify".
41. Do not claim certainty where it has not been checked.