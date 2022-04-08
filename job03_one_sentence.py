import pandas as pd

df = pd.read_csv('./crawling_data/cleaned_review_2022.csv')
print(df.head())
print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
df.info()

one_sentences = []
for title in df['title'].unique():
    temp = df[df['title']==title]
    temp = temp['cleaned_sentences']
    one_sentence = ' '.join(temp)
    one_sentences.append(one_sentence)
df_one_sentences = pd.DataFrame(
    {'titles':df['title'].unique(), 'cleaned_sentences':one_sentences})
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling_data/movie_review_onesentence_2022.csv',
                        index=False)





















