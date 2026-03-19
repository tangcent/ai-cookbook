---
name: learn-from-mistakes
description: "Detect when the user is correcting the AI's approach or pointing out mistakes. Trigger phrases include 'you should', 'why not', 'that's wrong', 'use X instead', 'not like that', 'I said', 'no, do', 'wrong tool', 'wrong approach', 'I meant', 'actually', 'instead of', '不对', '应该用', '为什么不', '错了'. On activation, the AI reflects on what went wrong, identifies the correct approach, and logs the lesson to Obsidian for future reference."
---

# Learn From Mistakes Skill

## Purpose

Build a persistent, cross-tool knowledge base of AI mistakes and corrections. When the user corrects the AI (in any AI tool — Kiro, Cursor, Claude, Cline, etc.), this skill captures the context, analyzes what went wrong, and records the lesson in Obsidian. These records can feed back into any AI tool's context system, so the same mistakes don't repeat regardless of which tool is being used.

## When to Activate

Activate when the user's message contains correction signals:

- Direct corrections: "you should", "why not", "that's wrong", "not like that", "wrong tool", "wrong approach"
- Redirections: "use X instead", "I said", "no, do", "I meant", "actually, I wanted", "instead of"
- Frustration signals: "again?", "I already told you", "still wrong", "not what I asked"
- Chinese equivalents: "不对", "应该用", "为什么不", "错了", "我说的是", "不是这样"

**Principle: when in doubt, activate.** A false positive just means we reflect and find nothing to log. A false negative means we miss a learning opportunity.

## Workflow

### Step 1: Reflect and Summarize

Before doing anything else, pause and analyze:

1. **What did the user ask for?** — Restate the original intent.
2. **What did the AI do instead?** — Identify the specific action, tool, or approach that was wrong.
3. **Why was it wrong?** — Root cause: misunderstood intent? Wrong tool choice? Incorrect assumption? Ignored context?
4. **What's the correct approach?** — Based on the user's correction, state the right way.

Format this as a brief internal summary (do NOT dump this on the user — just acknowledge the correction naturally and move on).

### Step 2: Determine Tags

Build the tag set for this lesson. Every lesson gets the base tags, then add contextual tags based on analysis:

**Base tags (always applied):**

- `ai-lesson` — marks it as a lesson entry
- `ai-mistake` — marks it as originating from a mistake

**Scope tags (pick one):**

- `scope/global` — lesson applies universally across all projects (e.g., "don't use editCode for single-line changes")
- `scope/project-<name>` — lesson is specific to a project (e.g., `scope/project-payment-gateway`). Use the project/repo name.

**Domain tags (pick all that apply):**

- `domain/api` — REST API, HTTP, endpoint design, request/response handling
- `domain/kafka` — Kafka producers, consumers, topics, message handling
- `domain/redis` — Redis caching, pub/sub, data structures
- `domain/mysql` — MySQL queries, schema, migrations, MyBatis
- `domain/mongodb` — MongoDB queries, aggregation, schema design
- `domain/elasticsearch` — ES queries, indexing, mapping
- `domain/docker` — Dockerfile, compose, container config
- `domain/k8s` — Kubernetes manifests, deployments, services
- `domain/git` — Git operations, branching, merging
- `domain/testing` — Unit tests, integration tests, test strategy
- `domain/config` — Configuration files, environment variables, properties
- `domain/security` — Auth, encryption, secrets, permissions
- `domain/performance` — Optimization, profiling, caching strategy
- `domain/ci-cd` — Pipelines, builds, deployments
- `domain/frontend` — UI, CSS, JavaScript, React, Vue
- `domain/infra` — Infrastructure, cloud, networking
- Add new `domain/<name>` tags as needed — don't limit to this list

**Error type tags (pick one):**

- `error/tool-choice` — used the wrong tool or command
- `error/intent-misread` — misunderstood what the user wanted
- `error/wrong-assumption` — made an incorrect assumption about the codebase or context
- `error/ignored-context` — had the right info but didn't use it
- `error/code-error` — generated incorrect or buggy code
- `error/workflow-error` — followed the wrong process or sequence

**AI tool tag (pick one):**

- `tool/kiro`, `tool/cursor`, `tool/claude`, `tool/cline`, `tool/copilot`, `tool/trae`, etc.
- This tracks which AI tool made the mistake — useful for spotting tool-specific patterns

