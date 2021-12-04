import io
import unittest

from core import ExecCore

SAMPLE1_CODE = """## sample1
MOV LEFT, ACC
ADD ACC
MOVE ACC, RIGHT"""

class TestCore(unittest.TestCase):

    def testLload(self):
        core = ExecCore()

        code = io.StringIO(SAMPLE1_CODE)
        core.load(code)
        self.assertEquals(core._title, "sample1")
