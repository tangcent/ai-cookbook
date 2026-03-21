---
name: grafana-dashboard
description: Build and modify Grafana dashboards following the user's established style conventions. Use when creating new dashboards, adding panels, modifying existing dashboards, or reviewing dashboard JSON for consistency. Requires the Grafana MCP to be enabled.
---

# Grafana Dashboard Skill

## When to Activate

Activate this skill when the user asks to:

- Create a new Grafana dashboard
- Add or modify panels on an existing dashboard
- Review a dashboard for style consistency
- Build monitoring dashboards for a service or component
- Generate dashboard JSON or PromQL queries for Grafana

## Pre-Flight Check — Grafana MCP Required

Before performing any Grafana operation, verify the Grafana MCP is available by attempting a lightweight call (e.g. `search_dashboards`).

If the Grafana MCP is **not available or not responding**, stop and tell the user:

> The Grafana MCP server is not enabled. To use this skill you need to configure it.
>
> 1. Install `mcp-grafana` — see `mcp/grafana.md` in this repo for instructions.
> 2. Add the server config to `.kiro/settings/mcp.json` (or your user-level config).
> 3. Reconnect MCP servers from the Kiro MCP panel.
>
> Once the Grafana MCP is connected, try again.

Do **not** attempt to generate raw JSON without the MCP — the skill relies on live queries to discover metrics, labels, and datasource UIDs.

## Dashboard Style Guide — User Preferences

The following conventions are extracted from the user's existing dashboards. **All new dashboards and panels MUST follow these rules.**

### 1. Overall Structure

- **Folder**: Place dashboards in the appropriate project folder. Ask the user if unsure.
- **Tags**: Every dashboard MUST have descriptive, lowercase, hyphenated tags (e.g. `http`, `performance`, `tracking`, `business`, `sdk`, `grpc`, `kafka`). Tags should cover: the domain, the component, and the dashboard purpose.
- **Project/application identity tags are mandatory on new dashboards**: When creating a dashboard, always add the project name and application name as tags, normalized to lowercase hyphenated form. Example: project `Ads Delivery Platform` -> tag `ads-delivery-platform`; application `tracking-api` -> tag `tracking-api`.
- **Do not create a new dashboard until those identity tags are known**: Infer them from the user's request, folder context, datasource labels, or existing related dashboards. If still unclear, ask the user for the project name and application name before creating the dashboard skeleton.
- **Description**: Every dashboard MUST have a `description` field — one sentence summarizing what it monitors and for which service.
- **Default time range**: `now-6h` to `now` for business/performance dashboards; `now-1h` to `now` for operational/real-time dashboards.
- **Auto-refresh**: Set `refresh: "30s"` only for operational dashboards (queues, pipelines). Omit for analytical dashboards.

### 2. Template Variables

- Always include a `cluster` variable:
  - Type: `query`
  - Datasource: Prometheus (uid `M2qX4-R4k`)
  - Query pattern: `label_values(<a_relevant_metric>{...}, cluster)`
  - `includeAll: true`, `allValue: ".*"`
- Include an `app` variable when the dashboard covers multiple apps:
  - Query pattern: `label_values(<metric>{kubernetes_namespace="<ns>"}, app)`
  - `includeAll: false`
- Additional filter variables (e.g. `method_filter`, `brand`, `pod`) as custom or query types when needed.
- Variable queries use `label_values(...)` syntax, refresh on dashboard load (`refresh: 1`).

### 3. Layout — Row & Panel Organization

The dashboard follows a **top-down drill-down** pattern:

1. **Overview row** (collapsed: false) — a horizontal strip of `stat` panels showing KPIs at a glance.
2. **Timeseries rows** — key trend charts (QPS, latency, error rate) directly below the overview.
3. **Detail / Drill-down rows** (collapsed: true) — per-endpoint, per-status, per-dimension breakdowns.
4. **Error Detail row** (collapsed: true) — error-specific panels.
5. **Supplementary rows** (collapsed: true) — version adoption, runtime health, etc.

Row IDs use round numbers with spacing for future inserts: 100, 200, 300, 400, 500, 600.

