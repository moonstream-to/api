import React, { useContext } from "react";
import { Flex, HStack, Skeleton, Heading } from "@chakra-ui/react";
import { useTxInfo } from "../core/hooks";
import FourOFour from "./FourOFour";
import FourOThree from "./FourOThree";
import Tags from "./Tags";
import Scrollable from "./Scrollable";
import TxInfo from "./TxInfo";
import UIContext from "../core/providers/UIProvider/context";

const SteamEntryDetails = () => {
  const ui = useContext(UIContext);

  const {
    data: entry,
    isFetchedAfterMount,
    isLoading,
    isFetching, //If transaction.tx is undefined, will not fetch
    isError,
    error,
  } = useTxInfo({ tx: ui.currentTransaction });
  if (!isFetching) {
    return "";
  }
  if (isError && error.response.status === 404) return <FourOFour />;
  if (isError && error.response.status === 403) return <FourOThree />;

  return (
    <Flex id="Entry" height="100%" flexGrow="1" flexDirection="column">
      <Skeleton
        id="EntryNameSkeleton"
        mx={2}
        mt={2}
        overflow="initial"
        isLoaded={!isLoading}
      >
        <HStack id="EntryHeader" width="100%" m={0}>
          <Heading
            width={entry?.context_url ? "calc(100% - 28px)" : "100%"}
            minH="36px"
            style={{ marginLeft: "0" }}
            m={0}
            p={0}
            fontWeight="600"
            fontSize="md"
            textAlign="left"
          >
            {entry && `Hash: ${entry.tx.hash}`}
          </Heading>
        </HStack>
      </Skeleton>
      <Skeleton
        id="TagsSkeleton"
        mx={2}
        overflow="initial"
        mt={1}
        isLoaded={isFetchedAfterMount || entry}
      >
        <Tags entry={entry} />
      </Skeleton>
      <Skeleton
        height="10px"
        flexGrow={1}
        id="EditorSkeleton"
        mx={2}
        mr={isFetchedAfterMount || entry ? 0 : 2}
        mt={1}
        isLoaded={isFetchedAfterMount || entry}
      >
        <Scrollable>
          {!isLoading && <TxInfo transaction={entry}></TxInfo>}
        </Scrollable>
      </Skeleton>
    </Flex>
  );
};

export default SteamEntryDetails;
