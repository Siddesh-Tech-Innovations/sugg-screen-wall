import hashlib
from dotenv import load_dotenv

load_dotenv()

def hash_ip(ip: str) -> str:
    return hashlib.sha256(ip.encode()).hexdigest()

def classify_submission(text: str) -> str:
    text = text.lower()
    
    keyword_map = {
        "Suggestion": {"suggest", "recommend", "should", "improvement", "enhance"},
        "Inquiry": {"question", "why", "how", "what", "when", "where"},
        "Request": {"need", "want", "please", "request", "require"},
        "Feedback": {"think", "feel", "experience", "opinion", "good", "bad", "excellent"},
    }

    scores = {
        category: 0 for category in keyword_map
    }

    for word in text.split():
        for category, keywords in keyword_map.items():
            if word in keywords:
                scores[category] += 1

    # Return the category with the highest score, or "Feedback" as a default.
    return max(scores, key=scores.get) if any(scores.values()) else "Feedback"
