# main.py
import asyncio
from game import Game

if __name__ == "__main__":
    flappINO_app = Game()
    # <-- NEW: Runs the async loop
    asyncio.run(flappINO_app.run())