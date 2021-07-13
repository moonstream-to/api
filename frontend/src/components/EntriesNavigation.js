
import { jsx } from "@emotion/react";
import { useState, useRef, useEffect, useContext } from "react";
import {
  Box,
  Flex,
  Spinner,
  Container,
  Button,
  VStack,
  Center,
} from "@chakra-ui/react";
import {
  useJournalEntries,
  useRouter,
  useJournalPermissions,
} from "../core/hooks";
import { EntryList, NewEntryModal } from ".";
import UIContext from "../core/providers/UIProvider/context";

const pageSize = 25;
const isContent = false;

const EntriesNavigation = () => {
  const ui = useContext(UIContext);
  const router = useRouter();

  const { currentUserPermissions: permissions } = useJournalPermissions(
    router.params.id,
    router.params.appScope
  );

  const loadMoreButtonRef = useRef(null);
  const { id: journalId, appScope } = router.params;

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
  const [newEntryModal, toggleNewEntryModal] = useState();

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
    ? EntriesPages.map((page) => {
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
      <Flex align="center" height={12} borderColor="white.300">
        {canCreate && (
          <Button
            width="100%"
            variant="solid"
            colorScheme="secondary"
            alignSelf="center"
            height={12}
            m={0}
            borderRadius={0}
            // mb={2}
            onClick={() => toggleNewEntryModal(true)}
          >
            New Entry
          </Button>
        )}
      </Flex>
      {entries && !isLoading ? (
        <Flex
          className="ScrollableWrapper"
          height="100%"
          maxH="100%"
          overflow="hidden"
          direction="column"
          flexGrow={1}
        >
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
            {entries.length === 0 && (
              <Center>
                <VStack>
                  <Container pt={8}>
                    This journal has no entries so far.{" "}
                  </Container>
                  <Button
                    onClick={() => toggleNewEntryModal(true)}
                    variant="outline"
                    colorScheme="suggested"
                  >
                    Create one
                  </Button>
                </VStack>
              </Center>
            )}
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

      {newEntryModal && (
        <NewEntryModal
          toggleModal={toggleNewEntryModal}
          journalId={journalId}
        />
      )}
    </Box>
  );
};

export default EntriesNavigation;
