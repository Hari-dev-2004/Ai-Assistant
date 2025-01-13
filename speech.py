import speech_recognition as sr
import pyttsx3
import os
import time
import json

# Global variables to store the latest conversation
query = ""
text = ""

json_file_path = "conversation_data.json"  # File to save conversation data

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

def save_conversation(query, response):
    conversation = {
        "user_query": query,
        "assistant_response": response
    }

    # Overwrite the existing data with only the current conversation
    with open(json_file_path, 'w') as file:
        json.dump(conversation, file, indent=4)  # Only save the latest conversation

def listen():
    global query
    recognizer = sr.Recognizer()
    print("Listening...")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            query = ""  # Empty query if not recognized
            return ""
        except sr.RequestError:
            print("Could not request results; check your network.")
            query = ""  # Empty query if request fails
            return ""

def speak(text_input):
    global text
    print("Assistant:", text_input)
    text = text_input  # Store the assistant's response in the global variable

    # Save conversation data before speaking
    save_conversation(query, text_input)  # Save data before speaking starts

    # Use pyttsx3 for text-to-speech
    engine.say(text_input)
    engine.runAndWait()

# Getter functions to retrieve the latest query and assistant response
def get_query():
    return query

def get_response():
    return text
