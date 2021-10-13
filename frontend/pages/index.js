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
import { AWS_ASSETS_PATH } from "../src/core/constants";
import mixpanel from "mixpanel-browser";
import UIContext from "../src/core/providers/UIProvider/context";
const SplitWithImage = dynamic(
  () => import("../src/components/SplitWithImage"),
  {
    ssr: false,
  }
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

const ConnectedButtons = dynamic(
  () => import("../src/components/ConnectedButtons"),
  {
    ssr: false,
  }
);
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
  comicWhite: `${AWS_ASSETS_PATH}/moonstream-comic-white.png`,
  smartDevelopers: `${AWS_ASSETS_PATH}/smart+contract+developers.png`,
};
const Homepage = () => {
  const ui = useContext(UIContext);
  const [background, setBackground] = useState("background720");
  const [backgroundLoaded720, setBackgroundLoaded720] = useState(false);
  const [backgroundLoaded1920, setBackgroundLoaded1920] = useState(false);
  const [backgroundLoaded2880, setBackgroundLoaded2880] = useState(false);
  const [backgroundLoaded3840, setBackgroundLoaded3840] = useState(false);

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
                      </Stack>
                    </Flex>
                  </Box>
                </chakra.header>
              </GridItem>

              <GridItem px="7%" colSpan="12" pt={0} minH="100vh">
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

                <Heading
                  {...HEADING_PROPS}
                  textAlign="center"
                  mt={48}
                  pb={[12, 12, 12, null, 24]}
                >
                  See how your smart contracts are being used from:
                </Heading>
                <SimpleGrid columns={[1, 2, 2, 4, null, 4]}>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["minedTransactions"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">
                      Ethereum mined transactions
                    </Heading>
                  </Stack>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["pendingTransactions"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">
                      Ethereum pending transactions
                    </Heading>
                  </Stack>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["priceInformation"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">Centralized exchanges</Heading>
                  </Stack>
                  <Stack spacing={1} px={1} alignItems="center">
                    <ChakraImage
                      boxSize={["220px", "220px", "xs", null, "xs"]}
                      objectFit="contain"
                      src={assets["socialMediaPosts"]}
                      alt="mined transactions"
                    />
                    <Heading textAlign="center ">Social media posts</Heading>
                  </Stack>
                </SimpleGrid>
                <Center>
                  <Heading pt="160px" pb="60px">
                    Moonstream is meant for you if
                  </Heading>
                </Center>
                <Flex
                  w="100%"
                  direction={["column", "row", "column", null, "column"]}
                  flexWrap={["nowrap", "nowrap", "nowrap", null, "nowrap"]}
                  pb="32px"
                >
                  <ConnectedButtons
                    title={"You need a fusion of..."}
                    button4={{
                      label: "Blockchain analytics",
                      link: "/#analytics",
                      onClick: () => {
                        mixpanel.get_distinct_id() &&
                          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                            [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Connected buttons: scroll to analytics`,
                          });
                      },
                    }}
                    button1={{
                      label: "TX pool real time data",
                      link: "/#txpool",
                      onClick: () => {
                        mixpanel.get_distinct_id() &&
                          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                            [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Connected buttons: scroll to txpool`,
                          });
                      },
                    }}
                    button2={{
                      label: "Exchange price stream",
                      link: "/#exchanges",
                      onClick: () => {
                        mixpanel.get_distinct_id() &&
                          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                            [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Connected buttons: scroll to exchanges`,
                          });
                      },
                    }}
                    button3={{
                      label: "Social media posts",
                      link: "/#smartDeveloper",
                      onClick: () => {
                        mixpanel.get_distinct_id() &&
                          mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                            [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Connected buttons: scroll to developer`,
                          });
                      },
                    }}
                  />
                </Flex>
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["1rem", "1rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="txpool"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    label: "I want early access!",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer txpool button`,
                        });
                      toggleModal("hubspot-developer");
                    },
                  }}
                  elementName={"element1"}
                  colorScheme="green"
                  badge={`Transaction pool data`}
                  title={`Get real-time access to transaction pool`}
                  body={`In blockchains, transaction pool is place where future blocks are being forged.
                  Having insight in to this dynamic, always changing data means to be in the present moment
                  `}
                  bullets={[
                    {
                      text: `Subscribe to the defi contracts you care about`,
                      icon: FaFileContract,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Get data directly from the transaction pool through our global network of Ethereum nodes
                      `,
                      icon: RiDashboardFill,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                    {
                      text: `Setup notifications to be first to know when and how your contract is being interacted`,
                      icon: GiMeshBall,
                      color: "green.50",
                      bgColor: "green.900",
                    },
                  ]}
                  imgURL={assets["pendingTransactions"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["1rem", "1rem", "5.125rem", null, "5.125rem"]}
                pb={["0", "66px", null, "66px"]}
                id="exchanges"
                minH={ui.isMobileView ? "100vh" : null}
              >
                <SplitWithImage
                  cta={{
                    label: "I want early access!",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer exchanges button`,
                        });
                      toggleModal("hubspot-developer");
                    },
                  }}
                  elementName={"element2"}
                  mirror={true}
                  colorScheme="orange"
                  badge={`Centralized exchange prices`}
                  title={`Market data - just in time! `}
                  body={`Moonstream is your tool of choice to built algorithms and tools which need to source data from exchange services. Whether it is on-chian automatic market maker, or centralized exchange - get numbers in one dashboard`}
                  bullets={[
                    {
                      text: `Get API access to your stream`,
                      icon: AiFillApi,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Set conditions that trigger predefined actions`,
                      icon: GiLogicGateXor,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                    {
                      text: `Execute transactions directly on Moonstream nodes`,
                      icon: BiTransfer,
                      color: "orange.50",
                      bgColor: "orange.900",
                    },
                  ]}
                  imgURL={assets["priceInformation"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["1rem", "1rem", "1.125rem", null, "5.125rem"]}
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
                      toggleModal("hubspot-developer");
                    },
                  }}
                  socialButton={{
                    url: "https://github.com/bugout-dev/moonstream/",
                    network: "github",
                    label: "See our github",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Github link in landing page`,
                        });
                    },
                  }}
                  elementName={"element3"}
                  colorScheme="blue"
                  title={`What really matters - is people`}
                  badge={`stay social`}
                  body={`It's all about the community. Stay informed about what happens in social networks, news portals and rss feeds`}
                  bullets={[
                    {
                      text: `Use our AI to get semantics and find patterns`,
                      icon: GiMeshBall,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `Secure your community wellbeing by automatically detecting social scam`,
                      icon: GiSuspicious,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                    {
                      text: `Register on-chain webhooks to take action`,
                      icon: GiHook,
                      color: "blue.50",
                      bgColor: "blue.900",
                    },
                  ]}
                  imgURL={assets["socialMediaPosts"]}
                />
              </GridItem>
              <GridItem
                px="7%"
                colSpan="12"
                pt={["1rem", "1rem", "1.125rem", null, "5.125rem"]}
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
                      toggleModal("hubspot-developer");
                    },
                  }}
                  socialButton={{
                    url: "https://github.com/bugout-dev/moonstream/",
                    network: "github",
                    label: "See our github",
                    onClick: () => {
                      mixpanel.get_distinct_id() &&
                        mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                          [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Github link in landing page`,
                        });
                    },
                  }}
                  elementName={"element3"}
                  colorScheme="red"
                  badge={`Analyse blockchain activity`}
                  bullets={[
                    {
                      text: `Monitor blockchain data in real time`,
                      icon: IoTelescopeSharp,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Set up alerts on suspicious activity`,
                      icon: GiSuspicious,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                    {
                      text: `Register webhooks to connect your off-chain infrastructure`,
                      icon: GiHook,
                      color: "red.50",
                      bgColor: "red.900",
                    },
                  ]}
                  imgURL={assets["smartDevelopers"]}
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
                  <Stack placeContent="center">
                    <Text fontWeight="500" fontSize="24px">
                      Want to find out more? Reach out to us on{" "}
                      <Link
                        color="orange.900"
                        onClick={() => {
                          mixpanel.get_distinct_id() &&
                            mixpanel.track(
                              `${MIXPANEL_EVENTS.BUTTON_CLICKED}`,
                              {
                                [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Join our discord`,
                              }
                            );
                        }}
                        isExternal
                        href={"https://discord.gg/K56VNUQGvA"}
                      >
                        Discord
                      </Link>{" "}
                      or{" "}
                      <Link
                        color="orange.900"
                        onClick={() => {
                          mixpanel.get_distinct_id() &&
                            mixpanel.track(
                              `${MIXPANEL_EVENTS.BUTTON_CLICKED}`,
                              {
                                [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Early access CTA: developer want to find more button`,
                              }
                            );
                          toggleModal("hubspot-developer");
                        }}
                      >
                        request early access
                      </Link>
                    </Text>
                  </Stack>
                </Center>
              </GridItem>
              <GridItem
                placeItems="center"
                w="100%"
                colSpan="12"
                pt={["0", "0", "5.125rem", null, "5.125rem"]}
                pb="120px"
              >
                <Center>
                  <ChakraImage src={assets["comicWhite"]}></ChakraImage>
                </Center>
              </GridItem>
            </Grid>
          </Flex>
        </Box>
      </Fade>
    </Suspense>
  );
};

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream.to: All your crypto data in one stream",
    description:
      "From the Ethereum transaction pool to Elon Musk’s latest tweets get all the crypto data you care about in one stream.",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized",
    url: "https://www.moonstream.to",
    image: `${AWS_ASSETS_PATH}/crypto+traders.png`,
  };

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
    props: { metaTags, preloads },
  };
}

export default Homepage;
