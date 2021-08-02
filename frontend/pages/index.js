import React, {
  useLayoutEffect,
  useEffect,
  Suspense,
  useContext,
  useState,
} from "react";
import {
  Flex,
  Heading,
  Box,
  Image as ChakraImage,
  Button,
  Center,
  Fade,
  chakra,
  Stack,
  Link,
  SimpleGrid,
  useMediaQuery,
} from "@chakra-ui/react";
import { Grid, GridItem } from "@chakra-ui/react";
import { useUser, useAnalytics, useModals, useRouter } from "../src/core/hooks";
import { getLayout } from "../src/layouts";
import SplitWithImage from "../src/components/SplitWithImage";
import ConnectedButtons from "../src/components/ConnectedButtons";
import UIContext from "../src/core/providers/UIProvider/context";
import { MIXPANEL_PROPS } from "../src/core/providers/AnalyticsProvider/constants";
import { FaFileContract } from "react-icons/fa";
import { RiDashboardFill } from "react-icons/ri";
import {
  GiMeshBall,
  GiLogicGateXor,
  GiSuspicious,
  GiHook,
} from "react-icons/gi";
import { AiFillApi } from "react-icons/ai";
import { BiTransfer } from "react-icons/bi";
import { IoTelescopeSharp } from "react-icons/io5";

const HEADING_PROPS = {
  fontWeight: "700",
  fontSize: ["4xl", "5xl", "4xl", "5xl", "6xl", "7xl"],
};
const AWS_PATH =
  "https://s3.amazonaws.com/static.simiotics.com/moonstream/assets";

