import Tkinter
class DDList(Tkinter.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, **kw):
        kw['selectmode'] = Tkinter.SINGLE
        Tkinter.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None
    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)
    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

if __name__ == '__main__':
	tk = Tkinter.Tk()
	length = 10
	dd = DDList(tk, height=length)
	dd.pack()
	for i in xrange(length):
		dd.insert(Tkinter.END, str(i))

def show():
	for x in dd.get(0, Tkinter.END):
		print x

print
tk.after(2000, show)
tk.after(2000, show)
tk.mainloop( )