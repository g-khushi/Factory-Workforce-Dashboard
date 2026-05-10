from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv(dotenv_path=".env")

# Read environment variables
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# DEBUG CHECK
print("URI:", URI)
print("USER:", USER)
print("PASSWORD:", PASSWORD)

# Neo4j connection
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# -----------------------------------
# Overworked Workers Query
# -----------------------------------
def get_overworked_workers():

    query = """
    MATCH (w:Worker)
    RETURN w.name AS name
    LIMIT 10
    """

    with driver.session() as session:
        result = session.run(query)

        workers = []

        for record in result:
            workers.append({
                "name": record["name"]
            })

        return workers
# -----------------------------------
# Project Capacity Query
# -----------------------------------
def get_project_capacity():

    query = """
    MATCH (p:Project)
    RETURN p.id AS project
    """

    with driver.session() as session:
        result = session.run(query)

        projects = []

        for record in result:
            projects.append({
                "project": record["project"]
            })

        return projects