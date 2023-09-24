import React from "react";
import "./App.css";
export function CycleButton(props) {
  const handleCycleButton = async () => {
    const fetchDataFunc = props.fetchFunc;
    if (fetchDataFunc === null) {
      console.log("Could not fetch data");
      return;
    }
    const resultPromise = fetchDataFunc('/cycle', {});
    let result = await resultPromise;
    console.log(result);
    if (result === null) {
      console.log("Could not fetch data");
      return;
    }
    props.onClick(result.tables);
  };

  return (
    <div>
      <button className="button" onClick={handleCycleButton}>Cycle</button>
    </div>
  );
}
