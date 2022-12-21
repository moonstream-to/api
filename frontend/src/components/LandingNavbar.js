import React, { Fragment, useContext } from "react";
import RouterLink from "next/link";
import {
  Button,
  Image,
  ButtonGroup,
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
        <Flex px="7%" w="100%" justifyContent="space-between">
          <Flex
            justifySelf="flex-start"
            py={1}
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
          <ButtonGroup variant="link" spacing={4}>
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
                        fontWeight="500"
                        fontSize="16px"
                        _expanded={{ color: "white", fontWeight: "700" }}
                        _focus={{ textDecoration: "none" }}
                        _hover={{ textDecoration: "none", fontWeight: "700" }}
                      >
                        {item.title}
                      </MenuButton>
                      <Portal>
                        <MenuList
                          zIndex={100}
                          bg="black.300"
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
                                  backgroundColor: "black.300",
                                  color: "orange.1000",
                                  fontWeight: "700",
                                }}
                                _focus={{ backgroundColor: "black.300" }}
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
          <ButtonGroup variant="link" spacing={4} minW="160px">
            {ui.isLoggedIn && (
              <RouterLink href="/welcome" passHref>
                <Box
                  bg="orange.1000"
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
                bg="orange.1000"
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
        </Flex>
      )}
    </>
  );
};

export default LandingNavbar;
