import re

class SentimentAnalyzer:
    def __init__(self):
        # Expanded polarity lexicons (add more as needed)
        self.positive = set([
            "love","love","loves","loving","great","amazing","happy","good","wonderful",
            "excellent","fantastic","awesome","like","liked","enjoy","enjoyed",
            "pleased","delighted","joy","joyful","positive","best","nice","yay","better"
        ])
        self.negative = set([
            "hate","hates","hating","terrible","bad","awful","worst","sad","angry",
            "disappointed","disappoint","disappointing","disappoints","disappointer",
            "disappoints","dislike","disliked","problem","issue","annoying","upset",
            "horrible","failed","frustrat","displease","displeased","displeasing"
        ])
        # Common negations
        self.negations = set(["not","no","never","none","nobody","nothing","nowhere","n't","cannot","can't","dont","don't","doesn't","doesnt","isn't","isnt","wasn't","wasnt"])
        # Intensifiers mapping
        self.intensifiers = {"very":1.3, "extremely":1.6, "really":1.2, "so":1.2, "too":1.1}
        # regex for tokens
        self.token_re = re.compile(r"[\w']+|[.,!?;]")

    def tokenize(self, text):
        return [t.lower() for t in self.token_re.findall(text)]

    def _normalize_token(self, tok):
        """Basic normalization: strip common endings to match base lexicon words.
           This is a light-weight alternative to installing NLTK/Spacy.
        """
        t = tok.lower()
        # remove common punctuation if any
        t = re.sub(r"[^\w']", "", t)
        # common suffix stripping
        for suf in ("ing","ed","es","s"):
            if t.endswith(suf) and len(t) - len(suf) >= 3:
                t = t[:-len(suf)]
                break
        return t

    def analyze_text(self, text):
        """
        Return dict: {'text': text, 'score': float, 'pos_count': int, 'neg_count': int, 'label': str}
        Score thresholds adjusted: score >= 1 -> Positive, score <= -1 -> Negative
        """
        tokens = self.tokenize(text)
        pos = 0.0
        neg = 0.0
        pos_count = 0
        neg_count = 0
        for i, tok in enumerate(tokens):
            norm = self._normalize_token(tok)
            # check intensifier previous token
            multiplier = 1.0
            if i>0 and tokens[i-1].lower() in self.intensifiers:
                multiplier = self.intensifiers[tokens[i-1].lower()]
            # handle positive
            if norm in self.positive:
                flip = self._has_negation(tokens, i)
                if flip:
                    neg -= 1.0 * multiplier
                    neg_count += 1
                else:
                    pos += 1.0 * multiplier
                    pos_count += 1
            elif norm in self.negative:
                flip = self._has_negation(tokens, i)
                if flip:
                    pos += 1.0 * multiplier
                    pos_count += 1
                else:
                    neg -= 1.0 * multiplier
                    neg_count += 1
        score = pos + neg  # neg is negative
        # Decide label with looser thresholds so single-word matches count
        if pos_count > 0 and neg_count > 0:
            # Mixed if both present and magnitudes similar
            if abs(score) <= 0.9:
                label = "Mixed"
            else:
                label = "Positive" if score > 0 else "Negative"
        else:
            if score >= 1.0:
                label = "Positive"
            elif score <= -1.0:
                label = "Negative"
            elif -0.9 < score < 0.9:
                label = "Neutral"
            else:
                label = "Positive" if score > 0 else "Negative"
        return {
            "text": text,
            "score": round(score, 3),
            "pos_count": pos_count,
            "neg_count": neg_count,
            "label": label
        }

    def _has_negation(self, tokens, idx, window=3):
        # check up to `window` tokens before idx for negation
        start = max(0, idx - window)
        for j in range(start, idx):
            if tokens[j].lower() in self.negations:
                return True
        return False
