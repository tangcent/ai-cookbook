#!/usr/bin/env python3
"""Deterministic helpers for spec-driven artifacts.

Replaces the read-count-edit-verify loops the model would otherwise run by hand.
Standard library only; no third-party dependencies.

Subcommands:
  status <spec>                 artifact inventory, requirement/task counts, checkbox progress
  dag <spec>                    dependency graph over unchecked tasks + parallel groups
  done <spec> <id>              check off a task (and its sub-tasks) in place
  trace <spec>                  task references <-> requirement acceptance criteria
  check <spec>                  structural validation (index links, Files: lines, numbering)

Every subcommand accepts --spec-dir to point at a spec directory directly
(default: <cwd>/.spec/<spec>), and --json for machine-readable output.

Exit codes: 0 = clean, 1 = findings/error.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

TASK_LINE = re.compile(r"^(\s*)- \[([ xX])\](\*)?\s+(\d+(?:\.\d+)*)\.?\s+(.+)$")
FILES_LINE = re.compile(r"^\s*- Files:\s*(.+)$")
PHASE_LINE = re.compile(r"^###\s+Phase\s+(\d+)\s*:\s*(.+)$")
REQ_LINE = re.compile(r"^###\s+Requirement\s+(\d+)\s*:\s*(.+)$")
AC_HEADING = re.compile(r"^####\s+Acceptance\s+Criteria", re.IGNORECASE)
NUM_ITEM = re.compile(r"^\s*(\d+)\.\s+")
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")

ARTIFACT_GLOBS = ("requirements*.md", "design*.md", "tasks*.md", "plan.md", "review.md")


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def out(text=""):
    sys.stdout.write(str(text) + "\n")


def emit(payload, as_json, render_text):
    if as_json:
        out(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        render_text(payload)


def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read().splitlines()


def norm_module(value):
    """Normalize a module name for comparison: lowercase, alphanumeric only."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def module_from_filename(name, kind):
    """requirements-auth.md -> 'auth'; tasks.md -> ''."""
    stem = name[: -len(".md")] if name.endswith(".md") else name
    prefix = kind + "-"
    if stem.startswith(prefix):
        return stem[len(prefix):]
    return ""


def files_from_line(rest):
    """Parse the text after 'Files:' into a list of paths."""
    rest = rest.strip()
    if not rest:
        return []
    paths = re.findall(r"`([^`]+)`", rest)
    if not paths:
        plain = rest.strip("()").strip().lower()
        if plain == "none":
            return []
        paths = [p.strip().strip("`") for p in rest.split(",")]
    return [p.strip() for p in paths if p.strip() and p.strip().lower() != "none"]


# --------------------------------------------------------------------------- #
# spec location
# --------------------------------------------------------------------------- #

def resolve_spec_dir(args, workspace):
    if args.spec_dir:
        path = Path(args.spec_dir).resolve()
    elif args.spec:
        path = (Path(workspace) / ".spec" / args.spec).resolve()
    else:
        path = (Path(workspace) / ".spec").resolve()
    if not path.exists():
        raise SystemExit("error: spec directory not found: %s" % path)
    return path


def list_artifacts(spec_dir):
    found = {}
    for pattern in ARTIFACT_GLOBS:
        for path in sorted(spec_dir.glob(pattern)):
            found[path.name] = path
    return found


# --------------------------------------------------------------------------- #
# parsers
# --------------------------------------------------------------------------- #

