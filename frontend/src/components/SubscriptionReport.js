import React from "react";
import { usePresignedURL } from "../core/hooks";
import Report from "./Report";
import { Spinner, Flex, Heading, Text } from "@chakra-ui/react";
import { v4 } from "uuid";

const HOUR_KEY = "Hourly";
const DAY_KEY = "Daily";
const WEEK_KEY = "Weekly";
let timeMap = {};
timeMap[HOUR_KEY] = "hour";
timeMap[DAY_KEY] = "day";
timeMap[WEEK_KEY] = "week";

const SubscriptionReport = ({ timeRange, url, id, type, refetchLinks }) => {
  const { data, isLoading } = usePresignedURL({
    url: url,
    isEnabled: true,
    id: id,
    type: type,
    requestNewURLCallback: refetchLinks,
  });
  const plotMinW = "250px";
  if (!data || isLoading) return <Spinner />;
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
        {data?.web3_metric.map((metric) => {
          return (
            <Flex
              flexGrow={1}
              flexBasis="100px"
              placeSelf="center"
              p={2}
              m={1}
              bgColor="blue.100"
              key={v4()}
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
      {data?.events && Object.keys(data?.events) && (
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
          {Object.keys(data.events).map((key) => {
            return (
              <Flex
                key={v4()}
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
      {data?.functions && Object.keys(data?.functions) && (
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
          {Object.keys(data.functions).map((key) => {
            return (
              <Flex
                key={v4()}
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
      {data?.generic && Object.keys(data?.generic) && (
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
                key={v4()}
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

export default SubscriptionReport;
