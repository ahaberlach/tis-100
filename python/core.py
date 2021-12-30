from arch import Opcode
from arch import Register

class ExecCore:
    def __init__(self, instructions):
        self.instructions = instructions

        self.pc = 0
        self.acc = 0
        self.bak = 0

    def _fetch_reg_value(self, reg):
        if reg == Register.NIL:
            return 0
        if reg == Register.ACC:
            return self.acc
        if reg == Register.BAK:
            return self.bak
        raise Exception(f"Unknown register: {reg}")


    def _set_reg_value(self, reg, val):
        if reg == Register.NIL:
            pass
        elif reg == Register.ACC:
            self.acc = val
        elif reg == Register.BAK:
            self.bak = val
        else:
            raise Exception(f"Unknown register: {reg}")


    def dump(self, verbose=False):
        print(f'PC: {self.pc}')
        print(f'ACC: {self.acc}')
        print(f'BAK: {self.bak}')
        if verbose:
            for i in self.instructions:
                print(f'  {i}')

    def step(self):
        print(f'PC: {self.pc}')
        print(f'ACC: {self.acc}')
        instr = self.instructions[self.pc]
        # Default to moving one step forward, but Jump instructions may
        # override this.
        next_pc = self.pc + 1
        print(f'Executing: {instr}')

        if instr._op == Opcode.NOP:
            pass
        elif instr._op == Opcode.MOV_LIT_REG:
            self._set_reg_value(instr._dst, instr._src)
        elif instr._op == Opcode.MOV_REG_REG:
            val = self._fetch_reg_value(instr._src)
            self._set_reg_value(instr._dst, val)
        elif instr._op == Opcode.SWP:
            tmp = self._fetch_reg_value(Register.BAK)
            self._set_reg_value(Register.BAK, self._fetch_reg_value(Register.ACC))
            self._set_reg_value(Register.ACC, tmp)
        elif instr._op == Opcode.SAV:
            self._set_reg_value(Register.BAK, self._fetch_reg_value(Register.ACC))
        elif instr._op == Opcode.ADD_LIT:
            self.acc += instr._src
        elif instr._op == Opcode.ADD_REG:
            #  TODO(adam) Test this
            self.acc += self._get_reg_value(instr._src)
        elif instr._op == Opcode.SUB_LIT:
            self.acc -= instr._src
        elif instr._op == Opcode.SUB_REG:
            #  TODO(adam) Test this
            self.acc -= self._get_reg_value(instr._src)
        elif instr._op == Opcode.NEG:
            self.acc = -self.acc
        # Assembler should have rewritten the jump to label
        # into a literal, so these are the same.
        elif instr._op in [Opcode.JMP, Opcode.JRO_LIT]:
            next_pc = instr._dst
        elif instr._op == Opcode.JEZ:
            if self.acc == 0:
                next_pc = instr._dst
        elif instr._op == Opcode.JNZ:
            if self.acc != 0:
                next_pc = instr._dst
        elif instr._op == Opcode.JGZ:
            if self.acc > 0:
                next_pc = instr._dst
        elif instr._op == Opcode.JLZ:
            if self.acc < 0:
                next_pc = instr._dst
        elif instr._op == Opcode.JRO_REG:
            next_pc = self._get_reg_value(instr._src)
        else:
            raise Exception(f"Unhandled instruction: {instr}")
            
        self.pc = next_pc
        if self.pc >= len(self.instructions):
            self.pc = 0