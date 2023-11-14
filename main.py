import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttkb
font_name1 = "Arial"
font_name2 = "Impact"
font_name3 = "Georgia"
def fetch_weather(city_name):
    api_key = "d454ea7978d7bfc6867281125ca53fa5"
    api_addr = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    request_to_respond = requests.get(api_addr)

    if request_to_respond.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    weather_info = request_to_respond.json()
    icon_id = weather_info['weather'][0]['icon']
    temperature = weather_info['main']['temp'] - 273.15
    description = weather_info['weather'][0]['description']
    city = weather_info['name']
    country = weather_info['sys']['country']

    icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temperature, description, city, country)

def display_weather_update():
    city_name = city_name_entry.get()
    result = fetch_weather(city_name)
    if result is None:
        return

    icon_url, temperature, description, city, country = result
    location_widget.config(text=f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    weather_icon = ImageTk.PhotoImage(image)
    icon_place.config(image=weather_icon)
    icon_place.image = weather_icon

    temp_widget.config(text=f"Temperature: {temperature:.2f}°C")
    details_widget.config(text=f"Condition: {description}")

root = ttkb.Window(themename="darkly")
root.title("Weather App")
root.geometry("700x500")
root.resizable(False, False)


city_name_entry = tk.StringVar()

city_entry = ttkb.Entry(root, font=(font_name3, 15, "bold"), textvariable=city_name_entry, width=30)
city_entry.pack(ipadx=10, ipady=8, pady=20)
city_entry.focus_set()
search_button = ttkb.Button(root, text="Search", bootstyle="info", command=display_weather_update)
search_button.pack(pady=10, padx=40)
location_widget = tk.Label(root, font=(font_name2, 30, "bold"))
location_widget.pack()
icon_place = tk.Label(root)
icon_place.pack(pady=10)
temp_widget = tk.Label(root, font=(font_name1, 18))
temp_widget.pack()
details_widget = tk.Label(root, font=(font_name1, 16, "italic"))
details_widget.pack()

root.mainloop()
