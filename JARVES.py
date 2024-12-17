import pyttsx3
import wikipediaapi
from googletrans import Translator
import requests
import speech_recognition as sr
import datetime

# Initialize Wikipedia, Translator, and Text-to-Speech engine
wiki = wikipediaapi.Wikipedia('en-US')
translator = Translator()
engine = pyttsx3.init()

# OpenWeatherMap API Key
API_KEY = "your_openweathermap_api_key_here"  # Replace with your OpenWeatherMap API Key

# Function to convert text to speech
def speak(text, language='en', whisper=False):
    if whisper:
        engine.setProperty('volume', 0.3)  # Whisper mode
    else:
        engine.setProperty('volume', 1.0)  # Normal mode
    
    # Set voice based on language
    voices = engine.getProperty('voices')
    if language == 'hi':
        engine.setProperty('voice', voices[1].id)  # Assuming voice[1] supports Hindi
    else:
        engine.setProperty('voice', voices[0].id)  # Default voice for English
    
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech in both Hindi and English
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Processing...")
            # Recognize speech using Hindi-English support
            text = recognizer.recognize_google(audio, language="hi-IN,en-IN")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please repeat.")
            return None
        except sr.RequestError:
            speak("Network error. Try again.")
            return None

# Function to detect the spoken language
def detect_language(text):
    if all('\u0900' <= char <= '\u097F' for char in text):  # Detect Hindi script
        return 'hi'
    else:
        return 'en'

# Function to fetch Wikipedia summaries
def get_wikipedia_summary(query, language):
    translated_query = query
    if language == 'hi':
        translated_query = translator.translate(query, src='hi', dest='en').text

    # Fetch Wikipedia summary
    page = wiki.page(translated_query)
    if page.exists():
        summary = page.summary
        if language == 'hi':
            summary = translator.translate(summary, src='en', dest='hi').text
        return summary
    else:
        return "Sorry, no information is available on this topic." if language == 'en' else "माफ़ कीजिए, इस विषय पर जानकारी उपलब्ध नहीं है।"

# Function to fetch weather information
def get_weather(city, language):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']

        weather_info = (f"The current weather in {city} is {weather} with a temperature of {temperature}°C, "
                        f"feels like {feels_like}°C, and humidity of {humidity}%.")
        if language == 'hi':
            weather_info = translator.translate(weather_info, src='en', dest='hi').text
        return weather_info
    else:
        return "Unable to fetch weather data. Check the city name." if language == 'en' else "मौसम की जानकारी प्राप्त नहीं हो सकी। कृपया शहर का नाम जांचें।"

# Function to announce daily activities
def daily_activities(language):
    now = datetime.datetime.now()
    if language == 'en':
        speak(f"Good day! Today's date is {now.strftime('%B %d, %Y')}, and the time is {now.strftime('%I:%M %p')}.", language)
        speak("Here is a motivational quote: 'The future depends on what you do today.'", language)
    else:
        speak(f"नमस्ते! आज की तारीख है {now.strftime('%d %B, %Y')} और समय है {now.strftime('%I:%M %p')}.", language)
        speak("यहाँ एक प्रेरणादायक उद्धरण है: 'भविष्य इस बात पर निर्भर करता है कि आप आज क्या करते हैं।'", language)

# Wake word listener
def wake_word_listener():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'JARVES' to activate...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="en-IN,hi-IN").lower()
                if "jarves" in command or "जार्विस" in command:
                    print("JARVES Activated!")
                    speak("Hello, I am JARVES. How can I assist you?", language='en')
                    return True
            except sr.UnknownValueError:
                pass  # Ignore unrecognized audio
            except sr.RequestError:
                print("Speech recognition service unavailable.")
                return False

# Main function
def main():
    while True:
        if wake_word_listener():
            while True:
                speak("What would you like to do? Wikipedia, Weather, Daily Activities, Whisper mode, or Exit.", language='en')
                task = listen()

                if task:
                    language = detect_language(task)

                    if "विकिपीडिया" in task or "wikipedia" in task:
                        speak("What topic would you like to search?", language)
                        query = listen()
                        if query:
                            result = get_wikipedia_summary(query, language)
                            speak("Here is what I found.", language)
                            print(result)
                            speak(result, language)
                    elif "मौसम" in task or "weather" in task:
                        speak("Please tell me the city name.", language)
                        city = listen()
                        if city:
                            result = get_weather(city, language)
                            speak(result, language)
                    elif "daily" in task or "activities" in task or "दैनिक" in task:
                        daily_activities(language)
                    elif "whisper" in task or "धीरे बोलो" in task:
                        speak("Whisper mode activated. I will speak softly now.", language, whisper=True)
                    elif "exit" in task or "बाहर निकलो" in task:
                        speak("Goodbye!", language)
                        return
                    else:
                        speak("I didn't understand. Please try again.", language)

if __name__ == "__main__":
    main()
