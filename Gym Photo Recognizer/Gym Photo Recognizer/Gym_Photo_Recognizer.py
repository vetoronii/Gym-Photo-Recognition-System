from asyncio.windows_events import NULL
from cProfile import label
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mess
from tkinter.font import BOLD
from tkinter import filedialog
from turtle import title
import numpy as np
import pandas as pd
import os
import cv2
import glob
import h5py
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

##################################### Small Functions ##################################################
def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

def instruction():
    mess._show(title='Instruction', 
    message='USER INSTRUCTION \n\n 1. Go to Recognize page. \n 2. Upload your image. \n 3. Click Recognize. \n 4. Obtain result.')


##################################### Important Functions #########################################
def uploadImage():
    global filename
    message1.config(text='Uploading Image...')
    """
    1. Open file explorer
    2. Choose file
    3. Try to upload file

    if(image uploaded):
        message1.config(text='Ready to Analyze!')
        return
    """
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Portable Graphics Format", "*.png"),
                                          ("all files","*.*")
                                          )
                                          )
    message1.config(text='Upload Complete! Ready to Predict.')
    img.config(file=filename)
    imgLabel.config(image=img)

    


    

def recognizeImage():
    message1.config(text='Prediction Complete!')

    path = h5py.File('images.h5','r')
    X = np.array(path.get('image'))
    path_label = h5py.File('labels.h5','r')
    y = np.array(path_label.get('label'))

    scaler = StandardScaler()
    scaler.fit(X)

    knn = KNeighborsClassifier(n_neighbors=1, p=1)
    knn.fit(X, y)

    image = cv2.imread(filename)
    res = cv2.resize(image, dsize=(200, 150), interpolation=cv2.INTER_CUBIC)
    image_np = np.array(res).astype("uint8")
    image_np_reshape = image_np.reshape(-1, 150*200*3)

    pred = knn.predict(image_np_reshape)

    if pred == 1:
        mess._show(title='Prediction', message='Anytime Fitness')
    
    elif pred == 2:
        mess._show(title='Prediction', message='7 Days Fitness')

    elif pred == 3:
        mess._show(title='Prediction', message='Top Speed Fitness')

    elif pred == 4:
        mess._show(title='Prediction', message='The X Gym')

    elif pred == 5:
        mess._show(title='Prediction', message='Surya Gym')

    message1.config(text='Ready for next image.')

    return

    """
    1. Start to analyze the image
    2. Give prediction
    3. Set message1 to prediction
    """


###################################### GUI #######################################################
def recognize():
    global recognize_window, message1, imgFrame, img,imgLabel

    window.destroy()
    recognize_window = Tk()
    recognize_window.title('Gym Photo Recognizer/Recognize')
    recognize_window.geometry('600x500')
    recognize_window.focus_force()
    recognize_window.resizable(False, False)

    recognize_window.iconbitmap('media/Mini-Robot.ico')


    h1 = Label(recognize_window, text='Upload Image to Recognize!', font=("Times New Roman", 25))
    h1.pack()

    imgFrame = Frame(recognize_window)
    imgFrame.place(relx=0.2, rely=0.10, relwidth=0.6, relheight=0.45)

    img = PhotoImage()
    imgLabel = Label(imgFrame)
    imgLabel.pack()

    msgFrame = Frame(recognize_window)
    msgFrame.place(relx=0.2, rely=0.55, relwidth=0.6)

    message1 = Label(msgFrame, text='No Image Data', font=("Courier New", 12))
    message1.pack()

    upload = Button(recognize_window, text='Upload Image', fg='black', bg='yellow', font=("Courier New", 15), command=uploadImage)
    upload.place(relx=0.2, rely=0.65, relwidth=0.6)
    changeOnHover(upload, '#fffbc3', 'yellow')

    analyze = Button(recognize_window, text='Start Analyzing', fg='white', bg='blue', font=("Courier New", 15), command=recognizeImage)
    analyze.place(relx=0.2, rely=0.8, relwidth=0.6)
    changeOnHover(analyze, '#3da8ff', 'blue')


    back = Button(recognize_window, text='Back', fg='white', bg='blue', font=("Courier New", 15), command=main_window)
    back.place(relx=0.01, rely=0.01)
    changeOnHover(back, '#3da8ff', 'blue')


def main_window():    
    global window

    try:
        recognize_window.destroy()
    except:
        pass
    
    window=Tk()
    window.title('Gym Photo Recognizer')
    window.geometry('600x500')
    window.focus_force()
    window.resizable(False, False)

    window.iconbitmap('media/Mini-Robot.ico')

    h1 = Label(window, text='Gym Photo Recognizer', font=("Times New Roman", 25))
    h1.pack()

    h2 = Label(window, text='BY GROUP VEGE', fg='green',font=("Times New Roman", 12, BOLD))
    h2.pack()

    frame1 = Frame(window, bg='#c5d3dc')
    frame1.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.5)

    b1 = Button(frame1, text='Recognize', fg='black', bg='yellow', font=("Courier New", 20), command=recognize)
    b1.place(relx=0.15, rely=0.1, relwidth=0.7)
    changeOnHover(b1, '#fffbc3', 'yellow')

    b2 = Button(frame1, text='Help', fg='white', bg='blue', font=("Courier New", 20), command=instruction)
    b2.place(relx=0.15, rely=0.4, relwidth=0.7)
    changeOnHover(b2, '#3da8ff', 'blue')

    b3 = Button(frame1, text='Quit', fg='black', bg='red', font=("Courier New", 20), command=window.destroy)
    b3.place(relx=0.15, rely=0.7, relwidth=0.7)
    changeOnHover(b3, '#ff9393', 'red')

    window.mainloop()


main_window()