def parse_task_file(path):
    """Parse one tasks/plan markdown file into an ordered task list."""
    lines = read_lines(path)
    kind = "tasks" if path.name.startswith("tasks") else "plan"
    module = module_from_filename(path.name, "tasks") if kind == "tasks" else ""
    tasks = []
    current = None
    phase = None
    in_exec_order = False
    exec_phase = 0
    module_order = {}
    section = ""

    for idx, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip().lower()
            in_exec_order = section.startswith("execution order")
            if section.startswith("tasks"):
                phase = None
            current = None
            continue

        if in_exec_order:
            heading = re.match(r"^###\s+Phase\s+(\d+)", line)
            if heading:
                exec_phase = int(heading.group(1))
            for target in MD_LINK.findall(line):
                if target[1].startswith("tasks-"):
                    module_order[module_from_filename(target[1], "tasks")] = exec_phase
            continue

        heading = PHASE_LINE.match(line)
        if heading:
            phase = int(heading.group(1))
            current = None
            continue

        match = TASK_LINE.match(line)
        if match:
            task_id = match.group(4)
            if "." not in task_id:
                current = {
                    "id": task_id,
                    "title": match.group(5).strip(),
                    "checked": match.group(2).lower() == "x",
                    "optional": bool(match.group(3)),
                    "files": None,
                    "phase": phase,
                    "lineno": idx,
                    "subs": [],
                    "refs": [],
                    "ref_owner": task_id,
                }
                tasks.append(current)
            elif current is not None:
                current["subs"].append({
                    "id": task_id,
                    "title": match.group(5).strip(),
                    "checked": match.group(2).lower() == "x",
                    "optional": bool(match.group(3)),
                })
                current["ref_owner"] = task_id
            continue

        fmatch = FILES_LINE.match(line)
        if fmatch and current is not None and current["files"] is None:
            current["files"] = files_from_line(fmatch.group(1))
            continue

        if current is not None and "_Requirements:" in line:
            ref_text = line.split("_Requirements:", 1)[1].strip()
            ref_text = ref_text.rstrip("_").strip()
            if ref_text:
                current["refs"].append({"owner": current["ref_owner"], "text": ref_text})

    for task in tasks:
        task["checkpoint"] = task["title"].lower().startswith("checkpoint")

    return {
        "file": path.name,
        "path": path,
        "module": module,
        "kind": kind,
        "tasks": tasks,
        "module_order": module_order,
    }


def parse_requirement_file(path):
    """Parse one requirements markdown file into requirement/acceptance-criteria structure."""
    lines = read_lines(path)
    module = module_from_filename(path.name, "requirements")
    reqs = {}
    current = None
    in_criteria = False

    for line in lines:
        if line.startswith("## "):
            current = None
            in_criteria = False
            continue
        if line.startswith("### "):
            match = REQ_LINE.match(line)
            if match:
                current = {"number": int(match.group(1)), "title": match.group(2).strip(), "criteria": []}
                reqs[current["number"]] = current
                in_criteria = False
            else:
                current = reqs.get(current["number"]) if current else None
                in_criteria = False
            continue
        if AC_HEADING.match(line):
            in_criteria = True
            continue
        if line.startswith("#### "):
            in_criteria = False
            continue
        if in_criteria and current is not None:
            item = NUM_ITEM.match(line)
            if item:
                current["criteria"].append(int(item.group(1)))

    return {"file": path.name, "module": module, "requirements": reqs}


# --------------------------------------------------------------------------- #
# status
# --------------------------------------------------------------------------- #

def collect_status(spec_dir):
    artifacts = list_artifacts(spec_dir)
    payload = {
        "spec": spec_dir.name,
        "dir": str(spec_dir),
        "artifacts": [],
        "requirements": [],
        "tasks": [],
    }
    for name, path in artifacts.items():
        payload["artifacts"].append({
            "file": name,
            "bytes": path.stat().st_size,
            "lines": len(read_lines(path)),
        })

    req_paths = sorted([p for p in artifacts.values() if p.name.startswith("requirements")])
    for path in req_paths:
        parsed = parse_requirement_file(path)
        payload["requirements"].append({
            "file": path.name,
            "module": parsed["module"],
            "requirements": len(parsed["requirements"]),
            "acceptance_criteria": sum(len(r["criteria"]) for r in parsed["requirements"].values()),
        })

    task_paths = sorted([p for p in artifacts.values() if p.name.startswith(("tasks", "plan"))])
    for path in task_paths:
        parsed = parse_task_file(path)
        top = len(parsed["tasks"])
        top_done = sum(1 for t in parsed["tasks"] if t["checked"])
        subs = sum(len(t["subs"]) for t in parsed["tasks"])
        subs_done = sum(1 for t in parsed["tasks"] for s in t["subs"] if s["checked"])
        phases = sorted({t["phase"] for t in parsed["tasks"] if t["phase"] is not None})
        next_task = next((t for t in parsed["tasks"] if not t["checked"]), None)
        payload["tasks"].append({
            "file": path.name,
            "module": parsed["module"],
            "top_level": {"total": top, "done": top_done},
            "sub_tasks": {"total": subs, "done": subs_done},
            "phases": len(phases),
            "checkpoints": sum(1 for t in parsed["tasks"] if t["checkpoint"]),
            "percent": round(100.0 * (top_done / top), 1) if top else 0.0,
            "next": {"id": next_task["id"], "title": next_task["title"]} if next_task else None,
        })

    payload["clean"] = not payload["tasks"] or all(
        t["top_level"]["done"] == t["top_level"]["total"] for t in payload["tasks"]
    )
    return payload


