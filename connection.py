from flask import Flask, request, jsonify
from typing import Optional

import tables
from tables import Instruction, Opcode, Operand

app = Flask(__name__)


def stringToOperand(string):
    if string[0] == 'R':
        return Operand(int(string[1:]), True, False)
    elif string[0] == 'P':
        return Operand(int(string[1:]), True, True)
    else:
        return Operand(int(string), False, False)


@app.route('/fetch-instruction', methods=['POST'])
def fetch_instruction():
    # get the new instruction from the request body
    fetched_instruction = request.json
    instruction = Instruction(Opcode(fetched_instruction['opcode']),
                              (stringToOperand(fetched_instruction['operands'][0]),
                               stringToOperand(fetched_instruction['operands'][1]),
                               stringToOperand(fetched_instruction['operands'][2])))
    tables.process(instruction)
    # Implement your logic to fetch a new instruction
    # Return the current tables along with the fetched instruction (if any)
    # Example response structure:
    response = {
        'tables': {
            'RAT': tables.RAT,
            'ROB': tables.ROB,
            'ROB_CONT': tables.ROB_CONT,
            'cycle': tables.cycle
        },
    }
    return jsonify(response)


@app.route('/run-cycle', methods=['POST'])
def run_cycle():
    # Implement your logic to run a cycle
    tables.cycle()
    # Return the new tables after running the cycle
    response = {
        'tables': {
            'RAT': tables.RAT,
            'ROB': tables.ROB,
            'ROB_CONT': tables.ROB_CONT,
        }
    }
    return jsonify(response)


@app.route('/reset', methods=['GET'])
def reset():
    tables.reset()
    response = {
        'tables': {
            'RAT': tables.RAT,
            'ROB': tables.ROB,
            'ROB_CONT': tables.ROB_CONT,
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
