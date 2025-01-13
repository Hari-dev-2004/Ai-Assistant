import pyttsx3

def text_to_speech_with_bass(text):
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Get available voices
        voices = engine.getProperty('voices')
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"{i}: {voice.name}")

        # Select a deeper voice (modify the index as per the output)
        engine.setProperty('voice', voices[0].id)  # Change to 1, 2, etc., based on preference

        # Adjust speech rate (optional)
        engine.setProperty('rate', 120)  # Slow down for more impact

        # Adjust volume (optional)
        engine.setProperty('volume', 1.0)  # Set volume (range: 0.0 to 1.0)

        # Speak the text
        engine.say(text)
        engine.runAndWait()

        print("Speech completed successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
text = "dttt,dddd,td"
text_to_speech_with_bass(text)
