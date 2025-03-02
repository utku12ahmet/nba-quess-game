import pandas as pd
import os
import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def start_game():
    global random_player, selected_category, selected_tolerance, points
    points = 0
    score_label.config(text=f"Score: {points}")
    selected_category = category_var.get()
    selected_tolerance = int(tolerance_var.get())
    if selected_category not in ['PTS', 'BLK', 'STL', 'AST', 'TRB']:
        messagebox.showerror("Error", "Invalid category selection!")
        return
    next_player()

def next_player():
    global random_player
    random_player = df.sample(n=1).iloc[0]
    player_label.config(text=f"Player: {random_player['Player']}")

def check_guess():
    global points, random_player, high_score
    try:
        guess = float(guess_entry.get())
        avg_value = random_player[selected_category]
        diff = abs(avg_value - guess)
        if diff == 0:
            messagebox.showinfo("Result", "Perfect Guess!")
            points += 2
        elif diff <= selected_tolerance:
            messagebox.showinfo("Result", f"Correct Guess! Actual Value: {avg_value}")
            points += 1
        else:
            if points > high_score:
                high_score = points
                high_score_label.config(text=f"High Score: {high_score}")
            restart = messagebox.askyesno("Game Over", f"Wrong Guess! Actual Value: {avg_value}\nFinal Score: {points}\nDo you want to play again?")
            if restart:
                start_game()
            else:
                root.quit()
            return
        score_label.config(text=f"Score: {points}")
        next_player()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

file_path = "nba_data_processed.csv"
if not os.path.exists(file_path):
    messagebox.showerror("Error", f"{file_path} not found. Please check the file path!")
    exit()

df = pd.read_csv(file_path)
df.dropna(inplace=True)

root = tk.Tk()
root.title("NBA Guessing Game")
root.geometry("500x600")
root.configure(bg="#2C3E50")

points = 0
high_score = 0
random_player = None
selected_category = "PTS"
selected_tolerance = 2

category_var = tk.StringVar(value='PTS')
tolerance_var = tk.StringVar(value='2')

tk.Label(root, text="Select Category:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").pack()
category_menu = tk.OptionMenu(root, category_var, 'PTS', 'BLK', 'STL', 'AST', 'TRB')
category_menu.pack()

tk.Label(root, text="Select Tolerance:", font=("Arial", 14, "bold"), bg="#2C3E50", fg="white").pack()
tolerance_menu = tk.OptionMenu(root, tolerance_var, '0', '1', '2', '3', '4', '5')
tolerance_menu.pack()

start_button = tk.Button(root, text="Start Game", font=("Arial", 14), bg="#27AE60", fg="white", command=start_game)
start_button.pack(pady=10)

player_label = tk.Label(root, text="Player: ", font=("Arial", 16, "bold"), bg="#2C3E50", fg="yellow")
player_label.pack(pady=10)

guess_entry = tk.Entry(root, font=("Arial", 14))
guess_entry.pack(pady=5)

guess_button = tk.Button(root, text="Make a Guess", font=("Arial", 14), bg="#2980B9", fg="white", command=check_guess)
guess_button.pack(pady=10)

score_label = tk.Label(root, text="Score: 0", font=("Arial", 18, "bold"), bg="#2C3E50", fg="red")
score_label.pack(pady=10)

high_score_label = tk.Label(root, text="High Score: 0", font=("Arial", 18, "bold"), bg="#2C3E50", fg="gold")
high_score_label.pack(pady=10)

root.mainloop()
