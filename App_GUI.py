from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
from PIL import ImageOps
import numpy as np

path = 'D:\\PYTHON\\Machine Learning\\Digit Recognizer\\'
model = load_model(path+'digit_recognizer_kaggle.h5')
def predict_digit(img, invert):
    if invert:
        img = ImageOps.invert(img)
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)

class App(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.line_width = 8
        self.line_color = "white"
        self.bg_color = "black"

        self.resizable(False, False)
        #Keep same ratio when expanding
        for i in range(0,2):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = self.bg_color, cursor="cross")
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        self.button_color = tk.Button(self, text="Switch Colors", command=self.switch_colors)

        #Format Width button
        self.width = tk.Frame(self)
        # + and - button
        self.button_width_minus = tk.Button(self.width, text="-", command=self.decrease_width)
        self.button_width_minus.pack(side = LEFT, padx = 2, pady=2)

        self.label_width = tk.Label(self.width, text="Width: {}".format(self.line_width))
        self.label_width.pack(side=LEFT)

        self.button_width_plus = tk.Button(self.width, text="+", command=self.increase_width)
        self.button_width_plus.pack(side = LEFT, padx = 2, pady=2)
        
        
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky="nsew")
        self.label.grid(row=0, column=1, pady=2, padx=2, sticky="nsew")
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2, sticky="nsew")
        self.button_clear.grid(row=1, column=0, pady=2, sticky="nsew")
        self.button_color.grid(row=2, column=0, pady=2, sticky="nsew")
        self.width.grid(row=2, column=1, pady=2)

        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def switch_colors(self):
        self.line_color, self.bg_color = self.bg_color, self.line_color
        self.canvas.config(bg=self.bg_color)
        self.canvas.itemconfig("draw_line", fill=self.line_color)
    
    def increase_width(self):
        self.line_width += 1
        self.label_width.config(text="Width: {}".format(self.line_width))
    
    def decrease_width(self):
        self.line_width -= 1
        self.line_width = max(1, self.line_width)
        self.label_width.config(text="Width: {}".format(self.line_width))

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        im = ImageGrab.grab(rect)
        invert = (self.line_color == 'black')
        digit, acc = predict_digit(im, invert)
        self.label.configure(text= f'Digit: {digit} \nAccuracy: {int(acc*100)}%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = self.line_width // 2
        self.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=self.line_color, tags="draw_line")

app = App()
mainloop()