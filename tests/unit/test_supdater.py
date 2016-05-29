import unittest
from pyawe.utils.supdater import degree_to_rhumb
from pyawe.utils.supdater import rhumb_to_direction

from pyawe.utils.supdater import send_data


class TestSupdater(unittest.TestCase):

    __degrees = 15
    __south_west = "Юго-Западный"
    __test_instance = degree_to_rhumb(__degrees)

    def test_init_fails_when_negative_data_provided(self):
        self.assertRaises(ValueError, degree_to_rhumb, -15)

    def test_init_fails_when_greater_data_provided(self):
        self.assertRaises(ValueError, degree_to_rhumb, 759)

    def test_getters_return_expected_data(self):
        self.assertEqual(rhumb_to_direction(10), self.__south_west)


