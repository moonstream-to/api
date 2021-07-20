import React from "react";
import { Flex, Link, HStack, Skeleton, Box, Heading } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { useJournalEntry, useRouter } from "../../src/core/hooks";
import FourOFour from "../../src/components/FourOFour";
import FourOThree from "../../src/components/FourOThree";
import Tags from "../../src/components/Tags";
import CustomIcon from "../../src/components/CustomIcon";
import { getLayout } from "../../src/layouts/EntriesLayout";
import MarkdownView from "react-showdown";
import Scrollable from "../../src/components/Scrollable";

const Entry = () => {
  const showdownHighlight = require("showdown-highlight");
  const router = useRouter();
  const { entryId } = router.params;
  const journalId = `9b0d7567-4634-4bf7-946d-60ef4414aa93`;
  const {
    data: entry,
    isFetchedAfterMount,
    isLoading,
    isError,
    error,
  } = useJournalEntry(journalId, entryId, "personal");

  const contextUrl = () => {
    if (entry?.context_url) {
      switch (entry.context_type) {
        case "slack":
          return (
            <Link href={entry.context_url} isExternal>
              <CustomIcon width="28px" icon="slack" />
            </Link>
          );
        case "github":
          return (
            <Link href={entry.context_url} isExternal>
              <CustomIcon width="28px" icon="github" />
            </Link>
          );
        default:
          return (
            <Link href={entry.context_url} isExternal>
              <ExternalLinkIcon bg="none" boxSize="18px" />
            </Link>
          );
      }
    } else return "";
  };

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
          <Box
            id="ContextURL"
            transition="0.3s"
            _hover={{ transform: "scale(1.2)" }}
            pl={2}
            pr={entry?.context_url ? 2 : 0}
          >
            {contextUrl()}
          </Box>
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
            {entry?.title}
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
          <MarkdownView
            markdown={entry?.content}
            options={{ tables: true, emoji: true }}
            extensions={showdownHighlight()}
          />
        </Scrollable>
      </Skeleton>
    </Flex>
  );
};

Entry.getLayout = getLayout;
export default Entry;
