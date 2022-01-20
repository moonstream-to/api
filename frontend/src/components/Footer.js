import React from "react";
import {
  Text,
  Link,
  Box,
  Container,
  SimpleGrid,
  Stack,
  Image as ChakraImage,
  useColorModeValue,
  VisuallyHidden,
  chakra,
} from "@chakra-ui/react";
import RouterLink from "next/link";
import {
  WHITE_LOGO_W_TEXT_URL,
  ALL_NAV_PATHES,
  FOOTER_COLUMNS,
} from "../core/constants";
import { FaGithub, FaTwitter, FaDiscord } from "react-icons/fa";
import moment from "moment";

const LINKS_SIZES = {
  fontWeight: "300",
  fontSize: "lg",
};

const ListHeader = ({ children }) => {
  return (
    <Text
      fontWeight={"500"}
      fontSize={"lg"}
      mb={2}
      borderBottom="1px"
      borderColor="blue.700"
      textColor="blue.500"
    >
      {children}
    </Text>
  );
};

const SocialButton = ({ children, label, href }) => {
  return (
    <chakra.button
      bg={useColorModeValue("blackAlpha.100", "whiteAlpha.100")}
      rounded={"full"}
      w={8}
      h={8}
      cursor={"pointer"}
      as={"a"}
      href={href}
      display={"inline-flex"}
      alignItems={"center"}
      justifyContent={"center"}
      transition={"background 0.3s ease"}
      _hover={{
        bg: useColorModeValue("blackAlpha.200", "whiteAlpha.200"),
      }}
    >
      <VisuallyHidden>{label}</VisuallyHidden>
      {children}
    </chakra.button>
  );
};

const Footer = () => (
  <Box
    bg={useColorModeValue("blue.900", "gray.900")}
    color={useColorModeValue("gray.700", "gray.200")}
  >
    <Container as={Stack} maxW={"6xl"} py={10}>
      <SimpleGrid
        templateColumns={{ sm: "1fr 1fr", md: "2fr 1fr 1fr 2fr" }}
        spacing={8}
      >
        <Stack spacing={6}>
          <Box>
            <Link href="/" alignSelf="center">
              <ChakraImage
                alignSelf="center"
                // as={Link}
                // to="/"
                h="2.5rem"
                minW="2.5rem"
                src={WHITE_LOGO_W_TEXT_URL}
                alt="Go to app root"
              />
            </Link>
          </Box>
          <Text fontSize={"sm"}>
            © {moment().year()} Moonstream.to All rights reserved
          </Text>
          <Stack direction={"row"} spacing={6}>
            <SocialButton
              label={"Twitter"}
              href={"https://twitter.com/moonstreamto"}
            >
              <FaTwitter />
            </SocialButton>
            <SocialButton
              label={"Github"}
              href={"https://github.com/bugout-dev/moonstream"}
            >
              <FaGithub />
            </SocialButton>
            <SocialButton
              label={"Discord"}
              href={"https://discord.gg/K56VNUQGvA"}
            >
              <FaDiscord />
            </SocialButton>
          </Stack>
        </Stack>
        {Object.values(FOOTER_COLUMNS).map((columnEnum, colIndex) => {
          return (
            <Stack align={"flex-start"} key={`footer-list-column-${colIndex}`}>
              {ALL_NAV_PATHES.filter(
                (navPath) => navPath.footerCategory === columnEnum
              ).length > 0 && (
                <>
                  <ListHeader>{columnEnum}</ListHeader>
                  {ALL_NAV_PATHES.filter(
                    (navPath) => navPath.footerCategory === columnEnum
                  ).map((linkItem, linkItemIndex) => {
                    return (
                      <RouterLink
                        passHref
                        href={linkItem.path}
                        key={`footer-list-link-item-${linkItemIndex}-col-${colIndex}`}
                      >
                        <Link {...LINKS_SIZES}>{linkItem.title}</Link>
                      </RouterLink>
                    );
                  })}
                </>
              )}
            </Stack>
          );
        })}
      </SimpleGrid>
    </Container>
  </Box>
);

export default Footer;
