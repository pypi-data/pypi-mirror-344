import unittest
from dotenv import dotenv_values
from schipholapi import SchipholAPI

config = dotenv_values(".env")


class TestSchipholAPI(unittest.TestCase):
    def setUp(self):
        self.api = SchipholAPI(app_id=config["APP_ID"], app_key=config["APP_KEY"])

    def test_get_flights(self):
        # Call the method
        result = self.api.get_flights()

        # Check the result
        self.assertIsNotNone(result)
        self.assertEqual(len(result['flights']), 20)


if __name__ == '__main__':
    unittest.main()
