
import { jsx } from "@emotion/react";
import { ProSidebar } from "react-pro-sidebar";
import AppSidebar from "./AppSidebar";
import { useContext } from "react";
import RouterLink from "next/link";
import {
  Button,
  Image,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  Link,
} from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
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
      {!ui.isMobileView && (
        <Link href="/" bgColor="primary.1200">
          <Image
            // as={Link}
            // to="/"
            h="3rem"
            py="0.75rem"
            pl={5}
            src="/icons/bugout-dev-white.svg"
            alt="bugout.dev"
          />
        </Link>
      )}
      {ui.isMobileView && (
        <Menu>
          <MenuButton
            as={Button}
            m={0}
            variant="solid"
            w={["100%", "100%", "18rem", "20rem", "22rem", "24rem"]}
            p={5}
            colorScheme="primary"
            h="3rem"
            borderRadius={0}
            // bgColor="primary.900"
            rightIcon={<ChevronDownIcon boxSize="1.5rem" />}
          >
            {" "}
            <Image
              h="3rem"
              py="0.75rem"
              pl={5}
              src="/icons/bugout-dev-white.svg"
              alt="bugout.dev"
            />
          </MenuButton>

          <MenuList
            zIndex="dropdown"
            width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
            borderRadius={0}
            m={0}
          >
            <MenuGroup>
              <RouterLink href="/case-studies/activeloop" passHref>
                <MenuItem>case studies</MenuItem>
              </RouterLink>
            </MenuGroup>
            <MenuDivider />
            <RouterLink href="/events" passHref>
              <MenuItem>events</MenuItem>
            </RouterLink>
            <RouterLink href="/team" passHref>
              <MenuItem>team</MenuItem>
            </RouterLink>
            <RouterLink href="/pricing" passHref>
              <MenuItem>pricing</MenuItem>
            </RouterLink>
          </MenuList>
        </Menu>
      )}
      {ui.isAppView && ui.isAppReady && ui.isLoggedIn && <AppSidebar />}
      {/* <Menu iconShape="square">
        <MenuItem>Dashboard</MenuItem>
        <SubMenu title="Components">
          <MenuItem>Component 1</MenuItem>
          <MenuItem>Component 2</MenuItem>
        </SubMenu>
      </Menu> */}
    </ProSidebar>
  );
};

export default Sidebar;
