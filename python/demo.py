import io

import compiler
import core

SAMPLE_TIS_1 = """MOV NIL ACC
L: ADD 1
JMP L"""

instructions = compiler.compile(io.StringIO(SAMPLE_TIS_1))
for i in instructions:
    print(i)

core = core.ExecCore(instructions)
print(instructions)
core.dump(verbose=True)
for i in range(0, 20):
    print(f'step: {i}')
    core.step()