### Step 3: Log to Obsidian

Create or append to an Obsidian note using the CLI:

**Note naming convention:** `AI-Lesson-<short-description>-YYYY-MM-DD`

- Use lowercase kebab-case for the description, 3-5 words max
- Examples: `AI-Lesson-wrong-mybatis-xml-edit-2025-01-15`, `AI-Lesson-missed-redis-cache-pattern-2025-03-20`
- One note per lesson (not grouped by day) — makes each lesson individually searchable and linkable

**Note structure:**

```markdown
---
tags:
  - ai-lesson
  - ai-mistake
  - <scope-tag>
  - <domain-tags>
  - <error-tag>
  - <tool-tag>
date: YYYY-MM-DD
---

# <Short Descriptive Title>

**Context:** <what the user was trying to do>
**Mistake:** <what the AI did wrong>
**Root Cause:** <why — one sentence>
**Correction:** <the right approach>
**Rule:** <distilled into a one-line rule for future reference>
```

The `Rule` field is key — it's the one-liner that gets promoted to steering files. Examples:
- "When modifying MyBatis XML, always check the corresponding Java mapper interface first"
- "For Redis cache invalidation in payment-gateway, use the event-driven pattern, not direct delete"
- "User says 'clean up' → lint/format only, not rewrite"

Use the Obsidian CLI to create:

```bash
obsidian create name="AI-Lesson-wrong-mybatis-xml-edit-2025-01-15" content="..." silent
```

### Step 4: Apply the Correction

After logging, immediately proceed with the correct approach the user indicated. Don't just log — fix it.

## Using the Lesson Records

### 1. Steering File Compilation (Recommended)

When the user asks "compile my AI lessons into steering", search and distill:

```bash
# All lessons
obsidian search query="tag:#ai-lesson" limit=50

# Project-specific lessons
obsidian search query="tag:#scope/project-payment-gateway" limit=20

# Domain-specific lessons
obsidian search query="tag:#domain/mysql" limit=20

# Global rules only
obsidian search query="tag:#scope/global" limit=30
```

Compile the `Rule` fields into the steering file, organized by domain:

```markdown
---
inclusion: always
---

# Lessons Learned

## Global Rules
- User says "clean up" → lint/format only, not rewrite
- For single-line changes, use strReplace, not editCode

## API Rules
- Always check existing error handling patterns before adding new ones

## MySQL / MyBatis Rules
- When modifying mapper XML, check the Java interface first
- Use `<if>` for optional WHERE clauses, not string concatenation

## Kafka Rules
- Consumer group IDs follow pattern: {service}-{topic}-consumer

## Redis Rules
- Cache keys follow pattern: {service}:{entity}:{id}
```

### 2. Cross-Tool Usage

The Obsidian vault is the single source of truth. Different AI tools can consume lessons through their own context mechanisms:

| AI Tool | How to Feed Lessons |
|---------|-------------------|
| Kiro | `.kiro/steering/lessons-learned.md` (auto-included) |
| Cursor | `.cursorrules` or `.cursor/rules/*.md` |
| Claude Code | `CLAUDE.md` or `.claude/rules/*.md` |
| Cline | `.clinerules` |
| Copilot | `.github/copilot-instructions.md` |

The compile step can target any of these formats. Ask: "compile lessons for cursor" or "compile lessons for claude".

### 3. Obsidian Base for Review

Create a `.base` file to browse and filter lessons:

```yaml
filters:
  and:
    - file.tags == "ai-lesson"
formulas:
  age: '(today() - date(date)).days'
views:
  - type: table
    name: "All Lessons"
    order:
      - file.name
      - tags
      - age
    groupBy:
      property: tags
      direction: ASC
  - type: table
    name: "By Domain"
    filters:
      and:
        - file.tags == "domain"
    order:
      - file.name
      - tags
```

### 4. Pre-Flight Context (Advanced)

Set up a hook on `promptSubmit` to search past lessons before the AI starts working. This gives the AI relevant past mistakes as context for the current task.

### 5. Periodic Review

Ask any of these to trigger review:
- "review my AI lessons"
- "compile lessons into steering"
- "compile lessons for cursor"
- "what mistakes do I keep making?"
- "show me mysql-related lessons"

## References

- Obsidian CLI: `obsidian help`
- Steering files: `.kiro/steering/*.md`