#### CRITICAL: Every Row Must Fill the Full 24-Column Width — No Orphan Panels

Grafana uses a 24-column grid. **Every horizontal line of panels MUST sum to exactly 24 columns.** Never leave empty space at the end of a row.

**The core principle: plan the full row first, then assign widths.**

1. Decide which panels belong on the same horizontal line.
2. Count them.
3. Divide 24 by that count and distribute widths so they sum to exactly 24.
4. If a panel would be alone or leave a gap, **widen it to fill the remaining space**, or **pull it up to join the previous row** (adjusting widths of that row to accommodate).

**Handling orphan panels (the most common mistake):**

An "orphan" is a panel that ends up alone (or with too few siblings) on a row, leaving large empty space. This looks bad:

```
BAD:  [■■■][                     ]   ← 1 stat alone on a row (w:3, 21 cols wasted)
BAD:  [■■■■■■■■■■■■][            ]   ← 1 timeseries alone (w:12, 12 cols wasted)
```

**Fix orphan panels using one of these strategies (in order of preference):**

1. **Widen to fill**: A single stat → `w:24`. A single timeseries → `w:24`. Two stats → `w:12` each. Three stats → `w:8` each.
2. **Merge into adjacent row**: Move the orphan panel onto the same horizontal line as related panels above or below, and redistribute widths. For example, 1 orphan stat + 2 timeseries → `[stat w:4][timeseries w:10][timeseries w:10]` = 24.
3. **Pair with a related timeseries**: A stat + its corresponding timeseries on the same row → `[stat w:4][timeseries w:20]` = 24, or `[stat w:3][timeseries w:21]` = 24.

**Never place a panel that occupies less than the full 24 columns on a row by itself.**

**Stat panel row sizing — pick the width that fills the row:**

| Stat count per row | Width each | Layout | Total |
|---|---|---|---|
| 8 | `w: 3` | `3×8` | 24 ✓ |
| 6 | `w: 4` | `4×6` | 24 ✓ |
| 5 | `w: 5,5,5,5,4` | mixed | 24 ✓ |
| 4 | `w: 6` | `6×4` | 24 ✓ |
| 3 | `w: 8` | `8×3` | 24 ✓ |
| 2 | `w: 12` | `12×2` | 24 ✓ |
| 1 | `w: 24` | full-width | 24 ✓ |
| 7 | `w: 3,3,3,3,4,4,4` | mixed | 24 ✓ |

When the count doesn't divide evenly into 24, **widen the last few panels** to absorb the remainder. For example, 7 stats → four `w:3` + three `w:4` = 24.

**Multi-row stat blocks** (e.g. 9+ stats): fill complete rows of 8 (`w:3`) first, then apply the table above to the remainder row. Example: 9 stats → row 1: eight `w:3`, row 2: one stat `w:3` **merged with related timeseries** to fill 24, or widened to `w:24` if standalone.

**Multi-row stat blocks by group** (e.g. Outbound API with 12 stats grouped by protocol): arrange as multiple full rows. Example: 6 stats per row × 2 rows, each `w:4`.

**Timeseries panel row sizing:**

| Panel count per row | Width each | Total |
|---|---|---|
| 1 | `w: 24` | 24 ✓ |
| 2 | `w: 12` | 24 ✓ |
| 3 | `w: 8` | 24 ✓ |

**A single timeseries MUST be `w:24`** — never `w:12` alone on a row.

**Pie + Timeseries paired rows** (used in Validation dashboards):

Each dimension gets a pie chart + timeseries side by side. Two pairs per row:
`[pie w:4] [timeseries w:8] [pie w:4] [timeseries w:8]` = 24 ✓

One pair alone on a row: `[pie w:6] [timeseries w:18]` = 24 ✓ (widen to fill)

**Stat + Timeseries mixed rows** (used in Pipeline dashboards):

When combining stat cards with a large timeseries in the same row, ensure they tile to 24:
`[stat w:4] [stat w:3] [timeseries w:17]` = 24 ✓

**Bar gauge / Bar chart panels**: Use `w:12` (half, paired with another panel) or `w:24` (full) to fill the row.

