import io
import unittest

from arch import Register, Opcode
from compiler import Instruction
import compiler

SAMPLE_TIS_1 = """L: MOV NIL ACC
ADD 1
JMP L"""


class TestCompiler(unittest.TestCase):

    def testCompile(self):
        prog = compiler.compile(io.StringIO(SAMPLE_TIS_1))
        for i in prog:
            print(i)
        self.assertEqual(prog[0], Instruction(Opcode.MOV_REG_REG, src=Register.NIL, dst=Register.ACC, label="L"))
        self.assertEqual(prog[1], Instruction(Opcode.ADD_LIT, src = 1))
        # Compiler should have translated the label to direct to instruction 0
        self.assertEqual(prog[2], Instruction(Opcode.JMP, dst = 0))

    def testDecode(self):
        self.assertEqual(Instruction(
            Opcode.NOP), compiler._decode(""))

        # Labels.
        self.assertEqual(Instruction(Opcode.NOP, label="BLAH"),
                         compiler._decode('BLAH:'))
        self.assertEqual(Instruction(Opcode.SWP, label="D"),
                         compiler._decode('D: SWP'))

        # No-argument ops.
        for op in ['NOP', 'SWP', 'SAV', 'NEG']:
            self.assertEqual(Instruction(
                Opcode[op]), compiler._decode(op))
        # Add/Subtract register and literal.
        self.assertEqual(Instruction(Opcode.ADD_LIT, src=123),
                         compiler._decode('ADD 123'))
        self.assertEqual(Instruction(Opcode.ADD_LIT, src=-567),
                         compiler._decode('ADD -567'))
        self.assertEqual(Instruction(Opcode.ADD_REG, src=Register.NIL),
                         compiler._decode('ADD NIL'))
        self.assertEqual(Instruction(Opcode.SUB_LIT, src=123),
                         compiler._decode('SUB 123'))
        self.assertEqual(Instruction(Opcode.SUB_LIT, src=-567),
                         compiler._decode('SUB -567'))
        self.assertEqual(Instruction(Opcode.SUB_REG, src=Register.NIL),
                         compiler._decode('SUB NIL'))

        # Assignment for literals and registers.
        self.assertEqual(Instruction(Opcode.MOV_LIT_REG, src=123, dst=Register.ACC),
                         compiler._decode('MOV 123 ACC'))
        self.assertEqual(Instruction(Opcode.MOV_LIT_REG, src=-567, dst=Register.ACC),
                        compiler._decode('MOV -567 ACC'))
        self.assertEqual(Instruction(Opcode.MOV_REG_REG, src=Register.NIL,
                                     dst=Register.ACC),
                         compiler._decode('MOV NIL ACC'))
