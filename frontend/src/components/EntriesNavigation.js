import React, { useRef, useEffect, useContext, useState } from "react";
import { Box, Flex, Spinner, Button, Center, Text } from "@chakra-ui/react";
import { useJournalEntries, useJournalPermissions } from "../core/hooks";
import EntryList from "./EntryList";
import UIContext from "../core/providers/UIProvider/context";

const pageSize = 25;
const isContent = false;

const EntriesNavigation = () => {
  const ui = useContext(UIContext);
  const [mode, setMode] = useState("live");

  const { currentUserPermissions: permissions } = useJournalPermissions(
    `9b0d7567-4634-4bf7-946d-60ef4414aa93`,
    `personal`
  );

  const loadMoreButtonRef = useRef(null);

  const journalId = `9b0d7567-4634-4bf7-946d-60ef4414aa93`;
  const appScope = `personal`;

  const {
    fetchMore,
    isFetchingMore,
    canFetchMore,
    refetch,
    EntriesPages,
    isLoading,
    setSearchTerm,
  } = useJournalEntries({
    journalId,
    journalType: appScope,
    pageSize,
    isContent,
    searchQuery: ui.searchTerm,
  });

  const handleScroll = ({ currentTarget }) => {
    if (
      currentTarget.scrollTop + currentTarget.clientHeight >=
      0.5 * currentTarget.scrollHeight
    ) {
      if (!isFetchingMore && canFetchMore) {
        fetchMore();
      }
    }
  };

  useEffect(() => {
    if (journalId) {
      refetch();
    }
  }, [journalId, ui.searchTerm, refetch, setSearchTerm]);

  const entriesPagesData = EntriesPages
    ? EntriesPages.pages.map((page) => {
        return page.data;
      })
    : [""];

  const entries = entriesPagesData.flat();

  const canCreate =
    appScope !== "public" && permissions?.includes("journals.entries.create");

  const canDelete =
    appScope !== "public" && permissions?.includes("journals.entries.delete");

  return (
    <Box
      id="JournalNavigation"
      height="100%"
      maxH="100%"
      overflow="hidden"
      direction="column"
      flexGrow={1}
    >
      {entries && !isLoading ? (
        <Flex
          className="ScrollableWrapper"
          height="100%"
          maxH="100%"
          overflow="hidden"
          direction="column"
          flexGrow={1}
        >
          <Flex h="3rem">
            <Button
              isActive={mode === "live"}
              colorScheme="secondary"
              bgColor="white.100"
              textColor="primary.900"
              _active={{
                bgColor: "secondary.900",
                textColor: "white.100",
              }}
              _hover={{
                textColor: "white.100",
                bgColor: "secondary.600",
              }}
              m={0}
              h="100%"
              w="50%"
              borderRadius="0"
              onClick={() => setMode("live")}
            >
              Live view
            </Button>
            <Button
              m={0}
              isActive={mode == "analysis"}
              _active={{
                bgColor: "secondary.900",
                textColor: "white.100",
              }}
              _hover={{
                textColor: "white.100",
                bgColor: "secondary.600",
              }}
              bgColor="white.100"
              textColor="primary.900"
              colorScheme="secondary"
              h="100%"
              w="50%"
              onClick={() => setMode("analysis")}
              borderRadius="0"
            >
              Analysis view
            </Button>
          </Flex>
          <Flex h="3rem" w="100%" bgColor="white.200">
            <Flex
              flexBasis="50px"
              flexGrow={1}
              justifyContent="center"
              alignItems="center"
            >
              <Text fontWeight="600">Status</Text>
            </Flex>
            <Flex
              flexBasis="50px"
              flexGrow={1}
              justifyContent="center"
              alignItems="center"
            >
              <Text fontWeight="600">Source</Text>
            </Flex>
            <Flex
              flexBasis="50px"
              flexGrow={1}
              justifyContent="center"
              alignItems="center"
            >
              <Text fontWeight="600">Alias</Text>
            </Flex>
            <Flex
              flexBasis="50px"
              flexGrow={1}
              justifyContent="center"
              alignItems="center"
            >
              <Text fontWeight="600">Ammount</Text>
            </Flex>
            <Flex
              flexBasis="50px"
              flexGrow={1}
              justifyContent="center"
              alignItems="center"
            >
              <Text fontWeight="600">Date</Text>
            </Flex>
          </Flex>
          <Flex
            className="Scrollable"
            id="entryList"
            // flexGrow={1}
            overflowY="scroll"
            direction="column"
            height="100%"
            onScroll={(e) => handleScroll(e)}
          >
            {entries.map((entry) => (
              <EntryList
                key={`entry-list-${entry.id}`}
                entry={entry}
                disableDelete={!canDelete}
                disableCopy={!canCreate}
              />
            ))}
            {canFetchMore && !isFetchingMore && (
              <Center>
                <Button
                  onClick={() => fetchMore()}
                  variant="outline"
                  colorScheme="suggested"
                >
                  Load more entries
                </Button>
              </Center>
            )}
            {canFetchMore && isFetchingMore && (
              <Center>
                <Spinner
                  hidden={!isFetchingMore}
                  ref={loadMoreButtonRef}
                  my={8}
                  size="lg"
                  color="primary.500"
                  thickness="4px"
                  speed="1.5s"
                />
              </Center>
            )}
          </Flex>
        </Flex>
      ) : (
        <Center>
          <Spinner
            mt="50%"
            size="lg"
            color="primary.500"
            thickness="4px"
            speed="1.5s"
          />
        </Center>
      )}
    </Box>
  );
};

export default EntriesNavigation;
