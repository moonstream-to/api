import React, { useRef, useEffect, useContext } from "react";
import {
  Flex,
  Spinner,
  Button,
  Center,
  Text,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Heading,
} from "@chakra-ui/react";
import { useJournalEntries, useJournalPermissions } from "../core/hooks";
import EntryList from "./EntryList";
import UIContext from "../core/providers/UIProvider/context";
import HubspotForm from "react-hubspot-form";
const pageSize = 25;
const isContent = false;

const EntriesNavigation = () => {
  const ui = useContext(UIContext);

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
    <Flex
      id="JournalNavigation"
      height="100%"
      maxH="100%"
      overflow="hidden"
      direction="column"
      flexGrow={1}
    >
      <Tabs colorScheme="red" variant="solid" isLazy isFitted h="100%">
        <TabList>
          <Tab
            fontWeight="600"
            h="3rem"
            transition="0.5s"
            _hover={{ bg: "secondary.100" }}
            bgColor="white.200"
            _selected={{
              color: "white",
              bg: "secondary.900",
              boxShadow: "lg",
            }}
          >
            Live view
          </Tab>
          <Tab
            fontWeight="600"
            h="3rem"
            transition="0.5s"
            _hover={{ bg: "secondary.100" }}
            bgColor="white.200"
            _selected={{
              color: "white",
              bg: "secondary.900",
              boxShadow: "lg",
            }}
          >
            Analysis
          </Tab>
        </TabList>

        <TabPanels px={0} h="calc(100% - 3rem)">
          <TabPanel p={0} h="100%">
            {entries && !isLoading ? (
              <>
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
                  className="ScrollableWrapper"
                  w="100%"
                  overflowY="hidden"
                  // maxH="100%"
                  h="calc(100% - 3rem)"
                >
                  <Flex
                    className="Scrollable"
                    id="entryList"
                    // flexGrow={1}
                    overflowY="scroll"
                    direction="column"
                    height="100%"
                    w="100%"
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
              </>
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
          </TabPanel>
          <TabPanel>
            <Heading as="h1">This section is under construction</Heading>
            <Heading as="h2" size="sm">Message us to tell your needs for this page</Heading>
            <HubspotForm
              portalId="8018701"
              formId="b9b3da3d-f47d-41da-863c-eb8229c3bfc0"
              loading={<Spinner colorScheme="primary" speed="1s" />}
            />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Flex>
  );
};

export default EntriesNavigation;

{
  /* {entries && !isLoading ? (
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

          {/* {mode === "analysis" && <Flex>tell us morex</Flex>}
          <Fade in={mode === "analysis"}> tell me moar</Fade>
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
      )} */
}
