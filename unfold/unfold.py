import numpy as np

#args:
#	detector is a function taking an energy range and a spectrum function
#	responses are the measured responses with given detector
#	bases are tuples of base functions.and their range
#ret:
#	it returns a coefficients for the base functions

def unfold(detector, responses, bases):
	return scipy.linalg.solve([detector(b) for b in bases], responses)
