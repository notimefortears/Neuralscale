from fastapi import APIRouter
from .db import pg_conn, neo4j_driver

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

@router.get("/events/recent")
def recent_events(limit: int = 25):
    q = "SELECT id, source, created_at, title, url, severity, entities FROM threat_events ORDER BY created_at DESC LIMIT %s;"
    with pg_conn() as conn:
        rows = conn.execute(q, (limit,)).fetchall()
    return [{"id": r[0], "source": r[1], "created_at": r[2], "title": r[3], "url": r[4], "severity": r[5], "entities": r[6]} for r in rows]

@router.get("/graph/top-entities")
def top_entities(limit: int = 15):
    cypher = """
    MATCH (e:ThreatEvent)-[:MENTIONS]->(n:Entity)
    RETURN n.label AS label, n.text AS text, count(*) AS c
    ORDER BY c DESC
    LIMIT $limit
    """
    with neo4j_driver.session() as s:
        res = s.run(cypher, limit=limit).data()
    return res
