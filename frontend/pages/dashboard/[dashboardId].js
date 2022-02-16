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
  Editable,
  EditableInput,
  EditablePreview,
  Button,
} from "@chakra-ui/react";
import { RepeatIcon } from "@chakra-ui/icons";
import Scrollable from "../../src/components/Scrollable";
import RangeSelector from "../../src/components/RangeSelector";
import useDashboard from "../../src/core/hooks/useDashboard";
import { useRouter, useSubscriptions } from "../../src/core/hooks";
import { BiTrash } from "react-icons/bi";
import OverlayContext from "../../src/core/providers/OverlayProvider/context";
import SubscriptionReport from "../../src/components/SubscriptionReport";
import { DRAWER_TYPES } from "../../src/core/providers/OverlayProvider/constants";
import Page404 from "../../src/components/FourOFour";
import { BsGear } from "react-icons/bs";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const MINUTE_KEY = "Minutes";
let timeMap = {};
timeMap[DAY_KEY] = "month";
timeMap[HOUR_KEY] = "week";
timeMap[MINUTE_KEY] = "day";

const Analytics = () => {
  const { toggleAlert } = useContext(OverlayContext);

  const [timeRange, setTimeRange] = useState(timeMap[DAY_KEY]);
  const router = useRouter();
  const overlay = useContext(OverlayContext);
  const { dashboardId } = router.params;
  const {
    dashboardCache,
    dashboardLinksCache,
    deleteDashboard,
    updateDashboard,
    refreshDashboard,
  } = useDashboard(dashboardId);

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

  const updateCallback = ({ name }) => {
    updateDashboard.mutate({
      id: dashboardCache.data.id,
      dashboard: {
        dashboard_id: dashboardCache.data.id,
        name: name,
        subscription_cache:
          dashboardCache.data.resource_data.subscription_setting,
      },
    });
  };

  if (
    dashboardCache.isLoading ||
    dashboardLinksCache.isLoading ||
    subscriptionsCache.isLoading
  )
    return <Spinner />;

  if (
    dashboardCache.isLoadingError &&
    dashboardCache?.error?.response?.status === 404
  ) {
    return <Page404 />;
  }

  const plotMinW = "250px";

  const refereshCharts = () => {
    refreshDashboard.mutate({
      dashboardId: dashboardCache.data.id,
      timeRange: timeRange,
    });
  };

  const retryCallbackFn = (attempts, status) => {
    if (status === 304 && attempts > 5) {
      refereshCharts();
    }
    return status === 404 || status === 403 ? false : true;
  };

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
        <Stack
          direction={["column", "row", null]}
          w="100%"
          placeItems="center"
          pt={2}
        >
          <Editable
            as={Heading}
            colorScheme="blue"
            placeholder="enter note here"
            defaultValue={dashboardCache.data.resource_data.name}
            onSubmit={(nextValue) =>
              updateCallback({
                name: nextValue,
              })
            }
          >
            <EditablePreview maxW="40rem" _placeholder={{ color: "black" }} />
            <EditableInput maxW="40rem" />
          </Editable>
          <Heading as="h1" py={2} fontSize={["md", "xl"]}></Heading>
          <IconButton
            icon={<BiTrash />}
            variant="ghost"
            colorScheme="red"
            size="sm"
            onClick={() => toggleAlert(() => deleteDashboard.mutate())}
          />
          <Spacer />
          <RangeSelector
            initialRange={DAY_KEY}
            ranges={Object.keys(timeMap)}
            size={["sm", "md", null]}
            onChange={(e) => {
              setTimeRange(timeMap[e]);
            }}
          />
          <IconButton
            onClick={() =>
              overlay.toggleDrawer({
                type: DRAWER_TYPES.NEW_DASHBOARD_ITEM,
                props: dashboardCache.data.resource_data,
              })
            }
            size="md"
            colorScheme="blue"
            variant="outline"
            icon={<BsGear />}
          />
          <IconButton
            isLoading={
              refreshDashboard.isLoading || refreshDashboard.isFetching
            }
            icon={<RepeatIcon />}
            variant="ghost"
            colorScheme="green"
            size="sm"
            onClick={() => {
              refereshCharts();
            }}
          />
        </Stack>

        <Flex w="100%" direction="row" flexWrap="wrap-reverse" id="container">
          <>
            {Object.keys(dashboardLinksCache.data.data)?.map((key) => {
              const s3PresignedURLs = dashboardLinksCache.data.data[key];
              const name = subscriptionsCache.data.subscriptions.find(
                (subscription) => subscription.id === key
              )?.label;
              return (
                <Flex
                  key={`${dashboardId}-subscription-report-${key}-${timeRange}`}
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
                    {name ?? ""}
                  </Text>

                  <SubscriptionReport
                    retryCallbackFn={retryCallbackFn}
                    timeRange={timeRange}
                    presignedRequest={s3PresignedURLs[timeRange]}
                    id={dashboardId}
                    refetchLinks={dashboardLinksCache.refetch}
                  />
                </Flex>
              );
            })}
            {dashboardCache.data.resource_data.subscription_settings[0] ===
              undefined && (
              <Flex pt="220px" w="100%" placeContent="center">
                <Button
                  size="lg"
                  colorScheme="orange"
                  onClick={() =>
                    overlay.toggleDrawer({
                      type: DRAWER_TYPES.NEW_DASHBOARD_ITEM,
                      props: dashboardCache.data.resource_data,
                    })
                  }
                >
                  Populate dashboard
                </Button>
              </Flex>
            )}
          </>
        </Flex>
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