def render_status(payload):
    out("Spec: %s" % payload["spec"])
    out("Dir:  %s" % payload["dir"])
    out()
    out("Artifacts:")
    if not payload["artifacts"]:
        out("  (none)")
    for item in payload["artifacts"]:
        out("  %-32s %6d bytes  %4d lines" % (item["file"], item["bytes"], item["lines"]))
    out()
    out("Requirements:")
    if not payload["requirements"]:
        out("  (none)")
    for item in payload["requirements"]:
        label = item["module"] or "(master)"
        out("  %-32s %-12s %d requirements, %d acceptance criteria"
            % (item["file"], label, item["requirements"], item["acceptance_criteria"]))
    out()
    out("Progress:")
    if not payload["tasks"]:
        out("  (no task files)")
    for item in payload["tasks"]:
        out("  %-32s tasks %d/%d (%.1f%%)  sub-tasks %d/%d  phases %d  checkpoints %d"
            % (item["file"], item["top_level"]["done"], item["top_level"]["total"], item["percent"],
               item["sub_tasks"]["done"], item["sub_tasks"]["total"], item["phases"], item["checkpoints"]))
        if item["next"]:
            out("  %-32s next: %s. %s" % ("", item["next"]["id"], item["next"]["title"]))
    out()
    out("State: %s" % ("complete" if payload["clean"] else "in progress"))


# --------------------------------------------------------------------------- #
# dag
# --------------------------------------------------------------------------- #