**Self-check before finalizing any dashboard:** Scan every `y` coordinate. For each unique `y`, sum the `w` values of all panels at that `y`. If any sum is less than 24, fix it before saving.

#### CRITICAL: No Uncovered Vertical Space Next to a Taller Panel

When panels on the same row have different heights, the shorter panel(s) must collectively fill the full column height — otherwise a blank gap appears below them.

```
BAD:  [stat h:4          ][timeseries h:8]
      [     gap h:4       ]
      ← stat leaves 4 rows of blank space below it

GOOD: [stat h:8          ][timeseries h:8]   ← single stat stretched to match
GOOD: [stat h:4][stat h:4][timeseries h:8]   ← two stats stacked (y and y+4) fill h:8 together
```

**Rule: For any column of panels adjacent to a taller panel, the sum of `h` values in that column MUST equal the height of the tallest panel in the row.**

Concretely, when pairing stat(s) with a timeseries (`h:8`):
- 1 stat alone → set `h:8`
- 2 stats stacked → each `h:4` (4+4=8 ✓)
- 3 stats stacked → not recommended; use `h:3,h:3,h:2` or restructure

### 4. Stat Panels (KPI Cards)

- **Panel type**: `stat`
- **Color mode**: `background_solid`
- **Graph mode**: `none`
- **Reduce calc**: `lastNotNull`
- **Height**: `h: 4` always.
- **Width**: Determined by the row-fill rule above — typically `w: 3` (8 per row), `w: 4` (6 per row), or `w: 5` (≈5 per row with mixed widths). Choose the width that makes the row sum to exactly 24.
- **Every stat panel MUST have a `description`** explaining what it shows and (for threshold-based ones) the threshold meaning.

#### Standard Threshold Conventions

| Metric Type | Unit | Thresholds (color steps) |
|---|---|---|
| Count / Total | `short` | Single step: `blue` at base |
| Success Rate | `percentunit` | `green` (base) → `yellow` at 0.95 → `red` below 0.95 (inverted: higher is better) |
| Error Rate | `percentunit` | `green` (base) → `orange` at 0.01 → `red` at 0.05 |
| Mean Latency | `ms` | `green` (base) → `yellow` at 50 → `red` at 100 |
| P95 Latency | `ms` | `green` (base) → `yellow` at 100 → `red` at 200 |
| Kafka Success Rate | `percentunit` | `green` (base) → `yellow` at 0.99 → `red` below 0.99 |
| Flagged / Blocked % | `percentunit` | `green` (base) → `orange` at 0.05 → `red` at 0.10 |
| Queue depth / Pending | `short` | `green` (base) → `yellow` at warning → `red` at critical (context-dependent) |

### 5. Timeseries Panels

- **Height**: `h: 8` always.
- **Width**: Must fill the full 24-column row — `w: 12` (2 per row), `w: 8` (3 per row), or `w: 24` (full-width). Never use a width that leaves a gap.
- **Draw style**: `line`
- **Line interpolation**: `smooth`
- **Line width**: `1`
- **Fill opacity**: `15`
- **Gradient mode**: `opacity`
- **Point size**: `5`, show points: `auto`
- **Stacking**: `none` (unless explicitly showing stacked throughput by status)
- **Tooltip**: `multi` with sort `desc` for multi-query panels; `single` for single-query panels.
- **Legend**: `list` placement `bottom`. Include `calcs: ["max", "mean"]` for latency panels; omit calcs for throughput panels.
- **Scale**: Use `symlog` (log base 10) for latency panels to handle spikes. Use `linear` for throughput/QPS panels.

#### Latency Panels

- Show P99, P95, P90, P50 as separate queries in one panel.
- Use `histogram_quantile()` with `sum(rate(..._bucket{...}[1m])) by (le)`.
- Multiply by `1000` to convert seconds → milliseconds. Unit: `ms`.
- Use overrides with `byRegexp` matcher to set display names: `P99`, `P95`, `P90`, `P50`.

#### Throughput Panels

- Use `sum(rate(..._count{...}[1m]))` for QPS timeseries.
- Use `sum(rate(...[1m])) by (status)` to break down by status.
- Rate interval: `1m` for timeseries panels, `5m` for stat panel averages.

