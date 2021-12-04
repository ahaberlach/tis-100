import io
import unittest

import compiler


class TestCompiler(unittest.TestCase):

    def testDecode(self):
        self.assertEqual(compiler.Instruction(
            compiler.Opcode.NOP), compiler._decode(""))

        # Labels.
        self.assertEqual(compiler.Instruction(compiler.Opcode.NOP, label="BLAH"),
        compiler._decode('BLAH:'))
        self.assertEqual(compiler.Instruction(compiler.Opcode.SWP, label="D"),
        compiler._decode('D: SWP'))        

        # No-argument ops.
        for op in ['NOP', 'SWP', 'SAV', 'NEG']:
            self.assertEqual(compiler.Instruction(
                compiler.Opcode[op]), compiler._decode(op))
        # Add/Subtract register and literal
        self.assertEqual(compiler.Instruction(compiler.Opcode.ADD_LIT, src=123),
                          compiler._decode('ADD 123'))
        self.assertEqual(compiler.Instruction(compiler.Opcode.ADD_REG, src=compiler.Register.NIL),
                          compiler._decode('ADD NIL'))
        self.assertEqual(compiler.Instruction(compiler.Opcode.SUB_LIT, src=123),
                          compiler._decode('SUB 123'))
        self.assertEqual(compiler.Instruction(compiler.Opcode.SUB_REG, src=compiler.Register.NIL),
                          compiler._decode('SUB NIL'))

        self.assertEqual(compiler.Instruction(compiler.Opcode.MOV_LIT_REG, src=123, dst=compiler.Register.ACC),
                          compiler._decode('MOV 123 ACC'))
        self.assertEqual(compiler.Instruction(compiler.Opcode.MOV_REG_REG, src=compiler.Register.NIL,
                                               dst=compiler.Register.ACC),
                          compiler._decode('MOV NIL ACC'))
