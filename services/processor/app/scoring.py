def risk_score(event: dict) -> float:
    """
    Lightweight 'online' scoring function.
    You can later swap this with your real ML model scoring.
    """
    score = 0.0

    tactic = (event.get("tactic") or "").lower()
    amount = float(event.get("amount") or 0.0)
    channel = (event.get("channel") or "").lower()
    country = (event.get("country") or "").upper()

    if tactic in {"credential_access", "exfiltration", "command_and_control"}:
        score += 0.4
    if amount > 1500:
        score += 0.25
    if channel == "api":
        score += 0.15
    if country in {"BR", "RO"}:
        score += 0.10

    # clamp to [0, 1]
    if score < 0:
        score = 0.0
    if score > 1:
        score = 1.0
    return score
