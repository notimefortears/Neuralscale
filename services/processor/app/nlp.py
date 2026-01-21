"""
We start with a strong baseline: HuggingFace NER + a heuristic severity score.
Later steps will add:
- event extraction (TTPs)
- topic modeling
- malware/vuln linking
- temporal trend detection
"""
from transformers import pipeline

class NLPEngine:
    def __init__(self):
        # Lightweight NER model. You can swap to DeBERTa or a cyber-finetuned model later.
        self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    def extract(self, text: str) -> list[dict]:
        ents = self.ner(text)
        out = []
        for e in ents:
            out.append({"label": e.get("entity_group"), "text": e.get("word"), "score": float(e.get("score", 0.0))})
        return out

    def severity(self, text: str) -> float:
        t = text.lower()
        score = 0.2
        if "rce" in t or "remote code" in t: score += 0.35
        if "auth bypass" in t: score += 0.25
        if "exploitation" in t or "weaponized" in t: score += 0.2
        if "patch" in t or "asap" in t: score += 0.1
        return max(0.0, min(1.0, score))
