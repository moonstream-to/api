import React, { useContext } from "react";
import RouterLink from "next/link";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  IconButton,
  chakra,
} from "@chakra-ui/react";
import { RiAccountCircleLine } from "react-icons/ri";
import useLogout from "../core/hooks/useLogout";
import UIContext from "../core/providers/UIProvider/context";
import { ALL_NAV_PATHES } from "../core/constants";
import { v4 } from "uuid";

const AccountIconButton = (props) => {
  const { logout } = useLogout();
  const ui = useContext(UIContext);

  return (
    <Menu>
      <MenuButton
        {...props}
        variant="inherit"
        colorScheme="inherit"
        as={IconButton}
        aria-label="Account menu"
        icon={<RiAccountCircleLine m={0} size="26px" />}
        color="gray.100"
      />
      <MenuList
        zIndex="dropdown"
        width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
        borderRadius={0}
      >
        <MenuGroup>
          <RouterLink href="/account/security" passHref>
            <MenuItem>Security</MenuItem>
          </RouterLink>
          <RouterLink href="/account/tokens" passHref>
            <MenuItem>API tokens</MenuItem>
          </RouterLink>
        </MenuGroup>
        <MenuDivider />
        {ui.isMobileView &&
          ALL_NAV_PATHES.map((pathToLink) => {
            return (
              <MenuItem key={v4()}>
                <RouterLink href={pathToLink.path}>
                  {pathToLink.title}
                </RouterLink>
              </MenuItem>
            );
          })}
        <MenuDivider />
        <MenuItem
          onClick={() => {
            logout();
          }}
        >
          Logout
        </MenuItem>
      </MenuList>
    </Menu>
  );
};

const ChakraAccountIconButton = chakra(AccountIconButton);

export default ChakraAccountIconButton;
