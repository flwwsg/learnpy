'''threadpower.py'''
import threading

class Power():
	"""docstring for Power"""
	def __init__(self, i):
		self.i = i

	def action(self):
		print(self.i ** 32)


obj = Power(2)
threading.Thread(target=obj.action).start()
