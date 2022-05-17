import time

import pandas as pd

from CHAR_1977_Automatic_review_validation.src.Filters.offensive_filter import \
    OffensiveFilter

filter_object = OffensiveFilter('..//..//artifacts//')

reviews_df = pd.read_csv('Data/AmazonReviews_df.csv', sep=',')

sample_size = 5000
results_data_dicts = []

for text in reviews_df.sample(sample_size, replace=True)['reviews.text']:
    if isinstance(text, str) and len(text) > 0:
        words_count = len(text.split(' '))
        start = time.time()
        output = filter_object.predict(text)
        end = time.time()

        result = {'text': text.replace(',', ' ').replace('\r', '').replace('\n', ''),
                  'words_count': words_count, 'time_elapsed': end-start}

        results_data_dicts.append(result)

pd.DataFrame(results_data_dicts).to_csv('Data//time_elapsed_df.csv', sep=',', index=False)
