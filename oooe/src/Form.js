import "./App.css";
import useStates from "./useStates.js";
// import { print_tables } from "./tables";
import fetchData from "./fetch.js";
// import Table from "./Table.js";
import InputRegister from "./InputRegister";
function Form(props) {
  const [instruction, updateInstruction] = useStates({
    inputRegister: "R1",
    operator: "ADD",
    inputRegister2: "R2",
    outputRegister: "R3",
    specialCommand: 0,
    option: 1,
  });

  const [input_type, updateInputType] = useStates({
    input_1: "register",
    input_2: "register",
  });

  const handleEnterButton = async () => {
    if (instruction.option === 0) {
      // Handle special command logic
      console.log("Selected Special Command:", instruction.specialCommand);
    } else {
      const fetchDataFunc = await fetchData;
      if (fetchDataFunc === null) {
        console.log("Could not fetch data");
        return;
      }
      console.log(fetchDataFunc);
      const resultPromise = fetchDataFunc("/fetch", {
        opcode: instruction.operator,
        operands: [
          instruction.outputRegister,
          instruction.inputRegister,
          instruction.inputRegister2,
        ],
      });
      let result = await resultPromise;
      if (result === null) {
        console.log("Could not fetch data");
        return;
      }
      props.onClick(result.tables);
    }
  };
  return (
    <div className="form">
      <div className="buttons">
        <div id="input-options">
          <div
            id="regular-input"
            style={{ display: instruction.option === 0 ? "none" : "flex" }}
          >
            <select
              title="output-register"
              id="output-register"
              value={instruction.outputRegister}
              onChange={(e) =>
                updateInstruction({ outputRegister: e.target.value })
              }
            >
              <option value="R1">R1</option>
              <option value="R2">R2</option>
              <option value="R3">R3</option>
              <option value="R4">R4</option>
              <option value="R5">R5</option>
            </select>
            =
            <InputRegister
              value={instruction.inputRegister}
              style={{
                display: input_type.input_1 === "register" ? "inline" : "none",
              }}
              onChange={(value) => updateInstruction({ inputRegister: value })}
              inputType={input_type.input_1}
              onToggle={() =>
                updateInputType({
                  input_1:
                    input_type.input_1 === "register" ? "number" : "register",
                })
              }
            />
            <select
              title="operator"
              id="operator"
              value={instruction.operator}
              onChange={(e) => updateInstruction({ operator: e.target.value })}
            >
              <option value="ADD">+</option>
              <option value="SUB">-</option>
              <option value="MUL">*</option>
              <option value="DIV">/</option>
            </select>
            <InputRegister
              value={instruction.inputRegister2}
              style={{
                display: input_type.input_2 === "register" ? "inline" : "none",
              }}
              onChange={(value) => updateInstruction({ inputRegister2: value })}
              inputType={input_type.input_2}
              onToggle={() =>
                updateInputType({
                  input_2:
                    input_type.input_2 === "register" ? "number" : "register",
                })
              }
            />
          </div>
          <div
            id="special-command"
            style={{ display: instruction.option === 0 ? "block" : "none" }}
          >
            <select
              title="special-command"
              id="special-commands"
              value={instruction.specialCommand}
              onChange={(e) =>
                updateInstruction({ specialCommand: e.target.value })
              }
            >
              <option value="0">Jmp %RIP</option>
              <option value="1">Jmp %RSP</option>
            </select>
          </div>
        </div>
        <input
          className="button"
          type="submit"
          value="Fetch"
          onClick={handleEnterButton}
        />
      </div>
      <button
        className="bt-special-commands"
        id="toggle-options"
        onClick={() =>
          updateInstruction({ option: 1 - Number(instruction.option) })
        }
      >
        {instruction.option === 0 ? "Regular Input" : "Special Commands"}
      </button>
    </div>
  );
}

export default Form;
