from sklearn.feature_extraction.text import TfidfVectorizer

def main():
    docs = []
    for i in range(1, 4):
        with open(f'tourist{i}.txt', 'r') as file:
            docs.append(file.read())

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)

    print("Vocabulary:", vectorizer.get_feature_names_out())
    print("TF-IDF Matrix:\n", X.toarray())

if __name__ == "__main__":
    main()
