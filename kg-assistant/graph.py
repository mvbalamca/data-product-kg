from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

import re

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def clean_cypher_query(cypher_query: str) -> str:
    """
    Removes markdown formatting (triple backticks) and trims whitespace from the Cypher query.
    """
    # Remove triple backticks and any leading/trailing whitespace
    return re.sub(r"```+", "", cypher_query).strip()

def run_cypher(cypher_query: str) -> list:
    """
    Executes a Cypher query against Neo4j and returns results.
    """
    cleaned_query = clean_cypher_query(cypher_query)
    with driver.session() as session:
        result = session.run(cleaned_query)
        return [record.data() for record in result]