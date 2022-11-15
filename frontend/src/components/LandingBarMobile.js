import React, { useContext } from "react";
import RouterLink from "next/link";
import { Image, Link, Flex, Spacer, Text, Box } from "@chakra-ui/react";
import { PRIMARY_MOON_LOGO_URL } from "../core/constants";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import useModals from "../core/hooks/useModals";
import UIContext from "../core/providers/UIProvider/context";
import PlainButton from "./atoms/PlainButton";

const LandingBarMobile = () => {
  const ui = useContext(UIContext);
  const { toggleModal } = useModals();
  return (
    <Flex direction="column" width={"100%"}>
      <Flex width={"100%"} alignItems="center" flex="flex: 0 0 100%" px="27px">
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
              bg="#F56646"
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
              // pb="5px"
            >
              <Text lineHeight="25px">App</Text>
            </Box>
          </RouterLink>
        )}
      </Flex>
    </Flex>
  );
};

export default LandingBarMobile;
