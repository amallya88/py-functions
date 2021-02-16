import turtle
import math
wn = turtle.Screen()
wn.screensize(480,640)


t = turtle.Turtle()

t.pen(pencolor="black", fillcolor="yellow")
t.speed(20)

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
for j in range(petals):
    if j % 2 == 0:
        t.setheading((360/petals)/2)
    else:
        t.setheading((360/petals))
    layer_heading = t.heading()
    for i in range(petals):
        draw_petal(t, next_petalSize, angle)
        t.setheading(layer_heading + (360/petals)*(i+1))
    next_petalSize -= (size*0.618)/petals

t.dot(next_petalSize/2)
t.hideturtle()
"""
t.fillcolor('brown')
t.up()
t.circle(size,angle)
t.setheading(90+math.degrees(math.asin(t.ycor()/t.distance(0,0))))
t.down()
for i in range(petals):
    t.begin_fill()
    t.circle(t.distance(0,0), 360/petals)
    t.end_fill()
"""

wn.exitonclick()