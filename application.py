import os
import pyautogui
import pygetwindow as gw
import time
from speech import speak

def get_active_window():
    """
    Returns the title of the currently active window.
    """
    try:
        active_window = gw.getActiveWindow()
        return active_window.title.lower() if active_window else None
    except:
        return None

def search_in_active_application(query):
    """
    Performs a search based on the currently active application window.
    """
    active_window = get_active_window()
    search_term = query.split("search for", 1)[1].strip()

    if active_window:
        if "youtube" in active_window:
            # If YouTube is active, use YouTube's search
            pyautogui.hotkey('/', '')  # Focus YouTube search
            time.sleep(0.5)
            pyautogui.write(search_term)
            pyautogui.press('enter')
            speak("opening youtube")
            return True
        elif "whatsapp" in active_window:
            # If WhatsApp is active, use WhatsApp's search
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.write(search_term)
            return True
        elif "amazon" in active_window:
            # If Amazon is active, use Amazon's search
            pyautogui.click(x=500, y=60)  # Adjust coordinates for Amazon search bar
            time.sleep(0.5)
            pyautogui.write(search_term)
            pyautogui.press('enter')
            return True
        elif "vlc" in active_window:
            # If VLC is active, use playlist search
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.write(search_term)
            return True
    return False

def open_application(query):
    """
    Opens the specified application (browser or desktop application).
    """
    if "whatsapp" in query:
        pyautogui.hotkey('win')
        time.sleep(2)
        pyautogui.write('whatsapp')
        time.sleep(1)
        pyautogui.press('enter')
    elif "chrome" in query or "browser" in query:
        os.system("start chrome")
        speak("Opening Chrome")
        time.sleep(3)  # Wait for Chrome to open
    elif "spotify" in query or "play music" in query:
        os.system("start spotify")
        speak("Opening spotify")
        time.sleep(3)
        pyautogui.press('space')
    elif "vlc" in query:
        os.system("start vlc")
        speak("opening vlc")
        time.sleep(3)  # Wait for VLC to open
    elif "clipchamp" in query:
        os.system("start clipchamp")
        speak("Opening clipchamp")
        time.sleep(3)  # Wait for Clipchamp to open
    elif "amazon" in query:
        os.system("start https://www.amazon.com")
        time.sleep(3)  # Wait for Amazon to open
    elif "youtube" in query:
        os.system("start https://www.youtube.com")
        speak("Opening youtube")
        time.sleep(3)  # Wait for YouTube to open
    else:
        print(f"Application '{query}' not recognized.")

def search_in_browser(query):
    """
    Search for specific topics in the browser or active application.
    """
    # If explicitly asking for Google search
    if "google search for" in query:
        search_topic = query.split("search for", 1)[1].strip()
        os.system(f'start chrome https://www.google.com/search?q={search_topic}')
        speak("searching")
        time.sleep(3)
        return

    # Try to search in active application first
    if "search for" or "search" in query and search_in_active_application(query):
        return

    # If no active application or search not handled, proceed with default search behavior
    if "search for" in query:
        if "youtube" in query:
            search_video = query.split("search for", 1)[1].strip()
            os.system(f'start https://www.youtube.com/results?search_query={search_video}')
        elif "amazon" in query:
            search_item = query.split("search for", 1)[1].strip()
            os.system(f'start https://www.amazon.com/s?k={search_item}')
        elif "wikipedia" in query:
            search_article = query.split("search for", 1)[1].strip()
            os.system(f'start https://www.wikipedia.org/wiki/{search_article}')
        else:
            search_topic = query.split("search for", 1)[1].strip()
            os.system(f'start chrome https://www.google.com/search?q={search_topic}')
        time.sleep(3)
    else:
        print(f"Search functionality for '{query}' not implemented yet.")

def scroll_down():
    """
    Simulates a scroll down action in the browser or any open window.
    """
    pyautogui.scroll(-500)  # Scroll down by 500 units (adjust as needed)

def scroll_up():
    pyautogui.scroll(+500)

def screenshot():
    pyautogui.screenshot()
    

def open_first_result_in_chrome():
    """
    Opens the first result in Google Chrome after a search.
    """
    pyautogui.hotkey('ctrl', 't')  # Open a new tab in Chrome
    time.sleep(1)
    pyautogui.write('https://www.google.com')  # Type the URL of Google
    pyautogui.press('enter')  # Press Enter to go to Google
    time.sleep(3)
    pyautogui.moveTo(500, 300)  # Move the mouse to the first search result (adjust coordinates)
    pyautogui.click()  # Click the first result
    time.sleep(3)

def play_first_video_on_youtube():
    """
    Play the first video on YouTube after performing a search.
    """
    # Assuming YouTube search results are loaded in the browser
    pyautogui.moveTo(500, 350)  # Move to the first video on YouTube (adjust coordinates)
    pyautogui.click()  # Click the first video to play
    time.sleep(3)

def open_website(query):
    """
    Open websites based on the query.
    """
    if "youtube" in query:
        os.system("start https://www.youtube.com")
        time.sleep(3)
    elif "amazon" in query:
        os.system("start https://www.amazon.com")
        time.sleep(3)
    elif "wikipedia" in query:
        os.system("start https://www.wikipedia.org")
        time.sleep(3)
    else:
        print(f"Website '{query}' not recognized.")

def handle_action_based_on_query(query):
    """
    Main function to handle all search and action queries.
    """
    if "search for" in query:
        search_in_browser(query)
    elif "open" in query:
        if "website" in query or any(site in query for site in ["youtube", "amazon", "wikipedia"]):
            open_website(query)
        else:
            open_application(query)
    elif "scroll down" in query:
        scroll_down()
    elif "scroll up" in query:
        scroll_up()
    elif "open first result" in query:
        open_first_result_in_chrome()
    elif "play first video" in query:
        play_first_video_on_youtube()
    else:
        print("No valid action found for the query.")

# Example usage:
if __name__ == "__main__":
    while True:
        query = input("Enter your command (or 'exit' to quit): ").lower()
        if query == 'exit':
            break
        handle_action_based_on_query(query)