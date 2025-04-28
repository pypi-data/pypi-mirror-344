import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from app import CompanyDatabaseProcessor, CompanyRow

class TestCompanyDatabaseProcessorFull(unittest.TestCase):

    def setUp(self):
        self.processor = CompanyDatabaseProcessor()
        self.processor.minelead_api_key = "FAKE_KEY"
        self.processor.million_verifier_api_key = "FAKE_KEY"
        self.processor.zero_bounce_api_key = "FAKE_KEY"
        self.processor.google_api_key = "FAKE_KEY"
        self.processor.google_cse_id = "FAKE_ID"
        tmp_dir = "temp"
        path = self.create_temp_csv(tmp_dir, None)
        self.processor.import_csv(path)

    def create_temp_csv(self, tmp_dir, content: str=None) -> str:
        os.makedirs(tmp_dir, exist_ok=True)
        file_path = os.path.join(tmp_dir, "test.csv")
        return file_path

    def test_set_api_keys(self):
        self.processor.set_api_keys(million_verifier_api_key="key1", zero_bounce_api_key="key2")
        self.assertEqual(self.processor.million_verifier_api_key, "key1")
        self.assertEqual(self.processor.zero_bounce_api_key, "key2")

    def test_parse_emails_from_websites_empty(self):
        self.processor.df = pd.DataFrame(columns=['website', 'email'])
        success = self.processor.parse_emails_from_websites()
        self.assertTrue(success)

    @patch('app.requests.get')
    def test_parse_emails_from_websites_scrape(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html>ceo@example.com</html>"
        mock_get.return_value = mock_response

        self.processor.df = pd.DataFrame([{
            'url': 'http://example.com',
            'email': None,
            'company_name': 'Test Company'
        }])

        success = self.processor.parse_emails_from_websites()
        self.assertTrue(success)
        self.assertIn('ceo@example.com', self.processor.df.loc[0, 'email'])

    def test_scrape_website_no_url(self):
        result = self.processor._scrape_website(None)
        self.assertEqual(result['status'], 'No URL provided')
        self.assertEqual(result['emails'], [])

    def test_is_email_relevant(self):
        text = "Our top architect is available: ceo@company.com"
        relevant = self.processor._is_email_relevant('ceo@company.com', text)
        self.assertTrue(relevant)

    @patch('app.requests.get')
    def test_find_websites_for_companies(self, mock_get):
        mock_response = MagicMock()
        mock_response.execute.return_value = {
            'items': [{'link': 'http://foundsite.com'}]
        }
        mock_service = MagicMock()
        mock_service.cse.return_value.list.return_value = mock_response

        with patch('app.build', return_value=mock_service):
            self.processor.df = pd.DataFrame([{
                'name': 'Test Company',
                'website': None,
                'email': None
            }])

            success = self.processor.find_websites_for_companies()
            self.assertTrue(success)

    def test_export_by_state(self):
        tmp_dir = "temp"
        os.makedirs(tmp_dir, exist_ok=True)

        self.processor.df = pd.DataFrame([
            {'name': 'A', 'state': 'CA'},
            {'name': 'B', 'state': 'TX'},
            {'name': 'C', 'state': 'CA'}
        ])

        success = self.processor.export_by_state(tmp_dir)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(tmp_dir, "CA.csv")))
        self.assertTrue(os.path.exists(os.path.join(tmp_dir, "TX.csv")))

    # def test_load_from_company_rows(self):
    #     rows = [
    #         CompanyRow(name="Test Company 1", email="test1@test.com"),
    #         CompanyRow(name="Test Company 2", email="test2@test.com")
    #     ]
    #     self.processor.load_from_company_rows(rows)
    #     self.assertEqual(len(self.processor.df), 2)
    #     self.assertEqual(self.processor.df.iloc[0]['email'], "test1@test.com")

if __name__ == "__main__":
    unittest.main()
