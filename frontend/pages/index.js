import React, {
  useState,
  Suspense,
  useEffect,
  useLayoutEffect,
  useContext,
} from "react";
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
  Accordion,
} from "@chakra-ui/react";
import useUser from "../src/core/hooks/useUser";
import useRouter from "../src/core/hooks/useRouter";
import { AWS_ASSETS_PATH, DEFAULT_METATAGS } from "../src/core/constants";
import TrustedBadge from "../src/components/TrustedBadge";
import RouteButton from "../src/components/RouteButton";
import AnalyticsContext from "../src/core/providers/AnalyticsProvider/context";
import RouterLink from "next/link";
import FAQCard from "../src/components/FAQCard";
import EngineOverviewDiagram from "../src/components/EngineOverviewDiagram";

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "5xl", "5xl", "6xl", "7xl"],
};

const assets = {
  arbitrum: `${AWS_ASSETS_PATH}/arbitrum_logo.png`,
  background720: `${AWS_ASSETS_PATH}/background720.png`,
  background1920: `${AWS_ASSETS_PATH}/background720.png`,
  background2880: `${AWS_ASSETS_PATH}/background720.png`,
  background3840: `${AWS_ASSETS_PATH}/background720.png`,
  bc101: `${AWS_ASSETS_PATH}/featured_by/blockchain101_logo.png`,
  bulliverse: `${AWS_ASSETS_PATH}/bullieverse_logo.png`,
  cgcConference: `${AWS_ASSETS_PATH}/featured_by/cgc_conference_2022_logo.jpg`,
  cointelegraph: `${AWS_ASSETS_PATH}/featured_by/Cointelegraph_logo.png`,
  cryptoGuilds: `${AWS_ASSETS_PATH}/crypto_guilds_logo.png`,
  cryptoinsiders: `${AWS_ASSETS_PATH}/featured_by/crypto_insiders.png`,
  cryptoslate: `${AWS_ASSETS_PATH}/featured_by/cs-media-logo-light.png`,
  cryptoTraders: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  cryptoUnicorns: `${AWS_ASSETS_PATH}/crypto_unicorns_logo.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  educativesessions: `${AWS_ASSETS_PATH}/featured_by/educative_logo.png`,
  ethereum_blockchain: `${AWS_ASSETS_PATH}/ethereum_blockchain_logo.png`,
  evmos: `${AWS_ASSETS_PATH}/evmos_logo.png`,
  forte: `${AWS_ASSETS_PATH}/forte_logo.png`,
  game7io: `${AWS_ASSETS_PATH}/featured_by/game7io_logo.png`,
  gnosis: `${AWS_ASSETS_PATH}/gnosis_chain_logo.png`,
  laguna: `${AWS_ASSETS_PATH}/featured_by/laguna_logo.svg`,
  lender: `${AWS_ASSETS_PATH}/lender.png`,
  meetup: `${AWS_ASSETS_PATH}/featured_by/meetup_logo.png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
  optimism: `${AWS_ASSETS_PATH}/optimism_logo.png`,
  orangedao: `${AWS_ASSETS_PATH}/featured_by/orangedao_logo.png`,
  polygon: `${AWS_ASSETS_PATH}/polygon_blockchain_logo.png`,
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

  const { buttonReport } = useContext(AnalyticsContext);

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

  const blueBackgroundColor = "#212698";
  const lightOrangeColor = "#FF9473";

  const Feature = ({ title, altText, image, ...props }) => {
    return (
      <Box onClick={props.onClick}>
        <RouterLink href={props.href}>
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
            m={[2, 3, 3, 4, 8, 12]}
            pb={2}
            minH={[null, null, "400px", null]}
          >
            <ChakraImage
              boxSize={["220px", "220px", "xs", null, "xs"]}
              objectFit="contain"
              src={image}
              alt={altText}
            />
            <Heading
              textAlign="center"
              fontSize={["md", "md", "lg", "3xl", "4xl"]}
            >
              {title}
            </Heading>
          </Stack>
        </RouterLink>
      </Box>
    );
  };

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
              <GridItem colSpan="12" bgColor={"blue.50"} id="Header grid item">
                <chakra.header boxSize="full" minH="50vh" mb={0}>
                  <Box
                    bgPos="bottom"
                    bgColor="transparent"
                    backgroundImage={`url(${assets[`${background}`]})`}
                    bgSize="cover"
                    boxSize="full"
                  >
                    <Flex
                      align="center"
                      justify="center"
                      boxSize="full"
                      pt="120px"
                      pb={10}
                    >
                      <Stack
                        textAlign="center"
                        alignItems="center"
                        spacing={6}
                        maxW={["1620px", null, null, null, "1620px", "2222px"]}
                        w="100%"
                        px="7%"
                      >
                        <Heading
                          fontSize={["lg", "4xl", "5xl", "5xl", "5xl", "6xl"]}
                          fontWeight="semibold"
                          color="white"
                          as="h1"
                          pb={4}
                          maxW="58%"
                        >
                          Build a Sustainable Game Economy in Only a Few Clicks
                        </Heading>
                        <chakra.span
                          pb={4}
                          fontSize={["sm", "sm", "md", "md", "lg", "lg"]}
                          display="inline-block"
                          color="white"
                          maxW="75%"
                        >
                          Moonstream Engine empowers web3 game designers to grow
                          healthy economies. Moonstream smart contracts and APIs
                          allow you to integrate our game mechanics with zero
                          effort.
                        </chakra.span>
                        <Stack
                          direction={[
                            "column",
                            "column",
                            "row",
                            "row",
                            "row",
                            "row",
                          ]}
                          pb={4}
                        >
                          <Center>
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
                              onClick={() => {
                                buttonReport(
                                  "Boost my game economy",
                                  "front-and-center",
                                  "landing"
                                );
                              }}
                              href={"/contact"}
                            >
                              Boost my game economy
                            </RouteButton>
                          </Center>
                          <Center>
                            <RouteButton
                              variant="orangeAndBlue"
                              bg={blueBackgroundColor}
                              borderColor={lightOrangeColor}
                              textColor="white"
                              minW={[
                                "200px",
                                "250px",
                                "250px",
                                "300px",
                                "350px",
                                "400px",
                              ]}
                              onClick={() => {
                                buttonReport(
                                  "Join our Discord",
                                  "front-and-center",
                                  "landing"
                                );
                              }}
                              href={"/discordleed"}
                              isExternal
                            >
                              Join our Discord
                            </RouteButton>
                          </Center>
                        </Stack>
                        <Box
                          bgColor="white"
                          w={[null, null, "40%"]}
                          rounded={["lg", "xl", "2xl"]}
                          px={5}
                        >
                          <Stack
                            direction={[
                              "column",
                              "column",
                              "row",
                              "row",
                              "row",
                              "row",
                            ]}
                            h="100%"
                          >
                            <Center w={[null, null, "40%"]} h="100%">
                              <Flex>
                                <Center w="100%">
                                  <VStack>
                                    <Text
                                      fontSize={[
                                        "md",
                                        "xl",
                                        "2xl",
                                        "3xl",
                                        "3xl",
                                        "3xl",
                                      ]}
                                      fontWeight="semibold"
                                      textColor={lightOrangeColor}
                                      pt="20px"
                                    >
                                      &gt;$3b
                                    </Text>
                                    <Text pb="20px">
                                      transaction volume.
                                      <br />
                                      And growing
                                    </Text>
                                  </VStack>
                                </Center>
                              </Flex>
                            </Center>
                            <Center w={[null, null, "60%"]} h="100%">
                              <Flex>
                                {" "}
                                <Center w="100%">
                                  <VStack>
                                    <Text
                                      fontSize={[
                                        "md",
                                        "xl",
                                        "2xl",
                                        "3xl",
                                        "3xl",
                                        "3xl",
                                      ]}
                                      fontWeight="semibold"
                                      textColor={lightOrangeColor}
                                      pt="20px"
                                    >
                                      &gt;22k
                                    </Text>
                                    <Text pb="20px">
                                      active users in game economies
                                      <br />
                                      built with our engine
                                    </Text>
                                  </VStack>
                                </Center>
                              </Flex>
                            </Center>
                          </Stack>
                        </Box>
                      </Stack>
                    </Flex>
                  </Box>
                </chakra.header>
              </GridItem>

              <GridItem px="7%" py={10} colSpan="12" bgColor="white.100">
                <VStack>
                  <Heading
                    as="h3"
                    {...HEADING_PROPS}
                    fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
                    fontWeight="semibold"
                  >
                    Trusted by visionaries in the industry
                  </Heading>
                  <Flex
                    wrap="wrap"
                    direction="row"
                    justifyContent="center"
                    pb={10}
                  >
                    <Suspense fallback={""}>
                      <TrustedBadge
                        name="Bullieverse"
                        ImgURL={assets["bulliverse"]}
                        boxURL="https://bullieverisland.com/"
                        scaling={1.5}
                      />{" "}
                      <TrustedBadge
                        scaling={1.5}
                        name="Crypto Guilds"
                        ImgURL={assets["cryptoGuilds"]}
                        boxURL="https://crypto-guilds.com/"
                      />
                      <TrustedBadge
                        scaling={1.5}
                        name="Crypto Unicorns"
                        ImgURL={assets["cryptoUnicorns"]}
                        boxURL="https://www.cryptounicorns.fun/"
                      />
                      <TrustedBadge
                        scaling={1.5}
                        name="game7io"
                        ImgURL={assets["game7io"]}
                        boxURL="https://game7.io/"
                      />
                      <TrustedBadge
                        scaling={1.5}
                        name="orangedao"
                        ImgURL={assets["orangedao"]}
                        boxURL="https://lfg.orangedao.xyz/"
                      />
                    </Suspense>
                  </Flex>
                  <Heading
                    as="h3"
                    {...HEADING_PROPS}
                    fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
                    fontWeight="semibold"
                  >
                    Supported blockchains
                  </Heading>
                  <Flex
                    wrap="wrap"
                    direction="row"
                    justifyContent="center"
                    pb={10}
                  >
                    <Suspense fallback={""}>
                      <TrustedBadge
                        scaling={1.5}
                        name="ethereum"
                        ImgURL={assets["ethereum_blockchain"]}
                        boxURL="https://ethereum.org/"
                      />
                      <TrustedBadge
                        scaling={1.3}
                        name="gnosis"
                        ImgURL={assets["gnosis"]}
                        boxURL="https://gnosis.io/"
                      />
                      <TrustedBadge
                        scaling={1.1}
                        name="polygon"
                        ImgURL={assets["polygon"]}
                        boxURL="https://polygon.technology/"
                      />
                    </Suspense>
                  </Flex>
                  <Heading
                    as="h3"
                    {...HEADING_PROPS}
                    fontSize={["md", "lg", "xl", "2xl", "3xl", "3xl"]}
                    fontWeight="semibold"
                  >
                    Upcoming Integrations
                  </Heading>
                  <Flex wrap="wrap" direction="row" justifyContent="center">
                    <Suspense fallback={""}>
                      <TrustedBadge
                        scaling={1.2}
                        name="arbitrum"
                        ImgURL={assets["arbitrum"]}
                        boxURL="https://bridge.arbitrum.io/"
                      />
                      <TrustedBadge
                        scaling={1.2}
                        name="evmos"
                        ImgURL={assets["evmos"]}
                        boxURL="https://evmos.org/"
                      />
                      <TrustedBadge
                        scaling={1.2}
                        name="forte"
                        ImgURL={assets["forte"]}
                        boxURL="https://www.forte.io/"
                      />
                      <TrustedBadge
                        scaling={1.2}
                        name="optimism"
                        ImgURL={assets["optimism"]}
                        boxURL="https://www.optimism.io/"
                      />
                    </Suspense>
                  </Flex>
                </VStack>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                colSpan="12"
                pt={12}
                bgColor={"blue.900"}
                textColor="white"
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={6} as="h2">
                  Features
                </Heading>
                <Center fontSize={["sm", "sm", "md", "md", "lg", "lg"]} py={4}>
                  <chakra.span textAlign="center" width="85%">
                    {`Lootboxes, crafting recipes, deck building, you name it! With Moonstream Engine you can deploy on-chain mechanics with one click.
                    Read our Use Cases or explore the features to know more.   `}
                  </chakra.span>
                </Center>
                <SimpleGrid
                  columns={[1, 2, 2, 4, 4, 4]}
                  justifyContent="center"
                  w="100%"
                  placeContent={"space-between"}
                  mx={[0, -2, -4]}
                  paddingTop="20px"
                >
                  <Feature
                    title="Assemble Lootboxes"
                    altText="Lootboxes"
                    path="/features/#lootboxes"
                    image={assets["cryptoTraders"]}
                    href="/features/#lootboxes"
                    onClick={() => {
                      console.log("Sending report to mixpanel");
                      buttonReport("Lootboxes", "features", "landing");
                    }}
                  />
                  <Feature
                    title="Create Crafting Recipes"
                    altText="Crafting Recipes"
                    path="/features/#crafting"
                    image={assets["NFT"]}
                    href="/features/#crafting"
                    onClick={() => {
                      buttonReport("Crafting Recipes", "features", "landing");
                    }}
                  />
                  <Feature
                    title="Deploy Minigames"
                    altText="Minigames"
                    path="/features/#minigames"
                    image={assets["DAO"]}
                    href="/features/#minigames"
                    onClick={() => {
                      buttonReport("Minigames", "features", "landing");
                    }}
                  />
                  <Feature
                    title="Manage Airdrops"
                    altText="Airdrops"
                    path="/features/#airdrops"
                    image={assets["lender"]}
                    href="/features/#airdrops"
                    onClick={() => {
                      buttonReport("Airdrops", "features", "landing");
                    }}
                  />
                </SimpleGrid>
                <Center py={8}>
                  <Stack
                    direction={["column", "column", "row", "row", "row", "row"]}
                    pb={4}
                  >
                    <Center>
                      <RouteButton
                        variant="orangeAndBlue"
                        minW={[
                          "250px",
                          "250px",
                          "250px",
                          "300px",
                          "350px",
                          "400px",
                        ]}
                        onClick={() => {
                          buttonReport(
                            "Boost my game economy",
                            "front-and-center",
                            "landing"
                          );
                        }}
                        href={"/contact"}
                      >
                        Learn more about our features
                      </RouteButton>
                    </Center>
                    <Center>
                      <RouteButton
                        variant="orangeAndBlue"
                        bg={blueBackgroundColor}
                        borderColor={lightOrangeColor}
                        textColor="white"
                        minW={[
                          "250px",
                          "250px",
                          "250px",
                          "300px",
                          "350px",
                          "400px",
                        ]}
                        onClick={() => {
                          buttonReport(
                            "Join our Discord",
                            "front-and-center",
                            "landing"
                          );
                        }}
                        href={"/discordleed"}
                        isExternal
                      >
                        Explore the use cases
                      </RouteButton>
                    </Center>
                  </Stack>
                </Center>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                py={10}
                colSpan="12"
                bgColor="white.100"
                minH="50vh"
              >
                <Heading {...HEADING_PROPS} textAlign="center" as="h2" pb={10}>
                  FAQ
                </Heading>
                <Accordion defaultIndex={[0]} allowMultiple allowToggle>
                  <FAQCard
                    heading="I’m a game designer. What can Moonstream engine do for me?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        {" "}
                        Moonstream is a hassle-free way to ultimate game design
                        and superb user experience. You’ll be able to add
                        on-chain mechanics from our web app into your project
                        within a click.
                        <br />
                        <br />
                        Imagine you had a menu of ready-to-use game
                        functionalities... That’s what Moonstream Engine is
                        about.
                      </>
                    }
                  />
                  <FAQCard
                    heading="What on-chain mechanics are we talking about?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        {" "}
                        Use Moonstream to add minigames, in-game items,
                        airdrops, lootboxes, loyalty programs, leaderboards,
                        crafting, and some other mechanics into your game. If
                        you want to add something that’s not on the list - feel
                        free to discuss it with the team.
                        <br />
                        <br />
                        Once you contact us to discuss your project, we’ll
                        provide you with options.
                      </>
                    }
                  />
                  <FAQCard
                    heading="I’m a game developer. How will I benefit?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        {" "}
                        Moonstream removes the complexity of smart contact
                        development. It will save you weeks of time. Moonstream
                        Engine is your backend.
                        <br />
                        <br />
                        You can find code examples below on this page.
                        Integration is easy even if you have no experience with
                        web3.
                      </>
                    }
                  />
                  <FAQCard
                    heading="Is it free?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        {" "}
                        Everything we build is open source and free to self-host
                        or modify.
                        <Link
                          href="https://github.com/bugout-dev/moonstream"
                          textColor="blue.700"
                          isExternal
                        >
                          {" "}
                          <u>Here&apos;s</u>{" "}
                        </Link>
                        our GitHub. We’ll be happy to help you get set up.
                        <br />
                        <br />
                        We also have a managed option, where we manage the smart
                        contracts and the APIs. This is free for indie projects.
                        For larger projects, please reach out to @zomglings on
                        Discord for a quote.
                      </>
                    }
                  />
                  <FAQCard
                    heading="I’m a data scientist. Can I use Moonstream for research?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        You can use{" "}
                        <Link
                          href="https://github.com/bugout-dev/moonstream"
                          isExternal
                        >
                          <u>Moonworm</u>
                        </Link>
                        , our free open source tool, to build datasets of
                        on-chain data related to market activity.
                        <br />
                        <br />
                        We also have a dataset with on-chain activity from the
                        Ethereum NFT market (April 1 to September 25, 2021){" "}
                        <Link
                          href="https://www.kaggle.com/datasets/simiotic/ethereum-nfts"
                          isExternal
                        >
                          <u>here</u>
                        </Link>
                        . And{" "}
                        <Link
                          href="https://github.com/bugout-dev/moonstream/blob/main/datasets/nfts/papers/ethereum-nfts.pdf"
                          isExternal
                        >
                          <u>here</u>
                        </Link>{" "}
                        is our full report on it.
                        <br />
                        <br />
                        We’re working on V2 of the dataset above. You can
                        collaborate with us and become a co-author, just
                        @moonstream on Discord to connect with the team.{" "}
                        <Link
                          href="https://scratched-molybdenum-f03.notion.site/NFT-dataset-v2-33a2900cce3840c0bc048bbc4a0425f8"
                          isExternal
                        >
                          <u>Here</u>
                        </Link>{" "}
                        you can find sample V2 datasets.
                      </>
                    }
                  />
                  <FAQCard
                    heading="What is the Sign Up button for?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        One of the tools we built is the Analytics platform.
                        With it game designers, developers, data scientists and
                        crypto enthusiasts can create dashboards to track
                        on-chain activity and gain insights into web3 economy
                        and its health.
                        <br />
                        <br />
                        <Link
                          href="https://voracious-gerbil-120.notion.site/Creating-dashboard-for-a-smart-contract-288b1bfa64984b109b79895f69129fce"
                          isExternal
                        >
                          <u>Here&apos;s</u>
                        </Link>{" "}
                        a tutorial on how to use the tool.
                        <br />
                        <br />
                        You can get access to our analytics platform by signing
                        up for a Moonstream account on our website. It’s free.
                      </>
                    }
                  />
                  <FAQCard
                    heading="I’m a player. Does Moonstream have anything for me?"
                    headingProps={HEADING_PROPS}
                    panelContent={
                      <>
                        The next big thing coming out soon is for players.{" "}
                        <Link
                          href="/discordleed"
                          onClick={() => {
                            buttonReport(
                              "Join our Discord",
                              "inline-text",
                              "landing"
                            );
                          }}
                          isExternal
                        >
                          <u>Join us on Discord</u>{" "}
                        </Link>
                        for early access.
                      </>
                    }
                  />
                </Accordion>
              </GridItem>
              <GridItem
                px={["7%", "7%", "7%", "15%"]}
                py={10}
                colSpan="12"
                bgColor="white.100"
                minH="100vh"
              >
                <Heading {...HEADING_PROPS} textAlign="center" as="h2" pb={10}>
                  Engine Overview
                </Heading>
                <Center>
                  <EngineOverviewDiagram />
                </Center>
              </GridItem>
              <GridItem
                px={["7%", null, "12%", "15%"]}
                py={10}
                colSpan="12"
                bgColor="white.100"
                minH="100vh"
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={14} as="h2">
                  Our Workflow
                </Heading>
                <HStack alignItems="top" py={5}>
                  <Flex height="100%" width="25%">
                    <Heading
                      as="h3"
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
                      as="h3"
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
                      <Link
                        href="/discordleed"
                        onClick={() => {
                          buttonReport(
                            "Join our Discord",
                            "inline-text",
                            "landing"
                          );
                        }}
                        isExternal
                      >
                        <u>Join our Discord</u>{" "}
                      </Link>{" "}
                      to get in touch with the team (@zomglings). Tell us about
                      your game and schedule a call if needed.
                    </chakra.span>
                  </Flex>
                </HStack>
                <HStack alignItems="top" py={5}>
                  <Flex bgColor="grey.100" width="25%" height="100%">
                    <Heading
                      as="h3"
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
                py={12}
                colSpan="12"
                bgColor="blue.900"
                textColor="white"
                minH="40vh"
              >
                <Heading as="h2" {...HEADING_PROPS} textAlign="center" pb={10}>
                  Featured by{" "}
                </Heading>
                <Center>
                  <Flex
                    width="81%"
                    wrap="wrap"
                    direction="row"
                    justifyContent="center"
                    bgColor="white"
                    rounded={["lg", "xl", "2xl", "3xl", "4xl", "4xl"]}
                  >
                    <Suspense fallback={""}>
                      <TrustedBadge
                        scaling={0.9}
                        name="cointelegraph"
                        caseURL=""
                        ImgURL={assets["cointelegraph"]}
                        boxURL="https://cointelegraph.com/news/17-of-addresses-snapped-up-80-of-all-ethereum-nfts-since-april"
                      />
                      <TrustedBadge
                        scaling={0.9}
                        name="CryptoInsiders"
                        ImgURL={assets["cryptoinsiders"]}
                        boxURL="https://www.crypto-insiders.nl/nieuws/altcoin/17-van-ethereum-whales-bezitten-meer-dan-80-van-alle-nfts-op-de-blockchain/"
                      />
                      <TrustedBadge
                        scaling={0.8}
                        name="cryptoslate"
                        ImgURL={assets["cryptoslate"]}
                        boxURL="https://cryptoslate.com/should-investors-care-80-of-all-nfts-belong-to-17-of-addresses/"
                      />
                      <TrustedBadge
                        scaling={1.2}
                        name="bc101"
                        ImgURL={assets["meetup"]}
                        boxURL="https://www.meetup.com/SF-Bay-Area-Data-Science-Initiative/events/283215538/"
                      />
                      <TrustedBadge
                        name="educative sessions"
                        scaling={1.5}
                        ImgURL={assets["educativesessions"]}
                        boxURL="https://youtu.be/DN8zRzJuy0M"
                      />
                      <TrustedBadge
                        scaling={1.5}
                        name="bc101"
                        ImgURL={assets["bc101"]}
                        boxURL="https://blockchain101.com/"
                      />
                      <TrustedBadge
                        scaling={1.2}
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
                py={10}
                colSpan="12"
                bgColor="white"
                minH="50vh"
              >
                <VStack
                  bgColor="blue.900"
                  rounded={["lg", "xl", "2xl"]}
                  textColor="white"
                  py={8}
                  mb={8}
                >
                  <Heading
                    as="h2"
                    fontSize={["md", "xl", "3xl", "4xl", "4xl", "5xl"]}
                    letterSpacing="wide"
                  >
                    Sign up to grow your economy
                  </Heading>
                  <chakra.span
                    fontSize={["xs", "xs", "sm", "md", "lg", "lg"]}
                    py={4}
                  >
                    {`Answer 5 questions about your project to get whitelisted.`}
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
                    onClick={() => {
                      buttonReport("Boost my game", "page-bottom", "landing");
                    }}
                    href={"/contact"}
                  >
                    Boost my game
                  </RouteButton>
                </VStack>
                <Flex
                  w="100%"
                  alignItems="center"
                  justifyContent="center"
                  direction={["column", "column", "row"]}
                  border="2px"
                  color="blue.900"
                  rounded={["lg", "xl", "2xl"]}
                  px={10}
                >
                  <chakra.span
                    display="block"
                    my={12}
                    fontSize={["sm", "sm", "md", "lg", "xl", "xl"]}
                    textAlign={["justify", "justify", "left", null]}
                    mr={[0, 0, 14]}
                    letterSpacing="tight"
                  >
                    {`Learn more about crypto, NFT and DAOs, find links to educational resources, discuss gaming projects, and laugh at memes.`}
                  </chakra.span>

                  <RouteButton
                    variant="orangeAndBlue"
                    bg="white"
                    borderColor={lightOrangeColor}
                    textColor="blue.900"
                    minW={[
                      "200px",
                      "250px",
                      "250px",
                      "300px",
                      "350px",
                      "400px",
                    ]}
                    onClick={() => {
                      buttonReport(
                        "Join our Discord",
                        "page-bottom",
                        "landing"
                      );
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
