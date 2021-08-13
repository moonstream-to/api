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
import { Flex, Image, IconButton, Tooltip } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import React from "react";
import { HamburgerIcon, ArrowLeftIcon, ArrowRightIcon } from "@chakra-ui/icons";
import { MdTimeline, MdSettings } from "react-icons/md";
import { ImStatsBars } from "react-icons/im";

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
                <Tooltip
                  shouldWrapChildren
                  hasArrow
                  label="Access app menu here"
                  isOpen={ui.showPopOvers}
                  variant="onboarding"
                >
                  <HamburgerIcon />
                </Tooltip>
              ) : ui.sidebarCollapsed ? (
                <Tooltip
                  shouldWrapChildren
                  hasArrow
                  label="Expand sidebar"
                  isOpen={ui.showPopOvers}
                  variant="onboarding"
                >
                  <ArrowRightIcon />
                </Tooltip>
              ) : (
                <Tooltip
                  shouldWrapChildren
                  hasArrow
                  label="Collapse sidebar"
                  isOpen={ui.showPopOvers}
                  variant="onboarding"
                >
                  <ArrowLeftIcon />
                </Tooltip>
              )
            }
            onClick={() => {
              ui.isMobileView
                ? ui.setSidebarToggled(!ui.sidebarToggled)
                : ui.setSidebarCollapsed(!ui.sidebarCollapsed);
            }}
          />
          <Tooltip
            shouldWrapChildren
            hasArrow
            label="go to homepage"
            variant="onboarding"
            // isOpen={ui.showPopOvers} variant="onboarding"
            isDisabled
          >
            <Image
              // as={Link}
              // to="/"
              w="150px"
              py="0.75rem"
              pl={5}
              src="https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/White+logo.svg"
              alt="moonstream.to"
            />
          </Tooltip>
        </Flex>
      </SidebarHeader>
      {ui.isLoggedIn && (
        <SidebarContent>
          <Menu iconShape="square">
            <Tooltip
              // shouldWrapChildren
              hasArrow
              label="Live stream of addresses you subscribed to"
              variant="onboarding"
              isOpen={
                ui.showPopOvers &&
                ((ui.sidebarToggled && ui.isMobileView) || !ui.isMobileView)
              }
            >
              <MenuItem icon={<MdTimeline />}>
                <RouterLink href="/stream">Stream</RouterLink>
              </MenuItem>
            </Tooltip>
          </Menu>
          <Menu iconShape="square">
            <Tooltip
              variant="onboarding"
              // shouldWrapChildren
              hasArrow
              label="Analytical mode to build your monitors"
              isOpen={
                ui.showPopOvers &&
                ((ui.sidebarToggled && ui.isMobileView) || !ui.isMobileView)
              }
            >
              <MenuItem icon={<ImStatsBars />}>
                <RouterLink href="/analytics">Analytics</RouterLink>
              </MenuItem>
            </Tooltip>
          </Menu>
          <Menu iconShape="square">
            <Tooltip
              variant="onboarding"
              // shouldWrapChildren
              hasArrow
              label="Set up subscriptions here to get data in to moonstream!"
              isOpen={
                ui.showPopOvers &&
                ((ui.sidebarToggled && ui.isMobileView) || !ui.isMobileView)
              }
            >
              <MenuItem icon={<MdSettings />}>
                <RouterLink href="/subscriptions">Subscriptions</RouterLink>
              </MenuItem>
            </Tooltip>
          </Menu>
        </SidebarContent>
      )}
      {!ui.isLoggedIn && (
        <SidebarContent>
          <Menu iconShape="square">
            <MenuItem
              onClick={() => {
                ui.toggleModal("register");
                ui.setSidebarToggled(false);
              }}
            >
              Sign up
            </MenuItem>
          </Menu>
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