const assets = {
  background720: `${AWS_PATH}/background720.png`,
  background1920: `${AWS_PATH}/background720.png`,
  background2880: `${AWS_PATH}/background720.png`,
  background3840: `${AWS_PATH}/background720.png`,
  minedTransactions: `${AWS_PATH}/Ethereum+mined+transactions.png`,
  pendingTransactions: `${AWS_PATH}/Ethereum+pending+transactions.png`,
  priceInformation: `${AWS_PATH}/Price+information.png`,
  socialMediaPosts: `${AWS_PATH}/Social+media+posts.png`,
  algorithmicFunds: `${AWS_PATH}/algorithmic+funds.png`,
  cryptoTraders: `${AWS_PATH}/crypto+traders.png`,
  smartDevelopers: `${AWS_PATH}/smart+contract+developers.png`,
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
  const { MIXPANEL_EVENTS, track } = useAnalytics();
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
    assets["background720"] = `${AWS_PATH}/background720.png`;
    assets["background1920"] = `${AWS_PATH}/background1920.png`;
    assets["background2880"] = `${AWS_PATH}/background2880.png`;
    assets["background3840"] = `${AWS_PATH}/background3840.png`;
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
      router.nextRouter.asPath.slice(0, 2) !== "/#"
    ) {
      router.replace(router.nextRouter.asPath, undefined, {
        shallow: true,
      });
    }
  }, [isInit, router]);

  useLayoutEffect(() => {
    console.log("rerender check");
    const imageLoader720 = new Image();
    imageLoader720.src = `${AWS_PATH}/background720.png`;
    imageLoader720.onload = () => {
      setBackgroundLoaded720(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader1920 = new Image();
    imageLoader1920.src = `${AWS_PATH}/background1920.png`;
    imageLoader1920.onload = () => {
      setBackgroundLoaded1920(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader2880 = new Image();
    imageLoader2880.src = `${AWS_PATH}/background2880.png`;
    imageLoader2880.onload = () => {
      setBackgroundLoaded2880(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader3840 = new Image();
    imageLoader3840.src = `${AWS_PATH}/background3840.png`;
    imageLoader3840.onload = () => {
      setBackgroundLoaded3840(true);
    };
  }, []);


  return (
    <Fade in>
      <Box
        width="100%"
        flexDirection="column"
        sx={{ scrollBehavior: "smooth" }}
        // bgColor="primary.1900"
        // backgroundImage={`url(${assets["background"]})`}
        // backgroundImage={`url(https://cdn3.vectorstock.com/i/1000x1000/75/62/moon-landscape-game-background-vector-24977562.jpg)`}
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
              // bgColor="primary.1200"
            >
              <chakra.header boxSize="full" minH="100vh">
                <Box
                  // h="100%"
                  // w="full"
                  // transition=""
                  // bgPos={["initial", "initial", "center", null, "center"]}
                  bgPos="bottom"
                  bgColor="transparent"
                  backgroundImage={`url(${assets[`${background}`]})`}
                  bgSize="cover"
                  boxSize="full"
                  minH="100vh"
                  // bgP
                  // h="container.sm"
                  // h={backgroundH}
                  // minH="100vh"
                  // minH="auto"
                >
                  <Flex
                    align="center"
                    // pos="relative"
                    justify="center"
                    boxSize="full"
                    // bg="blackAlpha.700"
                  >
                    <Stack
                      textAlign="center"
                      alignItems="center"
                      spacing={6}
                      maxW="1620px"
                      px="7%"
                      h="100%"
                      pt={["10vh", null, "30vh"]}
                    >
                      <Heading
                        size="2xl"
                        fontWeight="semibold"
                        color="white"
                        // textTransform="uppercase"
                      >
                        {/* <LoadingDots isActive> */}
                        All the crypto data you care about in a single stream
                        {/* </LoadingDots> */}
                      </Heading>
                      <chakra.span
                        my={12}
                        fontSize={["lg", null, "xl"]}
                        display="inline-block"
                        color="primary.200"
                        textDecor="underline"
                      >
                        Get all the crypto data you need in a single stream.
                        From pending transactions in the Ethereum transaction
                        pool to Elon Musk’s latest tweets.
                      </chakra.span>
                      <chakra.span
                        fontSize={["lg", null, "xl"]}
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
              minH="100vh"
              // bgSize="cover"
              // bgImage={`url(${assets["background"]})`}
            >
              <Heading
                {...HEADING_PROPS}
                textAlign="center"
                pb={[12, 12, 12, null, 48]}
              >
                Data you can add to your stream:
              </Heading>

              <SimpleGrid
                columns={[1, 2, 2, 4, null, 4]}
                // overflowY="clip"
                // direction={["column", null, "row"]}
                // flexWrap="nowrap"
                // justifyContent={["center", null, "space-evenly"]}
              >
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
                  Moonstream is ment for you if
                </Heading>
              </Center>
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
                    onClick: () => {
                      track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                        [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `scroll to CryptoTrader`,
                      });
                    },
                  }}
                  button2={{
                    label: "Algorithmic Fund",
                    link: "/#algoFund",
                    onClick: () => {
                      track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                        [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `scroll to AlgoFund`,
                      });
                    },
                  }}
                  button3={{
                    label: "Developer",
                    link: "/#smartDeveloper",
                    onClick: () => {
                      track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                        [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `scroll to Developer`,
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
              id="cryptoTrader"
              minH={ui.isMobileView ? "100vh" : null}
            >
              <SplitWithImage
                cta={{
                  label: "I want early access!",
                  onClick: () => {
                    track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                      [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `Early access CTA: Crypto trader`,
                    });
                    toggleModal("hubspot-trader");
                  },
                }}
                elementName={"element1"}
                colorScheme="suggested"
                badge={`For crypto traders`}
                title={``}
                body={``}
                bullets={[
                  {
                    text: `Subscribe to the defi contracts you care about`,
                    icon: FaFileContract,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                  {
                    text: `Make sense of how others are calling these contracts using Moonstream dashboards.
                    `,
                    icon: RiDashboardFill,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                  {
                    text: `Get data directly from the transaction pool through our global network of Ethereum nodes`,
                    icon: GiMeshBall,
                    color: "suggested.50",
                    bgColor: "suggested.900",
                  },
                ]}
                imgURL={assets["cryptoTraders"]}
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
                cta={{
                  label: "I want early access!",
                  onClick: () => {
                    track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                      [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `Early access CTA: Algo fund`,
                    });
                    toggleModal("hubspot-fund");
                  },
                }}
                elementName={"element2"}
                mirror={true}
                colorScheme="secondary"
                badge={`For algorithmic funds`}
                bullets={[
                  {
                    text: `Get API access to your stream`,
                    icon: AiFillApi,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                  {
                    text: `Set conditions that trigger predefined actions`,
                    icon: GiLogicGateXor,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                  {
                    text: `Execute transactions directly on Moonstream nodes`,
                    icon: BiTransfer,
                    color: "secondary.50",
                    bgColor: "secondary.900",
                  },
                ]}
                imgURL={assets["algorithmicFunds"]}
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
                cta={{
                  label: "I want early access!",
                  onClick: () => {
                    track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                      [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `Early access CTA: developer`,
                    });
                    toggleModal("hubspot-developer");
                  },
                }}
                elementName={"element3"}
                colorScheme="primary"
                badge={`For smart contract developers`}
                bullets={[
                  {
                    text: `See how people use your smart contracts`,
                    icon: IoTelescopeSharp,
                    color: "primary.50",
                    bgColor: "primary.900",
                  },
                  {
                    text: `Set up alerts on suspicious activity`,
                    icon: GiSuspicious,
                    color: "primary.50",
                    bgColor: "primary.900",
                  },
                  {
                    text: `Register webhooks to connect your off-chain infrastructure`,
                    icon: GiHook,
                    color: "primary.50",
                    bgColor: "primary.900",
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
                <Button
                  as={Link}
                  isExternal
                  href={"https://discord.gg/FetK5BxD"}
                  size="lg"
                  variant="solid"
                  colorScheme="suggested"
                  id="test"
                  onClick={() => {
                    track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                      [`${MIXPANEL_PROPS.BUTTON_CLICKED}`]: `Join our discord`,
                    });
                    toggleModal("hubspot");
                  }}
                >
                  Join our discord
                </Button>
              </Center>
            </GridItem>
          </Grid>
        </Flex>
      </Box>
    </Fade>
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
    image: `${AWS_PATH}/crypto+traders.png`,
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

Homepage.layout = "default";
Homepage.getLayout = getLayout;

export default Homepage;