def build_dag(spec_dir):
    artifacts = list_artifacts(spec_dir)
    task_paths = [p for name, p in sorted(artifacts.items()) if p.name.startswith(("tasks", "plan"))]
    if not task_paths:
        return {"spec": spec_dir.name, "nodes": [], "rounds": [], "error": "no task files found"}

    parsed_files = [parse_task_file(p) for p in task_paths]
    master = next((p for p in parsed_files if p["file"] in ("tasks.md", "plan.md")), parsed_files[0])
    parsed_files = [master] + [p for p in parsed_files if p is not master]
    serial_fallback = master["kind"] == "plan"

    master_order = dict(master["module_order"])
    nodes = []
    for parsed in parsed_files:
        file_phase = master_order.get(parsed["module"]) if parsed["module"] else 0
        for order, task in enumerate(parsed["tasks"]):
            if task["checked"]:
                continue
            if task["files"] is None and not task["checkpoint"]:
                serial_fallback = True
            nodes.append({
                "id": task["id"],
                "file": parsed["file"],
                "module": parsed["module"],
                "title": task["title"],
                "files": sorted(task["files"] or []),
                "declared": task["files"] is not None,
                "phase": task["phase"],
                "module_phase": file_phase,
                "checkpoint": task["checkpoint"],
                "order": order,
                "deps": [],
            })

    def key_of(node):
        return (node["file"], node["id"])

    # file conflicts: earlier task in the same file wins
    by_file = {}
    for node in nodes:
        by_file.setdefault(node["file"], []).append(node)

    for nodes_in_file in by_file.values():
        for i, later in enumerate(nodes_in_file):
            for earlier in nodes_in_file[:i]:
                if set(later["files"]) & set(earlier["files"]):
                    later["deps"].append(key_of(earlier))

    # phase barriers inside a file: later phases wait for every earlier phase
    for nodes_in_file in by_file.values():
        for node in nodes_in_file:
            if node["phase"] is None:
                continue
            for other in nodes_in_file:
                if other is node or other["phase"] is None:
                    continue
                if other["phase"] < node["phase"]:
                    node["deps"].append(key_of(other))

    # checkpoint barriers inside a file: a checkpoint waits for the work before it,
    # and anything after a checkpoint waits for that checkpoint.
    # Indexes must come from the unchecked-node list, not from the task's position
    # in the full file (checked-off tasks are absent from this list).
    for nodes_in_file in by_file.values():
        checkpoints = [(index, node) for index, node in enumerate(nodes_in_file) if node["checkpoint"]]
        for index, node in enumerate(nodes_in_file):
            for cp_index, cp in checkpoints:
                if cp_index < index and key_of(cp) not in node["deps"]:
                    node["deps"].append(key_of(cp))
        for cp_index, cp in checkpoints:
            for earlier in nodes_in_file[:cp_index]:
                if key_of(earlier) not in cp["deps"]:
                    cp["deps"].append(key_of(earlier))

    # cross-module ordering from the master "Execution Order" table
    for node in nodes:
        if not node["module"] or node["module_phase"] is None:
            continue
        for other in nodes:
            if other["module"] == node["module"] or other["module_phase"] is None:
                continue
            if other["module_phase"] < node["module_phase"]:
                node["deps"].append(key_of(other))

    # serial fallback: a task with no Files: line blocks everything after it in its file
    if serial_fallback:
        for nodes_in_file in by_file.values():
            blocker = None
            for node in nodes_in_file:
                if blocker is not None and key_of(blocker) not in node["deps"]:
                    node["deps"].append(key_of(blocker))
                if not node["declared"]:
                    blocker = node

    deps = {key_of(n): set(n["deps"]) for n in nodes}
    depth = {}

    def compute_depth(node, stack=None):
        key = key_of(node)
        if key in depth:
            return depth[key]
        stack = stack or set()
        if key in stack:
            return 0  # cycle guard; check() reports cycles separately
        stack.add(key)
        deepest = 0
        for dep in deps[key]:
            target = next((n for n in nodes if key_of(n) == dep), None)
            if target is not None:
                deepest = max(deepest, compute_depth(target, stack))
        stack.discard(key)
        depth[key] = deepest + 1
        return depth[key]

    for node in nodes:
        compute_depth(node)

    # simulate the schedule: each round runs everything whose deps are satisfied
    done = set()
    remaining = list(nodes)
    rounds = []
    round_no = 0
    blocked = False
    while remaining and round_no < 200:
        round_no += 1
        ready = [n for n in remaining if deps[key_of(n)] <= done]
        if not ready:
            blocked = True
            rounds.append({"round": round_no, "blocked": [n["id"] for n in remaining]})
            break
        batches = []
        for node in ready:
            if not node["files"] or node["checkpoint"]:
                batches.append([node])
                continue
            placed = False
            for batch in batches:
                batch_files = set()
                for member in batch:
                    batch_files |= set(member["files"])
                if batch_files and not (batch_files & set(node["files"])):
                    batch.append(node)
                    placed = True
                    break
            if not placed:
                batches.append([node])
        rounds.append({
            "round": round_no,
            "batches": [[{
                "id": n["id"],
                "file": n["file"],
                "title": n["title"],
                "files": n["files"],
                "checkpoint": n["checkpoint"],
            } for n in batch] for batch in batches],
        })
        for node in ready:
            done.add(key_of(node))
            remaining.remove(node)

    for node in nodes:
        node["depth"] = depth.get(key_of(node), 1)

    return {
        "spec": spec_dir.name,
        "serial_fallback": serial_fallback,
        "blocked": blocked,
        "pending": len(nodes),
        "rounds": rounds,
        "nodes": nodes,
    }


