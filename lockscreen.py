import tkinter as tk
import json
import random
import string

# Config
MAX_ATTEMPTS = 3
LOCKOUT_SECONDS = 15
TIMER_SECONDS = 30

# State
attempts = 0
time_left = TIMER_SECONDS
locked_out = False

# Load riddles
with open("puzzles.json") as f:
    all_puzzles = json.load(f)

puzzle = random.choice(all_puzzles)

# Normalize function (removes punctuation, whitespace, lowercase)
def normalize(text):
    return ''.join(c for c in text.lower() if c not in string.punctuation).strip()

# Setup UI
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')
root.title("🔒 Solve to Unlock")

label = tk.Label(root, text="🧠 Solve this to unlock your screen:", fg='white', bg='black', font=("Courier", 26))
label.pack(pady=40)

question_label = tk.Label(root, text=puzzle["question"], fg='cyan', bg='black', font=("Courier", 20), wraplength=1000)
question_label.pack(pady=20)

entry = tk.Entry(root, font=("Courier", 20), width=40)
entry.pack(pady=20)

status = tk.Label(root, text="", fg='red', bg='black', font=("Courier", 16))
status.pack()

timer_label = tk.Label(root, text="", fg='yellow', bg='black', font=("Courier", 16))
timer_label.pack(pady=10)

# Lockout function
def lockout(reason):
    global locked_out
    locked_out = True
    status.config(text=f"{reason} 🔒 Locked for {LOCKOUT_SECONDS} sec")
    entry.config(state='disabled')
    root.after(LOCKOUT_SECONDS * 1000, reset_lock)

# Timer countdown
def update_timer():
    global time_left
    if locked_out:
        return
    if time_left > 0:
        timer_label.config(text=f"⏱ Time left: {time_left} seconds")
        time_left -= 1
        root.after(1000, update_timer)
    else:
        lockout("⏰ Time's up!")

# Reset state after lockout
def reset_lock():
    global attempts, time_left, locked_out, puzzle
    attempts = 0
    time_left = TIMER_SECONDS
    locked_out = False
    puzzle = random.choice(all_puzzles)
    question_label.config(text=puzzle["question"])
    status.config(text="")
    entry.config(state='normal')
    entry.delete(0, tk.END)
    update_timer()

# Answer checker
def check_answer(event=None):
    global attempts
    if locked_out:
        return
    user_input = normalize(entry.get())
    correct_answer = normalize(puzzle["answer"])
    if user_input == correct_answer:
        root.destroy()
    else:
        attempts += 1
        if attempts >= MAX_ATTEMPTS:
            lockout("❌ 3 wrong attempts!")
        else:
            status.config(text=f"❌ Incorrect! Attempts left: {MAX_ATTEMPTS - attempts}")
            entry.delete(0, tk.END)

# Bindings & config
entry.bind('<Return>', check_answer)
root.protocol("WM_DELETE_WINDOW", lambda: None)
root.lift()
root.attributes("-topmost", True)

# Start timer
update_timer()
root.mainloop()