### 6. Pie Chart Panels

- Used for **percentage distribution** breakdowns (e.g. "Issues — % by Issue Type").
- Always paired with a corresponding timeseries "Rate by ..." panel.
- Query uses `sum(increase(...[$__range])) by (dimension)`.
- Title pattern: `<Metric> — % by <Dimension>`.

### 7. Bar Gauge / Bar Chart Panels

- Used for **Top N** rankings (e.g. "Top 10 Slowest Endpoints", "Top 10 Issue Types").
- Query uses `topk(N, ...)`.
- Used for **categorical breakdowns** (e.g. "Failure Codes (1h)") with `sum by (code) (increase(...[1h]))`.

### 8. PromQL Conventions

- **Always filter by `cluster=~"$cluster"`** in every query.
- **Always filter by `app="$app"`** when the `app` variable exists.
- For stat panels showing totals over the selected range: use `sum(increase(...[$__range]))`.
- For stat panels showing averages: use `avg_over_time(sum(rate(...[5m]))[$__range])`.
- For stat panels showing ratios: use `sum(increase(...{success}[$__range])) / clamp_min(sum(increase(...[$__range])), 1)`.
  - **Always use `clamp_min(..., 1)` on denominators** to avoid division by zero. Exception: when the denominator is guaranteed non-zero (e.g. total requests in a high-traffic service), a plain division is acceptable.
- For timeseries rate panels: use `$__rate_interval` or `1m` as the rate window.
- Latency from histogram: `histogram_quantile(0.XX, sum(rate(..._bucket{...}[interval])) by (le)) * 1000`.
- Mean latency: `sum(rate(..._sum{...}[interval])) / sum(rate(..._count{...}[interval])) * 1000`.
- Metric naming convention observed: `<namespace>_<component>_<metric_name>_<unit>` (e.g. `as_sdk_tracking_sdk_tracking_request_seconds_count`).

### 9. Panel Descriptions

**Every panel MUST have a `description` field.** Follow this pattern:

- For stat panels: State what the number represents, and if thresholds apply, describe them inline.
  - Example: `"Average request latency across all endpoints over the selected time range. Green < 50ms, yellow < 100ms, red >= 100ms."`
- For timeseries panels: State what the chart shows and how it's computed.
  - Example: `"Aggregate HTTP request throughput across all endpoints, computed as a 1-minute rate."`
- For pie/bar panels: State the dimension being broken down.
  - Example: `"Top Pixel validation issue types over the selected time range."`

### 10. Panel Title Naming Conventions

- Stat panels: Short noun phrases — `Total Events`, `Mean QPS`, `Success Rate`, `P95 Latency`, `Error Rate`.
- Timeseries panels: Descriptive — `Event Throughput by Status (QPS)`, `Request Latency`, `Non-Success Request Rate`.
- Paired pie+timeseries: `<Subject> — % by <Dim>` and `<Subject> — Rate by <Dim>`.
- Row titles: Functional groupings — `Overview`, `Detail`, `Error Detail`, `Queue & Throughput`, `Latency & Audit Quality`, `Runtime Health`.

### 11. Dashboard Patterns by Category

#### HTTP Service Performance Dashboard
Overview stats: Total Requests → Mean QPS → Error Rate → Active Requests → Mean Latency → P95 → P90 → P50.
Timeseries: QPS → Latency Percentiles → Top 10 Slowest Endpoints → Error Rate → Volume by Endpoint.
Drill-down rows: Detailed URI Performance, Error Details.

#### Business Metrics Dashboard
Overview stats: Total Events → Mean QPS → Success Rate → Mean Latency → P95 Latency → HTTP Error Rate → Kafka Success Rate → Flagged %.
Timeseries: Event Throughput by Status → Avg Latency.
Drill-down rows: Regional Breakdown, Detail, Error Detail, SDK Version Adoption.

#### Outbound API Performance Dashboard
Overview stats: grouped by protocol (gRPC / HTTP Client / Feign) — each group has Total Calls → Success Rate → QPS → Mean Latency.
Detail rows: one per protocol + Kafka Producer.

