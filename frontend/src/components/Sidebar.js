import {
  ProSidebar,
  Menu,
  MenuItem,
  SidebarHeader,
  SidebarFooter,
  SidebarContent,
} from "react-pro-sidebar";
import { useContext } from "react";
import RouterLink from "next/link";
import { Flex, Image, IconButton, Divider } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import React from "react";
import {
  HamburgerIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  LockIcon,
} from "@chakra-ui/icons";
import { MdSettings } from "react-icons/md";
import { HiAcademicCap } from "react-icons/hi";
import { WHITE_LOGO_W_TEXT_URL } from "../core/constants";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const Sidebar = () => {
  const ui = useContext(UIContext);
  return (
    <ProSidebar
      width="240px"
      breakPoint="lg"
      toggled={ui.sidebarToggled}
      onToggle={ui.setSidebarToggled}
      collapsed={ui.sidebarCollapsed}
      hidden={!ui.sidebarVisible}
    >
      <SidebarHeader>
        <Flex>
          <IconButton
            ml={4}
            justifySelf="flex-start"
            colorScheme="blue"
            aria-label="App navigation"
            icon={
              ui.isMobileView ? (
                <HamburgerIcon />
              ) : ui.sidebarCollapsed ? (
                <ArrowRightIcon />
              ) : (
                <ArrowLeftIcon />
              )
            }
            onClick={() => {
              ui.isMobileView
                ? ui.setSidebarToggled(!ui.sidebarToggled)
                : ui.setSidebarCollapsed(!ui.sidebarCollapsed);
            }}
          />
          <Image
            // h="full"
            // maxH="100%"
            maxW="120px"
            py="0.75rem"
            pl={5}
            src={WHITE_LOGO_W_TEXT_URL}
            alt="bugout.dev"
          />
        </Flex>
      </SidebarHeader>
      {ui.isLoggedIn && (
        <SidebarContent>
          <Menu iconShape="square"></Menu>
          <Menu iconShape="square"></Menu>
          {ui.isMobileView && (
            <Menu iconShape="square">
              <MenuItem icon={<HiAcademicCap />}>
                <RouterLink href="/welcome">
                  Learn how to use Moonstream
                </RouterLink>
              </MenuItem>
            </Menu>
          )}
        </SidebarContent>
      )}
      {!ui.isLoggedIn && (
        <SidebarContent>
          {/* <Menu iconShape="square">
            <MenuItem
              onClick={() => {
                ui.toggleModal("register");
                ui.setSidebarToggled(false);
              }}
            >
              Sign up
            </MenuItem>
          </Menu> */}
          <Menu iconShape="square">
            <MenuItem
              onClick={() => {
                ui.toggleModal({ type: MODAL_TYPES.LOGIN });
                ui.setSidebarToggled(false);
              }}
            >
              Login
            </MenuItem>
            <MenuItem>
              {" "}
              <RouterLink href="/product">Product </RouterLink>
            </MenuItem>
            <MenuItem>
              {" "}
              <RouterLink href="/team">Team </RouterLink>
            </MenuItem>
          </Menu>
        </SidebarContent>
      )}

      <SidebarFooter style={{ paddingBottom: "3rem" }}>
        <Divider color="gray.300" w="100%" />
        {ui.isLoggedIn && (
          <Menu iconShape="square">
            <MenuItem icon={<LockIcon />}>
              <RouterLink href="/account/tokens">API Tokens</RouterLink>
            </MenuItem>
            <MenuItem icon={<MdSettings />}>
              {" "}
              <RouterLink href="/subscriptions">Subscriptions </RouterLink>
            </MenuItem>
          </Menu>
        )}
      </SidebarFooter>
    </ProSidebar>
  );
};

export default Sidebar;
