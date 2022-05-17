import re


class PersonalInformationFilter:

    def __init__(self):
        self.regex_dict = {'email': r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",
                           'UK phone number': r"(((\(\+44|0044|00 44|44)?(\s\(0\)\s|\s0\s|\s)?)|0)7\d{3}(\s)?\d{6}",
                           'Spanish phone number': r"(\+34|0034|00 34|34)?[ -]*(6|7|9|8)[ -]*([0-9][ -]*){8}",
                           'French phone number': r"(\+33|0033|00 33|33)?[ -]*(1|2|3|4|5|6)[ -]*(([0-9][ -]*){2}){4}",
                           'Spanish DNI/NIE': r"((([X-Z])|([LM])){1}([-,' ']?)((\d){7})([-]?)([A-Z]{1}))|"
                                              r"((\d{8})([-, ' ']?)([A-Z]))",
                           'French id (insee)': r"\b\b\d{15}\b\b",
                           'UK id': r"([a-zA-Z]){2}([-,' ']?)([0-9]){2}([-,' ']?)"
                                    r"([0-9]){2}([-,' ']?)([0-9]){2}([-,' '])?([Aa-dD]){1}?$",
                           'French drivers licence': r"\b\d{12}\b",
                           'UK drivers licence': r"[A-Z9]{5}\d{6}[A-Z9]{2}\d[A-Z]{2}",
                           'French passport': r"\d{2}[A-Za-z0-9]{2}\d{5}\D",
                           'UK passport': r"\b\d{9}\b",
                           'UK National health service number': r"\b\d{3}\s?\d{3}\s?\d{4}\b",
                           'Social Security Spanish number': r"\b\d{2}\s?\-?\/?\d{8}\/?\d{2}\b",
                           'Credit card number': r"\b((4\d{3}|5[1-5]\d{2}|2\d{3}|3[47]\d{1,2})"
                                                r"[\s\-]?\d{4,6}[\s\-]?\d{4,6}?([\s\-]\d{3,4})?(\d{3})?)\b",
                           'SWIFT': r"\b([A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?)\b",
                           'IBAN': r"\b([A-Z]{2}[ \-]?[0-9]{2})(?=(?:[ \-]?[A-Z0-9]){9,30}$)"
                                   r"((?:[ \-]?[A-Z0-9]{3,5}){2,7})([ \-]?[A-Z0-9]{1,3})?$\b",
                           'IP': r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}",
                           'username': r"(^| )(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.)))"
                                       r"{0,28}(?:[A-Za-z0-9_]))?)"
                           }

    def personal_information_filter(self, text):
        list_motives = []
        for key, value in self.regex_dict.items():
            found_motive = re.findall(value, text)
            if len(found_motive) > 0:
                list_motives.append(key)

        if len(list_motives) >= 1:
            result_dict = {'suspicious': True, 'filter_failed': 'Personal information',
                           'motive': ", ".join(list_motives)}
        else:
            result_dict = {'suspicious': False, 'filter_failed': '',
                           'motive': ""}
        return result_dict

    def predict(self, review: str):
        return self.personal_information_filter(review)
