
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
import subprocess

def get_lang_detector(nlp, name):
    return LanguageDetector()

def create_language_detection_model():
    
    nlp = spacy.load("en_core_web_sm")
    Language.factory("language_detector", func=get_lang_detector)
    nlp.add_pipe('language_detector', last=True)
    
    return nlp


def Lang_filter(model, text):
    
    doc = model(text)
    lang = doc._.language
    
    if (lang['language'] not in ['en', 'fr', 'es']) or (lang['score'] < 0.9):
        
        result_dict = {}
        result_dict['suspicious'] = True
        result_dict['filter_failed'] = 'Filler Filter'
        result_dict['motive'] = "Nonsense language" if (lang['score'] < 0.9) else f"Detected {lang['language']} idiom. Not soported"
        result_dict['probability'] = 1 - lang['score']
    else: 
        result_dict = {}
        result_dict['suspicious'] = False
        result_dict['filter_failed'] = ''
        result_dict['motive'] = ''
        result_dict['probability'] = 0.0

    return result_dict