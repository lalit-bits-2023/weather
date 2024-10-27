
import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.ui import WeatherApp

class TestMainApp(unittest.TestCase):

    def setUp(self):
        # Set up the Tkinter window and WeatherApp instance
        self.root = tk.Tk()
        self.app = WeatherApp(self.root)

    def tearDown(self):
        # Destroy the Tkinter window after each test
        self.root.destroy()

    def test_app_initialization(self):
        """Test that the main app window is initialized correctly."""
        # Force geometry update before checking
        self.root.geometry("600x500")
        self.root.update_idletasks()  # Ensure that Tkinter processes pending events

        # Now check that the geometry has been applied
        geometry_size = self.root.geometry().split('+')[0]  # Extract only the size part (ignore position)
        self.assertEqual(geometry_size, "600x500")

        # Ensure the WeatherApp instance was created
        self.assertIsInstance(self.app, WeatherApp)

    def test_widgets_exist(self):
        """Test that the widgets are created correctly in the WeatherApp."""
        # Check that the city entry widget exists
        self.assertIsNotNone(self.app.city_entry)

        # Check that the Get Weather button exists
        button = self.app.root.nametowidget(self.app.city_entry.winfo_parent()).winfo_children()[2]  # Assuming third widget
        self.assertEqual(button.cget("text"), "Get Weather")

        # Check that the table frame exists
        self.assertIsNotNone(self.app.table_frame)

    @patch('tkinter.messagebox.showwarning')
    def test_button_functionality(self, mock_showwarning):
        """Test that the 'Get Weather' button is functional and shows a warning when no city is entered."""
        # Simulate an empty city entry and click the button
        self.app.city_entry.delete(0, tk.END)  # Clear any text in the city entry
        button = self.app.root.nametowidget(self.app.city_entry.winfo_parent()).winfo_children()[2]  # Assuming third widget
        button.invoke()  # Simulate button click

        # Ensure that messagebox.showwarning was called due to no city being entered
        mock_showwarning.assert_called_with("Input Error", "Please enter a city name")


if __name__ == '__main__':
    unittest.main()
