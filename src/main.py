"""
Console entrypoint for the Sentiment Chatbot project.
Type messages and the bot will respond. Type "summary" to see conversation-level sentiment.
Type "exit" or Ctrl+C to quit.
"""
from .conversation_manager import ConversationManager
from .sentiment_analyzer import SentimentAnalyzer
from .chatbot import Chatbot

def main():
    convo = ConversationManager()
    analyzer = SentimentAnalyzer()
    bot = Chatbot(convo, analyzer)
    print("Sentiment Chatbot (type 'summary' to see conversation-level sentiment, 'exit' to quit)")
    try:
        while True:
            user = input("You: ").strip()
            if not user:
                continue
            if user.lower() in {"exit","quit"}:
                print("Goodbye!")
                break
            if user.lower() == "summary":
                print(bot.end_conversation_summary())
                continue
            # Generate response
            resp = bot.generate_response(user)
            # Print sentiment arrow line and bot response
            last = convo.history[-2] if len(convo.history) >= 2 else None
            if last and last[0] == 'user' and last[2]:
                a = last[2]
                print(f"-> Sentiment: {a['label']}")
            print("Chatbot:", f'"{resp}"')
    except KeyboardInterrupt:
        print("\\nExiting. Here's the conversation summary:")
        print(bot.end_conversation_summary())

if __name__ == '__main__':
    main()
