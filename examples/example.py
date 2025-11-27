from src.conversation_manager import ConversationManager
from src.sentiment_analyzer import SentimentAnalyzer
from src.chatbot import Chatbot

convo = ConversationManager()
analyzer = SentimentAnalyzer()
bot = Chatbot(convo, analyzer)

print(bot.generate_response("Hi there!"))
print(bot.generate_response("I absolutely love this."))
print(bot.generate_response("This is terrible, I hate it."))
