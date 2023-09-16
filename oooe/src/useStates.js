
import { useState } from 'react';

const useStates = (initialState) => {
  const [state, setState] = useState(initialState);
  const setStates = (newState) => {
    setState((prevState) => ({ ...prevState, ...newState }));
  };
  return [state, setStates];
}

export default useStates;