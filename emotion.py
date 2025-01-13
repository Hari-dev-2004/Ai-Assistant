import cv2
import time
from deepface import DeepFace
import threading

# Keep track of detected users
detected_users = set()

def capture_image():
    """Capture a single frame from the webcam."""
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    
    ret, frame = cap.read()
    cap.release()  # Release the webcam immediately after capturing a frame

    if not ret:
        print("Failed to capture image")
        return None

    return frame

def detect_emotion_and_gender(frame):
    """Analyze the captured image for emotion and gender."""
    try:
        # Analyze the current frame for emotions and genders
        analyses = DeepFace.analyze(frame, actions=['emotion', 'gender'], enforce_detection=False)

        # Iterate over detected faces
        for analysis in analyses:
            emotion = analysis['dominant_emotion']
            gender = analysis['dominant_gender']
            x, y, w, h = analysis['region']['x'], analysis['region']['y'], analysis['region']['w'], analysis['region']['h']

            # Generate a unique user ID based on face features (bounding box)
            user_id = hash(str(x) + str(y) + str(w) + str(h))

            # Print for debugging
            print(f"Emotion: {emotion}, Gender: {gender}, User ID: {user_id}")

            # Draw the emotion and gender on the frame
            cv2.putText(frame, f"Emotion: {emotion}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Gender: {gender}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Keep track of detected users (if new user)
            if user_id not in detected_users:
                detected_users.add(user_id)
                print(f"New user detected: {user_id}")
            else:
                print(f"User {user_id} already detected.")

        # Show the frame with emotion and gender detected
        cv2.imshow("Emotion and Gender Detection", frame)

        # Wait for a key press and close the window
        cv2.waitKey(0)  # Wait indefinitely until a key is pressed
        cv2.destroyAllWindows()  # Close the window after key press

    except Exception as e:
        print(f"Error in emotion and gender detection: {e}")

def start_periodic_detection():
    """Periodically capture images and detect emotions and genders every 40 seconds."""
    while True:
        print("Capturing image and detecting emotion and gender...")
        frame = capture_image()  # Capture an image from the webcam

        if frame is not None:
            detect_emotion_and_gender(frame)  # Perform the detection

        time.sleep(40)  # Wait for 40 seconds before capturing the next image

# Start the periodic detection in a separate thread
detection_thread = threading.Thread(target=start_periodic_detection)
detection_thread.daemon = True  # This ensures the thread exits when the program exits
detection_thread.start()

# Main program loop (can be expanded for other functionality)
while True:
    # Your main program loop for other tasks, such as listening for queries, etc.
    time.sleep(1)  # Add a sleep to prevent 100% CPU usage, or other tasks can go here.
