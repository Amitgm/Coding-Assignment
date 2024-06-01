This is a coding Assignment for ping pong game ran on two servers

The below two commands must be ran on the path the two files are downloaded

To run the first server open command terminal and run: uvicorn server:app --port 8001
To run the second server open another command terminal and run: uvicorn server:app --port 8000

To run the game, run the command python ping_pong.py start --delay 1000
