from sklearn.feature_extraction.text import CountVectorizer

def main():
    docs = []
    for i in range(1, 4):
        with open(f'movie{i}.txt', 'r') as file:
            docs.append(file.read())

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(docs)

    print("Vocabulary:", vectorizer.get_feature_names_out())
    print("Bag of Words Matrix:\n", X.toarray())

if __name__ == "__main__":
    main()
