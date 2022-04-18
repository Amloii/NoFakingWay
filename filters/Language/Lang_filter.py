
import spacy
from spacy.language import Language as LanguageManager
from spacy_langdetect import LanguageDetector
from langcodes import standardize_tag
from langcodes import Language 


def get_lang_detector(nlp, name):
    return LanguageDetector()

def create_language_detection_model():
    
    nlp = spacy.load("en_core_web_sm")
    LanguageManager.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    
    return nlp


def Lang_filter(model, text):
    
    doc = model(text)
    lang = doc._.language
    
    if (lang['language'] not in ['en', 'fr', 'es']) or (lang['score'] < 0.7):
        
        result_dict = {}
        result_dict['suspicious'] = True
        result_dict['filter_failed'] = 'Filler Filter'
        result_dict['motive'] = "Nonsense language" if (lang['score'] < 0.7) else f"{Language.make(language=standardize_tag(lang['language'])).display_name()} language detected, not supported"
        
    else: 
        result_dict = {}
        result_dict['suspicious'] = False
        result_dict['filter_failed'] = ''
        result_dict['motive'] = ''

    return result_dict