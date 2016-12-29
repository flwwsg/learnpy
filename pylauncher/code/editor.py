#!/usr/bin/python3
#-*-code:UTF-8-*-
import os
from tkinter import *
from code.buttons import *
from code.windows import MainWindow, QuietPopuWindow, PopupWindow, showinfo
from code.dialogs import FileDlg
from code.scrolledlist import ScrolledList
from code.launcherexcept import *

path = os.getcwd()
path = os.path.join(path, 'config.txt')
CONFIG = path

def getLabels():
	labels = dict()
	klist = list()
	if not os.path.exists(CONFIG):
		return labels, klist
	lines = open(CONFIG, encoding='utf-8').readlines()
	for line in lines:
		line = line.strip()
		if not line:
			continue
		fname, fpath = line.split('=')
		fname = fname.rstrip()
		fpath = fpath.lstrip()
		labels[fname] = fpath
		klist.append(fname)
	return labels, klist

@EditorWrapper
def addProgram(root, dicts):
	labels = [('新程序名称',None,None),
			  ('新程序路径','浏览文件...',OpenFile)]
	fdlg = FileDlg(labels,root,dicts)
	return fdlg

def editProgram():
	dicts,labels = getLabels()
	root = PopupWindow('editor')
	fdlg = addProgram(root, dicts)
	btnroot = Frame(root)
	btnroot.pack(side=RIGHT)
	slist = ScrolledList(labels,root)
	slist.listbox.selection_set(0)
	CustomBtn('Add', lambda: addNewFile(slist, fdlg,dicts) ,btnroot)
	CustomBtn('Up', lambda: moveUpline(slist) ,btnroot)
	CustomBtn('Down', lambda:moveDownline(slist) ,btnroot)
	CustomBtn('Del', lambda:deline(slist, dicts) ,btnroot)
	CustomBtn('SaveAll', lambda:saveAll(slist,dicts) ,btnroot)

@EditorWrapper
def addNewFile(slist, fdlg, dicts):
	fname, fpath = fdlg.onSubmit()
	slist.listbox.insert(END, fname)
	dicts[fname] = fpath

@EditorWrapper
def chkSelected(slist):
	index = slist.listbox.curselection()
	if not index:
		raise SelectedNoneExcept()
	return index[0]

@EditorWrapper
def moveUpline(slist):
	index = chkSelected(slist) 
	if index == 0:
		raise TouchHeadExcept()

	tmp = slist.listbox.get(index-1)
	tmp2 = slist.listbox.get(index)

	slist.listbox.delete(index-1)
	slist.listbox.insert(index-1, tmp2)
	slist.listbox.delete(index)
	slist.listbox.insert(index, tmp)
	slist.listbox.selection_set(index-1)

@EditorWrapper
def moveDownline(slist):
	index = chkSelected(slist)
	length = slist.listbox.size()
	if index == length-1:
		raise ReachTailExcept()

	tmp = slist.listbox.get(index+1)
	tmp2 = slist.listbox.get(index)

	slist.listbox.delete(index+1)
	slist.listbox.insert(index+1, tmp2)
	slist.listbox.delete(index)
	slist.listbox.insert(index, tmp)
	slist.listbox.selection_set(index+1)

def deline(slist, dicts):
	index = chkSelected(slist) 
	length = slist.listbox.size()
	key = slist.listbox.get(index)
	for i in range(index, length-1):
		nextlabel = slist.listbox.get(i+1)
		slist.listbox.delete(i)
		slist.listbox.insert(i, nextlabel)
	slist.listbox.delete(length-1,last=None)
	del dicts[key]

@EditorWrapper
def saveAll(slist,dicts):
	if os.path.exists(CONFIG):
		os.remove(CONFIG)
	fs = open(CONFIG,'w', encoding='utf-8')
	for index in range(slist.listbox.size()):
		label = slist.listbox.get(index)
		fs.write(label+'='+dicts[label]+'\n')
	fs.close()
	raise SaveFileExcept()
	

def makeEntries(root):
	if not os.path.exists(CONFIG):
		return False
	lines = open(CONFIG, encoding='utf-8').readlines()
	for line in lines:
		line = line.lstrip().rstrip()
		if not line:
			continue
		fname, fpath = line.split('=')
		fname = fname.rstrip()
		fpath = fpath.lstrip()
		AddEntry(fname, fname, fpath, root)