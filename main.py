#Simple Snake Game created using Python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty,NumericProperty,ReferenceListProperty,ListProperty,BooleanProperty,OptionProperty
from kivy.vector import Vector
from kivy.graphics import Rectangle,Triangle
from kivy.clock import Clock
from random import randint
class Garden(Widget):
	snek=ObjectProperty(None)
	food=ObjectProperty(None)
	col=16
	row=9
	score=NumericProperty(0)
	count=NumericProperty(0)
	food_rytm=NumericProperty(0)
	touch_start_pos=ListProperty()
	act_trig=BooleanProperty(False)
	def start(self):
		self.new_snek()
		self.update()
	def reset(self):
		self.count=0
		self.score=0
		self.snek.rem()
		self.food.rem()
	        Clock.unschedule(self.pop_food)
	        Clock.unschedule(self.food.rem)
	        Clock.unschedule(self.update)
	def new_snek(self):
		start=(8,5)
		self.snek.set_pos(start)
		dire=["R"][0]
		self.snek.set_dir(dire)
	def pop_food(self,*args):
		rand_coord=[randint(1,self.col),randint(1,self.row)]
		snek_space = self.snek.get_full_pos()
		while rand_coord in snek_space:
            		rand_coord = [randint(1, self.col), randint(1, self.row)]
		self.food.pop(rand_coord)
	def defeat(self):
		snek_pos=self.snek.get_pos()
		if snek_pos in self.snek.t.blk_pos:
			return True
		if snek_pos[0]>self.col or snek_pos[0]<1 or snek_pos[1]>self.row or snek_pos[1]<1:
			return True
		return False
	def update(self,*args):
		if self.count==0:
			self.food_rytm=self.food.intl+self.food.dur
			Clock.schedule_interval(self.food.rem,self.food_rytm)
		elif self.count==self.food.intl:
			Clock.schedule_interval(self.pop_food,self.food_rytm)
		self.snek.move()
		if self.defeat():
			self.reset()
			self.start()
			return
		if self.food.is_board():
			if self.snek.get_pos()==self.food.pos:
				self.food.rem()
				self.score+=1
				self.snek.t.size+=1
		self.count+=1
		Clock.schedule_once(self.update,1)
	def on_touch_down(self,touch):
		self.touch_start_pos=touch.spos
	def on_touch_move(self,touch):
		delta=Vector(*touch.spos)-Vector(*self.touch_start_pos)
		if not self.act_trig and (abs(delta[0])>0.1 or abs(delta[1])>0.1):
			if abs(delta[0])>abs(delta[1]):
				if delta[0]>0:
					self.snek.set_dir("R")
				else:
					self.snek.set_dir("L")
			else:
				if delta[1]>0:
					self.snek.set_dir("U")
				else:
					self.snek.set_dir("D")
			self.act_trig=True
	def on_touch_up(self,touch):
		self.act_trig=False
class Food(Widget):
	dur=NumericProperty(10)
	intl=NumericProperty(3)
	ob_board=ObjectProperty(None)
	state=BooleanProperty(False)
	def is_board(self):
		return self.state
	def rem(self,*args):
		if self.is_board():
			self.canvas.remove(self.ob_board)
			ob_board=ObjectProperty(None)
			self.state=False
	def pop(self,pos):
		self.pos=pos
		with self.canvas:
			x=(pos[0]-1)*self.size[0]
			y=(pos[1]-1)*self.size[1]
			coor=(x,y)
			self.ob_board=Rectangle(pos=coor,size=self.size)
			self.state=True
class Snek(Widget):
	h=ObjectProperty(None)
	t=ObjectProperty(None)
	def move(self):
		next_tpos=list(self.h.pos)
		self.h.move()
		self.t.add_blk(next_tpos)
	def rem(self):
		self.h.rem()
		self.t.rem()
	def set_pos(self,pos):
		self.h.pos=pos
	def get_pos(self):
		return self.h.pos
	def get_full_pos(self):
		return self.h.pos+self.t.blk_pos
	def set_dir(self,dit):
		self.h.dit=dit
	def get_dir(self):
		return self.h.dir
class H(Widget):
	dit=ObjectProperty("R",ops=["U","D","L","R"])
	x_pos=NumericProperty(0)
	y_pos=NumericProperty(0)
	pos=ReferenceListProperty(x_pos,y_pos)
	points=ListProperty([0]*6)
	ob_board=ObjectProperty(None)
	state=BooleanProperty(False)
	def is_board(self):
		return self.state
	def rem(self):
		if self.is_board():
			self.canvas.remove(self.ob_board)
			self.ob_board=ObjectProperty(None)
			self.state=False
	def show(self):
		with self.canvas:
			if not self.is_board():
				self.ob_board=Rectangle(points=self.points)
				self.state=True
			else:
				self.canvas.remove(self.ob_board)
				self.ob_board=Triangle(points=self.points)
	def move(self):
		if self.dit=="R":
			self.pos[0]+=1
        	    	x0=self.pos[0]*self.width
            		y0=(self.pos[1]-0.5)*self.height
            		x1=x0-self.width
            		y1=y0+self.height/2
            		x2=x0-self.width
            		y2=y0-self.height/2
        	elif self.dit=="L":
            		self.pos[0]-=1
            		x0=(self.pos[0]-1)*self.width
            		y0=(self.pos[1]-0.5)*self.height
            		x1=x0+self.width
            		y1=y0-self.height/2
            		x2=x0+self.width
            		y2=y0+self.height/2
        	elif self.dit=="U":
            		self.pos[1]+=1
            		x0=(self.pos[0]-0.5)*self.width
            		y0=self.pos[1]*self.height
            		x1=x0-self.width/2
            		y1=y0-self.height
            		x2=x0+self.width/2
            		y2=y0-self.height
        	elif self.dit=="D":
            		self.pos[1]-=1
            		x0=(self.pos[0]-0.5)*self.width
            		y0=(self.pos[1]-1)*self.height
            		x1=x0+self.width/2
            		y1=y0+self.height
            		x2=x0-self.width/2
            		y2=y0+self.height
		self.points=[x0,y0,x1,y1,x2,y2]
		self.show()
class T(Widget):
	size=NumericProperty(2)
	blk_pos=ListProperty()
	t_blk_obs=ListProperty()
	def rem(self):
		self.size=2
		for blck in self.t_blk_obs:
			self.canvas.remove(blck)
		self.blk_pos=[]
		self.t_blk_pos=[]
	def add_blk(self,pos):
		self.blk_pos.append(pos)
		if len(self.blk_pos)>self.size:
			self.blk_pos.pop(0)
		with self.canvas:
			for blck_pos in self.blk_pos:
				x=(blck_pos[0]-1)*self.width
				y=(blck_pos[1]-1)*self.height
				coord=(x,y)
				blck=Rectangle(pos=coord,size=(self.width,self.height))
				self.t_blk_obs.append(blck)
				if len(self.t_blk_obs)>self.size:
					last_blk=self.t_blk_obs.pop(0)
					self.canvas.remove(last_blk)
class SnekApp(App):
	game_engine=ObjectProperty(None)
	def on_start(self):
		self.game_engine.start()
	def build(self):
		self.game_engine=Garden()
		return self.game_engine
if __name__=='__main__':
	SnekApp().run()
