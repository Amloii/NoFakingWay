from urlextract import URLExtract


class URLFilter:
    def __init__(self):

        self.extractor = URLExtract()

    def detect_URL(self, text):

        if self.extractor.has_urls(text):
            result_dict = {'suspicious': True,
                           'filter_failed': "URL",
                           'motive': "Given text contains some URL"}

        else:
            result_dict = {'suspicious': False,
                           'filter_failed': "",
                           'motive': ""}
        return result_dict

    def predict(self, text):

        return self.detect_URL(text)
