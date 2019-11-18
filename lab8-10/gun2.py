from random import randrange as rnd, choice
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)

g = 2  # ускорение свободного падения
point = 1 # количество очков, прибавляемых за каждую уничтоженную цель
t = 0.03  # время между перерисовкой кадров

class ball():
	def __init__(self, x=40, y=450):
		""" Конструктор класса ball
		Args:
		x - начальное положение мяча по горизонтали
		y - начальное положение мяча по вертикали
		"""
		self.x = x
		self.y = y
		self.r = 10
		self.vx = 0
		self.vy = 0
		self.color = choice(['blue', 'green', 'red', 'brown'])
		self.id = canv.create_oval(
			self.x - self.r,
			self.y - self.r,
			self.x + self.r,
			self.y + self.r,
			fill=self.color
		)
		self.live = 30

	def set_coords(self):
		canv.coords(
			self.id,
			self.x - self.r,
			self.y - self.r,
			self.x + self.r,
			self.y + self.r
		)

	def move(self):
		"""Переместить мяч по прошествии единицы времени.
		Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
		self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
		и стен по краям окна (размер окна 800х600).
		"""
		if (self.x + self.r > 800 and self.vx > 0) or (self.x - self.r < 0 and self.vx < 0):  # отскок мяча
			self.vx = -self.vx
		if (self.y + self.r > 550 and self.vy < 0) or (self.y - self.r < 0 and self.vy > 0):
			self.vy = -self.vy
		self.vy = self.vy - 2  # гравитация
		self.x += self.vx
		self.y += -self.vy
		self.vx -= self.vx / 100  # вязкое трение
		self.vy -= self.vy / 100



	def hittest(self, obj):
		"""Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
		Args:
			obj: Обьект, с которым проверяется столкновение.
		Returns:
			Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
		"""
		if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2):
			return True

	def __del__(self):
		canv.delete(self.id)


class gun():
	def __init__(self):
		self.f2_power = 10
		self.f2_on = 0
		self.an = 1
		self.id = canv.create_line(20, 450, 50, 420, width=7)

	def fire2_start(self, event):
		self.f2_on = 1

	def fire2_end(self, event):
		"""Выстрел мячом.
		Происходит при отпускании кнопки мыши.
		Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
		"""
		global balls, bullet
		bullet += 1
		new_ball = ball()
		new_ball.r += 5
		self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
		new_ball.vx = self.f2_power * math.cos(self.an)
		new_ball.vy = - self.f2_power * math.sin(self.an)
		balls += [new_ball]
		self.f2_on = 0
		self.f2_power = 10

	def targetting(self, event=0):
		"""Прицеливание. Зависит от положения мыши."""
		if event:
			self.an = math.atan((event.y - 450) / (event.x - 20))
		if self.f2_on:
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')
		canv.coords(self.id, 20, 450,
					20 + max(self.f2_power, 20) * math.cos(self.an),
					450 + max(self.f2_power, 20) * math.sin(self.an)
					)

	def power_up(self):
		if self.f2_on:
			if self.f2_power < 100:
				self.f2_power += 1
			canv.itemconfig(self.id, fill='orange')
		else:
			canv.itemconfig(self.id, fill='black')

	#функция, отвечающая за возвращение пушки в первоначальное положение после победы
	def return_gun(self):
		self.f2_power = 0
		canv.itemconfig(self.id, fill='black')
		self.f2_on = 0

points = 0 #количество очков

class target():
	def __init__(self):
		self.points = 0
		self.live = 1
		self.id = canv.create_oval(0, 0, 0, 0)
		self.new_target()

	def new_target(self):
		""" Инициализация новой цели. """
		x = self.x = rnd(600, 780)
		y = self.y = rnd(300, 550)
		r = self.r = rnd(2, 50)
		color = self.color = 'red'
		canv.coords(self.id, x - r, y - r, x + r, y + r)
		canv.itemconfig(self.id, fill=color)

	def hit(self):
		"""Попадание шарика в цель."""
		global points
		canv.coords(self.id, -10, -10, -10, -10)
		points += point #прибавление очков за уничтоженную цель

t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = gun()
bullet = 0
balls = []
# Вывод очков на экран
canv.points = canv.create_text(100, 30, text='Количество очков: ' + str(points), font='28')
def new_game(event=''):
	global t1, t2, screen1, balls, bullet
	t1.new_target()
	t2.new_target()
	bullet = 0
	balls = []
	canv.bind('<Button-1>', g1.fire2_start)
	canv.bind('<ButtonRelease-1>', g1.fire2_end)
	canv.bind('<Motion>', g1.targetting)

	t1.live = 1
	t2.live = 1
	while (t1.live or t2.live) or balls:
		for b in list(balls):
			b.move()
			# удаление мячиков с маленькими скоростями
			if abs(b.vy) < g and b.y+b.r > 550:
				balls.remove(b)
				del(b)
				continue
			b.set_coords()
			if b.hittest(t1) and t1.live:
				t1.live = 0
				t1.hit()
				canv.itemconfig(canv.points, text='Количество очков: ' + str(points))
			if b.hittest(t2) and t2.live:
				t2.live = 0
				t2.hit()
				canv.itemconfig(canv.points, text='Количество очков: ' + str(points))
			if t1.live == 0 and t2.live == 0:
				canv.bind('<Button-1>', '')
				canv.bind('<ButtonRelease-1>', '')
				# возвращение вида пушки к первоначальному после уничтожения целей
				g1.return_gun()
				if bullet == 1:
					canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрел')
				if bullet >= 2 and bullet <= 4:
					canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрела')
				if bullet >= 5:
					canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
		canv.update()
		time.sleep(t)
		g1.targetting()
		g1.power_up()
	canv.itemconfig(screen1, text='')
	canv.delete(g1)
	root.after(750, new_game)

new_game()
tk.mainloop()
