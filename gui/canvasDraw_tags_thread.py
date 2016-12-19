'''canvasDraw_tags_thread.py'''
from tkinter import *
import canvasDraw_tags
import _thread, time

class CanvasEventsDemo(canvasDraw_tags.CanvasEventsDemo):
	def moveEm(self, tag, moremoves):
		for i in range(5):
			for (diffx, diffy) in [(+20, 0), (0, +20), (-20,0), (0,-20)]:
				self.canvas.move(tag, diffx, diffy)
				time.sleep(.25)

	def moveInSquares(self, tag):
		_thread.start_new_thread(self.moveEm, (tag,))

if __name__ == '__main__':
	CanvasEventsDemo()
	mainloop()