from graph import*
from math import*
g=2
time = 0
dt = 5
vx0=5
vy0=5
x0=5
y0=300
canvasSize(1005,605)
windowSize(1005,605)
x=x0
y=y0
vx=vx0
vy=-vy0
def anim():
	global time
	global x
	global y
	global x0
	global y0
	global vx0
	global vy0
	global vx
	global vy
	global g
	brushColor('yellow')
	rectangle(0,0,1005,605)
	brushColor('red')
	if x > 995 or x < 5:
		if x > 1000:
			x=1000
		vx=-vx
		time = 0
	if y <= 595 and y >= 5:
		vy=vy+g*dt
	else:
		if y > 595:
			y=595
		vy = -vy+g*dt
		time = 0
	x=x+vx*dt
	y=y+vy*dt
	circle(x,y,5)
	time+=dt
onTimer(anim,dt)
run()
