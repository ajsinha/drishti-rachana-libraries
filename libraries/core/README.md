<!-- Copyright (c) 2026 Ashutosh Sinha <ajsinha@gmail.com>. All rights reserved. -->
---
library: core
version: 1.0.0
summary: Generic screens for any domain - figures, records, tables, basic charts, forms, states and history - as typed fragments.
fragments: 28
language: "1.2"
licence: proprietary (see LICENSE)
---

# Core library

Generic screens for any domain - figures, records, tables, basic charts, forms, states and history - as typed fragments.

28 fragments, written as typed fragments (fragments are functions): local parameter and column names, the caller maps its own data and column names at the use, hermetic, events returned. Each has an example Sutra under `examples/` and a ViewModel snapshot under `goldens/`.

## Figures

### `core/gauge-figure@1`

A value against a maximum as a gauge.

| Parameter | Kind | Notes |
|---|---|---|
| `value` | number | required. The amount used |
| `max` | number | required. The maximum the gauge runs to |
| `label` | text | default 'Used'. What the gauge measures |
| `fmt` | format | default 'pct0'. How the figure is written |

Example: `examples/gauge-figure.sutra.yaml`.

### `core/key-figure@1`

One headline number, large, with its label and a caption.

| Parameter | Kind | Notes |
|---|---|---|
| `value` | number | required. The figure |
| `label` | text | default 'Value'. What the figure is |
| `fmt` | format | default 'amount2'. How the figure is written |
| `caption` | text | optional. A line under the figure |
| `delta` | number | optional. The change against a reference |
| `delta-fmt` | format | default 'signed2'. How the change is written |
| `tone` | enum | default 'accent'. How the figure is toned: by its sign, or one fixed tone |

Example: `examples/key-figure.sutra.yaml`.

### `core/period-compare@1`

One measure now against the same measure in a reference period, with the change.

| Parameter | Kind | Notes |
|---|---|---|
| `now` | number | required. The measure now |
| `then` | number | required. The same measure in the reference period |
| `label` | text | default 'Now'. What the measure is |
| `then-label` | text | default 'Before'. What the reference period is called |
| `fmt` | format | default 'amount0'. How the measure is written |
| `delta-fmt` | format | default 'signed0'. How the change is written |
| `delta-tone` | enum | default 'sign'. How the change is toned: sign (up is good) or a fixed tone |

Example: `examples/period-compare.sutra.yaml`.

### `core/status-badges@1`

A short row of named states, each toned by its value.

| Parameter | Kind | Notes |
|---|---|---|
| `fields` | columns | required. The states: a list of { label, bind } where bind reads the caller's own data |

Example: `examples/status-badges.sutra.yaml`.

## Records

### `core/field-list@1`

The facts of one record as label and value.

| Parameter | Kind | Notes |
|---|---|---|
| `record` | record{} | required. The record whose facts are shown |
| `fields` | columns | required. The facts: a list of { label, bind: "@.field", fmt } |
| `title` | text | default 'Facts'. The panel's title |

Example: `examples/field-list.sutra.yaml`.

### `core/note@1`

A short note telling the reader how to read the figures beside it.

| Parameter | Kind | Notes |
|---|---|---|
| `text` | text | required. The note |

Example: `examples/note.sutra.yaml`.

### `core/record-card@1`

A record as a card, with its name, a line under it, chosen facts and a status.

| Parameter | Kind | Notes |
|---|---|---|
| `record` | record{name: text, subtitle: text, status: text} | required. The card's head: name, subtitle, status |
| `facts` | columns | required. The facts: a list of { label, bind: "@.field", fmt } over the same record |

Slots: `footer`

Example: `examples/record-card.sutra.yaml`.

### `core/source-note@1`

The foot of a screen over published data: publisher, dataset, retrieval date, licence.

| Parameter | Kind | Notes |
|---|---|---|
| `publisher` | text | required. Who published the data |
| `dataset` | text | optional. The dataset or table |
| `retrieved` | text | optional. The day it was retrieved, as you want it written |
| `licence` | text | optional. The licence it is published under |

Example: `examples/source-note.sutra.yaml`.

## Tables

### `core/data-table@1`

A sortable, searchable table of rows with the columns you give, totals and a row event.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(key) | required. The rows |
| `columns` | columns | required. The columns: label, bind over a row as @.name, fmt, total |
| `title` | text | default 'Table'. The panel's title |
| `search` | boolean | default True. Whether the reader can search the rows |
| `limit` | integer | default 200. The most rows drawn |
| `total-label` | text | default 'Total'. The label of the totals row |

