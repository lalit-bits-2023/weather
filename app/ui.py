import tkinter as tk
from tkinter import messagebox
from app.weather import get_weather

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        # Create a frame for central alignment
        main_frame = tk.Frame(root)
        main_frame.pack(pady=20)  # Add some padding to the main frame

        # Create and place the label, entry, and button
        city_label = tk.Label(main_frame, text="Enter City", fg="black", font=("Arial", 13, "bold"))
        city_label.pack(pady=10)

        self.city_entry = tk.Entry(main_frame, width=18, justify="center")  # Center text in entry
        self.city_entry.pack(pady=10)

        get_weather_button = tk.Button(main_frame, text="Get Weather", font=("Arial", 13, "bold"), command=self.display_weather)
        get_weather_button.pack(pady=10)

        # Create a frame to hold the table
        self.table_frame = tk.Frame(main_frame)  # Nest table frame within main_frame
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
            tk.Label(self.table_frame, text="Weather", font=("Arial", 12)).grid(row=1, column=0, sticky="ew")
            tk.Label(self.table_frame, text="Temperature (°C)", font=("Arial", 12)).grid(row=1, column=1, sticky="ew")
            tk.Label(self.table_frame, text="Humidity (%)", font=("Arial", 12)).grid(row=1, column=2, sticky="ew")

            # Insert current weather data
            tk.Label(self.table_frame, text=current_weather[0]).grid(row=2, column=0, sticky="ew")
            tk.Label(self.table_frame, text=current_weather[1]).grid(row=2, column=1, sticky="ew")
            tk.Label(self.table_frame, text=current_weather[2]).grid(row=2, column=2, sticky="ew")

            # Create table headers for forecast weather
            tk.Label(self.table_frame, text="Forecast (Next 24 hours)", font=("Arial", 14, "bold")).grid(row=3, column=0, columnspan=3, pady=(10, 0))
            tk.Label(self.table_frame, text="Time", font=("Arial", 12)).grid(row=4, column=0, sticky="ew")
            tk.Label(self.table_frame, text="Weather", font=("Arial", 12)).grid(row=4, column=1, sticky="ew")
            tk.Label(self.table_frame, text="Temperature (°C)", font=("Arial", 12)).grid(row=4, column=2, sticky="ew")

            # Insert forecast data
            for index, forecast in enumerate(forecast_info):
                tk.Label(self.table_frame, text=forecast[0]).grid(row=5 + index, column=0, sticky="ew")
                tk.Label(self.table_frame, text=forecast[1]).grid(row=5 + index, column=1, sticky="ew")
                tk.Label(self.table_frame, text=forecast[2]).grid(row=5 + index, column=2, sticky="ew")

            # Configure column weight to allow equal distribution
            for i in range(3):  # Assuming you have 3 columns
                self.table_frame.grid_columnconfigure(i, weight=1)

        else:
            messagebox.showwarning("Input Error", "Please enter a city name")