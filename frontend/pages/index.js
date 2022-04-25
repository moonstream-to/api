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
  useMediaQuery,
  Grid,
  Text,
  GridItem,
  SimpleGrid,
  Button,
  Image as ChakraImage,
} from "@chakra-ui/react";
import dynamic from "next/dynamic";
import Link from "next/dist/client/link";
import useUser from "../src/core/hooks/useUser";
import useModals from "../src/core/hooks/useModals";
import useRouter from "../src/core/hooks/useRouter";
import { AWS_ASSETS_PATH, DEFAULT_METATAGS } from "../src/core/constants";
import UIContext from "../src/core/providers/UIProvider/context";
import TrustedBadge from "../src/components/TrustedBadge";
import Slider from "react-slick";
import { v4 as uuidv4 } from "uuid";
import RouteButton from "../src/components/RouteButton";
import { MODAL_TYPES } from "../src/core/providers/OverlayProvider/constants";
import mixpanel from "mixpanel-browser";
import { MIXPANEL_EVENTS } from "../src/core/providers/AnalyticsProvider/constants";

const SplitWithImage = dynamic(
  () => import("../src/components/SplitWithImage"),
  {
    ssr: false,
  }
);
const FaStoreAlt = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaStoreAlt)
);
const FaDiscord = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaDiscord)
);

const GiRiver = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRiver)
);

const GiCrossedChains = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiCrossedChains)
);

const GiChainedHeart = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiChainedHeart)
);

const MdOutlineVerifiedUser = dynamic(() =>
  import("react-icons/md").then((mod) => mod.MdOutlineVerifiedUser)
);

const GiRadarCrossSection = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRadarCrossSection)
);

const GiMedallist = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiMedallist)
);

const GiRobotGolem = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiRobotGolem)
);

const CgUserlane = dynamic(() =>
  import("react-icons/cg").then((mod) => mod.CgUserlane)
);

const GiChaingun = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiChaingun)
);

const GiQuickSlash = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiQuickSlash)
);

const GiConcentrationOrb = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiConcentrationOrb)
);

const GiTakeMyMoney = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiTakeMyMoney)
);

const FaGithubSquare = dynamic(() =>
  import("react-icons/fa").then((mod) => mod.FaGithubSquare)
);
const GiMeshBall = dynamic(() =>
  import("react-icons/gi").then((mod) => mod.GiMeshBall)
);

const VscOrganization = dynamic(() =>
  import("react-icons/vsc").then((mod) => mod.VscOrganization)
);

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "5xl", "5xl", "6xl", "7xl"],
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
  forte: `${AWS_ASSETS_PATH}/featured_by/forte_logo.png`,
  educativesessions: `${AWS_ASSETS_PATH}/featured_by/educative_logo.png`,
  cryptoinsiders: `${AWS_ASSETS_PATH}/featured_by/crypto_insiders.png`,
  cryptoslate: `${AWS_ASSETS_PATH}/featured_by/cs-media-logo-light.png`,
  bitcoinLogo: `${AWS_ASSETS_PATH}/bitcoin.png`,
  ethereumBlackLogo: `${AWS_ASSETS_PATH}/eth-diamond-black.png`,
  ethereumRainbowLogo: `${AWS_ASSETS_PATH}/eth-diamond-rainbow.png`,
  maticLogo: `${AWS_ASSETS_PATH}/matic-token-inverted-icon.png`,
  lender: `${AWS_ASSETS_PATH}/lender.png`,
  DAO: `${AWS_ASSETS_PATH}/DAO .png`,
  NFT: `${AWS_ASSETS_PATH}/NFT.png`,
  bc101: `${AWS_ASSETS_PATH}/featured_by/blockchain101_logo.png`,
  laguna: `${AWS_ASSETS_PATH}/featured_by/laguna_logo.svg`,
  game7io: `${AWS_ASSETS_PATH}/featured_by/game7io_logo.png`,
  orangedao: `${AWS_ASSETS_PATH}/featured_by/orangedao_logo.png`,
  meetup: `${AWS_ASSETS_PATH}/featured_by/meetup_logo.png`,
  gnosis: `${AWS_ASSETS_PATH}/gnosis_chain_logo_no_text.png`,
  immutable: `${AWS_ASSETS_PATH}/immutable_x_logo.png`,
};

