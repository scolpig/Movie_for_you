import pandas as pd
import glob
data_paths = glob.glob('./crawling_data/datasets/*')
print(data_paths)
df = pd.DataFrame()
for path in data_paths[1:]:
    df_temp = pd.read_csv(path)
    df_temp.columns = ['title', 'cleaned_sentences']
    df = pd.concat([df, df_temp], ignore_index=True,
              axis='rows')
df.info()
df.to_csv('./crawling_data/datasets/movie_review_2018_2022.csv',
          index=False)