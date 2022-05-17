# In local
import langdetect
import language_data
from langcodes import Language, standardize_tag

from CHAR_1977_Automatic_review_validation.src.Filters.Filler_filter import \
    FillerFilter
from CHAR_1977_Automatic_review_validation.src.Filters.offensive_filter import \
    OffensiveFilter
from CHAR_1977_Automatic_review_validation.src.Filters.PII_filter import \
    PersonalInformationFilter
from CHAR_1977_Automatic_review_validation.src.Filters.URL_filter import \
    URLFilter

# In AWS
# from src.Filters.Filler_filter import FillerFilter
# from src.Filters.offensive_filter import OffensiveFilter
# from src.Filters.PII_filter import PersonalInformationFilter
# from src.Filters.URL_filter import URLFilter


class EnsembleModel:
    def __init__(self, data_folder_path='CHAR_1977_Automatic_review_validation//src//artifacts//'):
        # def __init__(self, data_folder_path='src/artifacts/'):
        self.pii_filter = PersonalInformationFilter()
        self.fi_filter = FillerFilter()
        self.offensive_filter = OffensiveFilter(data_folder_path)
        self.url_filter = URLFilter()


    def _detect_language(self, review):
        try:
            language_693_1 = langdetect.detect(review)
        except langdetect.lang_detect_exception.LangDetectException:
            language_693_1 = None

        try:
            language_name = Language.make(language=standardize_tag(language_693_1)).display_name().lower()
        except AttributeError:
            language_name = None

        return {'693_1': language_693_1, 'name': language_name}

    def predict_review(self, review: str):
        review_detected_language = self._detect_language(review)

        res_filler = self.fi_filter.predict(review, review_detected_language)
        if res_filler.get('suspicious'):
            return res_filler
        else:
            res_pii = self.pii_filter.predict(review)
            if res_pii.get('suspicious'):
                return res_pii
            else:
                res_offensive = self.offensive_filter.predict(review, review_detected_language)
                if res_offensive.get('suspicious'):
                    return res_offensive
                else:
                    res_url = self.url_filter.predict(review)
                    return res_url

    def predict(self, dict_review: dict):
        return self.predict_review(dict_review.get('review'))
    
    
    