def render_dag(payload):
    out("Spec: %s" % payload["spec"])
    if payload.get("error"):
        out("error: %s" % payload["error"])
        return
    out("Pending tasks: %d" % payload["pending"])
    if payload["serial_fallback"]:
        out("Note: serial fallback active (plan.md or a task is missing a Files: line)")
    out()
    total_parallel = 0
    for rd in payload["rounds"]:
        if rd.get("blocked"):
            out("Round %d: BLOCKED -> %s" % (rd["round"], ", ".join(rd["blocked"])))
            out("  (dependency cycle or unsatisfiable dependency; inspect the task list)")
            continue
        out("Round %d" % rd["round"])
        for i, batch in enumerate(rd["batches"], 1):
            if len(batch) > 1:
                total_parallel += len(batch) - 1
                out("  Parallel batch %d" % i)
            else:
                out("  Sequential")
            for node in batch:
                tag = " [checkpoint]" if node["checkpoint"] else ""
                files = ", ".join(node["files"]) if node["files"] else "no files"
                out("    - %s. %s%s  (%s)" % (node["id"], node["title"], tag, files))
        out()
    out("Parallelism gained: %d task(s) dispatched concurrently" % total_parallel)


# --------------------------------------------------------------------------- #
# done
# --------------------------------------------------------------------------- #

def find_task_file(spec_dir, module, task_id):
    artifacts = list_artifacts(spec_dir)
    candidates = []
    for name, path in artifacts.items():
        if not name.startswith(("tasks", "plan")):
            continue
        if module:
            if norm_module(module_from_filename(name, "tasks")) != norm_module(module) \
                    and norm_module(name) != norm_module(module):
                continue
        parsed = parse_task_file(path)
        for task in parsed["tasks"]:
            if task["id"] == task_id:
                candidates.append((path, task))
            elif task_id.startswith(task["id"] + "."):
                candidates.append((path, task))
    if not candidates:
        return None, "no task with id '%s'%s" % (task_id, (" in module '%s'" % module) if module else "")
    files = {str(path) for path, _ in candidates}
    if len(files) > 1:
        listing = ", ".join("%s:%s" % (Path(p).name, t["id"]) for p, t in candidates)
        return None, "ambiguous task id '%s' (candidates: %s) — use <module>:%s" % (task_id, listing, task_id)
    return candidates[0][0], None


def check_off(spec_dir, module, task_id):
    path, error = find_task_file(spec_dir, module, task_id)
    if error:
        return None, error

    lines = read_lines(path)
    changed = []
    prefix = task_id + "."
    for idx, line in enumerate(lines):
        match = TASK_LINE.match(line)
        if not match:
            continue
        tid = match.group(4)
        if tid != task_id and not tid.startswith(prefix):
            continue
        if match.group(2).lower() == "x":
            continue
        lines[idx] = re.sub(r"- \[[ xX]\]", "- [x]", line, count=1)
        changed.append(tid)

    if not changed:
        return None, "task '%s' is already checked off in %s" % (task_id, path.name)

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"file": path.name, "task": task_id, "updated": changed}, None


# --------------------------------------------------------------------------- #
# trace
# --------------------------------------------------------------------------- #

REF_ITEM = re.compile(r"^(.*?)(\d+)(?:\.(\d+))?$")


def parse_reference(ref_text):
    """'Auth 2.1, 2.3' -> [('auth', 2, 1), ('auth', 2, 3)]; module None when omitted."""
    items = []
    last_module = None
    for raw in [chunk.strip() for chunk in ref_text.split(",") if chunk.strip()]:
        match = REF_ITEM.match(raw)
        if not match:
            items.append({"raw": raw, "module": None, "requirement": None, "criterion": None})
            continue
        module = match.group(1).strip().strip("[]") or last_module
        if module:
            last_module = module
        items.append({
            "raw": raw,
            "module": module,
            "requirement": int(match.group(2)),
            "criterion": int(match.group(3)) if match.group(3) else None,
        })
    return items


