import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def correct_spelling(tokens):
    corrected = []
    for word in tokens:
        blob = TextBlob(word)
        corrected.append(str(blob.correct()))
    return corrected

def main():
    with open('textfile.txt', 'r') as file:
        text = file.read()

    cleaned_text = clean_text(text)
    tokens = word_tokenize(cleaned_text)
    
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    corrected_tokens = correct_spelling(tokens)

    print("Final Tokens after processing:", corrected_tokens)

if __name__ == "__main__":
    main()
