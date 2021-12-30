from arch import Register, Opcode

class ParseException(Exception):
    pass

class Instruction:
    def __init__(self, op, label=None, src=None, dst=None):
        self._op = op
        self._src = None
        self._dst = None
        self._label = None
        if src is not None:
            self._src = src
        if dst is not None:
            self._dst = dst
        if label is not None:
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
        out = ""
        if self._label is not None:
            out += self._label + ": "
        out += self._op.name
        if self._src is not None:
            if type(self._src) == int:
                out += " %d" % self._src
            else:
                out += " " + self._src.name
        if self._dst is not None:
            if type(self._dst) == int:
                out += " %d" % self._dst
            # Internal to the compiler, we can store strings containing a jump label.
            elif type(self._dst) == str:
                out += " " + self._dst
            else:
                out += "->" + self._dst.name
        return out


def compile(fileio):
    """Compiles a TIS-100 program, converting from assembly code object code.
    """
    # First pass, we parse and translate, and collect the location of
    # labels.
    labels = {}
    pass1 = []
    for (number, line) in enumerate(fileio.readlines()):
        instruction = _decode(line)
        if instruction._label:
            labels[instruction._label] = number
        pass1.append(instruction)
    # Second pass, we substitute any destination labels with literals.
    # TODO(adam): Do we want to carry symbol information?
    output = []
    for i in pass1:
        # Jump-to-label instructions get remapped to their destination.
        # TODO(adam): Implement position-indepdendent code.
        if i._op in [Opcode.JMP, Opcode.JEZ, Opcode.JNZ, Opcode.JGZ, Opcode.JLZ]:
            output.append(Instruction(i._op, dst=labels[i._dst]))
        else:
            output.append(i)
    return output



def _decode(line):
    """Decodes a single line of a TIS-100 assembly program."""
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
        # isnumeric doesn't work with negative numbers.
        if parts[1].lstrip('-').isnumeric():
            return Instruction(Opcode.MOV_LIT_REG, label=label, src=int(parts[1]),  dst=Register[parts[2]])
        return Instruction(Opcode.MOV_REG_REG, label=label, src=Register[parts[1]], dst=Register[parts[2]])
    if parts[0] in ['ADD', 'SUB']:
        # isnumeric doesn't work with negative numbers.
        if parts[1].lstrip('-').isnumeric():
            return Instruction(Opcode[parts[0] + '_LIT'], label=label, src=int(parts[1]))
        return Instruction(Opcode(Opcode[parts[0] + '_REG']), label=label, src=Register[parts[1]])

     # These jumps are all to a destination.  The VM cares what operator it is, we don't.
    if parts[0] in ['JMP', 'JEZ', 'JNZ', 'JGZ', 'JLZ']:
        return Instruction(Opcode[parts[0]], dst = parts[1])

    #  TODO(ahaberlach): JRO
    raise ParseException(f'Could not parse line: {line}')