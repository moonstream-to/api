import React, { useState, useEffect, Suspense, useContext } from "react";
import {
  Flex,
  Heading,
  Text,
  Box,
  Image,
  Button,
  useBreakpointValue,
  Center,
  Fade,
  chakra,
  Stack,
} from "@chakra-ui/react";
import { Grid, GridItem } from "@chakra-ui/react";
import { useUser, useAnalytics, useModals, useRouter } from "../src/core/hooks";
import { getLayout } from "../src/layouts";
import SplitWithImage from "../src/components/SplitWithImage";
import {
  IoAnalyticsSharp,
  IoLogoBitcoin,
  IoSearchSharp,
} from "react-icons/io5";
import ConnectedButtons from "../src/components/ConnectedButtons";
import UIContext from "../src/core/providers/UIProvider/context";

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "4xl", "5xl", "6xl", "7xl"],
};

const TRIPLE_PICS_PROPS = {
  fontSize: ["1xl", "2xl", "2xl", "2xl", "3xl", "3xl"],
  textAlign: "center",
  fontWeight: "600",
  py: 4,
};

const TRIPLE_PICS_TEXT = {
  fontSize: ["lg", "xl", "xl", "xl", "2xl", "3xl"],
  textAlign: "center",
  fontWeight: "400",
  mb: ["2rem", "2rem", "0", null, "0"],
};

const CARD_CONTAINER = {
  className: "CardContainer",
  w: "100%",
  mx: [0, 0, "2rem", null, "4rem"],

  alignSelf: ["center", null, "flex-start"],
};

const IMAGE_CONTAINER = {
  className: "ImageContainer",
  // objectFit: "contain",
  h: ["10rem", null],
  // h: ["10rem", "14rem", "14rem", "15rem", "18rem", "20rem"],
  justifyContent: "center",
};

const AWS_PATH =
  "https://s3.amazonaws.com/static.simiotics.com/moonstream/assets";

