from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis")

    def analyze_sentiment(self, text):
        result = self.sentiment_pipeline(text)[0]
        return {
            "label": result["label"],
            "score": result["score"]
        }

    def analyze_reviews(self, reviews):
        sentiments = [self.analyze_sentiment(review) for review in reviews]
        positive = sum(1 for s in sentiments if s["label"] == "POSITIVE")
        negative = sum(1 for s in sentiments if s["label"] == "NEGATIVE")
        
        return {
            "positive_ratio": positive / len(reviews),
            "negative_ratio": negative / len(reviews),
            "average_score": sum(s["score"] for s in sentiments) / len(reviews)
        }
