trace = True

def rangetest(**argchecks):
	def onDecorator(func):
		if not __debug__:
			return func
		else:
			code 		= func.__code__
			allargs 	= code.co_varnames[:code.co_argcount]
			funcname	= func.__name__

			def onCall(*pargs, **kargs):
				expected = list(allargs)
				positinals = expected[:len(pargs)]

				for (arname, (low, high)) in argchecks.items():
					if arname in kargs:
						if kargs[arname] < low or kargs[arname] > high:
							errmsg = '{0} argument "{1}" not in {2}..{3} '
							errmsg = errmsg.format(funcname, arname, low, high)
							raise TypeError(errmsg)

					elif arname in positinals:
						position = positinals.index(arname)
						if pargs[position] < low or pargs[position] > high:
							errmsg = '{0} argument "{1}" not in {2}..{3} '
							errmsg = errmsg.format(funcname, arname, low, high)
							raise TypeError(errmsg)
					else:
						if trace:
							print('Argument "{0}" defaulted'.format(arname))
				return func(*pargs, **kargs)
			return onCall
	return onDecorator
	

