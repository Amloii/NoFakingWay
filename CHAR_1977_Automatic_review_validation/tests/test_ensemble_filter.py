import pytest

from CHAR_1977_Automatic_review_validation.src.Ensemble.Ensemble_filter import \
    EnsembleModel


class TestEnsemble:
    def setup_class(self):
        self.ensemble_model = EnsembleModel('CHAR_1977_Automatic_review_validation//tests//resources//')
        self.prefix_path = 'CHAR_1977_Automatic_review_validation.src.'

        self.english_language_object = {'693_1': 'en', 'name': 'english'}
        self.spanish_language_object = {'693_1': 'es', 'name': 'spanish'}
        self.french_language_object = {'693_1': 'fr', 'name': 'french'}
        self.none_language_object = {'693_1': None, 'name': None}

    def test_build_an_ensemble_model_object(self):
        assert isinstance(self.ensemble_model, EnsembleModel)

    def test__detect_language_returns_true_language_when_an_english_review_passed(self):
        assert self.ensemble_model._detect_language('This is an english review') == self.english_language_object

    def test__detect_language_returns_true_language_when_an_spanish_review_passed(self):
        assert self.ensemble_model._detect_language('Esta es una review escrita en español') == \
               self.spanish_language_object

    def test__detect_language_returns_true_language_when_an_french_review_passed(self):
        assert self.ensemble_model._detect_language('Ceci est une critique rédigée en espagnol') == \
               self.french_language_object

    def test__detect_language_returns_null_language_dict_when_a_void_review_passed(self):
        assert self.ensemble_model._detect_language('') == self.none_language_object


    def test_predict_calls__filler_filter(self, _filler_filter_predict_mock):
        self.ensemble_model.predict({'review': '*-*/'})
        _filler_filter_predict_mock.assert_called()

    def test_predict_calls__pii_filter(self, _pii_filter_predict_mock):
        self.ensemble_model.predict({'review': 'Mi número es 616000000'})
        _pii_filter_predict_mock.assert_called()

    def test_predict_calls__offensive_filter(self, _offensive_filter_predict_mock):
        self.ensemble_model.predict({'review': 'Eres tonto'})
        _offensive_filter_predict_mock.assert_called()

    def test_predict_calls__url_filter(self, _url_filter_predict_mock):
        self.ensemble_model.predict({'review': 'Buscalo en www.google.es'})
        _url_filter_predict_mock.assert_called()

    @pytest.fixture()
    def _filler_filter_predict_mock(self, mocker):
        path_filler = 'Filters.Filler_filter.FillerFilter'
        yield mocker.patch(self.prefix_path + path_filler + '.predict',
                           return_value={'suspicious': True, 'filter_failed': 'Filler',
                                         'motive': "Review doesn't contain alphanumeric characters"})

    @pytest.fixture()
    def _pii_filter_predict_mock(self, mocker):
        path_pii = 'Filters.PII_filter.PersonalInformationFilter'
        yield mocker.patch(self.prefix_path + path_pii + '.predict',
                           return_value={'suspicious': True, 'filter_failed': 'Personal information',
                                         'motive': "Review doesn't contain alphanumeric characters"})

    @pytest.fixture()
    def _offensive_filter_predict_mock(self, mocker):
        path_offensive = 'Filters.offensive_filter.OffensiveFilter'
        yield mocker.patch(self.prefix_path + path_offensive + '.predict',
                           return_value={'suspicious': True, 'Offensive': 'Filler',
                                         'motive': "Review doesn't contain alphanumeric characters"})

    @pytest.fixture()
    def _url_filter_predict_mock(self, mocker):
        path_url = 'Filters.URL_filter.URLFilter'
        yield mocker.patch(self.prefix_path + path_url + '.predict',
                           return_value={'suspicious': True, 'filter_failed': 'URL',
                                         'motive': "Review doesn't contain alphanumeric characters"})

    @pytest.fixture()
    def _detect_language_mock(self, mocker):
        path_ensemble = 'Ensemble.Ensemble_filter'
        yield mocker.patch(self.prefix_path + path_ensemble + '._detect_language', return_value={'693_1': 'en', 'iso': 'english'})
