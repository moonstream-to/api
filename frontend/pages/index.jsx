import React, { useState, useEffect, Suspense } from "react";
import {
  Flex,
  Heading,
  Text,
  Box,
  Image,
  ListItem,
  Button,
  Link,
  ListIcon,
  List,
  useBreakpointValue,
  Center,
  Fade,
} from "@chakra-ui/react";
import { Grid, GridItem } from "@chakra-ui/react";
import { useUser, useAnalytics, useModals, useRouter } from "../src/core/hooks";
import { openPopupWidget, InlineWidget } from "react-calendly";
import TrustedBadge from "../src/components/TrustedBadge"
import { getLayout } from "../src/layouts";

const TEXT_PROPS = {
  fontSize: ["lg", null, "xl"],
  fontWeight: "600",
};

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "4xl", "5xl", "6xl", "7xl"],
};

const TITLE_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "5xl", "5xl", "6xl", "120px"],
};

const TRIPLE_PICS_PROPS = {
  fontSize: ["2xl", "3xl", "3xl", "3xl", "4xl", "4xl"],
  textAlign: "center",
  fontWeight: "500",
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
  h: ["10rem", "14rem", "14rem", "15rem", "18rem", "20rem"],
  justifyContent: "center",
};

const AWS_PATH = "https://s3.amazonaws.com/static.simiotics.com/landing";

