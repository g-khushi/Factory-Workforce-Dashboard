from neo4j import GraphDatabase
import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path

# ---------------- LOAD ENV ----------------
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

print("URI:", URI)
print("USER:", USER)
print("PASSWORD:", PASSWORD)

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# ---------------- CONSTRAINTS ----------------
def create_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Project) REQUIRE p.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Station) REQUIRE s.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (w:Worker) REQUIRE w.id IS UNIQUE")
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (wk:Week) REQUIRE wk.id IS UNIQUE")


# ---------------- LOAD WORKERS ----------------
def load_workers(tx):
    df = pd.read_csv("factory_workers.csv")

    for _, row in df.iterrows():
        tx.run("""
            MERGE (w:Worker {id:$id})
            SET w.name=$name,
                w.role=$role,
                w.type=$type

            MERGE (s:Station {id:$station})
            MERGE (w)-[:WORKS_AT]->(s)
        """,
        id=row["worker_id"],
        name=row["name"],
        role=row["role"],
        type=row["type"],
        station=str(row["primary_station"])
        )


# ---------------- LOAD PRODUCTION ----------------
def load_production(tx):
    df = pd.read_csv("factory_production.csv")

    for _, row in df.iterrows():
        tx.run("""
            MERGE (p:Project {id:$pid})
            MERGE (s:Station {id:$sid})
            MERGE (wk:Week {id:$week})

            MERGE (p)-[r:SCHEDULED_AT]->(s)
            SET r.planned_hours=$planned,
                r.actual_hours=$actual,
                r.week=$week

            MERGE (p)-[:SCHEDULED_IN]->(wk)
        """,
        pid=row["project_id"],
        sid=str(row["station_code"]),
        week=row["week"],
        planned=row["planned_hours"],
        actual=row["actual_hours"]
        )


# ---------------- LOAD CAPACITY ----------------
def load_capacity(tx):
    df = pd.read_csv("factory_capacity.csv")

    for _, row in df.iterrows():
        tx.run("""
            MERGE (wk:Week {id:$week})
            MERGE (c:Capacity {week:$week})

            SET c.total_capacity=$cap,
                c.total_planned=$planned,
                c.deficit=$deficit

            MERGE (wk)-[:HAS_CAPACITY]->(c)
        """,
        week=row["week"],
        cap=row["total_capacity"],
        planned=row["total_planned"],
        deficit=row["deficit"]
        )


# ---------------- MAIN ----------------
def main():
    with driver.session() as session:
        session.execute_write(create_constraints)
        session.execute_write(load_workers)
        session.execute_write(load_production)
        session.execute_write(load_capacity)

    driver.close()
    print("✅ Graph Loaded Successfully!")


if __name__ == "__main__":
    main()