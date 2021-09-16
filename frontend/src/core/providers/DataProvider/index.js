import React, { useState } from "react";
import DataContext from "./context";

const DataProvider = ({ children }) => {
  const [streamCache, setStreamCache] = useState([]);
  const [cursor, setCursor] = useState(0);
  return (
    <DataContext.Provider
      value={{ streamCache, setStreamCache, cursor, setCursor }}
    >
      {children}
    </DataContext.Provider>
  );
};

export default DataProvider;
