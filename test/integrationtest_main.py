import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from app.ui import WeatherApp
from app.weather import get_weather

class TestWeatherAppIntegration(unittest.TestCase):

    @patch('ui.get_weather')  # Mock the get_weather function in ui.py
    def setUp(self, mock_get_weather):
        # Set up a mock return value for get_weather
        mock_get_weather.return_value = (
            ('Clear sky', 25.0, 60),  # Current weather: (description, temp, humidity)
            [
                ('2024-10-20 09:00:00', 'Clear sky', 24.0),
                ('2024-10-20 12:00:00', 'Few clouds', 26.0),
            ]
        )
        
        # Create the Tkinter root window and WeatherApp
        self.root = tk.Tk()
        self.app = WeatherApp(self.root)
    
    def tearDown(self):
        # Close the Tkinter window after each test
        self.root.quit()
        self.root.update()

    def test_integration_weather_display(self):
        # Simulate entering the city name
        #self.app.city_entry.insert(0, "London")
        
        # Simulate pressing the 'Get Weather' button
        self.app.display_weather()

        # Check if the current weather data is displayed correctly
        current_weather_labels = {
            (2, 0): None,  # Weather description
            (2, 1): None,  # Temperature
            (2, 2): None,  # Humidity
        }

        for widget in self.app.table_frame.winfo_children():
            info = widget.grid_info()
            row = info.get("row")
            column = info.get("column")
            if (row, column) in current_weather_labels:
                current_weather_labels[(row, column)] = widget

        # Assert that current weather is displayed correctly
        self.assertEqual(current_weather_labels[(2, 0)].cget("text"), "Mist")
        self.assertEqual(current_weather_labels[(2, 1)].cget("text"), 28.2)
        self.assertEqual(float(current_weather_labels[(2, 2)].cget("text")), 90.0)

        # Check if the forecast data is displayed correctly
        forecast_labels = {
            (5, 0): None,  # First forecast time
            (5, 1): None,  # First forecast description
            (5, 2): None,  # First forecast temperature
        }

        for widget in self.app.table_frame.winfo_children():
            info = widget.grid_info()
            row = info.get("row")
            column = info.get("column")
            if (row, column) in forecast_labels:
                forecast_labels[(row, column)] = widget

        # Assert that the forecast weather is displayed correctly
        self.assertEqual(forecast_labels[(5, 0)].cget("text"), "2024-12-02 06:00:00")
        self.assertEqual(forecast_labels[(5, 1)].cget("text"), "Light rain")
        self.assertEqual(float(forecast_labels[(5, 2)].cget("text")), 28.33)


if __name__ == '__main__':
    unittest.main()
