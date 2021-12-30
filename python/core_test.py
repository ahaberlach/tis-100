import io
import unittest

import compiler
from core import ExecCore

class TestCore(unittest.TestCase):

    # Start counting upwards from 23 in order to test assignment of literals
    # to the accumulator and addition of literals to accumulator.
    INCREMENT = """MOV 23 ACC
    L: ADD 1
    JMP L"""

    def testIncrement(self):
        instructions = compiler.compile(io.StringIO(TestCore.INCREMENT))

        core = ExecCore(instructions)
        self.assertEqual(0, core.pc)
        self.assertEqual(0, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(23, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(24, core.acc)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(24, core.acc)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(25, core.acc)

    # Start counting downwards by 2s from 23.
    DECREMENT = """MOV 23 ACC
    L: SUB 2
    JMP L"""

    def testDecrement(self):
        instructions = compiler.compile(io.StringIO(TestCore.DECREMENT))

        core = ExecCore(instructions)
        self.assertEqual(0, core.pc)
        self.assertEqual(0, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(23, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(21, core.acc)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(21, core.acc)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(19, core.acc)

    NEGATE = """MOV 3 ACC
    NEG
    MOV -11 ACC
    NEG"""

    def testNegate(self):
        instructions = compiler.compile(io.StringIO(TestCore.NEGATE))

        core = ExecCore(instructions)
        self.assertEqual(0, core.pc)
        self.assertEqual(0, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(3, core.acc)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(-3, core.acc)

        core.step()
        self.assertEqual(3, core.pc)
        self.assertEqual(-11, core.acc)

        core.step()
        self.assertEqual(0, core.pc)
        self.assertEqual(11, core.acc)

    # Move a literal to an accumulator, swap it to bak, move another, and
    # save it.
    SWAP_SAVE = """MOV 6 ACC
    SWP
    MOV 9 ACC
    SAV"""

    def testSwap(self):
        instructions = compiler.compile(io.StringIO(TestCore.SWAP_SAVE))

        core = ExecCore(instructions)
        self.assertEqual(0, core.pc)
        self.assertEqual(0, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(1, core.pc)
        self.assertEqual(6, core.acc)
        self.assertEqual(0, core.bak)

        core.step()
        self.assertEqual(2, core.pc)
        self.assertEqual(0, core.acc)
        self.assertEqual(6, core.bak)

        core.step()
        self.assertEqual(3, core.pc)
        self.assertEqual(9, core.acc)
        self.assertEqual(6, core.bak)

        core.step()
        # Loops back to PC == 0
        self.assertEqual(0, core.pc)
        self.assertEqual(9, core.acc)
        self.assertEqual(9, core.bak)
        