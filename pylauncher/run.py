#!/usr/bin/python3
#-*-code:UTF-8-*-
from tkinter import *
from code.windows import MainWindow, QuietPopuWindow, PopupWindow
from code.buttons import *
from code.dialogs import FileDlg
from code.buttons import OpenFile

CONFIG = os.path.abspath('./config.txt')
def addProgram():
	newprogram = QuietPopuWindow('新增程序')
	labels = [('新程序名称',None,None),
			  ('新程序路径','浏览文件...',OpenFile)]
	FileDlg(labels,newprogram, Root, CONFIG)

def editProgram():
	PopupWindow('editor')

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

Root = MainWindow('简易启动菜单')
makeEntries()
NewProgram(parent=Root, command=addProgram)
EditProgram(parent=Root, command=editProgram)
Quitter(Root)

Root.mainloop()