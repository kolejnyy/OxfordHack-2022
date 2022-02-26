from State import State
import random
import sys

file_name = 'datasets/water/water_sets.npy'
if len(sys.argv) > 1:
    file_name = sys.argv[1]

categories = ["ph", "Hardness", "Conductivity", "Potability"]
num_of_data_sets = 2200
game_state = State(file_name, 1000, categories, True)

while True:
    game_state.printState()
    b = random.randint(0, 1)
    b = b == 1
    if b:
        print("Guess higher ", b)
    else:
        print("Guessing lower ", b)
    bet = random.randint(1, 50)
    print("betting ", bet)
    print("guessed?", game_state.checkAnswer(b))
    game_state.updateState(b, bet)
    flag = input()
    if flag == 'exit':
        break