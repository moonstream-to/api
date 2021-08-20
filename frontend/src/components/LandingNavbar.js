import React, { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Flex,
  Button,
  Image,
  ButtonGroup,
  Spacer,
  Link,
  IconButton,
} from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import ChakraAccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import { ALL_NAV_PATHES } from "../core/constants";
import router from "next/router";

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <>
      <>
        {ui.isMobileView && (
          <>
            <IconButton
              alignSelf="flex-start"
              colorScheme="primary"
              variant="solid"
              onClick={() => ui.setSidebarToggled(!ui.sidebarToggled)}
              icon={<HamburgerIcon />}
            />
          </>
        )}
        <Flex ml={ui.isMobileView ? 2 : 8} justifySelf="flex-start">
          <RouterLink href="/" passHref>
            <Link>
              <Image
                w="200px"
                src="https://s3.amazonaws.com/static.simiotics.com/moonstream/assets/White+logo.svg"
                alt="Moonstream logo"
              />
            </Link>
          </RouterLink>
        </Flex>

        {!ui.isMobileView && (
          <>
            <Spacer />
            <ButtonGroup
              variant="link"
              colorScheme="secondary"
              spacing={4}
              pr={16}
            >
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
                <RouterLink href="/stream" passHref>
                  <Button
                    as={Link}
                    colorScheme="secondary"
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
                  colorScheme="whiteAlpha"
                  variant="outline"
                  onClick={() => toggleModal("register")}
                  size="sm"
                  fontWeight="400"
                  borderRadius="2xl"
                >
                  Get started
                </Button>
              )}
              {!ui.isLoggedIn && (
                <Button
                  color="white"
                  onClick={() => toggleModal("login")}
                  fontWeight="400"
                >
                  Log in
                </Button>
              )}
              {ui.isLoggedIn && (
                <ChakraAccountIconButton
                  variant="link"
                  colorScheme="secondary"
                />
              )}
            </ButtonGroup>
          </>
        )}
        {ui.isLoggedIn && ui.isMobileView && (
          <>
            <Spacer />
            <ChakraAccountIconButton variant="link" colorScheme="secondary" />
          </>
        )}
      </>
    </>
  );
};

export default LandingNavbar;
