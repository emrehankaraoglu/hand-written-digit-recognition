from tensorflow.keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import numpy as np

model = load_model("digit.h5")
model.load_weights("digit_weight.h5")

def digit_prediction(image):
    image = image.resize((28,28))
    
    image = image.convert('L')
    image = np.array(image)
    
    image = image.reshape(1,28,28,1)
    image = image/255.0
    
    pred = model.predict(image)[0]
    return np.argmax(pred), max(pred)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        
        self.canvas = tk.Canvas(self,width = 200, height=200,
                               bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Gimme digit!", font=("Courier New", 36))
        self.classify_btn = tk.Button(self, text = "Predict", command =  self.classify_handwriting)
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND) 
        im = ImageGrab.grab(rect)
        digit, acc = digit_prediction(im)
        self.label.configure(text= "Prediction : "+str(digit)+' \n '+ "Accuracy   : " +str(int(acc*100))+'%')
        
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=12
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
        
app = App()
mainloop()