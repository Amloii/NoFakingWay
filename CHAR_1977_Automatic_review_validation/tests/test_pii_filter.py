# coding=utf-8
import pytest

from CHAR_1977_Automatic_review_validation.src.Filters.PII_filter import \
    PersonalInformationFilter


class TestPersonalInformationFilter:
    def setup_class(self):
        self.filter_object = PersonalInformationFilter()
        self.prefix_path = 'CHAR_1977_Automatic_review_validation.src.Filters.PII_filter.PersonalInformationFilter'

    def test_build_an_PersonalInformationFilter_object(self):
        assert isinstance(self.filter_object, PersonalInformationFilter)

    def test__review_is_suspicious_because_is_email(self):
        assert self.filter_object.personal_information_filter('Mi email es laksdjnba@gmail.com') == \
               {'suspicious': True, 'filter_failed': 'Personal information',
                'motive': "email"
                }

    def test__review_is_not_suspicious(self):
        assert self.filter_object.personal_information_filter('No hay pii') == \
               {'suspicious': False, 'filter_failed': '',
                'motive': ""
                }

    def test__predict_calls_personal_information_filter(self, _personal_information_filter_mock):
        self.filter_object.predict('Esta reseña tiene el numero de telefono 666000000')
        _personal_information_filter_mock.assert_called()

    @pytest.fixture()
    def _personal_information_filter_mock(self, mocker):
        yield mocker.patch(self.prefix_path + '.personal_information_filter', return_value=dict())
