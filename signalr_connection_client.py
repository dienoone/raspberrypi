from signalrcore.hub_connection_builder import HubConnectionBuilder
from raspberry_pi_interface import RaspberryPiInterface

class SignalRClient:
    def __init__(self, hub_url, url):
        self.hub_url = hub_url
        self.url = url
        self.connected = False
        self.hub_connection = HubConnectionBuilder() \
            .with_url(self.hub_url) \
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 5
            }).build()

        self.hub_connection.on_open(self.on_open)
        self.hub_connection.on_close(self.on_close)
        self.hub_connection.on_error(self.on_error)
        self.hub_connection.on("StartCapture", self.init_capture)
        self.hub_connection.on("StopCapture", self.end_capture)
        self.hub_connection.on("StartLiveStream", self.get_live_stream)
        self.hub_connection.on("EndLiveStream", self.stop_live_stream)
        self.hub_connection.on("TakeImage", self.capture_image)

        RaspberryPiInterface.hub_connection = self.hub_connection
        RaspberryPiInterface.url = self.url

    def on_open(self):
        print("Connection opened")
        self.connected = True

    def on_close(self):
        print("Connection closed")
        self.connected = False

    def on_error(self, error):
        print(f"Error: {error}")
        self.connected = False

    def start(self):
        self.hub_connection.start()
        print("Connection started")

    def stop(self):
        self.hub_connection.stop()
        self.connected = False
        print("Connection stopped")

    def init_capture(self, data):
        interval = data[0] if data else 15  # Default to 15 seconds if no interval is provided
        print(f"Initializing capture with interval of {interval} seconds")
        RaspberryPiInterface.start_capture(interval)

    def end_capture(self, data):
        print("Ending capture")
        RaspberryPiInterface.stop_capture()

    def get_live_stream(self, data):
        print("Starting live stream")
        RaspberryPiInterface.start_live_stream()

    def stop_live_stream(self, data):
        print("Stopping live stream")
        RaspberryPiInterface.stop_live_stream()

    def capture_image(self, data):
        print("Capturing image")
        RaspberryPiInterface.capture_image()
