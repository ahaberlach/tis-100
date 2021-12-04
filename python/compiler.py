from enum import Enum


class Register(Enum):
    ACC = 1  # Accumulator
    BAK = 2  # Backup register (not addressable)
    NIL = 3  # Zero register (always returns zero)
    #  Communications Registers
    LEFT = 4
    RIGHT = 5
    UP = 6
    DOWN = 7
    #  Reads/Writes to next ready communications register
    ANY = 8
    #  Reads/Writes to most recently successfully used register
    LAST = 9


class Opcode(Enum):
    # TODO(adam): Translate this to ADD NIL
    NOP = 1
    # Move a literal value to a register
    MOV_LIT_REG = 2
    # Move from one register to another
    MOV_REG_REG = 4
    # Swap between two registers
    SWP = 5
    # Save ACC to BAK
    SAV = 6
    # Add a literal the accumulator
    ADD_LIT = 7
    # Add the value from a register to the accumulator
    ADD_REG = 8
    # Subtract a literal from the accumulator
    SUB_LIT = 9
    # Subtract the value in a register from the accumulator
    SUB_REG = 10
    # Negate the accumulator
    NEG = 11
    # Jump to specified Label
    JMP = 13
    # Conditionally jump to specified label (if ACC is zero)
    JEZ = 14
    # Conditionally jump to specified label (if ACC is not zero)
    JNZ = 15
    # Conditionally jump to specified label (if ACC > 0)
    JGZ = 16
    # Conditionally jump to specified label (if ACC < 0)
    JLZ = 17
    # Transfer execution unconditionally: jump to absolute offset
    JRO_LIT = 18
    # Transfer execution unconditionally: jump to offset in register
    JRO_REG = 19


class Instruction:
    def __init__(self, op, label=None, src=None, dst=None):
        self._op = op
        self._src = None
        self._dst = None
        self._label = None
        if src:
            self._src = src
        if dst:
            self._dst = dst
        if label:
            self._label = label

    # For testing.
    def __eq__(self, other):
        if self._op != other._op:
            return False
        if self._src != other._src:
            return False
        if self._dst != other._dst:
            return False
        if self._label != other._label:
            return False
        return True

    def __repr__(self):
        if self._label:
            return f'{self._label} {self._op}'
        return f'{self._op}'


def _str_to_reg(str):
    return Register[str]


def compile(fileio):
    return [_decode(line) for line in fileio.readlines()]


def _decode(line):
    # Just sort this out now.
    line = line.upper()
    parts = line.split()

    # Handle labels by checking to see if the first (or only) item in the line ends in :
    # if so we save it for later, and just pass the rest of the line along.
    label = None
    if parts and parts[0][-1] == ':':
        label = parts[0][:-1]
        parts = parts[1:]
    if not parts:
        return Instruction(Opcode.NOP, label=label)
    # Take advantage of the fact that all no-argument opcode names match the enum.
    if len(parts) == 1:
        return Instruction(Opcode[parts[0]], label=label)
    if parts[0] == 'MOV':
        if parts[1].isnumeric():
            return Instruction(Opcode.MOV_LIT_REG, label=label, src=int(parts[1]),  dst=_str_to_reg(parts[2]))
        return Instruction(Opcode.MOV_REG_REG, label=label, src=_str_to_reg(parts[1]), dst=_str_to_reg(parts[2]))
    if parts[0] in ['ADD', 'SUB']:
        if parts[1].isnumeric():
            return Instruction(Opcode[parts[0] + '_LIT'], label=label, src=int(parts[1]))
        return Instruction(Opcode(Opcode[parts[0] + '_REG']), label=label, src=_str_to_reg(parts[1]))
