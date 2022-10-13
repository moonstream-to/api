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
  PRIMARY_MOON_LOGO_URL,
  SITEMAP,
  BACKGROUND_COLOR,
} from "../core/constants";
import { FaGithub, FaTwitter, FaDiscord } from "react-icons/fa";
import moment from "moment";

const LINKS_SIZES = {
  fontWeight: "300",
  fontSize: "md",
};

const ListHeader = ({ children }) => {
  return (
    <Text fontWeight="semibold" fontSize={"md"} mb={2}>
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
    bg={BACKGROUND_COLOR}
    textColor="white"
    borderTop="1px"
    borderColor="white"
  >
    <Container as={Stack} maxW={"8xl"} py={10}>
      <SimpleGrid
        templateColumns={{ sm: "1fr 1fr", md: "2fr 1fr 1fr 1fr 1fr 1fr" }}
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
                src={PRIMARY_MOON_LOGO_URL}
                alt="Go to app root"
              />
            </Link>
          </Box>
          <Text fontSize={"sm"}>
            © {moment().year()} Moonstream.to All rights reserved
          </Text>
        </Stack>
        <Stack>
          <Text fontWeight="semibold">Follow Us</Text>
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
            <SocialButton label={"Discord"} href={"/discordleed"}>
              <FaDiscord />
            </SocialButton>
          </Stack>
        </Stack>
        {Object.values(SITEMAP).map((category, colIndex) => {
          return (
            <Stack align={"flex-start"} key={`footer-list-column-${colIndex}`}>
              <>
                <ListHeader>{category.title}</ListHeader>
                {category.children.map((linkItem, linkItemIndex) => {
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
            </Stack>
          );
        })}
      </SimpleGrid>
    </Container>
  </Box>
);

export default Footer;
