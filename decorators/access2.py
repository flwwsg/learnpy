traceMe = False
def trace(*args):
	if traceMe:
		print('['+' '.join(map(str, args)) + ']')

def accessControl(failIf):
	def onDecorator(aClass):
		class onInstance:
			def __init__(self, *args, **kargs):
				self.__wrapped = aClass(*args, **kargs)

			def __getattr__(self, attr):
				trace('get:', attr)
				if failIf(attr):
					raise TypeError('private attribute fetch: '+attr)
				else:
					return getattr(self.__wrapped, attr)

			def __setattr__(self, attr, value):
				trace('set:', attr, value )
				if attr == '_onInstance__wrapped':
					self.__dict__[attr] = value
				elif failIf(attr):
					raise TypeError('private attribute change: '+attr)
				else:
					setattr(self.__wrapped, attr, value)
		return onInstance
	return onDecorator

def Private(*attributes):
	return accessControl(failIf=(lambda attr: attr in attributes))

def Public(*attributes):
	return accessControl(failIf=(lambda attr: attr in attributes))

if __name__ == '__main__':
	@Private('age')
	class Person:
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
