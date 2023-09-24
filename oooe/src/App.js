import React from "react";
import { useState } from "react";
import "./App.css";
import "./Form.js";
import Form from "./Form.js";
import Table from "./Table.js";
import { CycleButton } from "./CycleButton";
import { ConfigureForm } from "./ConfigureForm";
import fetchData from "./fetch.js";

function App() {

  const [tables, setTables] = useState({
    RAT: [null,null,null,null,null],
    ROB: [[null,null],[null,null],[null,null],[null,null],[null,null]],
    ROB_CONT: [null,null,null,null,null],
    REGS: [0,1,2,3,4],
  });
  const [costs, setCosts] = useState({
    'ADD': 1,
    'SUB': 1,
    'MUL': 2,
    'DIV': 2,
  });
  const [fetchDataFunc, setFetchDataFunc] = useState(null);
 function updateTables(newTables) {
   setTables(newTables);
  }
  return (
    <div className="container">
    <div className="configure-container">
      <h1>Configure Processor</h1>
      <ConfigureForm regs={tables['REGS']} setRegs={(regs) => setTables({...tables, 'REGS': regs})}
      costs={costs} setCosts={(costs) => setCosts(costs)}
      />
    </div>
    <div className="arrow"
    onClick={() => {
      fetchData(tables['REGS'], costs).then((fetchData) => {
        if (fetchData === null) {
          console.log("Could not fetch data");
          return;
        }
        document.querySelector(".form-container").style.opacity = 1;
        document.querySelector(".configure-container").style.opacity = 0.5;
        document.querySelector(".configure-container").style.pointerEvents = "none";;
        document.querySelector(".form-container").style.pointerEvents = "auto";
        setFetchDataFunc(() => fetchData);
      });
    }}>
      <button></button>
      <button></button>
      <button></button>
    </div>
    <div className="form-container">
      <h1>OOOE Simulator</h1>
      <Form onClick={updateTables} fetchFunc={fetchDataFunc}/>
      <Table RAT={tables.RAT} ROB={tables.ROB} REGS={tables.REGS} ROB_CONT={tables.ROB_CONT}/>
      <CycleButton onClick={updateTables} fetchFunc={fetchDataFunc}/>
    </div>
    </div>
  );
}

export default App;
export { fetchData };
