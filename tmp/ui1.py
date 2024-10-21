# ui.py
import tkinter as tk
from tkinter import messagebox
from weather import get_weather

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        # Create and place the label, entry, and button
        city_label = tk.Label(root, text="Enter City", fg="red", font=("Arial", 14))
        city_label.pack(pady=10)

        self.city_entry = tk.Entry(root, width=18, justify="left")
        self.city_entry.pack(pady=10)

        get_weather_button = tk.Button(root, text="Get Weather", font=("Arial", 13), command=self.display_weather)
        get_weather_button.pack(pady=10)

        # Create a frame to hold the table
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def display_weather(self):
        city = self.city_entry.get()
        if city:
            current_weather, forecast_info = get_weather(city)
            
            # Clear existing labels in the table_frame
            for widget in self.table_frame.winfo_children():
                widget.destroy()

            if current_weather is None:
                messagebox.showwarning("Error", forecast_info)
                return

            # Create table headers for current weather
            tk.Label(self.table_frame, text="Current Weather", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=3)
            tk.Label(self.table_frame, text="Weather", font=("Arial", 12)).grid(row=1, column=0)
            tk.Label(self.table_frame, text="Temperature (°C)", font=("Arial", 12)).grid(row=1, column=1)
            tk.Label(self.table_frame, text="Humidity (%)", font=("Arial", 12)).grid(row=1, column=2)

            # Insert current weather data
            tk.Label(self.table_frame, text=current_weather[0]).grid(row=2, column=0)
            tk.Label(self.table_frame, text=current_weather[1]).grid(row=2, column=1)
            tk.Label(self.table_frame, text=current_weather[2]).grid(row=2, column=2)

            # Create table headers for forecast weather
            tk.Label(self.table_frame, text="Forecast (Next 24 hours)", font=("Arial", 14, "bold")).grid(row=3, column=0, columnspan=3, pady=(10, 0))
            tk.Label(self.table_frame, text="Time", font=("Arial", 12)).grid(row=4, column=0)
            tk.Label(self.table_frame, text="Weather", font=("Arial", 12)).grid(row=4, column=1)
            tk.Label(self.table_frame, text="Temperature (°C)", font=("Arial", 12)).grid(row=4, column=2)

            # Insert forecast data
            for index, forecast in enumerate(forecast_info):
                tk.Label(self.table_frame, text=forecast[0]).grid(row=5 + index, column=0)
                tk.Label(self.table_frame, text=forecast[1]).grid(row=5 + index, column=1)
                tk.Label(self.table_frame, text=forecast[2]).grid(row=5 + index, column=2)

        else:
            messagebox.showwarning("Input Error", "Please enter a city name")
