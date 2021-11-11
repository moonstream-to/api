import React, {
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
} from "react";
import { getLayout } from "../../src/layouts/AppLayout";
import { Spinner, Flex, Heading, Stack, Text, Spacer } from "@chakra-ui/react";
import Scrollable from "../../src/components/Scrollable";
import RangeSelector from "../../src/components/RangeSelector";
// import StatsCard from "../src/components/StatsCard";
import useWindowSize from "../../src/core/hooks/useWindowSize";
import useDashboard from "../../../src/core/hooks/useDashboard";
// import NFTChart from "../src/components/NFTChart";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
// const WEEK_KEY = "Weekly";
let timeMap = {};
timeMap[HOUR_KEY] = "hour";
timeMap[DAY_KEY] = "day";
// timeMap[WEEK_KEY] = "week";

const Analytics = () => {
  const windowSize = useWindowSize();
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `NFT Analytics`;
    }
  }, []);

  const [nodesReady, setNodeReady] = useState({
    ntx: false,
    values: false,
    mints: false,
    NFTOwners: false,
    minters: false,
  });

  const nTxRef_ = useRef();
  const valueRef_ = useRef();
  const mintsRef_ = useRef();
  const uniqueNFTOwnersRef_ = useRef();
  const mintersRef_ = useRef();

  //   const nTxRef = useCallback(
  //     (node) => {
  //       if (node !== null && !nodesReady.ntx) {
  //         setNodeReady({ ...nodesReady, ntx: true });
  //         nTxRef_.current = node;
  //       }
  //     },
  //     [nodesReady]
  //   );
  //   const valueRef = useCallback(
  //     (node) => {
  //       if (node !== null && !nodesReady.values) {
  //         setNodeReady({ ...nodesReady, values: true });
  //         valueRef_.current = node;
  //       }
  //     },
  //     [nodesReady]
  //   );
  //   const mintsRef = useCallback(
  //     (node) => {
  //       if (node !== null && !nodesReady.mints) {
  //         setNodeReady({ ...nodesReady, mints: true });
  //         mintsRef_.current = node;
  //       }
  //     },
  //     [nodesReady]
  //   );

  //   const uniqueNFTOwnersRef = useCallback(
  //     (node) => {
  //       if (node !== null && !nodesReady.NFTOwners) {
  //         setNodeReady({ ...nodesReady, NFTOwners: true });
  //         uniqueNFTOwnersRef_.current = node;
  //       }
  //     },
  //     [nodesReady]
  //   );

  //   const mintersRef = useCallback(
  //     (node) => {
  //       if (node !== null && !nodesReady.minters) {
  //         setNodeReady({ ...nodesReady, minters: true });
  //         mintersRef_.current = node;
  //       }
  //     },
  //     [nodesReady]
  //   );

  const [timeRange, setTimeRange] = useState(HOUR_KEY);
  const { dashboardCache } = useDashboard();

  //   useLayoutEffect(() => {
  //     const items = [
  //       nTxRef_,
  //       valueRef_,
  //       mintsRef_,
  //       uniqueNFTOwnersRef_,
  //       mintersRef_,
  //     ];
  //     console.log("useeffect fired");
  //     if (items.some((item) => !!item.current)) {
  //       console.log("brder fun");
  //       var firstItemInCurrentRow = items[0];
  //       items.forEach((item) => {
  //         if (item.current) {
  //           if (item !== firstItemInCurrentRow) {
  //             // Check if the current item is at the same
  //             // height as the first item in the current row.
  //             if (
  //               item.current.offsetTop === firstItemInCurrentRow.current.offsetTop
  //             ) {
  //               item.current.style.borderLeft =
  //                 "3px dashed var(--chakra-colors-gray-600)";
  //             } else {
  //               // This item was lower, it must be
  //               // the first in a new row.
  //               firstItemInCurrentRow = item;
  //               item.current.style.borderLeft = "0px dashed black";
  //             }
  //           }
  //         } else {
  //           firstItemInCurrentRow = item;
  //         }
  //       });
  //     }
  //   }, [nodesReady, windowSize]);

  if (dashboardCache.isLoading) return <Spinner />;

  const plotMinW = "500px";

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
        <Stack direction="row" w="100%" placeItems="center">
          <Heading as="h1" py={2} fontSize={["md", "xl"]}>
            NFT market analysis
          </Heading>
          <Spacer />
          <RangeSelector
            initialRange={timeRange}
            ranges={Object.keys(timeMap)}
            size={["sm", "md", null]}
            onChange={(e) => setTimeRange(e)}
          />
        </Stack>
        <Stack
          w="100%"
          wrap="wrap"
          my={2}
          h="auto"
          direction="row"
          minW="240px"
          spacing={[0, 0, null]}
          boxShadow="md"
          borderRadius="lg"
          bgColor="gray.100"
        >
          {/* <StatsCard
            ref={(node) => nTxRef(node)}
            labelKey="nft_transfers"
            totalKey="num_transactions"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Number of NFT purchases"
          />
          <StatsCard
            ref={(node) => valueRef(node)}
            labelKey="nft_transfer_value"
            totalKey="total_value"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Money spent"
          />
          <StatsCard
            ref={(node) => mintsRef(node)}
            labelKey="nft_mints"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="NFTs created"
          />
          <StatsCard
            ref={(node) => uniqueNFTOwnersRef(node)}
            labelKey="nft_owners"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Number of buyers"
          />

          <StatsCard
            ref={(node) => mintersRef(node)}
            labelKey="nft_minters"
            timeRange={timeMap[timeRange]}
            netLabel="Ethereum mainnet"
            label="Number of creators"
          /> */}
        </Stack>
        <Flex w="100%" direction="row" flexWrap="wrap-reverse">
          <Flex
            flexBasis={plotMinW}
            flexGrow={1}
            minW={plotMinW}
            minH="320px"
            maxH="420px"
            direction="column"
            boxShadow="md"
            m={2}
          >
            <Text
              w="100%"
              py={2}
              bgColor="gray.50"
              fontWeight="600"
              textAlign="center"
            >
              New NFTs
            </Text>
            {/* <NFTChart keyPosition={`nft_mints`} timeRange={timeRange} /> */}
          </Flex>
          <Flex
            flexBasis={plotMinW}
            flexGrow={1}
            minW={plotMinW}
            minH="320px"
            maxH="420px"
            direction="column"
            boxShadow="md"
            m={2}
          >
            <Text
              w="100%"
              py={2}
              bgColor="gray.50"
              fontWeight="600"
              textAlign="center"
            >
              NFT creators
            </Text>
            {/* <NFTChart keyPosition={`nft_minters`} timeRange={timeRange} /> */}
          </Flex>
          <Flex
            flexBasis={plotMinW}
            flexGrow={1}
            minW={plotMinW}
            minH="320px"
            maxH="420px"
            direction="column"
            boxShadow="md"
            m={2}
          >
            <Text
              w="100%"
              py={2}
              bgColor="gray.50"
              fontWeight="600"
              textAlign="center"
            >
              NFT Buyers
            </Text>
            {/* <NFTChart keyPosition={`nft_owners`} timeRange={timeRange} /> */}
          </Flex>
          <Flex
            flexBasis={plotMinW}
            flexGrow={1}
            minW={plotMinW}
            minH="320px"
            maxH="420px"
            direction="column"
            boxShadow="md"
            m={2}
          >
            <Text
              w="100%"
              py={2}
              bgColor="gray.50"
              fontWeight="600"
              textAlign="center"
            >
              Transaction volume
            </Text>
            {/* <NFTChart
              keyPosition={`nft_transfers`}
              keyTotal={`num_transactions`}
              timeRange={timeRange}
            /> */}
          </Flex>

          <Flex
            flexBasis={plotMinW}
            flexGrow={1}
            minW={plotMinW}
            minH="320px"
            maxH="420px"
            direction="column"
            boxShadow="md"
            m={2}
          >
            <Text
              w="100%"
              py={2}
              bgColor="gray.50"
              fontWeight="600"
              textAlign="center"
            >
              Transaction value
            </Text>
            {/* <NFTChart
              keyPosition={`nft_transfer_value`}
              keyTotal={`total_value`}
              timeRange={timeRange}
            /> */}
          </Flex>
        </Flex>
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
