<!-- Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved. -->
# Changelog

## Unreleased

### core 1.0.0 (baseline LB1), built against the Rachana g2/integration build at language level 1.2

Built, 28 fragments, each with typed parameters, local column names, a one-line doc, an example Sutra that maps its own
columns, and a ViewModel snapshot:

- figures: `key-figure`, `gauge-figure`, `status-badges`, `period-compare`
- records: `field-list`, `record-card`, `note`, `source-note`
- tables: `data-table`, `measure-table`, `row-picker`, `drill-table`, `tree-table`, `pivot-table`, `headline-list`
- charts: `series-line`, `area-stack`, `ranked-bars`, `donut-breakdown`, `distribution`, `scatter-plot`, `steps-waterfall`, `network-graph`
- states: `alert-banner`, `freshness-badge`
- history: `event-timeline`, `audit-trail`, `version-diff`

Not built (3 of the 31), with the missing feature:

- `entry-form`, `stepped-form`: Core has no standalone form panel; `form:` rides a `table` and its submit is a host action
  (needs the forms items F1 to F4 and host actions in `on:`, I1).
- `compare-ab`: differences computed and toned per field need an iteration over a list of fields (`fn` parameters, X13, or
  `each`, L1).

Differences from the catalogue, forced by what the compiler builds today (to be lifted as it grows):

- a list of records cannot be a parameter (`list<record{...}>` is not a value type), so `status-badges`, `record-card`,
  `field-list`, `period-compare` and the like take a `record{...}` plus a `columns` parameter (`{ label, bind }` entries over it);
- a table parameter must name its columns, so "any columns" tables (`data-table`, `pivot-table`, `drill-table`) declare one
  optional placeholder column `key`; the caller's own columns are read through `columns` or name parameters;
- a `text` parameter is text as written (never an expression), so a message with a figure in it is not possible; the figure
  goes in a `key-figure` beside it (`alert-banner`, `source-note`);
- the rename of caller columns reaches a panel only when its `rows` is the table parameter itself; a sorted or limited
  `rows` loses it (RCH-2120), so `ranked-bars`, `headline-list`, `event-timeline` draw rows in the order given (`limit` is the
  panel's own option); `steps-waterfall` and `network-graph` reshape with `map` to the fixed field names their panels read;
- no `when-bound` on a column (an unmapped optional column draws blank), no `top` or "Other" slice, no `warn-at` band on the
  gauge (the painter draws the bands), no `tone` on `note` (markdown has none), no `feeds:` selection (state is not built);
- events exist only on `table` rows (`row-click`) and `hbar` bars (`bar-click`): `row-picker`, `headline-list`, `ranked-bars`,
  `donut-breakdown` return events, the other charts do not;
- `freshness-badge` is in days against the business day (`today()`), not seconds.

Findings in the Rachana build (for the compiler's owner):

- the keys of an event's `wire.emits` entry come out in a different order from run to run (`{"name":..,"on":..}` or
  `{"on":..,"name":..}`), so a byte-exact ViewModel golden is unstable; `tools/LibCheck.java` compares with object keys sorted.
- a column rename does not apply inside `difference(arg.t, ...)[?@.col ...]` and gives no problem (the filter silently reads
  nothing); `version-diff` uses plain `arg.t[?@.key ...]` filters and `intersect(difference(...), ...)` to stay on the safe forms.
- the Core host has no pivot engine, so the `pivot-table` snapshot is the engine-less state ("this host has no pivot engine");
  its compile check is the test.
- `rachana lib build` writes `exports.fragments` with `name` and `majors` only (no `category`, `status`, `needs`), and there is
  no generator of the docs gallery (LIBRARIES 14) or the gates LG1 to LG5 and LG8 yet; `tools/build.py` writes a library
  `README.md` from the fragment files in their place and `tools/LibCheck.java` stands in for the example and snapshot gate.
