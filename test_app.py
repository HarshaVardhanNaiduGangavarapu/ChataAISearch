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

        actual_data = response.get_json()
        expected_data = read_file_json_data('health.json')
        self.assertEqual(actual_data, expected_data)

    def test_search_with_exist_str(self):
        request_body = {'str': 'Now is'}
        response = self.client.post('/search', json=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_with_exist_str.json')
        self.assertEqual(actual_data, expected_data)

    def test_search_with_not_exist_str(self):
        request_body = {'str': 'ChataAI'}
        response = self.client.post('/search', json=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_with_not_exist_str.json')
        self.assertEqual(actual_data, expected_data)

    def test_search_empty_str(self):
        request_body = {'str': ''}
        response = self.client.post('/search', json=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_empty_str.json')
        self.assertEqual(actual_data, expected_data)

    def test_search_none_str(self):
        request_body = {'name': 'ChataAI'}
        response = self.client.post('/search', json=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_empty_none_str.json')
        self.assertEqual(actual_data, expected_data)

    def test_multiple_keys_req_body(self):
        request_body = {'str': 'Chata', 'name': 'ChataAI'}
        response = self.client.post('/search', json=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('multiple_keys_req_body.json')
        self.assertEqual(actual_data, expected_data)

    def test_unsupported_mediatype_req_body(self):
        request_body = '<api>chataAI</api>';
        response = self.client.post('/search', data=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 415)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_unsupported_mediatype.json')
        self.assertEqual(actual_data, expected_data)

    def test_invalid_json_req_body(self):
        invalid_request_body = "{'str': "
        response = self.client.post('/search', data=invalid_request_body, content_type='application/json')
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_invalid_json_req_body.json')
        self.assertEqual(actual_data, expected_data)

    def test_empty_req_body(self):
        # when req_body is ''
        request_body = b''
        response = self.client.post('/search', data=request_body)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_empty_req_body.json')
        self.assertEqual(actual_data, expected_data)

        # when req_body is None
        response = self.client.post('/search', data=None)
        self.assertIsNotNone(response)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        actual_data = response.get_json()
        expected_data = read_file_json_data('search_empty_req_body.json')
        self.assertEqual(actual_data, expected_data)

    def test_swagger_json(self):
        swagger_response = self.client.get('/swagger.json')
        self.assertEqual(swagger_response.status_code, 200)

        with open('swagger.json', 'r') as file:
            expected_content = json.load(file)

        actual_content = swagger_response.get_json()
        self.assertEqual(actual_content,expected_content)


if __name__ == '__main__':
    unittest.main()
