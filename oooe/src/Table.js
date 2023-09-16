import React, { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
// import "./RatTables.css"; // Include your CSS file if needed
// import rat_table from "./tables.js";
import "./Table.css";
function RatTables(props) {
  const RAT = props.RAT;
  const ROB = props.ROB;
  const REGS = props.REGS;
  const ROB_CONT = props.ROB_CONT;
  const [canDrag, setCanDrag] = useState(false);
  function opToStr(operand) {
    if (operand == null) {
      return "";
    } else if (operand.is_register) {
      if (operand.is_physical) return "P" + operand.value;
      else return "R" + operand.value;
    } else {
      return operand.value;
    }
  }

  return (
    <div className="tables">
      <div style={{display: "inline-block"}}>
        <h2>RAT</h2>
        <table>
          <thead>
            <tr>
              <th>Reg</th>
              <th>ROB/RRF</th>
              <th>Physical</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
          <AnimatePresence>
            {RAT.map((reg, index) => (
                <motion.tr
                  key={[index,(RAT[index])]}
                  initial={{ backgroundColor: "#bcbcbc" }}
                  animate={{ backgroundColor: "#f9f9f9" }} 
                  layout
                  transition={{ duration: 10, layout: "ease" }}
                >
                  <td> {"R" + index} </td>
                  <td> {reg == null ? "RRF" : "ROB"} </td>
                  <td> {reg != null ? "P" + reg : ""} </td>
                  <td> {REGS[index]} </td>
                </motion.tr>
            ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>

      <div style={{display: "inline-block"}}>
        <h2>ROB</h2>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Valid</th>
              <th>Dest</th>
              <th>Data V</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
          <AnimatePresence>
            {ROB.map((reg, index) => (
              <motion.tr
              key={[index,(ROB[index])]}
              initial={{ backgroundColor: "#bcbcbc" }}
              animate={{ backgroundColor: "#f9f9f9" }} 
              layout
              transition={{ duration: 10, layout: "ease" }}
            >
                <td> {"P" + index} </td>
                <td> {+(reg[0] != null)} </td>
                <td> {opToStr(reg[0])} </td>
                <td> {+(reg[1] != null)} </td>
                <td> {reg[1] != null ? reg[1] : ""} </td>
              </motion.tr>
            ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>

      <div style={{ display: "inline-block" }}>
        <h2>ROB Cont</h2>
        <table>
          <thead>
            <tr>
              <th>Op</th>
              <th>Src1 r</th>
              <th>Src1</th>
              <th>Src2 r</th>
              <th>Src2</th>
              <th>Dest</th>
              <th>Cycles Left</th>
            </tr>
          </thead>
          <tbody>
          <AnimatePresence>
            {ROB_CONT.filter((item) => item != null).map((reg, index) => (
              <motion.tr
              key={[index,(ROB_CONT[index])]}
              initial={{ backgroundColor: "#bcbcbc" }}
              animate={{ backgroundColor: "#f9f9f9" }} 
              layout
              transition={{ duration: 10, layout: "ease" }}
            >
                <td> {ROB_CONT[index][0]} </td>
                <td> {+ROB_CONT[index][1]} </td>
                <td> {opToStr(ROB_CONT[index][2])} </td>
                <td> {+ROB_CONT[index][3]} </td>
                <td> {opToStr(ROB_CONT[index][4])} </td>
                <td> {opToStr(ROB_CONT[index][5])} </td>
                <td> {ROB_CONT[index][6]}</td>
              </motion.tr>
            ))}
            </AnimatePresence>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RatTables;
