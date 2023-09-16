import React from "react";

function InputRegister({ label, value, style, onChange, inputType, onToggle }) {
  return (
    <div style={{ display: "inline-block", position: "relative" }}>
      <label>{label}</label>
      {inputType === "register" ? (
        <select
          value={value}
          style={style}
          onChange={(e) => onChange(e.target.value)}
        >
            <option value="R1">R1</option>
            <option value="R2">R2</option>
            <option value="R3">R3</option>
            <option value="R4">R4</option>
            <option value="R5">R5</option>
        </select>
      ) : (
        <input
          type="number"
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      )}
      <button className="input-register-switcher" onClick={onToggle}>
        {inputType === "register" ? "˅" : "^"}
      </button>
    </div>
  );
}

export default InputRegister;
