import turtle
import math
wn = turtle.Screen()
wn.screensize(480,640)

t = turtle.Turtle()

t.pen(pencolor="black", fillcolor="yellow")
t.speed(0)

def draw_petal(turtleName, size, angle):
    init_heading = turtleName.heading()
    turtleName.begin_fill()
    turtleName.circle(size,angle)
    turtleName.setheading(init_heading+180)
    turtleName.circle(size,angle)
    turtleName.end_fill()

petals=8
size=300
angle=64
next_petalSize = size
for j in range(petals**2):
    layer_heading = t.heading()
    draw_petal(t, next_petalSize, angle)    
    t.setheading(layer_heading+(360*0.618))
    if(t.heading() < layer_heading):
        next_petalSize -= (size*0.618)/petals**2

t.dot(next_petalSize/2)
t.hideturtle()

wn.exitonclick()