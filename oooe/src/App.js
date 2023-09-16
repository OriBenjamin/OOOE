import React from "react";
import { useState } from "react";
import "./App.css";
import "./Form.js";
import Form from "./Form.js";
import Table from "./Table.js";
import { CycleButton } from "./CycleButton";


function App() {

  const [tables, setTables] = useState({
    RAT: [null,null,null,null,null],
    ROB: [[null,null],[null,null],[null,null],[null,null],[null,null]],
    ROB_CONT: [null,null,null,null,null],
    REGS: [0,1,2,3,4],
  });
 function updateTables(newTables) {
   setTables(newTables);
  }
  return (
    <div className="form-container">
      <h1>OOOE Simulator</h1>
      <Form onClick={updateTables}/>
      <Table RAT={tables.RAT} ROB={tables.ROB} REGS={tables.REGS} ROB_CONT={tables.ROB_CONT}/>
      <CycleButton onClick={updateTables}/>
    </div>
  );
}

export default App;

