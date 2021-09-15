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
import { Flex, Image, IconButton } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import React from "react";
import { HamburgerIcon, ArrowLeftIcon, ArrowRightIcon } from "@chakra-ui/icons";
import { MdTimeline, MdSettings } from "react-icons/md";
import { ImStatsBars } from "react-icons/im";
import { HiAcademicCap } from "react-icons/hi";
import { WHITE_LOGO_W_TEXT_URL } from "../core/constants";

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
            colorScheme="primary"
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
          <Menu iconShape="square">
            <MenuItem icon={<MdTimeline />}>
              {" "}
              <RouterLink href="/stream">Stream</RouterLink>
            </MenuItem>
          </Menu>
          <Menu iconShape="square">
            <MenuItem icon={<ImStatsBars />}>
              {" "}
              <RouterLink href="/analytics">Analytics </RouterLink>
            </MenuItem>
          </Menu>
          <Menu iconShape="square">
            <MenuItem icon={<MdSettings />}>
              {" "}
              <RouterLink href="/subscriptions">Subscriptions </RouterLink>
            </MenuItem>
          </Menu>
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
                ui.toggleModal("login");
                ui.setSidebarToggled(false);
              }}
            >
              Login
            </MenuItem>
          </Menu>
        </SidebarContent>
      )}

      <SidebarFooter></SidebarFooter>
    </ProSidebar>
  );
};

export default Sidebar;
