import speech_recognition as sr
import pyttsx3
import wikipedia
import pyjokes
import requests
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
# Function to listen to microphone input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print(e)
        print("Sorry, I didn't get that. Please try again.")
        return "None"
    return query.lower()


# Function to speak out the response
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function to process user commands
def process_text(input_text):
    if 'wikipedia' in input_text:
        speak("Searching Wikipedia...")
        input_text = input_text.replace("wikipedia", "")
        results = wikipedia.summary(input_text, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'joke' in input_text:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)

    elif 'weather' in input_text:
        speak("Please specify the city name")
        city = listen()
        get_weather(city)

    elif 'news' in input_text:
        get_news()

    elif 'bye' in input_text or 'exit' in input_text or 'quit' in input_text:
        speak("Goodbye!")
        exit()

    elif 'time please' in input_text:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        codePath = 'C:\\Users\\Alok Ray\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
        os.startfile(codePath)

    elif 'open spotify' in query:
        codePath = 'C:\\Users\\Alok Ray\\AppData\\Roaming\\Spotify\\Spotify.exe'
        os.startfile(codePath)

    elif 'play music' in query:
        music_dir = 'C:\\Users\\Alok Ray\\Music\\Musics'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))

    elif 'open photos' in input_text:
        photo_dir = 'C:\\Users\\Alok Ray\\OneDrive\\Pictures'
        os.startfile(photo_dir)

    elif 'play my favorite' in query:
        music_dir = 'C:\\Users\\Alok Ray\\Music\\Musics\\MyMusics'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile(os.path.join(music_dir, songs[0]))

    elif 'open youtube' in input_text:
        webbrowser.open("youtube.com")

    elif 'open google' in input_text:
        webbrowser.open("google.com")

    elif 'open github' in input_text:
        webbrowser.open("github.com")

    elif 'open instagram' in input_text:
        webbrowser.open("instagram.com")

    elif 'open chat gpt' in input_text:
        webbrowser.open("chatgpt.com")

    elif 'thank you' in input_text or 'thanks' in input_text or 'thank' in input_text:
        speak("You are Welcome boss!")

    else:
        speak("Sorry, Please repeat.")


# Function to fetch weather information
def get_weather(city):
    api_key = 'cc736ce1f7c302bfc6324c93f1110cb0'  # Replace with your OpenWeatherMap API key
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    weather_data = response.json()

    if weather_data['cod'] == '404':
        speak("City not found.")
        return

    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    weather_report = f"The weather in {city} is currently {description}. "
    weather_report += f"The temperature is {temperature} degrees Celsius, with humidity at {humidity} percent."

    print(weather_report)
    speak(weather_report)


# Function to fetch latest news headlines
def get_news():
    api_key = 'a0eb480bb309413aa4a6ef3cae6bb43c'  # Replace with your News API key
    url = f'http://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        articles = news_data['articles']
        for idx, article in enumerate(articles[:5], start=1):
            title = article['title']
            speak(f"News {idx}: {title}")
            print(f"News {idx}: {title}")
    else:
        speak("Sorry, I couldn't fetch the latest news.")


# Main execution loop
if __name__ == "__main__":
    print("------------------------------------------------")
    print("Hello! I am Jarvis. How can I assist you today?")
    print("------------------------------------------------")
    speak("Hello! I am Jarvis. How can I assist you today?")

    while True:
        query = listen()
        process_text(query)
