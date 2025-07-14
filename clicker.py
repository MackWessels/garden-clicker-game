import tkinter as tk

root = tk.Tk()
root.title("Garden Clicker Game")

score = 0

def click():
    global score
    score += 1
    score_label.config(text=f"Score: {score}")

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16))
score_label.pack(pady=10)

click_button = tk.Button(root, text="Click Me!", font=("Arial", 14), command=click)
click_button.pack(pady=10)

root.mainloop()
