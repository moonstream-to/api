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
  Box,
} from "@chakra-ui/react";

import { PAGETYPE, SITEMAP, PRIMARY_MOON_LOGO_URL } from "../core/constants";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import PlainButton from "./atoms/PlainButton";
import ChakraAccountIconButton from "./AccountIconButton";

const LandingBarMobile = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <Flex
      h={ui.isAppView ? "72px" : "89px"}
      direction="column"
      width={"100%"}
      justifyContent={ui.isLoggedIn ? "center" : "space-between"}
    >
      <Flex
        width={"100%"}
        alignItems="center"
        flex="flex: 0 0 100%"
        pl="10px"
        pr="27px"
        mt={ui.isLoggedIn ? "0px" : "12px"}
      >
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
          <PlainButton
            style={{
              marginRight: "12px",
              fontSize: "14px",
              padding: "2px 10px",
            }}
            onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
          >
            Sign up
          </PlainButton>
        )}
        {!ui.isLoggedIn && (
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
        )}
        {ui.isLoggedIn && (
          <RouterLink href="/welcome" passHref>
            <Box
              bg="orange.1000"
              alignSelf={"center"}
              as={Link}
              color="white"
              size="sm"
              fontWeight="700"
              borderRadius="15px"
              w="47px"
              h="25px"
              textAlign="center"
              fontSize="14px"
            >
              <Text lineHeight="25px">App</Text>
            </Box>
          </RouterLink>
        )}
        {ui.isLoggedIn && ui.isMobileView && (
          <>
            <ChakraAccountIconButton variant="link" colorScheme="orange" />
          </>
        )}
      </Flex>
      <ButtonGroup
        justifyContent="center"
        w="100%"
        variant="link"
        spacing={4}
        flexGrow={0.5}
      >
        {SITEMAP.map((item, idx) => {
          return (
            <React.Fragment key={`Fragment-${idx}`}>
              {item.type !== PAGETYPE.FOOTER_CATEGORY && item.children && (
                <Menu>
                  <MenuButton variant="mobile" mb="0px" p="0px" as={Button}>
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
                            m={0}
                            fontSize="sm"
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
    </Flex>
  );
};

export default LandingBarMobile;
