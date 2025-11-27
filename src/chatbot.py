"""
Chatbot - ties together ConversationManager and SentimentAnalyzer
Generates responses based on per-message sentiment and supports end-of-conversation summary.
"""
from typing import Optional
from .sentiment_analyzer import SentimentAnalyzer

class Chatbot:
    def __init__(self, convo, analyzer: Optional[SentimentAnalyzer]=None):
        self.convo = convo
        self.analyzer = analyzer or SentimentAnalyzer()
    
    def generate_response(self, user_text: str) -> str:
        # Analyze the message
        analysis = self.analyzer.analyze_text(user_text)
        # Store user message with analysis
        self.convo.add_user_message(user_text, analysis)
        label = analysis.get("label", "Neutral")
        # Simple response logic
        if label == "Positive":
            resp = "I'm glad to hear that — thank you for the feedback."
        elif label == "Negative":
            resp = "I'll make sure your concern is addressed."
        elif label == "Mixed":
            resp = "I sense mixed feelings — tell me more so I can understand."
        else:
            resp = "Thanks for sharing."
        # Store bot response
        self.convo.add_bot_message(resp)
        return resp
    
    def end_conversation_summary(self):
        # Produce conversation-level sentiment summary
        summary = self.convo.summary_sentiment()
        lines = [
            f"Conversation summary: {summary['label']} (avg score {summary['score']})",
            f"Analyzed {summary.get('messages_count',0)} user messages."
        ]
        return "\\n".join(lines)
