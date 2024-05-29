# pong_cli.py
import click
import time
import requests
import threading

instance1_url = "http://localhost:8000/ping"
instance2_url = "http://localhost:8001/ping"
game_running = False
game_thread = None
pong_time_ms = 1000  # Default delay in milliseconds

def ping_pong(pong_time_ms):
    global game_running
    while game_running:
        try:

            print("Instance1 sent: ping")
            response = requests.post(instance2_url, json={"pong_time_ms": pong_time_ms})
            if response.status_code == 200:
                print("Instance2 received:", response.json()['message'])
            else:
                print("Instance1 ping failed.")


            print("Instance2 sent: ping")
            response = requests.post(instance1_url, json={"pong_time_ms": pong_time_ms})
            if response.status_code == 200:
                print("Instance1 received:", response.json()['message'])
            else:
                print("Instance2 ping failed.")
            
            time.sleep(pong_time_ms / 1000)  # Wait for pong_time_ms milliseconds before sending the next ping
        except Exception as e:
            print(f"Error during ping-pong: {e}")
            break

@click.group()
def cli():
    pass

@click.command()
@click.option('--delay', default=1000, help='Delay between pings in milliseconds.')
def start(delay):
    global game_running, game_thread, pong_time_ms
    if not game_running:
        game_running = True
        pong_time_ms = delay
        game_thread = threading.Thread(target=ping_pong, args=(pong_time_ms,))
        game_thread.start()
        print("Starting the game with delay:", pong_time_ms, "ms")
    else:
        print("The game is already running.")

@click.command()
def stop():
    global game_running, game_thread
    if game_running:
        game_running = False
        game_thread.join()
        print("Stopping the game...")
    else:
        print("The game is not running.")

@click.command()
def pause():
    global game_running
    if game_running:
        game_running = False
        print("Pausing the game...")
    else:
        print("The game is not running.")

@click.command()
@click.option('--delay', default=1000, help='Delay between pings in milliseconds.')
def resume(delay):
    global game_running, game_thread, pong_time_ms
    if not game_running:
        game_running = True
        pong_time_ms = delay
        game_thread = threading.Thread(target=ping_pong, args=(pong_time_ms,))
        game_thread.start()
        print("Resuming the game with delay:", pong_time_ms, "ms")
    else:
        print("The game is already running.")

cli.add_command(start)
cli.add_command(stop)
cli.add_command(pause)
cli.add_command(resume)

if __name__ == "__main__":
    cli()
