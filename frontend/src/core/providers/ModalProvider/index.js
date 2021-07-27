import React, { useState } from "react";
import ModalContext from "./context";

const ModalProvider = ({ children }) => {
  const [modal, toggleModal] = useState();
  return (
    <ModalContext.Provider value={{ modal, toggleModal }}>
      {children}
    </ModalContext.Provider>
  );
};

export default ModalProvider;
