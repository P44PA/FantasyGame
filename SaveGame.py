
import json
from tkinter import messagebox, simpledialog

def save_game(player):
    filename = f"{player.name}_save.json"
    data = {
        "name": player.name,
        "hp": player.hp,
        "mp": player.mp,
        "attack": player.attack,
        "inventory": player.inventory
    }
    with open(filename, 'w') as file:
        json.dump(data, file)
    messagebox.showinfo("Save Game", f"Game progress saved for {player.name}!")

def save_game_auto(player):
    filename = f"{player.name}_save.json"
    data = {
        "name": player.name,
        "hp": player.hp,
        "mp": player.mp,
        "attack": player.attack,
        "inventory": player.inventory
    }
    with open(filename, 'w') as file:
        json.dump(data, file)