Example: `examples/data-table.sutra.yaml`.

### `core/drill-table@1`

A table that groups its rows by a list of levels, outermost first, and opens down them in place.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(key) | required. Rows holding every level column and measure |
| `levels` | columns | required. The columns that group the rows, outermost first: a list of your own column names |
| `columns` | columns | required. The columns: the levels and the measures, each { label, bind: "@.field", fmt, total } |
| `title` | text | default 'Drill'. The panel's title |

Example: `examples/drill-table.sutra.yaml`.

### `core/headline-list@1`

Dated items with a headline, a source and a link: news, announcements, filings.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(date, headline, source, link) | required. One row per item |
| `title` | text | default 'Headlines'. The panel's title |
| `limit` | integer | default 20. The most items shown |
| `date-fmt` | format | default 'date'. How the date is written |

Events: `open`

Example: `examples/headline-list.sutra.yaml`.

### `core/measure-table@1`

A list as a table - a name and two measures, the first totalled, the second toned by sign.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(name, first, second) | required. One row per name |
| `title` | text | default 'Measures'. The panel's title |
| `name-label` | text | default 'Name'. Heading of the name column |
| `first-label` | text | default 'Value'. Heading of the first measure |
| `first-fmt` | format | default 'amount0'. How the first measure is written |
| `second-label` | text | default 'Change'. Heading of the second measure |
| `second-fmt` | format | default 'signed2'. How the second measure is written |

Example: `examples/measure-table.sutra.yaml`.

### `core/pivot-table@1`

A cross-tabulation of one measure by a row field and a column field, with totals and an optional heat scale.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(key) | required. Rows at any grain; the three fields named below are read from them |
| `by` | id | required. The column of your rows whose values run down the side |
| `across` | id | required. The column of your rows whose values run across the top |
| `value` | id | required. The numeric column that is added up |
| `agg` | enum | default 'sum'. How the measure is added up |
| `fmt` | format | default 'amount0'. How the measure is written |
| `heat` | boolean | default False. Whether cells are shaded by size |
| `totals` | boolean | default True. Whether row and column totals are shown |
| `title` | text | default 'Cross-tab'. The panel's title |

Example: `examples/pivot-table.sutra.yaml`.

### `core/row-picker@1`

A compact table whose rows, clicked, raise an event with the row's id - the master of a master-detail screen.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(id, name, type, amount, date) | required. One row per item |
| `title` | text | default 'Pick one'. The panel's title |
| `name-label` | text | default 'Name'. Heading of the name column |
| `type-label` | text | default 'Type'. Heading of the type column |
| `amount-label` | text | default 'Amount'. Heading of the amount column |
| `date-label` | text | default 'Date'. Heading of the date column |
| `amount-fmt` | format | default 'amount0'. How the amount is written |

Events: `select`

Example: `examples/row-picker.sutra.yaml`.

### `core/tree-table@1`

A hierarchy given as rows with a parent column, shown as an expanding table with measures per node.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(id, parent, name) | required. One row per node |
| `title` | text | default 'Hierarchy'. The panel's title |
| `open` | integer | default 1. How many levels start open |

Example: `examples/tree-table.sutra.yaml`.

## Charts

### `core/area-stack@1`

Series stacked as areas over time, with an optional horizontal limit.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(x) | required. One row per x, one column per series |
| `series` | columns | required. The columns to stack, in order: a list of { label, value } where value is your own column name |
| `title` | text | default 'Stacked areas'. The panel's title |
| `limit` | number | optional. A horizontal limit drawn across the stack |
| `limit-label` | text | default 'Limit'. What the limit is called |
| `unit` | text | default ''. The unit |

Example: `examples/area-stack.sutra.yaml`.

### `core/distribution@1`

A histogram of one numeric column, with an optional marked value.

| Parameter | Kind | Notes |
|---|---|---|
| `values` | list<number> | required. The values to count into bins |
| `title` | text | default 'Distribution'. The panel's title |
| `bins` | integer | default 40. How many bins |
| `marker` | number | optional. A value to mark |
| `marker-label` | text | default 'Marker'. What the marked value is called |
| `fmt` | format | default 'compact'. How the values are written |
| `unit` | text | default ''. The unit |

