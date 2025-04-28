import datetime
import random
import unittest
from unittest.mock import patch, MagicMock

from requests import Response
from zerobouncesdk import ZBSendFileResponse

from million_verifier import MVUploadFileResponse, MVStatus, MVGetFileResponse
from app import CompanyDatabaseProcessor, add_translation


class TestEmailValidation(unittest.TestCase):

    def setUp(self):
        self.processor = CompanyDatabaseProcessor()
        self.processor.million_verifier_api_key = "FAKE_API_KEY"
        self.processor.zero_bounce_api_key = "FAKE_API_KEY"
        self.file_id = 940
        add_translation()
        self.processor.import_csv('temp/test.csv', 100)
        self.processor.filter_generic_emails()
        self.processor.analyze_data()
        self.processor.export_csv('temp/export.csv')

    @patch('apis.million_verifier.mv.MillionVerifier')
    @patch('apis.million_verifier.mv.requests.post')
    def test_million_verifier_valid(self, mv_post, mock_verifier):
        mock_instance = mock_verifier.return_value
        json = {
            "file_id": f"{self.file_id}",
            "file_name": "mails500.txt",
            "status": "in_progress",
            "unique_emails": 257,
            "updated_at": "2021-05-16 12:25:42",
            "createdate": "2021-05-16 12:25:42",
            "percent": 60,
            "total_rows": 500,
            "verified": 0,
            "unverified": 0,
            "ok": 0,
            "catch_all": 0,
            "disposable": 0,
            "invalid": 0,
            "unknown": 0,
            "reverify": 0,
            "credit": 0,
            "estimated_time_sec": 120,
            "error": ""
        }
        mv_post_response = Response()
        mv_post_response.status_code = 200
        mv_post_response.json = lambda: json
        mv_post_response.headers['Content-Type'] = "application/json"
        mv_post.return_value = mv_post_response
        response = MVUploadFileResponse(json)
        mock_instance.upload_file.return_value = response

        result = self.processor._validate_emails_million_verifier()
        self.assertEqual(result, response.file_id)

    @patch('apis.million_verifier.mv.requests.get')
    @patch('apis.million_verifier.mv.MillionVerifier')
    def test_check_file_status_mv_success(self, mock_mv_class, mock_requests_get):
        # Create a mock instance for the MillionVerifier class
        mock_mv_instance = mock_mv_class.return_value
        status: MVStatus = random.choice([MVStatus.success, MVStatus.unknown, MVStatus.in_progress])
        # Mock the response for the API call
        json = {
            "file_id": f"{self.file_id}",
            "file_name": "emails.txt",
            "status": status.value,
            "unique_emails": random.randint(0, 500),
            "updated_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "createdate": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "percent": random.randint(0, 100),
            "total_rows": random.randint(0, 500),
            "verified": random.randint(0, 500),
            "unverified": random.randint(0, 500),
            "ok": random.randint(0, 500),
            "catch_all": random.randint(0, 500),
            "disposable": random.randint(0, 500),
            "invalid": random.randint(0, 500),
            "unknown": random.randint(0, 500),
            "reverify": random.randint(0, 500),
            "credit": random.randint(0, 500),
            "estimated_time_sec": 120,
            "error": ""
        }
        mock_response = Response()
        mock_response.status_code = 200
        # Переконуємося, що response.json() буде працювати правильно
        # Для цього перезаписуємо метод json
        mock_response.json = lambda: json
        mock_requests_get.return_value = mock_response
        byte: bytes
        with open('emails.txt', mode='rb') as b:
            byte = b.read()
        mock_response._content = byte
        mock_response.headers['Content-Type'] = "application/octet-stream"

        # Mock file_status method of MillionVerifier
        mock_status_response = MagicMock()
        mock_status_response.status = status.value
        mock_mv_instance.file_status.return_value = mock_status_response

        # Mock get_file method to return a file object
        file_result = MVGetFileResponse(json)
        mock_mv_instance.get_file.return_value = file_result

        # Set API key and call the method being tested

        result = self.processor._check_file_status('millionverifier')

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.file_name, "emails.txt")

    @patch('app.requests.get')
    def test_million_verifier_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = self.processor._validate_emails_million_verifier()
        self.assertIsNone(result)

    @patch('zerobouncesdk.zerobouncesdk.requests.post')
    @patch('zerobouncesdk.ZeroBounce')
    def test_zerobounce_valid(self, mock_zb_class, mock_post):
        mock_instance = mock_zb_class.return_value
        json = {
          "success": True,
          "message": "File Accepted",
          "file_name": "Your file name.csv",
          "file_id": "aaaaaaaa-zzzz-xxxx-yyyy-5003727fffff"
        }
        mock_instance.send_file.return_value = ZBSendFileResponse(json)
        mv_post_response = Response()
        mv_post_response.status_code = 200
        mv_post_response.json = lambda: json
        mv_post_response.headers['Content-Type'] = "application/json"
        mock_post.return_value = mv_post_response
        result = self.processor._validate_email_zerobounce()
        self.assertEqual(json['file_id'], result)

    @patch('app.requests.get')
    def test_zerobounce_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.processor._validate_email_zerobounce()
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
