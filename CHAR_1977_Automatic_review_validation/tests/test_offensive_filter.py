
import pytest

from CHAR_1977_Automatic_review_validation.src.Filters.offensive_filter import \
    OffensiveFilter


class TestOffensiveFilter:
    def setup_class(self):
        self.filter_object = OffensiveFilter('CHAR_1977_Automatic_review_validation//tests//resources//')

        self.prefix_path = 'CHAR_1977_Automatic_review_validation.src.Filters.offensive_filter.OffensiveFilter'

        self.filter_triggered_output = {'filter_failed': 'Offensive', 'motive': 'explicit_sex', 'suspicious': True}

        self.english_language_object = {'693_1': 'en', 'name': 'english'}
        self.spanish_language_object = {'693_1': 'es', 'name': 'spanish'}
        self.italian_language_object = {'693_1': 'it', 'name': 'italian'}
        self.none_language_object = {'693_1': None, 'name': None}

    def test_build_an_offensivefilter_object(self):
        assert isinstance(self.filter_object, OffensiveFilter)

    def test__transform_chars_to_letters_transforms_selected_chars_to_letters(self):
        assert sorted(self.filter_object._transform_chars_to_letters('f00l')) == ['f00l', 'fool']

    def test__transform_chars_to_letters_do_not_modify_words_with_no_selected_chars(self):

        assert self.filter_object._transform_chars_to_letters('fool') == {'fool'}

    def test__build_alt_forms_from_word_calls__transform_chars_to_letters(self, _transform_chars_to_letters_mock):
        self.filter_object._build_alternative_forms_from_word('word')
        _transform_chars_to_letters_mock.assert_called()

    def test_predict_calls__build_alternative_forms_from_word(self, _build_alternative_forms_from_word_mock):
        self.filter_object.predict('Any review', self.english_language_object)
        _build_alternative_forms_from_word_mock.assert_called()

    def test__check_dictionary_returns_boolean_when_check_word_is_true(self):
        assert isinstance(self.filter_object._check_dictionary('any_word', self.english_language_object, True),
                          bool)

    def test__check_dictionary_returns_false_when_check_word_is_false(self):
        assert not self.filter_object._check_dictionary('any_word', self.english_language_object, False)

    def test_predict_calls__check_rude_words_list(self, _check_rude_words_list_mock):
        self.filter_object.predict('Any review', self.english_language_object)
        _check_rude_words_list_mock.assert_called()

    def test_predict_calls__check_dictionary_when_not_recorded_toxic_words_passed(self, _check_dictionary_mock):
        self.filter_object.predict('review composed by not recorded toxic words', self.english_language_object)
        _check_dictionary_mock.assert_called()

    def test_predict_calls_metric_based_methods_when_strange_words_passed(self, _damerau_levenshtein_search_mock,
                                                                          _mra_search_mock):
        self.filter_object.predict('review composed by not recorded toxic words but contains a special_word',
                                   self.english_language_object)

        _damerau_levenshtein_search_mock.assert_called()
        _mra_search_mock.assert_called()

    def test_predict_calls__transform_output(self, _format_output_mock):
        self.filter_object.predict('Any review', self.english_language_object)
        _format_output_mock.assert_called()

    def test_offensive_filter_detect_rude_words_that_appear_in_record(self):
        assert self.filter_object.predict(
            'This is an english review but contains anilingus', self.english_language_object) == \
                self.filter_triggered_output

    def test_offensive_filter_detect_rude_words_that_sounds_similar_to_some_word_in_record(self):
        assert self.filter_object.predict(
            'This is an english review but contains anilinguss', self.english_language_object) == \
               self.filter_triggered_output

    def test_offensive_filter_detect_rude_words_that_are_written_like_word_in_record(self):
        assert self.filter_object.predict(
            'This is an english review but contains anilingvs', self.english_language_object) == \
               self.filter_triggered_output

    @pytest.fixture()
    def _transform_chars_to_letters_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._transform_chars_to_letters', return_value=['transformations'])

    @pytest.fixture()
    def _detect_language_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._detect_language', return_value={'693_1': 'en', 'iso': 'english'})

    @pytest.fixture()
    def _build_alternative_forms_from_word_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._build_alternative_forms_from_word', return_value=['alts'])

    @pytest.fixture()
    def _check_rude_words_list_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._check_rude_words_list', return_value=False)

    @pytest.fixture()
    def _check_dictionary_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._check_dictionary', return_value=True)

    @pytest.fixture()
    def _damerau_levenshtein_search_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._damerau_levenshtein_search', return_value=[])

    @pytest.fixture()
    def _mra_search_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._mra_search', return_value=[])

    @pytest.fixture()
    def _format_output_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._format_output', return_value={})

    @pytest.fixture()
    def _get_language_dictionary_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '._get_language_dictionary')
