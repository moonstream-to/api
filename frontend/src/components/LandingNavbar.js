import React, { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Button,
  Image,
  ButtonGroup,
  Spacer,
  Link,
  IconButton,
  Flex,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Portal,
} from "@chakra-ui/react";
import { ChevronDownIcon, HamburgerIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import ChakraAccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import { PAGETYPE, SITEMAP, PRIMARY_MOON_LOGO_URL } from "../core/constants";
import router from "next/router";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <>
      {ui.isMobileView && (
        <>
          <IconButton
            alignSelf="flex-start"
            colorScheme="blue"
            variant="solid"
            onClick={() => ui.setSidebarToggled(!ui.sidebarToggled)}
            icon={<HamburgerIcon />}
          />
        </>
      )}
      <Flex
        pl={ui.isMobileView ? 2 : "100px"}
        justifySelf="flex-start"
        h="48px"
        py={1}
        flexBasis="200px"
        flexGrow={1}
        id="Logo Container"
        alignItems="center"
      >
        <RouterLink href="/" passHref>
          <Link
            as={Image}
            w="auto"
            h={["70%", "85%"]}
            justifyContent="left"
            src={PRIMARY_MOON_LOGO_URL}
            alt="Moonstream logo"
          />
        </RouterLink>
      </Flex>

      {!ui.isMobileView && (
        <>
          <Spacer />
          <ButtonGroup variant="link" colorScheme="orange" spacing={4} pr={16}>
            {SITEMAP.map((item, idx) => {
              return (
                <React.Fragment key={`Fragment-${idx}`}>
                  {!item.children && item.type !== PAGETYPE.FOOTER_CATEGORY && (
                    <RouteButton
                      key={`${idx}-${item.title}-landing-all-links`}
                      variant="link"
                      href={item.path}
                      color="white"
                      isActive={!!(router.pathname === item.path)}
                    >
                      {item.title}
                    </RouteButton>
                  )}
                  {item.type !== PAGETYPE.FOOTER_CATEGORY && item.children && (
                    <Menu>
                      <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
                        {item.title}
                      </MenuButton>
                      <Portal>
                        <MenuList zIndex={100}>
                          {item.children.map((child, idx) => (
                            <RouterLink
                              shallow={true}
                              key={`${idx}-${item.title}-menu-links`}
                              href={child.path}
                              passHref
                            >
                              <MenuItem key={`menu-${idx}`} as={"a"} m={0}>
                                {child.title}
                              </MenuItem>
                            </RouterLink>
                          ))}
                        </MenuList>
                      </Portal>
                    </Menu>
                  )}
                </React.Fragment>
              );
            })}

            {ui.isLoggedIn && (
              <RouterLink href="/welcome" passHref>
                <Button
                  alignSelf={"center"}
                  as={Link}
                  colorScheme="orange"
                  variant="outline"
                  size="sm"
                  fontWeight="400"
                  borderRadius="2xl"
                >
                  App
                </Button>
              </RouterLink>
            )}
            {!ui.isLoggedIn && (
              <Button
                colorScheme="orange"
                variant="solid"
                onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
                size="sm"
                fontWeight="400"
                borderRadius="2xl"
              >
                Sign Up
              </Button>
            )}
            {!ui.isLoggedIn && (
              <Button
                color="white"
                onClick={() => toggleModal({ type: MODAL_TYPES.LOGIN })}
                fontWeight="400"
              >
                Log in
              </Button>
            )}
            {ui.isLoggedIn && (
              <ChakraAccountIconButton variant="link" colorScheme="orange" />
            )}
          </ButtonGroup>
        </>
      )}
      {ui.isLoggedIn && ui.isMobileView && (
        <>
          <Spacer />
          <ChakraAccountIconButton variant="link" colorScheme="orange" />
        </>
      )}
    </>
  );
};

export default LandingNavbar;
