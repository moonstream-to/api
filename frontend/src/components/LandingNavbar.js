
import { jsx } from "@emotion/react";
import { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Flex,
  Button,
  Image,
  ButtonGroup,
  Spacer,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  MenuDivider,
  IconButton,
  Link,
} from "@chakra-ui/react";
import { ChevronDownIcon, HamburgerIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <>
      {!ui.isMobileView && (
        <Fragment>
          <Flex pl="7%">
            <RouterLink href="/" passHref>
              <Link>
                <Image
                  h="2rem"
                  src="/icons/bugout-dev-white.svg"
                  alt="bugout.dev"
                />
              </Link>
            </RouterLink>
          </Flex>

          <ButtonGroup
            variant="link"
            colorScheme="secondary"
            spacing={4}
            justifyContent="space-evenly"
            width="100%"
            pr={16}
          >
            <Spacer />
            {ui.isLoggedIn && (
              <RouterLink href="/app" passHref>
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
            <RouterLink href="/pricing" passHref>
              <Button color="white" fontWeight="400">
                Pricing
              </Button>
            </RouterLink>
            <RouterLink href="/case-studies/activeloop" passHref>
              <Button color="white" fontWeight="400" as={Link}>
                Case study
              </Button>
            </RouterLink>

            <Menu>
              <MenuButton
                size="xl"
                aria-label="menu"
                as={IconButton}
                color="white"
                icon={<HamburgerIcon />}
              >
                About us
              </MenuButton>
              <MenuList
                w={["100%", "16rem", "18rem", "20rem", "22rem", "24rem"]}
              >
                <RouterLink href="/team" passHref>
                  <MenuItem>Team and careers</MenuItem>
                </RouterLink>
                <RouterLink href="/events" passHref>
                  <MenuItem>Bugout events</MenuItem>
                </RouterLink>
                <MenuItem as="a" href="http://blog.bugout.dev">
                  Blog
                </MenuItem>
              </MenuList>
            </Menu>
          </ButtonGroup>
        </Fragment>
      )}
      {ui.isMobileView && (
        <Menu>
          <MenuButton
            as={Button}
            m={0}
            variant="solid"
            w={["100%", "100%", "18rem", "20rem", "22rem", "24rem"]}
            p={3}
            colorScheme="primary"
            h="3rem"
            borderRadius={0}
            rightIcon={<ChevronDownIcon boxSize="1.5rem" />}
          >
            <Image
              h="1.5rem"
              src="/icons/bugout-dev-white.svg"
              alt="bugout.dev"
            />
          </MenuButton>
          <MenuList
            zIndex={100}
            width={["100vw", "100vw", "18rem", "20rem", "22rem", "24rem"]}
            borderRadius={0}
            m={0}
          >
            <MenuGroup>
              {ui.isLoggedIn && (
                <RouterLink href="/app" passHref>
                  <MenuItem bgColor="secondary.600">Open App</MenuItem>
                </RouterLink>
              )}
              {!ui.isLoggedIn && (
                <>
                  <MenuItem onClick={() => toggleModal("register")}>
                    Sign Up
                  </MenuItem>
                  <MenuItem onClick={() => toggleModal("login")}>
                    Login
                  </MenuItem>
                </>
              )}
            </MenuGroup>

            <MenuDivider />
            <RouterLink href="/" passHref>
              <MenuItem>Home</MenuItem>
            </RouterLink>
            <RouterLink href="/pricing" passHref>
              <MenuItem>Pricing</MenuItem>
            </RouterLink>
            <RouterLink href="/case-studies/activeloop" passHref>
              <MenuItem>Case study</MenuItem>
            </RouterLink>
            <RouterLink href="/team" passHref>
              <MenuItem>Team</MenuItem>
            </RouterLink>
            <RouterLink href="/events" passHref>
              <MenuItem>Events</MenuItem>
            </RouterLink>

            <MenuItem as="a" href="http://blog.bugout.dev">
              Blog
            </MenuItem>
          </MenuList>
          {/* <Box bg="pink" w={["15rem", "15rem", "15rem", "18rem", "20rem"]} h="100%"></Box> */}
        </Menu>
      )}
    </>
  );
};

export default LandingNavbar;
