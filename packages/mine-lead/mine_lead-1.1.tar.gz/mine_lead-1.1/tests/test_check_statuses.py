import datetime
import json
import random
import unittest
import uuid
from unittest.mock import patch, MagicMock

from million_verifier import MVStatus, MVGetFileResponse
from million_verifier.exceptions import MVApiException
from requests import Response
from zerobouncesdk import ZBGetFileResponse

from app import CompanyDatabaseProcessor


class TestCheckStatusesFull(unittest.TestCase):

    def setUp(self):
        self.processor = CompanyDatabaseProcessor()
        self.processor.df = "mock_df"
        self.processor.million_verifier_api_key = "FAKE_API_KEY"
        self.processor.zero_bounce_api_key = "FAKE_API_KEY"
        self.processor.output_path = "output.csv"
        self.processor.zb_file_id = str(uuid.uuid4())
        self.processor.mv_file_id = str(random.randint(0, 9999))

    @patch('zerobouncesdk.zerobouncesdk.requests.get')
    @patch('zerobouncesdk.ZeroBounce')
    def test_check_file_status_zero_bounce_success(self, mock_zero_bounce, mv_get):
        mock_instance = mock_zero_bounce.return_value
        mock_response = Response()
        mock_response.status_code = 200
        json = {
            "success": True,
            "file_id": "aaaaaaaa-zzzz-xxxx-yyyy-5003727fffff",
            "file_name": "zb_result.csv",
            "upload_date": "2023-04-28T15:25:41Z",
            "file_status": "Complete",
            "complete_percentage": "100%",
            "return_url": "Your return URL if provided when calling sendfile API"
        }
        mock_response.headers['Content-Type'] = "application/json"
        mock_response.json = lambda: json
        mv_get.return_value = mock_response
        mock_instance.file_status.return_value = mock_response
        mock_instance.get_file.return_value = mock_response

        result = self.processor._check_file_status("zerobounce")

        self.assertEqual(result.file_name, "zb_result.csv")

    @patch('zerobouncesdk.zerobouncesdk.requests.get')
    @patch('zerobouncesdk.ZeroBounce')
    def test_check_file_status_zero_bounce_failure(self, mock_zero_bounce, mv_get):
        # Мокаємо інстанс ZeroBounce
        mock_instance = mock_zero_bounce.return_value
        # Створюємо мок відповіді
        mock_response = Response()
        mock_response.status_code = 400
        mock_response.headers['Content-Type'] = "application/json"
        json ={
            "success": False,
            "error_message": "Error messages"
        }
        mock_response.json = lambda: json
        mv_get.return_value = mock_response
        mock_status_response = MagicMock()
        mock_instance.file_status.return_value = mock_status_response
        # Mock get_file method to return a file object
        file_result = ZBGetFileResponse(json)
        mock_instance.get_file.return_value = file_result
        result = self.processor._check_file_status('zerobounce')

        self.assertIsNone(result)

    @patch('million_verifier.MillionVerifier.requests.get')
    @patch('million_verifier.MillionVerifier.MillionVerifier')
    def test_check_file_status_mv_success(self, mock_mv_class, mock_requests_get):
        # Create a mock instance for the MillionVerifier class
        mock_mv_instance = mock_mv_class.return_value
        status: MVStatus = random.choice([MVStatus.success, MVStatus.unknown, MVStatus.in_progress])
        # Mock the response for the API call
        json = {
          "file_id": "940",
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

        result = self.processor._check_file_status('million_verifier')

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.file_name, "emails.txt")


    @patch('million_verifier.MillionVerifier.MillionVerifier')
    def test_check_file_status_mv_exception(self, mock_mv):
        mock_instance = mock_mv.return_value
        mock_instance.file_status.side_effect = MVApiException("Test Exception")

        self.processor.million_verifier_api_key = "fake_key"
        result = self.processor._check_file_status("million_verifier")

        self.assertIsNone(result)

    @patch('app.CompanyDatabaseProcessor._check_file_status')
    def test_check_statuses_both_success(self, mock_zb):
        mock_zb.return_value = MagicMock(local_file_path="zb_file.csv")
        result = self.processor.check_statuses('both')

        self.assertIsNone(result)
        mock_zb.assert_called_once()

    @patch('app.CompanyDatabaseProcessor._check_file_status')
    def test_check_statuses_only_zb(self, mock_zb):
        mock_zb.return_value = MagicMock(local_file_path="zb_file.csv")

        self.processor.million_verifier_api_key = None
        self.processor.zero_bounce_api_key = "key"

        result = self.processor.check_statuses('zerobounce')

        self.assertIsNone(result)
        mock_zb.assert_called_once()

    @patch('app.CompanyDatabaseProcessor._check_file_status')
    def test_check_statuses_only_mv(self, mock_mv):
        mock_mv.return_value = MagicMock(local_file_path="mv_file.csv")

        result = self.processor.check_statuses('million_verifier')

        self.assertIsNone(result)
        mock_mv.assert_called_once()

    def test_check_statuses_invalid_provider(self):
        self.processor.million_verifier_api_key = "key"
        self.processor.zero_bounce_api_key = "key"

        result = self.processor.check_statuses('invalid')
        self.assertFalse(result)

    def test_check_statuses_no_df(self):
        processor = CompanyDatabaseProcessor()
        processor.million_verifier_api_key = "key"
        processor.zero_bounce_api_key = "key"

        result = processor.check_statuses('both')
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
