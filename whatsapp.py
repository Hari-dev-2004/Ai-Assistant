from speech import listen, speak
import pyautogui
import time

def send_whatsapp_message():
    """
    Sends a WhatsApp message to the specified contact.
    """
    speak("What is the contact name?")
    contact_name = listen()

    if contact_name:
        speak("What is the message you want to send?")
        message = listen()

        if message:
            speak(f"You want to send the message '{message}' to {contact_name}. Is this correct?")
            confirmation = listen()

            if "yes" in confirmation.lower():
                send_whatsapp_message_to_contact(contact_name, message)
                speak("Message sent successfully.")
            else:
                speak("Message not sent.")

def send_whatsapp_message_to_contact(contact_name, message):
    pyautogui.press('win')
    pyautogui.write('whatsapp')
    pyautogui.press('enter')
    time.sleep(2)
    # Search for the contact
    pyautogui.click(100, 150)  # Click on the search bar
    pyautogui.write(contact_name)
    time.sleep(2)
    pyautogui.keyDown('down')
    time.sleep(1)
    pyautogui.press('enter')
    
    # Type the message and send it
    pyautogui.click(400, 900)
    pyautogui.write(message)
    pyautogui.press('enter')

def call_whatsapp_contact():
    """
    Calls a WhatsApp contact.
    """
    speak("What is the contact name?")
    contact_name = listen()

    if contact_name:
        call_whatsapp_contact_by_name(contact_name)
        speak(f"Calling {contact_name} on WhatsApp.")

def call_whatsapp_contact_by_name(contact_name):
    """
    Calls a WhatsApp contact.
    
    Parameters:
    contact_name (str): Name of the WhatsApp contact to call.
    """
    # Open WhatsApp web
    pyautogui.press('win')
    pyautogui.write('whatsapp')
    pyautogui.press('enter')
    time.sleep(2)
    # Search for the contact
    pyautogui.click(100, 150)  # Click on the search bar
    pyautogui.write(contact_name)
    time.sleep(2)
    pyautogui.keyDown('down')
    time.sleep(1)
    pyautogui.press('enter')
    
    # Click the call button
    pyautogui.click(400, 500)  # Click on the call button