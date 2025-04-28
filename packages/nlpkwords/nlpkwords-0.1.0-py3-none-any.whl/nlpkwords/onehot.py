from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def main():
    docs = []
    for i in range(1, 4):
        with open(f'tech{i}.txt', 'r') as file:
            docs.append(file.read())

    all_text = ' '.join(docs).lower().split()

    unique_words = list(set(all_text))
    df = pd.DataFrame(unique_words, columns=['Word'])

    encoder = OneHotEncoder(sparse_output=False)
    one_hot = encoder.fit_transform(df[['Word']])

    one_hot_df = pd.DataFrame(one_hot, columns=encoder.get_feature_names_out(['Word']))
    print(one_hot_df)

if __name__ == "__main__":
    main()
