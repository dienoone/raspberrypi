import asyncio
from signalr_connection_client import SignalRClient

async def main():
    hub_url = "https://localhost:5000/detection?type=raspberrypi"
    url = "https://localhost:5000/api/file"

    # Create and start the SignalR client
    client = SignalRClient(hub_url, url)
    client.start()

    # Wait a moment to ensure the connection is fully established
    await asyncio.sleep(2)

    # Keep the connection alive
    while True:
        await asyncio.sleep(3600)  # Sleep in one-hour increments

if __name__ == "__main__":
    asyncio.run(main())
