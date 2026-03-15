---
name: audit-sql
description: Perform a production-readiness SQL audit on MyBatis mapper XML files. Use when reviewing SQL queries, auditing database performance, checking index usage, analyzing locking risks, or reviewing mapper XML files for a Java/MyBatis project.
---

# SQL Audit Skill

## When to Activate

Activate this skill when the user asks to:

- Review SQL queries for production readiness
- Audit database performance or index usage
- Analyze locking risks or concurrency issues
- Review MyBatis mapper XML files
- Check SQL scalability for large datasets

## Hard Rule

- Audit ALL mapper XML files in the project — do not skip any.
- Every SQL statement must be checked against ALL review criteria below.
- Report findings with severity ratings — do not silently pass questionable queries.

## Instructions

1. **Discover the project structure:**
   - Search for DDL schema files (e.g., `*.sql` in `sqls/`, `db/`, `migration/`, `schema/`, or `src/main/resources/db/` directories) to understand all table definitions, indexes, partitions, and column types.
   - Search for all MyBatis mapper XML files (typically `*Mapper.xml` or `*.xml` in `**/resources/mapper/` or `**/resources/mybatis/` directories).
   - If no DDL schema files are found, infer table structures from the mapper XML files and any entity/model Java classes.
2. **Read and analyze** the DDL schema to understand table definitions, indexes, partitions, and column types.
3. **Read every MyBatis mapper XML** found in the project.
4. **Audit each SQL statement** against ALL of the criteria below.
5. **Produce a structured report** grouped by mapper file, with severity ratings.

## Review Criteria

### 1. Index Integrity
- Flag any `WHERE`, `JOIN`, or `ORDER BY` clause referencing columns that lack a supporting index.
- Detect **composite index misuse**: queries that skip the leftmost prefix of a composite index (e.g., querying on `col_b` alone when the index is `(col_a, col_b)`).
- Detect **Implicit Type Conversion**: parameter types that may differ from column types (e.g., passing a Java `Long` to a `VARCHAR` column, or `String` to `TINYINT`), which silently invalidates index usage.

### 2. Execution Plan Risks
- Identify patterns leading to **Full Table Scans**:
  - Leading wildcards: `LIKE '%abc'`
  - Functions applied to indexed columns: `WHERE YEAR(date_col) = 2024`, `WHERE DATE(created_at) = ...`
  - `OR` conditions that prevent index usage
  - `NOT IN` / `<>` / `!=` on indexed columns
- Flag `DATE_SUB(NOW(), INTERVAL ...)` or similar date function comparisons on indexed columns — confirm the function is applied to the constant side, not the column side.
- Flag queries missing `LIMIT` that could return unbounded result sets.

### 3. Concurrency & Locking
- Analyze **Batch Polling** queries (any SELECT used for polling pending/due/dispatched/timed-out rows) for:
  - Missing `FOR UPDATE SKIP LOCKED` or equivalent — concurrent pollers may claim the same rows.
  - Non-indexed `WHERE` conditions causing full-table lock scans.
  - `ORDER BY` on non-indexed columns under InnoDB row-level locking.
- Analyze **Retention Cleanup / Batch Delete** queries for:
  - Large `LIMIT` values that hold row locks for extended periods.
  - Missing index on the filter columns (e.g., `status` + `created_at` combination).
  - Potential deadlocks when concurrent deletes target overlapping row ranges.
- Flag any `UPDATE ... WHERE status = X` without an index on `status` (or the relevant composite).
- Flag blanket status-reset UPDATEs (e.g., `WHERE status = N` without additional filters) for lock contention risk.

### 4. Resource Pressure
- Flag **`SELECT *`** on tables with `TEXT`/`MEDIUMTEXT`/`BLOB`/`LONGTEXT` columns — these cause unnecessary I/O and memory pressure. Identify which columns are large-object types from the DDL schema.
- Flag **N+1 query patterns**: queries called per-item inside loops (check the Java mapper interfaces and service layer for loop-based calls).
- Flag **Offset-based pagination** on large datasets (`OFFSET N LIMIT M`) — recommend keyset/cursor pagination instead.
- Flag batch INSERT without size limits that could generate oversized SQL statements.

### 5. Scalability (Production Blocker Detection)
- For each query, evaluate: "Will this work at 1M+ rows?"
- Flag queries that perform:
  - **Correlated subqueries** or **subquery in DELETE/UPDATE** that may degrade to O(n²)
  - **Cartesian products** from missing JOIN conditions
  - **COUNT(*)** without a covering index
  - **Unbounded JOINs** between large tables without LIMIT
- Flag `DELETE ... WHERE id IN (SELECT ...)` anti-patterns — on MySQL this can cause issues with the same-table subquery limitation.
- Check **partition pruning**: if tables use partitioning, queries that don't filter by the partition key will scan all partitions.

## Report Format

For each finding, report:

```
### [SEVERITY] Finding Title
**Mapper:** FileName.xml → `<queryId>`
**Line:** approximate line in XML
**Issue:** Clear description of the problem
**Risk:** What happens in production (latency, locks, OOM, etc.)
**Recommendation:** Specific fix with code example if applicable
```

Severity levels:
- **CRITICAL** — Will cause outages or data corruption at scale. Must fix before production.
- **HIGH** — Significant performance degradation or locking issues under load.
- **MEDIUM** — Suboptimal but tolerable at moderate scale. Should fix soon.
- **LOW** — Minor optimization opportunity or best-practice deviation.

## Final Summary

End with:
1. A severity count table (CRITICAL / HIGH / MEDIUM / LOW)
2. Top 3 highest-priority fixes
3. Suggested composite indexes to add (with exact DDL)
4. Any schema-level recommendations (missing indexes, partition strategy improvements)
