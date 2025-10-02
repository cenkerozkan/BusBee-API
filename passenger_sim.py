import asyncio
import websockets
import json
import uuid
import time # Added time module

# Configuration
WS_URL = "ws://busops-acb3c422b0e4.herokuapp.com/passenger/ws/fetch_vehicle_location"
API_KEY = "iWeGAgNoxpw04IPX3F2xqzF78e0mqTmpdQIWt7xZ"  # Replace with your actual API key
JOURNAL_UUID = "d04a11cb-2c20-4346-aa02-42934219c31b" # Use a journal_uuid from your driver or a known one
NUM_PASSENGERS = 1500
REQUEST_DELAY_SECONDS = 1 # Delay between requests for each passenger

async def fetch_location_for_passenger(passenger_id):
    """Simulates a single passenger fetching location updates."""
    uri = WS_URL
    payload = {"journal_uuid": JOURNAL_UUID}

    while True:
        try:
            async with websockets.connect(uri, additional_headers={"PASSENGER-API-KEY": API_KEY}) as websocket:
                print(f"Passenger {passenger_id}: Connected.")
                
                start_time = time.monotonic() # Record time before sending
                await websocket.send(json.dumps(payload))
                print(f"Passenger {passenger_id}: Sent request for journal {JOURNAL_UUID}")
                
                response = await websocket.recv()
                end_time = time.monotonic() # Record time after receiving response
                response_time = end_time - start_time
                print(f"Passenger {passenger_id}: Received response in {response_time:.4f} seconds: {response}")
                
                # Keep the connection open and periodically request, or close and reconnect
                # For this stress test, we'll close and reconnect after a delay
                # If the server supports persistent connections for fetching, adjust accordingly.
                # For now, we assume a request-response pattern per connection.

        except websockets.exceptions.ConnectionClosed as e:
            print(f"Passenger {passenger_id}: Connection closed - {e}. Reconnecting in {REQUEST_DELAY_SECONDS}s...")
        except Exception as e:
            print(f"Passenger {passenger_id}: An error occurred: {e}. Retrying in {REQUEST_DELAY_SECONDS}s...")
        
        await asyncio.sleep(REQUEST_DELAY_SECONDS)


async def main():
    """Runs multiple passenger simulations concurrently."""
    if API_KEY == "your-api-key-here":
        print("Please replace 'your-api-key-here' with your actual passenger API key in the script.")
        return

    tasks = []
    for i in range(NUM_PASSENGERS):
        tasks.append(fetch_location_for_passenger(i + 1))
    
    print(f"Starting {NUM_PASSENGERS} passenger simulations...")
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nPassenger simulation script terminated by user.")

if __name__ == "__main__":
    asyncio.run(main())