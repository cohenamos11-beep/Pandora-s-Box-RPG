import numpy as np
import time
import keyboard
import os
import json
import folium
from rooms import World_Rooms, get_master_map, get_house_interior

#Check if Save Exists Before Starting Game

def load_game():
    if not os.path.exists("savegame.json"):
        return None

    with open("savegame.json", "r") as file:
        return json.load(file)

def save_game(player_x, player_y, player_name, weapon, Difficulty):
    game_data = {
        "x": player_x,
        "y": player_y,
        "player_name": player_name,
        "weapon": weapon,
        "difficulty": Difficulty
    }

    with open("savegame.json", "w") as file:
        json.dump(game_data, file, indent=4)

    print("\nGame saved successfully! Press ESC to exit game.")

#Basic Game Mechanic Variables

player_health = 100        


#Starting Screen and Difficulty Selection

print("------------Pandora's Box RPG------------")

saved_game = load_game()
resume_game = (
    saved_game is not None
    and input("A save was found. Resume it? (yes/no):").strip().lower() == "yes"
)

if resume_game:
    player_x = saved_game["x"]
    player_y = saved_game["y"]
    weapon = saved_game["weapon"]
    difficulty = saved_game["difficulty"]
    player_name = saved_game["player_name"]
else:
    player_x = 4
    player_y = 4

if not resume_game:

    while True:
        difficulty = input("Choose your difficulty (Easy, Normal, Hard): ")
        if difficulty.lower() == "hard":
            confirm = input("Are you sure you would like to play on hard mode?: ")
            if confirm.lower() == "yes":
                print("Good luck! You will need it.")

            else:
                print("Returning to difficulty selection...")
                time.sleep(0.25)
                print(".")
                time.sleep(0.25)
                print(".")
                time.sleep(0.25)
                print(".")
                time.sleep(0.25)
                continue

        break

#Starting of the Adventure

    print("Welcome to Pandora's Box RPG! You will be facing many challenges and enemies on your journey.")
    time.sleep(2)
    player_name = input("What is your name, adventurer?: ")
    print(f"Welcome, {player_name}! Your journey begins now.")
    time.sleep(2)
    print("Welcome to the world of Farizon. This once peaceful land has been corrupted by the evil forces of the underworld. You must embark on a journey through Farizon, to the Underworld Gates to defeat the dark forces.")
    time.sleep(8)
    print("On this journey you will face many enemies. It would be best if you chose a weapon to aid you in battle.")
    time.sleep(3)

#Weapon Selection

    print("What weapon would you like to start with?")
    time.sleep(1)

    while True:

        print("Sword - A perfectly balenced choice.", "\033[3mIt's broad and short just like me!\033[0m")
        time.sleep(1)

        print("Battle Axe - This powerful weapon is great for battle, but it feels heavy in your hands.", "\033[3mToo bad I skipped arm day.\033[0m")
        time.sleep(1)

        print("Bow - A ranged weapon that allows you to attack from a distance.", "\033[3mDon't forget your arrows!\033[0m")
        weapon = input("")

        if weapon.lower() == "sword":
            print("\n-----Stats-----")
            print("Power: 60\nSpeed: 60\nRange: 30\n")
            confirm = input("Are you sure you want this weapon?: ")
    
            if confirm.lower() == "yes":
                break

            else:
                print("Please select a different weapon.")
                continue

        if weapon.lower() == "battle axe":
            print("\n-----Stats-----")
            print("Power: 80\nSpeed: 40\nRange: 30\n")
            confirm = input("Are you sure you want this weapon?: ")
    
            if confirm.lower() == "yes":
                break

            else:
                print("Please select a different weapon.")
                continue

        if weapon.lower() == "bow":
            print("\n-----Stats-----")
            print("Power: 50\nSpeed: 70\nRange: 80\n")
            confirm = input("Are you sure you want this weapon?: ")
    
            if confirm.lower() == "yes":
                break

            else:
                print("Please select a different weapon.")
                continue

    print(f"You have chosen the {weapon}. Good luck on your journey, {player_name}!")

#Beginning of the Story

    #Map Builder

my_world = get_master_map()

print("\033[2j", end="")
def draw_map(my_world, player_x, player_y, is_talking=False):
    print("\033[H", end="")

    in_range = abs(player_x - villager_x[0]) <= 1 and abs(player_y - villager_y[0]) <= 1

    for y, row in enumerate(my_world):
        row_string = ""
        for x, tile in enumerate(row):
            if x == player_x and y == player_y:
                row_string += "P "
            elif x == villager_x[0] and y == villager_y[0]:
                if in_range:
                    row_string += "! "
                else:
                    row_string += "V "
            else:
                row_string += tile + " "
        print(row_string)

print("\033[3mUse W, A, S, D to move. Press ESC to quit. Press T to enter game. Press Q to save the game.\033[0m")

outdoor_world = get_master_map()
indoor_world = get_house_interior()

current_map = outdoor_world
is_indoors = False

print("\033[2j", end="")

#Movement Loop

while True:
    #Temporarily store where player wants to go
    moved = False
    new_x = player_x
    new_y = player_y

    #Stores Villager Data

    villager_x = [31]
    villager_y = [3]

    #Tracks if Player is Currently Talking

    is_talking = False

    #Check which key is being pressed
    if keyboard.is_pressed('w'):
        new_y -= 1
        moved = True
    elif keyboard.is_pressed('s'):
        new_y += 1
        moved = True
    elif keyboard.is_pressed('a'):
        new_x -= 1
        moved = True
    elif keyboard.is_pressed('d'):
        new_x += 1
        moved = True
    elif keyboard.is_pressed('esc'):
        print("Exiting game...")
        time.sleep(1)
        break
    elif keyboard.is_pressed('t'):
        moved = True
    elif keyboard.is_pressed('q'):
        save_game(player_x, player_y, weapon, difficulty, player_name)
        time.sleep(0.2)
    elif keyboard.is_pressed('f'):
        if abs(player_x - villager_x[0]) <= 1 and abs(player_y - villager_y[0]) <= 1:
            is_talking = not is_talking
            draw_map(my_world, player_x, player_y, is_talking)
            if is_talking:
                print("\n\033[33mVillager: 'Hello! Welcome to our village! You are welcome to look around and stay awhile!'\033[0m")
            else:
                print("\n" + " " * 50)
        time.sleep(0.2)
        continue

    #Collision Detection
    if moved:
        target_tile = current_map[new_y][new_x]

        if target_tile != "#":

            if not is_indoors and target_tile == "]":
                current_map = indoor_world
                is_indoors = True
                player_x, player_y = 5, 2
                print("\033[2J", end="")

            elif is_indoors and target_tile == "[":
                current_map = outdoor_world
                is_indoors = False
                player_x, player_y = 40, 11
                print("\033[2J", end="")

            else:
                current_map = outdoor_world
                player_x = new_x
                player_y = new_y

            if is_indoors:
                draw_map(current_map, player_x, player_y)
            else:
                draw_map(outdoor_world, player_x, player_y)

        time.sleep(0.08) # Add a small delay to prevent too fast movement
    time.sleep(0.12)



