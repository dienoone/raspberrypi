import cv2
import requests
import time
import threading

class RaspberryPiInterface:
    camera = None
    capturing = False

    @staticmethod
    def start_capture(interval):
        # Start capturing images
        RaspberryPiInterface.capturing = True
        RaspberryPiInterface.capture_thread = threading.Thread(target=RaspberryPiInterface.capture_images, args=(interval,))
        RaspberryPiInterface.capture_thread.start()

    @staticmethod
    def capture_images(interval):
        while RaspberryPiInterface.capturing:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                print("Error: Camera could not be opened")
                camera.release()
                return

            # Allow the camera to warm up
            time.sleep(2)

            ret, frame = camera.read()
            if not ret:
                print("Error: Failed to capture image")
                camera.release()
                break

            # Encode the image as JPEG directly in memory
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode image")
                camera.release()
                continue

            # Convert to bytes and send
            RaspberryPiInterface.send_file_request(jpeg.tobytes(), "https://localhost:5000/api/file/SendImage?methodName=capture")

            # Release the camera
            camera.release()

            # Wait for the specified interval
            time.sleep(interval)
 

    @staticmethod
    def stop_capture():
        print("Stopping capture")
        RaspberryPiInterface.capturing = False
        if RaspberryPiInterface.capture_thread is not None:
            RaspberryPiInterface.capture_thread.join() 

    @staticmethod
    def stop_camera():
        if RaspberryPiInterface.camera is not None:
            RaspberryPiInterface.camera.release()
            RaspberryPiInterface.camera = None
            cv2.destroyAllWindows()
            print("Camera stopped")

    @staticmethod
    def send_file_request(file_bytes, url):
        files = {'file': ('image.jpg', file_bytes, 'image/jpeg')}
        response = requests.post(url, files=files, verify=False)
        if response.status_code == 200:
            print('File uploaded successfully')
            print('Server response:', response.text)
        else:
            print(f"File upload failed with status code {response.status_code}")
            print('Server response:', response.text) 
    
    @staticmethod
    def start_live_stream():
        # Logic to start live stream
        print("Starting live stream")
        # Example: send a request to the Pi to start live stream

    @staticmethod
    def stop_live_stream():
        # Logic to stop live stream
        print("Stopping live stream")
        # Example: send a request to the Pi to stop live stream

    @staticmethod
    def capture_image():
        # Logic to capture an image
        print("Capturing image")
        # Example: send a request to the Pi to capture an image
