import tkinter as tk
import speech_recognition as sr
import pyttsx3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from flask import Flask
from flask_mail import Mail, Message
import threading

# Initialize Flask app
app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "harimarathi224@gmail.com"  # Replace with your email
app.config['MAIL_PASSWORD'] = "wnzekwqkrwbltikk"  # Replace with your app password
mail = Mail(app)

# Initialize the Groq client
client = Groq(api_key="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")

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()

# Predefined recipient emails
PREDEFINED_RECIPIENTS = {
    "john": "john.doe@example.com",
    "alice": "alice.smith@example.com",
    "bob": "bob.jones@example.com",
    "Hari": "knaik7720@gmail.com",
}

# Function to handle text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for speech input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speak("Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            
            # Replace "at" with "@" for email addresses
            if " at " in text:
                text = text.replace(" at ", "@")
            
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            listen()
        except sr.RequestError:
            speak("There was an error with the speech recognition service.")
            return None

# Function to generate the email body using Llama AI via Groq
def generate_email(recipient_name, email_topic):
    try:
        query = f"Write a formal email to {recipient_name} about '{email_topic}'. Include a subject line and body in the response, and the sender name is 'Hari'."
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": query}],
            temperature=0.7,
            max_tokens=1024
        )

        response_text = completion.choices[0].message.content.strip()
        
        # Extract the subject and body
        subject = ""
        body = response_text
        if "Subject:" in response_text:
            parts = response_text.split("Subject:", 1)
            subject = parts[1].split("\n", 1)[0].strip()
            body = parts[1].split("\n", 1)[1].strip()
        
        return subject, body
    except Exception as e:
        speak("Error generating email content.")
        return f"Error: {e}", ""

# Function to send the email using Flask-Mail
def send_email(to_email, subject, body, window):
    try:
        with app.app_context():
            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to_email])
            msg.body = body
            mail.send(msg)
        speak("Email sent successfully!")
        window.destroy()
    except Exception as e:
        speak(f"Failed to send email: {e}")

# Function to handle email workflow in a background thread
def handle_email_flow(window, to_entry, subject_entry, body_text):
    # Ask for the recipient email address
    speak("Please provide the email address to send the email to.")
    to_email = listen()

    # Update the recipient field in the GUI
    to_entry.delete(0, tk.END)
    to_entry.insert(0, to_email)

    # Ask for the recipient's name
    speak("What is the recipient's name?")
    recipient_name = listen()

    # Ask for the topic of the email
    speak(f"What is the topic of the email to {recipient_name}?")
    email_topic = listen()

    # Generate the email content
    speak("Generating the email. Please wait.")
    email_subject, email_body = generate_email(recipient_name, email_topic)

    # Update the subject and body fields in the GUI
    subject_entry.delete(0, tk.END)
    subject_entry.insert(0, email_subject)
    body_text.delete("1.0", tk.END)
    if "Error:" not in email_subject:
        body_text.insert("1.0", email_body)
    else:
        body_text.insert("1.0", "Failed to generate email. Please try again.")

    # Ask for confirmation to send the email
    speak("Would you like to send this email? Say 'yes' to send or 'no' to cancel.")
    confirmation = listen()

    if confirmation and ("yes" in confirmation or "send" in confirmation):
        send_email(to_email, email_subject, email_body)
    else:
        speak("Email sending canceled.")

# Function to open the email GUI
def open_mail_ui():
    window = tk.Tk()
    window.title("Voice-based Email Sender")

    # UI Elements
    to_label = tk.Label(window, text="To:")
    to_label.pack()
    to_entry = tk.Entry(window)
    to_entry.pack()

    subject_label = tk.Label(window, text="Subject:")
    subject_label.pack()
    subject_entry = tk.Entry(window)
    subject_entry.pack()

    body_label = tk.Label(window, text="Body:")
    body_label.pack()
    body_text = tk.Text(window)
    body_text.pack()

    # Start the email flow in a background thread to keep the GUI responsive
    email_thread = threading.Thread(target=handle_email_flow, args=(window, to_entry, subject_entry, body_text))
    email_thread.daemon = True
    email_thread.start()

    window.mainloop()

# Main function
if __name__ == "__main__":
    open_mail_ui()
