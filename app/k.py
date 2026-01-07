import turtle
import random

def draw_poly(k, poly, color):
    k.up()
    k.goto(poly[0])
    k.down()
    k.color(color)
    k.begin_fill()
    for x, y in poly:
        k.goto(x, y)
    k.end_fill()

def draw_star(k, x, y, size, color):
    k.up()
    k.goto(x, y)
    k.setheading(0)
    k.color(color)
    k.begin_fill()
    k.down()
    for _ in range(5):
        k.forward(size)
        k.right(144)
    k.end_fill()

screen = turtle.Screen()
screen.bgcolor("black")
k = turtle.Turtle()
k.speed(0)

colors = ["yellow", "orange", "red", "cyan", "white", "pink"]
for _ in range(25):
    draw_star(k, random.randint(-350, 350), random.randint(-300, 300),
              20, random.choice(colors))

poly_R = [(-150, 80), (-90, 80), (-90, 20), (-120, 20),
          (-120, -80), (-150, -80),
          (-150, 80), (-90, 80), (-90, 50),
          (-120, 50), (-120, 20), (-90, 20),
          (-60, -80), (-90, -80)]
poly_A = [(-40, -80), (-10, 80), (10, 80), (40, -80),
          (15, -80), (8, -40), (-8, -40), (-15, -80)]
poly_H = [(70, 80), (100, 80), (100, 20), (130, 20),
          (130, 80), (160, 80), (160, -80),
          (130, -80), (130, -20), (100, -20),
          (100, -80), (70, -80)]


draw_poly(k, poly_R, "deep sky blue")
draw_poly(k, poly_A, "green yellow")
draw_poly(k, poly_H, "orangered")

k.up()
k.color("white")
k.goto(0, 250)
k.write("Roll No: 50 | Name: Rahul Narayanan", align="center", font=("Arial", 18, "bold"))

k.goto(0, -280)
k.color("red")
k.write("Merry Xmas", align="center", font=("Arial", 22, "italic"))

k.hideturtle()
screen.mainloop()