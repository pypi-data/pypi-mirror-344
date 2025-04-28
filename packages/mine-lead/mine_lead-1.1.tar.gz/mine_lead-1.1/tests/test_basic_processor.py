import os
import unittest

from app import CompanyDatabaseProcessor


class TestCompanyDatabaseProcessorBasic(unittest.TestCase):

    def setUp(self):
        self.processor = CompanyDatabaseProcessor()

    def create_temp_csv(self, tmp_dir, content: str=None) -> str:
        os.makedirs(tmp_dir, exist_ok=True)
        file_path = os.path.join(tmp_dir, "test.csv")
        return file_path

    def test_import_csv_success(self):
        tmp_dir = "temp"
        path = self.create_temp_csv(tmp_dir, None)

        success = self.processor.import_csv(path)
        self.assertTrue(success)
        self.assertIsNotNone(self.processor.df)

    def test_analyze_data_empty(self):
        stats = self.processor.analyze_data()
        self.assertIsNone(stats)

    def test_filter_generic_emails(self):
        tmp_dir = "temp"
        csv_content = """company_name,website,email,state
Company,example.com,info@example.com,CA
"""
        path = self.create_temp_csv(tmp_dir, csv_content)

        self.processor.import_csv(path)
        self.processor.filter_generic_emails()

        generic_emails = [row for row in self.processor.rows if row.email_status == "Generic Email"]
        self.assertEqual(len(generic_emails), 1)

if __name__ == "__main__":
    unittest.main()
