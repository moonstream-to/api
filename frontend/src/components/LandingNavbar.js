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
} from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import ChakraAccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import { ALL_NAV_PATHES, WHITE_LOGO_W_TEXT_URL } from "../core/constants";
import router from "next/router";
import { MODAL_TYPES } from "../core/providers/ModalProvider/constants";

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
        pl={ui.isMobileView ? 2 : 8}
        justifySelf="flex-start"
        h="100%"
        py={1}
        flexBasis="200px"
        flexGrow={1}
        id="Logo Container"
      >
        <RouterLink href="/" passHref>
          <Link
            as={Image}
            w="auto"
            h="full"
            justifyContent="left"
            src={WHITE_LOGO_W_TEXT_URL}
            alt="Moonstream logo"
          />
        </RouterLink>
      </Flex>

      {!ui.isMobileView && (
        <>
          <Spacer />
          <ButtonGroup variant="link" colorScheme="orange" spacing={4} pr={16}>
            {ALL_NAV_PATHES.map((item, idx) => (
              <RouteButton
                key={`${idx}-${item.title}-landing-all-links`}
                variant="link"
                href={item.path}
                color="white"
                isActive={!!(router.pathname === item.path)}
              >
                {item.title}
              </RouteButton>
            ))}

            {ui.isLoggedIn && (
              <RouterLink href="/welcome" passHref>
                <Button
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
            {/* {!ui.isLoggedIn && (
              <Button
                colorScheme="whiteAlpha"
                variant="outline"
                onClick={() => toggleModal("register")}
                size="sm"
                fontWeight="400"
                borderRadius="2xl"
              >
                Get started
              </Button>
            )} */}
            {!ui.isLoggedIn && (
              <Button
                color="white"
                onClick={() => toggleModal(MODAL_TYPES.LOGIN)}
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
