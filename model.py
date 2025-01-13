from groq import Groq
from speech import listen, speak
from detection import detect_emotion_and_gender
import threading

# Initialize the Groq client
client = Groq(api_key="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")

# Start emotion and gender detection in a separate thread
emotion = "neutral"
gender = "unknown"

def start_emotion_detection():
    global emotion, gender
    while True:
        current_emotion, current_gender, user_id = detect_emotion_and_gender()
        if current_emotion and current_gender:
            emotion = current_emotion
            gender = current_gender
            print(f"Updated Emotion: {emotion}, Gender: {gender}")

# Start the detection thread
detection_thread = threading.Thread(target=start_emotion_detection)
detection_thread.daemon = True
detection_thread.start()

def get_concise_answer(user_input):
    return f"{user_input} (give response briefly in 1-2 sentences)"

def get_detailed_answer(user_input):
    return f"explain in detail: {user_input}"

def detect_query_type(query):
    """
    Detects if a query is informational or conversational.
    
    Returns:
        str: 'informational' or 'conversational'
    """
    informational_keywords = ["tell me", "explain", "what is", "who is", "details on", "information about"]
    for keyword in informational_keywords:
        if keyword in query.lower():
            return 'informational'
    return 'conversational'

def handle_model_query(query, voice_output=False):
    """
    Handle queries using Groq model, adding context of emotion and gender.
    
    Args:
        query (str): User's query
        voice_output (bool): Whether to use speech output
    
    Returns:
        str: Model's response
    """
    try:
        global emotion, gender
        
        # Determine query type and process accordingly
        query_type = detect_query_type(query)
        
        if query_type == 'informational':
            processed_query = get_concise_answer(query)
        else:
            processed_query = (f"{query}. Respond shortly with a sarcastic and playful tone, considering "
                               f"the user is feeling {emotion} and is a {gender}.")
        
        # Call the model with the processed query
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": processed_query}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )
        
        # Collect response text
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        
        # Use voice output if enabled
        if voice_output:
            speak(response_text)
        
        return response_text
    
    except Exception as e:
        error_msg = f"Error getting model response: {str(e)}"
        print(error_msg)
        return error_msg

def get_model_response():
    """Interactive chat function with voice support and emotion/gender handling"""
    print("AI: Hi! How can I assist you today?")
    last_answer = None
    
    while True:
        user_input = listen().strip().lower()
        
        # Exit on 'exit' command
        if user_input == "exit":
            speak("Goodbye!")
            print("AI: Goodbye!")
            break

        # Check if the user wants a detailed response for the last answer
        if last_answer and ("detail" in user_input or "explain more" in user_input or 
                            "describe" in user_input or "explain in detail" in user_input):
            user_input = get_detailed_answer(last_answer)
        else:
            user_input = get_concise_answer(user_input)
        
        # Get model response with emotion and gender context
        response_text = handle_model_query(user_input, voice_output=True)
        print("AI: " + response_text)
        
        # Store last answer for potential follow-up requests
        last_answer = response_text

if __name__ == "__main__":
    get_model_response()
