def rangetest(*argchecks):
	def onDecorator(func):
		if not __debug__:
			return func
		else:
			def onCall(*args):
				for (ix, low, high) in argchecks:
					if args[ix] < low or args[ix] > high:
						errmsg = 'Argument %s not in %s .. %s' % (ix, low, high)
						raise TypeError(errmsg)
				return func(*args)
			return onCall
	return onDecorator

