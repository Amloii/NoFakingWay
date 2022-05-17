from CHAR_1977_Automatic_review_validation.src.Filters.URL_filter import \
    URLFilter


class TestURLFilter:
    def setup_class(self):
        self.filter_object = URLFilter()
        self.prefix_path = 'CHAR_1977_Automatic_review_validation.src.Filters.URL_filter'

    def test_build_an_URLFilter_object(self):
        assert isinstance(self.filter_object, URLFilter)

    def test__review_is_suspicious_because_contains_URL(self):
        review1 = "I'd like to show off a TTS system I have been working " \
                  "on for the past year. I've open-sourced all the code and " \
                  "the trained model weights: https://github.com/neonbjb/tortoise-tts"
        assert self.filter_object.predict(review1) == \
               {'suspicious': True, 'filter_failed': "URL",
                'motive': "Given text contains some URL"}

    def test__review_is_not_suspicious_because_doesnt_contain_URL(self):
        review2 = "This was born out of a desire to reproduce the original DALLE with speech. " \
                  "It is zero-shot because you feed the text and examples of a voice to mimic as " \
                  "prompts to an autoregressive LLM. "
        assert self.filter_object.predict(review2) == \
               {'suspicious': False, 'filter_failed': "",
                'motive': ""}
