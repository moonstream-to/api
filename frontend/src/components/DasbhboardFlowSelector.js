import React, { useContext } from "react";
import { chakra, ButtonGroup, Button } from "@chakra-ui/react";
import OverlayContext from "../core/providers/OverlayProvider/context";
import {
  DRAWER_TYPES,
  MODAL_TYPES,
} from "../core/providers/OverlayProvider/constants";
import { useDashboard } from "../core/hooks";

const NewDashboard = () => {
  const overlay = useContext(OverlayContext);
  const { createDashboard } = useDashboard();

  return (
    <>
      <ButtonGroup>
        <Button
          onClick={() => {
            overlay.toggleModal({ type: MODAL_TYPES.OFF });
            sessionStorage.removeItem("new_dashboard");
            createDashboard.mutate();
          }}
        >
          Empty dashboard
        </Button>
        <Button
          onClick={() => {
            overlay.toggleModal({ type: MODAL_TYPES.OFF });
            overlay.toggleDrawer({ type: DRAWER_TYPES.NEW_DASHBOARD });
          }}
        >
          Automatically define from ABI
        </Button>
      </ButtonGroup>
    </>
  );
};

const ChakraNewDashboard = chakra(NewDashboard);

export default ChakraNewDashboard;