def collect_trace(spec_dir):
    artifacts = list_artifacts(spec_dir)
    req_files = [p for name, p in sorted(artifacts.items()) if name.startswith("requirements")]
    task_files = [p for name, p in sorted(artifacts.items()) if name.startswith(("tasks", "plan"))]

    registry = {}
    for path in req_files:
        parsed = parse_requirement_file(path)
        registry[norm_module(parsed["module"])] = parsed

    findings = {"unresolved": [], "uncovered": [], "references": [], "ambiguous": []}
    covered = set()

    for path in task_files:
        parsed = parse_task_file(path)
        task_module = norm_module(parsed["module"])
        for task in parsed["tasks"]:
            if not task["refs"]:
                continue
            for ref in task["refs"]:
                owner = ref["owner"]
                for item in parse_reference(ref["text"]):
                    findings["references"].append({"file": path.name, "task": owner, "ref": item["raw"]})
                    if item["requirement"] is None:
                        findings["unresolved"].append({
                            "file": path.name,
                            "task": owner,
                            "ref": item["raw"],
                            "reason": "not a requirement reference",
                        })
                        continue
                    target_module, problem = resolve_module(item["module"], task_module, registry, item["requirement"])
                    if problem == "ambiguous":
                        findings["ambiguous"].append({
                            "file": path.name,
                            "task": owner,
                            "ref": item["raw"],
                            "reason": "matches more than one requirements file",
                        })
                        continue
                    if problem:
                        findings["unresolved"].append({
                            "file": path.name,
                            "task": owner,
                            "ref": item["raw"],
                            "reason": problem,
                        })
                        continue
                    reqs = registry[target_module]["requirements"]
                    requirement = reqs.get(item["requirement"])
                    if requirement is None:
                        findings["unresolved"].append({
                            "file": path.name,
                            "task": owner,
                            "ref": item["raw"],
                            "reason": "requirement %d not found in %s"
                            % (item["requirement"], registry[target_module]["file"]),
                        })
                        continue
                    if item["criterion"] is None:
                        if requirement["criteria"]:
                            for crit in requirement["criteria"]:
                                covered.add((target_module, item["requirement"], crit))
                        else:
                            covered.add((target_module, item["requirement"], None))
                        continue
                    if requirement["criteria"] and item["criterion"] not in requirement["criteria"]:
                        findings["unresolved"].append({
                            "file": path.name,
                            "task": task["id"],
                            "ref": item["raw"],
                            "reason": "criterion %d.%d not found in %s"
                            % (item["requirement"], item["criterion"], registry[target_module]["file"]),
                        })
                        continue
                    covered.add((target_module, item["requirement"], item["criterion"]))

    for module_key, parsed in registry.items():
        for number, requirement in parsed["requirements"].items():
            criteria = requirement["criteria"] or [None]
            for crit in criteria:
                if (module_key, number, crit) not in covered:
                    findings["uncovered"].append({
                        "file": parsed["file"],
                        "module": parsed["module"],
                        "requirement": number,
                        "title": requirement["title"],
                        "criterion": crit,
                    })

    findings["clean"] = not (findings["unresolved"] or findings["uncovered"] or findings["ambiguous"])
    findings["covered_count"] = len(covered)
    findings["spec"] = spec_dir.name
    return findings


def resolve_module(module_raw, task_module, registry, requirement):
    if module_raw:
        key = norm_module(module_raw)
        if key in registry:
            return key, None
        matches = [k for k in registry if k and (k.startswith(key) or key.startswith(k))]
        if len(matches) == 1:
            return matches[0], None
        return None, "no requirements file for module '%s'" % module_raw

    if task_module and task_module in registry:
        return task_module, None
    if "" in registry and requirement in registry[""]["requirements"]:
        return "", None

    matches = [k for k in registry if requirement in registry[k]["requirements"]]
    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, "ambiguous"
    return None, "requirement %d not found in any requirements file" % requirement


