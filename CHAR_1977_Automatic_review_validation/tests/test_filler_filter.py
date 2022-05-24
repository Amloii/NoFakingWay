import pytest
import os
import sys

# Load src folder (in all cases)
filters_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(filters_dir)

from src.Filters.Filler_filter import FillerFilter


class TestFillerFilter:
    def setup_class(self):
        self.filter_object = FillerFilter()
        self.prefix_path = 'src.Filters.Filler_filter.FillerFilter'
        self.filter_non_triggered_output = {'filter_failed': '', 'motive': '', 'suspicious': False}

        self.english_language_object = {'693_1': 'en', 'name': 'english'}
        self.spanish_language_object = {'693_1': 'es', 'name': 'spanish'}
        self.italian_language_object = {'693_1': 'it', 'name': 'italian'}
        self.none_language_object = {'693_1': None, 'name': None}

    def test_build_an_FillerFilter_object(self):
        assert isinstance(self.filter_object, FillerFilter)

    def test__review_is_suspicious_because_is_not_alphanumeric(self):
        assert self.filter_object.filler_filter_alphanumeric('*/-*') == \
               {'suspicious': True, 'filter_failed': 'Filler',
                'motive': "Review doesn't contain alphanumeric characters"}

    def test__review_is_not_suspicious_because_is_alphanumeric(self):
        assert self.filter_object.filler_filter_alphanumeric('alpha7') == \
               self.filter_non_triggered_output

    def test__filler_filter_is_valid_language(self):
        assert self.filter_object.filler_filter_valid_language(self.spanish_language_object) == \
               self.filter_non_triggered_output

    def test__filler_filter_is_not_valid_language(self):

        assert self.filter_object.filler_filter_valid_language(self.italian_language_object) == \
               {'suspicious': True, 'filter_failed': 'Filler',
                'motive': "Italian language detected, not supported"}

    def test__predict_calls_filler_filter_alphanumeric(self, _filler_filter_alphanumeric_mock):
        self.filter_object.predict('La comida estaba muy buena', self.spanish_language_object)
        _filler_filter_alphanumeric_mock.assert_called()

    def test__predict_calls_filler_filter_valid_language(self, _filler_filter_valid_language_mock):
        self.filter_object.predict('Un capolavoro, indispensabile per chi adora i classici. ',
                                   self.italian_language_object)
        _filler_filter_valid_language_mock.assert_called()

    def test__predict_empty(self):
        assert self.filter_object.predict('', self.none_language_object) == \
               {'suspicious': True, 'filter_failed': 'Filler',
                'motive': "Review doesn't contain alphanumeric characters"}

    def test__predict_not_alphanumeric(self):
        assert self.filter_object.predict('*/-', self.none_language_object) == \
               {'suspicious': True, 'filter_failed': 'Filler',
                'motive': "Review doesn't contain alphanumeric characters"}

    def test__predict_not_valid_language(self):
        review = 'Un capolavoro, "indispensabile per" chi adora i classici. Libro arrivato in tempo e in perfette ' \
                 'condizioni. '
        assert self.filter_object.predict(review, self.italian_language_object) == \
               {'suspicious': True, 'filter_failed': 'Filler',
                'motive': "Italian language detected, not supported"}

    def test__predict_valid_language(self):
        review = 'reseña válida'
        assert self.filter_object.predict(review, self.spanish_language_object) == \
               self.filter_non_triggered_output

    def test__predict_valid_language_quotes(self):
        review = '"reseña" válida'
        assert self.filter_object.predict(review, self.spanish_language_object) == \
               self.filter_non_triggered_output

    @pytest.fixture()
    def _predict_alphanumeric_make_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '.predict', return_value=dict())

    @pytest.fixture()
    def _filler_filter_alphanumeric_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '.filler_filter_alphanumeric', return_value=dict())

    @pytest.fixture()
    def _filler_filter_valid_language_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '.filler_filter_valid_language', return_value=dict())
