import requests
import pyttsx3
import pyautogui
import geocoder
import time
import nltk
import os
import subprocess
import threading
import webbrowser
import ollama
from pygame.locals import *
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

class Chatbot:
    def __init__(self):
        self.text_to_speech = TextToSpeech()
        self.speech_recognition = SpeechRecognition()
        self.weather_api = WeatherAPI()
        self.nlp_tool = NLPTool()
        self.geolocation = Geolocation()
        self.app_launcher = AppLauncher()
        self.reminder = Reminder()
        self.notes = Notes()
        self.search_tool = SearchTool()
        self.file_search = FileSearch()
        self.code_writer = CodeWriter()
        self.file_uploader = FileUploader()

    def main(self):
        print("Welcome to the Chatbot! Select an option:")
        print("1. Get Weather\n2. Speech Recognition\n3. Text-to-Speech\n4. Open Application\n5. Get Geolocation\n6. Search the Web\n7. Search for a File\n8. Desktop Mouse Click\n9. Set Reminder\n10. Take Notes\n11. Generate ML/AI Code\n12. Upload File for Model Training\n13. Upload File for Code Generation\n14. Exit")

        while True:
            user_input = input("You: ")

            if user_input == "1":
                location = self.geolocation.get_location()
                if location:
                    weather_info = self.weather_api.get_weather_by_coords(location[0], location[1])
                    print(f"Weather at your location: {weather_info}")
                else:
                    print("Could not retrieve your location.")

            elif user_input == "2":
                text = self.speech_recognition.recognize()
                if text:
                    print(f"Chatbot: {text}")
                    response = self.nlp_tool.analyze_sentiment(text)
                    print(f"Sentiment Analysis Score: {response['compound']}")
                else:
                    print("Could not recognize speech.")

            elif user_input == "3":
                text = input("Enter a message: ")
                self.text_to_speech.speak(text)

            elif user_input == "4":
                available_apps = self.app_launcher.list_installed_apps()
                print("Available Applications:")
                for idx, app in enumerate(available_apps, 1):
                    print(f"{idx}. {app}")
                app_choice = int(input("Select an application number to open: "))
                if 1 <= app_choice <= len(available_apps):
                    self.app_launcher.open_application(available_apps[app_choice - 1])
                else:
                    print("Invalid selection.")

            elif user_input == "5":
                location = self.geolocation.get_location()
                if location:
                    print(f"Latitude: {location[0]}, Longitude: {location[1]}")
                else:
                    print("Could not retrieve location.")

            elif user_input == "6":
                query = input("Enter your search query: ")
                self.search_tool.search_web(query)

            elif user_input == "7":
                filename = input("Enter the filename to search for: ")
                directory = input("Enter the directory to search in (leave blank for root directory): ")
                directory = directory if directory else os.path.expanduser("~")
                found_files = self.file_search.search_file(filename, directory)
                if found_files:
                    print("Found files:")
                    for file in found_files:
                        print(file)
                else:
                    print("No files found.")

            elif user_input == "8":
                x, y = map(int, input("Enter mouse coordinates (x, y): ").split())
                self.geolocation.click(x, y)
                print(f"Clicked at: ({x}, {y})")

            elif user_input == "9":
                reminder_time = input("Enter reminder time (HH:MM format): ")
                message = input("Enter reminder message: ")
                self.reminder.set_reminder(reminder_time, message)
                print("Reminder set successfully!")

            elif user_input == "10":
                note = input("Enter your note: ")
                self.notes.add_note(note)
                print("Note saved successfully!")

            elif user_input == "11":
                model_type = input("Enter ML/AI model type (e.g., CNN, Decision Tree, Transformer): ")
                code = self.code_writer.generate_code(model_type)
                print("Generated Code:")
                print(code)

            elif user_input == "12":
                file_path = input("Enter the file path for model training: ")
                self.file_uploader.upload_file(file_path)

            elif user_input == "13":
                file_path = input("Enter the file path for code generation: ")
                code = self.code_writer.generate_code_from_file(file_path)
                print("Generated Code:")
                print(code)

            elif user_input == "14":
                print("Exiting Chatbot...")
                break

            else:
                print("Invalid option. Please try again.")

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


