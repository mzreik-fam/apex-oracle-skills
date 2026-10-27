---
name: apex-ux
description: Make Oracle APEX screens clear and user friendly for the people who actually use them: headings, column names, filters, editable versus locked fields, grids versus reports, dialogs, empty states, and showing names instead of ids. Use this whenever designing, building, reviewing or improving any APEX page, report, grid, form, dashboard or navigation, when a user says a screen is confusing, cluttered or hard to use, or before showing a new APEX screen to its users, even if they do not mention UX.
---

# APEX UX: screens people understand without help

The test for every screen: could a new colleague use it without asking anyone? Users scan, they do not read. Every extra column, label or button spends their attention, so each one should earn its place.

## Before designing: ask these three things

1. **Who uses this and what decision do they make with it?** The screen exists for that decision; build around it, not around the table.
2. **What do they look for first, and what do they change?** The first becomes the leading columns and the filters; the second is the only editable part.
3. **What does a wrong value cost?** The higher the cost, the more you lock, confirm and explain.

## Rules (and why)

- **Show names, not ids.** People recognise "Business Bay", not 526. Keep the id only where people copy it elsewhere, and label it ("DLD project number").
- **Plain headings.** "Property Number", not `PROPERTY_NUM` or "prop_no_fk". Use the words the business uses. If a technical term is unavoidable, add a one-line hint.
- **Lock what must not change, and make that visible.** Read-only cells look read-only (grey, no input box). Editable cells look editable. Never leave a field editable that the save process will ignore.
- **One fact, one place.** If a name appears in a heading, the page title and a column, the reader wonders which is the real one. Show the path or parent once.
- **Search and filters first.** Put search at the top, filters where users already look (a left column of clickable counts works well). Show the count next to each filter: an empty filter should not look like a bug. Default to a useful sort and 50 rows, not 10 and unsorted.
- **Choose grid or report on purpose.** A grid is for scanning and editing rows in place. A report is for summarising (group by, pivot, download). If people need both, offer a switch on the same page over the same query rather than two copies of the logic.
- **Use a dialog for detail, a page for work.** Click a name to see its detail in a modal; keep the main page for the list.
- **Dropdowns you can search.** Use a popup list of values for anything with more than about 15 values.
- **Say what happened.** After a save, show what changed; after an error, say what to do next in plain words. An empty result says why it is empty and what to try.
- **Be consistent.** The same thing has the same name on every page (Flag, not Flag here and Level there). The same action sits in the same place.
- **Respect attention.** Show 5 to 10 columns by default and let people add more. Group related columns together; put identifiers and notes last.
- **Accessibility basics.** Do not rely on colour alone; keep contrast readable; every control has a label.

## When you change something people already use

People customise screens in the browser (column choices, headings). Warn before a deploy resets their private saved reports, and keep their headings: export the live page first (see `apex-dev`).

## Finish with a walk-through

Open the page as a new user and try the three most common tasks. Note every moment of hesitation; each one is a fix. Then run the `apex-audit` skill. A checklist you can run line by line is in `references/ux-checklist.md`.
