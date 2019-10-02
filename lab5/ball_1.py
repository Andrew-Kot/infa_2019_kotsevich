from graph import*
from math import*
time = 0
x = 1
y = 1
dt = 1
vx0=2
vy0=5
x0=0
y0=300
canvasSize(1000,600)
windowSize(1000,600)
def anim():
	global time
	global x
	global y
	global x0
	global y0
	global vx0
	global vy0
	brushColor('yellow')
	rectangle(0,0,1000,600)
	brushColor('red')
	if x > 1000 or x < 0:
		vx0=-vx0
		if x < 0:
			x = 0
		elif x > 600:
			x = 600
		x0=x
		y0=y
		time = 0
	if y > 600 or y < 0:
		vy0=-vy0
		if y < 0:
			y = 0
		elif y > 600:
			y = 600
		y0=y
		x0=x
		time = 0
	x=x0+vx0*time
	y=y0-vy0*time+time*time/50
	circle(x,y,5)
	time+=dt
onTimer(anim,5*dt)
run()
