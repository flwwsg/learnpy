#!/usr/bin/python3
#-*-code:UTF-8-*-
import os
from tkinter import *
from code.buttons import *
from code.windows import MainWindow, QuietPopuWindow, PopupWindow, showinfo
from code.dialogs import FileDlg
from code.scrolledlist import ScrolledList

path = os.getcwd()
path = os.path.join(path, 'config.txt')
CONFIG = path

def getLabels():
	lines = open(CONFIG, encoding='utf-8').readlines()
	labels = dict()
	klist = list()
	for line in lines:
		line = line.lstrip().rstrip()
		if not line:
			continue
		fname, fpath = line.split('=')
		fname = fname.rstrip()
		fpath = fpath.lstrip()
		labels[fname] = fpath
		klist.append(fname)
	return labels, klist

def addProgram(root):
	labels = [('新程序名称',None,None),
			  ('新程序路径','浏览文件...',OpenFile)]
	fdlg = FileDlg(labels,root)
	return fdlg

def editProgram():
	dicts,labels = getLabels()
	root = PopupWindow('editor')
	fdlg = addProgram(root)
	btnroot = Frame(root)
	btnroot.pack(side=RIGHT)
	slist = ScrolledList(labels,root)
	CustomBtn('Add', lambda: addNewFile(slist, fdlg,dicts) ,btnroot)
	CustomBtn('Up', lambda: moveUpline(slist) ,btnroot)
	CustomBtn('Down', lambda:moveDownline(slist) ,btnroot)
	CustomBtn('Del', lambda:deline(slist) ,btnroot)
	CustomBtn('SaveAll', lambda:saveAll(slist,dicts) ,btnroot)

def addNewFile(slist, fdlg, dicts):
	fname, fpath = fdlg.onSubmit()
	if not fname or not fpath:
		showinfo('请输入新程序名称及路径','请输入新程序名称及路径')
		return False
	if not os.path.exists(fpath):
		showinfo('请输入正确路径','请输入正确路径')
		return False
	if fname in dicts.keys():
		showinfo('重复程序！','重复程序！')
		return False
	slist.listbox.insert(END, fname)
	dicts[fname] = fpath

def chkSelected(slist):
	index = slist.listbox.curselection()
	if not index:
		return -1
	return index[0]

def moveUpline(slist):
	index = chkSelected(slist) 
	if index == -1 or index == 0:
		return False
	tmp = slist.listbox.get(index-1)
	tmp2 = slist.listbox.get(index)

	slist.listbox.delete(index-1)
	slist.listbox.insert(index-1, tmp2)
	slist.listbox.delete(index)
	slist.listbox.insert(index, tmp)

def moveDownline(slist):
	index = chkSelected(slist)
	length = slist.listbox.size()
	if index == -1 or index == length-1:
		return False

	tmp = slist.listbox.get(index1)
	tmp2 = slist.listbox.get(index)

	slist.listbox.delete(index1)
	slist.listbox.insert(index1, tmp2)
	slist.listbox.delete(index)
	slist.listbox.insert(index, tmp)

def deline(slist):
	index = chkSelected(slist) 
	if index == -1:
		return False
	length = slist.listbox.size()
	for i in range(index, length-1):
		nextlabel = slist.listbox.get(i)
		slist.listbox.delete(i)
		slist.listbox.insert(i, nextlabel)
	slist.listbox.delete(length-1,last=None)

def saveAll(slist,dicts):
	os.remove(CONFIG)
	fs = open(CONFIG,'w', encoding='utf-8')
	for index in range(slist.listbox.size()):
		label = slist.listbox.get(index)
		fs.write(label+'='+dicts[label]+'\n')
	fs.close()
	showinfo('保存成功','保存成功')
	

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