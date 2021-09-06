import React, { useEffect, useState } from "react";
import { getLayout } from "../src/layouts/AppLayout";
import { Spinner, Flex, Heading, Stack } from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";
import useNFTs from "../src/core/hooks/useNFTs";
import RangeSelector from "../src/components/RangeSelector";
import StatsCard from "../src/components/StatsCard";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const WEEK_KEY = "Weekly";
let timeMap = {};
timeMap[HOUR_KEY] = "hour";
timeMap[DAY_KEY] = "day";
timeMap[WEEK_KEY] = "week";

const Analytics = () => {
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Analytics: Page under construction`;
    }
  }, []);

  const [timeRange, setTimeRange] = useState(HOUR_KEY);
  const { nftCache } = useNFTs();

  if (nftCache.isLoading) return <Spinner />;

  return (
    <Scrollable>
      <Flex
        h="100%"
        w="100%"
        m={0}
        px="7%"
        direction="column"
        alignItems="center"
        minH="100vh"
      >
        <Heading as="h1" py={4}>
          NFT market analysis
        </Heading>
        <RangeSelector
          placeSelf="flex-start"
          initialRange={timeRange}
          ranges={Object.keys(timeMap)}
          onChange={(e) => setTimeRange(e)}
        />
        <Stack
          w="100%"
          wrap="wrap"
          my={12}
          h="auto"
          direction="row"
          minW="240px"
          spacing={[2, 0, null]}
          boxShadow="md"
          borderRadius="lg"
          bgColor="gray.100"
        >
          <StatsCard
            labelKey="transactions"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Number of transactions"
          />
          <StatsCard
            labelKey="values"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Value of transactions"
          />
          <StatsCard
            labelKey="mints"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Minted NFTs"
          />
        </Stack>
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
