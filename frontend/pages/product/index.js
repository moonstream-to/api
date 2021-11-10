import React, { useEffect, useState, useLayoutEffect } from "react";
import {
  Text,
  Flex,
  Link,
  Stack,
  useMediaQuery,
  useBreakpointValue,
  Center,
} from "@chakra-ui/react";
import { AWS_ASSETS_PATH } from "../../src/core/constants";
import SplitWithImage from "../../src/components/SplitWithImage";
import mixpanel from "mixpanel-browser";
import {
  MIXPANEL_PROPS,
  MIXPANEL_EVENTS,
} from "../../src/core/providers/AnalyticsProvider/constants";
const assets = {
  background720: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background1920: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background2880: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background3840: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  environment: `${AWS_ASSETS_PATH}/product_comic/environment.png`,
  developers: `${AWS_ASSETS_PATH}/product_comic/developers.png`,
  meanwhile: `${AWS_ASSETS_PATH}/product_comic/meanwhile.png`,
  struggle: `${AWS_ASSETS_PATH}/product_comic/struggle.png`,
  solution: `${AWS_ASSETS_PATH}/product_comic/solution.png`,
};

const Product = () => {
  const [background, setBackground] = useState("background720");
  const [backgroundLoaded720, setBackgroundLoaded720] = useState(false);
  const [backgroundLoaded1920, setBackgroundLoaded1920] = useState(false);
  const [backgroundLoaded2880, setBackgroundLoaded2880] = useState(false);
  const [backgroundLoaded3840, setBackgroundLoaded3840] = useState(false);

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
    assets[
      "background720"
    ] = `${AWS_ASSETS_PATH}/product-background-720x405.png`;
    assets[
      "background1920"
    ] = `${AWS_ASSETS_PATH}/product-background-1920x1080.png`;
    assets[
      "background2880"
    ] = `${AWS_ASSETS_PATH}/product-background-2880x1620.png`;
    assets[
      "background3840"
    ] = `${AWS_ASSETS_PATH}/product-background-3840x2160.png`;
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

  useLayoutEffect(() => {
    const imageLoader720 = new Image();
    imageLoader720.src = `${AWS_ASSETS_PATH}/product-background-720x405.png`;
    imageLoader720.onload = () => {
      setBackgroundLoaded720(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader1920 = new Image();
    imageLoader1920.src = `${AWS_ASSETS_PATH}/product-background-1920x1080.png`;
    imageLoader1920.onload = () => {
      setBackgroundLoaded1920(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader2880 = new Image();
    imageLoader2880.src = `${AWS_ASSETS_PATH}/product-background-2880x1620.png`;
    imageLoader2880.onload = () => {
      setBackgroundLoaded2880(true);
    };
  }, []);

  useLayoutEffect(() => {
    const imageLoader3840 = new Image();
    imageLoader3840.src = `${AWS_ASSETS_PATH}/product-background-3840x2160.png`;
    imageLoader3840.onload = () => {
      setBackgroundLoaded3840(true);
    };
  }, []);

  const margin = useBreakpointValue({
    base: "1%",
    sm: "2%",
    md: "3%",
    lg: "15%",
    xl: "20%",
    "2xl": "25%",
  });

  return (
    <Flex
      bgPos="bottom"
      bgColor="transparent"
      backgroundImage={`url(${assets[`${background}`]})`}
      bgSize="cover"
      minH="100vh"
      direction="column"
      alignItems="center"
      pb={24}
    >
      <Stack mx={margin} my={[4, 6, 12]} maxW="1700px" textAlign="justify">
        <SplitWithImage
          py={["12px", "24px", "48px"]}
          title={`Smart contracts are starting to dominate blockchain activity`}
          elementName={"element1"}
          colorScheme="blue"
          body={`web3 stands for decentralized automation through smart contracts.
          Smart contract developers are building the future of the decentralized web.
          `}
          imgURL={assets["environment"]}
          imgBoxShadow="lg"
        />
        <SplitWithImage
          mirror
          py={["12px", "24px", "48px"]}
          elementName={"element1"}
          colorScheme="blue"
          title={`But smart contract activity can be opaque`}
          body={`Even smart contract developers have a difficult time finding out who is using their smart contracts and how.
          This makes it difficult for them to improve their users’ experience and to secure their decentralized applications.`}
          imgURL={assets["developers"]}
          imgBoxShadow="lg"
        />
        <SplitWithImage
          elementName={"element1"}
          colorScheme="blue"
          py={["12px", "24px", "48px"]}
          title={`Blockchain explorers are not enough`}
          body={`Today, analyzing smart contract activity involves viewing data in or crawling data from blockchain explorers.
          The process is tedious and unreliable, and the data is difficult to interpret.
          `}
          imgURL={assets["struggle"]}
          imgBoxShadow="lg"
        />
        <SplitWithImage
          mirror
          elementName={"element1"}
          py={["12px", "24px", "48px"]}
          colorScheme="blue"
          title={`Meanwhile, on Web 2.0`}
          body={`Developers on the centralized web have access to tools like Google Analytics and Mixpanel.
          They can instantly build dashboards to understand their user journeys and identify any issues that their users may be experiencing.
          Nothing like this exists for the decentralized web… until now.
          `}
          imgURL={assets["meanwhile"]}
          imgBoxShadow="lg"
        />
        <SplitWithImage
          elementName={"element1"}
          colorScheme="blue"
          py={["12px", "24px", "48px"]}
          title={`Meet Moonstream!`}
          body={`Moonstream brings product analytics to web3.
          Instantly get analytics for any smart contract you write.
          We don’t care which EIPs you implement and which ones you don’t, or how custom your code is. Moonstream will immediately start giving you insights into what your users are doing with your contracts.
          `}
          imgURL={assets["solution"]}
          imgBoxShadow="lg"
        />
        <Center>
          <Stack placeContent="center">
            <Text fontWeight="500" fontSize="24px">
              To find out more, join us on{" "}
              <Link
                color="orange.900"
                onClick={() => {
                  mixpanel.get_distinct_id() &&
                    mixpanel.track(`${MIXPANEL_EVENTS.BUTTON_CLICKED}`, {
                      [`${MIXPANEL_PROPS.BUTTON_NAME}`]: `Join our discord`,
                    });
                }}
                isExternal
                href={"https://discord.gg/K56VNUQGvA"}
              >
                Discord
              </Link>{" "}
            </Text>
          </Stack>
        </Center>
      </Stack>
    </Flex>
  );
};

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream.to: web3 analytics",
    description:
      "Moonstream brings product analytics to web3. Instantly get analytics for any smart contract you write.",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product",
    url: "https://www.moonstream.to/product",
    image: `${AWS_ASSETS_PATH}/product_comic/solution.png`,
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

export default Product;
