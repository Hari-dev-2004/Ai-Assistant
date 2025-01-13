import cv2
from ultralytics import YOLO
from deepface import DeepFace
import threading

def detect_emotion_and_gender(frame):
    try:
        # Analyze the frame for emotions and genders
        analyses = DeepFace.analyze(frame, actions=['emotion', 'gender'], enforce_detection=False)

        for analysis in analyses:
            emotion = analysis['dominant_emotion']
            gender = analysis['dominant_gender']
            x, y, w, h = analysis['region']['x'], analysis['region']['y'], analysis['region']['w'], analysis['region']['h']

            # Draw the emotion and gender on the frame
            cv2.putText(frame, f"Emotion: {emotion}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(frame, f"Gender: {gender}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    except Exception as e:
        print(f"Error in emotion and gender detection: {e}")

def live_object_and_emotion_detection():
    # Load the YOLOv8 model
    model = YOLO("yolov8n.pt")  # Replace with your YOLO model file

    # Start video capture
    cap = cv2.VideoCapture(0)  # Default webcam

    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Perform object detection
        results = model.predict(source=frame, conf=0.5, show=False)

        # Annotate frame with object detections
        detected_objects = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                conf = box.conf[0]  # Confidence score
                cls = int(box.cls[0])  # Class index
                label = model.names[cls]  # Class label

                detected_objects.append(label)

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        # Emotion and gender detection
        detect_emotion_and_gender(frame)

        # Display the frame
        cv2.imshow("Live Object and Emotion Detection", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    print("Detection ended.")

# Run the combined detection
live_object_and_emotion_detection()
