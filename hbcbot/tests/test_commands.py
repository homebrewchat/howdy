import unittest
from unittest.mock import patch

from hbcbot import commands


class TestAbv(unittest.TestCase):
    def test_pastryboi(self):
        abv = commands._abv(1.135, 1.045)
        abv = round(abv, 1)
        self.assertEqual(abv, 14.1)


class TestBrix(unittest.TestCase):
    def test_brix(self):
        brix = commands._brix_to_og(31.2)
        brix = round(brix, 3)
        self.assertEqual(brix, 1.135)


class TestHydrometer(unittest.TestCase):
    def test_hyadj(self):
        ag = commands._hydro_temp_adj(1.131, 90, 60)
        ag = round(ag, 3)
        self.assertEqual(ag, 1.135)


class TestUntappd(unittest.TestCase):
    @patch("hbcbot.commands.requests.get")
    @patch.dict(
        "os.environ",
        {
            "UNTAPPD_CLIENT_ID": "mock_client_id",
            "UNTAPPD_CLIENT_SECRET": "mock_client_secret",
        },
    )
    def test_untappd_with_valid_input(self, mock_get):
        # Mock the response from the API
        expected_data = {"response": {"beers": {"items": [{"beer": {"bid": "12345"}}]}}}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        # Test the function with valid input
        args = "Heineken"
        expected_output = "https://untappd.com/beer/12345"
        self.assertEqual(commands.untappd(args), expected_output)

    @patch("hbcbot.commands.requests.get")
    @patch.dict(
        "os.environ",
        {
            "UNTAPPD_CLIENT_ID": "mock_client_id",
            "UNTAPPD_CLIENT_SECRET": "mock_client_secret",
        },
    )
    def test_untappd_with_invalid_input(self, mock_get):
        # Mock the response from the API
        expected_data = {}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        # Test the function with invalid input
        args = "Invalid Beer Name"
        expected_output = "Type in beer name accurately"
        self.assertEqual(commands.untappd(args), expected_output)

    @patch.dict(
        "os.environ",
        {
            "UNTAPPD_CLIENT_ID": "mock_client_id",
            "UNTAPPD_CLIENT_SECRET": "mock_client_secret",
        },
    )
    def test_untappd_api_call(self):
        # Test the API call made by the function
        args = "Heineken"
        expected_api_url = "https://api.untappd.com/v4/search/beer?q=Heineken&client_id=mock_client_id&client_secret=mock_client_secret"
        with patch("hbcbot.commands.requests.get") as mock_get:
            commands.untappd(args)
            mock_get.assert_called_with(expected_api_url)

    @patch.dict(
        "os.environ",
        {
            "UNTAPPD_CLIENT_ID": "mock_client_id",
            "UNTAPPD_CLIENT_SECRET": "mock_client_secret",
        },
    )
    def test_no_args(self):
        expected = "Usage: .untappd <beer name>"
        result = untappd(None)
        self.assertEqual(result, expected)

class TestFX(unittest.TestCase):
    @patch('hbcbot.commands.requests.get')
    def test_no_args(self):
        expected = "Usage: .fx <AMOUNT> <FROM> <TO>"
        result = conv_fx(None)
        self.assertEqual(result, expected)

    @patch('hbcbot.commands.requests.get')
    def test_invalid_args(self):
        expected = "Usage: .fx <AMOUNT> <FROM> <TO>"
        result = conv_fx(['100'])
        self.assertEqual(result, expected)

    @patch.dict(
        "os.environ",
        {
            "AV_KEY": "mock_key"
        },
    )
    def test_mocked_api_call_with_valid_input(self):
        args = ['100', 'USD', 'EUR']
        expected_api_url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey=mock_key"
        with patch('hbcbot.commands.requests.get') as mock_get:
            commands.conv_fx(args)
            mock_get.assert_called_with(expected_api_url)
 
class TestStonks(unittest.TestCase):
    @patch('hbcbot.commands.requests.get')
    def test_no_args(self):
        expected = "Usage: .q <STONK>"
        result = stonks(None)
        self.assertEqual(result, expected)

    @patch('hbcbot.commands.requests.get')
    def test_invalid_args(self):
        expected = "Usage: .q <STONK>"
        result = stonks('AAPLAAPL')
        self.assertEqual(result, expected)

    @patch.dict(
        "os.environ",
        {
            "AV_KEY": "mock_key"
        },
    )
    def test_mocked_api_call_with_valid_input(self):
        args = ['AAPL']
        expected_api_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=mock_key"
        with patch('hbcbot.commands.requests.get') as mock_get:
            commands.stonks(args)
            mock_get.assert_called_with(expected_api_url)

 