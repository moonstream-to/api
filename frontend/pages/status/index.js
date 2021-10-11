import React, { useEffect, useState, useLayoutEffect } from "react";
import { useStatus } from "../../src/core/hooks";
import {
  Heading,
  Text,
  Flex,
  Spacer,
  Stack,
  chakra,
  useMediaQuery,
  useBreakpointValue,
} from "@chakra-ui/react";
import { AWS_ASSETS_PATH } from "../../src/core/constants";

const assets = {
  background720: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background1920: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background2880: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
  background3840: `${AWS_ASSETS_PATH}/product-background-720x405.png`,
};

const Status = () => {
  const healthyStatusText = "Available";
  const downStatusText = "Unavailable";
  const healthyStatusColor = "green.900";
  const downStatusColor = "red.600";

  const shortTimestamp = (rawTimestamp) => {
    return rawTimestamp.replace(/^.+T/, "").replace(/\..+/, "");
  };

  const {
    apiServerStatusCache,
    ethereumClusterServerStatusCache,
    gethStatusCache,
    crawlersStatusCache,
    dbServerStatusCache,
    latestBlockDBStatusCache,
  } = useStatus();

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
      // boxSize="full"
      minH="100vh"
      direction="column"
      alignItems="center"
      pb={24}
    >
      <Stack mx={margin} my={12} maxW="1700px">
        <Heading
          as="h2"
          size="md"
          placeSelf="center"
          px={12}
          py={2}
          borderTopRadius="xl"
        >
          {`Status page`}
        </Heading>
        <chakra.span pl={2} px={12} py={2} width="400px">
          <Flex mb={3}>
            <Text>Backend server</Text>
            <Spacer />
            <Text
              color={
                !apiServerStatusCache.isLoading &&
                apiServerStatusCache?.data?.status == "ok"
                  ? healthyStatusColor
                  : downStatusColor
              }
            >
              {!apiServerStatusCache.isLoading &&
              apiServerStatusCache?.data?.status == "ok"
                ? healthyStatusText
                : downStatusText}
            </Text>
          </Flex>
          <br />
          <Flex mb={3}>
            <Text>Crawlers server</Text>
            <Spacer />
            <Text
              color={
                !ethereumClusterServerStatusCache.isLoading &&
                ethereumClusterServerStatusCache?.data?.status == "ok"
                  ? healthyStatusColor
                  : downStatusColor
              }
            >
              {!ethereumClusterServerStatusCache.isLoading &&
              ethereumClusterServerStatusCache?.data
                ? healthyStatusText
                : downStatusText}
            </Text>
          </Flex>
          <Flex mb={3}>
            <Text>Latest block in Geth</Text>
            <Spacer />
            <Text>
              {!gethStatusCache.isLoading &&
              gethStatusCache?.data?.current_block
                ? gethStatusCache.data.current_block
                : 0}
            </Text>
          </Flex>
          <Flex mb={3}>
            <Text>Txpool latest record ts</Text>
            <Spacer />
            <Text>
              {!crawlersStatusCache.isLoading &&
              crawlersStatusCache?.data?.ethereum_txpool_timestamp
                ? shortTimestamp(
                    crawlersStatusCache?.data?.ethereum_txpool_timestamp
                  )
                : downStatusText}
            </Text>
          </Flex>
          <Flex mb={3}>
            <Text>Trending latest record ts</Text>
            <Spacer />
            <Text>
              {!crawlersStatusCache.isLoading &&
              crawlersStatusCache?.data?.ethereum_trending_timestamp
                ? shortTimestamp(
                    crawlersStatusCache?.data?.ethereum_trending_timestamp
                  )
                : downStatusText}
            </Text>
          </Flex>
          <br />
          <Flex mb={3}>
            <Text>Database server</Text>
            <Spacer />
            <Text
              color={
                !dbServerStatusCache.isLoading &&
                dbServerStatusCache?.data?.status == "ok"
                  ? healthyStatusColor
                  : downStatusColor
              }
            >
              {!dbServerStatusCache.isLoading &&
              dbServerStatusCache?.data?.status == "ok"
                ? healthyStatusText
                : downStatusText}
            </Text>
          </Flex>
          <Flex mb={3}>
            <Text>Latest block in Database</Text>
            <Spacer />
            <Text>
              {!latestBlockDBStatusCache.isLoading &&
              latestBlockDBStatusCache?.data?.block_number
                ? latestBlockDBStatusCache.data.block_number
                : 0}
            </Text>
          </Flex>
        </chakra.span>
      </Stack>
    </Flex>
  );
};

export default Status;
