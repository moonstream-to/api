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
  Portal,
} from "@chakra-ui/react";
import { RiAccountCircleLine } from "react-icons/ri";
import useLogout from "../core/hooks/useLogout";
import UIContext from "../core/providers/UIProvider/context";
import { SITEMAP } from "../core/constants";

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
      <Portal>
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
            SITEMAP.map((item, idx) => {
              if (item.children) {
                return (
                  <MenuGroup key={`AccountIconButton-MenuGroup-${idx}`}>
                    {item.children.map((child, idx) => {
                      return (
                        <MenuItem key={`AccountIconButton-SITEMAP-${idx}`}>
                          <RouterLink href={child.path}>
                            {child.title}
                          </RouterLink>
                        </MenuItem>
                      );
                    })}
                  </MenuGroup>
                );
              }
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
      </Portal>
    </Menu>
  );
};

const ChakraAccountIconButton = chakra(AccountIconButton);

export default ChakraAccountIconButton;
