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


# opcodes
ADD = 0x00
SUB = 0x01
MUL = 0x02
DIV = 0x03

# tables

# RAT: architectonic register to physical register and value
RAT = [None] * 5
REGS = range(5)
# ROB: physical register to architectonic register and data
ROB = [(None, None)] * 5

# ROB_CONT: (op, src1_ready, src1, src2_ready, src2, dest)
ROB_CONT = []

last_physical_register = Operand(0, True, True)


class Instruction:
    def __init__(self, opcode, operands: tuple[Operand, Operand, Operand]):
        self.opcode = opcode
        self.operands = operands

    def __str__(self):
        return f"Instruction(opcode={self.opcode}, operands={self.operands})"


def process(instruction: Instruction):
    global last_physical_register
    ROB[last_physical_register.value] = (instruction.operands[0].value, None)
    ROB_CONT.append([instruction.opcode, False, instruction.operands[1], False, instruction.operands[2], last_physical_register])
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
        'Dest': [f"R{reg[0]}" if (reg[0] is not None) else "" for reg in ROB],
        'Data v': [(reg[1] is not None) for reg in ROB],
        'Data': [reg[1] for reg in ROB]
    }
    print("ROB:")
    print(tabulate(rob_table, headers='keys', tablefmt='psql'))
    rob_cont_table = ROB_CONT
    print("ROB_CONT:")
    print(tabulate(rob_cont_table, headers=['Op', 'src1_ready', 'src1', 'rc2_ready', 'src2', 'dest'], tablefmt='psql'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_tables()
    process(Instruction(DIV, (Operand(2), Operand(4), Operand(3))))
    process(Instruction(MUL, (Operand(3), Operand(50, False), Operand(4))))
    process(Instruction(DIV, (Operand(1), Operand(2), Operand(3))))
    process(Instruction(ADD, (Operand(2), Operand(4), Operand(3))))
    process(Instruction(ADD, (Operand(3), Operand(2), Operand(3))))
    print_tables()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
