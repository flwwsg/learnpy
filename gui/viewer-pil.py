'''viewer-pil.py'''
import os,sys
from tkinter import *
from PIL.ImageTk import PhotoImage

imgdir = '../images/'
imgfile = 'forests1.jpg'
if len(sys.argv) > 1:
	imgfile = sys.argv[1]
imgpath = os.path.join(imgdir, imgfile)

win = Tk()
win.title(imgfile)
imgobj = PhotoImage(file=imgpath)
Label(win, image=imgobj).pack()
win.mainloop()
print(imgobj.width(), imgobj.height())
