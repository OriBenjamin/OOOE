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
    def __init__(self, name):
        self.name = name
        if self.name == 'ADD':
            self.cycles = 1
        elif self.name == 'SUB':
            self.cycles = 1
        elif self.name == 'MUL':
            self.cycles = 2
        elif self.name == 'DIV':
            self.cycles = 4
        else:
            raise Exception("Invalid opcode")

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


# TODO: move to a class
RAT = [None] * 5
REGS: list[float] = list(range(5))
ROB: list[tuple[Optional[Operand], Optional[float]]] = [(None, None)] * 5
ROB_start = 0
ROB_CONT = []
last_physical_register = Operand(0, True, True)


def reset():
    global RAT, REGS, ROB, ROB_start, ROB_CONT, last_physical_register
    RAT = [None] * 5
    REGS = list(range(5))
    ROB = [(None, None)] * 5
    ROB_start = 0
    ROB_CONT = []
    last_physical_register = Operand(0, True, True)


class Instruction:
    def __init__(self, opcode: Opcode, operands: tuple[Operand, Operand, Operand]):
        self.opcode = opcode
        self.operands = operands

    def __str__(self):
        return f"Instruction(opcode={self.opcode}, operands={self.operands})"


def process(instruction: Instruction):
    global last_physical_register
    ROB[last_physical_register.value] = (instruction.operands[0], None)
    ROB_CONT.append(
        [instruction.opcode, False, instruction.operands[1], False, instruction.operands[2], last_physical_register])
    if not instruction.operands[1].is_register:
        ROB_CONT[-1][1] = True
    else:
        if RAT[instruction.operands[1].value] is not None:
            ROB_CONT[-1][1] = False
            ROB_CONT[-1][2] = Operand(RAT[instruction.operands[1].value], True, True)
        else:
            ROB_CONT[-1][1] = True
            ROB_CONT[-1][2] = Operand(REGS[instruction.operands[1].value], False)
    if not instruction.operands[2].is_register:
        ROB_CONT[-1][3] = True
    else:
        if RAT[instruction.operands[2].value] is not None:
            ROB_CONT[-1][3] = False
            ROB_CONT[-1][4] = Operand(RAT[instruction.operands[2].value], True, True)
        else:
            ROB_CONT[-1][3] = True
            ROB_CONT[-1][4] = Operand(REGS[instruction.operands[2].value], False)
    RAT[instruction.operands[0].value] = last_physical_register.value
    last_physical_register = Operand(last_physical_register.value + 1, True, True)


def process_instructions(instructions):
    for instruction in instructions:
        process(instruction)


def cycle():
    global ROB_start
    while ROB_start < len(ROB) and ROB[ROB_start][0] is not None and ROB[ROB_start][1] is not None:
        REGS[ROB[ROB_start][0].value] = ROB[ROB_start][1]
        ROB[ROB_start] = (None, None)
        ROB_start += 1
    readyValues = []
    for inst in ROB_CONT:
        if inst[1] and inst[3]:
            inst[0].cycles -= 1
            if inst[0].cycles == 0:
                ROB[inst[5].value] = (ROB[inst[5].value][0], inst[0].compute(inst[2].value, inst[4].value))
                readyValues.append((inst[5], ROB[inst[5].value][1]))
                ROB_CONT.remove(inst)
    for readyValue in readyValues:
        for inst in ROB_CONT:
            if inst[2] == readyValue[0]:
                inst[1] = True
                inst[2] = Operand(readyValue[1], False)
            if inst[4] == readyValue[0]:
                inst[3] = True
                inst[4] = Operand(readyValue[1], False)


def print_tables():
    rat_table = {
        'Reg': [f"R{i}" for i in range(len(RAT))],
        'ROB/RRF': ["RRF" if (reg is None) else "ROB" for reg in RAT],
        'Phys': [f"P{reg}" if (reg is not None) else "" for reg in RAT],
        'Val': REGS
    }
    print("RAT:")
    print(tabulate(rat_table, headers='keys', tablefmt='psql'))
    rob_table = {
        '#': [f"P{i}" for i in range(len(ROB))],
        'Valid': [(reg[0] is not None) for reg in ROB],
        'Dest': [reg[0] if (reg[0] is not None) else "" for reg in ROB],
        'Data v': [(reg[1] is not None) for reg in ROB],
        'Data': [reg[1] for reg in ROB]
    }
    print("ROB:")
    print(tabulate(rob_table, headers='keys', tablefmt='psql'))
    rob_cont_table = ROB_CONT
    print("ROB_CONT:")
    print(tabulate(rob_cont_table, headers=['Op', 'src1_ready', 'src1', 'rc2_ready', 'src2', 'dest'],
                   tablefmt='psql'))


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     reset()
#     # print_tables()
#     process(Instruction(Opcode('DIV'), (Operand(2), Operand(4), Operand(3))))
#     process(Instruction(Opcode('MUL'), (Operand(3), Operand(50, False), Operand(4))))
#     process(Instruction(Opcode('DIV'), (Operand(1), Operand(2), Operand(3))))
#     process(Instruction(Opcode('ADD'), (Operand(2), Operand(4), Operand(3))))
#     process(Instruction(Opcode('ADD'), (Operand(3), Operand(2), Operand(3))))
#     print_tables()
#     cycle()
#     cycle()
#     cycle()
#     cycle()
#     cycle()
#     cycle()
#     cycle()
#     cycle()
#     print_tables()
