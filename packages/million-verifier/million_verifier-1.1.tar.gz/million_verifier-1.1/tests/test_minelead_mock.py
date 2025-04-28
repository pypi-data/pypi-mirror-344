import os
import unittest
from unittest.mock import patch, MagicMock
from app import CompanyDatabaseProcessor, CompanyRow, add_translation


class TestMineLeadDiscovery(unittest.TestCase):

    def setUp(self):
        self.processor = CompanyDatabaseProcessor()
        self.processor.mineLead_api_key = "FAKE_API_KEY"
        tmp_dir = "temp"
        path = self.create_temp_csv(tmp_dir)
        add_translation()
        self.processor.import_csv(path)
        self.processor.filter_generic_emails()
        self.processor.analyze_data()

    def create_temp_csv(self, tmp_dir) -> str:
        os.makedirs(tmp_dir, exist_ok=True)
        file_path = os.path.join(tmp_dir, "test.csv")
        return file_path

    @patch('app.requests.get')
    def test_mineLead_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "domain": "example.com",
            "status": "found",
            "pattern": "{first}@example.com",
            "emails": [dict(email="ceo@example.com")]
        }
        mock_get.return_value = mock_response
        test_row = CompanyRow(email="ceo@example.com",
                              first_name="ceo@example.com".split('@')[0].split('.')[0].capitalize(),
                        url="example.com")
        self.processor.rows = [(CompanyRow(url="example.com", email_status="Generic Email"))]
        result = self.processor.mineLead_email_discovery()
        self.processor.analyze_data()
        self.assertIn(test_row, result)

        self.processor.export_csv("test.csv")
        mock_get.assert_called()

    @patch('app.requests.get')
    def test_mineLead_server_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        self.processor.rows = [CompanyRow(url="example.com")]
        success = self.processor.mineLead_email_discovery()

        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
