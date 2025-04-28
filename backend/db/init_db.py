#!/usr/bin/env python3
"""
init_db.py ── bootstrap script for your local NeuralTask database

Usage:
    python init_db.py

The configuration is read from the .env file in the backend directory. Required variables:
    NEURATASK_DB ‑ target database name
    PGUSER       ‑ PostgreSQL super‑user / role with CREATEDB privilege
    PGPASSWORD   ‑ password for PGUSER
    PGHOST       ‑ host
    PGPORT       ‑ port

The script will:
  1. Create the database if it doesn't exist.
  2. Execute the SQL in the sibling file `schema.sql`.
  3. Run a tiny smoke‑test that inserts one user, one workspace, and one task, then queries them back.

Dependencies:
    pip install psycopg2‑binary python-dotenv
"""
from __future__ import annotations
import os
import sys
import pathlib
import textwrap
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql, errors
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters from environment variables
DB_NAME = os.getenv("NEURATASK_DB")
DB_USER = os.getenv("PGUSER")
DB_PWD = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT")

# Validate required environment variables
if not all([DB_NAME, DB_USER, DB_PWD, DB_HOST, DB_PORT]):
    sys.exit("❌ Missing required environment variables in .env file - aborting")

try:
    DB_PORT = int(DB_PORT)
except ValueError:
    sys.exit("❌ PGPORT must be a number")

SCHEMA = pathlib.Path(__file__).with_name("schema.sql")

if not SCHEMA.exists():
    sys.exit("❌ schema.sql file not found next to init_db.py — aborting")


def _connect(dbname: str) -> psycopg2.extensions.connection:
    return psycopg2.connect(
        dbname=dbname,
        user=DB_USER,
        password=DB_PWD,
        host=DB_HOST,
        port=DB_PORT,
    )


def create_database() -> None:
    """Create target DB unless it already exists."""
    con = _connect("postgres")  # connect to maintenance DB
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    try:
        cur.execute(sql.SQL("CREATE DATABASE {}".format(sql.Identifier(DB_NAME).string)))
        print(f"✅ Database '{DB_NAME}' created")
    except errors.DuplicateDatabase:
        print(f"ℹ️  Database '{DB_NAME}' already exists — skipping create")
    finally:
        cur.close(); con.close()


def apply_schema() -> None:
    with _connect(DB_NAME) as con, con.cursor() as cur:
        ddl = SCHEMA.read_text()
        cur.execute(ddl)
        con.commit()
        print("✅ Schema applied (extensions, tables, types, indexes)")


def smoke_test() -> None:
    sql_insert = textwrap.dedent(
        """
        INSERT INTO users (auth0_sub, name, email)
        VALUES ('auth0|demo', 'Jane Demo', 'jane@example.com')
        RETURNING id;"""
    )
    with _connect(DB_NAME) as con, con.cursor() as cur:
        # 1. user
        cur.execute(sql_insert)
        user_id = cur.fetchone()[0]
        # 2. workspace
        cur.execute("INSERT INTO workspaces (owner_id, name) VALUES (%s, 'Demo WS') RETURNING id;", (user_id,))
        ws_id = cur.fetchone()[0]
        # 3. project
        cur.execute("INSERT INTO projects (workspace_id, name) VALUES (%s, 'Inbox') RETURNING id;", (ws_id,))
        proj_id = cur.fetchone()[0]
        # 4. task
        cur.execute(
            "INSERT INTO tasks (project_id, title, created_by) VALUES (%s, 'Hello task!', %s) RETURNING id;",
            (proj_id, user_id),
        )
        task_id = cur.fetchone()[0]
        con.commit()
        # verify
        cur.execute("SELECT title, status, created_at FROM tasks WHERE id = %s;", (task_id,))
        row = cur.fetchone()
        print("🔍 Smoke‑test task:", json.dumps(dict(title=row[0], status=row[1], created_at=str(row[2])), indent=2))


def main():
    create_database()
    apply_schema()
    smoke_test()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted — goodbye!")
