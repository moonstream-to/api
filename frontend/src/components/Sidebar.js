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
import {
  Flex,
  Image,
  IconButton,
  Divider,
  Text,
  Button,
} from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import React from "react";
import {
  HamburgerIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  LockIcon,
} from "@chakra-ui/icons";
import { MdSettings, MdDashboard, MdTimeline } from "react-icons/md";
import { WHITE_LOGO_W_TEXT_URL, ALL_NAV_PATHES } from "../core/constants";
import useDashboard from "../core/hooks/useDashboard";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import OverlayContext from "../core/providers/OverlayProvider/context";
import moment from "moment";

const Sidebar = () => {
  const ui = useContext(UIContext);
  const { dashboardsListCache } = useDashboard();
  const overlay = useContext(OverlayContext);
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
          <RouterLink href="/" passHref>
            <Image
              // h="full"
              // maxH="100%"
              maxW="120px"
              py="0.75rem"
              pl={5}
              src={WHITE_LOGO_W_TEXT_URL}
              alt="Moonstream To"
            />
          </RouterLink>
        </Flex>
      </SidebarHeader>
      <SidebarContent>
        <Divider borderColor="blue.600" />
        <Menu iconShape="square">
          {!ui.isLoggedIn && (
            <>
              <MenuItem
                onClick={() => {
                  overlay.toggleModal({ type: MODAL_TYPES.SIGNUP });
                  ui.setSidebarToggled(false);
                }}
              >
                Sign up
              </MenuItem>

              <MenuItem
                onClick={() => {
                  overlay.toggleModal({ type: MODAL_TYPES.LOGIN });
                  ui.setSidebarToggled(false);
                }}
              >
                Login
              </MenuItem>
              {ui.isMobileView &&
                ALL_NAV_PATHES.map((pathToLink, linkItemIndex) => {
                  return (
                    <MenuItem key={`mobile-all-nav-path-item-${linkItemIndex}`}>
                      <RouterLink href={pathToLink.path}>
                        {pathToLink.title}
                      </RouterLink>
                    </MenuItem>
                  );
                })}
            </>
          )}
          {ui.isLoggedIn && (
            <>
              <Text
                textColor="gray.300"
                size="sm"
                justifyContent="center"
                fontWeight="600"
                pl={2}
                pt={3}
              >
                Dashboards
              </Text>
              <Menu iconShape="square">
                <>
                  {dashboardsListCache.data &&
                    dashboardsListCache.data.data.resources.map(
                      (dashboard, idx) => {
                        return (
                          <MenuItem
                            icon={<MdDashboard />}
                            key={`dashboard-link-${idx}`}
                          >
                            <RouterLink href={`/dashboard/${dashboard?.id}`}>
                              {dashboard.resource_data.name}
                            </RouterLink>
                          </MenuItem>
                        );
                      }
                    )}
                </>
                <MenuItem>
                  <Button
                    variant="solid"
                    colorScheme="orange"
                    size="sm"
                    onClick={() =>
                      overlay.toggleModal({
                        type: MODAL_TYPES.NEW_DASHBOARD_FLOW,
                      })
                    }
                    // w="100%"
                    // borderRadius={0}
                  >
                    New dashboard
                  </Button>
                </MenuItem>
              </Menu>
            </>
          )}
          <Divider
            colorScheme="blue"
            bgColor="gray.300"
            color="blue.700"
            borderColor="blue.700"
          />
        </Menu>
      </SidebarContent>

      <SidebarFooter style={{ paddingBottom: "3rem" }}>
        <Divider color="gray.300" w="100%" />
        {ui.isLoggedIn && (
          <Menu iconShape="square">
            <MenuItem icon={<MdSettings />}>
              <RouterLink href="/subscriptions">Subscriptions </RouterLink>
            </MenuItem>
            <MenuItem icon={<MdTimeline />}>
              <RouterLink href="/stream">Stream</RouterLink>
            </MenuItem>
            <MenuItem icon={<LockIcon />}>
              <RouterLink href="/account/tokens">API Tokens</RouterLink>
            </MenuItem>
            <Divider />
            <Text
              pt={4}
              fontSize={"sm"}
              textColor="gray.700"
              textAlign="center"
            >
              © {moment().year()} Moonstream.to
            </Text>
          </Menu>
        )}
      </SidebarFooter>
    </ProSidebar>
  );
};

export default Sidebar;
