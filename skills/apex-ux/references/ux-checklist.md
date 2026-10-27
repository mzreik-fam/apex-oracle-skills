# UX checklist for an APEX page

Go down the list on the finished page. Anything you answer "no" to is a fix.

## First look
- [ ] The page title says what the page is, in words a user would use.
- [ ] A one-line description says what each row is and what to do here.
- [ ] The most important columns are first; ids, technical flags and notes are last.
- [ ] Default sort and rows per page are sensible (50 or more, sorted by the thing people look for).

## Columns
- [ ] Every heading is plain language, short, and the same as elsewhere in the app.
- [ ] No raw database names (`PROJECT_ID`, `NAME_EN`) in any heading.
- [ ] Ids are replaced by names, or clearly labelled when kept.
- [ ] Dates, numbers and money are formatted and right-aligned where it helps reading.
- [ ] Long text is truncated with the full value on hover or in a detail dialog.

## Editing
- [ ] Only the columns people should change are editable, and they look editable.
- [ ] Locked columns look locked, and it is clear why (a hint or a heading note).
- [ ] Lists of values are searchable when long.
- [ ] Deleting is limited to what may be deleted; the rest uses an Active flag.
- [ ] Save gives feedback; errors say what to do.

## Finding things
- [ ] Search box and column filters work; filters show counts.
- [ ] People can group, sort and download if they need to (use a report for this).
- [ ] An empty state explains itself.

## Navigation
- [ ] Menu names match page titles.
- [ ] Links to detail open a dialog, and closing it returns to the same place.
- [ ] Tabs or switches show which view is current.

## Safety
- [ ] Nothing the user customised was lost in the last deploy (export first).
- [ ] Production data is not changed from a test page.

## Accessibility
- [ ] Information is not conveyed by colour alone; contrast is readable; controls are labelled.