#### Pipeline / Queue Dashboard
Overview stats: queue depths (Pending, Processing, Dispatched) → resource counts (Engines Registered, Available) → throughput stats (Request Rate, Success Rate, Avg Latency).
Timeseries: Pipeline State Over Time (multiple gauge queries overlaid).
Detail rows: one per pipeline stage (Ingestion, Dispatch, Engine Pool, Result Processing, Callback, System Health).

#### Validation / Quality Dashboard
Overview stats: Total Events → Invalid Ratio → Rejected % → Flagged %.
Sections per event source (SDK / Pixel): Total Issues → Avg Rate → Top 10 bar gauge → paired (pie + timeseries) for each dimension.

### 12. Incremental Dashboard Building — Avoid Large JSON

**NEVER send a full dashboard JSON in a single `update_dashboard` call** unless creating a brand-new empty dashboard skeleton. Large JSON payloads are expensive on context, error-prone, and hard to debug.

Instead, use **incremental patch operations** to build and modify dashboards piece by piece:

#### Creating a New Dashboard

1. Create a minimal skeleton first — just the title, description, tags, variables, and time range. No panels.
2. Confirm the skeleton tags include both normalized identity tags: `<project-name>` and `<application-name>`.
3. Append panels one row at a time using patch `add` operations.

```
Step 1: collect or infer the project name and application name, normalize them to lowercase hyphenated tags
Step 2: update_dashboard with minimal dashboard JSON (no panels, just metadata + templating), ensuring `tags` includes both identity tags plus any domain/purpose tags
Step 3: update_dashboard with uid + operations: [{"op": "add", "path": "$.panels/- ", "value": <row panel>}]
Step 4: update_dashboard with uid + operations: [{"op": "add", "path": "$.panels/- ", "value": <stat panel 1>}]
...repeat for each panel or small batch of panels
```

#### Modifying an Existing Dashboard

Use `uid` + `operations` (patch mode) to make targeted changes:

| Task | Patch operation |
|---|---|
| Change a panel title | `{"op": "replace", "path": "$.panels[2].title", "value": "New Title"}` |
| Update a query | `{"op": "replace", "path": "$.panels[2].targets[0].expr", "value": "new_promql{...}"}` |
| Add a panel at the end | `{"op": "add", "path": "$.panels/- ", "value": <panel JSON>}` |
| Remove a panel | `{"op": "remove", "path": "$.panels[5]"}` |
| Update dashboard description | `{"op": "replace", "path": "$.description", "value": "..."}` |
| Change time range | `{"op": "replace", "path": "$.time", "value": {"from": "now-6h", "to": "now"}}` |

#### Rules

- **Prefer multiple small patch calls over one large JSON call.** Each call should touch at most a few panels.
- When adding multiple panels, batch them into logical groups (e.g. all stat panels for one overview row in one call, then the timeseries row in the next call).
- Always use `get_dashboard_summary` or `get_dashboard_property` to inspect the current state before patching — don't guess panel indices.
- When removing multiple panels, the MCP auto-reorders indices to avoid shift issues, but still verify with `get_dashboard_summary` after bulk removes.

## Workflow

1. **Understand the requirement**: Ask the user what project and application the dashboard belongs to, what service/component it is for, what metrics are available, and what the monitoring goal is.
2. **Discover metrics**: Use `list_prometheus_metric_names` and `list_prometheus_label_values` to find available metrics and labels for the target service.
3. **Pick a dashboard pattern** from the categories above (or combine patterns).
4. **Build the required tag set**: Normalize the project name and application name into lowercase hyphenated tags, then add any extra domain/purpose tags needed for discoverability.
5. **Create the dashboard skeleton**: Use `update_dashboard` with a minimal JSON — title, description, tags, templating variables, time range. No panels yet. The `tags` array must include both the project tag and the application tag.
6. **Add panels incrementally**: Use `update_dashboard` with `uid` + `operations` (patch mode) to append panels row by row — overview stats first, then timeseries, then drill-down rows.
7. **Verify**: Use `get_dashboard_summary` to confirm the dashboard structure is correct, including the required identity tags.
8. **Share**: Use `generate_deeplink` to give the user a direct link.
