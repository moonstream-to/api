import OverlayContext from "../providers/OverlayProvider/context";
import { useContext } from "react";

const useModals = () => {
  const modals = useContext(OverlayContext);

  return modals;
};

export default useModals;
