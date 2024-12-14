import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
from SaveGame import *
from UseCharacter import *
from Enemy import *

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Game")
        self.root.geometry("500x400")

        self.background_image = ImageTk.PhotoImage(Image.open("Images/WAR.jpg"))

        self.start_frame = tk.Frame(root)
        self.game_frame = tk.Frame(root)

        self.player = None
        self.enemy_image = None
        self.combat_window = None

        self.log_text = None
        self.create_start_frame()

    def create_start_frame(self):
        canvas = tk.Canvas(self.start_frame, width=600, height=500)
        canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        canvas.pack(fill="both", expand=True)

        tk.Label(self.start_frame, text="Welcome to the Fantasy Game!", font=("Arial", 16), bg="black", fg="white").place(relx=0.5, rely=0.3, anchor="center")
        tk.Label(self.start_frame, text="Enter your character's name:", bg="black", fg="white").place(relx=0.5, rely=0.4, anchor="center")

        self.name_entry = tk.Entry(self.start_frame)
        self.name_entry.place(relx=0.5, rely=0.45, anchor="center")

        tk.Button(self.start_frame, text="Start Game", command=self.start_game).place(relx=0.5, rely=0.55, anchor="center")

        self.start_frame.pack(fill="both", expand=True)

    def create_game_frame(self):
        self.game_frame.pack(fill="both", expand=True)

        tk.Label(self.game_frame, text="Game Status", font=("Arial", 14)).pack()

        self.status_frame = tk.Frame(self.game_frame)
        self.status_frame.pack(pady=10)

        self.status_label = tk.Label(self.status_frame, font=("Arial", 12))
        self.status_label.grid(row=0, column=0, padx=10)

        self.inventory_frame = tk.Frame(self.game_frame)
        self.inventory_frame.pack(pady=10)

        self.inventory_label = tk.Label(self.inventory_frame, font=("Arial", 12))
        self.inventory_label.pack()

        self.log_text = tk.Text(self.game_frame, height=10, state="disabled", wrap="word")
        self.log_text.pack(pady=10, fill="x")

        self.main_menu = tk.Frame(self.game_frame)
        self.main_menu.pack()

        tk.Button(self.main_menu, text="View Status", command=self.view_status).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.main_menu, text="Explore", command=self.explore_world).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.main_menu, text="Inventory", command=self.manage_inventory).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.main_menu, text="Save Game", command=lambda: save_game(self.player)).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.main_menu, text="Exit", command=self.root.quit).grid(row=0, column=4, padx=5, pady=5)

    def start_game(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Invalid Input", "Please enter a character name.")
            return

        self.player = load_or_create_character(name)
        self.start_frame.pack_forget()
        self.create_game_frame()
        self.update_status()

        self.autosave_thread = threading.Thread(target=self.autosave)
        self.autosave_thread.daemon = True  # Set the thread as a daemon thread
        self.autosave_thread.start()


    def autosave(self):
        while True:
            try:
                save_game_auto(self.player)
                time.sleep(1)  # Adjust the interval as needed
            except Exception as e:
                print(f"Error during autosave: {e}")

            # Check if the main window is still open
            if not self.root.winfo_exists():
                break

    def view_status(self):
        messagebox.showinfo("Status", f"Name: {self.player.name}\nHP: {self.player.hp}\nMP: {self.player.mp}\nAttack: {self.player.attack}")

    def update_status(self):
        self.status_label.config(text=f"{self.player.name} - HP: {self.player.hp}, MP: {self.player.mp}, Attack: {self.player.attack}")
        # self.inventory_label.config(text=f"Inventory: {[item['name'] for item in self.player.inventory]}")

    def log_event(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def explore_world(self):
        event = random.choice(["enemy", "treasure", "empty"])
        if event == "enemy":
            enemy = Enemy("Goblin", random.randint(30, 50), random.randint(5, 10))
            self.log_event(f"A wild {enemy.name} appears! HP: {enemy.hp}, Attack: {enemy.attack}")
            self.show_combat_window(enemy)
        elif event == "treasure":
            item = {'name': 'Magic Elixir', 'type': 'healing', 'effect': 30}
            self.player.inventory.append(item)
            self.log_event(f"You found a {item['name']}! It has been added to your inventory.")
            self.update_status()
        else:
            self.log_event("The area is quiet. Nothing happens.")

    def manage_inventory(self):
        if not self.player.inventory:
            messagebox.showinfo("Inventory", "Your inventory is empty.")
            return

        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventory")

        for idx, item in enumerate(self.player.inventory):
            item_label = tk.Label(inventory_window, text=f"{item['name']} ({item['effect']} HP)")
            item_label.grid(row=idx, column=0)

            use_button = tk.Button(inventory_window, text="Use", command=lambda i=item: self.use_item(i, inventory_window))
            use_button.grid(row=idx, column=1)

    def use_item(self, item, window):
        self.player.use_item(item)
        self.log_event(f"Used {item['name']}, recovered {item['effect']} HP!")
        self.update_status()
        window.destroy()

    def combat(self, enemy, action):
        if action == "attack":
            # Perform attack logic
            damage = self.player.attack + random.randint(-2, 2)
            enemy.take_damage(damage)
            self.log_event(f"You dealt {damage} damage to {enemy.name}. Remaining HP: {enemy.hp}")
            self.enemy_stats_label.config(text=f"Name: {enemy.name}\nHP: {enemy.hp}\nAttack: {enemy.attack}")
            self.root.after(100, self.update_status)  # Schedule status update

            if enemy.hp <= 0:
                self.log_event(f"You defeated {enemy.name}!")
                self.combat_window.destroy()
                return

            # Enemy attacks
            player_damage = enemy.attack
            self.player.take_damage(player_damage)
            self.log_event(f"{enemy.name} attacked you for {player_damage} damage. Remaining HP: {self.player.hp}")

            self.root.after(100, self.update_status)  # Schedule status update

            if self.player.hp <= 0:
                self.log_event(f"You were defeated by {enemy.name}!")
                self.combat_window.destroy()
                self.root.quit()

        elif action == "run":
            self.log_event("You fled the battle!")
            self.combat_window.destroy()

    def show_combat_window(self, enemy):
        self.combat_window = tk.Toplevel(self.root)
        self.combat_window.title("Combat")

        # Load JPEG image using PIL (replace with your actual image path)
        goblin_image = Image.open("Images/People.jpg")
        photo = ImageTk.PhotoImage(goblin_image)

        image_label = tk.Label(self.combat_window, image=photo)
        image_label.image = photo  # Keep a reference to prevent garbage collection
        image_label.grid(row=0, column=0, columnspan=2)

        # Create a variable to store the enemy stats label (for easier updating)
        self.enemy_stats_label = tk.Label(self.combat_window,
                                          text=f"Name: {enemy.name}\nHP: {enemy.hp}\nAttack: {enemy.attack}",
                                          font=("Arial", 12))
        self.enemy_stats_label.grid(row=1, column=0, columnspan=2)

        attack_button = tk.Button(self.combat_window, text="Attack", command=lambda: self.combat(enemy, "attack"))
        attack_button.grid(row=2, column=0)

        run_button = tk.Button(self.combat_window, text="Run Away", command=lambda: self.combat(enemy, "run"))
        run_button.grid(row=2, column=1)

        self.combat_window.grab_set()  # Block main window while combat window is open
    def combat_action(self, enemy, action):
        if action == "attack":
            # Perform attack logic
            self.combat(enemy)

            # Close combat window after combat is resolved
            if enemy.hp <= 0 or self.player.hp <= 0:
                self.combat_window.destroy()
                self.combat_window = None

        elif action == "run":
            self.log_event("You fled the battle!")
            self.combat_window.destroy()
            self.combat_window = None

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()