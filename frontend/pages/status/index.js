import React from "react";
import { useStatus } from "../../src/core/hooks";
import { Heading, Text, Flex, Spacer, chakra, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/InfoPageLayout";

const Status = () => {
  const healthyStatusText = "Available";
  const downStatusText = "Unavailable";
  const healthyStatusColor = "green.1000";
  const downStatusColor = "red.600";

  const { serverListStatusCache } = useStatus();

  const moonstreamapiStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "moonstream_api"
  )[0];
  const moonstreamCrawlersStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "moonstream_crawlers"
  )[0];
  const nodeBalacerStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "moonstream_node_balancer"
  )[0];
  const nodeEthereumAStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "node_ethereum_a"
  )[0];
  const nodeEthereumBStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "node_ethereum_b"
  )[0];
  const nodePolygonAStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "node_polygon_a"
  )[0];
  const nodePolygonBStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "node_polygon_b"
  )[0];
  const dbServerStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "moonstream_database"
  )[0];
  const dbReplicaServerStatus = serverListStatusCache?.data?.filter(
    (i) => i.name === "moonstream_database_replica"
  )[0];

  const StatusRow = (props) => {
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
        mt="72px"
      >
        {`Status page`}
      </Heading>
      <chakra.span pl={2} px={12} py={2} width="400px">
        <StatusRow title="Backend server" cache={serverListStatusCache}>
          <Text
            color={
              moonstreamapiStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {moonstreamapiStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>

        <br />

        <StatusRow title="Crawlers server" cache={serverListStatusCache}>
          <Text
            color={
              moonstreamCrawlersStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {moonstreamCrawlersStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>

        <br />

        <StatusRow title="Node balancer server" cache={serverListStatusCache}>
          <Text
            color={
              nodeBalacerStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodeBalacerStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>

        <br />

        <StatusRow title="Node Ethereum A" cache={serverListStatusCache}>
          <Text
            color={
              nodeEthereumAStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodeEthereumAStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodeEthereumAStatus?.response?.current_block
              ? nodeEthereumAStatus.response.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Ethereum B" cache={serverListStatusCache}>
          <Text
            color={
              nodeEthereumBStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodeEthereumBStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodeEthereumBStatus?.response?.current_block
              ? nodeEthereumBStatus.response.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Polygon A" cache={serverListStatusCache}>
          <Text
            color={
              nodePolygonAStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodePolygonAStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodePolygonAStatus?.response?.current_block
              ? nodePolygonAStatus.response.current_block
              : 0}
          </Text>
        </StatusRow>
        <br />
        <StatusRow title="Node Polygon B" cache={serverListStatusCache}>
          <Text
            color={
              nodePolygonBStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {nodePolygonBStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Current block" cache={serverListStatusCache}>
          <Text>
            {nodePolygonBStatus?.response?.current_block
              ? nodePolygonBStatus.response.current_block
              : 0}
          </Text>
        </StatusRow>

        <br />

        <StatusRow title="Database server" cache={serverListStatusCache}>
          <Text
            color={
              dbServerStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {dbServerStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Ethereum latest block" cache={serverListStatusCache}>
          <Text>
            {dbServerStatus?.response?.ethereum_block_latest
              ? dbServerStatus.response.ethereum_block_latest
              : 0}
          </Text>
        </StatusRow>
        <StatusRow title="Polygon latest block" cache={serverListStatusCache}>
          <Text>
            {dbServerStatus?.response?.polygon_block_latest
              ? dbServerStatus.response.polygon_block_latest
              : 0}
          </Text>
        </StatusRow>

        <br />

        <StatusRow
          title="Database replica server"
          cache={serverListStatusCache}
        >
          <Text
            color={
              dbReplicaServerStatus?.status_code == 200
                ? healthyStatusColor
                : downStatusColor
            }
          >
            {dbReplicaServerStatus?.status_code == 200
              ? healthyStatusText
              : downStatusText}
          </Text>
        </StatusRow>
        <StatusRow title="Ethereum latest block" cache={serverListStatusCache}>
          <Text>
            {dbReplicaServerStatus?.response?.ethereum_block_latest
              ? dbReplicaServerStatus.response.ethereum_block_latest
              : 0}
          </Text>
        </StatusRow>
        <StatusRow title="Polygon latest block" cache={serverListStatusCache}>
          <Text>
            {dbReplicaServerStatus?.response?.polygon_block_latest
              ? dbReplicaServerStatus.response.polygon_block_latest
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
