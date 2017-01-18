def eggsfunc(obj):
	return obj.value * 4

def hamfunc(obj, value):
	return value + 'ham'


def Extender(aClass):
	aClass.eggs = eggsfunc
	aClass.ham = hamfunc
	return aClass

@Extender
class Client1:
	def __init__(self, value):
		self.value = value

	def spam(self):
		return self.value * 2

@Extender
class Client2:
	value = 'ni?'

X = Client1('Ni!')
print(X.spam())
print(X.eggs())
print(X.ham('bacon'))

Y = Client2()
print(Y.eggs())
print(Y.ham('bacon'))

