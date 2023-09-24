import React, { useState } from 'react';
import './App.css'
import './ConfigureForm.css'
function ConfigureForm(props) {
    // a table of registers to fill the cycles of
    const handleEnterButton = () => {
        // fetchData(registers, null).then((fetchData) => {
        //     if (fetchData === null) {
        //         console.log("Could not fetch data");
        //         return;
        //     }
        //     console.log(fetchData);
        //     props.onClick(fetchData.tables);
        // });
    }

    const setRegister = (index, value) => {
        let newRegs = [...props.regs];
        newRegs[index] = value;
        props.setRegs(newRegs);
    }

    const setCost = (op, value) => {
        let newCosts = {...props.costs};
        newCosts[op] = value;
        props.setCosts(newCosts);
    }

    return (
        <div className='configure-div'>
        <div className='costs-div'>
        <div>
            ADD
            <input type="number" value={props.costs['ADD']} onChange={(e) => setCost('ADD', parseInt(e.target.value) || '')} />
        </div>
        <div>
            SUB
            <input type="number" value={props.costs['SUB']} onChange={(e) => setCost('SUB', parseInt(e.target.value) || '')} />
        </div>
        <div>
            MUL
            <input type="number" value={props.costs['MUL']} onChange={(e) => setCost('MUL', parseInt(e.target.value) || '')} />
        </div>
        <div>
            DIV
            <input type="number" value={props.costs['DIV']} onChange={(e) => setCost('DIV', parseInt(e.target.value) || '')} />
        </div>
        </div>
        <div className='registers-div'>
        <div> 
            R0
            <input type="number" value={props.regs[0]} onChange={(e) => setRegister(0, parseInt(e.target.value) || '')} />
        </div>
        <div>
            R1
            <input type="number" value={props.regs[1]} onChange={(e) => setRegister(1, parseInt(e.target.value) || '')} />
        </div>
        <div>
            R2
            <input type="number" value={props.regs[2]} onChange={(e) => setRegister(2, parseInt(e.target.value) || '')} />
        </div>
        <div>
            R3
            <input type="number" value={props.regs[3]} onChange={(e) => setRegister(3, parseInt(e.target.value) || '')} />
        </div>
        <div>
            R4
            <input type="number" value={props.regs[4]} onChange={(e) => setRegister(4, parseInt(e.target.value) || '')} />
        </div>
        </div>
        </div>
    )
}

export { ConfigureForm };