#!/usr/bin/python3

from tkinter.messagebox import showinfo

class LauncherExcept(Exception):
	def __init__(self, title, info):
		self.title = title
		self.info = info

	def popinfo(self):
		showinfo(self.title, self.info)

class WrongFilePathExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '路径不存在', '请输入正确路径')
		
class EmptyFileExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '没有输入','请输入新程序名称及路径')

class DulptyFileExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '文件已存在','菜单已存在该程序')

class SaveFileExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '保存成功', '菜单保存成功')

class TouchHeadExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '不能再移', '已经在第一位')

class ReachTailExcept(LauncherExcept):
	def __init__(self):
		LauncherExcept.__init__(self, '不能再移', '已经在最后位')

		