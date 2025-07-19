import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import threading
import time
import random

root = tk.Tk()
root.title("Garden Clicker Game")
root.geometry("800x600")

score = 0
has_mower = False
has_flower_upgrade = False
flowers = []

# Load images
background_img = Image.open("pictures/garden.jpg").resize((800, 600))
background_photo = ImageTk.PhotoImage(background_img)

mower_img_original = Image.open("pictures/mower.png").resize((100, 100))
mower_photo = ImageTk.PhotoImage(mower_img_original)

flower_img_original = Image.open("pictures/flower.png")

# Set up canvas and elements
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

canvas_bg = canvas.create_image(0, 0, image=background_photo, anchor="nw")
mower = canvas.create_image(-200, 450, image=mower_photo, anchor="nw")

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), bg="lightgreen")
score_label.place(x=10, y=10)

# Normal click
def click():
    global score
    score += 1
    score_label.config(text=f"Score: {score}")

click_button = tk.Button(root, text="Click Me!", font=("Arial", 14), command=click)
click_button.place(x=10, y=50)

# Mower logic
def start_mower():
    global has_mower
    def mower_loop():
        global score, mower_photo
        while has_mower:
            from_left = random.choice([True, False])
            y_pos = random.randint(400, 480)
            if from_left:
                current_img = mower_img_original
                start_x = -200
                end_x = 800
                step = 10
            else:
                flipped_img = ImageOps.mirror(mower_img_original)
                current_img = flipped_img
                start_x = 800
                end_x = -200
                step = -10
            mower_photo = ImageTk.PhotoImage(current_img)
            canvas.itemconfig(mower, image=mower_photo)
            for x in range(start_x, end_x, step):
                canvas.coords(mower, x, y_pos)
                time.sleep(0.02)
            score += 10
            score_label.config(text=f"Score: {score}")
            canvas.coords(mower, -200, 450)
            time.sleep(10)
    t = threading.Thread(target=mower_loop, daemon=True)
    t.start()

def buy_mower():
    global has_mower, score
    if not has_mower and score >= 50:
        has_mower = True
        start_mower()
        buy_button.config(state="disabled")

buy_button = tk.Button(root, text="Buy Mower (50)", font=("Arial", 14), command=buy_mower)
buy_button.place(x=10, y=100)

# Flower logic
def collect_flower(flower_id, image_ref):
    global score
    score += 3
    score_label.config(text=f"Score: {score}")
    canvas.delete(flower_id)
    flowers[:] = [f for f in flowers if f[0] != flower_id]

def spawn_flower():
    def grow_flower(x, y):
        size = 10
        max_size = 80
        flower = None

        def grow():
            nonlocal size, flower
            if flower:
                canvas.delete(flower)
            if size >= max_size:
                img = flower_img_original.resize((max_size, max_size))
                photo = ImageTk.PhotoImage(img)
                flower = canvas.create_image(x, y, image=photo, anchor="center")
                canvas.tag_bind(flower, "<Button-1>", lambda e: collect_flower(flower, photo))
                flowers.append((flower, photo))
            else:
                img = flower_img_original.resize((size, size))
                photo = ImageTk.PhotoImage(img)
                flower = canvas.create_image(x, y, image=photo, anchor="center")
                flowers.append((flower, photo))
                canvas.after(50, grow)
                size += 5

        grow()

    x = random.randint(100, 700)
    y = random.randint(300, 550)
    grow_flower(x, y)

def flower_spawner_loop():
    if has_flower_upgrade:
        spawn_flower()
    root.after(4000, flower_spawner_loop)

def buy_flower_upgrade():
    global has_flower_upgrade, score
    if not has_flower_upgrade and score >= 30:
        score -= 30
        score_label.config(text=f"Score: {score}")
        has_flower_upgrade = True
        flower_button.config(state="disabled")
        flower_spawner_loop()

flower_button = tk.Button(root, text="Buy Flower Seeds (30)", font=("Arial", 14), command=buy_flower_upgrade)
flower_button.place(x=10, y=150)

root.mainloop()
