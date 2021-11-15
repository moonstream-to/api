import React, {
  useState,
  useContext,
  Suspense,
  useEffect,
  useLayoutEffect,
} from "react";
import {
  Fade,
  Flex,
  Heading,
  Box,
  Center,
  chakra,
  Stack,
  Link,
  useMediaQuery,
  Grid,
  Text,
  GridItem,
  SimpleGrid,
  Image as ChakraImage,
} from "@chakra-ui/react";
import dynamic from "next/dynamic";
import useUser from "../src/core/hooks/useUser";
import useModals from "../src/core/hooks/useModals";
import useRouter from "../src/core/hooks/useRouter";
import {
  MIXPANEL_PROPS,
  MIXPANEL_EVENTS,
} from "../src/core/providers/AnalyticsProvider/constants";
import { AWS_ASSETS_PATH, DEFAULT_METATAGS } from "../src/core/constants";
import mixpanel from "mixpanel-browser";
import UIContext from "../src/core/providers/UIProvider/context";
import TrustedBadge from "../src/components/TrustedBadge";
import Slider from "react-slick";
import SchematicPlayground from "../src/components/SchematicPlayground";
import { v4 as uuidv4 } from "uuid";
import RouteButton from "../src/components/RouteButton";
import { FaDiscord } from "react-icons/fa";
import { MODAL_TYPES } from "../src/core/providers/OverlayProvider/constants";
const SplitWithImage = dynamic(
  () => import("../src/components/SplitWithImage"),
  {
    ssr: false,
  }
);
const FaGithubSquare = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaGithubSquare)
);
const GiSuspicious = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiSuspicious)
);

const GiHook = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiHook)
);

const IoTelescopeSharp = dynamic(() =>
  import("react-icons/io5").then((mod) => mod.IoTelescopeSharp)
);

const AiFillApi = dynamic(() =>
  import("react-icons/ai").then((mod) => mod.AiFillApi)
);

const BiTransfer = dynamic(() =>
  import("react-icons/bi").then((mod) => mod.BiTransfer)
);

const RiDashboardFill = dynamic(() =>
  import("react-icons/ri").then((mod) => mod.RiDashboardFill)
);
const FaFileContract = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaFileContract)
);
const GiMeshBall = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiMeshBall)
);

const GiLogicGateXor = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiLogicGateXor)
);

const VscOrganization = dynamic(() =>
  import("react-icons/vsc").then((mod) => mod.VscOrganization)
);
const FaVoteYea = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaVoteYea)
);

const RiOrganizationChart = dynamic(() =>
  import("react-icons/ri").then((mod) => mod.RiOrganizationChart)
);
const FiActivity = dynamic(() =>
  import("react-icons/fi").then((mod) => mod.FiActivity)
);

const RiMapPinUserLine = dynamic(() =>
  import("react-icons/ri").then((mod) => mod.RiMapPinUserLine)
);
const AiOutlinePieChart = dynamic(() =>
  import("react-icons/ai").then((mod) => mod.AiOutlinePieChart)
);

const BiBot = dynamic(() => import("react-icons/bi").then((mod) => mod.BiBot));

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "4xl", "5xl", "6xl", "7xl"],
};