const assets = {
  background: `${AWS_PATH}/landing-background-2.png`,
  aviator: `${AWS_PATH}/aviator-2.svg`,
  icon1: `${AWS_PATH}/v2/Icon+1.svg`,
  icon2: `${AWS_PATH}/v2/Icon+2.svg`,
  icon3: `${AWS_PATH}/v2/Icon+3.svg`,
  icon4: `${AWS_PATH}/v2/Icon+4.svg`,
  icon5: `${AWS_PATH}/v2/Icon+5.svg`,
  icon6: `${AWS_PATH}/v2/Icon+6.svg`,
  activeloopLogo: `${AWS_PATH}/activeloop.svg`,
  aiIncubeLogo: `${AWS_PATH}/ai incube.svg`,
  b612Logo: `${AWS_PATH}/b612.svg`,
  harvardLogo: `${AWS_PATH}/harvard.svg`,
  mattermarkLogo: `${AWS_PATH}/mattermark.svg`,
  mixrankLogo: `${AWS_PATH}/mixrank.svg`,
  toolchainLogo: `${AWS_PATH}/toolchain.svg`,
};
const Homepage = () => {
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

  const DoubleCTAButton = () => (
    <Flex
      justifyContent="flex-start"
      // mt={20}
      flexWrap="wrap"
      width="100%"
    >
      <Button
        variant="solid"
        w={buttonWidth}
        minW={buttonMinWidth}
        borderRadius={ButtonRadius}
        colorScheme="secondary"
        size={buttonSize}
        onClick={() => toggleModal("register")}
        mr="1.25rem"
        color="white"
        border="2px solid #D35725"
        fontWeight="400"
      >
        Sign up for free
      </Button>

      <Suspense fallback={""}>
        <Button
          variant="outline"
          colorScheme="gray"
          color="black"
          borderRadius={ButtonRadius}
          w={buttonWidth}
          minW={buttonMinWidth}
          mr="1.25rem"
          size={buttonSize}
          fontWeight="400"
          onClick={() => {
            openPopupWidget({
              url: "https://calendly.com/neeraj-simiotics/bugout-30",
            });
          }}
        >
          Book office hours
        </Button>
      </Suspense>
    </Flex>
  );

  useEffect(() => {
    if (
      router.nextRouter.asPath !== "/" &&
      router.nextRouter.asPath.slice(0, 2) !== "/?"
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
            <GridItem px="7%" colSpan="12" pb={[1, 2, null, 8]}>
              <Flex w="100%" wrap="wrap">
                <Flex
                  direction="column"
                  alignItems="left"
                  pr={[0, null, 24]}
                  flexBasis="300px"
                  flexGrow={1}
                >
                  <Heading
                    pt={["2rem", "3rem", "3rem", "10rem", "12rem", "14rem"]}
                    {...TITLE_PROPS}
                    mb={3}
                    fontWeight="700"
                  >
                    Measure the success of your dev tool
                  </Heading>
                  <Text
                    fontSize={["3xl", "4xl", "3xl", "4xl", "5xl", "6xl"]}
                    pb={[0, 0, 0, 0, 0, "3rem"]}
                    mb={20}
                    fontWeight="600"
                    color="primary.1000"
                    lineHeight="100%"
                  >
                    Get usage metrics and crash reports <br />{" "}
                    {`Improve your
                    users' experience`}
                  </Text>
                  <DoubleCTAButton />
                </Flex>
                <Flex flexBasis="200px" flexGrow={1} flexShrink={1}>
                  <Image
                    rel="preconnect"
                    src={assets["aviator"]}
                    alt="Bugout is on the fly to report your crashes"
                  />
                </Flex>
              </Flex>
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
                See what your users are experiencing with your library, API, or
                command line tool
              </Heading>

              <Flex
                direction={["column", null, "row"]}
                flexWrap="nowrap"
                justifyContent={["center", null, "space-evenly"]}
              >
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      w="100%"
                      src={assets["icon2"]}
                      alt="privacy is our prioriy"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Catch and fix bugs faster
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    Learn about errors as they occur, with full stack traces.
                  </Text>
                </Box>
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image w="100%" src={assets["icon1"]} alt="live metrics" />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Understand your user engagement and retention
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    Learn how users are using your tool, and how frequently.
                  </Text>
                </Box>

                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      w="100%"
                      src={assets["icon3"]}
                      alt="we make it simple for user"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Inform your product roadmap
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    Understand which features people are actually using.
                  </Text>
                </Box>
              </Flex>
              <Text
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
              </Text>
            </GridItem>
            <GridItem px="7%" colSpan="12" pt="5.125rem" pb="66px">
              <Heading {...HEADING_PROPS} textAlign="center" pb={12}>
                Engage with your users on a deeper level
              </Heading>

              <Flex
                direction={["column", null, "row"]}
                flexWrap="nowrap"
                justifyContent={["center", null, "space-evenly"]}
              >
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image w="100%" src={assets["icon4"]} alt="live metrics" />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>Live dashboards</Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    See your users’ journeys as they happen
                  </Text>
                </Box>
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      w="100%"
                      src={assets["icon5"]}
                      alt="privacy is our prioriy"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>GDPR compliance</Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    Automatically handle GDPR-related user requests
                  </Text>
                </Box>
                <Box {...CARD_CONTAINER}>
                  <Flex {...IMAGE_CONTAINER}>
                    <Image
                      w="100%"
                      src={assets["icon6"]}
                      alt="we make it simple for user"
                    />
                  </Flex>
                  <Heading {...TRIPLE_PICS_PROPS}>
                    Simple user consent flows
                  </Heading>
                  <Text {...TRIPLE_PICS_TEXT}>
                    Define principled user consent flows in only a few lines of
                    code.
                  </Text>
                </Box>
              </Flex>
              <Center>
                <Flex
                  m={0}
                  mt="120px"
                  flexWrap="wrap"
                  width="100%"
                  w={["360px", "360px", "500px", null, "800px"]}
                >
                  <Button
                    variant="solid"
                    w={buttonWidth}
                    minW="14rem"
                    borderRadius={ButtonRadius}
                    colorScheme="secondary"
                    size={buttonSize}
                    onClick={() => toggleModal("register")}
                    mr="1.25rem"
                    color="white"
                    border="2px solid #D35725"
                    fontWeight="400"
                  >
                    Sign up for free
                  </Button>

                  <Button
                    variant="outline"
                    colorScheme="gray"
                    color="black"
                    borderRadius={ButtonRadius}
                    w={buttonWidth}
                    minW="14rem"
                    mr="1.25rem"
                    size={buttonSize}
                    fontWeight="400"
                    onClick={() => {
                      openPopupWidget({
                        url: "https://calendly.com/neeraj-simiotics/bugout-30",
                      });
                    }}
                  >
                    Book office hours
                  </Button>
                </Flex>
              </Center>
            </GridItem>
            <GridItem
              px="7%"
              colSpan="12"
              pt="66px"
              bgColor="primary.50"
              pb={["20px", "30px", "92px", null, "92px", "196px"]}
            >
              <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                Loved by proactive teams{" "}
                <span role="img" aria-label="heart">
                  &#128153;
                </span>
              </Heading>
              <Flex wrap="wrap" direction="row" justifyContent="center">
                <Suspense fallback={""}>
                  <TrustedBadge
                    name="activeloop"
                    caseURL="/case-studies/activeloop"
                    ImgURL={assets["activeloopLogo"]}
                  />
                  <TrustedBadge
                    name="ai incube"
                    ImgURL={assets["aiIncubeLogo"]}
                  />
                  <TrustedBadge name="b612" ImgURL={assets["b612Logo"]} />
                  <TrustedBadge name="harvard" ImgURL={assets["harvardLogo"]} />
                  <TrustedBadge
                    name="mattermark"
                    ImgURL={assets["mattermarkLogo"]}
                  />
                  <TrustedBadge name="mixrank" ImgURL={assets["mixrankLogo"]} />
                  <TrustedBadge
                    name="toolchain"
                    ImgURL={assets["toolchainLogo"]}
                  />
                </Suspense>
              </Flex>
            </GridItem>
            <GridItem px="7%" colSpan="12" py={24}>
              <Heading textAlign="center" {...HEADING_PROPS} pb={8}>
                Ready to learn more?
              </Heading>
              <Text textAlign="center" {...TEXT_PROPS}>
                Book office hours with Neeraj Kashyap (
                <Link
                  color="primary.500"
                  isExternal
                  href="https://github.com/zomglings"
                >
                  @zomglings
                </Link>
                ), CEO of Bugout
              </Text>
            </GridItem>

            <GridItem px="7%" colSpan="12"></GridItem>
          </Grid>
          <Flex
            bg="primary.1200"
            direction={["column", null, "row"]}
            w="100%"
            py="2rem"
            px="7%"
            h="100%"
          >
            <Flex
              w={["100%", null, "50%"]}
              textColor="white.200"
              direction="column"
              pr={[0, 0, 12, null, 12]}
            >
              <Heading
                fontSize={["xl", "3xl", null, "3xl", "5xl", "5xl"]}
                fontWeight="500"
                alignSelf="left"
                pt={[4, 4, 24, null, 24]}
                pb={[6, 6, 12, null, 16]}
              >
                {`Let's talk about:`}
              </Heading>
              <List
                fontWeight="400"
                fontSize={["md", null, "2xl", "2xl", "3xl", "4xl"]}
                alignSelf="center"
                spacing={[4, 4, 8, null, 8]}
              >
                <ListItem>
                  <ListIcon as={() => "- "} />
                  How to measure and improve the quality of your users’
                  experience
                </ListItem>
                <ListItem>
                  <ListIcon as={() => "- "} />
                  Ethical data collection
                </ListItem>
                <ListItem>
                  <ListIcon as={() => "- "} />
                  Developer tools best practices, pulling from our experience at
                  OpenAI and Google (TensorFlow, Kubeflow, Google Cloud)
                </ListItem>
              </List>
              <Heading
                fontSize={["xl", "3xl", null, "3xl", "5xl", "5xl"]}
                fontWeight="500"
                pt={[4, null, 8, 16, 24]}
              >
                Book now &#8594;
              </Heading>
            </Flex>
            <Flex className="CalendlyWrapper" w={["100%", null, "45%"]}>
              <InlineWidget
                styles={{
                  width: "100%",
                  height: "720px",
                }}
                hid
                url="https://calendly.com/neeraj-simiotics/bugout-30?hide_event_type_details=1"
              />
            </Flex>
          </Flex>

          <Grid px="7%" templateColumns="repeat(12,1fr)">
            <GridItem colSpan="4" py={2}>
              &nbsp;
            </GridItem>
            <GridItem colSpan="4" py={2}>
              <Center>
                <iframe
                  title="substack"
                  src="https://bugout.substack.com/embed"
                  width="480"
                  height="320"
                  frameBorder="0"
                  scrolling="no"
                ></iframe>
              </Center>
            </GridItem>
            <GridItem colSpan="4" py={2}>
              &nbsp;
            </GridItem>
          </Grid>
        </Flex>
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
