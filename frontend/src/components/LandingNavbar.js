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

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <>
      <>
        <Flex position="absolute" left="calc(50% - 100px)">
          <RouterLink href="/" passHref>
            <Link>
              <Image
                w="200px"
                src="/icons/bugout-dev-white.svg"
                alt="bugout.dev"
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
              {ui.isLoggedIn && <ChakraAccountIconButton />}
            </ButtonGroup>
          </>
        )}
      </>

      {ui.isMobileView && (
        <>
          <IconButton
            colorScheme="secondary"
            variant="solid"
            onClick={() => ui.setSidebarToggled(!ui.sidebarToggled)}
            icon={<HamburgerIcon />}
          />
        </>
      )}
    </>
  );
};

export default LandingNavbar;
