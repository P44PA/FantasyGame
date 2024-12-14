import os
import json
import random
from Character import Character

def load_or_create_character(name):
    filename = f"{name}_save.json"
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        player = Character(data["name"], data["hp"], data["mp"], data["attack"])
        player.inventory = data.get("inventory", [])
        return player
    else:
        hp = random.randint(50, 100)
        mp = random.randint(20, 50)
        attack = random.randint(5, 15)
        return Character(name, hp, mp, attack)