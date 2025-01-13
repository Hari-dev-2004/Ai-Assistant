import cv2
import numpy as np
import threading
from deepface import DeepFace
import face_recognition
from mediapipe import solutions
import pyautogui
import speech_recognition as sr
import pyttsx3
from collections import deque
import time

class GestureSystem:
    def __init__(self):
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Slower speaking rate for clarity

        # Face detection variables
        self.detected_faces = []
        self.face_data = {}  # Store face data with timestamps
        self.last_face_check = 0
        self.face_check_interval = 2  # Check for new faces every 2 seconds
        
        # Drawing variables
        self.drawing_mode = False
        self.canvas = None
        
        # Mouse smoothing
        self.pointer_history = deque(maxlen=5)  # Store last 5 positions for smoothing
        self.last_click_time = 0
        self.click_cooldown = 0.5  # Minimum time between clicks (seconds)
        
        # Speech recognition variables
        self.speech_pause_time = 0.5  # Pause between speech recognition attempts
        self.last_speech_time = 0
        
        # Configure PyAutoGUI
        pyautogui.MINIMUM_DURATION = 0  # Remove minimum movement time
        pyautogui.PAUSE = 0  # Remove pause between actions
        
    def smooth_pointer(self, new_pos):
        """Apply smoothing to pointer movement"""
        self.pointer_history.append(new_pos)
        if len(self.pointer_history) < 2:
            return new_pos
        
        # Calculate weighted average of recent positions
        weights = np.linspace(0.5, 1.0, len(self.pointer_history))
        weights = weights / np.sum(weights)
        
        smoothed_x = int(sum(p[0] * w for p, w in zip(self.pointer_history, weights)))
        smoothed_y = int(sum(p[1] * w for p, w in zip(self.pointer_history, weights)))
        
        return (smoothed_x, smoothed_y)
    
    def detect_emotion_gender(self, frame, face_location):
        """Detect emotion and gender for a specific face."""
        try:
            # Crop the face region for analysis
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            
            # Analyze only if face image is valid
            if face_image.size > 0:
                result = DeepFace.analyze(face_image, 
                                        actions=['emotion', 'gender'],
                                        enforce_detection=False)
                # Extract dominant emotion and gender
                dominant_emotion = result[0]['dominant_emotion']
                gender = result[0]['gender']

                # Normalize gender to 'Man' or 'Woman'
                normalized_gender = "Man" if gender == "Male" else "Woman"

                return dominant_emotion, normalized_gender
        except Exception as e:
            print(f"Error in emotion/gender detection: {e}")
        return None, None


    def process_faces(self, frame):
        """Process faces for emotion and gender detection"""
        current_time = time.time()
        
        # Only process faces periodically
        if current_time - self.last_face_check < self.face_check_interval:
            return
            
        self.last_face_check = current_time
        
        # Detect faces
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            is_new_face = True
            
            # Check if face was detected before
            for known_face in self.detected_faces:
                if face_recognition.compare_faces([known_face], face_encoding)[0]:
                    is_new_face = False
                    break
            
            if is_new_face:
                self.detected_faces.append(face_encoding)
                emotion, gender = self.detect_emotion_gender(frame, face_location)
                
                if emotion and gender:
                    message = f"New person detected. Emotion: {emotion}, Gender: {gender}"
                    print(message)
                    threading.Thread(target=self.speak_async, args=(message,)).start()

    def speak_async(self, text):
        """Asynchronous text-to-speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def hand_tracking(self):
        """Improved hand tracking function"""
        mp_hands = solutions.hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1  # Track only one hand for better performance
        )
        
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            
            if self.canvas is None:
                self.canvas = np.zeros_like(frame)

            # Process hands
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = mp_hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0].landmark
                h, w, _ = frame.shape
                
                # Get index finger and thumb positions
                index_tip = (int(landmarks[8].x * w), int(landmarks[8].y * h))
                thumb_tip = (int(landmarks[4].x * w), int(landmarks[4].y * h))
                
                # Apply smoothing to pointer movement
                smoothed_pos = self.smooth_pointer(index_tip)
                
                # Draw pointer
                cv2.circle(frame, smoothed_pos, 10, (0, 255, 0), cv2.FILLED)
                
                # Move mouse pointer
                screen_w, screen_h = pyautogui.size()
                scaled_x = int((smoothed_pos[0] / w) * screen_w)
                scaled_y = int((smoothed_pos[1] / h) * screen_h)
                pyautogui.moveTo(scaled_x, scaled_y, duration=0)
                
                # Handle click gesture
                distance = np.linalg.norm(np.array(index_tip) - np.array(thumb_tip))
                current_time = time.time()
                
                if distance < 20 and current_time - self.last_click_time > self.click_cooldown:
                    pyautogui.click()
                    self.last_click_time = current_time
                
                # Handle drawing
                if self.drawing_mode:
                    cv2.circle(self.canvas, smoothed_pos, 5, (255, 0, 0), cv2.FILLED)
            
            # Process faces
            self.process_faces(frame)
            
            # Combine frame and canvas
            combined_frame = cv2.addWeighted(frame, 0.8, self.canvas, 0.2, 0)
            cv2.imshow('Gesture Recognition', combined_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def speech_recognition(self):
        """Improved speech recognition function"""
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Speech recognition ready...")
            
            while True:
                if time.time() - self.last_speech_time < self.speech_pause_time:
                    continue
                    
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    self.last_speech_time = time.time()
                    
                    print(f"Command recognized: {command}")
                    
                    if "drawing" in command:
                        self.drawing_mode = True
                        threading.Thread(target=self.speak_async, 
                                      args=("Virtual drawing enabled",)).start()
                    elif "stop drawing" in command:
                        self.drawing_mode = False
                        threading.Thread(target=self.speak_async,
                                      args=("Virtual drawing disabled",)).start()
                    elif "clear" in command:
                        self.canvas = np.zeros_like(self.canvas)
                        threading.Thread(target=self.speak_async,
                                      args=("Canvas cleared",)).start()
                
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Speech recognition error: {e}")

    def run(self):
        """Main function to run the system"""
        # Start threads
        threading.Thread(target=self.hand_tracking, daemon=True).start()
        threading.Thread(target=self.speech_recognition, daemon=True).start()
        
        # Keep the program running
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    system = GestureSystem()
    system.run()