import numpy as np
import pandas as pd

from time import sleep

from copy import deepcopy

from State import State, toPrice

from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

class MyFirstGUI:
	def __init__(self, master):

		# Initialize the game state
		self.states = [	State("datasets/avocado/avocado_sets.npy", 100, categories=np.load("datasets/avocado/avocado_columns.npy"),
							title = "Avocado prices", question="How is the price compared to:   "),
						State("datasets/water/water_sets.npy", 100, categories=np.load("datasets/water/water_categories.npy"),
							title = "Water potability", question="How is the potability compared to:  ", is_binary=True),
						State("datasets/nba/nba_sets.npy", 100, categories=np.load("datasets/nba/nba_categories.npy"),
							title = "NBA Player stats", question="How is the points average compared to: ")
						]
		self.state 		= self.states[0]
		self.states_num = len(self.states)
		# Main window characterization
		self.master = master
		master.title("Jungle Game")
		master.geometry("1280x768")
		master.resizable(False, False)
		
		# Style specification
		self.background_color = "#bc784b"
		self.text_color = "#ffd599"
		self.font = "Garamond"

		self.xstarts = [715, 830, 950, 1069]
		self.ystarts = [180, 220, 250, 280, 310, 340, 370]
		self.widths  = [115, 120, 100, 70]
		self.heights = [30, 30, 30, 30, 30, 30, 30]

		# Background frame
		self.bg_frame = Frame(master)
		self.bg_frame.place(height=768, width=1280, x=0, y=0)
		# Title frame
		self.title_frame = Frame(master, bg = self.background_color)
		self.title_frame.place(height=45, width = 500, x=680, y = 90)
		self.title_label = Label(self.title_frame, text = "", bg=self.background_color,
								font=self.font+" 30 italic bold")
		self.title_label.pack()
		# Data frames
		self.data_frames = []
		self.data_labels = []
		self.data_frames.append([])
		self.data_labels.append([])
		for i in range(4):
			self.data_frames[0].append(Frame(master, bg=self.background_color))
			self.data_frames[0][i].place(height=self.heights[0], width=self.widths[i], x = self.xstarts[i], y = self.ystarts[0])
			self.data_labels[0].append(Label(self.data_frames[0][i], text = str(i), bg=self.background_color,
											font=self.font+" 12 italic bold"))
			self.data_labels[0][i].pack()
		for i in range(6):
			self.data_frames.append([])
			self.data_labels.append([])
			for j in range(4):
				self.data_frames[-1].append(Frame(master, bg=self.background_color))
				self.data_frames[-1][-1].place(height=self.heights[i+1], width=self.widths[j], x=self.xstarts[j], y = self.ystarts[i+1])
				self.data_labels[-1].append(Label(self.data_frames[-1][j], text = str(i*4+j+4), bg=self.background_color,
											font=self.font+" 12 italic bold"))
				self.data_labels[-1][-1].pack()
		# Coin display frame		
		self.coin_frame = Frame(master, bg=self.background_color)
		self.coin_frame.place(height="30", width="100", x=130, y=51)
		self.coin_label = Label(self.coin_frame, text = "", bg=self.background_color,
								font=self.font+" 27 bold")
		self.coin_label.pack()
		# Prediction frame		
		self.pred_frame = Frame(master, bg=self.background_color)
		self.pred_frame.place(height="58", width="500", x=680, y=515)
		self.pred_label = Label(self.pred_frame, text="eee", bg=self.background_color,
								font=self.font+" 18 italic bold")
		self.pred_label.pack()
		# Bet frames
		self.bet_sub_frame = Frame(master, bg="red")
		self.bet_sub_frame.place(height=40, width = 40, x = 640, y = 660)
		self.bet_add_frame = Frame(master, bg="red")
		self.bet_add_frame.place(height=40, width = 40, x = 760, y = 660)
		self.bet_frame = Frame(master, bg=self.background_color)
		self.bet_frame.place(height=40, width = 80, x = 680, y = 660)
		self.bet_text = Label(self.bet_frame, text="0", bg=self.background_color,
								font=self.font+" 32 italic bold")
		# Higher frame
		self.high_frame = Frame(master)
		self.high_frame.place(height=100, width = 175, x = 875, y = 630)
		# Lower frame
		self.low_frame = Frame(master)
		self.low_frame.place(height=100, width = 175, x = 1075, y = 630)

		# Next frame
		self.next_frame = Frame(master, bg="red")

		self.update_data()

		# Background frame initialization
		self.bg_label = Label(self.bg_frame)
		img = Image.open("images/bg_def.jpg")
		self.bg_label.img = ImageTk.PhotoImage(img)
		self.bg_label['image'] = self.bg_label.img
		self.bg_label.pack()




		# Buttons
		self.button_image = ImageTk.PhotoImage(Image.open("images/button.gif"))  
		self.button_long_image = ImageTk.PhotoImage(Image.open("images/long_button.gif"))  

		self.button_next = Button(self.next_frame, text = "NEXT QUESTION", height = 125, width = 650, command=self.next_question,
						image = self.button_long_image, fg = self.text_color, compound='center',
						font=self.font+" 35 italic bold")
		self.button_high = Button(self.high_frame, text='HIGHER', height = 100, width = 175, command=self.click_higher,
						image = self.button_image, fg = self.text_color, compound='center',
						font=self.font+" 27 italic bold")
		self.button_high.pack()
		
		self.button_low = Button(self.low_frame, text='LOWER', height = 100, width = 175, command=self.click_lower,
						image = self.button_image, fg = self.text_color, compound='center',
						font=self.font+" 27 italic bold")
		self.button_low.pack()

		self.button_add = Button(self.bet_add_frame, height=40, width=40, text="+", command=self.add_bet, bg=self.background_color)
		self.button_sub = Button(self.bet_sub_frame, height=40, width=40, text="-", command=self.sub_bet, bg=self.background_color)

		self.button_sub.pack()
		self.bet_text.pack()
		self.button_add.pack()


	def click_higher(self):

		self.data_labels[6][3]['text'] = self.state.answer[3]

		if self.state.checkAnswer(True):
			img = Image.open("images/bg_good.jpg")
		else:
			img = Image.open("images/bg_mad.jpg")
		self.bg_label.img = ImageTk.PhotoImage(img)
		self.bg_label['image'] = self.bg_label.img
		self.next_frame.place(height=125, width = 650, x=600, y=620)
		self.button_next.pack()

		self.state.updateState(True, int(self.bet_text['text']))
		current_gold = self.state.gold
		self.state = self.states[np.random.randint(0, len(self.states))]
		self.state.gold = current_gold


	def click_lower(self):
		self.data_labels[6][3]['text'] = self.state.answer[3]
		
		if self.state.checkAnswer(False):
			img = Image.open("images/bg_good.jpg")
		else:
			img = Image.open("images/bg_mad.jpg")
		self.bg_label.img = ImageTk.PhotoImage(img)
		self.bg_label['image'] = self.bg_label.img
		self.next_frame.place(height=125, width = 650, x=600, y=620)
		self.button_next.pack()
		
		self.state.updateState(False, int(self.bet_text['text']))
		current_gold = self.state.gold
		self.state = self.states[np.random.randint(0, len(self.states))]
		self.state.gold = current_gold

	def add_bet(self):
		val = int(self.bet_text.cget("text"))
		self.bet_text["text"]=str(min(val+1, self.state.gold))
	
	def sub_bet(self):
		val = int(self.bet_text.cget("text"))
		self.bet_text["text"]=str(max(val-1, 0))
		
	def next_question(self):
		self.next_frame.place_forget()
		self.button_next.pack_forget()
		img = Image.open("images/bg_def.jpg")
		self.bg_label.img = ImageTk.PhotoImage(img)
		self.bg_label['image'] = self.bg_label.img

		self.update_data()
	
	def click_next(self):
		return 0

	def update_data(self):
		for i in range(4):
			self.data_labels[0][i]['text'] = self.state.categories[i]
		for i in range(1,6):
			for j in range(4):
				self.data_labels[i][j]['text'] = str(self.state.query[i-1][j])
				if type(self.state.query[i-1][j]) is np.float64:
					self.data_labels[i][j]['text'] = toPrice(self.state.query[i-1][j])
		for i in range(3):
			self.data_labels[6][i]['text'] = str(self.state.answer[i])
			if type(self.state.answer[i]) is np.float64:
				self.data_labels[6][i]['text'] = toPrice(self.state.answer[i])		
		self.data_labels[6][3]['text'] = '?'

		self.title_label['text'] = self.state.title
		self.coin_label['text'] = self.state.gold
		self.pred_label['text'] = self.state.question+str(toPrice(self.state.getPrediction()))
		self.bet_text['text'] = str(self.state.gold//10)

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()