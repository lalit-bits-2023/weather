import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox
from app.ui import WeatherApp  # Assuming your class is in the ui.py file


class TestWeatherApp(unittest.TestCase):

    def setUp(self):
        # Set up the Tkinter root and WeatherApp instance
        self.root = tk.Tk()
        self.app = WeatherApp(self.root)

    def tearDown(self):
        # Destroy the Tkinter root window after each test
        self.root.destroy()

    @patch('ui.get_weather')  # Mock the get_weather function
    def test_display_weather_success(self, mock_get_weather):
        # Mock the return value for a successful weather call
        mock_get_weather.return_value = (
            ('Clear sky', 25.0, 60),  # Current weather: (description, temp, humidity)
            [
                ('2024-10-20 09:00:00', 'Clear sky', 24.0),
                ('2024-10-20 12:00:00', 'Few clouds', 26.0),
            ]
        )
        
        # Simulate user input
        self.app.city_entry.insert(0, "London")

        # Call the method
        self.app.display_weather()

        # Find the widgets by their row and column in the grid
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

        # Assert the current weather output
        self.assertEqual(current_weather_labels[(2, 0)].cget("text"), "Overcast clouds")
        self.assertEqual(current_weather_labels[(2, 1)].cget("text"), 11.79)
        self.assertEqual(current_weather_labels[(2, 2)].cget("text"), 82)

        # Similarly, check forecast labels
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

        self.assertEqual(forecast_labels[(5, 0)].cget("text"), "2024-11-01 09:00:00")
        self.assertEqual(forecast_labels[(5, 1)].cget("text"), "Overcast clouds")
        self.assertEqual(forecast_labels[(5, 2)].cget("text"), 12.08)  # Convert expected value to string

    @patch('ui.get_weather')
    @patch('tkinter.messagebox.showwarning')  # Mock messagebox.showwarning
    def test_display_weather_city_not_found(self, mock_messagebox, mock_get_weather):
        # Mock the return value for a city not found
        mock_get_weather.return_value = (None, "City not found!")

        # Simulate user input
        self.app.city_entry.insert(0, "UnknownCity")

        # Call the method
        self.app.display_weather()

        # Assert that the warning message was shown
        mock_messagebox.assert_called_once_with("Error", "City not found!")

    @patch('ui.get_weather')
    @patch('tkinter.messagebox.showwarning')
    def test_display_weather_no_city_input(self, mock_messagebox, mock_get_weather):
        # Simulate empty city entry
        self.app.city_entry.delete(0, tk.END)

        # Call the method
        self.app.display_weather()

        # Assert that the warning message was shown for empty input
        mock_messagebox.assert_called_once_with("Input Error", "Please enter a city name")

    @patch('ui.get_weather')
    def test_display_weather_table_cleared(self, mock_get_weather):
        # Mock a successful weather response
        mock_get_weather.return_value = (
            ('Clear sky', 25.0, 60),
            [
                ('2024-10-20 09:00:00', 'Clear sky', 24.0),
                ('2024-10-20 12:00:00', 'Few clouds', 26.0),
            ]
        )

        # Simulate user input
        self.app.city_entry.insert(0, "London")

        # Populate the table with some data first
        self.app.display_weather()

        # Call the method again to ensure the table is cleared before repopulating
        self.app.display_weather()

        # Assert that the table contains exactly the new set of labels (6 for current weather, additional for forecast)
        self.assertGreaterEqual(len(self.app.table_frame.winfo_children()), 6)

    
if __name__ == '__main__':
    unittest.main()
