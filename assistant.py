import wikipediaapi
from googletrans import Translator
import requests
import pyttsx3
import speech_recognition as sr

# Initialize Wikipedia, Translator, and Text-to-Speech engine
wiki = wikipediaapi.Wikipedia('en')
translator = Translator()
engine = pyttsx3.init()

# OpenWeatherMap API Key
API_KEY = "your_openweathermap_api_key_here"  # Replace with your OpenWeatherMap API Key

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and convert it to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("I am listening, please speak.")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("Processing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, I am having trouble accessing speech recognition services.")
            return None

# Function to fetch Wikipedia summaries
def get_wikipedia_summary(query, user_language):
    if user_language == 'hi':
        translated_query = translator.translate(query, src='hi', dest='en').text
        print(f"Translating '{query}' to '{translated_query}'...")
    else:
        translated_query = query

    # Fetch Wikipedia summary
    page = wiki.page(translated_query)
    if page.exists():
        if user_language == 'hi':
            summary = translator.translate(page.summary, src='en', dest='hi').text
        else:
            summary = page.summary
        return summary
    else:
        return "Sorry, no information is available on this topic." if user_language == 'en' else "माफ़ कीजिए, इस विषय पर जानकारी उपलब्ध नहीं है।"

# Function to fetch weather information
def get_weather(city, user_language):
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
        
        if user_language == 'hi':
            weather_info = translator.translate(weather_info, src='en', dest='hi').text
        return weather_info
    else:
        return "Unable to fetch weather data. Please check the city name." if user_language == 'en' else "मौसम की जानकारी प्राप्त करने में असमर्थ। कृपया शहर का नाम जांचें।"

def main():
    # Choose language
    speak("Choose your language. Say 'English' for English or 'Hindi' for Hindi.")
    print("Choose your language: English or Hindi")
    language_input = listen()
    if language_input and "hindi" in language_input.lower():
        user_language = 'hi'
        speak("आपने हिंदी चुनी है।")
        print("आपने हिंदी चुनी है।")
    else:
        user_language = 'en'
        speak("You have selected English.")
        print("You have selected English.")

    # Start the assistant loop
    while True:
        if user_language == 'en':
            speak("What would you like to do? Say 'Wikipedia' for Wikipedia search, 'Weather' for weather info, or 'Exit' to quit.")
        else:
            speak("आप क्या करना चाहते हैं? विकिपीडिया खोजने के लिए 'विकिपीडिया' कहें, मौसम की जानकारी के लिए 'मौसम' कहें, या बाहर निकलने के लिए 'बाहर निकलें' कहें।")

        print("Listening for your choice...")
        task_choice = listen()

        if task_choice:
            # Wikipedia Search
            if "wikipedia" in task_choice.lower() or ("विकिपीडिया" in task_choice.lower() and user_language == 'hi'):
                if user_language == 'en':
                    speak("What topic would you like to search on Wikipedia?")
                    print("What topic would you like to search?")
                else:
                    speak("आप विकिपीडिया पर किस विषय को खोजना चाहेंगे?")
                    print("आप विकिपीडिया पर किस विषय को खोजना चाहेंगे?")
                
                query = listen()
                if query:
                    result = get_wikipedia_summary(query, user_language)
                    speak("Here is what I found.")
                    print(result)
                    speak(result)

            # Weather Information
            elif "weather" in task_choice.lower() or ("मौसम" in task_choice.lower() and user_language == 'hi'):
                if user_language == 'en':
                    speak("Please tell me the name of the city.")
                    print("Enter the city name:")
                else:
                    speak("कृपया मुझे शहर का नाम बताएं।")
                    print("शहर का नाम दर्ज करें:")

                city = listen()
                if city:
                    result = get_weather(city, user_language)
                    speak("Here is the weather information.")
                    print(result)
                    speak(result)

            # Exit
            elif "exit" in task_choice.lower() or ("बाहर निकलें" in task_choice.lower() and user_language == 'hi'):
                if user_language == 'en':
                    speak("Goodbye!")
                else:
                    speak("अलविदा!")
                break

            # Invalid Option
            else:
                if user_language == 'en':
                    speak("I didn't understand that. Please try again.")
                    print("Invalid option. Please try again.")
                else:
                    speak("मुझे समझ नहीं आया। कृपया पुनः प्रयास करें।")
                    print("अमान्य विकल्प। कृपया पुनः प्रयास करें।")

if _name_ == "_main_":
    main()