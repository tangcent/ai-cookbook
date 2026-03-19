# Bases Functions Reference

## Global Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `date()` | `date(string): date` | Parse string to date (`YYYY-MM-DD HH:mm:ss`) |
| `duration()` | `duration(string): duration` | Parse duration string |
| `now()` | `now(): date` | Current date and time |
| `today()` | `today(): date` | Current date (time = 00:00:00) |
| `if()` | `if(condition, trueResult, falseResult?)` | Conditional |
| `min()` | `min(n1, n2, ...): number` | Smallest number |
| `max()` | `max(n1, n2, ...): number` | Largest number |
| `number()` | `number(any): number` | Convert to number |
| `link()` | `link(path, display?): Link` | Create a link |
| `list()` | `list(element): List` | Wrap in list if not already |
| `file()` | `file(path): file` | Get file object |
| `image()` | `image(path): image` | Create image for rendering |
| `icon()` | `icon(name): icon` | Lucide icon by name |
| `html()` | `html(string): html` | Render as HTML |
| `escapeHTML()` | `escapeHTML(string): string` | Escape HTML characters |

## Any Type

| Function | Description |
|----------|-------------|
| `any.isTruthy()` | Coerce to boolean |
| `any.isType(type)` | Check type |
| `any.toString()` | Convert to string |

## Date Functions & Fields

Fields: `date.year`, `date.month`, `date.day`, `date.hour`, `date.minute`, `date.second`, `date.millisecond`

| Function | Description |
|----------|-------------|
| `date.date()` | Remove time portion |
| `date.format(string)` | Format with Moment.js pattern |
| `date.time()` | Get time as string |
| `date.relative()` | Human-readable relative time |
| `date.isEmpty()` | Always false for dates |

## Duration Type

Subtracting two dates returns a Duration (not a number).

Fields: `.days`, `.hours`, `.minutes`, `.seconds`, `.milliseconds`

Duration does NOT support `.round()` directly. Access a numeric field first:

```yaml
# CORRECT
"(date(due_date) - today()).days"
"(now() - file.ctime).days.round(0)"

# WRONG
"(now() - file.ctime).round(0)"
```

### Date Arithmetic

```yaml
"now() + \"1 day\""       # Tomorrow
"today() + \"7d\""        # A week from today
"now() - file.ctime"      # Returns Duration
"(now() - file.ctime).days"  # Days as number
```

Duration units: `y/year/years`, `M/month/months`, `d/day/days`, `w/week/weeks`, `h/hour/hours`, `m/minute/minutes`, `s/second/seconds`


## String Functions

Field: `string.length`

| Function | Description |
|----------|-------------|
| `string.contains(value)` | Check substring |
| `string.containsAll(...values)` | All substrings present |
| `string.containsAny(...values)` | Any substring present |
| `string.startsWith(query)` | Starts with query |
| `string.endsWith(query)` | Ends with query |
| `string.isEmpty()` | Empty or not present |
| `string.lower()` | To lowercase |
| `string.title()` | To Title Case |
| `string.trim()` | Remove whitespace |
| `string.replace(pattern, replacement)` | Replace pattern |
| `string.repeat(count)` | Repeat string |
| `string.reverse()` | Reverse string |
| `string.slice(start, end?)` | Substring |
| `string.split(separator, n?)` | Split to list |

## Number Functions

| Function | Description |
|----------|-------------|
| `number.abs()` | Absolute value |
| `number.ceil()` | Round up |
| `number.floor()` | Round down |
| `number.round(digits?)` | Round to digits |
| `number.toFixed(precision)` | Fixed-point notation |
| `number.isEmpty()` | Not present |

## List Functions

Field: `list.length`

| Function | Description |
|----------|-------------|
| `list.contains(value)` | Element exists |
| `list.containsAll(...values)` | All elements exist |
| `list.containsAny(...values)` | Any element exists |
| `list.filter(expression)` | Filter by condition (uses `value`, `index`) |
| `list.map(expression)` | Transform elements (uses `value`, `index`) |
| `list.reduce(expression, initial)` | Reduce (uses `value`, `index`, `acc`) |
| `list.flat()` | Flatten nested lists |
| `list.join(separator)` | Join to string |
| `list.reverse()` | Reverse order |
| `list.slice(start, end?)` | Sublist |
| `list.sort()` | Sort ascending |
| `list.unique()` | Remove duplicates |
| `list.isEmpty()` | No elements |

## File Functions

| Function | Description |
|----------|-------------|
| `file.asLink(display?)` | Convert to link |
| `file.hasLink(otherFile)` | Has link to file |
| `file.hasTag(...tags)` | Has any of the tags |
| `file.hasProperty(name)` | Has property |
| `file.inFolder(folder)` | In folder or subfolder |

## Link Functions

| Function | Description |
|----------|-------------|
| `link.asFile()` | Get file object |
| `link.linksTo(file)` | Links to file |

## Object Functions

| Function | Description |
|----------|-------------|
| `object.isEmpty()` | No properties |
| `object.keys()` | List of keys |
| `object.values()` | List of values |

## Regular Expression Functions

| Function | Description |
|----------|-------------|
| `regexp.matches(string)` | Test if matches |
