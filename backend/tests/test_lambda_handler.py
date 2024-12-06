import unittest
from unittest.mock import patch
import json
from src.main import lambda_handler 

class TestLambdaHandler(unittest.TestCase):

    @patch('src.main.boto3.client')
    @patch('src.main.write_url')
    @patch('src.main.shorten')
    def test_post_method(self, mock_shorten, mock_write_url, mock_boto3_client):
        # Arrange
        mock_shorten.return_value = 'abc123'
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'url': 'https://example.com'})
        }
        context = {}

        # Act
        response = lambda_handler(event, context)

        # Assert
        self.assertEqual(response['statusCode'], 201)
        body = json.loads(response['body'])
        self.assertTrue(body['success'])
        self.assertEqual(body['short_url'], 'abc123')
        mock_shorten.assert_called_once_with('https://example.com')
        mock_write_url.assert_called_once()

    @patch('src.main.boto3.client')
    @patch('src.main.get_url')
    def test_get_method_with_key(self, mock_get_url, mock_boto3_client):
        # Arrange
        mock_get_url.return_value = 'https://example.com'
        event = {
            'httpMethod': 'GET',
            'path': '/abc123'
        }
        context = {}

        # Act
        response = lambda_handler(event, context)

        # Assert
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertTrue(body['success'])
        self.assertEqual(body['long_url'], 'https://example.com')
        mock_get_url.assert_called_once_with('/abc123', '/testpath', mock_boto3_client())

    @patch('src.main.boto3.client')
    def test_get_method_without_key(self, mock_boto3_client):
        # Arrange
        event = {
            'httpMethod': 'GET',
            'path': ''
        }
        context = {}

        # Act
        response = lambda_handler(event, context)

        # Assert
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertTrue(body['success'])
        self.assertEqual(body['message'], 'no url requested')

    def test_invalid_method(self):
        # Arrange
        event = {
            'httpMethod': 'PUT',
            'body': json.dumps({'url': 'https://example.com'})
        }
        context = {}

        # Act
        response = lambda_handler(event, context)

        # Assert
        self.assertIsNone(response)  # Or whatever behavior you expect for invalid methods

if __name__ == '__main__':
    unittest.main()