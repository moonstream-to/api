import {
  React,
  useState,
  useContext,
  useRef,
  useLayoutEffect,
  useEffect,
} from "react";
import {
  Input,
  InputLeftElement,
  InputGroup,
  Box,
  Flex,
  chakra,
  InputRightElement,
  Menu,
  MenuItem,
  MenuList,
  MenuButton,
  Button,
  Portal,
  MenuGroup,
  Spinner,
} from "@chakra-ui/react";
import { Search2Icon, CloseIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
import { useJournalEntries, useJournals, useRouter } from "../core/hooks";

const SearchBar = (props) => {
  const ui = useContext(UIContext);
  const router = useRouter();
  const { refetch } = useJournalEntries({
    journalId: router.params.id,
    journalType: router.params.appScope,
    pageSize: 25,
    isContent: false,
    searchQuery: ui.searchTerm,
  });

  const [selectedJournal, setSelectedJournal] = useState();
  const [showError, setShowError] = useState(false);
  const [InputFieldValue, setInputFieldValue] = useState(ui.serachTerm ?? "");
  const { journalsCache, publicJournalsCache } = useJournals();

  const inputRef = useRef(null);
  const showSearchBar = !ui.isMobileView || ui.searchBarActive;

  const handleSearch = (e) => {
    e.preventDefault();

    const journalIdToSearchIn =
      selectedJournal?.id ?? router.params.id ?? false;
    const searchAtSameRoute =
      router.params.id &&
      journalIdToSearchIn &&
      router.params.id === journalIdToSearchIn;

    if (journalIdToSearchIn) {
      if (searchAtSameRoute) {
        ui.searchTerm === InputFieldValue
          ? refetch()
          : ui.setSearchTerm(InputFieldValue);
      } else {
        const newQuery = { ...router.nextRouter.query };
        newQuery.id = selectedJournal.id;
        newQuery.appScope = selectedJournal.isPublic ? "public" : "personal";

        delete newQuery.entryId;
        ui.setSearchTerm(InputFieldValue);
        router.push({ pathname: "/stream/", query: newQuery }, undefined, {
          shallow: false,
        });
      }
    } else {
      setShowError(true);
    }
  };

  useLayoutEffect(() => {
    showError && setTimeout(() => setShowError(false), 200);
  }, [showError]);

  useEffect(() => {
    const cache =
      router.params.appScope === "personal"
        ? publicJournalsCache
        : journalsCache;
    if (router.params.id && !cache.isLoading) {
      const newJournal = cache.data.find(
        (journal) => journal.id === router.params.id
      );
      newJournal && setSelectedJournal(newJournal);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router.params.id, journalsCache, publicJournalsCache]);

  useLayoutEffect(() => {
    if (ui.searchTerm !== InputFieldValue) {
      setInputFieldValue(ui.searchTerm);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ui.searchTerm]);

  const handleBlur = (e) => {
    const currentTarget = e.currentTarget;

    // Check the newly focused element in the next tick of the event loop
    setTimeout(() => {
      // Check if the new activeElement is a child of the original container
      if (
        !currentTarget.contains(document.activeElement) &&
        !document.activeElement.className.includes("bugout-search-bar")
      ) {
        // You can invoke a callback or add custom logic here
        ui.setSearchBarActive(false);
      }
    }, 100);
  };

  const handleLeftElementClick = () => {
    if (!showSearchBar) {
      ui.setSearchBarActive(true);
    }
    inputRef.current.focus();
  };

  const handleCloseSearchBar = () => {
    ui.setSearchBarActive(false);
    ui.setSearchTerm("");
  };

  return (
    <Flex {...props} transition="1s">
      <form
        onSubmit={(e) => handleSearch(e)}
        style={{ width: "100%", height: "100%" }}
      >
        <InputGroup
          bgColor={showSearchBar ? "white" : "transparent"}
          borderRadius="lg"
          overflow="hidden"
          h="100%"
          w="100%"
          onFocus={() => {
            ui.setSearchBarActive(true);
          }}
          onBlur={handleBlur}
        >
          <InputLeftElement
            onClick={() => handleLeftElementClick()}
            minW="48px"
            w="fit-content"
            position="static"
            justifySelf="flex-start"
            h="100%"
            overflowY="visible"
            transform="1s"
          >
            {!ui.searchBarActive && (
              <Search2Icon
                color={showSearchBar ? "primary.1200" : "white.100"}
              />
            )}
            {ui.searchBarActive && (
              <Menu>
                <MenuButton
                  as={Button}
                  variant="ghost"
                  colorScheme="primary"
                  h="100%"
                  m={0}
                  borderRightRadius={0}
                  transition="0.05s"
                  className="bugout-search-bar"
                  bgColor={showError ? "unsafe.900" : "primary.100"}
                  textColor={showError ? "white.100" : "primary.900"}
                >
                  {`Search in: ${
                    router.params.id && !selectedJournal?.name
                      ? "current"
                      : selectedJournal?.name ?? "Select one"
                  }`}
                </MenuButton>
                <Portal>
                  <MenuList
                    overflowY="scroll"
                    maxH="300px"
                    className="bugout-search-bar"
                  >
                    {router.params.id && (
                      <MenuItem
                        className="bugout-search-bar"
                        onClick={() =>
                          setSelectedJournal(
                            journalsCache.data.filter(
                              (journal) => journal.id === router.params.id
                            )[0]
                          )
                        }
                      >
                        Current
                      </MenuItem>
                    )}
                    <MenuGroup textColor="gray" title="personal  journals">
                      {journalsCache.isLoading && <Spinner />}
                      {!journalsCache.isLoading &&
                        journalsCache.data.map((journal, idx) => (
                          <MenuItem
                            className="bugout-search-bar"
                            key={`journal-search-list-${idx}`}
                            onClick={() =>
                              setSelectedJournal({
                                ...journal,
                                isPublic: false,
                              })
                            }
                          >
                            {journal.name}
                          </MenuItem>
                        ))}
                    </MenuGroup>
                    <MenuGroup textColor="gray" title="public  journals">
                      {publicJournalsCache.isLoading && <Spinner />}
                      {!publicJournalsCache.isLoading &&
                        publicJournalsCache.data.map((journal, idx) => (
                          <MenuItem
                            className="bugout-search-bar"
                            key={`public-journal-search-list-${idx}`}
                            onClick={() =>
                              setSelectedJournal({
                                ...journal,
                                isPublic: true,
                              })
                            }
                          >
                            {journal.name}
                          </MenuItem>
                        ))}
                    </MenuGroup>
                  </MenuList>
                </Portal>
              </Menu>
            )}
          </InputLeftElement>
          <Input
            hidden={!showSearchBar}
            h="100%"
            px="8px"
            display="flex"
            paddingInlineStart="8px !important"
            sx={{
              WebkitPaddingStart: "8px !important",
              WebkitPaddingEnd: "8px !important",
            }}
            flexBasis="50px"
            flexGrow={1}
            textColor="black"
            ref={inputRef}
            _hover={{ bgColor: "white" }}
            _active={{ bgColor: "white" }}
            _focus={{ bgColor: "white", textColor: "black" }}
            value={InputFieldValue}
            onChange={(e) => setInputFieldValue(e.target.value)}
          />
          <InputRightElement
            h="100%"
            position="static"
            justifySelf="flex-end"
            hidden={!ui.searchBarActive}
          >
            <Box
              onClick={() => handleCloseSearchBar()}
              transition="1s"
              _hover={{ transform: "scale(1.2)" }}
            >
              <CloseIcon color="primary.1200" />
            </Box>
          </InputRightElement>
        </InputGroup>
      </form>
    </Flex>
  );
};

const ChakraSearchBar = chakra(SearchBar);

export default ChakraSearchBar;
