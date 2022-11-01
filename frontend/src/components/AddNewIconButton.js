import React, { useContext } from "react";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  IconButton,
  Text,
  chakra,
} from "@chakra-ui/react";
import { PlusSquareIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
import OverlayContext from "../core/providers/OverlayProvider/context";

import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const AddNewIconButton = (props) => {
  const ui = useContext(UIContext);
  const overlay = useContext(OverlayContext);

  return (
    <Menu>
      <MenuButton
        {...props}
        as={IconButton}
        // onClick={ui.addNewDrawerState.onOpen}
        aria-label="Account menu"
        icon={<PlusSquareIcon m={0} size="26px" />}
        // variant="outline"
        color="gray.100"
      />
      <MenuList
        zIndex="dropdown"
        width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
        borderRadius={0}
      >
        <MenuGroup>
          <MenuItem
            onClick={() =>
              overlay.toggleModal({
                type: MODAL_TYPES.NEW_DASHBOARD_FLOW,
                props: undefined,
              })
            }
          >
            <Text color="black">New Dashboard...</Text>
          </MenuItem>
          <MenuItem
            onClick={() =>
              overlay.toggleModal({
                type: MODAL_TYPES.NEW_SUBSCRIPTON,
                props: undefined,
              })
            }
          >
            <Text color="black">New Subscription...</Text>
          </MenuItem>

          {ui.isInDashboard && <MenuItem>New report...</MenuItem>}
        </MenuGroup>
        <MenuDivider />
      </MenuList>
    </Menu>
  );
};

const ChakraAddNewIconButton = chakra(AddNewIconButton);

export default ChakraAddNewIconButton;
