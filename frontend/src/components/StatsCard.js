import React, { useEffect, useState } from "react";
import { Stack, Text, chakra, Box, SimpleGrid, Link } from "@chakra-ui/react";
import { TriangleDownIcon, TriangleUpIcon } from "@chakra-ui/icons";
import useNFTs from "../core/hooks/useNFTs";

const isNumberNonzeroAndFinite = (str) => {
  return !(isNaN(Number(str)) || Number(str) === 0);
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

  let item = lookup
    .slice()
    .reverse()
    .find(function (element) {
      return num >= element.value;
    });
  return item ? (num / item.value).toFixed(digits) + item.symbol : "0";
};

const getChange = (a, b) => {
  console.log(`change:`, a, b);
  if (isNumberNonzeroAndFinite(a) && isNumberNonzeroAndFinite(b)) {
    let retval = (Math.abs(Number(a) - Number(b)) * 100) / Number(b);
    retval =
      Math.abs(retval) > 9999 ? nFormatter(retval, 2) : retval.toFixed(2);
    console.log(`change returns:`, retval);
    return retval;
  } else {
    return "-";
  }
};

const getDiff = (a, b) => {
  if (isNaN(a) || isNaN(b)) {
    return "-";
  } else {
    return Number(Number(a) - Number(b)).toFixed(2);
  }
};

const isZeroOrPositive = (a) => {
  if (isNaN(a)) return "-";
  return Number(a) >= 0 ? true : false;
};

const StatsCard_ = ({
  className,
  label,
  netLabel,
  labelKey,
  totalKey,
  timeRange,
  innerRef,
}) => {
  console.log("stats card");
  const { nftCache } = useNFTs();

  const [nftData, setData] = useState();

  useEffect(() => {
    if (nftCache.data) {
      const resolution =
        timeRange === "hour" ? 1 : timeRange === "day" ? 24 : 24 * 7;

      let currentPeriod = 0,
        previousPeriod = 0,
        currentTotalPeriod = 0,
        previousTotalPeriod = 0;
      for (let i = 0; i < resolution; i++) {
        currentPeriod += Number(nftCache.data[i][labelKey]);
        previousPeriod += Number(nftCache.data[resolution + i][labelKey]);
        if (totalKey) {
          currentTotalPeriod += Number(nftCache.data[i][totalKey]);
          previousTotalPeriod += Number(
            nftCache.data[resolution + i][totalKey]
          );
        }
      }
      console.log(
        "card,",
        totalKey,
        labelKey,
        currentPeriod,
        currentTotalPeriod
      );
      // percentage =
      // const cacheData = nftCache.data[TIME_PERIOD.current][labelKey][timeRange];
      // const prevCacheData =
      //   nftCache.data[TIME_PERIOD.previous][labelKey][timeRange];
      const valueChange = getChange(currentPeriod, previousPeriod);
      totalKey &&
        console.log(
          "getting change in share",
          labelKey,
          currentPeriod,
          currentTotalPeriod
        );

      const share = !totalKey
        ? "-"
        : Number((currentPeriod * 100) / currentTotalPeriod).toFixed(2);
      const shareChange = getDiff(
        share,
        Number((previousPeriod * 100) / previousTotalPeriod).toFixed(2)
      );
      totalKey && console.log("share", share);

      setData({
        dimension: labelKey === "nft_transfer_value" ? "$" : "#",
        isValueIncrease: isZeroOrPositive(valueChange),
        isShareIncrease: isZeroOrPositive(shareChange),
        valueChange,
        shareChange,
        share,
        value:
          labelKey === "nft_transfer_value"
            ? nFormatter((currentPeriod / 1e18) * 3473.13, 2)
            : // ? getEthValue(currentPeriod)
              nFormatter(currentPeriod, 2),
      });
    }
  }, [nftCache?.data, nftCache.isLoading, labelKey, totalKey, timeRange]);
  console.log("nftData", nftData);
  if (nftCache.isLoading || !nftData) return "";

  return (
    <Stack className={className} ref={innerRef}>
      <Box
        id="nft-card-title"
        w="full"
        borderRadius="base"
        fontWeight="600"
        bgColor="gray.200"
        textAlign="center"
        fontSize={["sm", "md", null]}
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
          fontSize={["1rem", "1.125rem", null]}
          borderStyle="dashed"
          borderRightWidth="3px"
          borderRightColor="gray.300"
          //   alignItems="center"
          h="100%"
          id="nft-card-value"
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
          fontSize={["1rem", "1.125rem", null]}
          placeContent="center"
          alignItems="center"
          id="nft-card-value-change"
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
              fontSize={["0.625rem", "0.825rem", null]}
              id="nft-card-share-label"
            >
              Total share in {netLabel}
            </Text>
            <Text id="nft-card-share-value">{nftData.share}%</Text>
            <Stack
              direction="row"
              placeContent="center"
              alignItems="center"
              id="nft-card-share-change"
            >
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
    // borderRightWidth: "1px",
    borderRightColor: "gray.600",
    w: "240px",
    minW: "240px",
    flexBasis: "240px",
    flexGrow: 1,
  },
});

export default React.forwardRef((props, ref) => (
  <StatsCard innerRef={ref} {...props} />
));
