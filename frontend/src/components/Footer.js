import React, { useContext } from "react";
import {
  Text,
  Link,
  Box,
  Container,
  Stack,
  Image as ChakraImage,
  useColorModeValue,
  VisuallyHidden,
  chakra,
  Flex,
  Spacer,
} from "@chakra-ui/react";
import RouterLink from "next/link";
import {
  PRIMARY_MOON_LOGO_URL,
  SITEMAP,
  BACKGROUND_COLOR,
  PAGETYPE,
} from "../core/constants";
import moment from "moment";
import { AWS_ASSETS_PATH } from "../core/constants";
import UIContext from "../core/providers/UIProvider/context";
import AnalyticsContext from "../core/providers/AnalyticsProvider/context";

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
  const { buttonReport } = useContext(AnalyticsContext);
  return (
    <chakra.button
      bg={useColorModeValue("blackAlpha.100", "whiteAlpha.100")}
      rounded={"full"}
      cursor={"pointer"}
      onClick={() => {
        buttonReport(label, "footer", "landing");
        window.open(href);
      }}
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

const Footer = () => {
  const ui = useContext(UIContext);
  return (
    <Box
      bg={BACKGROUND_COLOR}
      textColor="white"
      borderTop="1px"
      borderColor="white"
      px="7%"
      mx="auto"
    >
      <Container as={Stack} py={10} px="0px" maxW="1238px">
        <Flex direction={["column", "column", "row"]}>
          <Stack spacing={6}>
            <Box pb={ui.isMobileView ? "40px" : "0px"}>
              <Link href="/" alignSelf="center">
                <ChakraImage
                  alignSelf="center"
                  w="160px"
                  src={PRIMARY_MOON_LOGO_URL}
                  alt="Go to app root"
                />
              </Link>
            </Box>
            {!ui.isMobileView && (
              <>
                <Flex justifyContent="start">
                  <Link href="/privacy-policy">Privacy policy</Link>
                  <Link href="/tos" ml="20px">
                    Terms of Service
                  </Link>
                </Flex>
                <Text fontSize={"sm"}>
                  © {moment().year()} Moonstream.to
                  All&nbsp;rights&nbsp;reserved
                </Text>
              </>
            )}
          </Stack>
          <Spacer />
          <Flex
            direction="column"
            pb={ui.isMobileView ? "40px" : "0px"}
            ml={["0px", "0px", "5vw", "100px"]}
          >
            <Text fontWeight="semibold" mb="20px">
              Follow Us
            </Text>
            <Flex width="158px" justifyContent="space-between">
              <SocialButton label={"Discord"} href={"/discordleed"}>
                <ChakraImage
                  w="26px"
                  src={`${AWS_ASSETS_PATH}/icons/discord-logo.png`}
                />
              </SocialButton>
              <SocialButton
                label={"Twitter"}
                href={"https://twitter.com/moonstreamto"}
              >
                <ChakraImage
                  w="24px"
                  size={1}
                  src={`${AWS_ASSETS_PATH}/icons/twitter-logo.png`}
                />
              </SocialButton>
              <SocialButton
                label={"Github"}
                href={"https://github.com/bugout-dev/moonstream"}
              >
                <ChakraImage
                  w="24px"
                  src={`${AWS_ASSETS_PATH}/icons/github-logo.png`}
                />
              </SocialButton>
              <SocialButton
                label={"LinkedIn"}
                href={"https://www.linkedin.com/company/moonstream/"}
              >
                <ChakraImage
                  w="24px"
                  src={`${AWS_ASSETS_PATH}/icons/linkedin-logo.png`}
                />
              </SocialButton>
            </Flex>
          </Flex>
          <Flex
            justifyContent="space-between"
            pb={ui.isMobileView ? "40px" : "0px"}
          >
            {Object.values(SITEMAP).map((category, colIndex) => {
              return (
                <Stack
                  ml={["0px", "0px", "5vw", "100px"]}
                  align={"flex-start"}
                  key={`footer-list-column-${colIndex}`}
                >
                  <>
                    <ListHeader>{category.title}</ListHeader>
                    {category.children.map((linkItem, linkItemIndex) => {
                      return (
                        <RouterLink
                          passHref
                          href={linkItem.path}
                          key={`footer-list-link-item-${linkItemIndex}-col-${colIndex}`}
                        >
                          <Link
                            {...LINKS_SIZES}
                            target={
                              linkItem.type === PAGETYPE.EXTERNAL
                                ? "_blank"
                                : "_self"
                            }
                          >
                            {linkItem.title}
                          </Link>
                        </RouterLink>
                      );
                    })}
                  </>
                </Stack>
              );
            })}
          </Flex>
          {ui.isMobileView && (
            <Text fontSize={"sm"}>
              © {moment().year()} Moonstream.to All&nbsp;rights&nbsp;reserved
            </Text>
          )}
        </Flex>
      </Container>
    </Box>
  );
};

export default Footer;
