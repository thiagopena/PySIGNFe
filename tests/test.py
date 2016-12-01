import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pysignfe.nf_e import nf_e

class NfeTests(unittest.TestCase):
    def test_nfe_instantiation(self):
        new_nfe = nf_e()
        self.assertIsNotNone(new_nfe)
        

if __name__=='__main__':
    unittest.main()