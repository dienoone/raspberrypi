import base64
import cv2
import time
import threading
import requests

class RaspberryPiInterface:
    camera_lock = threading.Lock()
    capturing = False
    live_streaming = False
    hub_connection = None
    url = None
    camera = None

    @staticmethod
    def initialize_camera():
        gst_pipeline = (
            "libcamerasrc ! "
            "videoconvert ! "
            "appsink"
        )
        RaspberryPiInterface.camera = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
        if not RaspberryPiInterface.camera.isOpened():
            print("Error: Camera could not be opened")
            RaspberryPiInterface.camera = None
        else:
            print("Camera initialized")

    @staticmethod
    def release_camera():
        if RaspberryPiInterface.camera:
            RaspberryPiInterface.camera.release()
            RaspberryPiInterface.camera = None
            cv2.destroyAllWindows()
            print("Camera released")

    @staticmethod
    def start_capture(interval):
        RaspberryPiInterface.capturing = True
        RaspberryPiInterface.capture_thread = threading.Thread(target=RaspberryPiInterface.capture_images, args=(interval,))
        RaspberryPiInterface.capture_thread.start()

    @staticmethod
    def capture_images(interval):
        while RaspberryPiInterface.capturing:
            RaspberryPiInterface.cap_image("capture")
            time.sleep(interval)

    @staticmethod
    def stop_capture():
        print("Stopping capture")
        RaspberryPiInterface.capturing = False
        if RaspberryPiInterface.capture_thread is not None:
            RaspberryPiInterface.capture_thread.join()

    @staticmethod
    def start_live_stream():
        if RaspberryPiInterface.live_streaming:
            print("Live stream already in progress")
            return
        print("Starting live stream")
        RaspberryPiInterface.live_streaming = True
        RaspberryPiInterface.live_stream_thread = threading.Thread(target=RaspberryPiInterface.stream_video)
        RaspberryPiInterface.live_stream_thread.start()

    @staticmethod
    def stream_video():
        while RaspberryPiInterface.live_streaming:
            with RaspberryPiInterface.camera_lock:
                if RaspberryPiInterface.camera is None:
                    RaspberryPiInterface.initialize_camera()
                ret, frame = RaspberryPiInterface.camera.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break

            frame_base64 = RaspberryPiInterface.frame_to_base64(frame)
            chunk_size = 8192
            total_chunks = len(frame_base64) // chunk_size + 1
            for i in range(0, len(frame_base64), chunk_size):
                chunk = frame_base64[i:i + chunk_size]
                RaspberryPiInterface.send_video_chunk(chunk, i, chunk_size, total_chunks)

            time.sleep(0.0033)

        print("Live stream ended")

    @staticmethod
    def stop_live_stream():
        print("Stopping live stream")
        RaspberryPiInterface.live_streaming = False
        if RaspberryPiInterface.live_stream_thread is not None:
            RaspberryPiInterface.live_stream_thread.join()

    @staticmethod
    def capture_image():
        if RaspberryPiInterface.live_streaming:
            RaspberryPiInterface.stop_live_stream()
            RaspberryPiInterface.cap_image("take")
            RaspberryPiInterface.start_live_stream()
        else:
            RaspberryPiInterface.cap_image("take")

    @staticmethod
    def send_file_request(file_bytes, url):
        files = {'file': ('image.jpg', file_bytes, 'image/jpeg')}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print('File uploaded successfully')
            print('Server response:', response.text)
        else:
            print(f"File upload failed with status code {response.status_code}")
            print('Server response:', response.text)

    @staticmethod
    def send_video_chunk(chunk, i, chunk_size, total_chunks):
        if RaspberryPiInterface.hub_connection:
            RaspberryPiInterface.hub_connection.send("UploadLiveStream", [chunk, i // chunk_size, total_chunks])
        else:
            print("Error: Hub connection is not established")

    @staticmethod
    def frame_to_base64(frame):
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        return frame_base64

    @staticmethod
    def cap_image(methodName):
        with RaspberryPiInterface.camera_lock:
            if RaspberryPiInterface.camera is None:
                RaspberryPiInterface.initialize_camera()
            ret, frame = RaspberryPiInterface.camera.read()
            if not ret:
                print("Error: Failed to capture image")
                return

            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode image")
                return

            RaspberryPiInterface.send_file_request(jpeg.tobytes(), f"{RaspberryPiInterface.url}?methodName={methodName}")
        print("Image captured")