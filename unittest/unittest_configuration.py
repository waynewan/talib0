import unittest
from jackutil.configuration import configuration

basespec = {
	"a" : 1,
	"b" : 2,
	"x" : { "c" : 3, "d" : 4 }
}

class unittest_configuration(unittest.TestCase):
	def test_simple_variations(self):
		delta = { "a" : range(3, 20, 3) }
		c = configuration(basespec=basespec,variations=delta)
		for ii in c:
		
