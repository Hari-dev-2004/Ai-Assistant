import http.client
import json
import re
from speech import speak, listen

# RapidAPI credentials
RAPIDAPI_KEY = "6fbffe8419msh0fce495ef13c2f7p19bb87jsn909207c34db3"
RAPIDAPI_HOST = "open-weather13.p.rapidapi.com"

def fetch_weather_data(city):
    """
    Fetches weather data for the specified city using the Open Weather API on RapidAPI.
    """
    try:
        # Set up connection
        conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
        
        # Configure headers with RapidAPI key
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }
        
        # Send GET request for the specified city
        conn.request("GET", f"/city/{city}/EN", headers=headers)
        
        # Read and parse response data
        res = conn.getresponse()
        data = res.read()
        weather_data = json.loads(data.decode("utf-8"))

        # Check if response contains an error or city not found
        if weather_data.get("message") or not weather_data.get("main"):
            message = f"Could not retrieve weather for {city}. Reason: {weather_data.get('message', 'Unknown error')}"
            speak(message)
            return message
        
        # Extract required weather details
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        # Convert temperature from Kelvin to Celsius if needed (API response is in Kelvin by default)
        temp_celsius = temp - 273.15
        
        # Format weather information in Celsius
        weather_info = (f"The current temperature in {city.capitalize()} is {temp_celsius:.2f}°C with {description}. "
                        f"Humidity is at {humidity}%, and the wind speed is {wind_speed} meters per second.")
        
        # Speak and return the weather information
        speak(weather_info)
        return weather_info
                
    except Exception as e:
        error_message = f"Error fetching weather data: {str(e)}"
        speak(error_message)
        return error_message

def get_weather():
    """
    Listens for a weather query from the user, identifies the city, and retrieves the weather data.
    """
    speak("Please ask about the weather in a city.")
    query = listen()  # Capture user's voice input
    print(f"User query: {query}")
    
    # Attempt to detect the city directly from the query, ignoring additional details
    city_match = re.search(r"weather in ([a-zA-Z\s]+)", query)
    
    # If regex didn't find a city, use the entire query as the city name
    city = city_match.group(1).strip() if city_match else query.strip()
    
    # Fetch and return the weather data for the identified city
    return fetch_weather_data(city)
