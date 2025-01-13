from application import (
    open_application,
    search_in_browser,
    handle_action_based_on_query,
    get_active_window,
    search_in_active_application
)
from model import handle_model_query
from weather import get_weather
from whatsapp import call_whatsapp_contact,send_whatsapp_message
import email_program
from speech import speak,listen
import pygetwindow as gw
import time
import pyautogui
import re
from commands import handle_typing,press_keys

# Global flag to track continuous typing mode
continuous_typing_mode = False

def close_application(query):
    """
    Closes the specified application if it's open.
    """
    try:
        app_name = query.split("close", 1)[1].strip().lower()
        windows = gw.getAllWindows()
        
        for window in windows:
            title = window.title.lower()
            
            # Check if the app name is in the window title
            if app_name in title:
                try:
                    window.close()
                    time.sleep(1)
                    return True
                except:
                    window.kill()  # Force close if normal close fails
                    time.sleep(1)
                    return True
                    
        # If we reach here, no matching window was found
        print(f"Could not find '{app_name}' running.")
        return False
        
    except Exception as e:
        print(f"Error closing application: {str(e)}")
        return False

def extract_email_or_contact(query):
    # Check for an email pattern
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', query)
    if email_match:
        return email_match.group(0)  # Return the email address


def handle_query(query):
    """
    Handles various queries related to opening apps, searching websites, and performing actions.
    """
    global continuous_typing_mode
    query = query.lower()
    
    # Get active window context
    active_window = get_active_window()
    
    # Handle continuous typing and type once commands
    if "start typing" in query:
        continuous_typing_mode = True  # Enable continuous typing mode
        print("Started typing...")
    
    elif "stop typing" in query:
        continuous_typing_mode = False  # Disable continuous typing mode
        print("Stopped typing.")
    
    elif "type" in query and continuous_typing_mode:
        # If continuous typing mode is active, keep typing
        handle_typing(query, continuous=True)
    
    elif "type" in query:
        # If it's a single typing action
        handle_typing(query, continuous=False)

    # Handle close application command
    elif "close" in query:
        close_application(query)
        
    # Handle key press commands like "press control + t"
    elif "press" in query:
        press_keys(query)
    
    # First check if the query matches a known command for opening applications
    elif "open" in query:
        open_application(query)
    
    elif "message" in query:
        send_whatsapp_message()

    elif "call" in query:
        call_whatsapp_contact()

    elif "send mail" in query or "write mail" in query:
        email_program.open_mail_ui()

    # Handle search commands with context awareness
    elif "search for" in query:
        if "google search for" in query:
            search_in_browser(query)
        elif active_window and search_in_active_application(query):
            pass  # Search already performed in active application
        else:
            search_in_browser(query)
    
    # Handle action commands (scroll, play first video, etc.)
    elif "scroll down" in query or "open first result" in query or "play first video" in query or "scroll up" in query or "play this video" in query:
        handle_action_based_on_query(query)

    elif any(weather_query in query for weather_query in ["weather", "how is the weather", "what is the weather", "how's the weather", "is it raining", "what's the weather like"]):
        weather_response = get_weather()
        print(f"Weather: {weather_response}")

    
    else:
        try:
            response = handle_model_query(query, voice_output=True)
            print(f"AI: {response}")
        except Exception as e:
            print(f"Error getting AI response: {str(e)}")
            print(f"Query '{query}' not recognized.")
