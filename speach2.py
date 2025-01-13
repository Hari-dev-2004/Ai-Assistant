import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time

# Global variables to store the latest conversation
query = ""
text = ""

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
    tts = gTTS(text=text_input, lang="en")
    filename = "response.mp3"
    tts.save(filename)
    
    # Initialize pygame mixer and play audio
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)  # Allow for smooth checking

    # Quit pygame mixer and remove the file
    pygame.mixer.music.unload()
    pygame.mixer.quit()
    os.remove(filename)

# Getter functions to retrieve the latest query and assistant response
def get_query():
    return query

def get_response():
    return text
