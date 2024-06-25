import uuid
import cv2
import asyncio
from signalrcore.hub_connection_builder import HubConnectionBuilder
import logging
import base64

hub_url = "https://localhost:5000/camera?type=raspberrypi"
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

def chunk_data(data, chunk_size):
    """Split data into chunks of specified size."""
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


async def stream_video():
    hub_connection = HubConnectionBuilder() \
        .with_url(hub_url=hub_url, options={"verify_ssl": False}) \
        .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

    hub_connection.start()

    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()

            # Base64 encode the image bytes
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')

            # Chunk the data
            chunk_size = 1024  # Adjust chunk size as necessary
            chunks = chunk_data(image_base64, chunk_size)
            message_id = str(uuid.uuid4())  # Unique ID for each message 

            for chunk_index, chunk in enumerate(chunks):
                # Create a dictionary object with chunk data
                image_obj = {
                    "data": chunk,
                    "messageId": message_id,
                    "chunkIndex": chunk_index,
                    "totalChunks": len(chunks)
                }

                # Send chunk to SignalR hub
                try:
                    hub_connection.send("SendFrame", [image_obj])
                except Exception as e:
                    print(f"Error sending chunk: {e}")
                    break

            # Display the resulting frame (for local testing)
            cv2.imshow('Video', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the webcam and close any open windows
        cap.release()
        cv2.destroyAllWindows()
        hub_connection.stop()

if __name__ == "__main__":
    asyncio.run(stream_video())