const assets = {
  background720: `${AWS_ASSETS_PATH}/background720.png`,
  background1920: `${AWS_ASSETS_PATH}/background720.png`,
  background2880: `${AWS_ASSETS_PATH}/background720.png`,
  background3840: `${AWS_ASSETS_PATH}/background720.png`,
  minedTransactions: `${AWS_ASSETS_PATH}/Ethereum+mined+transactions.png`,
  pendingTransactions: `${AWS_ASSETS_PATH}/Ethereum+pending+transactions.png`,
  priceInformation: `${AWS_ASSETS_PATH}/Price+information.png`,
  socialMediaPosts: `${AWS_ASSETS_PATH}/Social+media+posts.png`,
  cryptoTraders: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  smartDevelopers: `${AWS_ASSETS_PATH}/smart+contract+developers.png`,
  cointelegraph: `${AWS_ASSETS_PATH}/featured_by/Cointelegraph_logo.png`,
  cryptoinsiders: `${AWS_ASSETS_PATH}/featured_by/crypto_insiders.png`,
  cryptoslate: `${AWS_ASSETS_PATH}/featured_by/cs-media-logo-light.png`,
  bitcoinLogo: `${AWS_ASSETS_PATH}/bitcoin.png`,
  ethereumBlackLogo: `${AWS_ASSETS_PATH}/eth-diamond-black.png`,
  ethereumRainbowLogo: `${AWS_ASSETS_PATH}/eth-diamond-rainbow.png`,
  maticLogo: `${AWS_ASSETS_PATH}/matic-token-inverted-icon.png`,
  erc20: `${AWS_ASSETS_PATH}/ERC 20.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
};

const carousel_content = [
  { title: "Bitcoin coming soon!", img: assets["bitcoinLogo"] },
  { title: "Ethereum", img: assets["ethereumBlackLogo"] },
  { title: "Ethereum transaction pool", img: assets["ethereumRainbowLogo"] },
  { title: "Polygon coming soon!", img: assets["maticLogo"] },
  { title: "Bitcoin coming soon!", img: assets["bitcoinLogo"] },
  { title: "Ethereum", img: assets["ethereumBlackLogo"] },
  { title: "Ethereum transaction pool", img: assets["ethereumRainbowLogo"] },
  { title: "Polygon coming soon!", img: assets["maticLogo"] },
];
const Homepage = () => {
  const ui = useContext(UIContext);
  const [background, setBackground] = useState("background720");
  const [backgroundLoaded720, setBackgroundLoaded720] = useState(false);
  const [backgroundLoaded1920, setBackgroundLoaded1920] = useState(false);
  const [backgroundLoaded2880, setBackgroundLoaded2880] = useState(false);
  const [backgroundLoaded3840, setBackgroundLoaded3840] = useState(false);

  const [imageIndex, setImageIndex] = useState(0);

  const router = useRouter();
  const { isInit } = useUser();
  const { toggleModal } = useModals();
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

  const settings = {
    infinite: true,
    lazyLoad: true,
    speed: 2000,
    autoplay: true,
    autoplaySpeed: 0,
    // cssEase: "linear",
    cssEase: "cubic-bezier(0.165, 0.840, 0.440, 1.000)",
    // cssEase: "ease-in",
    slidesToScroll: 1,
    slidesToShow: ui.isMobileView ? 3 : 5,
    centerMode: true,
    centerPadding: 0,
    // nextArrow: "",
    // prevArrow: "",
    beforeChange: (current, next) => setImageIndex(next),
  };

  return (
    <Suspense fallback="">
      <Fade in>
        <Box
          width="100%"
          flexDirection="column"
          sx={{ scrollBehavior: "smooth" }}
          bgSize="cover"
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
                px="0"
                colSpan="12"
                pb={[1, 2, null, 8]}
                minH="100vh"
              >
                <chakra.header boxSize="full" minH="100vh">
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
                          Open source blockchain analytics
                        </Heading>
                        <chakra.span
                          my={12}
                          fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                          display="inline-block"
                          color="blue.200"
                        >
                          Product analytics for Web3. Moonstream helps you
                          understand exactly how people are using your smart
                          contracts.
                        </chakra.span>
                        <Box
                          w="100vw"
                          minH="200px"
                          // px="7%"
                          py={0}
                          overflowX="hidden"
                          overflowY="visible"
                        >
                          <Slider
                            {...settings}
                            // adaptiveHeight={true}
                            arrows={false}
                            autoplay={true}
                            autoplaySpeed={100}
                          >
                            {carousel_content.map((content_item, idx) => (
                              <Box
                                pt="80px"
                                h="auto"
                                w="150px"
                                maxW="150px"
                                // size="150px"
                                key={uuidv4()}
                                className={
                                  idx === imageIndex
                                    ? "slide activeSlide"
                                    : "slide"
                                }
                                // bgColor="blue.900"
                                // borderRadius="lg"
                                // boxShadow="lg"
                              >
                                <ChakraImage
                                  fit="contain"
                                  boxSize={["64px", "96px", "130px", null]}
                                  src={content_item.img}
                                />
                                <Text
                                  py={2}
                                  color="blue.300"
                                  fontSize={["sm", "md", null]}
                                >
                                  {content_item.title}
                                </Text>
                              </Box>
                            ))}
                          </Slider>
                        </Box>
                      </Stack>
                    </Flex>
                  </Box>
                </chakra.header>
              </GridItem>

              <GridItem px="7%" colSpan="12" pt={0} minH="100vh">
                <Heading
                  {...HEADING_PROPS}
                  textAlign="center"
                  mt={[24, 32, 48]}
                  pb={[12, 12, 12, null, 24]}
                >
                  Get analytics for your:
                </Heading>
                <SimpleGrid columns={[1, 2, 2, 4, null, 4]}>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["NFT"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">NFTs</Heading>
                  </Stack>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["erc20"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">Tokens</Heading>
                  </Stack>

                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["cryptoTraders"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">DEXs</Heading>
                  </Stack>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["DAO"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">{`DAOs`}</Heading>
                  </Stack>
                </SimpleGrid>
                <Center>
                  <Heading
                    pt={["32px", "160px", null]}
                    pb={["12px", "60px", null]}
                    fontSize={["18px", "32px", null]}
                    textAlign="center"
                  >
                    Your game changer in blockchain analytics
                  </Heading>
                </Center>
                <Flex
                  w="100%"
                  direction={["column", "row", "column", null, "column"]}
                  flexWrap={["nowrap", "nowrap", "nowrap", null, "nowrap"]}
                  pb="32px"
                  placeContent="center"
                >
                  <SchematicPlayground />
                </Flex>
              </GridItem>

              <GridItem
                px="7%"
                colSpan="12"
                pt="66px"
                bgColor="blue.50"
                pb={["20px", "30px", "92px", null, "92px", "196px"]}
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                  Featured by{" "}
                </Heading>
                <Flex wrap="wrap" direction="row" justifyContent="center">
                  <Suspense fallback={""}>
                    <TrustedBadge
                      name="cointelegraph"
                      caseURL=""
                      ImgURL={assets["cointelegraph"]}
                    />
                    <TrustedBadge
                      name="CryptoInsiders"
                      ImgURL={assets["cryptoinsiders"]}
                    />

                    <TrustedBadge
                      name="cryptoslate"
                      ImgURL={assets["cryptoslate"]}
                    />
                  </Suspense>
                </Flex>
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="txpool"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    label: "Want to find out more?",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer txpool button`,
                        });
                      toggleModal(MODAL_TYPES.HUBSPOT);
                    },
                  }}
                  elementName={"element1"}
                  colorScheme="green"
                  badge={`NFTs`}
                  title={`Custom analytics for NFTs`}
                  body={`Moonstream automatically understands smart contracts. Create your own custom dashboards. Doesn’t matter what the custom behavior is, you can track it.`}
                  bullets={[
                    {
                      text: `Who owns your NFTs?`,
                      icon: AiOutlinePieChart,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Who is selling your NFTs?`,
                      icon: FaFileContract,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `How much are your NFTs being sold for on OpenSea, Nifty Gateway, Rarible?`,
                      icon: RiDashboardFill,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Who is using the custom features of your NFTs?`,
                      icon: GiMeshBall,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `How are they using them?`,
                      icon: RiMapPinUserLine,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                  ]}
                  imgURL={assets["NFT"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="exchanges"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    label: "Want to find out more?",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer exchanges button`,
                        });
                      toggleModal(MODAL_TYPES.HUBSPOT);
                    },
                  }}
                  elementName={"element2"}
                  mirror={true}
                  colorScheme="orange"
                  badge={`ERC20`}
                  title={`Feel the pulse of token activity`}
                  body={`Visualize market activity with Moonstream dashboards. Monitor token activity on the blockchain and in the transaction pool.`}
                  bullets={[
                    {
                      text: `Who owns your tokens?`,
                      icon: GiSuspicious,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `What is your weekly, daily, or hourly transaction volume?`,
                      icon: AiFillApi,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Which exchanges is your token trending on?`,
                      icon: IoTelescopeSharp,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Which other tokens is your token being traded for?`,
                      icon: BiTransfer,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `How many people are holding your token versus actively using it?
                      `,
                      icon: GiLogicGateXor,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                  ]}
                  imgURL={assets["erc20"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="smartDeveloper"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    label: "Want to find out more?",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer smartDeveloper button`,
                        });
                      toggleModal(MODAL_TYPES.HUBSPOT);
                    },
                  }}
                  elementName={"element3"}
                  colorScheme="blue"
                  title={`All the data you need to make a market`}
                  badge={`DEXs`}
                  body={`Monitor the performance of your DEX live from the blockchain and from the transaction pool. Build dashboards that show you DEX activity monthly, weekly, daily, hourly, or by the minute.`}
                  bullets={[
                    {
                      text: `Who is providing liquidity on your DEX?`,
                      icon: GiSuspicious,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `How much liquidity for each token pair?`,
                      icon: GiMeshBall,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `Bot vs. human activity on your exchange`,
                      icon: BiBot,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `How large is your transaction pool backlog?`,
                      icon: GiHook,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                  ]}
                  imgURL={assets["cryptoTraders"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="analytics"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  mirror
                  cta={{
                    label: "Want to find out more?",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer analytics button`,
                        });
                      toggleModal(MODAL_TYPES.HUBSPOT);
                    },
                  }}
                  elementName={"element3"}
                  colorScheme="red"
                  badge={`DAOs`}
                  title={`What really matters is community`}
                  body={`Gain insight into your community. Build community dashboards to make participation more open. Monitor your DAO ecosystem.`}
                  bullets={[
                    {
                      text: `Who are your community members?`,
                      icon: VscOrganization,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Who is actively participating?`,
                      icon: GiSuspicious,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `What are the open initiatives for your DAO?`,
                      icon: FaVoteYea,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `What is the level of participation for each initiative?`,
                      icon: FiActivity,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Which DAOs or other protocols interact with yours?
                      `,
                      icon: RiOrganizationChart,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                  ]}
                  imgURL={assets["DAO"]}
                />
              </GridItem>
              <GridItem
                placeItems="center"
                w="100%"
                colSpan="12"
                pt={["0", "0", "5.125rem", null, "5.125rem"]}
                pb="120px"
                px="7%"
              >
                <Stack direction="column" justifyContent="center">
                  <chakra.span
                    textAlign="center"
                    fontWeight="600"
                    fontSize="lg"
                    w="100%"
                    h="fit-content"
                  >
                    <Text
                      mb={18}
                      fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                    >
                      We believe that the blockchain is for everyone. This
                      requires complete <b>transparency</b>. That’s why all our
                      software is{" "}
                      <chakra.span
                        display="inline-block"
                        textColor="orange.900"
                        as={Link}
                        href="https://github.com/bugout-dev/moonstream"
                      >
                        <i>open source</i>
                      </chakra.span>
                    </Text>
                  </chakra.span>
                  <Flex direction="row" flexWrap="wrap" placeContent="center">
                    <RouteButton
                      placeSelf="center"
                      isExternal
                      href={`https://github.com/bugout-dev/moonstream`}
                      size="md"
                      variant="outline"
                      colorScheme="blue"
                      w="250px"
                      leftIcon={<FaGithubSquare />}
                    >
                      git clone moonstream
                    </RouteButton>
                    <RouteButton
                      placeSelf="center"
                      isExternal
                      href={"https://discord.gg/K56VNUQGvA"}
                      size="md"
                      variant="outline"
                      colorScheme="blue"
                      leftIcon={<FaDiscord />}
                      w="250px"
                    >
                      Join our Discord
                    </RouteButton>
                  </Flex>
                  <RouteButton
                    placeSelf="center"
                    isExternal
                    w={["100%", "100%", "fit-content", null]}
                    maxW={["250px", null, "fit-content"]}
                    href={`https://github.com/bugout-dev/moonstream`}
                    size="lg"
                    variant="solid"
                    colorScheme="orange"
                  >
                    Sign up
                  </RouteButton>
                </Stack>
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
