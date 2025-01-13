import cv2
import numpy as np
import threading
from queue import Queue
from deepface import DeepFace
import face_recognition
from mediapipe import solutions
import pyautogui
import speech_recognition as sr
import pyttsx3
from collections import deque
import time
from queue import Queue
from datetime import datetime
import os
from hands import HandDetector
from canvas import Canvas

# Optional imports - system will work without these but with reduced functionality
HAVE_DEEPFACE = True
HAVE_FACE_RECOGNITION = True
HAVE_SPEECH = True

try:
    from deepface import DeepFace
except ImportError:
    HAVE_DEEPFACE = False
    print("DeepFace not available - emotion detection disabled")

try:
    import face_recognition
except ImportError:
    HAVE_FACE_RECOGNITION = False
    print("face_recognition not available - face recognition disabled")

try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:
    HAVE_SPEECH = False
    print("Speech packages not available - voice commands disabled")

class AdvancedDetectionSystem:
    def __init__(self):
        # Initialize face processing queue and thread
        self.face_queue = Queue(maxsize=5)
        self.face_thread = threading.Thread(target=self.process_face_queue, daemon=True)
        self.face_thread.start()
    def __init__(self):
        # Initialize basic components
        self.drawing_mode = False
        self.last_click_time = 0
        self.click_cooldown = 0.3
        self.screen_w, self.screen_h = pyautogui.size()
        self.pointer_history = deque(maxlen=3)
        self.background_mode = 'CAM'

        # After initializing screen dimensions
        self.canvas = Canvas(self.screen_w, self.screen_h)
        self.detector = HandDetector(self.background_mode)
        
        # Initialize speech if available
        self.speech_enabled = HAVE_SPEECH
        if self.speech_enabled:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.speech_queue = Queue()
            self.speech_thread = None
        
        # Initialize face detection if available
        self.face_enabled = HAVE_FACE_RECOGNITION and HAVE_DEEPFACE
        if self.face_enabled:
            self.detected_faces = []
            self.face_encodings = []
            self.face_times = {}
            self.face_check_interval = 2
            self.last_face_check = 0
        
        # Initialize YOLO
        self.classes = []
        self.output_layers = []
        self.last_object_detection = 0
        self.object_check_interval = 1
        self.last_detected_objects = set()
        
        # Configure PyAutoGUI
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = True

    def process_faces(self, frame):
        """Queue new faces for processing in a separate thread."""
        if not self.face_enabled:
            return
        
        try:
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for face_encoding, face_location in zip(current_face_encodings, face_locations):
                # Check if the face is already processed
                matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
                if not any(matches):
                    # Add new face to the queue for analysis
                    try:
                        top, right, bottom, left = face_location
                        face_image = frame[top:bottom, left:right]
                        self.face_queue.put((face_encoding, face_image), block=False)
                    except Exception as e:
                        print(f"Error queuing face for analysis: {e}")
        except Exception as e:
            print(f"Face detection error: {e}")
        """Process faces if a new face is detected, analyze emotion and gender once."""
        if not self.face_enabled:
            return
        
        try:
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for face_encoding, face_location in zip(current_face_encodings, face_locations):
                # Check if the face is already processed
                matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
                if not any(matches):
                    try:
                        # Capture and process the new face
                        top, right, bottom, left = face_location
                        face_image = frame[top:bottom, left:right]
                        
                        result = DeepFace.analyze(face_image, actions=['emotion', 'gender'], enforce_detection=False)
                        emotion = result[0]['dominant_emotion']
                        gender = result[0]['gender']
                        
                        # Store the face encoding to avoid reprocessing
                        self.face_encodings.append(face_encoding)
                        self.speak_async(f"New person detected. Appears to be a {gender} showing {emotion} emotion.")
                    except Exception as e:
                        print(f"Face analysis error: {e}")
        except Exception as e:
            print(f"Face detection error: {e}")
        """Process faces if face detection is enabled, ensuring one-time detection per person."""
        if not self.face_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_face_check < self.face_check_interval:
            return
        
        self.last_face_check = current_time
        
        try:
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for face_encoding, face_location in zip(current_face_encodings, face_locations):
                is_known = False
                
                if self.face_encodings:
                    matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
                    if True in matches:
                        face_index = matches.index(True)
                        last_seen = self.face_times.get(face_index, 0)
                        
                        # Skip processing if recently seen
                        if current_time - last_seen > 30:
                            self.speak_async("Welcome back! I recognize you.")
                        
                        self.face_times[face_index] = current_time
                        is_known = True
                
                if not is_known:
                    try:
                        top, right, bottom, left = face_location
                        face_image = frame[top:bottom, left:right]
                        
                        # Process emotion and gender only once
                        result = DeepFace.analyze(face_image, actions=['emotion', 'gender'], enforce_detection=False)
                        emotion = result[0]['dominant_emotion']
                        gender = result[0]['gender']
                        
                        self.face_encodings.append(face_encoding)
                        face_index = len(self.face_encodings) - 1
                        self.face_times[face_index] = current_time
                        
                        self.speak_async(f"New person detected. Appears to be a {gender} showing {emotion} emotion.")
                        
                    except Exception as e:
                        print(f"Face analysis error: {e}")
        except Exception as e:
            print(f"Face detection error: {e}")
        """Process faces if face detection is enabled"""
        if not self.face_enabled:
            return
            
        current_time = time.time()
        if current_time - self.last_face_check < self.face_check_interval:
            return
        
        self.last_face_check = current_time
        
        try:
            face_locations = face_recognition.face_locations(frame)
            current_face_encodings = face_recognition.face_encodings(frame, face_locations)
            
            for face_encoding, face_location in zip(current_face_encodings, face_locations):
                is_known = False
                
                if self.face_encodings:
                    matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
                    if True in matches:
                        face_index = matches.index(True)
                        last_seen = self.face_times.get(face_index, 0)
                        
                        if current_time - last_seen > 30:
                            self.speak_async("Welcome back! I recognize you.")
                        
                        self.face_times[face_index] = current_time
                        is_known = True
                
                if not is_known:
                    try:
                        top, right, bottom, left = face_location
                        face_image = frame[top:bottom, left:right]
                        
                        result = DeepFace.analyze(face_image, 
                                               actions=['emotion', 'gender'],
                                               enforce_detection=False)
                        
                        emotion = result[0]['dominant_emotion']
                        gender = result[0]['gender']
                        
                        self.face_encodings.append(face_encoding)
                        face_index = len(self.face_encodings) - 1
                        self.face_times[face_index] = current_time
                        
                        self.speak_async(f"New person detected. Appears to be a {gender} showing {emotion} emotion")
                        
                    except Exception as e:
                        print(f"Face analysis error: {e}")
                        
        except Exception as e:
            print(f"Face detection error: {e}")

    def smooth_pointer(self, new_pos, frame_dims):
        """Smooth pointer movement using recent history"""
        w, h = frame_dims
        
        # Normalize coordinates to -1 to 1 range
        norm_x = (new_pos[0] / w) * 2 - 1
        norm_y = (new_pos[1] / h) * 2 - 1
        
        # Apply slight amplification and clipping
        norm_x = np.clip(norm_x * 1.2, -1, 1)
        norm_y = np.clip(norm_y * 1.2, -1, 1)
        
        # Convert to screen coordinates
        screen_x = int((norm_x + 1) / 2 * self.screen_w)
        screen_y = int((norm_y + 1) / 2 * self.screen_h)
        
        self.pointer_history.append((screen_x, screen_y))
        
        if len(self.pointer_history) < 2:
            return screen_x, screen_y
            
        # Average recent positions for smoothing
        smoothed_x = int(sum(p[0] for p in self.pointer_history) / len(self.pointer_history))
        smoothed_y = int(sum(p[1] for p in self.pointer_history) / len(self.pointer_history))
        
        return smoothed_x, smoothed_y

    def speak_async(self, text):
        """Queue text for speech if speech is enabled"""
        if self.speech_enabled:
            self.speech_queue.put(text)
        else:
            print(f"Speech (disabled): {text}")

    def speak_worker(self):
        """Speech worker thread"""
        while self.speech_enabled:
            text = self.speech_queue.get()
            if text is None:
                break
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                self.engine.stop()
                time.sleep(0.1)

    def speech_recognition(self):
        """Speech recognition loop"""
        if not self.speech_enabled:
            return

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Speech recognition ready...")

            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Command recognized: {command}")

                    if "drawing" in command:
                        if not self.drawing_mode:
                            self.drawing_mode = True
                            self.canvas = Canvas(self.screen_w, self.screen_h)  # Initialize the canvas
                            self.speak_async("Drawing mode enabled")

                    elif "stop drawing" in command or "disable drawing" in command:
                        if self.drawing_mode:
                            self.drawing_mode = False
                            self.canvas = None  # Clear the canvas properly
                            self.speak_async("Drawing mode disabled")
                            print("Drawing mode disabled.")  # Debug print

                    elif "clear" in command:
                        if self.drawing_mode and self.canvas is not None:
                            self.canvas.clear()  # Add a method to clear canvas if required
                            self.speak_async("Canvas cleared")
                        else:
                            print("Canvas is not available.")  # Debug print

                    elif "quit" in command or "exit" in command:
                        self.speak_async("Shutting down")
                        break

                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Speech recognition error: {e}")
                    continue

    def hand_tracking(self):
        """Main processing loop with hand tracking, drawing, face tracking, and object detection."""
        mp_hands = solutions.hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1
        )

        # Initialize camera
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 60)

        print("Camera initialized. Press 'q' to quit.")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = cv2.flip(frame, 1)

            # Process hand gestures if enabled
            if self.drawing_mode:
                if not self.canvas:
                    # Create canvas lazily
                    self.canvas = Canvas(width=frame.shape[1], height=frame.shape[0])

                # Detect gestures
                request = self.detector.determine_gesture(frame, frame)
                gesture = request.get('gesture')

                if gesture != None:
                    idx_finger = request['idx_fing_tip']  # coordinates of tip of index fing
                    _, c, r = idx_finger

                    data = {'idx_finger': idx_finger}
                    rows, cols, _ = frame.shape

                    # check the radius of concern
                    if (0 < c < cols and 0 < r < rows):
                        if gesture == "DRAW":
                            self.canvas.push_point((r, c))
                        elif gesture == "ERASE":
                            # stop current line
                            self.canvas.end_line()

                            radius = request['idx_mid_radius']

                            _, mid_r, mid_c = request['mid_fing_tip']
                            self.canvas.erase_mode((mid_r, mid_c), int(radius * 0.5))

                            # add features for the drawing phase
                            data['mid_fing_tip'] = request['mid_fing_tip']
                            data['radius'] = radius
                        elif gesture == "HOVER":
                            self.canvas.end_line()
                        elif gesture == "TRANSLATE":
                            self.canvas.end_line()

                            idx_position = (r, c)
                            shift = request['shift']
                            radius = request['idx_pinky_radius']
                            radius = int(radius * .8)

                            self.canvas.translate_mode(idx_position, int(radius * .5), shift)

                            # add features for the drawing phase
                            data['radius'] = radius

                # Update canvas
                frame = self.canvas.draw_dashboard(frame, gesture)  # Draw dashboard
                frame = self.canvas.draw_lines(frame)  # Overlay drawings

            # Process mouse pointer if enabled
            else:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                hand_results = mp_hands.process(rgb_frame)

                if hand_results.multi_hand_landmarks:
                    landmarks = hand_results.multi_hand_landmarks[0].landmark
                    h, w, _ = frame.shape

                    # Get fingertip positions
                    index_tip = (int(landmarks[8].x * w), int(landmarks[8].y * h))
                    thumb_tip = (int(landmarks[4].x * w), int(landmarks[4].y * h))
                    middle_tip = (int(landmarks[12].x * w), int(landmarks[12].y * h))
                    # Move mouse pointer
                    screen_x, screen_y = self.smooth_pointer(index_tip, (w, h))
                    try:
                        pyautogui.moveTo(screen_x, screen_y, duration=0, _pause=False)
                    except:
                        pass

                    # Check for click gesture
                    pinch_distance = np.linalg.norm(np.array(index_tip) - np.array(thumb_tip))
                    index_middle_distance = np.linalg.norm(np.array(index_tip) - np.array(middle_tip))

                    # Gesture: Pinch = Left Click
                    current_time = time.time()
                    if pinch_distance < 20 and current_time - self.last_click_time > self.click_cooldown:
                        pyautogui.click(_pause=False)
                        self.last_click_time = current_time

                    # Gesture: Index + Middle Finger Tap = Right Click
                    if index_middle_distance < 20 and pinch_distance > 40 and current_time - self.last_click_time > self.click_cooldown:
                        pyautogui.rightClick(_pause=False)
                        self.last_click_time = current_time

                    # Gesture: Index + Middle Finger Move = Scroll
                    if index_middle_distance < 50 and pinch_distance > 40:
                        scroll_speed = int((middle_tip[1] - index_tip[1]) * 0.1)  # Adjust sensitivity
                        pyautogui.scroll(scroll_speed)

                    # Draw pointer and update canvas
                    cv2.circle(frame, index_tip, 8, (0, 255, 0), -1)

            # Process face detection if enabled
            if self.face_enabled:
                threading.Thread(target=self.process_faces, args=(frame,), daemon=True).start()

            # Process object detection if enabled

            # Show the updated frame
            cv2.imshow('Advanced Detection System', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        """Main execution"""
        if self.speech_enabled:
            self.speech_thread = threading.Thread(target=self.speak_worker, daemon=True)
            self.speech_thread.start()
            threading.Thread(target=self.speech_recognition, daemon=True).start()
        
        # Start hand tracking in the main thread
        try:
            self.hand_tracking()
        except KeyboardInterrupt:
            pass
        finally:
            if self.speech_enabled:
                self.speech_queue.put(None)  # Signal speech thread to stop
                self.speech_thread.join(timeout=1)
            print("\nShutting down system...")

def main():
    """Main entry point with error handling"""
    try:
        # Check for camera availability
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Unable to access webcam. Please check your camera connection.")
        cap.release()

        print("Initializing Advanced Detection System...")
        print("Available features:")
        print("- Hand tracking and gesture control")
        print("- Virtual drawing")
        print("- Mouse control")
        
        if HAVE_FACE_RECOGNITION and HAVE_DEEPFACE:
            print("- Face recognition and emotion detection")
        if HAVE_SPEECH:
            print("- Voice commands")
            print("  Commands: 'drawing', 'stop drawing', 'clear', 'quit'")

        system = AdvancedDetectionSystem()
        system.run()

    except KeyboardInterrupt:
        print("\nSystem interrupted by user.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your webcam is connected and not in use by another application")
        print("2. Check if all required packages are installed:")
        print("   pip install opencv-python numpy mediapipe pyautogui")
        print("3. For face recognition features:")
        print("   pip install deepface face-recognition")
        print("4. For voice commands:")
        print("   pip install SpeechRecognition pyttsx3")
    finally:
        print("\nSystem shutdown complete.")

if __name__ == "__main__":
    main()