import cv2

def main():
    # Adjust the GStreamer pipeline with a lower framerate for testing
    gst_pipeline = (
        "libcamerasrc ! "
        "videoconvert ! "
        "videobalance ! "
        "video/x-raw,format=BGR,width=1280,height=720,framerate=30/1 ! "
        "appsink"
    )

    # Open the camera
    camera = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not camera.isOpened():
        print("Error: Camera could not be opened")
        return

    # Set a larger window size
    cv2.namedWindow('Camera Test', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera Test', 1280, 720)

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            cv2.imshow('Camera Test', frame)

            # Check for 'q' key press to exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except Exception as e:
        print(f"Exception occurred: {e}")

    finally:
        # Release the camera and close all OpenCV windows
        camera.release()
        cv2.destroyAllWindows()
        print("Camera released")

if __name__ == "__main__":
    main()
