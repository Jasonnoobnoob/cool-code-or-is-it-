from tkinter import PhotoImage

class Ball:
    def __init__(self, canvas, x, y, radius, dx, dy, fill, outline, distortion):
        self.canvas = canvas
        self.id = canvas.create_oval(x, y, x + radius * 2, y + radius * 2 - distortion, fill=fill, outline=outline)
        self.radius = radius
        self.dx = dx
        self.dy = dy

    def move(self):
        self.canvas.move(self.id, self.dx, self.dy)

