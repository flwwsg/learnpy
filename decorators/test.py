class Wrapper:
	def __init__(self, object):
		self.wrapped = object

	def __getattr__(self, attrname):
		print('Trace:', attrname)
		return getattr(self.wrapped, attrname)

if __name__ == '__main__':
	x = Wrapper([1,2,4])
	x.append(5)
	print(x.wrapped)
	# input('press any key')
	x = Wrapper(dict(a=1,b=2))
	print(list(x.keys()))