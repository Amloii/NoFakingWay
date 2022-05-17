import os
import re
from itertools import product
from unidecode import unidecode
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textdistance import damerau_levenshtein, mra
from wordfreq import zipf_frequency

CHARS_REPLACING_DICT = {'0': ['o'], '1': ['i', 'l'], '3': ['b'], '4': ['a'], '8': ['b'], '$': ['s'], '&': ['s']}
SPECIAL_CHARACTERS = '.^$*+-?()[]{}\\|—/'


class OffensiveFilter:
    def __init__(self, data_folder_path='artifacts//'):
        self.data_folder_path = data_folder_path
        self.default_rude_words_record_path = self.data_folder_path + 'rude_words_ENGLISH_full_list.csv'
        self.allowed_languages_list = ['en', 'es', 'fr']

        self.frequency_threshold = 3
        self.dl_threshold = 3
        self.mra_threshold = 2

    @staticmethod
    def _transform_chars_to_letters(review_word):
        pattern = '|'.join('\\' + char if char in SPECIAL_CHARACTERS else char for char in CHARS_REPLACING_DICT.keys())

        transformations = []
        for mapping_values in product(*CHARS_REPLACING_DICT.values()):
            map_dict = dict(zip(CHARS_REPLACING_DICT.keys(), mapping_values))
            transformations.append(re.sub(pattern, lambda x: map_dict[x.group()], review_word))

        return set([review_word] + transformations)

    def _build_alternative_forms_from_word(self, word):

        word_alts = self._transform_chars_to_letters(word)

        return word_alts

    def _check_dictionary(self, word, review_language, check_word=True):

        if check_word and review_language['693_1'] in self.allowed_languages_list:
            word_in_dict = zipf_frequency(word, review_language['693_1'], 'small') > self.frequency_threshold
        elif check_word and review_language['693_1'] not in self.allowed_languages_list:
            word_in_dict = zipf_frequency(word, 'en', 'small') > self.frequency_threshold
        else:
            word_in_dict = False

        return word_in_dict

    @staticmethod
    def _check_rude_words_list(review_word, rude_words_record):

        return review_word in set(rude_words_record.bad_word)

    def _damerau_levenshtein_search(self, word, rude_words_record, check_word=True):
        if check_word:
            word_dl_scores = rude_words_record['bad_word'].apply(lambda bad_word: damerau_levenshtein.distance(bad_word,
                                                                                                               word))
            return list(rude_words_record[word_dl_scores < self.dl_threshold]['bad_word'])
        else:
            return []

    def _mra_search(self, word, rude_words_record, check_word=True):
        if check_word:
            word_mra_scores = rude_words_record['bad_word'].apply(lambda bad_word: mra.distance(bad_word, word))

            return list(rude_words_record[word_mra_scores < self.mra_threshold]['bad_word'])
        else:
            return []

    @staticmethod
    def _build_review_wordlist(review, review_language):

        if review_language['name'] in stopwords.fileids():
            stop_words = set(stopwords.words(review_language['name']))
        else:
            stop_words = set(stopwords.words('english'))

        if isinstance(review, str) and review:
            return set([unidecode(word) for word in word_tokenize(review.lower(), review_language['name']) if word not
                        in stop_words])
        else:
            return {}

    def _get_rude_words_records(self, review_language):

        record_file_name = 'rude_words_' + str(review_language['name']).upper() + '_full_list.csv'

        if record_file_name in os.listdir(self.data_folder_path):
            rude_words_record = pd.read_csv(self.data_folder_path + record_file_name, sep=',')
        else:
            rude_words_record = pd.read_csv(self.default_rude_words_record_path, sep=',')

        return rude_words_record

    @staticmethod
    def _format_output(rude_words_matches, rude_words_record):

        output = {'suspicious': len(rude_words_matches) > 0, 'filter_failed': 'Offensive'}

        if rude_words_record is not None:
            rude_words_tags = '-'.join(rude_words_record[rude_words_record['bad_word'].isin(rude_words_matches)]
                                       ['tags'])
            output['motive'] = ', '.join(set(rude_words_tags.split('-')))
        else:
            output['motive'] = ''

        return output

    def predict(self, review, review_language):

        review_wordlist = self._build_review_wordlist(review, review_language)

        if review_wordlist:
            rude_words_record = self._get_rude_words_records(review_language)

            review_wordlist_and_alts = set(sum([list(self._build_alternative_forms_from_word(word))
                                                for word in review_wordlist], []))

            review_wordlist_df = pd.DataFrame(columns=['review_word'], data=review_wordlist_and_alts)

            review_wordlist_df['rude_record_word'] = review_wordlist_df['review_word'].\
                apply(lambda word: self._check_rude_words_list(word, rude_words_record))

            review_wordlist_df['word_in_dict'] = review_wordlist_df.\
                apply(lambda row: self._check_dictionary(row['review_word'], review_language,
                                                         not row['rude_record_word']), axis=1)

            review_wordlist_df['check_mra'] = (~review_wordlist_df['rude_record_word']) & (~ review_wordlist_df
                                                                                           ['word_in_dict'])
            review_wordlist_df['mra_search'] = review_wordlist_df.\
                apply(lambda row: self._mra_search(row['review_word'], rude_words_record, row['check_mra']), axis=1)

            review_wordlist_df['check_dl'] = (review_wordlist_df['check_mra']) & (review_wordlist_df['mra_search'].
                                                                                  map(lambda lst: len(lst)) == 0)
            review_wordlist_df['damerau_levenshtein_search'] = review_wordlist_df.\
                apply(lambda row: self._damerau_levenshtein_search(row['review_word'], rude_words_record,
                                                                   row['check_dl']), axis=1)

            rude_words_matches = list(review_wordlist_df[review_wordlist_df['rude_record_word']]['review_word'])

            rude_words_matches += sum(review_wordlist_df['mra_search'], [])
            rude_words_matches += sum(review_wordlist_df['damerau_levenshtein_search'], [])

            return self._format_output(rude_words_matches, rude_words_record)
        else:
            return self._format_output([], None)
