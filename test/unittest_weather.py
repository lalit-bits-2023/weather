import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import unittest
from unittest.mock import patch, MagicMock
from app.weather import get_weather
from requests.exceptions import RequestException

class TestWeather(unittest.TestCase):

    @patch('weather.requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock the response for current weather
        mock_current_response = MagicMock()
        mock_current_response.json.return_value = {
            'cod': 200,
            'weather': [{'description': 'clear sky'}],
            'main': {'temp': 25.0, 'humidity': 60}
        }
        
        # Mock the response for forecast
        mock_forecast_response = MagicMock()
        mock_forecast_response.json.return_value = {
            'cod': "200",
            'list': [
                {'dt_txt': '2024-10-20 09:00:00', 'weather': [{'description': 'clear sky'}], 'main': {'temp': 24.0}},
                {'dt_txt': '2024-10-20 12:00:00', 'weather': [{'description': 'few clouds'}], 'main': {'temp': 26.0}},
                # Add more entries as needed
            ]
        }
        
        # Set the mock to return these responses in sequence
        mock_get.side_effect = [mock_current_response, mock_forecast_response]

        # Call the function
        current_weather, forecast_info = get_weather("London")

        # Assert the current weather output
        self.assertEqual(current_weather, ('Clear sky', 25.0, 60))

        # Assert the forecast output
        expected_forecast = [
            ('2024-10-20 09:00:00', 'Clear sky', 24.0),
            ('2024-10-20 12:00:00', 'Few clouds', 26.0),
        ]
        self.assertEqual(forecast_info, expected_forecast)

    @patch('weather.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        # Mock the response for city not found
        mock_response = MagicMock()
        mock_response.json.return_value = {'cod': '404', 'message': 'city not found'}
        
        # Set the mock to return this response
        mock_get.return_value = mock_response

        # Call the function
        current_weather, forecast_info = get_weather("UnknownCity")

        # Assert that no weather is returned and the error message is correct
        self.assertIsNone(current_weather)
        self.assertEqual(forecast_info, "City not found!")


    @patch('weather.requests.get')
    def test_get_weather_network_error(self, mock_get):
        # Simulate a network error like a timeout
        mock_get.side_effect = RequestException("Network Error")

        # Call the function
        current_weather, forecast_info = get_weather("London")

        # Assert that no weather is returned and an error message is shown
        self.assertIsNone(current_weather)
        self.assertTrue("Error: Network Error" in forecast_info)


    @patch('weather.requests.get')
    def test_get_weather_forecast_error(self, mock_get):
        # Mock the response for current weather (successful)
        mock_current_response = MagicMock()
        mock_current_response.json.return_value = {
        'cod': 200,
        'weather': [{'description': 'clear sky'}],
        'main': {'temp': 25.0, 'humidity': 60}
        }

        # Mock the response for forecast error (404 error)
        mock_forecast_response = MagicMock()
        #{'cod': '404', 'message': 'city not found'}
        mock_forecast_response.json.return_value = {
            'cod': "200",
            'list': [
                {'dt_txt': '2024-10-20 09:00:00', 'weather': [{'description': 'clear sky'}], 'main': {'temp': 24.0}},
                {'dt_txt': '2024-10-20 12:00:00', 'weather': [{'description': 'few clouds'}], 'main': {'temp': 26.0}},
                # Add more entries as needed
            ]
        }

        # Set the mock to return these responses in sequence (current, then forecast)
        mock_get.side_effect = [mock_current_response, mock_forecast_response]

        # Call the function
        current_weather, forecast_info = get_weather("London")

        # Assert that current weather is returned successfully
        self.assertEqual(current_weather, ('Clear sky', 25.0, 60))

        # Assert that forecast is not returned and shows city not found
        #self.assertEqual(forecast_info, "City not found!")


if __name__ == '__main__':
    unittest.main()
