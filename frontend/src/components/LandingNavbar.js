import React, { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Button,
  Image,
  ButtonGroup,
  Spacer,
  Link,
  Flex,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Portal,
  Box,
  Text,
} from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import ChakraAccountIconButton from "./AccountIconButton";
import RouteButton from "./RouteButton";
import { PAGETYPE, SITEMAP, PRIMARY_MOON_LOGO_URL } from "../core/constants";
import router from "next/router";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import LandingBarMobile from "./LandingBarMobile";

const LandingNavbar = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <>
      {ui.isMobileView && <LandingBarMobile />}
      {!ui.isMobileView && (
        <>
          <Flex
            pl={ui.isMobileView ? 2 : "60px"}
            justifySelf="flex-start"
            h="48px"
            py={1}
            flexBasis="200px"
            flexGrow={0.6}
            id="Logo Container"
            alignItems="center"
          >
            <RouterLink href="/" passHref>
              <Link
                as={Image}
                w={"160px"}
                justifyContent="left"
                src={PRIMARY_MOON_LOGO_URL}
                alt="Moonstream logo"
              />
            </RouterLink>
          </Flex>
          <ButtonGroup variant="link" spacing={4} pr={16} flexGrow={0.5}>
            {SITEMAP.map((item, idx) => {
              return (
                <React.Fragment key={`Fragment-${idx}`}>
                  {!item.children && item.type !== PAGETYPE.FOOTER_CATEGORY && (
                    <RouteButton
                      key={`${idx}-${item.title}-landing-all-links`}
                      variant="link"
                      href={item.path}
                      color="black"
                      fontSize="16px"
                      isActive={!!(router.pathname === item.path)}
                    >
                      {item.title}
                    </RouteButton>
                  )}
                  {item.type !== PAGETYPE.FOOTER_CATEGORY && item.children && (
                    <Menu autoSelect="false">
                      <MenuButton
                        as={Button}
                        rightIcon={<ChevronDownIcon />}
                        color="white"
                        fontSize="16px"
                        _expanded={{ color: "white" }}
                      >
                        {item.title}
                      </MenuButton>
                      <Portal>
                        <MenuList
                          zIndex={100}
                          bg="#1A1D22"
                          w="auto"
                          minW="auto"
                          borderRadius="10px"
                          p="20px 20px 10px 20px"
                          border="1px solid white"
                        >
                          {item.children.map((child, idx) => (
                            <RouterLink
                              shallow={true}
                              key={`${idx}-${item.title}-menu-links`}
                              href={child.path}
                              passHref
                            >
                              <MenuItem
                                key={`menu-${idx}`}
                                as={"a"}
                                m={0}
                                color="white"
                                fontWeight="400"
                                fontSize="16px"
                                px="0px"
                                mb="10px"
                                h="22px"
                                _hover={{
                                  backgroundColor: "#1A1D22",
                                  color: "#F56646",
                                  fontWeight: "700",
                                }}
                                _focus={{ backgroundColor: "#1A1D22" }}
                              >
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
          </ButtonGroup>
          <ButtonGroup variant="link" spacing={4} pr={16}>
            {ui.isLoggedIn && (
              <RouterLink href="/welcome" passHref>
                <Box
                  bg="#F56646"
                  alignSelf={"center"}
                  fontWeight="700"
                  borderRadius="15px"
                  w="51px"
                  h="32px"
                  textAlign="center"
                  px="10px"
                  cursor="pointer"
                  _hover={{
                    backgroundColor: "#F4532F",
                  }}
                >
                  <Text fontSize="16px" lineHeight="32px">
                    App
                  </Text>
                </Box>
              </RouterLink>
            )}
            {!ui.isLoggedIn && (
              <Button
                bg="#F56646"
                variant="solid"
                onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
                size="sm"
                fontWeight="700"
                borderRadius="2xl"
                textColor="white"
                _hover={{
                  backgroundColor: "#F4532F",
                }}
              >
                Sign up
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
