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