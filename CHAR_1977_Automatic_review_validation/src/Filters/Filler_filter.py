import re

import langdetect
from langcodes import Language, standardize_tag


class FillerFilter:

    def __init__(self):
        self.allowed_languages_list = ['en', 'es', 'fr']

    @staticmethod
    def filler_filter_alphanumeric(review: str):
        if not bool(re.match('[a-zA-Z0-9]', review)):
            result_dict = {'suspicious': True, 'filter_failed': 'Filler',
                           'motive': "Review doesn't contain alphanumeric characters"}
        else:
            result_dict = {'suspicious': False, 'filter_failed': '',
                           'motive': ''}
        return result_dict

    def filler_filter_valid_language(self, review: str, review_language):
        if review_language['693_1'] not in self.allowed_languages_list:
            result_dict = {'suspicious': True, 'filter_failed': 'Filler',
                           'motive':
                               review_language['name'].capitalize()
                               + " language detected, not supported"
                           }
        else:
            result_dict = {'suspicious': False, "filter_failed": "", "motive": ""}
        return result_dict

    def predict(self, review: str, review_language):
        result_alphanumeric = self.filler_filter_alphanumeric(review)
        if result_alphanumeric.get('suspicious'):
            return result_alphanumeric
        else:
            return self.filler_filter_valid_language(review, review_language)