class SpeechRecognition:
    def __init__(self):
        pass

    def recognize(self):
        return input("(Simulated Speech Recognition) Type what you said: ")


class WeatherAPI:
    def __init__(self):
        self.api_key = "EnterAPI"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather_by_coords(self, lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        if "main" in data and "weather" in data:
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"Weather: {weather_desc}, Temperature: {temperature}°C"
        else:
            return "Could not retrieve weather data."


class NLPTool:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, text):
        return self.sia.polarity_scores(text)


class Geolocation:
    def __init__(self):
        pass

    def get_location(self):
        try:
            g = geocoder.ip("me")
            if g.ok and g.latlng:
                return g.latlng
            else:
                print("Could not retrieve location using geocoder. Trying an alternative method...")
                response = requests.get("https://ipinfo.io/json")
                data = response.json()
                if "loc" in data:
                    lat, lon = map(float, data["loc"].split(","))
                    return [lat, lon]
                else:
                    return None
        except Exception as e:
            print(f"Error retrieving location: {e}")
            return None

    def click(self, x, y):
        pyautogui.click(x, y)


class AppLauncher:
    def __init__(self):
        pass

    def list_installed_apps(self):
        if os.name == "nt":
            output = subprocess.run("powershell Get-StartApps", capture_output=True, text=True, shell=True)
            return [line.split(None, 1)[-1] for line in output.stdout.splitlines()[3:] if line.strip()]
        elif os.uname().sysname == "Darwin":
            return os.listdir("/Applications")
        else:
            output = subprocess.run("ls /usr/share/applications", capture_output=True, text=True, shell=True)
            return [app.replace(".desktop", "") for app in output.stdout.splitlines()]

    def open_application(self, app_name):
        try:
            os.system(
                f"start {app_name}" if os.name == "nt" else f"open -a {app_name}" if os.uname().sysname == "Darwin" else f"xdg-open {app_name}")
            print(f"Opening {app_name}...")
        except Exception as e:
            print(f"Error opening application: {e}")


class Reminder:
    def __init__(self):
        self.reminders = []

    def set_reminder(self, time_str, message):
        reminder_time = datetime.strptime(time_str, "%H:%M").time()
        threading.Thread(target=self.check_reminder, args=(reminder_time, message)).start()

    def check_reminder(self, reminder_time, message):
        while True:
            now = datetime.now().time()
            if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                print(f"Reminder: {message}")
                break
            time.sleep(30)

class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)
        with open("notes.txt", "a") as file:
            file.write(note + "\n")

class FileSearch:
    def __init__(self):
        pass

    def search_file(self, filename, directory):
        found_files = []
        for root, dirs, files in os.walk(directory):
            if filename in files:
                found_files.append(os.path.join(root, filename))
        return found_files

class SearchTool:
    def __init__(self):
        pass

    def search_web(self, query):
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        print(f"Searching for: {query}")

class FileUploader:
    def __init__(self):
        pass

    def upload_file(self, file_path):
        if os.path.exists(file_path):
            print(f"File '{file_path}' uploaded successfully for training.")
        else:
            print("File not found. Please enter a valid file path.")

class CodeWriter:
    def __init__(self):
        pass

    def generate_code(self, model_type):
        prompt = f"Generate a Python script for {model_type} using popular libraries like TensorFlow, PyTorch, or Scikit-Learn. Include training and evaluation steps."
        response = ollama.chat(model='codellama', messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

    def generate_code_from_file(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                file_content = file.read()
            prompt = f"Generate a Python script based on the following content:\n{file_content}"
            response = ollama.chat(model='codellama', messages=[{"role": "user", "content": prompt}])
            return response['message']['content']
        else:
            return "File not found. Please enter a valid file path."

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.main()
