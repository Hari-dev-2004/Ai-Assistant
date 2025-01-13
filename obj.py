import cv2
from object_detection import detect_objects

def capture_image():
    # Open the camera
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Could not open webcam.")
        return None

    print("Opening camera... Press 's' to capture.")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to read from camera.")
            break

        # Show the camera feed
        cv2.imshow("Camera", frame)

        # Wait for user input to capture the image
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # 's' to capture
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {image_path}")
            cam.release()
            cv2.destroyAllWindows()
            return image_path
        elif key == ord('q'):  # 'q' to quit
            print("Exiting without capturing.")
            cam.release()
            cv2.destroyAllWindows()
            return None

def query_handler(query):
    if query.lower() == "detect object":
        image_path = capture_image()
        if image_path:
            detected_objects = detect_objects(image_path)
            print(f"Detected objects: {', '.join(detected_objects)}")
        else:
            print("No image captured.")

if __name__ == "__main__":
    while True:
        query = input("Enter a query: ")
        query_handler(query)
