import os
import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv

# --- Configuration ---
# Replace 'YOUR_API_KEY' in .env with your actual OpenWeatherMap API Key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Now")
        self.root.geometry("400x450")
        self.root.configure(bg="#f0f0f0")

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Weather App", font=("Helvetica", 20, "bold"), bg="#f0f0f0", pady=20)
        title_label.pack()

        # Search Frame
        search_frame = tk.Frame(self.root, bg="#f0f0f0")
        search_frame.pack(pady=10)

        self.city_entry = tk.Entry(search_frame, font=("Helvetica", 14), width=20)
        self.city_entry.pack(side=tk.LEFT, padx=10)
        self.city_entry.bind('<Return>', lambda event: self.get_weather())

        search_button = tk.Button(search_frame, text="Search", command=self.get_weather, font=("Helvetica", 12), bg="#4caf50", fg="white", padx=10)
        search_button.pack(side=tk.LEFT)

        # Results Area
        self.result_frame = tk.Frame(self.root, bg="#f0f0f0", pady=20)
        self.result_frame.pack(fill=tk.BOTH, expand=True)

        self.city_label = tk.Label(self.result_frame, text="", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        self.city_label.pack()

        self.temp_label = tk.Label(self.result_frame, text="", font=("Helvetica", 40), bg="#f0f0f0")
        self.temp_label.pack()

        self.desc_label = tk.Label(self.result_frame, text="", font=("Helvetica", 14, "italic"), bg="#f0f0f0")
        self.desc_label.pack()

        self.details_label = tk.Label(self.result_frame, text="", font=("Helvetica", 12), bg="#f0f0f0", pady=10)
        self.details_label.pack()

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name.")
            return

        if not API_KEY:
            messagebox.showerror("Error", "Please set your OpenWeatherMap API Key in the script.")
            return

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                messagebox.showerror("Error", f"City '{city}' not found.")
            else:
                messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
        except Exception as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def display_weather(self, data):
        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        self.city_label.config(text=f"{city_name}, {country}")
        self.temp_label.config(text=f"{temp:.1f}°C")
        self.desc_label.config(text=desc)
        self.details_label.config(text=f"Humidity: {humidity}%  |  Wind: {wind_speed} m/s")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