def render_trace(payload):
    out("Spec: %s" % payload["spec"])
    out("References: %d   Covered acceptance criteria: %d" % (len(payload["references"]), payload["covered_count"]))
    out()
    if not payload["unresolved"] and not payload["ambiguous"] and not payload["uncovered"]:
        out("Traceability: clean")
        return
    if payload["unresolved"]:
        out("Unresolved references:")
        for item in payload["unresolved"]:
            out("  %s task %s -> \"%s\": %s" % (item["file"], item["task"], item["ref"], item["reason"]))
        out()
    if payload["ambiguous"]:
        out("Ambiguous references:")
        for item in payload["ambiguous"]:
            out("  %s task %s -> \"%s\": %s" % (item["file"], item["task"], item["ref"], item["reason"]))
        out()
    if payload["uncovered"]:
        out("Uncovered acceptance criteria:")
        for item in payload["uncovered"]:
            where = "%s Requirement %d" % (item["file"], item["requirement"])
            if item["criterion"] is not None:
                where += " criterion %d" % item["criterion"]
            out("  %s — %s" % (where, item["title"]))
        out()


# --------------------------------------------------------------------------- #
# check
# --------------------------------------------------------------------------- #

def collect_check(spec_dir, workspace, check_paths):
    artifacts = list_artifacts(spec_dir)
    findings = []

    # 1. internal markdown links resolve
    for name, path in artifacts.items():
        for lineno, line in enumerate(read_lines(path), 1):
            for text, target in MD_LINK.findall(line):
                if target.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                target = target.split("#", 1)[0]
                if not target or not target.endswith(".md"):
                    continue
                if not (spec_dir / target).exists():
                    findings.append({
                        "kind": "broken-link",
                        "file": name,
                        "line": lineno,
                        "detail": "link target '%s' does not exist in %s" % (target, spec_dir.name),
                    })

    # 2. top-level tasks must declare a Files: line (tasks files only)
    for name, path in artifacts.items():
        if not name.startswith("tasks"):
            continue
        parsed = parse_task_file(path)
        for task in parsed["tasks"]:
            if task["files"] is None:
                findings.append({
                    "kind": "missing-files-line",
                    "file": name,
                    "line": task["lineno"] + 1,
                    "detail": "task %s has no Files: line" % task["id"],
                })

    # 3. numbering continuity
    for name, path in artifacts.items():
        if not name.startswith(("tasks", "plan")):
            continue
        parsed = parse_task_file(path)
        expected = 1
        for task in parsed["tasks"]:
            if int(task["id"]) != expected:
                findings.append({
                    "kind": "numbering",
                    "file": name,
                    "line": task["lineno"] + 1,
                    "detail": "top-level task numbering jumps: expected %d, found %s" % (expected, task["id"]),
                })
                expected = int(task["id"]) + 1
            else:
                expected += 1
        for task in parsed["tasks"]:
            expected_sub = 1
            for sub in task["subs"]:
                if not sub["id"].startswith(task["id"] + "."):
                    findings.append({
                        "kind": "numbering",
                        "file": name,
                        "line": task["lineno"] + 1,
                        "detail": "sub-task %s does not belong to task %s" % (sub["id"], task["id"]),
                    })
                    continue
                tail = int(sub["id"].rsplit(".", 1)[1])
                if tail != expected_sub:
                    findings.append({
                        "kind": "numbering",
                        "file": name,
                        "line": task["lineno"] + 1,
                        "detail": "sub-task numbering in task %s jumps: expected %s.%d, found %s"
                        % (task["id"], task["id"], expected_sub, sub["id"]),
                    })
                expected_sub = tail + 1

    # 4. optional reference paths exist
    if check_paths:
        seen = set()
        for name, path in artifacts.items():
            if not name.startswith(("tasks", "plan")):
                continue
            parsed = parse_task_file(path)
            for task in parsed["tasks"]:
                for target in (task["files"] or []):
                    if target in seen:
                        continue
                    seen.add(target)
                    if not (Path(workspace) / target).exists():
                        findings.append({
                            "kind": "missing-path",
                            "file": name,
                            "line": task["lineno"] + 1,
                            "detail": "task %s references missing path '%s'" % (task["id"], target),
                        })

    return {
        "spec": spec_dir.name,
        "checked_paths": bool(check_paths),
        "findings": findings,
        "clean": not findings,
    }


