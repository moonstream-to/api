import React, { useContext } from "react";
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
  Text,
} from "@chakra-ui/react";

import { PAGETYPE, SITEMAP, PRIMARY_MOON_LOGO_URL } from "../core/constants";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import PlainButton from "./atoms/PlainButton";
import ChakraAccountIconButton from "./AccountIconButton";
import router from "next/router";

const LandingBarMobile = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <Flex
      h={ui.isAppView ? "72px" : "89px"}
      direction="column"
      width={"100%"}
      justifyContent={ui.isLoggedIn ? "center" : "space-between"}
      p="12px 7% 0px 7%"
    >
      <Flex width={"100%"} alignItems="center" flex="flex: 0 0 100%" mb="12px">
        <RouterLink href="/" passHref>
          <Link
            as={Image}
            w={"160px"}
            h={"23px"}
            justifyContent="left"
            src={PRIMARY_MOON_LOGO_URL}
            alt="Moonstream logo"
          />
        </RouterLink>
        <Spacer />

        {!ui.isLoggedIn && (
          <Flex gap="12px" h="26px">
            <Text
              color="white"
              bg="transparent"
              onClick={() => toggleModal({ type: MODAL_TYPES.LOGIN })}
              fontWeight="400"
              p="0px"
              m="0px"
              _focus={{ backgroundColor: "transparent" }}
              _hover={{ backgroundColor: "transparent" }}
            >
              Log in
            </Text>
            <PlainButton
              style={{
                fontSize: "14px",
                padding: "2px 10px",
              }}
              onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
            >
              Sign up
            </PlainButton>
          </Flex>
        )}

        {ui.isLoggedIn && (
          <Flex gap="12px">
            <PlainButton
              style={{
                fontSize: "14px",
                padding: "2px 10px",
              }}
              onClick={() => router.push("/welcome")}
            >
              App
            </PlainButton>

            <ChakraAccountIconButton variant="link" colorScheme="orange" />
          </Flex>
        )}
      </Flex>
      <ButtonGroup
        justifyContent="center"
        w="100%"
        variant="link"
        gap="20px"
        py="10px"
      >
        {SITEMAP.map((item, idx) => {
          return (
            <React.Fragment key={`Fragment-${idx}`}>
              {item.type !== PAGETYPE.FOOTER_CATEGORY && item.children && (
                <Menu>
                  <MenuButton color="white" m="0px" p="0px" as={Button}>
                    {item.title}
                  </MenuButton>
                  <Portal>
                    <MenuList
                      zIndex={100}
                      bg="black.300"
                      w="auto"
                      minW="auto"
                      borderRadius="10px"
                      p="10px 20px 10px 20px"
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
                            color="white"
                            key={`menu-${idx}`}
                            as={"a"}
                            target={
                              child.type === PAGETYPE.EXTERNAL
                                ? "_blank"
                                : "_self"
                            }
                            m={0}
                            fontSize="sm"
                            _focus={{ backgroundColor: "black.300" }}
                            _active={{ backgroundColor: "black.300" }}
                            _hover={{ backgroundColor: "black.300" }}
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
    </Flex>
  );
};

export default LandingBarMobile;
