---
name: mysql-cli
description: Query, modify, and inspect MySQL databases via mysql-cli, a smart wrapper that supports multiple instances, auto-routes by table name, caches metadata, and executes .sql files. Use when the user asks to query MySQL, modify tables/data, check schemas, run SQL files, or verify database content.
---

# MySQL CLI Skill

## When to Activate

Activate this skill when the user asks to:

- Query MySQL data (e.g. "check the orders table")
- Modify data (INSERT, UPDATE, DELETE)
- Change table structure (ALTER TABLE, CREATE TABLE, etc.)
- Execute a .sql file against a database
- Inspect table structure or schema
- Verify data after code changes or deployments
- Browse databases or tables across MySQL instances

## Prerequisites

- `mysql` client must be installed and available in PATH.
- Config file `~/.mysql-instances.cnf` stores all instance credentials.
  - On first run, mysql-cli auto-creates this file with commented examples.
  - If the file has no `[instance]` sections, mysql-cli exits with guidance to edit it.
- Invoke the CLI as `scripts/mysql-cli`.

## Hard Rule

For MySQL tasks, **always use `mysql-cli`**.

- Do **not** invoke `mysql` directly — always go through the wrapper.
- Do **not** use browser automation for database inspection.
- Do **not** hardcode connection details in commands — they come from `~/.mysql-instances.cnf`.

## Config Setup

Config lives at `~/.mysql-instances.cnf` (INI format, auto-created with `chmod 600`):

```ini
[prod-master]
host=10.0.1.100
port=3306
user=readonly
password=secret
charset=utf8mb4
databases=app_db,log_db    # optional: restrict scanned databases

[test-db]
host=10.0.2.50
port=3306
user=root
password=root123
```

Each `[section]` is an instance name used with `--instance`.

## How mysql-cli Works

### Metadata Cache

On first use, mysql-cli connects to all configured instances and builds a local cache of databases and tables (stored in `.metadata/`). This enables automatic routing.

- Cache refreshes automatically when a queried table is not found.
- Manual refresh: `scripts/mysql-cli refresh`
- After `CREATE TABLE` or `DROP TABLE`, run `refresh` so the cache picks up the change.

### Auto-Routing

mysql-cli extracts table names from SQL, looks them up in the metadata cache, and connects to the correct instance and database automatically.

- Table found in exactly one place → auto-routes silently.
- Table found in multiple places → prints locations and asks user to specify `--instance` and/or `--db`.
- Table not found → auto-refreshes metadata and retries. If still not found, errors out.

### Routing Info

mysql-cli prints the resolved target to stderr:
```
[mysql-cli] → audit-gateway / audit_gateway
```
This does not pollute stdout, so `--format json` output is clean and safe for programmatic use.

## Command Reference

### List configured instances

```bash
scripts/mysql-cli instances
```

### List databases

```bash
scripts/mysql-cli dbs
scripts/mysql-cli dbs --instance prod-master
```

### List tables

```bash
scripts/mysql-cli tables
scripts/mysql-cli tables --instance prod-master
scripts/mysql-cli tables --instance prod-master --db app_db
```

### Refresh metadata cache

```bash
scripts/mysql-cli refresh
scripts/mysql-cli refresh --instance prod-master
```

### Describe a table (auto-routed)

```bash
scripts/mysql-cli desc user_order
scripts/mysql-cli desc user_order --instance prod-master
```

### Execute SQL — `exec` (any SQL: SELECT, DDL, DML)

```bash
# SELECT with auto-routing
scripts/mysql-cli exec "SELECT * FROM user_order WHERE id = 123"
scripts/mysql-cli exec "SELECT * FROM user_order ORDER BY created_at DESC" --limit 20

# INSERT / UPDATE / DELETE
scripts/mysql-cli exec "INSERT INTO user_order (user_id, status) VALUES (1, 'pending')"
scripts/mysql-cli exec "UPDATE user_order SET status = 'shipped' WHERE id = 123"
scripts/mysql-cli exec "DELETE FROM user_order WHERE status = 'cancelled' AND created_at < '2025-01-01'"

# DDL — use --instance and --db for CREATE TABLE (table not yet in cache)
scripts/mysql-cli exec "CREATE TABLE test_tbl (id INT PRIMARY KEY, name VARCHAR(50))" --instance prod-master --db app_db
scripts/mysql-cli exec "ALTER TABLE user_order ADD COLUMN tracking_no VARCHAR(64) DEFAULT NULL"
scripts/mysql-cli exec "CREATE INDEX idx_status_created ON user_order (status, created_at)"
scripts/mysql-cli exec "DROP TABLE test_tbl"
```

> `query` is accepted as an alias for `exec`.

### Execute a .sql file — `file`

```bash
scripts/mysql-cli file migration.sql
scripts/mysql-cli file scripts/init-data.sql --instance test-db --db app_db
```

The `file` command reads the .sql content to resolve the target, then pipes the entire file to mysql. Use `--instance`/`--db` when the file creates new tables that aren't in the cache yet.

### Force instance/database

```bash
scripts/mysql-cli exec "SELECT 1" --instance prod-master --db app_db
```

### Output formats

```bash
scripts/mysql-cli exec "SELECT * FROM user_order LIMIT 5" --format json
scripts/mysql-cli exec "SELECT * FROM user_order LIMIT 5" --format csv
scripts/mysql-cli exec "SELECT * FROM user_order LIMIT 1" --vertical
```

Prefer `--format json` when results will be inspected programmatically or reported to the user in a structured way.

### Dry run (show command without executing)

```bash
scripts/mysql-cli exec "SELECT * FROM user_order" --dry-run
```

## Workflow: Verify Data After Changes

1. Run the query — let mysql-cli auto-route:
   ```bash
   scripts/mysql-cli exec "SELECT * FROM <table> WHERE <condition>" --limit 20 --format json
   ```
2. If table not found, mysql-cli auto-refreshes metadata and retries. If still not found, ask the user to confirm the table name.
3. If multiple matches, show the user the options and ask which instance/db to use.
4. Inspect results and report findings.

## Workflow: Execute DDL/DML

1. For write operations (INSERT/UPDATE/DELETE/ALTER/DROP), **confirm the intent with the user before executing**.
2. For `CREATE TABLE`, always provide `--instance` and `--db` (the table doesn't exist in cache yet).
3. Run via `exec`:
   ```bash
   scripts/mysql-cli exec "<sql>"
   ```
4. For bulk changes, prefer using a `.sql` file:
   ```bash
   scripts/mysql-cli file changes.sql --instance <name> --db <database>
   ```
5. After creating or dropping tables, run `refresh` to update the cache:
   ```bash
   scripts/mysql-cli refresh
   ```

## Troubleshooting

- **"Config file not found. Creating..."** → First run. Edit `~/.mysql-instances.cnf` and add at least one instance.
- **"Config file is empty or has no instances"** → Add at least one `[instance]` section to `~/.mysql-instances.cnf`.
- **"Cannot connect to instance"** → Check host/port/credentials in config. Verify network access.
- **"Table not found in any instance/database"** → Run `scripts/mysql-cli refresh` then retry. If the table is brand new (just created), refresh is required. If still not found, confirm the exact table name with the user.
- **"Table found in multiple locations"** → Add `--instance <name>` and/or `--db <database>` to disambiguate.
- **Permission errors on exec** → The configured user may lack privileges (e.g. read-only user can't INSERT). Update `~/.mysql-instances.cnf` with a user that has the required permissions.