def render_check(payload):
    out("Spec: %s" % payload["spec"])
    if payload["clean"]:
        out("Structure: clean%s" % (" (paths verified)" if payload["checked_paths"] else ""))
        return
    out("Findings: %d" % len(payload["findings"]))
    out()
    for item in payload["findings"]:
        out("  [%s] %s:%d — %s" % (item["kind"], item["file"], item.get("line", 0), item["detail"]))
    out()


# --------------------------------------------------------------------------- #
# cli
# --------------------------------------------------------------------------- #

def extract_workspace(argv, default):
    """Allow --workspace anywhere on the command line, before or after the subcommand."""
    cleaned = []
    workspace = default
    index = 0
    while index < len(argv):
        item = argv[index]
        if item == "--workspace" and index + 1 < len(argv):
            workspace = argv[index + 1]
            index += 2
            continue
        if item.startswith("--workspace="):
            workspace = item.split("=", 1)[1]
            index += 1
            continue
        cleaned.append(item)
        index += 1
    return cleaned, workspace


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    raw_args = list(sys.argv[1:] if argv is None else argv)
    raw_args, workspace = extract_workspace(raw_args, os.getcwd())

    parser = argparse.ArgumentParser(
        prog="spec_tools.py",
        description="Deterministic helpers for spec-driven artifacts (.spec/<name>/).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (
        ("status", "artifact inventory and progress"),
        ("dag", "dependency graph and parallel groups"),
        ("trace", "task references vs acceptance criteria"),
        ("check", "structural validation"),
    ):
        cmd = sub.add_parser(name, help=help_text)
        cmd.add_argument("spec", nargs="?", help="spec name under .spec/")
        cmd.add_argument("--spec-dir", help="path to the spec directory")
        cmd.add_argument("--json", action="store_true", help="machine-readable output")
        if name == "check":
            cmd.add_argument("--paths", action="store_true", help="also verify Files: paths exist")
        cmd.set_defaults(handler=name)

    done_cmd = sub.add_parser("done", help="check off a task and its sub-tasks")
    done_cmd.add_argument("spec", nargs="?", help="spec name under .spec/")
    done_cmd.add_argument("id", help="task id: 3 | 3.1 | <module>:2")
    done_cmd.add_argument("--spec-dir", help="path to the spec directory")
    done_cmd.add_argument("--json", action="store_true")
    done_cmd.set_defaults(handler="done")

    args = parser.parse_args(raw_args)

    if not args.spec_dir and not args.spec:
        parser.error("provide a spec name or --spec-dir")

    spec_dir = resolve_spec_dir(args, workspace)

    if args.handler == "status":
        payload = collect_status(spec_dir)
        emit(payload, args.json, render_status)
        return 0

    if args.handler == "dag":
        payload = build_dag(spec_dir)
        emit(payload, args.json, render_dag)
        return 1 if (payload.get("error") or payload.get("blocked")) else 0

    if args.handler == "trace":
        payload = collect_trace(spec_dir)
        emit(payload, args.json, render_trace)
        return 0 if payload["clean"] else 1

    if args.handler == "check":
        payload = collect_check(spec_dir, workspace, args.paths)
        emit(payload, args.json, render_check)
        return 0 if payload["clean"] else 1

    # done
    module = None
    task_id = args.id
    if ":" in args.id:
        module, task_id = args.id.split(":", 1)
    result, error = check_off(spec_dir, module, task_id)
    if error:
        if args.json:
            out(json.dumps({"ok": False, "error": error}, indent=2))
        else:
            out("error: %s" % error)
        return 1
    if args.json:
        out(json.dumps({"ok": True, **result}, indent=2))
    else:
        out("Checked off %s in %s: %s" % (result["task"], result["file"], ", ".join(result["updated"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
