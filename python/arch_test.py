import unittest

import arch

class TestArch(unittest.TestCase):
    def testRegister(self):
        self.assertEqual(1, arch.Register.ACC.value)
        self.assertEqual("ACC", arch.Register.ACC.name)
