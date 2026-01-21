import os
import psycopg
from neo4j import GraphDatabase
import redis

PG_DSN = os.getenv("PG_DSN")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
REDIS_URL = os.getenv("REDIS_URL")

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def pg_conn():
    return psycopg.connect(PG_DSN)
