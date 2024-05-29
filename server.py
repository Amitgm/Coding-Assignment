# server.py
# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests

# app = FastAPI()

# # Define the data model for the response
# class PongResponse(BaseModel):
#     message: str

# # The ping endpoint
# @app.post("/ping")
# async def ping():
#     return PongResponse(message="pong")

# # Function to send a ping request to another server
# def send_ping(url: str):
#     try:
#         response = requests.post(url)
#         if response.status_code == 200:
#             print(response.json()['message'])
#         else:
#             print(f"Failed to ping {url}, status code: {response.status_code}")
#     except Exception as e:
#         print(f"Error pinging {url}: {e}")


# /////////////////////////////////////////////////////////////////////////

# server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import time
import threading

app = FastAPI()

class PongResponse(BaseModel):
    message: str

@app.post("/ping")
async def ping(request: Request):
    data = await request.json()
    pong_time_ms = data.get("pong_time_ms", 1000)
    
    # Respond with pong
    response = PongResponse(message="pong")
    
    # Ping back after pong_time_ms milliseconds
    threading.Thread(target=ping_back, args=(pong_time_ms,)).start()
    
    return response

def ping_back(pong_time_ms: int):
    time.sleep(pong_time_ms / 1000)
    url = "http://localhost:8000/ping" if app.root_path.endswith("1") else "http://localhost:8001/ping"
    try:
        requests.post(url, json={"pong_time_ms": pong_time_ms})
    except Exception as e:
        print(f"Error sending ping back: {e}")

