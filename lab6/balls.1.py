from tkinter import *
from random import randrange as rnd, choice
import time

root = Tk()
root.geometry('800x600')

l = Label(bg='black', fg='white', width=20)
canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)


N=0
ball=None

colors = ['red','orange','yellow','green','blue']
def new_ball():
	global x,y,r, N, ball, x, y, v_x, v_y, timerid
	canv.delete(ALL)
	x = rnd(100,700)
	y = rnd(100,500)
	r = rnd(30,50)
	v_x = rnd(-5,5)
	v_y = rnd(-5,5)
	ball=canv.create_oval(x-r,y-r,x+r,y+r,fill = choice(colors), width=0)
	timerid = root.after(1000,new_ball)


ident = 0
def move():
	global x, y, r, v_x, v_y
	canv.move(ball,v_x,v_y)
	x=x+v_x
	y=y+v_y
	if x+r>800 or x-r<0:
		v_x=-v_x
	if y+r>580 or y-r<0:
		v_y=-v_y
	root.after(10,move)

score = 0
def click(event):
	global score
	if ((event.x-v_x-x)**2+(event.y-y-v_y)**2) <= (r**2):
		score += 10
	print(score)
	l['text'] = score



new_ball()
canv.bind('<Button-1>', click)
move()
l.pack()
mainloop()
