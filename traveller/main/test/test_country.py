from django.test import TestCase, Client
from ..country import Country


class TestCountryMethod(TestCase):
    """Test dumping countries from get_list method"""

    def test_get_list(self) -> list:
        raw_result = Country()
        result = raw_result.get_list()
        self.assertTrue(type(result), list)