const assets = {
  background: `https://s3.amazonaws.com/static.simiotics.com/landing/landing-background-2.png`,
  aviator: `https://s3.amazonaws.com/static.simiotics.com/landing/aviator-2.svg`,
  icon1: `${AWS_PATH}/Image+1.png`,
  icon2: `${AWS_PATH}/Image+2.png`,
  icon3: `${AWS_PATH}/Image+3.png`,
  icon4: `${AWS_PATH}/Image+4.png`,
  icon5: `${AWS_PATH}/Image+5.png`,
  icon6: `${AWS_PATH}/Image+6.png`,
};
const Homepage = () => {
  const ui = useContext(UIContext);
  const router = useRouter();
  const buttonSize = useBreakpointValue({
    base: "md",
    sm: "md",
    md: "md",
    lg: "lg",
    xl: "xl",
    "2xl": "xl",
  });

  const ButtonRadius = "2xl";
  const buttonWidth = ["100%", "100%", "40%", "45%", "45%", "45%"];
  const buttonMinWidth = "10rem";
  const { isInit } = useUser();
  const { withTracking, MIXPANEL_EVENTS } = useAnalytics();

  const { toggleModal } = useModals();
  const [scrollDepth, setScrollDepth] = useState(0);

  const getScrollPrecent = ({ currentTarget }) => {
    const scroll_level =
      (100 * (currentTarget.scrollTop + currentTarget.clientHeight)) /
      currentTarget.scrollHeight;
    return scroll_level;
  };

  const handleScroll = (e) => {
    const currentScroll = Math.ceil(getScrollPrecent(e) / 10);

    if (currentScroll > scrollDepth) {
      withTracking(
        setScrollDepth(currentScroll),
        MIXPANEL_EVENTS.HOMEPAGE_SCROLL_DEPTH,
        scrollDepth
      );
    }
  };

  useEffect(() => {
    if (
      router.nextRouter.asPath !== "/" &&
      router.nextRouter.asPath.slice(0, 2) !== "/?" &&
      router.nextRouter.asPath.slice(0, 2) !== "/#"
    ) {
      router.replace(router.nextRouter.asPath, undefined, {
        shallow: true,
      });
    }
  }, [isInit, router]);

  return (
    <Fade in>
      <Box
        width="100%"
        flexDirection="column"
        onScroll={(e) => handleScroll(e)}
        sx={{ scrollBehavior: "smooth" }}
      >
        <Flex
          direction="column"
          h="auto"
          position="relative"
          w="100%"
          overflow="initial"
        >
          <Suspense fallback={""}></Suspense>

          <Grid templateColumns="repeat(12,1fr)">
            <GridItem px="0" colSpan="12" pb={[1, 2, null, 8]}>
              <chakra.header>
                <Box
                  w="full"
                  h="container.sm"
                  backgroundImage={`url(${assets["background"]})`}
                  bgPos="center"
                  bgSize="cover"
                >
                  <Flex
                    align="center"
                    pos="relative"
                    justify="center"
                    boxSize="full"
                    // bg="blackAlpha.700"
                  >
                    <Stack
                      textAlign="center"
                      alignItems="center"
                      spacing={6}
                      maxW="1220px"
                      px="7%"
                    >
                      <Heading
                        size="xl"
                        fontWeight="semibold"
                        color="white"
                        textTransform="uppercase"
                      >
                        {/* <LoadingDots isActive> */}
                        All the crypto data you care about in a single stream
                        {/* </LoadingDots> */}
                      </Heading>
                      <chakra.span
                        my={12}
                        display="inline-block"
                        color="primary.200"
                        textDecor="underline"
                      >
                        Get all the crypto data you need in a single stream.
                        From pending transactions in the Ethereum transaction
                        pool to Elon Musk’s latest tweets.
                      </chakra.span>
                      <chakra.span
                        display="inline-block"
                        color="primary.300"
                        textDecor="underline"
                      >
                        Access this data through the Moonstream dashboard or API
                      </chakra.span>
                    </Stack>
                  </Flex>
                </Box>
              </chakra.header>
            </GridItem>

            <GridItem
              px="7%"
              colSpan="12"
              pt={["20px", "20px", "100px", null, "120px"]}
              pb={["20px", "56px", null, "184px"]}
              bgSize="cover"
              bgImage={`url(${assets["background"]})`}
            >
              <Heading
                {...HEADING_PROPS}
                textAlign="center"
                pb={[12, 12, 12, null, 48]}
              >
                Data you can add to your stream:
              </Heading>

              <Flex
                direction={["column", null, "row"]}
                flexWrap="nowrap"
                justifyContent={["center", null, "space-evenly"]}
              >
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      objectFit="contain"
                      src={assets["icon2"]}
                      alt="privacy is our prioriy"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Ethereum mined transactions
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}></Text>
                </Box>
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      objectFit="contain"
                      src={assets["icon1"]}
                      alt="live metrics"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Ethereum pending transactions
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}></Text>
                </Box>
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      objectFit="contain"
                      src={assets["icon1"]}
                      alt="live metrics"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Centralized exchanges
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}></Text>
                </Box>

                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      objectFit="contain"
                      src={assets["icon3"]}
                      alt="we make it simple for user"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>Social media posts</Heading>
                  <Text {...TRIPLE_PICS_TEXT}></Text>
                </Box>
              </Flex>
              {/* <Text
                textAlign="center"
                fontSize={["xl", "2xl", "2xl", "3xl", "4xl", "5xl"]}
                fontWeight="600"
                pt={[4, null, 12]}
              >
                We currently support Python, Javascript and Go!
                <br />
                Want us to support other programming languages?{" "}
                <Button
                  size="2xl"
                  colorScheme="primary"
                  variant="link"
                  onClick={() => toggleModal("Integration")}
                >
                  Let us know
                </Button>
              </Text> */}
            </GridItem>
            <GridItem
              px={["7%", "12px", "7%", null, "7%"]}
              colSpan="12"
              pb={[1, 2, null, 8]}
              pt="5.125rem"
              mb="66px"
              bgGradient="linear-gradient(to bottom, #e9eaf4, #efeff7, #f4f4f9, #fafafc, #ffffff)"
              borderRadius="md"
            >
              <Flex
                w="100%"
                direction={["column", "row", "column", null, "column"]}
                flexWrap={["nowrap", "nowrap", "nowrap", null, "nowrap"]}
                // justifyContent="center"
                pb="66px"
              >
                <ConnectedButtons
                  // title={"Are you a..."}
                  title={"You are..."}
                  button1={{
                    label: "Crypto trader",
                    link: "/#cryptoTrader",
                    onClick: null,
                  }}
                  button2={{
                    label: "Algorithmic Fund",
                    link: "/#algoFund",
                    onClick: null,
                  }}
                  button3={{
                    label: "Developer",
                    link: "/#smartDeveloper",
                    onClick: null,
                  }}
                />
              </Flex>
            </GridItem>
            <GridItem
              px="7%"
              colSpan="12"
              pt={["1rem", "1rem", "5.125rem", null, "5.125rem"]}
              pb={["0", "66px", null, "66px"]}
              id="cryptoTrader"
              minH={ui.isMobileView ? "100vh" : null}
            >
              <SplitWithImage
                // cta={"Trader early access"}
                cta={"I want early access!"}
                elementName={"element1"}
                colorScheme="suggested"
                badge={`For crypto traders`}
                title={``}
                body={``}
                bullets={[
                  {
                    text: `Subscribe to the defi contracts you care about`,
                    icon: IoLogoBitcoin,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                  {
                    text: `Make sense of how others are calling these contracts using Moonstream dashboards.
                    `,
                    icon: IoAnalyticsSharp,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                  {
                    text: `Get data directly from the transaction pool through our global network of Ethereum nodes`,
                    icon: IoSearchSharp,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                ]}
                imgURL={assets["icon2"]}
              />
            </GridItem>
            <GridItem
              px="7%"
              colSpan="12"
              pt={["1rem", "1rem", "5.125rem", null, "5.125rem"]}
              pb={["0", "66px", null, "66px"]}
              id="algoFund"
              minH={ui.isMobileView ? "100vh" : null}
            >
              <SplitWithImage
                // cta={"Algoritmic fund early access"}
                cta={"I want early access!"}
                elementName={"element2"}
                mirror={true}
                colorScheme="secondary"
                badge={`For algorithmic funds`}
                //   title={`Get API access to your stream`}
                //   body={`Specify actions.
                //   Something happens on blockchain and we automatically execute for them.
                //  Algorithmic trading on the blockchain`}
                bullets={[
                  {
                    text: `Get API access to your stream`,
                    icon: IoLogoBitcoin,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                  {
                    text: `Set conditions that trigger predefined actions`,
                    icon: IoAnalyticsSharp,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                  {
                    text: `Execute transactions directly on Moonstream nodes`,
                    icon: IoSearchSharp,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                ]}
                imgURL={assets["icon3"]}
              />
            </GridItem>
            <GridItem
              px="7%"
              colSpan="12"
              pt={["1rem", "1rem", "5.125rem", null, "5.125rem"]}
              pb={["0", "66px", null, "66px"]}
              id="smartDeveloper"
              minH={ui.isMobileView ? "100vh" : null}
            >
              <SplitWithImage
                // cta={"Developer early access"}
                cta={"I want early access!"}
                elementName={"element3"}
                colorScheme="primary"
                badge={`For smart contract developers`}
                // title={`Learn how people use your smart contracts`}
                // body={`
                // Connect decentralized application with centralized application
                // Creat Blockchain based web hooks and get full visibility of your smart contracts`}
                bullets={[
                  {
                    text: `See how people use your smart contracts`,
                    icon: IoLogoBitcoin,
                    color: "primary.50",
                    bgColor: "primary.900",
                  },
                  {
                    text: `Set up alerts on suspicious activity`,
                    icon: IoAnalyticsSharp,
                    color: "primary.50",
                    bgColor: "primary.900",
                  },
                  {
                    text: `Register webhooks to connect your off-chain infrastructure`,
                    icon: IoSearchSharp,
                    color: "primary.50",
                    bgColor: "primary.900",
                  },
                ]}
                imgURL={assets["icon6"]}
              />
            </GridItem>
            <GridItem
              placeItems="center"
              w="100%"
              colSpan="12"
              pt={["0", "0", "5.125rem", null, "5.125rem"]}
              pb="120px"
            >
              <Center>
                <Button
                  size="lg"
                  variant="solid"
                  colorScheme="suggested"
                  id="test"
                >
                  Join our waitlist
                </Button>
              </Center>
            </GridItem>
          </Grid>
        </Flex>
        {/* <ConnectElements
          selector=".MoonBadge"
          overlay={100}
          elements={[
            { from: ".element1", to: ".element2" },
            { from: ".element2", to: ".element3" },
            // { from: ".element3", to: ".element4" },
            // { from: ".element5", to: ".element4" },
            // { from: ".element6", to: ".element4" },
            // { from: ".element7", to: ".element4" },
          ]}
        /> */}
      </Box>
    </Fade>
  );
};

export async function getStaticProps() {
  const metaTags = {
    title: "Bugout: Measure the success of your dev tool",
    description:
      "Get usage metrics and crash reports. Improve your users' experience",
    keywords:
      "bugout, bugout-dev, bugout.dev, usage-metrics, analytics, dev-tool ,knowledge, docs, journal, entry, find-anything",
    url: "https://bugout.dev",
    image:
      "https://s3.amazonaws.com/static.simiotics.com/landing/aviator-2.svg",
  };

  const assetPreload = Object.keys(assets).map((key) => {
    return {
      rel: "preload",
      href: assets[key],
      as: "image",
    };
  });
  const preconnects = [
    { rel: "preconnect", href: "https://s3.amazonaws.com" },
    { rel: "preconnect", href: "https://assets.calendly.com/" },
  ];

  const preloads = assetPreload.concat(preconnects);

  return {
    props: { metaTags, preloads },
  };
}

Homepage.layout = "default";
Homepage.getLayout = getLayout;

export default Homepage;
