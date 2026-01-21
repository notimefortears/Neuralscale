"""
Connectors are intentionally modular.
We start with a "public intel" connector that generates realistic events.
Next steps will add: NVD/CVE feed, RSS scrapers, Reddit, etc.
"""
from datetime import datetime, timezone
from .schemas import RawThreatEvent

SAMPLE_EVENTS = [
    ("Security Blog", "New RCE chain observed against exposed CI runners; attackers drop crypto-miner and steal env secrets."),
    ("CVE Watch", "CVE-2026-XXXX: auth bypass in popular gateway; exploitation chatter rising, patch recommended ASAP."),
    ("Threat Intel", "Phishing kit update adds MFA prompt relay and session token theft; targeting finance and SaaS admins."),
]

async def generate_events():
    now = datetime.now(timezone.utc)
    for src, txt in SAMPLE_EVENTS:
        yield RawThreatEvent(
            source=src,
            created_at=now,
            title=txt[:72],
            text=txt,
            url=None,
            meta={"confidence": 0.55},
        )
