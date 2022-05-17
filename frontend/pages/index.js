import React, { useState, Suspense, useEffect, useLayoutEffect } from "react";
import {
  Fade,
  Flex,
  Heading,
  Box,
  chakra,
  Stack,
  Link,
  Center,
  useMediaQuery,
  Grid,
  Text,
  GridItem,
  SimpleGrid,
  Image as ChakraImage,
  HStack,
  VStack,
} from "@chakra-ui/react";
import useUser from "../src/core/hooks/useUser";
import useRouter from "../src/core/hooks/useRouter";
import { AWS_ASSETS_PATH, DEFAULT_METATAGS } from "../src/core/constants";
import TrustedBadge from "../src/components/TrustedBadge";
import RouteButton from "../src/components/RouteButton";
import MilestoneBox from "../src/components/MilestoneBox";
import mixpanel from "mixpanel-browser";
import { MIXPANEL_EVENTS } from "../src/core/providers/AnalyticsProvider/constants";
import RouterLink from "next/link";

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "5xl", "5xl", "6xl", "7xl"],
};

const assets = {
  background720: `${AWS_ASSETS_PATH}/background720.png`,
  background1920: `${AWS_ASSETS_PATH}/background720.png`,
  background2880: `${AWS_ASSETS_PATH}/background720.png`,
  background3840: `${AWS_ASSETS_PATH}/background720.png`,
  cryptoTraders: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  cointelegraph: `${AWS_ASSETS_PATH}/featured_by/Cointelegraph_logo.png`,
  forte: `${AWS_ASSETS_PATH}/featured_by/forte_logo.png`,
  educativesessions: `${AWS_ASSETS_PATH}/featured_by/educative_logo.png`,
  cryptoinsiders: `${AWS_ASSETS_PATH}/featured_by/crypto_insiders.png`,
  cryptoslate: `${AWS_ASSETS_PATH}/featured_by/cs-media-logo-light.png`,
  cgcConference: `${AWS_ASSETS_PATH}/featured_by/cgc_conference_2022_logo.jpg`,
  lender: `${AWS_ASSETS_PATH}/lender.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
  bc101: `${AWS_ASSETS_PATH}/featured_by/blockchain101_logo.png`,
  laguna: `${AWS_ASSETS_PATH}/featured_by/laguna_logo.svg`,
  game7io: `${AWS_ASSETS_PATH}/featured_by/game7io_logo.png`,
  orangedao: `${AWS_ASSETS_PATH}/featured_by/orangedao_logo.png`,
  meetup: `${AWS_ASSETS_PATH}/featured_by/meetup_logo.png`,
};

const Feature = ({
  title,
  altText,
  path,
  mixpanel_url,
  mixpanel_name,
  image,
}) => {
  return (
    <RouterLink
      href={path}
      onClick={() => {
        if (mixpanel.get_distinct_id()) {
          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
            full_url: mixpanel_url,
            buttonName: mixpanel_name,
            page: `landing`,
            section: `features`,
          });
        }
      }}
    >
      <Stack
        transition={"1s"}
        spacing={1}
        px={1}
        alignItems="center"
        borderRadius="12px"
        borderColor="blue.700"
        bgColor={"blue.800"}
        borderWidth={"1px"}
        _hover={{ transform: "scale(1.05)", transition: "0.42s" }}
        cursor="pointer"
        m={[2, 3, null, 4, 8, 12]}
        pb={2}
      >
        <ChakraImage
          boxSize={["220px", "220px", "xs", null, "xs"]}
          objectFit="contain"
          src={image}
          alt={altText}
        />
        <Heading textAlign="center" fontSize={["md", "md", "lg", "3xl", "4xl"]}>
          {title}
        </Heading>
      </Stack>
    </RouterLink>
  );
};

const Homepage = () => {
  const [background, setBackground] = useState("background720");
  const [backgroundLoaded720, setBackgroundLoaded720] = useState(false);
  const [backgroundLoaded1920, setBackgroundLoaded1920] = useState(false);
  const [backgroundLoaded2880, setBackgroundLoaded2880] = useState(false);
  const [backgroundLoaded3840, setBackgroundLoaded3840] = useState(false);

  const router = useRouter();
  const { isInit } = useUser();
  const [
    isLargerThan720px,
    isLargerThan1920px,
    isLargerThan2880px,
    isLargerThan3840px,
  ] = useMediaQuery([
    "(min-width: 720px)",
    "(min-width: 1920px)",
    "(min-width: 2880px)",
    "(min-width: 3840px)",
  ]);

  useEffect(() => {
    assets["background720"] = `${AWS_ASSETS_PATH}/background720.png`;
    assets["background1920"] = `${AWS_ASSETS_PATH}/background1920.png`;
    assets["background2880"] = `${AWS_ASSETS_PATH}/background2880.png`;
    assets["background3840"] = `${AWS_ASSETS_PATH}/background3840.png`;
  }, []);

  useLayoutEffect(() => {
    if (backgroundLoaded3840) {
      setBackground("background3840");
    } else if (backgroundLoaded2880) {
      setBackground("background2880");
    } else if (backgroundLoaded1920) {
      setBackground("background1920");
    } else {
      setBackground("background720");
    }
  }, [
    isLargerThan720px,
    isLargerThan1920px,
    isLargerThan2880px,
    isLargerThan3840px,
    backgroundLoaded720,
    backgroundLoaded1920,
    backgroundLoaded2880,
    backgroundLoaded3840,
  ]);

  useEffect(() => {
    if (
      router.nextRouter.asPath !== "/" &&
      router.nextRouter.asPath.slice(0, 2) !== "/?" &&
      router.nextRouter.asPath.slice(0, 2) !== "/#" &&
      router.nextRouter.asPath.slice(0, 11) !== "/index.html"
    ) {
      console.warn("redirect attempt..");
      if (typeof window !== "undefined") {
        console.warn("window present:", window.location.pathname);
        router.replace(router.nextRouter.asPath, router.nextRouter.asPath, {
          shallow: false,
        });
      }
    }
  }, [isInit, router]);

  useLayoutEffect(() => {
    const imageLoader720 = new Image();
    imageLoader720.src = `${AWS_ASSETS_PATH}/background720.png`;
    imageLoader720.onload = () => {
      setBackgroundLoaded720(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader1920 = new Image();
    imageLoader1920.src = `${AWS_ASSETS_PATH}/background1920.png`;
    imageLoader1920.onload = () => {
      setBackgroundLoaded1920(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader2880 = new Image();
    imageLoader2880.src = `${AWS_ASSETS_PATH}/background2880.png`;
    imageLoader2880.onload = () => {
      setBackgroundLoaded2880(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader3840 = new Image();
    imageLoader3840.src = `${AWS_ASSETS_PATH}/background3840.png`;
    imageLoader3840.onload = () => {
      setBackgroundLoaded3840(true);
    };
  }, []);

  return (
    <Suspense fallback="">
      <Fade in>
        <Box
          width="100%"
          flexDirection="column"
          sx={{ scrollBehavior: "smooth" }}
          bgSize="cover"
          id="page:landing"
          bgColor={"blue.50"}
        >
          <Flex
            direction="column"
            h="auto"
            position="relative"
            w="100%"
            overflow="initial"
            pt={0}
          >
            <Suspense fallback={""}></Suspense>

            <Grid
              templateColumns="repeat(12,1fr)"
              mt={0}
              border="none"
              boxSizing="content-box"
            >
              <GridItem
                mt={0}
                mb={0}
                px="0"
                colSpan="12"
                minH="100vh"
                bgColor={"blue.50"}
                id="Header grid item"
              >
                <chakra.header boxSize="full" minH="100vh" mb={0}>
                  <Box
                    bgPos="bottom"
                    bgColor="transparent"
                    backgroundImage={`url(${assets[`${background}`]})`}
                    bgSize="cover"
                    boxSize="full"
                    minH="100vh"
                  >
                    <Flex align="center" justify="center" boxSize="full">
                      <Stack
                        textAlign="center"
                        alignItems="center"
                        spacing={6}
                        maxW={["1620px", null, null, null, "1620px", "2222px"]}
                        w="100%"
                        px="7%"
                        h="100%"
                        pt={["10vh", null, "20vh"]}
                      >
                        <Heading
                          fontSize={["lg", "4xl", "5xl", "5xl", "5xl", "6xl"]}
                          fontWeight="semibold"
                          color="white"
                        >
                          Build a Sustainable Game Economy in only a few clicks
                        </Heading>
                        <chakra.span
                          pt={4}
                          pb={4}
                          my={12}
                          fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
                          display="inline-block"
                          color="white"
                        >
                          Moonstream Engine empowers web3 game designers to grow
                          healthy economies. Moonstream smart contracts and APIs
                          allow you to integrate our game mechanics with zero
                          effort.
                        </chakra.span>
                        <RouteButton
                          variant="orangeAndBlue"
                          minW={[
                            "200px",
                            "250px",
                            "250px",
                            "300px",
                            "350px",
                            "400px",
                          ]}
                          fontSize={["lg", "xl", "2xl", "3xl", "4xl", "4xl"]}
                          onClick={() => {
                            if (mixpanel.get_distinct_id()) {
                              mixpanel.track(
                                `${MIXPANEL_EVENTS.BUTTON_CLICKED}`,
                                {
                                  full_url: router.nextRouter.asPath,
                                  buttonName: `Join our Discord`,
                                  page: `landing`,
                                  section: `front-and-center`,
                                }
                              );
                            }
                          }}
                          href={"/discordleed"}
                          isExternal
                        >
                          Join our Discord
                        </RouteButton>
                      </Stack>
                    </Flex>
                  </Box>
                </chakra.header>
              </GridItem>

              <GridItem
                px="7%"
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="white.100"
                minH="100vh"
              >
                <VStack align="center" justify="center" boxSize="full">
                  <Heading
                    fontSize={["lg", "4xl", "5xl", "5xl", "5xl", "6xl"]}
                    fontWeight="semibold"
                  >
                    Major Milestones
                  </Heading>
                  <Flex wrap="wrap" direction="row" justifyContent="center">
                    <MilestoneBox headingText="$3B transaction volume" />
                    <MilestoneBox headingText="22,000 active users" />
                  </Flex>
                  <Text
                    textAlign="center"
                    fontSize={["md", "xl", "2xl", "3xl", "3xl", "3xl"]}
                  >
                    And growing...
                  </Text>
                  <chakra.h2
                    fontSize={{ base: "3xl", sm: "2xl" }}
                    textAlign="center"
                    pb={4}
                    pt={16}
                    fontWeight="bold"
                  >
                    Trusted by{" "}
                  </chakra.h2>
                  <Flex wrap="wrap" direction="row" justifyContent="center">
                    <Suspense fallback={""}>
                      <TrustedBadge
                        scale={1.5}
                        name="Laguna games"
                        caseURL=""
                        ImgURL={assets["laguna"]}
                        boxURL="https://laguna.games/"
                        bgColor="blue.900"
                      />
                      <TrustedBadge
                        scale={1.5}
                        name="game7io"
                        ImgURL={assets["game7io"]}
                        boxURL="https://game7.io/"
                        bgColor="blue.900"
                      />

                      <TrustedBadge
                        scale={1.5}
                        name="orangedao"
                        ImgURL={assets["orangedao"]}
                        boxURL="https://lfg.orangedao.xyz/"
                        bgColor="blue.900"
                      />
                      <TrustedBadge
                        scale={1.5}
                        name="forte"
                        ImgURL={assets["forte"]}
                        boxURL="https://www.forte.io/"
                        bgColor="blue.900"
                        invertColors={true}
                      />
                    </Suspense>
                  </Flex>
                </VStack>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                colSpan="12"
                pt={24}
                minH="100vh"
                bgColor={"blue.900"}
                textColor="white"
              >
                <Heading
                  {...HEADING_PROPS}
                  textAlign="center"
                  pb={[3, 12, null]}
                  pt={0}
                >
                  Features
                </Heading>
                <Grid
                  templateColumns={{
                    base: "repeat(1, 1fr)",
                    sm: "repeat(1, 1fr)",
                    md: "repeat(2, 1fr)",
                  }}
                  gap={4}
                >
                  <GridItem>
                    <Flex>
                      <chakra.span
                        fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                        display="inline-block"
                        color="white"
                      >
                        Lootboxes, crafting recipes, deck building, you name it!
                        <br />
                        <br />
                        With Moonstream Engine you can deploy on-chain mechanics
                        with one click.
                        <br />
                        <br />
                        Read our Use Cases or explore the features to know more.
                      </chakra.span>
                    </Flex>
                  </GridItem>
                  <GridItem>
                    <Center w="100%" h="100%">
                      <RouteButton
                        variant="orangeAndBlue"
                        minW={[
                          "200px",
                          "250px",
                          "250px",
                          "300px",
                          "350px",
                          "400px",
                        ]}
                        fontSize={["lg", "xl", "2xl", "3xl", "4xl", "4xl"]}
                        px={[4, 4, 4, 8, 8]}
                        onClick={() => {
                          if (mixpanel.get_distinct_id()) {
                            mixpanel.track(
                              `${MIXPANEL_EVENTS.BUTTON_CLICKED}`,
                              {
                                full_url: router.nextRouter.asPath,
                                buttonName: `Explore the Use Cases`,
                                page: `landing`,
                                section: `Dive into Engine Features`,
                              }
                            );
                          }
                        }}
                        href="https://docs.google.com/document/d/1mjfF8SgRrAZvtCVVxB2qNSUcbbmrH6dTEYSMfHKdEgc/preview"
                        isExternal
                      >
                        Explore the Use Cases
                      </RouteButton>
                    </Center>
                  </GridItem>
                </Grid>
                <SimpleGrid
                  columns={[1, 2, 2, 4, null, 4]}
                  justifyContent="center"
                  w="100%"
                  placeContent={"space-between"}
                  mx={[0, -2, -4]}
                  paddingTop="20px"
                >
                  <Feature
                    title="Lootboxes"
                    altText="Lootboxes"
                    path="/features/#lootboxes"
                    mixpanel_name="lootboxes"
                    mixpanel_url={router.nextRouter.asPath}
                    image={assets["cryptoTraders"]}
                  />
                  <Feature
                    title="Crafting Recipes"
                    altText="Crafting Recipes"
                    path="/features/#crafting"
                    mixpanel_name="crafting"
                    mixpanel_url={router.nextRouter.asPath}
                    image={assets["NFT"]}
                  />
                  <Feature
                    title="Minigames"
                    altText="Minigames"
                    path="/features/#minigames"
                    mixpanel_name="minigames"
                    mixpanel_url={router.nextRouter.asPath}
                    image={assets["DAO"]}
                  />
                  <Feature
                    title="Airdrops"
                    altText="Airdrops"
                    path="/features/#airdrops"
                    mixpanel_name="airdrops"
                    mixpanel_url={router.nextRouter.asPath}
                    image={assets["lender"]}
                  />
                </SimpleGrid>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="white.100"
                minH="100vh"
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                  Our Workflow
                </Heading>
                <HStack alignItems="top" py={5}>
                  <Flex height="100%" width="25%">
                    <Heading
                      as="h2"
                      fontSize={["lg", "3xl", "4xl", "4xl", "4xl", "5xl"]}
                      display="inline-block"
                      fontWeight="semibold"
                    >
                      Step 1:
                    </Heading>
                  </Flex>
                  <Flex height="100%" width="75%">
                    <chakra.span
                      fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                      display="inline-block"
                    >
                      So you decided to build a healthy economy on the
                      blockchain. You are on the right path, traveler!
                    </chakra.span>
                  </Flex>
                </HStack>
                <HStack alignItems="top" py={5}>
                  <Flex bgColor="grey.100" width="25%" height="100%">
                    <Heading
                      as="h2"
                      fontSize={["lg", "3xl", "4xl", "4xl", "4xl", "5xl"]}
                      display="inline-block"
                      fontWeight="semibold"
                    >
                      Step 2:
                    </Heading>
                  </Flex>
                  <Flex width="75%">
                    <chakra.span
                      fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                      display="inline-block"
                    >
                      <Link href="/discordleed" isExternal>
                        <Text
                          as="u"
                          display="inline"
                          fontWeight="semibold"
                          onClick={() => {
                            if (mixpanel.get_distinct_id()) {
                              mixpanel.track(
                                `${MIXPANEL_EVENTS.BUTTON_CLICKED}`,
                                {
                                  full_url: router.nextRouter.asPath,
                                  buttonName: `Join our Discord`,
                                  page: `landing`,
                                  section: `bottom-line`,
                                }
                              );
                            }
                          }}
                        >
                          Join our Discord
                        </Text>
                      </Link>{" "}
                      to get in touch with the team (@zomglings). Tell us about
                      your game and schedule a call if needed.
                    </chakra.span>
                  </Flex>
                </HStack>
                <HStack alignItems="top" py={5}>
                  <Flex bgColor="grey.100" width="25%" height="100%">
                    <Heading
                      as="h2"
                      fontSize={["lg", "3xl", "4xl", "4xl", "4xl", "5xl"]}
                      display="inline-block"
                      fontWeight="semibold"
                    >
                      Step 3:
                    </Heading>
                  </Flex>
                  <Flex width="75%">
                    <chakra.span
                      fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                      display="inline-block"
                    >
                      Pick game mechanics that you&apos;d like to deploy.
                      Moonstream Engine provides you with back-end tools to put
                      them on the blockchain.
                      <br />
                      <br />
                      You&apos;re at the end of your development journey now,
                      traveler. Time to watch your game economy grow!
                    </chakra.span>
                  </Flex>
                </HStack>
              </GridItem>
              <GridItem
                px="7%"
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="blue.900"
                textColor="white"
                minH="100vh"
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                  Featured by{" "}
                </Heading>
                <Center>
                  <Flex
                    width="81%"
                    wrap="wrap"
                    direction="row"
                    justifyContent="center"
                    bgColor="white"
                  >
                    <Suspense fallback={""}>
                      <TrustedBadge
                        name="cointelegraph"
                        caseURL=""
                        ImgURL={assets["cointelegraph"]}
                        boxURL="https://cointelegraph.com/news/17-of-addresses-snapped-up-80-of-all-ethereum-nfts-since-april"
                      />
                      <TrustedBadge
                        name="CryptoInsiders"
                        ImgURL={assets["cryptoinsiders"]}
                        boxURL="https://www.crypto-insiders.nl/nieuws/altcoin/17-van-ethereum-whales-bezitten-meer-dan-80-van-alle-nfts-op-de-blockchain/"
                      />
                      <TrustedBadge
                        name="cryptoslate"
                        ImgURL={assets["cryptoslate"]}
                        boxURL="https://cryptoslate.com/should-investors-care-80-of-all-nfts-belong-to-17-of-addresses/"
                      />
                      <TrustedBadge
                        name="educative sessions"
                        scale={1.5}
                        ImgURL={assets["educativesessions"]}
                        boxURL="https://youtu.be/DN8zRzJuy0M"
                      />
                      <TrustedBadge
                        scale={1.5}
                        name="bc101"
                        ImgURL={assets["bc101"]}
                        boxURL="https://blockchain101.com/"
                      />
                      <TrustedBadge
                        scale={1.5}
                        name="bc101"
                        ImgURL={assets["meetup"]}
                        boxURL="https://www.meetup.com/SF-Bay-Area-Data-Science-Initiative/events/283215538/"
                      />
                      <TrustedBadge
                        scale={1.5}
                        name="cgc2022"
                        ImgURL={assets["cgcConference"]}
                        boxURL="https://www.cgc.one/"
                      />
                    </Suspense>
                  </Flex>
                </Center>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="white"
                minH="100vh"
              >
                <Flex
                  w="100%"
                  alignItems="center"
                  justifyContent="center"
                  direction={["column", "column", "row"]}
                  maxW="1024px"
                >
                  <chakra.span
                    display="block"
                    my={12}
                    fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                    textAlign={["justify", "left", null]}
                    mr={[0, 12, 14]}
                    letterSpacing="tight"
                  >
                    {`Contact us on Discord to discuss your project and keep up with the latest updates on Moonstream Engine.`}
                  </chakra.span>

                  <RouteButton
                    variant="orangeAndBlue"
                    minW={[
                      "200px",
                      "250px",
                      "250px",
                      "300px",
                      "350px",
                      "400px",
                    ]}
                    fontSize={["lg", "xl", "2xl", "3xl", "4xl", "4xl"]}
                    onClick={() => {
                      if (mixpanel.get_distinct_id()) {
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          full_url: router.nextRouter.asPath,
                          buttonName: `Join our Discord`,
                          page: `landing`,
                          section: `bottom-line`,
                        });
                      }
                    }}
                    href={"/discordleed"}
                    isExternal
                  >
                    Join our Discord
                  </RouteButton>
                </Flex>
              </GridItem>
            </Grid>
          </Flex>
        </Box>
      </Fade>
    </Suspense>
  );
};

export async function getStaticProps() {
  const assetPreload = Object.keys(assets).map((key) => {
    return {
      rel: "preload",
      href: assets[key],
      as: "image",
    };
  });
  const preconnects = [{ rel: "preconnect", href: "https://s3.amazonaws.com" }];

  const preloads = assetPreload.concat(preconnects);

  return {
    props: { metaTags: DEFAULT_METATAGS, preloads },
  };
}

export default Homepage;
