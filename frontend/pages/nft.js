import React, { useEffect, useState } from "react";
import { getLayout } from "../src/layouts/AppLayout";
import { Spinner, Flex, Heading, Stack } from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";
import useNFTs from "../src/core/hooks/useNFTs";
import RangeSelector from "../src/components/RangeSelector";
import { TIME_RANGE_SECONDS } from "../src/core/constants";
import StatsCard from "../src/components/StatsCard";
import web3 from "web3";

const TIME_PERIOD = {
  current: 0,
  previous: 1,
};

const Analytics = () => {
  const fromNNCtoDWM = (range) => {
    const timeMap = {
      "1h": "hour",
      "24h": "day",
      "7d": "week",
      "28d": "month",
    };

    return timeMap[`${range}`];
  };
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Analytics: Page under construction`;
    }
  }, []);

  const [timeRange, setTimeRange] = useState("24h");
  const { nftCache } = useNFTs(TIME_RANGE_SECONDS[fromNNCtoDWM(timeRange)]);

  if (nftCache.isLoading) return <Spinner />;

  const StatCardsData = {};

  Object.keys(nftCache.data[TIME_PERIOD.current]).map((key) => {
    let value, prevValue, valueChange, share, prevShare, shareChange;
    if (key !== "crawled_at") {
      switch (key) {
        case "blocks":
          value =
            Number(
              nftCache.data[TIME_PERIOD.current][`${key}`][
                fromNNCtoDWM(timeRange)
              ].end
            ) -
            Number(
              nftCache.data[TIME_PERIOD.current][`${key}`][
                fromNNCtoDWM(timeRange)
              ].start
            );
          prevValue =
            Number(
              nftCache.data[TIME_PERIOD.previous][`${key}`][
                fromNNCtoDWM(timeRange)
              ].end
            ) -
            Number(
              nftCache.data[TIME_PERIOD.previous][`${key}`][
                fromNNCtoDWM(timeRange)
              ].start
            );
          valueChange = (Math.abs(value - prevValue) * 100) / prevValue;
          StatCardsData[`${key}`] = {
            valueChange,
            value,
            label: `Blocks mined`,
            valueLabel: `${key}`,
            changeLabel: `${timeRange}%`,
            dimension: "#",
            netLabel: "Ethereum mainnet",
          };
          break;
        case "transactions":
          value = Number(
            nftCache.data[TIME_PERIOD.current][`${key}`][
              fromNNCtoDWM(timeRange)
            ].amount
          );
          prevValue = Number(
            nftCache.data[TIME_PERIOD.previous][`${key}`][
              fromNNCtoDWM(timeRange)
            ].amount
          );
          valueChange = (Math.abs(value - prevValue) * 100) / prevValue;
          value = value.toExponential(2);

          share = Number(
            nftCache.data[TIME_PERIOD.current][`${key}`][
              fromNNCtoDWM(timeRange)
            ].percentage
          );

          prevShare = Number(
            nftCache.data[TIME_PERIOD.previous][`${key}`][
              fromNNCtoDWM(timeRange)
            ].percentage
          );

          shareChange = prevShare - share;

          StatCardsData[`${key}`] = {
            valueChange,
            value,
            label: `Number of transactions`,
            valueLabel: `${key}`,
            changeLabel: `${timeRange}%`,
            dimension: "#",
            share,
            shareChange,
            netLabel: "Ethereum mainnet",
          };
          break;
        case "values":
          value = Number(
            web3.utils.fromWei(
              nftCache.data[TIME_PERIOD.current][`${key}`][
                fromNNCtoDWM(timeRange)
              ].amount,
              "ether"
            )
          );
          prevValue = Number(
            web3.utils.fromWei(
              nftCache.data[TIME_PERIOD.previous][`${key}`][
                fromNNCtoDWM(timeRange)
              ].amount,
              "ether"
            )
          );

          share = Number(
            nftCache.data[TIME_PERIOD.current][`${key}`][
              fromNNCtoDWM(timeRange)
            ].percentage
          );

          prevShare = Number(
            nftCache.data[TIME_PERIOD.previous][`${key}`][
              fromNNCtoDWM(timeRange)
            ].percentage
          );

          shareChange = prevShare - share;

          valueChange = (Math.abs(value - prevValue) * 100) / prevValue;

          value = value.toExponential(2);
          StatCardsData[`${key}`] = {
            valueChange,
            value,
            label: `Value of transactions`,
            valueLabel: `${key}`,
            changeLabel: `${timeRange}%`,
            dimension: "Eth",
            share,
            shareChange,
            netLabel: "Ethereum mainnet",
          };
          break;
        case "mints":
          value = Number(
            nftCache.data[TIME_PERIOD.current][`${key}`][
              fromNNCtoDWM(timeRange)
            ].amount
          );
          prevValue = Number(
            nftCache.data[TIME_PERIOD.previous][`${key}`][
              fromNNCtoDWM(timeRange)
            ].amount
          );
          valueChange = (Math.abs(value - prevValue) * 100) / prevValue;
          value = value.toExponential(2);
          StatCardsData[`${key}`] = {
            valueChange,
            value,
            label: `NFTs minted`,
            valueLabel: `${key}`,
            changeLabel: `${timeRange}%`,
            dimension: "#",
            netLabel: "Ethereum mainnet",
          };
          break;
      }
    }
  });


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
          ranges={["1h", "24h", "7d"]}
          onChange={(e) => setTimeRange(e)}
        />
        <Stack
          direction="row"
          wrap="wrap"
          w="100%"
          py={12}
          h="auto"
          spacing={6}
        >
          {Object.keys(StatCardsData).map((key, idx) => {
            return (
              <StatsCard
                key={`nft-stat-card-${key}-${idx}`}
                {...StatCardsData[`${key}`]}
              />
            );
          })}
        </Stack>
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
