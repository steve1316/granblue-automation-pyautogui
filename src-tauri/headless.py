from subprocess import run
from os import listdir
from os.path import isfile, join
import json
from inspect import cleandoc


print(
"""
A simple headless utlity that run the bot and provide simple settting
utilites, Design for Generic V2 mode.
""")

pref = {}
pref_path = "./backend/settings.json"
script_path = "./scripts"
game_mode = [
    "Generic V2",
    "Generic",
    "Quest",
    "Special",
    "Coop",
    "Raid",
    "Rise of the Beasts",
    "Event"
    "Event (Token Drawboxes)"
    "Guild Wars",
    "Dread Barrage",
    "Proving Grounds",
    "Xeno Clash",
    "Arcarum",
    "Arcarum Sandbox",
]

with open(pref_path, "r") as jsonFile:
    pref = json.load(jsonFile)


def write_file():
    """Call me every time you change the pref value"""
    with open(pref_path, "w") as jsonFile:
        json.dump(pref, jsonFile, indent=4)

def print_status():
    print(cleandoc(
        f"""---------------------------------------------------
        l :load a script                     {pref['game']['combatScriptName']}
        m :change game mode                  {pref['game']['farmingMode']}
        i :change repeat time/item to farm   {pref['game']['itemAmount']}
        q :quit current operation

        enter :run the bot
        ---------------------------------------------------
        """))



def load_script():
    scripts = [f for f in listdir(script_path) if isfile(join(script_path, f))]
    print("---------------------------------------------------")
    for i, script in enumerate(scripts):
        print(f"{i} -> {script}")
    print("---------------------------------------------------")
    while True:
        try:
            ins = input("Select a script index: ")
            if ins == 'q': return
            idx = int(ins)
            if idx < 0  or idx > len(scripts)-1 :
                raise ValueError
        except ValueError:
            print("Invalid number: Try again")
        else:
            with open(f"{script_path}/{scripts[idx]}") as script_file:
                pref['game']['combatScript'] = script_file.read().splitlines()
                pref['game']['combatScriptName'] = scripts[idx]
            write_file()
            print(f"script: {scripts[idx]} is succesfully loaded")
            break


def change_mode():
    print("---------------------------------------------------")
    for i, mode in enumerate(game_mode):
        print(f"{i} -> {mode}")
    print("---------------------------------------------------")
    while True:
        try:
            ins = input("Select a game mode: ")
            if ins == 'q': return
            idx = int(ins)
            if idx < 0  or idx > len(game_mode)-1 :
                raise ValueError
        except ValueError:
            print("Invalid number: Try again")
        else:
            pref['game']['farmingMode'] = game_mode[idx]
            write_file()
            print(f"Game Mode succesfullt changed to {game_mode[idx]}")
            break



def change_item_amount():
    print("---------------------------------------------------")
    while True:
        try:
            ins = input("Input the repeat times/ amount of items: ")
            if ins == 'q': return
            amount = int(ins)
            if amount < 1:
                raise ValueError
        except ValueError:
            print("Invalid number: Try again")
        else:
            pref['game']['itemAmount'] = amount
            write_file()
            print(f"Item amount succesfully changed to {amount}")
            break


while True:
    print_status()
    cmd = input("What would you like to do? :")
    if cmd == 'l':
        load_script()
    elif cmd == 'm':
        change_mode()
    elif cmd == 'i':
        change_item_amount()
    elif cmd == '':
        print("Bot starting now, user Ctrl-c to force terminate")
        run(["python", "./backend/main.py"])
    elif cmd == 'q':
        print("Bot quit successfully")
        break
    else:
        print(f"Invalid command: {cmd}\n")