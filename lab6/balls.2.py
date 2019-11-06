from random import randrange as rnd, choice
from tkinter import *
import time

root = Tk()
root.geometry('800x600')

updateTime = 30
balls = []

l = Label(bg='black', fg='white', width=20)
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']


class ball:                  #класс мячиков
    def __init__(self):
        self.x = rnd(65, 735)      #рандомная координата x
        self.y = rnd(65, 535)      #рандомная координата y
        self.vx = rnd(-15, 15)    #рандомная скорость vx
        self.vy = rnd(-15, 15)    #рандомная скорость vy
        self.r = rnd(0, 50)       #рандомный радиус r
        self.object = canv.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r,
                                       fill=choice(colors), width=0)              #создание овала

    def rebound(self):      #столконовения со стенкой
        if (self.x + self.r > 800) or (self.x - self.r < 0):
            self.vx = -self.vx   #изменение скорости vx
        if (self.y + self.r > 580) or (self.y - self.r < 0):
            self.vy = -self.vy   #изменение скорости vy

    def move(self):              #движение
        canv.move(self.object, self.vx, self.vy)
        self.x += self.vx
        self.y += self.vy

def updateScene():               #обновление картинки
    for b in balls:
        b.move()
        b.rebound()
    root.after(updateTime, updateScene)

score = 0
def click(event):                #подсчёт очков
    global score
    for b in balls:
        if (event.x - b.x) ** 2 + (event.y - b.y) ** 2 <= b.r ** 2:
            score += 10
        print(score)
        l['text']=score

#Создание шариков, количество можно изменять
for i in range(17):
    balls.append(ball())

root.after(updateTime, updateScene)
canv.bind("<Button-1>", click)
l.pack()
mainloop()
