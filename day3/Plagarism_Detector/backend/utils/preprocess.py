import re

def clean_text(text):
    """Clean individual text: remove extra spaces, special chars (basic), lowercase."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation (optional)
    return text.lower()  # Lowercase (optional)

def preprocess_texts(text_list):
    """Preprocess a list of texts."""
    return [clean_text(t) for t in text_list]