Example: `examples/distribution.sutra.yaml`.

### `core/donut-breakdown@1`

The shares of a whole as a donut.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(label, value) | required. One row per slice |
| `title` | text | default 'Mix'. The panel's title |
| `fmt` | format | default 'amount0'. How the values are written |

Events: `slice`

Example: `examples/donut-breakdown.sutra.yaml`.

### `core/network-graph@1`

Nodes and edges: who is connected to whom, grouped by colour.

| Parameter | Kind | Notes |
|---|---|---|
| `nodes` | table(id, label, group) | required. One row per node |
| `edges` | table(from, to, label) | required. One row per edge |
| `title` | text | default 'Network'. The panel's title |
| `layout` | enum | default 'force'. How the nodes are laid out |

Example: `examples/network-graph.sutra.yaml`.

### `core/ranked-bars@1`

One horizontal bar a row, labelled and sized by a value.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(label, value) | required. One row per bar |
| `title` | text | default 'Ranking'. The panel's title |
| `fmt` | format | default 'amount0'. How the values are written |
| `tone` | enum | default 'accent'. How the bars are toned |

Events: `bar`

Example: `examples/ranked-bars.sutra.yaml`.

### `core/scatter-plot@1`

Points by two measures, optionally sized, grouped by colour and labelled.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(x, y, label, group, size) | required. One row per point |
| `title` | text | default 'Scatter'. The panel's title |
| `x-label` | text | required. What x measures |
| `y-label` | text | required. What y measures |
| `x-fmt` | format | default 'amount2'. How x is written |
| `fmt` | format | default 'amount2'. How y is written |

Example: `examples/scatter-plot.sutra.yaml`.

### `core/series-line@1`

A line of one series: x along the bottom, y up the side.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(x, y) | required. One row per point, in x order |
| `title` | text | default 'Series'. The panel's title |
| `fmt` | format | default 'amount2'. How the values are written |
| `unit` | text | default ''. The unit |
| `step` | boolean | default False. Whether the line steps between points instead of joining them |
| `mark` | text | optional. An x value to mark |

Example: `examples/series-line.sutra.yaml`.

### `core/steps-waterfall@1`

From a starting total to an ending total through signed steps.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(label, value, total) | required. One row per step, in order |
| `title` | text | default 'Bridge'. The panel's title |
| `fmt` | format | default 'signed0'. How the amounts are written |
| `unit` | text | default ''. The unit |
| `sum-label` | text | default 'Total'. What the closing figure is called |

Example: `examples/steps-waterfall.sutra.yaml`.

## States and feedback

### `core/alert-banner@1`

A line across the screen, shown only while its condition holds.

| Parameter | Kind | Notes |
|---|---|---|
| `show` | boolean | required. Whether the banner is shown |
| `text` | text | required. The words of the banner |
| `label` | text | default 'Notice'. The word that heads the banner |

Example: `examples/alert-banner.sutra.yaml`.

### `core/freshness-badge@1`

How old the data is, and whether it is older than it should be.

| Parameter | Kind | Notes |
|---|---|---|
| `as-of` | date | required. The day the data was loaded or published |
| `stale-days` | integer | default 1. The age in days beyond which the data is stale |
| `label` | text | default 'As of'. What the date is called |

Example: `examples/freshness-badge.sutra.yaml`.

## History and comparison

### `core/audit-trail@1`

Who changed what and when: actor, time, field, the value before and after.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(at, actor, action, field, before, after) | required. One row per change |
| `title` | text | default 'Changes'. The panel's title |
| `limit` | integer | default 100. The most changes shown |

Example: `examples/audit-trail.sutra.yaml`.

### `core/event-timeline@1`

Dated events with a label, a detail line and a status.

| Parameter | Kind | Notes |
|---|---|---|
| `rows` | table(date, label, detail, status) | required. One row per event |
| `title` | text | default 'History'. The panel's title |

Example: `examples/event-timeline.sutra.yaml`.

### `core/version-diff@1`

Rows added, removed and changed between two versions of a keyed table.

| Parameter | Kind | Notes |
|---|---|---|
| `before` | table(key) | required. The old version |
| `after` | table(key) | required. The new version, with the same columns |
| `columns` | columns | required. The columns to show: a list of { label, bind: "@.field", fmt } |
| `title` | text | default 'Changes'. The title of the three tables |

Example: `examples/version-diff.sutra.yaml`.

