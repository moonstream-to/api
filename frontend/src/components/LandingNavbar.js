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
          <ButtonGroup
            variant="link"
            spacing={4}
            width="100%"
            justifyContent="center"
          >
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
                                target={
                                  child.type === PAGETYPE.EXTERNAL
                                    ? "_blank"
                                    : "_self"
                                }
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
          {ui.isLoggedIn && (
            <Flex gap="20px">
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
              <ChakraAccountIconButton
                variant="link"
                colorScheme="orange"
                h="32px"
              />
            </Flex>
          )}

          {!ui.isLoggedIn && (
            <Flex gap="20px" alignItems="center">
              <Text
                color="white"
                cursor="pointer"
                onClick={() => toggleModal({ type: MODAL_TYPES.LOGIN })}
                fontWeight="400"
                _hover={{ textDecoration: "underline" }}
              >
                Log&nbsp;in
              </Text>
              <Button
                variant="plainOrange"
                borderRadius="15px"
                p="5px 10px"
                fontSize="16px"
                m="0px"
                h="32px"
                onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
                fontWeight="700"
                textColor="white"
                _hover={{
                  backgroundColor: "#F4532F",
                }}
              >
                Sign&nbsp;up
              </Button>
            </Flex>
          )}
        </Flex>
      )}
    </>
  );
};

export default LandingNavbar;
