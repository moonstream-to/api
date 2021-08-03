import React from "react";
import { Flex, HStack, Skeleton, Box, Heading, Center, Spinner } from "@chakra-ui/react";
import { useTxInfo, useTxCashe, useRouter } from "../../src/core/hooks";
import FourOFour from "../../src/components/FourOFour";
import FourOThree from "../../src/components/FourOThree";
import Tags from "../../src/components/Tags";
import { getLayout } from "../../src/layouts/EntriesLayout";
import Scrollable from "../../src/components/Scrollable";
import TxInfo from "../../src/components/TxInfo"

const Entry = () => {
  const router = useRouter();
  const { entryId } = router.params;
  const txCache = useTxCashe;

  const transaction = txCache.getCurrentTransaction()
  if (!transaction || transaction.hash != entryId) {
      router.push({
        pathname: `/stream/`,
        query: router.query,
      });
      const LoadingSpinner = () => (
        <Box px="12%" my={12} width="100%">
          <Center>
            <Spinner
              hidden={false}
              my={0}
              size="lg"
              color="primary.500"
              thickness="4px"
              speed="1.5s"
            />
          </Center>
        </Box>
      );
      return (
        <LoadingSpinner/>
      )
  }
  const {
    data: entry,
    isFetchedAfterMount,
    isLoading,
    isError,
    error,
  } = useTxInfo({tx:transaction})
  const title = transaction.hash
  if (isError && error.response.status === 404) return <FourOFour />;
  if (isError && error.response.status === 403) return <FourOThree />;
  // if (!entry || isLoading) return "";

  return (
    <Flex
      id="Entry"
      height="100%"
      flexGrow="1"
      flexDirection="column"
      key={entryId}
    >
      <Skeleton
        id="EntryNameSkeleton"
        mx={2}
        mt={2}
        overflow="initial"
        isLoaded={!isLoading}
      >
        <HStack id="EntryHeader" width="100%" m={0}>
          <Heading
            overflow="hidden"
            width={entry?.context_url ? "calc(100% - 28px)" : "100%"}
            // height="auto"
            minH="36px"
            style={{ marginLeft: "0" }}
            m={0}
            p={0}
            fontWeight="600"
            fontSize="1.5rem"
            textAlign="left"
          >
            {title}
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
        {!isLoading && (<TxInfo transaction = {entry}></TxInfo> )}
        </Scrollable>
      </Skeleton>
    </Flex>
  );
};

Entry.getLayout = getLayout;
export default Entry;
