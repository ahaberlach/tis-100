

class ExecCore:
    def __init__(self):
        self._instructions = []
        self._title = 'UNKNOWN'
        self._pc = 0
        self._acc = 0
        self._bak = 0

    def dump(self):
        print(f'PC: {self._pc}')
        print(f'ACC: {self._acc}')
        print(f'BAK: {self._bak}')
        print(f'code: {self._title}')
        for i in self._instructions:
            print(f'  {i}')

    def load(self, fileio):
        for l in fileio.read().splitlines():
            if (l[0:2] == '##'):
                self._title = l[2:].strip()            
            self._instructions.append(l)
        if len(self._instructions) > 15:
            print(f'WARNING: program too long.')

    def run(self):
        while True:
            instr = self._instructions[self._pc]
            print(f'Executing: {instr}')

            self._pc += 1
            if self._pc >= len(self._instructions):
                self._pc = 0