import unittest
from unittest.mock import patch, MagicMock
import json
from webjsondatagetter import setup_driver, login, fetch_json_data, filter_json_content, save_json_to_file, CustomError

class TestSeleniumCurl(unittest.TestCase):

    @patch('webjsondatagetter.webdriver.Chrome')
    def test_setup_driver(self, MockWebDriver):
        driver = setup_driver()
        self.assertIsNotNone(driver)
        MockWebDriver.assert_called_once()

    @patch('webjsondatagetter.WebDriverWait')
    @patch('webjsondatagetter.webdriver.Chrome')
    def test_login(self, MockWebDriver, MockWebDriverWait):
        driver = MockWebDriver()
        MockWebDriverWait().until.return_value = True
        driver.find_element.return_value = MagicMock()
        login(driver, 'http://example.com/login', 'user', 'pass')
        driver.get.assert_called_with('http://example.com/login')

    @patch('webjsondatagetter.WebDriverWait')
    @patch('webjsondatagetter.webdriver.Chrome')
    def test_fetch_json_data(self, MockWebDriver, MockWebDriverWait):
        driver = MockWebDriver()
        MockWebDriverWait().until.return_value = True
        driver.find_element.return_value.text = '{"key": "value"}'
        result = fetch_json_data(driver, 'http://example.com/data')
        self.assertEqual(result, '{"key": "value"}')

    def test_filter_json_content(self):
        json_content = '[{"module": "LuxaSim16-01", "data": "value1"}, {"module": "OtherModule", "data": "value2"}]'
        filtered_content = filter_json_content(json_content, 'LuxaSim16-01')
        expected_content = json.dumps([{"module": "LuxaSim16-01", "data": "value1"}], indent=4)
        self.assertEqual(filtered_content, expected_content)

    @patch('builtins.open', unittest.mock.mock_open())
    def test_save_json_to_file(self):
        json_content = '{"key": "value"}'
        save_json_to_file(json_content, 'dummy_path')
        open.assert_called_with('dummy_path', 'w')
        open().write.assert_called_with(json_content)

if __name__ == '__main__':
    unittest.main()