const carousel_content = [
  { title: "Bitcoin coming soon!", img: assets["bitcoinLogo"] },
  { title: "Ethereum", img: assets["ethereumBlackLogo"] },
  { title: "Ethereum transaction pool", img: assets["ethereumRainbowLogo"] },
  { title: "Polygon", img: assets["maticLogo"] },
  { title: "immutable x coming soon!", img: assets["immutable"] },
  { title: "gnosis chain coming soon!", img: assets["gnosis"] },
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
          id="page:landing"
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
                          Building blocks for your blockchain economy
                        </Heading>
                        <chakra.span
                          my={12}
                          fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                          display="inline-block"
                          color="blue.200"
                        >
                          Moonstream DAO makes tools that help you build,
                          manage, and secure your blockchain economy.
                        </chakra.span>
                        <chakra.span
                          my={12}
                          fontSize={["md", "2xl", "3xl", "3xl", "3xl", "4xl"]}
                          display="inline-block"
                          color="blue.200"
                        >
                          Moonstream has handled over{" "}
                          <Text
                            fontWeight={600}
                            textColor="orange.900"
                            display={"inline-block"}
                          >
                            $1B
                          </Text>{" "}
                          in transaction value to date.
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
                  mt={[12, 14, 16]}
                  pb={[12, 12, 12, null, 24]}
                >
                  Features:
                </Heading>
                <SimpleGrid
                  columns={[1, 2, 2, 5, null, 5]}
                  justifyContent="center"
                >
                  <Link href="#more_about_analytics" shallow scroll>
                    <Stack
                      transition={"1s"}
                      spacing={1}
                      px={1}
                      alignItems="center"
                      borderRadius="12px"
                      borderColor="gray.100"
                      borderWidth={"1px"}
                      _hover={{ transform: "scale(1.05)", transition: "0.42s" }}
                      cursor="pointer"
                      m={2}
                      pb={2}
                    >
                      <ChakraImage
                        boxSize={["220px", "220px", "xs", null, "xs"]}
                        objectFit="contain"
                        src={assets["cryptoTraders"]}
                        alt="mined transactions"
                      />
                      <Heading textAlign="center ">Analytics</Heading>
                      <chakra.span
                        textAlign={"center"}
                        textColor="blue.600"
                        px={2}
                      >
                        Get the full picture of your economy with automated
                        customizable dashboards.
                      </chakra.span>
                    </Stack>
                  </Link>
                  <Link href="#more_about_markets" shallow scroll>
                    <Stack
                      transition={"1s"}
                      spacing={1}
                      px={1}
                      alignItems="center"
                      borderRadius="12px"
                      borderColor="gray.100"
                      borderWidth={"1px"}
                      _hover={{ transform: "scale(1.05)", transition: "0.42s" }}
                      m={2}
                      pb={2}
                    >
                      <ChakraImage
                        boxSize={["220px", "220px", "xs", null, "xs"]}
                        objectFit="contain"
                        src={assets["NFT"]}
                        alt="mined transactions"
                      />
                      <Heading textAlign="center ">Markets</Heading>
                      <chakra.span
                        textAlign={"center"}
                        textColor="blue.600"
                        px={2}
                      >
                        Create goods and resources for your economy. Set up
                        fully customizable storefronts for these items.
                      </chakra.span>
                    </Stack>
                  </Link>
                  <Link href="#more_about_bridges" shallow scroll>
                    <Stack
                      transition={"1s"}
                      spacing={1}
                      px={1}
                      alignItems="center"
                      borderRadius="12px"
                      borderColor="gray.100"
                      borderWidth={"1px"}
                      _hover={{ transform: "scale(1.05)", transition: "0.42s" }}
                      m={2}
                      pb={2}
                    >
                      <ChakraImage
                        boxSize={["220px", "220px", "xs", null, "xs"]}
                        objectFit="contain"
                        src={assets["lender"]}
                        alt="engine"
                      />
                      <Heading textAlign="center ">Engine</Heading>
                      <chakra.span
                        textAlign={"center"}
                        textColor="blue.600"
                        px={2}
                      >
                        Create and manage tokens with custom mechanics specific
                        to your project.
                      </chakra.span>
                    </Stack>
                  </Link>
                  <Link href="#more_about_loyalty" shallow scroll>
                    <Stack
                      transition={"1s"}
                      spacing={1}
                      px={1}
                      alignItems="center"
                      borderRadius="12px"
                      borderColor="gray.100"
                      borderWidth={"1px"}
                      _hover={{ transform: "scale(1.05)", transition: "0.42s" }}
                      m={2}
                      pb={2}
                    >
                      <ChakraImage
                        boxSize={["220px", "220px", "xs", null, "xs"]}
                        objectFit="contain"
                        src={assets["DAO"]}
                        alt="mined transactions"
                      />
                      <Heading textAlign="center ">{`Loyalty`}</Heading>
                      <chakra.span
                        textAlign={"center"}
                        textColor="blue.600"
                        px={2}
                      >
                        Reward the most active participants in your economy with
                        loyalty programs and token sale whitelists.
                      </chakra.span>
                    </Stack>
                  </Link>
                  <GridItem colSpan={[1, 2, 2, 1, null, 1]}>
                    <Link href="#more_about_security" shallow scroll>
                      <Stack
                        transition={"1s"}
                        spacing={1}
                        px={1}
                        alignItems="center"
                        borderRadius="12px"
                        borderColor="gray.100"
                        borderWidth={"1px"}
                        _hover={{
                          transform: "scale(1.05)",
                          transition: "0.42s",
                        }}
                        m={2}
                        pb={2}
                      >
                        <ChakraImage
                          boxSize={["220px", "220px", "xs", null, "xs"]}
                          objectFit="contain"
                          src={assets["smartDevelopers"]}
                          alt="mined transactions"
                        />
                        <Heading textAlign="center ">{`Security`}</Heading>
                        <chakra.span
                          textAlign={"center"}
                          textColor="blue.600"
                          px={2}
                        >
                          Secure your economy against bad actors. Detect attacks
                          on your economy and defend against them.
                        </chakra.span>
                      </Stack>
                    </Link>
                  </GridItem>
                </SimpleGrid>
              </GridItem>

              <GridItem
                px="7%"
                mt={["32px", "64px", null]}
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="blue.50"
              >
                <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                  Trusted by{" "}
                </Heading>
                <Flex wrap="wrap" direction="row" justifyContent="center">
                  <Suspense fallback={""}>
                    <TrustedBadge
                      scale={1.5}
                      name="Laguna games"
                      caseURL=""
                      ImgURL={assets["laguna"]}
                      boxURL="https://laguna.games/"
                    />
                    <TrustedBadge
                      scale={1.5}
                      name="game7io"
                      ImgURL={assets["game7io"]}
                      boxURL="https://game7.io/"
                    />

                    <TrustedBadge
                      scale={1.5}
                      name="orangedao"
                      ImgURL={assets["orangedao"]}
                      boxURL="https://lfg.orangedao.xyz/"
                    />
                    <TrustedBadge
                      scale={1.5}
                      name="forte"
                      ImgURL={assets["forte"]}
                      boxURL="https://www.forte.io/"
                    />
                  </Suspense>
                </Flex>
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "32px", null, "32px"]}
                id="exchanges"
              >
                <Center>
                  <Heading {...HEADING_PROPS} textAlign="center" pb={14} pt={0}>
                    Learn more about Moonstream DAO use cases
                  </Heading>
                </Center>
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="more_about_analytics"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    colorScheme: "orange",
                    onClick: () => {
                      router.push("/whitepapers");
                    },
                    label: "NFT market report",
                  }}
                  socialButton={{
                    url: "https://discord.gg/K56VNUQGvA",
                    title: "Contact us on discord",
                    icon: "discord",
                  }}
                  elementName={"element1"}
                  colorScheme="green"
                  badge={`Moonstream analytics`}
                  bullets={[
                    {
                      text: `See how value flows into and out of every component of your economy.`,
                      icon: GiRiver,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Track inflation or deflation of your currencies.`,
                      icon: GiTakeMyMoney,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Track the concentration of wealth in your economy.`,
                      icon: GiConcentrationOrb,
                      color: "green.50",
                      bgColor: "green.900",
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
                id="more_about_markets"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  elementName={"element2"}
                  mirror={true}
                  colorScheme="blue"
                  badge={`Moonstream Markets`}
                  socialButton={{
                    url: "https://discord.gg/K56VNUQGvA",
                    title: "Contact us on discord",
                    icon: "discord",
                  }}
                  bullets={[
                    {
                      text: `Deploy new goods or resources into your economy in seconds.`,
                      icon: GiQuickSlash,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `Easy liquidity for those goods and resources on DEXs and on secondary markets like Open Sea.`,
                      icon: GiMeshBall,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `Create custom NFT storefronts.`,
                      icon: FaStoreAlt,
                      color: "blue.50",
                      bgColor: "blue.900",
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
                id="more_about_bridges"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  socialButton={{
                    url: "https://discord.gg/K56VNUQGvA",
                    title: "Contact us on discord",
                    icon: "discord",
                  }}
                  elementName={"element3"}
                  colorScheme="orange"
                  badge={`Moonstream engine`}
                  bullets={[
                    {
                      text: `Deploy customizable and upgradable characters, items, and currencies into your economy`,
                      icon: GiCrossedChains,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Monitor interactions between these tokens`,
                      icon: GiChainedHeart,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Secure the tokens with Moonstream defense bots.`,
                      icon: GiChaingun,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                  ]}
                  imgURL={assets["lender"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="more_about_loyalty"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  mirror
                  socialButton={{
                    url: "https://discord.gg/K56VNUQGvA",
                    title: "Contact us on discord",
                    icon: "discord",
                  }}
                  elementName={"element3"}
                  colorScheme="red"
                  badge={`Moonstream Loyalty`}
                  bullets={[
                    {
                      text: `Track the most active participants in your economy and easily give them rewards for their engagement.`,
                      icon: VscOrganization,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Create and distribute whitelist tokens for your pre-sales. Make them tradeable on markets like OpenSea.`,
                      icon: GiMedallist,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Manage KYC information about your community.`,
                      icon: CgUserlane,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                  ]}
                  imgURL={assets["DAO"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["2rem", "2rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="more_about_security"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  socialButton={{
                    url: "https://discord.gg/K56VNUQGvA",
                    title: "Contact us on discord",
                    icon: "discord",
                  }}
                  elementName={"element3"}
                  colorScheme="green"
                  badge={`Moonstream security`}
                  bullets={[
                    {
                      text: `Moonstream smart contracts have been vetted in production with over $3B in value transacted.`,
                      icon: MdOutlineVerifiedUser,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Moonstream scanners constantly monitor accounts and transactions in your economy and identify threats in seconds.`,
                      icon: GiRadarCrossSection,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `One-click deploy defense bots which counter attacks as soon as they are detected.`,
                      icon: GiRobotGolem,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                  ]}
                  imgURL={assets["smartDevelopers"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                mt={["32px", "64px", null]}
                py={["98px", "128px", null]}
                colSpan="12"
                bgColor="blue.50"
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
                  </Suspense>
                </Flex>
              </GridItem>
              <GridItem
                placeItems="center"
                w="100%"
                colSpan="12"
                pt={["0", "0", "5.125rem", null, "5.125rem"]}
                pb="120px"
                px="7%"
                id={"bottom-line"}
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
                      Check out our GitHub repository and join our community on
                      Discord
                    </Text>
                  </chakra.span>
                  <Flex direction="row" flexWrap="wrap" placeContent="center">
                    <RouteButton
                      placeSelf="center"
                      href={"https://discord.gg/K56VNUQGvA"}
                      size="lg"
                      variant="outline"
                      colorScheme="blue"
                      leftIcon={<FaDiscord />}
                      w="280px"
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
                    >
                      Join our Discord
                    </RouteButton>
                    <RouteButton
                      // mt={3}
                      // p={8}
                      placeSelf="center"
                      href={`https://github.com/bugout-dev/moonstream`}
                      size="lg"
                      variant="outline"
                      colorScheme="blue"
                      w="280px"
                      onClick={() => {
                        if (mixpanel.get_distinct_id()) {
                          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                            full_url: router.nextRouter.asPath,
                            buttonName: `git clone moonstream`,
                            page: `landing`,
                            section: `bottom-line`,
                          });
                        }
                      }}
                      leftIcon={<FaGithubSquare />}
                    >
                      git clone moonstream
                    </RouteButton>
                  </Flex>
                  <Button
                    // mt={3}
                    placeSelf="center"
                    w={["100%", "100%", "fit-content", null]}
                    maxW={["280px", null, "fit-content"]}
                    onClick={() => {
                      if (mixpanel.get_distinct_id()) {
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          full_url: router.nextRouter.asPath,
                          buttonName: `sign up`,
                          page: `landing`,
                          section: `bottom-line`,
                        });
                      }
                      toggleModal({ type: MODAL_TYPES.SIGNUP });
                    }}
                    size="lg"
                    variant="solid"
                    colorScheme="orange"
                  >
                    Sign up
                  </Button>
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
