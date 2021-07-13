import ModalContext from "../providers/ModalProvider/context";
import { useContext } from "react";

const useModals = () => {
  const modals = useContext(ModalContext);

  return modals;
};

export default useModals;
