from tkinter import *
from random import randint
import winsound
from Attacks import *

window = Tk()
window.title("funny touhou game")
canvas = Canvas(window, width=1200, height=1000, background="black")
canvas.pack()
sprite_stop = PhotoImage(file="spirte1.png")
sprite_right = PhotoImage(file="right.png")
sprite_left = PhotoImage(file="left.png")
Letty = PhotoImage(file="Letty.png")
boss = canvas.create_image(150, -300, image=Letty)
canvas.move(boss, 480, 480)
sprite = canvas.create_image(605, 605, image=sprite_stop)
player = canvas.create_oval(600, 600, 609, 609, fill="white", outline="red", )
hitcount = 0
hitcounter = canvas.create_text(100, 750, text=str(hitcount) + " hitted", font=('bold', 20), fill="white")

speed = 5
dx, dy = 0, 0

balls = []



def update_player_position():
    global dx, dy
    canvas.move(player, dx, dy)
    canvas.move(sprite, dx, dy)  # Move the sprite along with the player
    window.after(20, update_player_position)


def move(event, direction):
    global dx, dy
    if direction == "stop":
        canvas.itemconfigure(sprite, image=sprite_stop)
        dx, dy = 0, 0
    else:
        dx, dy = speed * (direction.count("Right") - direction.count("Left")), speed * (
                direction.count("Down") - direction.count("Up"))
        canvas.itemconfigure(sprite, image=sprite_right if dx > 0 else sprite_left)


# Bind arrow keys for movement
for key in ["Left", "Right", "Up", "Down"]:
    window.bind(f"<KeyPress-{key}>", lambda event, key=key: move(event, key))
    window.bind(f"<KeyRelease-{key}>", lambda event, key=key: move(event, "stop"))

update_player_position()  # Start the update loop


def snow_rain(distortion, size, xv1, xv2, yv1, yv2, xs, xe, ys, ye):
    for i in range(200):
        b = Ball(canvas, randint(xs, xe), randint(ys, ye), size, randint(xv1, xv2), randint(yv1, yv2), "white",
                 'skyblue', distortion)
        balls.append(b)

def check_collision():
    global hitcount, invincible_time
    if invincible_time > 0:
        return  # If still invincible, do nothing

    player_pos = canvas.coords(player)
    player_center = [(player_pos[0] + player_pos[2]) / 2, (player_pos[1] + player_pos[3]) / 2]

    for ball in balls:
        ball_pos = canvas.coords(ball.id)
        ball_center = [(ball_pos[0] + ball_pos[2]) / 2, (ball_pos[1] + ball_pos[3]) / 2]

        distance = ((player_center[0] - ball_center[0]) ** 2 + (player_center[1] - ball_center[1]) ** 2) ** 0.5
        if distance < (player_pos[2] - player_pos[0]) / 2 + ball.radius:
            print("Collision!")
            hitcount += 1
            invincible_time = 30  # Set invincible time to 30 update cycles (600 ms at 20 ms interval)
            canvas.itemconfigure(hitcounter, text=hitcount)

def update_game():
    global invincible_time
    if invincible_time > 0:
        invincible_time -= 1  # Decrement invincible time
    for ball in balls:
        ball.move()
    check_collision()
    window.after(20, update_game)


# Initialize invincible time
invincible_time = 0

# fight sequence
winsound.PlaySound("music.wav", winsound.SND_ASYNC + winsound.SND_LOOP)
window.after(3000, lambda: snow_rain(5, 6, 1, 3, 2, 5, -1200, 1200, -300, 0))
window.after(7000, lambda: snow_rain(5, 6, 1, 3, 2, 5, -1200, 1200, -300, 0))
window.after(18000, lambda: snow_rain(0, 9, 0, 0, 4, 6, 0, 1200, -1000, 0))
window.after(28000, lambda: snow_rain(4, 7, 4, 7, 0, 1, -500, 0, 0, 1000))
window.after(40000, lambda: snow_rain(5, 6, 1, 3, 2, 5, -1200, 1200, -300, 0))
window.after(40000, lambda: snow_rain(5, 6, 1, 3, 2, 5, -1200, 1200, -300, 0))
window.after(40000, lambda: snow_rain(0, 9, 0, 0, 4, 6, 0, 1200, -1000, 0))
window.after(40000, lambda: snow_rain(4, 7, 4, 7, 0, 1, -500, 0, 0, 1000))

update_game()
window.mainloop()
