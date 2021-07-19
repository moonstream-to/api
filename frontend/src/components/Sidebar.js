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
import { HamburgerIcon } from "@chakra-ui/icons";
import { MdTimeline, MdSettings } from "react-icons/md";
// import RouterLink from "next/link";
// import RouterLink from "next/link";

const Sidebar = () => {
  const ui = useContext(UIContext);
  return (
    <ProSidebar
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
            icon={<HamburgerIcon />}
            onClick={() => {
              ui.isMobileView
                ? ui.setSidebarToggled(!ui.sidebarToggled)
                : ui.setSidebarCollapsed(!ui.sidebarCollapsed);
            }}
          />
          <Image
            // as={Link}
            // to="/"
            h="3rem"
            py="0.75rem"
            pl={5}
            src="/icons/bugout-dev-white.svg"
            alt="bugout.dev"
          />
        </Flex>
      </SidebarHeader>
      <SidebarContent>
        <Menu iconShape="square">
          <MenuItem icon={<MdTimeline />}>
            {" "}
            <RouterLink href="/stream">Stream</RouterLink>
          </MenuItem>
        </Menu>
        <Menu iconShape="square">
          <MenuItem icon={<MdSettings />}>
            {" "}
            <RouterLink href="/subscriptions">Subscriptions </RouterLink>
          </MenuItem>
        </Menu>
      </SidebarContent>
      <SidebarFooter>
        {/**
         *  You can add a footer for the sidebar ex: copyright
         */}
      </SidebarFooter>
    </ProSidebar>
  );
};

export default Sidebar;
