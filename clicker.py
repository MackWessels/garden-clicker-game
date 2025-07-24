import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import time
import random
import math

root = tk.Tk()
root.title("Garden Clicker Game")
root.geometry("800x600")

score = 0
has_mower = False
has_flower_upgrade = False
has_bee_upgrade = False
flowers = []

# Load images
background_img = Image.open("pictures/garden.jpg").resize((800, 600))
background_photo = ImageTk.PhotoImage(background_img)

mower_img_original = Image.open("pictures/mower.png").resize((100, 100))
mower_photo = ImageTk.PhotoImage(mower_img_original)

flower_img_original = Image.open("pictures/flower.png")
bee_img_base = Image.open("pictures/bee.png").resize((60, 60))
bee_img_right = bee_img_base.rotate(-90, expand=True)
bee_img_left = bee_img_base.rotate(90, expand=True)
bee_photo = ImageTk.PhotoImage(bee_img_right)

# Preload flower sizes to prevent lag
flower_images = {}
for size in range(10, 85, 5):
    img = flower_img_original.resize((size, size))
    flower_images[size] = ImageTk.PhotoImage(img)

# Set up canvas
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)

canvas_bg = canvas.create_image(0, 0, image=background_photo, anchor="nw")
mower = canvas.create_image(-200, 450, image=mower_photo, anchor="nw")
bee = canvas.create_image(-100, 100, image=bee_photo, anchor="nw")

score_label = tk.Label(root, text="Score: 0", font=("Arial", 16), bg="lightgreen")
score_label.place(x=10, y=10)

# Clicking logic
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
        from_left = random.choice([True, False])
        y_pos = random.randint(400, 480)
        if from_left:
            current_img = mower_img_original
            start_x = -200
            end_x = 800
            step = 10
        else:
            current_img = ImageOps.mirror(mower_img_original)
            start_x = 800
            end_x = -200
            step = -10
        mower_photo = ImageTk.PhotoImage(current_img)
        canvas.itemconfig(mower, image=mower_photo)

        def move(x=start_x):
            global score
            if (from_left and x > end_x) or (not from_left and x < end_x):
                canvas.coords(mower, -200, 450)
                score += 10
                score_label.config(text=f"Score: {score}")
                root.after(10000, mower_loop)
                return
            canvas.coords(mower, x, y_pos)
            root.after(20, lambda: move(x + step))

        move()

    mower_loop()

def buy_mower():
    global has_mower, score
    if not has_mower and score >= 50:
        has_mower = True
        score -= 50
        score_label.config(text=f"Score: {score}")
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

def grow_flower(x, y):
    size = 10
    max_size = 80
    flower = canvas.create_image(x, y, image=flower_images[size], anchor="center")

    def grow():
        nonlocal size
        if size >= max_size:
            canvas.tag_bind(flower, "<Button-1>", lambda e: collect_flower(flower, flower_images[max_size]))
            flowers.append((flower, flower_images[max_size]))
            return
        size += 5
        canvas.itemconfig(flower, image=flower_images[size])
        root.after(50, grow)

    grow()

def spawn_flower():
    x = random.randint(100, 700)
    y = random.randint(300, 550)
    grow_flower(x, y)

def flower_spawner_loop():
    if has_flower_upgrade and len(flowers) < 5:
        spawn_flower()
    root.after(12000, flower_spawner_loop)

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

# Bee logic
def start_bee():
    def bee_fly(from_left=True, t=0, x=-60):
        global score
        y_base = random.randint(100, 300)
        frequency = random.uniform(0.05, 0.15)
        amplitude = random.randint(20, 60)
        step = 5 if from_left else -5
        bee_img = bee_img_right if from_left else bee_img_left
        bee_photo_local = ImageTk.PhotoImage(bee_img)
        canvas.itemconfig(bee, image=bee_photo_local)
        canvas.image = bee_photo_local  # Prevent garbage collection

        def move():
            global score
            nonlocal t, x
            if (from_left and x > 800) or (not from_left and x < -60):
                score += 5
                score_label.config(text=f"Score: {score}")
                canvas.coords(bee, -100, 100)
                root.after(6000, lambda: bee_fly(random.choice([True, False])))
                return
            y = y_base + int(amplitude * math.sin(frequency * t))
            canvas.coords(bee, x, y)
            x += step
            t += 1
            root.after(20, move)

        move()

    bee_fly(from_left=True)

def buy_bee_upgrade():
    global has_bee_upgrade, score
    if not has_bee_upgrade and score >= 100:
        score -= 100
        score_label.config(text=f"Score: {score}")
        has_bee_upgrade = True
        bee_button.config(state="disabled")
        start_bee()

bee_button = tk.Button(root, text="Buy Bee (100)", font=("Arial", 14), command=buy_bee_upgrade)
bee_button.place(x=10, y=200)

root.mainloop()
