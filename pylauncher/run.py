#!/usr/bin/python3
#-*-code:UTF-8-*-
from tkinter import *
from code.windows import MainWindow
from code.editor import *
from code.launcherexcept import LauncherExcept

Root = MainWindow('简易启动菜单')
makeEntries(Root)
EditProgram(parent=Root, command=editProgram)
Quitter(Root)

Root.mainloop()