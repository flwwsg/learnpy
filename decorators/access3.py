'''return original class'''

traceMe = False
def trace(*args):
	if traceMe:
		print('['+' '.join(map(str, args)) + ']')

def accessControl(failIf):
	def onDecorator(aClass):
		def getattributes(self, attr):
			trace('get:', attr)
			if failIf(attr):
				raise TypeError('private attribute fetch: '+attr)
			else:
				return object.__getattribute__(self, attr)

		def setattributes(self, attr, value):
			trace('set:', attr)
			if failIf(attr):
				raise TypeError('private attribute change: '+attr)
			else:
				return object.__setattr__(self, attr, value)

		aClass.__getattribute__ = getattributes
		aClass.__setattr__ = setattributes
		return aClass			
	return onDecorator

def Private(*attributes):
	return accessControl(failIf=(lambda attr: attr in attributes))

def Public(*attributes):
	return accessControl(failIf=(lambda attr: attr in attributes))

if __name__ == '__main__':
	@Private('age')
	class Person:             #Person = Private(..)(Person)
		def __init__(self):
			# self.name = name
			self.age = 42

		def __str__(self):
			return 'Person: '+str(self.age)

		def __add__(self, yrs):
			self.age += yrs

	X = Person()
	# print(X.age)
	print(X)
	X+10
	print(X)
