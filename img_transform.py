import cv2
from deepface import DeepFace

def live_gender_detection():
    cap = cv2.VideoCapture(0)  # Open the webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        try:
            # Analyze the current frame for multiple faces and their genders
            analyses = DeepFace.analyze(frame, actions=['gender'], enforce_detection=False)
            print("Analyses:", analyses)

            # Display the detected gender for each face
            for analysis in analyses:
                gender = analysis['gender']
                (x, y, w, h) = analysis['region']
                cv2.putText(frame, f"Gender: {gender}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        except Exception as e:
            print(f"Error in gender detection: {e}")

        # Display the current frame with gender detection
        cv2.imshow("Live Gender Detection", frame)

        # Break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close OpenCV window

if __name__ == '__main__':
    live_gender_detection()