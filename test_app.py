from app import app
import unittest
import json

# Author: Harsha Gangavarapu
# Description: Test cases for Chata AI search API service application


def read_file_json_data(filename):
    with open('test_resources/' + filename, 'r') as file:
        return json.load(file)


class AppUnitTest(unittest.TestCase):
    def setUp(self):
        app.Testing = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

        data = response.get_json()
        expected_data = read_file_json_data('health.json')
        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()
