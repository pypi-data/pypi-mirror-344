import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def main():
    with open('textfile.txt', 'r') as file:
        text = file.read()

    cleaned_text = clean_text(text)
    tokens = word_tokenize(cleaned_text)

    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    stemmed = [ps.stem(word) for word in tokens]
    lemmatized = [lemmatizer.lemmatize(word) for word in stemmed]

    triplets = [lemmatized[i:i+3] for i in range(len(lemmatized)-2)]

    print("Triplets after lemmatization:", triplets)

if __name__ == "__main__":
    main()
