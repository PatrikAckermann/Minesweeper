from start import start
from game import game

# Beginner: 81 tiles(9x9), 10 mines
# Intermediate: 256 tiles(16x16), 40 mines
# Expert: 480 Tiles(22x22), 99 Mines

# start class: Contains a function to open a window which requests information for the game. For example how many rows and columns you want.
# run class: Starts the game class with variables from the start class.
# game class: Contains everything to run the game like the window and all the logic functions.
# field class: Contains all the important variables of a field.

# Currently limited to 35 rows and 70 columns. That means it has a maximum of 2450 fields because more causes huge performance problems and doesnt fit on a 1080p screen. This amount already runs bad

class run:
    def run(game):
        settings = start.showWindow()
        gameInstance = game(settings[0], settings[1], settings[2], settings[3])
        gameInstance.startGame()

if __name__ == "__main__":
    while True:
        run.run(game)