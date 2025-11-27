from src.sentiment_analyzer import SentimentAnalyzer

def test_positive_detection():
    a = SentimentAnalyzer()
    r = a.analyze_text("I am very happy and excited!")
    assert r["label"] == "Positive"

def test_negative_detection():
    a = SentimentAnalyzer()
    r = a.analyze_text("This is the worst, I hate it.")
    assert r["label"] == "Negative"

def test_negation_flip():
    a = SentimentAnalyzer()
    r = a.analyze_text("Not bad at all")
    assert r["label"] in {"Neutral","Positive"}
