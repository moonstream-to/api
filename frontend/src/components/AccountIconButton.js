import React, { useContext } from "react";
import RouterLink from "next/link";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  IconButton,
  chakra,
  Portal,
} from "@chakra-ui/react";
import { RiAccountCircleLine } from "react-icons/ri";
import useLogout from "../core/hooks/useLogout";
import UIContext from "../core/providers/UIProvider/context";
import { PAGETYPE, SITEMAP } from "../core/constants";

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
        icon={<RiAccountCircleLine size="26px" />}
        color="gray.100"
        h="26px"
        minW="26px"
        m="0px"
      />
      <Portal>
        <MenuList
          zIndex={100}
          bg="#1A1D22"
          w="auto"
          minW="auto"
          borderRadius="10px"
          p="20px 20px 10px 20px"
          border="1px solid white"
        >
          <MenuGroup>
            <RouterLink href="/account/security" passHref>
              <div className="desktop-menu-item">Security</div>
            </RouterLink>
            <RouterLink href="/account/tokens" passHref>
              <div className="desktop-menu-item" title="API tokens">
                API tokens
              </div>
            </RouterLink>
          </MenuGroup>
          {ui.isMobileView &&
            SITEMAP.map((item, idx) => {
              if (item.type !== PAGETYPE.FOOTER_CATEGORY && item.children) {
                return (
                  <MenuGroup key={`AccountIconButton-MenuGroup-${idx}`}>
                    {item.children.map((child, idx) => {
                      return (
                        <MenuItem
                          key={`AccountIconButton-SITEMAP-${idx}`}
                          m={0}
                          color="white"
                          fontWeight="400"
                          fontSize="16px"
                          px="0px"
                          mb="10px"
                          h="22px"
                          _hover={{
                            backgroundColor: "#1A1D22",
                            color: "#F56646",
                            fontWeight: "700",
                          }}
                          _focus={{ backgroundColor: "#1A1D22" }}
                        >
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
          <div
            className="desktop-menu-item"
            onClick={() => {
              logout();
            }}
          >
            Logout
          </div>
        </MenuList>
      </Portal>
    </Menu>
  );
};

const ChakraAccountIconButton = chakra(AccountIconButton);

export default ChakraAccountIconButton;
