from datetime import datetime, timedelta

from flask import Flask, request, jsonify, session
from typing import Optional
import uuid
import tables
from tables import Instruction, Opcode, Operand
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.config['PROPAGATE_EXCEPTIONS'] = False
app.secret_key = "your_secret_key_here"

sessions = {}


def jsonRob(session_tables):
    jsonROB = []
    for i in session_tables.ROB:
        if i[0] is None:
            jsonROB.append((None, i[1]))
        else:
            jsonROB.append((i[0].__dict__, i[1]))
    return jsonROB


def jsonRobCont(session_tables):
    jsonROB_CONT = []
    for i in session_tables.ROB_CONT:
        jsonROB_CONT.append([i[0].name, i[1], getattr(i[2], '__dict__', None), i[3], getattr(i[4], '__dict__', None),
                             getattr(i[5], '__dict__', None), i[0].cycles])
    return jsonROB_CONT


def stringToOperand(string):
    if string[0] == 'R':
        return Operand(int(string[1:]), True, False)
    elif string[0] == 'P':
        return Operand(int(string[1:]), True, True)
    else:
        return Operand(int(string), False, False)


@app.route('/start-session', methods=['POST'])
@cross_origin()
def start_session():
    session_id = str(uuid.uuid4())
    starting_registers = None
    if request.json['starting_registers'] is not None:
        starting_registers = request.json['starting_registers']
    costs = None
    if request.json['costs'] is not None:
        costs = request.json['costs']
    sessions[session_id] = {'tables': tables.Tables(starting_registers, costs),
                            'expiration': datetime.now() + timedelta(hours=1)}  # create new tables for this session
    return jsonify(session_id=session_id)


@app.route('/end-session', methods=['POST'])
@cross_origin()
def end_session():
    if request.json['session_id'] not in sessions:
        return jsonify(error='Session not started')
    del sessions[request.json['session_id']]
    return jsonify(success=True)


def check_session(session_id: str) -> Optional[jsonify]:
    if session_id not in sessions:
        return jsonify(error='Session not started')
    if datetime.now() > sessions[session_id]['expiration']:
        del sessions[session_id]
        return jsonify(error='Session expired')
    return None


@app.route('/fetch', methods=['POST'])
@cross_origin()
# if error return 500 and error message
def fetch_instruction():
    result = check_session(request.json['session_id'])
    if result is not None:
        return result
    session_tables = sessions[request.json['session_id']]['tables']
    # get the new instruction from the request body
    fetched_instruction = request.json
    instruction = Instruction(fetched_instruction['opcode'],
                              (stringToOperand(fetched_instruction['operands'][0]),
                               stringToOperand(fetched_instruction['operands'][1]),
                               stringToOperand(fetched_instruction['operands'][2])))
    session_tables.process(instruction)
    # Implement your logic to fetch a new instruction
    # Return the current tables along with the fetched instruction (if any)
    # Example response structure:
    # make ROB json serializable

    response = {
        'tables': {
            'RAT': session_tables.RAT,
            'ROB': jsonRob(session_tables),
            'ROB_CONT': jsonRobCont(session_tables),
            'REGS': session_tables.REGS,
        },
    }
    return jsonify(response)


@app.route('/cycle', methods=['POST'])
def run_cycle():
    result = check_session(request.json['session_id'])
    if result is not None:
        return result
    session_tables = sessions[request.json['session_id']]['tables']

    # Implement your logic to run a cycle
    session_tables.cycle()
    # Return the new tables after running the cycle
    response = {
        'tables': {
            'RAT': session_tables.RAT,
            'ROB': jsonRob(session_tables),
            'ROB_CONT': jsonRobCont(session_tables),
            'REGS': session_tables.REGS,
        },
    }
    return jsonify(response)


@app.route('/reset', methods=['POST'])
def reset():
    result = check_session(request.json['session_id'])
    if result is not None:
        return result
    session_tables = sessions[request.json['session_id']]['tables']

    session_tables.reset()
    response = {
        'tables': {
            'RAT': session_tables.RAT,
            'ROB': jsonRob(session_tables),
            'ROB_CONT': jsonRobCont(session_tables),
            'REGS': session_tables.REGS,
        },
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
