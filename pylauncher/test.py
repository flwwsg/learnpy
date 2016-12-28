#!/usr/bin/python3
#-*-code:UTF-8-*-
from windows import MainWindow, QuietPopuWindow, PopupWindow
from buttons import *
from tkinter import *
from dialogs import FileDlg
from buttons import OpenFile

CONFIG = './config.txt'
def addProgram():
	newprogram = QuietPopuWindow('new program')
	labels = [('file name',None,None),
			  ('file location','OpenFile',OpenFile)]
	FileDlg(labels,newprogram, Root)

def makeEntries():
	lines = open(CONFIG, encoding='utf-8').readlines()
	for line in lines:
		line = line.lstrip().rstrip()
		if not line:
			continue
		fname, fpath = line.split('=')
		fname = fname.rstrip()
		fpath = fpath.lstrip()
		AddEntry(fname, fname, fpath, Root)

Root = MainWindow('Test demo')
makeEntries()
NewProgram(parent=Root, command=addProgram)
Quitter(Root)

Root.mainloop()