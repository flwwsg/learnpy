#!/usr/bin/python3
#-*-code:UTF-8-*-
import os
from tkinter import *
from code.buttons import *
from code.windows import MainWindow, QuietPopuWindow, PopupWindow
from code.dialogs import FileDlg
from code.scrolledlist import ScrolledList

path = os.getcwd()
path = os.path.join(path, 'config.txt')
CONFIG = path

def addProgram(root):
	labels = [('新程序名称',None,None),
			  ('新程序路径','浏览文件...',OpenFile)]
	fdlg = FileDlg(labels,root)
	return fdlg

def editProgram():
	labels = dict(a='a', b='b', c='path')
	root = PopupWindow('editor')
	fdlg = addProgram(root)
	btnroot = Frame(root)
	btnroot.pack(side=RIGHT)
	slist = ScrolledList(labels,root)
	CustomBtn('Add', lambda: addNewFile(slist, fdlg) ,btnroot)
	CustomBtn('Up', lambda: moveUpline(slist) ,btnroot)
	CustomBtn('Down', lambda:moveDownline(slist) ,btnroot)
	CustomBtn('Del', lambda:deline(slist) ,btnroot)
	CustomBtn('SaveAll', lambda:saveAll(slist) ,btnroot)


def saveConfig():
	pass

def addNewFile(slist, fdlg):
	fname, fpath = fdlg.onSubmit()
	slist.listbox.insert(END, fname)

def moveUpline(slist):
	print('move up')

def moveDownline(slist):
	print('move down')

def deline(slist):
	index = slist.listbox.curselection()
	length = slist.listbox
	# label = slist.listbox.get(index)
	print(index, END)
	for i in range(index, END):
		print(index)
	# slist.listbox.delete(index)

def saveAll(slist):
	print('save all')

def makeEntries(root):
	lines = open(CONFIG, encoding='utf-8').readlines()
	for line in lines:
		line = line.lstrip().rstrip()
		if not line:
			continue
		fname, fpath = line.split('=')
		fname = fname.rstrip()
		fpath = fpath.lstrip()
		AddEntry(fname, fname, fpath, root)