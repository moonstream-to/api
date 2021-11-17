import React, { useContext, useEffect, useState } from "react";
import { getLayout } from "../../src/layouts/AppLayout";
import {
  Spinner,
  Flex,
  Heading,
  Stack,
  Text,
  Spacer,
  IconButton,
} from "@chakra-ui/react";
import Scrollable from "../../src/components/Scrollable";
import RangeSelector from "../../src/components/RangeSelector";
import useDashboard from "../../src/core/hooks/useDashboard";
import { useRouter, useSubscriptions } from "../../src/core/hooks";
import { BiTrash } from "react-icons/bi";
import OverlayContext from "../../src/core/providers/OverlayProvider/context";
import SubscriptionReport from "../../src/components/SubscriptionReport";
import { v4 } from "uuid";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const MINUTE_KEY = "Minutes";
let timeMap = {};
timeMap[DAY_KEY] = "month";
timeMap[HOUR_KEY] = "week";
timeMap[MINUTE_KEY] = "day";

const Analytics = () => {
  const { toggleAlert } = useContext(OverlayContext);

  // const [nodesReady, setNodeReady] = useState({
  //   ntx: false,
  //   values: false,
  //   mints: false,
  //   NFTOwners: false,
  //   minters: false,
  // });

  // const nTxRef_ = useRef();
  // const valueRef_ = useRef();
  // const mintsRef_ = useRef();
  // const uniqueNFTOwnersRef_ = useRef();
  // const mintersRef_ = useRef();

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

  const [timeRange, setTimeRange] = useState(timeMap[MINUTE_KEY]);
  const router = useRouter();
  const { dashboardId } = router.params;
  const { dashboardCache, dashboardLinksCache, deleteDashboard } =
    useDashboard(dashboardId);

  const { subscriptionsCache } = useSubscriptions();

  useEffect(() => {
    if (typeof window !== "undefined") {
      if (dashboardCache?.data?.data?.resource_data?.name) {
        document.title = dashboardCache?.data?.data?.resource_data?.name;
      } else {
        document.title = `Dashboard`;
      }
    }
  }, [dashboardCache?.data?.data?.resource_data?.name]);

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

  if (
    dashboardCache.isLoading ||
    dashboardLinksCache.isLoading ||
    subscriptionsCache.isLoading
  )
    return <Spinner />;

  const plotMinW = "250px";

  return (
    <Scrollable>
      <Flex
        h="100%"
        w="100%"
        m={0}
        px={["10px", "20px", "7%", null]}
        direction="column"
        alignItems="center"
        minH="100vh"
      >
        <Stack direction="row" w="100%" placeItems="center">
          <Heading as="h1" py={2} fontSize={["md", "xl"]}>
            {dashboardCache.data.data.resource_data.name}
          </Heading>
          <Spacer />
          <RangeSelector
            initialRange={MINUTE_KEY}
            ranges={Object.keys(timeMap)}
            size={["sm", "md", null]}
            onChange={(e) => {
              setTimeRange(timeMap[e]);
            }}
          />
          <IconButton
            icon={<BiTrash />}
            variant="ghost"
            colorScheme="red"
            size="sm"
            onClick={() => toggleAlert(() => deleteDashboard.mutate())}
          />
        </Stack>

        <Flex w="100%" direction="row" flexWrap="wrap-reverse" id="container">
          {Object.keys(dashboardLinksCache.data.data).map((key) => {
            const s3PresignedURLs = dashboardLinksCache.data.data[key];
            const name = subscriptionsCache.data.subscriptions.find(
              (subscription) => subscription.id === key
            ).label;
            return (
              <Flex
                key={v4()}
                flexBasis={plotMinW}
                flexGrow={1}
                minW={plotMinW}
                minH="320px"
                direction="column"
                boxShadow="md"
                m={["1px", 2]}
              >
                <Text
                  w="100%"
                  py={2}
                  bgColor="gray.50"
                  fontWeight="600"
                  textAlign="center"
                >
                  {name}
                </Text>
                <SubscriptionReport
                  timeRange={timeRange}
                  url={s3PresignedURLs[timeRange]}
                  id={v4()}
                  type={v4()}
                  refetchLinks={dashboardLinksCache.refetch}
                />
              </Flex>
            );
          })}
        </Flex>
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
