import cv2
import http.client
import requests
import json
import base64

# Function to capture a frame from the webcam and send it to the API
def detect_emotion(frame):
    # Convert the frame to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Set up the headers and payload for the API
    url = "https://faceanalyzer-ai.p.rapidapi.com/search-face-in-repository"
    headers = {
        'x-rapidapi-key': "6fbffe8419msh0fce495ef13c2f7p19bb87jsn909207c34db3",
        'x-rapidapi-host': "faceanalyzer-ai.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    payload = {
        "image": img_base64  # Send the base64 encoded image
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Assuming the response contains an 'emotion' key with the detected emotion
        emotion = data.get("emotion", "Unknown")
        return emotion
    else:
        print("Error detecting emotion")
        return "Error"

# Start the webcam and continuously capture frames
cap = cv2.VideoCapture(0)  # 0 for the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect emotion
    emotion = detect_emotion(frame)

    # Display the emotion on the frame
    cv2.putText(frame, f"Emotion: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the webcam feed with the emotion label
    cv2.imshow("Emotion Detection", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
