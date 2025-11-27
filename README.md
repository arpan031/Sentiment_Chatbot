## Overview
A Python-based chatbot capable of analyzing the **sentiment of every user message** and generating meaningful responses.  
Supports **conversation-level sentiment analysis** (Tier 1 requirement) and **enhanced rule-based response logic** (Tier 2 partial).

---

## How to Run
### 2. Create a virtual environment  
**Windows**
```
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the chatbot
```
python -m src.main
```
_or_
```
python src/main.py
```

### 5. Run auto tests
```
pytest
```

### 6. Example script
```
python examples/example.py
```

---

##  Chosen Technologies

- **Python 3.8+**
- **Rule-based Sentiment Analyzer**  
  Uses polarity dictionaries, negation logic, intensifiers, mixed-sentiment detection.
- **Custom Chatbot Engine**  
  Response logic varies with detected sentiment.
- **PyTest**  
  Included for automated testing.

---

## Sentiment Logic Explanation

### 1. Keyword Polarity Matching
Uses positive & negative word lists.  
Each word adjusts the sentiment scoring.

### 2. Negation Handling
Flips polarity for:
- not  
- don't / doesn’t  
- isn't / wasn’t  
- never  

Examples:  
- “not bad” → becomes **Neutral/Positive**  
- “don’t hate it” → becomes **Positive**  
- “not good” → becomes **Negative**

### 3. Mixed Sentiment Detection  
If both strong positive & negative cues → **Mixed**.

### 4. Final Classification
- score > +2 → **Positive**  
- score < -2 → **Negative**  
- -1 ≤ score ≤ +1 → **Neutral**  
- both present → **Mixed**

---

##  Tier 2 Implementation Status

### Implemented  
- Dynamic responses based on sentiment  
- Negation-aware detection  
- Conversation memory  
- Auto test script + CSV export  
- Partial intent recognition  

---

##  Project Structure
```
sentiment_chatbot/
│
├── src/
│   ├── chatbot.py
│   ├── sentiment_analyzer.py
│   ├── conversation_manager.py
│   └── main.py
│
├── examples/
├── tests/
├── requirements.txt
├── README.md
└── setup.py
```

---
