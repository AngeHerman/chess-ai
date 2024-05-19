import tkinter as tk
from tkinter import ttk
from interactions import *

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess AI")
        self.root.geometry("300x200")
        self.acceuil()

    def acceuil(self):
        button_a = tk.Button(self.root, text="Play against ai", command=self.game_against_ai)
        button_a.pack(padx=20, pady=20)

        button_b = tk.Button(self.root, text="Simulate ai against lichess ai", command=self.game_ai_against_lichess_ai)
        button_b.pack(padx=20, pady=20)

    def game_against_ai(self):
        a_window = tk.Toplevel(self.root)
        a_window.title("Settings")
        a_window.geometry("400x300")
        
        label_a = tk.Label(a_window, text="Select the level of the ai:")
        label_a.pack(pady=10)

        spinbox_a = ttk.Spinbox(a_window, from_=0, to=4, width=5)
        spinbox_a.pack(pady=10)
        play_button = tk.Button(a_window, text="Start the ai", command=lambda: self.play_ai_player(spinbox_a.get(), a_window))
        play_button.pack(pady=20)
        message_label = tk.Label(a_window, text="Go challenge \"ange_bot\" on lichess after starting the ai.\n You have 10 sec to challenge the ai after the click", fg="red")
        message_label.pack(pady=10)
        
        

    def game_ai_against_lichess_ai(self):
        b_window = tk.Toplevel(self.root)
        b_window.title("Settings")
        b_window.geometry("400x300")
        
        label_a = tk.Label(b_window, text="Select the level of our ai:")
        label_a.pack(pady=5)
        spinbox_a = ttk.Spinbox(b_window, from_=0, to=4, width=5)
        spinbox_a.pack(pady=5)

        label_b = tk.Label(b_window, text="Select the level of lichess ai:")
        label_b.pack(pady=5)

        spinbox_b = ttk.Spinbox(b_window, from_=1, to=8, width=5)
        spinbox_b.pack(pady=5)

        play_button = tk.Button(b_window, text="Start simulation", command=lambda: self.play_ai_ai(spinbox_a.get(), spinbox_b.get(), b_window))
        play_button.pack(pady=20)
        message_label = tk.Label(b_window, text="Surrender on lichess if you want the game to stop", fg="red")
        message_label.pack(pady=10)

    def play_ai_player(self, value, window):
        if value.isdigit():
            play_against_player_o(value)
            window.destroy()
        

    def play_ai_ai(self, level_ia, level_lichess_ai, window):
        if level_ia.isdigit() and level_lichess_ai.isdigit():
            play_against_ai_o(level_ia,level_lichess_ai)
            window.destroy()
        

    def run(self):
        self.root.mainloop()


