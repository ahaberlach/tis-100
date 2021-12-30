
# This defines the basic architecture of the TIS-100 in terms of registers and
# opcodes.  Because they are intended to be used on a microcontroller running
# CircuitPython, the standard python enum class is unavailable.  The SimpleEnum
# is a bare-mininum implementation of what is needed to tie the assembler and
# python-based virtual machine together.

class SimpleEnumElement:
    def __init__(self, name, value):
        self._name = name
        self._value = value
    
    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value


class SimpleEnum:
    def __init__(self, values):
        self._values = { v: SimpleEnumElement(v, i + 1)
                         for (i, v) in enumerate(values) }

    def __getattr__(self, name):
        return self._values[name]

    def __getitem__(self, name):
        return self._values[name]

Register = SimpleEnum(['ACC', 'BAK', 'NIL',
                       'LEFT', 'RIGHT', 'UP', 'DOWN',
                       'ANY', 'LAST'])

Opcode = SimpleEnum(['NOP',
                     'MOV_LIT_REG', 'MOV_REG_REG',
                     'SWP',
                     'SAV',
                     'ADD_LIT', 'ADD_REG',
                     'SUB_LIT', 'SUB_REG',
                     'NEG',
                     'JMP', 'JEZ', 'JNZ', 'JGZ', 'JLZ', 'JRO_LIT', 'JRO_REG'])

# class Opcode(Enum):
#     # TODO(adam): Translate this to ADD NIL
#     NOP = 1
#     # Move a literal value to a register
#     MOV_LIT_REG = 2
#     # Move from one register to another
#     MOV_REG_REG = 4
#     # Swap between two registers
#     SWP = 5
#     # Save ACC to BAK
#     SAV = 6
#     # Add a literal the accumulator
#     ADD_LIT = 7
#     # Add the value from a register to the accumulator
#     ADD_REG = 8
#     # Subtract a literal from the accumulator
#     SUB_LIT = 9
#     # Subtract the value in a register from the accumulator
#     SUB_REG = 10
#     # Negate the accumulator
#     NEG = 11
#     # Jump to specified Label
#     JMP = 13
#     # Conditionally jump to specified label (if ACC is zero)
#     JEZ = 14
#     # Conditionally jump to specified label (if ACC is not zero)
#     JNZ = 15
#     # Conditionally jump to specified label (if ACC > 0)
#     JGZ = 16
#     # Conditionally jump to specified label (if ACC < 0)
#     JLZ = 17
#     # Transfer execution unconditionally: jump to absolute offset
#     JRO_LIT = 18
#     # Transfer execution unconditionally: jump to offset in register
#     JRO_REG = 19