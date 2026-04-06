import os
import sqlite3
import argparse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "app.db")

def get_db_con():
    con = sqlite3.connect(DB_FILE)
    return con

def init_db():
    con = get_db_con()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            status TEXT,
            created_at TEXT,
            updated_at TEXT
        )    
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id INTEGER,
            title TEXT,
            description TEXT,
            status TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (entity_id) REFERENCES entities(id)
        )    
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id INTEGER,
            task_id INTEGER,
            title TEXT,
            description TEXT,
            created_at TEXT,
            FOREIGN KEY (entity_id) REFERENCES entities(id),
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )    
    """)

    con.commit()
    con.close()

class EntityManager:
    def add(self, name):
        con = get_db_con()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO entities (name, status, created_at) VALUES (?, ?, ?)",
            (name, "active", datetime.now().isoformat())
        )
        con.commit()
        con.close()
        print("Entity added")
    
    def list(self):
        con = get_db_con()
        cur = con.cursor()
        for row in cur.execute("SELECT id, name, status FROM entities"):
            print(row)
        con.close()

class TaskManager:
    def add(self, title, entity_id=None):
        con = get_db_con()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO tasks (title, status, entity_id, created_at) VALUES (?, ?, ?, ?)",
            (title, "todo", entity_id, datetime.now().isoformat())
        )
        con.commit()
        con.close()
        print("Task added")
    

    def list(self):
        con = get_db_con()
        cur = con.cursor()
        for row in cur.execute("SELECT id, title, status, entity_id FROM tasks"):
            print(row)
        con.close()

class EventManager:
    def add(self, entity_id, title):
        con = get_db_con()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO events (entity_id, title, created_at) VALUES (?, ?, ?)",
            (entity_id, title, datetime.now().isoformat())
        )
        con.commit()
        con.close()
        print("Event added")
    

    def list(self, entity_id):
        con = get_db_con()
        cur = con.cursor()
        for row in cur.execute("SELECT id, title, created_at FROM events WHERE entity_id = ?", (entity_id,)):
            print(row)
        con.close()

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init")
    
    entity_add = sub.add_parser("entity-add")
    entity_add.add_argument("name")
    sub.add_parser("entity-list")

    task_add = sub.add_parser("task-add")
    task_add.add_argument("title")
    task_add.add_argument("--entity", type=int)
    sub.add_parser("task-list")

    event_add = sub.add_parser("event-add")
    event_add.add_argument("entity_id", type=int)
    event_add.add_argument("title")
    event_list = sub.add_parser("event-list")
    event_list.add_argument("entity_id", type=int)

    args = parser.parse_args()

    em = EntityManager()
    tm = TaskManager()
    evm = EventManager()

    if args.cmd == "init":
        init_db()
        print("Database initiated")
    elif args.cmd == "entity-add":
        em.add(args.name)
    elif args.cmd == "entity-list":
        em.list()
    elif args.cmd == "task-add":
        tm.add(args.title, args.entity)
    elif args.cmd == "task-list":
        tm.list()
    elif args.cmd == "event-add":
        evm.add(args.entity_id, args.title)
    elif args.cmd == "event-list":
        evm.list(args.entity_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()