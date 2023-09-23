from typing import Optional

from tabulate import tabulate


class Operand:
    def __init__(self, value, is_register=True, is_physical=False):
        self.value = value
        self.is_register = is_register
        self.is_physical = is_physical

    def __str__(self):
        if self.is_register:
            if self.is_physical:
                return f"P{self.value}"
            else:
                return f"R{self.value}"
        else:
            return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, Operand):
            return self.value == other.value and self.is_register == other.is_register and self.is_physical == other.is_physical
        else:
            return self.value == other


class Opcode:
    def __init__(self, name, cycles=0):
        self.name = name
        self.cycles = cycles

    def __str__(self):
        return self.name

    def compute(self, src1, src2):
        if self.name == 'ADD':
            return src1 + src2
        elif self.name == 'SUB':
            return src1 - src2
        elif self.name == 'MUL':
            return src1 * src2
        elif self.name == 'DIV':
            return src1 / src2


class Instruction:
    def __init__(self, opcode: str, operands: tuple[Operand, Operand, Operand], costs: dict[str, int] = None):
        if costs is None:
            costs = {
                'ADD': 1,
                'SUB': 1,
                'MUL': 2,
                'DIV': 4
            }
        self.opcode = Opcode(opcode, costs[opcode])
        self.operands = operands

    def __str__(self):
        return f"Instruction(opcode={self.opcode}, operands={self.operands})"


class Tables:
    def __init__(self, starting_registers: list[float] = None, costs: dict[str, int] = None):
        if starting_registers is None:
            starting_registers = list(range(5))
        if costs is None:
            costs = {
                'ADD': 1,
                'SUB': 1,
                'MUL': 2,
                'DIV': 4
            }
        self.RAT: list[float | None] = [None] * 5
        self.starting_registers = starting_registers
        self.REGS: list[float] = starting_registers
        self.costs = costs
        self.ROB: list[tuple[Optional[Operand], Optional[float]]] = [(None, None)] * 5
        self.ROB_start = 0
        self.ROB_CONT = []
        self.last_physical_register = Operand(0, True, True)

    def reset(self):
        self.RAT = [None] * 5
        self.REGS: list[float] = self.starting_registers
        self.ROB: list[tuple[Optional[Operand], Optional[float]]] = [(None, None)] * 5
        self.ROB_start = 0
        self.ROB_CONT = []
        self.last_physical_register = Operand(0, True, True)

    def process(self, instruction: Instruction):
        # TODO: fix changing RAT bug
        self.ROB[self.last_physical_register.value] = (instruction.operands[0], None)
        self.ROB_CONT.append(
            [instruction.opcode, False, instruction.operands[1], False, instruction.operands[2],
             self.last_physical_register])
        new_row = self.ROB_CONT[-1]
        if not instruction.operands[1].is_register:
            new_row[1] = True
        else:
            if self.RAT[instruction.operands[1].value] is not None:
                new_row[1] = False
                new_row[2] = Operand(self.RAT[instruction.operands[1].value], True, True)
            else:
                new_row[1] = True
                # Change ready register to number
                new_row[2] = Operand(self.REGS[instruction.operands[1].value], False)
        if not instruction.operands[2].is_register:
            new_row[3] = True
        else:
            if self.RAT[instruction.operands[2].value] is not None:
                new_row[3] = False
                new_row[4] = Operand(self.RAT[instruction.operands[2].value], True, True)
            else:
                new_row[3] = True
                new_row[4] = Operand(self.REGS[instruction.operands[2].value], False)
        # self.last_physical_register.value = self.REGS[instruction.operands[0].value]
        self.RAT[instruction.operands[0].value] = self.last_physical_register.value
        self.last_physical_register = Operand(self.last_physical_register.value + 1, True, True)

    def cycle(self):
        while self.ROB_start < len(self.ROB) and self.ROB[self.ROB_start][0] is not None and self.ROB[self.ROB_start][1] is not None:
            self.REGS[self.ROB[self.ROB_start][0].value] = self.ROB[self.ROB_start][1]
            if self.ROB_start == self.RAT[self.ROB[self.ROB_start][0].value]:
                self.RAT[self.ROB[self.ROB_start][0].value] = None
            self.ROB[self.ROB_start] = (None, None)
            self.ROB_start += 1
        readyValues = []
        for inst in self.ROB_CONT:
            if inst[1] and inst[3]:
                inst[0].cycles -= 1
                if inst[0].cycles == 0:
                    self.ROB[inst[5].value] = (
                        self.ROB[inst[5].value][0], inst[0].compute(inst[2].value, inst[4].value))
                    readyValues.append((inst[5], self.ROB[inst[5].value][1]))
                    self.ROB_CONT.remove(inst)
        for readyValue in readyValues:
            for inst in self.ROB_CONT:
                if inst[2] == readyValue[0]:
                    inst[1] = True
                    inst[2] = Operand(readyValue[1], False)
                if inst[4] == readyValue[0]:
                    inst[3] = True
                    inst[4] = Operand(readyValue[1], False)


def print_tables(tables: Tables):
    rat_table = {
        'Reg': [f"R{i}" for i in range(len(tables.RAT))],
        'ROB/RRF': ["RRF" if (reg is None) else "ROB" for reg in tables.RAT],
        'Phys': [f"P{reg}" if (reg is not None) else "" for reg in tables.RAT],
        # show the physical register value if it exists, otherwise show the logical register value
        # 'val': [f"{reg}" if (reg is not None) else f"{tables.REGS[i]}" for i, reg in enumerate(tables.RAT)],
        'val': [f"{reg}" if (reg is not None) else "" for reg in tables.REGS],
    }
    print("RAT:")
    print(tabulate(rat_table, headers='keys', tablefmt='psql'))
    rob_table = {
        '#': [f"P{i}" for i in range(len(tables.ROB))],
        'Valid': [(reg[0] is not None) for reg in tables.ROB],
        'Dest': [reg[0] if (reg[0] is not None) else "" for reg in tables.ROB],
        'Data v': [(reg[1] is not None) for reg in tables.ROB],
        'Data': [reg[1] for reg in tables.ROB]
    }
    print("ROB:")
    print(tabulate(rob_table, headers='keys', tablefmt='psql'))
    rob_cont_table = tables.ROB_CONT
    print("ROB_CONT:")
    print(tabulate(rob_cont_table, headers=['Op', 'src1_ready', 'src1', 'rc2_ready', 'src2', 'dest'],
                   tablefmt='psql'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    table = Tables()
    table.reset()
    # print_tables()
    table.process(Instruction('DIV', (Operand(2), Operand(4), Operand(3))))
    table.process(Instruction('MUL', (Operand(3), Operand(50, False), Operand(4))))
    table.process(Instruction('DIV', (Operand(1), Operand(2), Operand(3))))
    table.process(Instruction('ADD', (Operand(2), Operand(4), Operand(3))))
    table.process(Instruction('ADD', (Operand(3), Operand(2), Operand(3))))
    print_tables(table)
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    table.cycle()
    print_tables(table)
