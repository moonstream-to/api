import React from "react";
import { useStatus } from "../../src/core/hooks";
import { Heading, Text, Flex, Spacer, chakra, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/InfoPageLayout";

const Status = () => {
  const healthyStatusText = "Available";
  const downStatusText = "Unavailable";
  const healthyStatusColor = "green.900";
  const downStatusColor = "red.600";

  const shortTimestamp = (rawTimestamp) => {
    return rawTimestamp.replace(/^.+T/, "").replace(/\..+/, "");
  };

  const {
    serverListStatusCache,
    crawlersStatusCache,
    dbServerStatusCache,
    latestBlockDBStatusCache,
  } = useStatus();

  const moonstreamapiStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "moonstreamapi"
  )[0];
  const moonstreamCrawlersStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "moonstream_crawlers"
  )[0];
  const nodeEthereumAStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_ethereum_a"
  )[0];
  const nodeEthereumAGeth = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_ethereum_a_geth"
  )[0];
  const nodeEthereumBStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_ethereum_b"
  )[0];
  const nodeEthereumBGeth = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_ethereum_b_geth"
  )[0];
  const nodePolygonAStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_polygon_a"
  )[0];
  const nodePolygonAGeth = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_polygon_a_geth"
  )[0];
  const nodePolygonBStatus = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_polygon_b"
  )[0];
  const nodePolygonBGeth = serverListStatusCache?.data?.filter(
    (i) => i.status.name === "node_polygon_b_geth"
  )[0];

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
        <StatusRow title="Backend server" cache={serverListStatusCache}>
          <Text
            color={
              moonstreamapiStatus?.status.body.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {moonstreamapiStatus?.status.body.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>

        <br />

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

        <StatusRow title="Node Ethereum A" cache={serverListStatusCache}>
          <Text
            color={
              nodeEthereumAStatus?.status.body.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodeEthereumAStatus?.status.body.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodeEthereumAGeth?.status.body.current_block
              ? nodeEthereumAGeth.status.body.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Ethereum B" cache={serverListStatusCache}>
          <Text
            color={
              nodeEthereumBStatus?.status.body.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodeEthereumBStatus?.status.body.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodeEthereumBGeth?.status.body.current_block
              ? nodeEthereumBGeth.status.body.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Polygon A" cache={serverListStatusCache}>
          <Text
            color={
              nodePolygonAStatus?.status.body.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodePolygonAStatus?.status.body.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodePolygonAGeth?.status.body.current_block
              ? nodePolygonAGeth.status.body.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Polygon B" cache={serverListStatusCache}>
          <Text
            color={
              nodePolygonBStatus?.status.body.status == "ok"
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodePolygonBStatus?.status.body.status == "ok"
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodePolygonBGeth?.status.body.current_block
              ? nodePolygonBGeth.status.body.current_block
              : 0}
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

export async function getStaticProps() {
  const metaTags = {
    title: "Moonstream: Status page",
    description: "Status of moonstream.to services",
    keywords:
      "blockchain, crypto, data, trading, smart contracts, ethereum, solana, transactions, defi, finance, decentralized, analytics, product, whitepapers",
    url: "https://www.moonstream.to/status",
  };
  const layoutProps = getLayoutProps();
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}
export default Status;
