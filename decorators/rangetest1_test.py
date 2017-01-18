from rangetest1 import rangetest

print(__debug__)

@rangetest((1,0,120))
def persinfo(name, age):
	print('%s is %s years old' % (name, age))

@rangetest([0,1,12], [1,1,31],[2,0,2009])
def birthday(M,D,Y):
	print('birthday = {0}/{1}/{2} '.format(M, D, Y))

class Person:
	def __init__(self, name, job, pay):
		self.name = name
		self.job = job
		self.pay = pay
		
	@rangetest([1, 0.0, 1.0])
	def giveRaise(self, percent):
		self.pay = int(self.pay * (1+percent))

persinfo('Bob', 45)
# persinfo('Bob', 200)

birthday(5,31,1978)
# birthday(5, 32,1978)

sue = Person('Sue Jones', 'dev', 100000)
sue.giveRaise(.10)
print(sue.pay)
# sue.giveRaise(1.2)
# print(sue.pay)