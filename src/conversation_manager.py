"""
ConversationManager
- Manages conversation history and can compute conversation-level sentiment summary.
"""
from typing import List, Dict

class ConversationManager:
    def __init__(self):
        self.history = []  # list of tuples (speaker, text, analysis_dict)
    
    def add_user_message(self, text, analysis=None):
        self.history.append(("user", text, analysis))
    
    def add_bot_message(self, text):
        self.history.append(("bot", text, None))
    
    def get_history(self) -> List[Dict]:
        return [{"speaker": s, "text": t, "analysis": a} for (s,t,a) in self.history]
    
    def summary_sentiment(self):
        # Aggregate per-message scores from analysis dicts for user messages
        scores = [a["score"] for (_s, _t, a) in self.history if _s=="user" and a and isinstance(a.get("score", None), (int,float))]
        if not scores:
            return {"label":"Neutral","score":0.0,"detail":"No user messages."}
        total = sum(scores)
        avg = total / len(scores)
        # Determine overall label using same thresholds as analyzer
        if avg > 1.5:
            label = "Positive"
        elif avg < -1.5:
            label = "Negative"
        elif -0.75 <= avg <= 0.75:
            label = "Neutral"
        else:
            label = "Mixed"
        explanation = self._explain_label(label)
        return {"label": label, "score": round(avg,3), "messages_count": len(scores), "explanation": explanation}

    def _explain_label(self, label):
        # Provide user-friendly explanation phrases for the final label
        mapping = {
            "Positive": "positive engagement or satisfaction",
            "Negative": "general dissatisfaction",
            "Neutral": "neutral — no strong sentiment",
            "Mixed": "mixed feelings"
        }
        return mapping.get(label, "No summary available")
