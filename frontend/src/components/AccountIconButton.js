import React from "react";
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

const AccountIconButton = (props) => {
  const { logout } = useLogout();

  return (
    <Menu>
      <MenuButton
        {...props}
        as={IconButton}
        aria-label="Account menu"
        icon={<RiAccountCircleLine size="26px" />}
        // variant="outline"
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
        </MenuGroup>
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
