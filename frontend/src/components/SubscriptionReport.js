import React, { useMemo } from "react";
import { usePresignedURL } from "../core/hooks";
import Report from "./Report";

import {
  Spinner,
  Flex,
  Heading,
  Text,
  Container,
  chakra,
  Link,
} from "@chakra-ui/react";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const WEEK_KEY = "Weekly";
let timeMap = {};
timeMap[HOUR_KEY] = "hour";
timeMap[DAY_KEY] = "day";
timeMap[WEEK_KEY] = "week";

const SubscriptionReport = ({
  timeRange,
  presignedRequest,
  id,
  refetchLinks,
  refreshingStatus: refreshingStatus,
  setRefreshingStatus: setRefreshingStatus,
}) => {
  const { data, isLoading, failureCount } = usePresignedURL({
    presignedRequest: presignedRequest,
    isEnabled: true,
    id: id,
    cacheType: `${timeRange} subscription_report`,
    requestNewURLCallback: refetchLinks,
    hideToastOn404: true,
    refreshingStatus: refreshingStatus,
    setRefreshingStatus: setRefreshingStatus,
  });
  const plotMinW = "250px";

  const eventKeys = useMemo(
    () =>
      Object.keys(data?.events ?? {}).length > 0
        ? Object.keys(data?.events)
        : undefined,
    [data]
  );
  const methodKeys = useMemo(
    () =>
      Object.keys(data?.methods ?? {}).length > 0
        ? Object.keys(data?.methods)
        : undefined,
    [data]
  );
  const genericKeys = useMemo(
    () =>
      Object.keys(data?.generic ?? {}).length > 0
        ? Object.keys(data?.generic)
        : undefined,
    [data]
  );

  if (failureCount < 1 && (!data || isLoading)) return <Spinner />;
  if (failureCount >= 1 && (!data || isLoading)) {
    return (
      <Container
        w="100%"
        size="lg"
        bgColor="orange.100"
        borderRadius="md"
        mt={14}
        mb={14}
        p={8}
        boxShadow="md"
      >
        <Heading mb={6}>We are crawling the blockchain </Heading>
        <chakra.span>
          <Text mb={4}>
            It takes about 5 minutes to populate this dashboard.
          </Text>
          <Text>
            If you have been looking at this message for more than 5 minutes,
            contact our team on
            {` `}
            <Link
              color="orange.900"
              isExternal
              href={"https://discord.gg/K56VNUQGvA"}
            >
              Discord
            </Link>
            {"."}
          </Text>
        </chakra.span>
        <br />
      </Container>
    );
  }

  return (
    <Flex
      w="100%"
      h="auto"
      flexGrow={1}
      flexBasis={plotMinW}
      direction="column"
    >
      <Flex
        bgColor="blue.50"
        direction={["column", "row", null]}
        flexWrap="wrap"
        alignContent={["inherit", "flex-start", null]}
      >
        {data?.web3_metric.map((metric, web3MetricIndex) => {
          return (
            <Flex
              flexGrow={1}
              flexBasis="100px"
              placeSelf="center"
              p={2}
              m={1}
              bgColor="blue.100"
              key={`web3-metric-${web3MetricIndex}`}
              size="sm"
              fontWeight="600"
              boxShadow="sm"
              direction="column"
              alignSelf="stretch"
            >
              <Text placeSelf="center">{metric.display_name}</Text>
              <Text
                p={2}
                fontSize={["24px", "24px", "42px", null]}
                placeSelf="center"
              >
                {metric.display_name == "Total weth earned"
                  ? Number.parseFloat(
                      Number.parseFloat(metric.value) / 1e18
                    ).toString()
                  : metric.value}
              </Text>
            </Flex>
          );
        })}
      </Flex>
      {data?.events && eventKeys && (
        <Flex
          w="100%"
          h="auto"
          flexGrow={1}
          flexBasis={plotMinW}
          direction="column"
        >
          <Heading size="md" pt={4}>
            Events
          </Heading>
          {eventKeys.map((key) => {
            return (
              <Flex
                key={`events-list-${key}`}
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
                  {key}
                </Text>
                <Report
                  data={data.events[key]}
                  metric={key}
                  timeRange={timeRange}
                />
              </Flex>
            );
          })}
        </Flex>
      )}
      {data?.functions && methodKeys && (
        <Flex
          w="100%"
          h="auto"
          flexGrow={1}
          flexBasis="420px"
          direction="column"
        >
          <Heading size="md" pt={4}>
            functions
          </Heading>
          {methodKeys.map((key) => {
            return (
              <Flex
                key={`methods-list-${key}`}
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
                  {key}
                </Text>
                <Report
                  data={data.functions[key]}
                  metric={key}
                  timeRange={timeRange}
                />
              </Flex>
            );
          })}
        </Flex>
      )}
      {data?.generic && genericKeys && (
        <Flex
          w="100%"
          h="auto"
          flexGrow={1}
          flexBasis="420px"
          direction="column"
        >
          <Heading size="md" pt={4}>
            Account generic
          </Heading>
          {Object.keys(data.generic).map((key) => {
            return (
              <Flex
                key={`generics-list-${key}`}
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
                  {key}
                </Text>
                <Report
                  data={data.generic[key]}
                  metric={key}
                  timeRange={timeRange}
                />
              </Flex>
            );
          })}
        </Flex>
      )}
    </Flex>
  );
};

export default React.memo(SubscriptionReport);
