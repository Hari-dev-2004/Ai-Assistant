import json
import time
import random
from speech import listen, speak
from query_handler import handle_query

def load_queries(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        speak("Query file not found.")
        return {}

def main():
    query_file = 'local_queries.json'
    predefined_queries = load_queries(query_file)
    speak("Hello! How can I assist you today?") # Set the interval for greetings (in seconds)

    while True:

        query = listen().lower()
        if not query.strip():
            continue

        response = predefined_queries.get(query)
        if response is not None:
            speak(response)
        elif query in ["what is your name", "who are you", "who are you", "hu r u"]:
            speak("I am Eris, I am ai based assistant,your dude!!")
        elif query in ["exit", "quit", "stop", "bye"]:
            speak("Goodbye!")
            break
        else:
            handle_query(query)

if __name__ == "__main__":
    main()
