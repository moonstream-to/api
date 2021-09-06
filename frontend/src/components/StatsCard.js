import React, { useEffect, useState } from "react";
import { Stack, Text, chakra, Box, SimpleGrid, Link } from "@chakra-ui/react";
import { TriangleDownIcon, TriangleUpIcon } from "@chakra-ui/icons";
import useNFTs from "../core/hooks/useNFTs";
import web3 from "web3";

const TIME_PERIOD = {
  current: 0,
  previous: 1,
};

const isNumberNotZero = (str) => {
  if (isNaN(Number(str) || Number(str) == 0)) {
    return false;
  } else {
    return true;
  }
};

const getEthValue = (string) => {
  const ether = web3.utils.fromWei(string, "ether");
  return nFormatter(ether, 3);
};

const nFormatter = (num, digits) => {
  const lookup = [
    { value: 1, symbol: "" },
    { value: 1e3, symbol: "k" },
    { value: 1e6, symbol: "M" },
    { value: 1e9, symbol: "G" },
    { value: 1e12, symbol: "T" },
    { value: 1e15, symbol: "P" },
    { value: 1e18, symbol: "E" },
  ];
  const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  var item = lookup
    .slice()
    .reverse()
    .find(function (item) {
      return num >= item.value;
    });
  return item
    ? (num / item.value).toFixed(digits).replace(rx, "$1") + item.symbol
    : "0";
};

const getChange = (a, b) => {
  if (isNumberNotZero(a) && isNumberNotZero(b)) {
    let retval = (Math.abs(Number(a) - Number(b)) * 100) / Number(b);
    retval = retval > 9999 ? nFormatter(retval, 3) : retval;
    return retval.toFixed(2);
  } else {
    return "-";
  }
};

const getDiff = (a, b) => {
  if (isNaN(a) || isNaN(b)) {
    return "-";
  } else {
    return Number(a) - Number(b);
  }
};

const getSign = (a) => {
  if (isNaN(a)) return "-";
  return Number(a) >= 0 ? true : false;
};
const StatsCard_ = ({ className, label, netLabel, labelKey, timeRange }) => {
  const { nftCache } = useNFTs();

  const [nftData, setData] = useState();

  useEffect(() => {
    if (nftCache.data[TIME_PERIOD.current][labelKey][timeRange]) {
      const cacheData = nftCache.data[TIME_PERIOD.current][labelKey][timeRange];
      const prevCacheData =
        nftCache.data[TIME_PERIOD.previous][labelKey][timeRange];
      const valueChange = getChange(cacheData.amount, prevCacheData.amount);
      const share = isNaN(cacheData.percentage)
        ? "-"
        : Number(cacheData.percentage).toFixed(2);
      const shareChange = getDiff(
        cacheData.percentage,
        prevCacheData.percentage
      );

      setData({
        dimension: labelKey === "values" ? "Eth" : "#",
        isValueIncrease: getSign(valueChange),
        isShareIncrease: getSign(shareChange),
        valueChange,
        shareChange,
        share,
        value:
          labelKey === "values"
            ? getEthValue(cacheData.amount)
            : nFormatter(cacheData.amount, 3),
      });
    }
  }, [nftCache?.data, nftCache.isLoading, labelKey, timeRange]);
  if (nftCache.isLoading || !nftData) return "";

  return (
    <Stack className={className}>
      <Box
        w="full"
        borderTopRadius="inherit"
        fontWeight="600"
        bgColor="gray.200"
        px={4}
        textAlign="center"
      >
        {label}
      </Box>
      <SimpleGrid
        columns={2}
        justifyItems="center"
        textAlign="center"
        h="100%"
        alignContent="center"
      >
        <Box
          w="100%"
          fontSize="1.125rem"
          borderStyle="dashed"
          borderRightWidth="3px"
          borderRightColor="gray.300"
          //   alignItems="center"
          h="100%"
        >
          <Link
            textDecorationLine="underline"
            textDecorationStyle="dashed"
            textUnderlineOffset={2}
            boxDecorationBreak="slice"
            textDecorationThickness="1px"
          >
            {nftData.value}
          </Link>
          <Text pl={2} display="inline-block">
            {nftData.dimension}
          </Text>
        </Box>
        <Stack
          w="100%"
          direction="row"
          fontSize="1.125rem"
          placeContent="center"
          alignItems="center"
        >
          {nftData.isValueIncrease && <TriangleUpIcon color="suggested.900" />}
          {!nftData.isValueIncrease && <TriangleDownIcon color="unsafe.900" />}
          <Text
            textColor={nftData.isValueIncrease ? "suggested.900" : "unsafe.900"}
          >
            {Math.abs(nftData.valueChange)}%
          </Text>
        </Stack>
        {nftData.share !== "-" && nftData.shareChange !== "-" && (
          <>
            <Text
              w="100%"
              borderTopWidth="3px"
              borderTopStyle="dashed"
              borderTopColor="gray.300"
              gridColumn="span 2"
              fontSize="0.825rem"
            >
              Total share in {netLabel}
            </Text>
            <Text>{nftData.share}%</Text>
            <Stack direction="row" placeContent="center" alignItems="center">
              {nftData.isShareIncrease && (
                <TriangleUpIcon color="suggested.900" />
              )}
              {!nftData.isShareIncrease && (
                <TriangleDownIcon color="unsafe.900" />
              )}
              <Text
                textColor={
                  nftData.isShareIncrease ? "suggested.900" : "unsafe.900"
                }
              >
                {nftData.shareChange}%
              </Text>
            </Stack>
          </>
        )}
      </SimpleGrid>
    </Stack>
  );
};

const StatsCard = chakra(StatsCard_, {
  baseStyle: {
    borderStyle: "solid",
    borderRightWidth: "1px",
    borderRightColor: "gray.600",
    w: "240px",
    minW: "240px",
    flexBasis: "240px",
    flexGrow: 1,
  },
});

export default StatsCard;
