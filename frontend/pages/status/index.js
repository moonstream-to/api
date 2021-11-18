import React from "react";
import { useStatus } from "../../src/core/hooks";
import { Heading, Text, Flex, Spacer, chakra, Spinner } from "@chakra-ui/react";
import { getLayout } from "../../src/layouts/InfoPageLayout";

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

  const StatusRow = (props) => {
    console.log(props.cache.data);
    return (
      <Flex mb={3}>
        <Text>{props.title}</Text>
        <Spacer />
        {!props.cache.isLoading && props.children}
        {props.cache.isLoading && <Spinner m={0} p={0} size="sm" />}
      </Flex>
    );
  };
  return (
    <>
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
        <StatusRow title="Backend server" cache={apiServerStatusCache}>
          <Text
            color={
              apiServerStatusCache?.data?.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {apiServerStatusCache?.data?.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <br />
        <StatusRow
          title="Crawlers server"
          cache={ethereumClusterServerStatusCache}
        >
          <Text
            color={
              ethereumClusterServerStatusCache?.data?.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {ethereumClusterServerStatusCache?.data
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Latest block in Geth" cache={gethStatusCache}>
          <Text>
            {gethStatusCache?.data?.current_block
              ? gethStatusCache.data.current_block
              : 0}
          </Text>
        </StatusRow>
        <StatusRow title="Txpool latest record ts" cache={crawlersStatusCache}>
          <Text>
            {crawlersStatusCache?.data?.ethereum_txpool_timestamp
              ? shortTimestamp(
                  crawlersStatusCache?.data?.ethereum_txpool_timestamp
                )
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow
          title="Trending latest record ts"
          cache={crawlersStatusCache}
        >
          <Text>
            {crawlersStatusCache?.data?.ethereum_trending_timestamp
              ? shortTimestamp(
                  crawlersStatusCache?.data?.ethereum_trending_timestamp
                )
              : downStatusText}
          </Text>
        </StatusRow>

        <br />
        <StatusRow title="Database server" cache={dbServerStatusCache}>
          <Text
            color={
              dbServerStatusCache?.data?.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {dbServerStatusCache?.data?.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow
          title="Latest block in Database"
          cache={latestBlockDBStatusCache}
        >
          <Text>
            {latestBlockDBStatusCache?.data?.block_number
              ? latestBlockDBStatusCache.data.block_number
              : 0}
          </Text>
        </StatusRow>
      </chakra.span>
    </>
  );
};

Status.getLayout = getLayout;
export default Status;
