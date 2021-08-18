import React, {
  useRef,
  useEffect,
  useContext,
  useState,
  useCallback,
} from "react";
import {
  Flex,
  Spinner,
  Button,
  Center,
  Text,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuGroup,
  IconButton,
  Input,
  Select,
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
  useDisclosure,
  Tag,
  TagLabel,
  TagCloseButton,
  Stack,
  Spacer,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import StreamEntry from "./StreamEntry";
import UIContext from "../core/providers/UIProvider/context";
import { FaFilter } from "react-icons/fa";
import useStream from "../core/hooks/useStream";
import { ImCancelCircle } from "react-icons/im";

const FILTER_TYPES = {
  ADDRESS: 0,
  GAS: 1,
  GAS_PRICE: 2,
  AMMOUNT: 3,
  HASH: 4,
  DISABLED: 99,
};
const DIRECTIONS = { SOURCE: "from", DESTINATION: "to" };
const CONDITION = {
  EQUAL: 0,
  CONTAINS: 1,
  LESS: 2,
  LESS_EQUAL: 3,
  GREATER: 4,
  GREATER_EQUAL: 5,
  NOT_EQUAL: 6,
};

const EntriesNavigation = () => {
  const ui = useContext(UIContext);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { subscriptionsCache } = useSubscriptions();
  const [newFilterState, setNewFilterState] = useState([
    {
      type: FILTER_TYPES.ADDRESS,
      direction: DIRECTIONS.SOURCE,
      condition: CONDITION.EQUAL,
      value: null,
    },
  ]);
  const [filterState, setFilterState] = useState([]);

  const loadMoreButtonRef = useRef(null);

  const [streamBoundary, setStreamBoundary] = useState({
    start_time: null,
    end_time: null,
    include_start: false,
    include_end: true,
    next_event_time: null,
    previous_event_time: null,
  });

  const updateStreamBoundaryWith = (pageBoundary) => {
    if (!pageBoundary) {
      return streamBoundary;
    }

    let newBoundary = { ...streamBoundary };
    // We do not check if there is no overlap between the streamBoundary and the pageBoundary - we assume
    // that there *is* an overlap and even if there isn't the stream should gracefully respect the
    // pageBoundary because that was the most recent request the user made.
    // TODO(zomglings): If there is no overlap in boundaries, replace streamBoundary with pageBoundary.
    // No overlap logic:
    // if (<no overlap>) {
    //   setStreamBoundary(pageBoundary)
    //   return pageBoundary
    // }

    if (
      !newBoundary.start_time ||
      (pageBoundary.start_time &&
        pageBoundary.start_time <= newBoundary.start_time)
    ) {
      newBoundary.start_time = pageBoundary.start_time;
      newBoundary.include_start =
        newBoundary.include_start || pageBoundary.include_start;
    }
    newBoundary.include_start =
      newBoundary.include_start || pageBoundary.include_start;

    if (
      !newBoundary.end_time ||
      (pageBoundary.end_time && pageBoundary.end_time >= newBoundary.end_time)
    ) {
      newBoundary.end_time = pageBoundary.end_time;
      newBoundary.include_end =
        newBoundary.include_end || pageBoundary.include_end;
    }

    newBoundary.include_end =
      newBoundary.include_end || pageBoundary.include_end;

    if (
      !newBoundary.next_event_time ||
      !pageBoundary.next_event_time ||
      (pageBoundary.next_event_time &&
        pageBoundary.next_event_time > newBoundary.next_event_time)
    ) {
      newBoundary.next_event_time = pageBoundary.next_event_time;
    }

    if (
      !newBoundary.previous_event_time ||
      !pageBoundary.previous_event_time ||
      (pageBoundary.previous_event_time &&
        pageBoundary.previous_event_time < newBoundary.previous_event_time)
    ) {
      newBoundary.previous_event_time = pageBoundary.previous_event_time;
    }
    setStreamBoundary(newBoundary);
    return newBoundary;
  };

  const { EntriesPages, isLoading, refetch, isFetching, remove } = useStream({
    searchQuery: ui.searchTerm,
    start_time: streamBoundary.start_time,
    end_time: streamBoundary.end_time,
    include_start: streamBoundary.include_start,
    include_end: streamBoundary.include_end,
    updateStreamBoundaryWith: updateStreamBoundaryWith,
    streamBoundary: streamBoundary,
    setStreamBoundary: setStreamBoundary,
    isContent: false,
  });

  useEffect(() => {
    if (!streamBoundary.start_time && !streamBoundary.end_time) {
      refetch();
    }
  }, [streamBoundary, refetch]);

  const setFilterProps = useCallback(
    (filterIdx, props) => {
      const newFilterProps = [...newFilterState];
      newFilterProps[filterIdx] = { ...newFilterProps[filterIdx], ...props };
      setNewFilterState(newFilterProps);
    },
    [newFilterState, setNewFilterState]
  );

  useEffect(() => {
    if (
      subscriptionsCache.data?.subscriptions[0]?.id &&
      newFilterState[0]?.value === null
    ) {
      setFilterProps(0, {
        value: subscriptionsCache?.data?.subscriptions[0]?.address,
      });
    }
  }, [subscriptionsCache, newFilterState, setFilterProps]);

  const entriesPagesData = EntriesPages
    ? EntriesPages.data.map((page) => {
        return page;
      })
    : [""];

  const entries = entriesPagesData.flat();
  const canCreate = false;

  const canDelete = false;

  const dropNewFilterArrayItem = (idx) => {
    const oldArray = [...newFilterState];

    const newArray = oldArray.filter(function (ele) {
      return ele != oldArray[idx];
    });
    setNewFilterState(newArray);
  };

  const dropFilterArrayItem = (idx) => {
    console.log("dropFilterArrayItem", idx, filterState);
    const oldArray = [...filterState];
    const newArray = oldArray.filter(function (ele) {
      return ele != oldArray[idx];
    });

    setFilterState(newArray);
    setNewFilterState(newArray);
    ui.setSearchTerm(
      newArray
        .map((filter) => {
          return filter.direction + ":" + filter.value;
        })
        .join("+")
    );
  };

  const handleFilterSubmit = () => {
    setFilterState(newFilterState);
    ui.setSearchTerm(
      newFilterState
        .map((filter) => {
          return filter.direction + ":" + filter.value;
        })
        .join("+")
    );
    onClose();
  };

  const handleAddressChange = (idx) => (e) => {
    setFilterProps(idx, { value: e.target.value });
  };

  const handleConditionChange = (idx) => (e) => {
    setFilterProps(idx, { condition: parseInt(e.target.value) });
  };

  const handleFilterStateCallback = (props) => {
    console.log("handleFilterStateCallback", props);
    const currentFilterState = [...filterState];
    currentFilterState.push({ ...props });

    ui.setSearchTerm(
      currentFilterState
        .map((filter) => {
          return filter.direction + ":" + filter.value;
        })
        .join("+")
    );

    setFilterState(currentFilterState);
  };
  if (subscriptionsCache.isLoading) return "";

  return (
    <Flex
      id="JournalNavigation"
      height="100%"
      maxH="100%"
      overflow="hidden"
      direction="column"
      flexGrow={1}
    >
      {entries && !isLoading ? (
        <>
          <Drawer onClose={onClose} isOpen={isOpen} size="lg">
            <DrawerOverlay />
            <DrawerContent bgColor="gray.100">
              <DrawerCloseButton />
              <DrawerHeader>{`Filter results`}</DrawerHeader>
              <DrawerBody>
                <Text pt={2} fontWeight="600">
                  Source:
                </Text>
                {newFilterState.map((filter, idx) => {
                  if (filter.type === FILTER_TYPES.DISABLED) return "";
                  return (
                    <Flex
                      key={`subscription-filter-item-${idx}`}
                      direction="column"
                    >
                      <Flex
                        mt={4}
                        direction="row"
                        flexWrap="nowrap"
                        placeItems="center"
                        bgColor="gray.300"
                        borderRadius="md"
                      >
                        {filter.type === FILTER_TYPES.ADDRESS && (
                          <>
                            <Flex w="120px" placeContent="center">
                              {filter.direction === DIRECTIONS.SOURCE
                                ? `From:`
                                : `To:`}
                            </Flex>
                            <Select
                              pr={2}
                              w="180px"
                              onChange={handleConditionChange(idx)}
                            >
                              <option value={CONDITION.EQUAL}>Is</option>
                              <option value={CONDITION.NOT_EQUAL}>
                                Is not
                              </option>
                            </Select>
                            {filter.direction === DIRECTIONS.SOURCE && (
                              <Select
                                variant="solid"
                                colorScheme="primary"
                                name="address"
                                onChange={handleAddressChange(idx)}
                              >
                                {!subscriptionsCache.isLoading &&
                                  subscriptionsCache?.data?.subscriptions.map(
                                    (subscription, idx) => {
                                      return (
                                        <option
                                          value={subscription.address}
                                          key={`subscription-filter-item-${idx}`}
                                        >
                                          {`${
                                            subscription.label
                                          } - ${subscription.address.slice(
                                            0,
                                            5
                                          )}...${subscription.address.slice(
                                            -3
                                          )}`}
                                        </option>
                                      );
                                    }
                                  )}
                              </Select>
                            )}
                            {filter.direction === DIRECTIONS.DESTINATION && (
                              <Input
                                type="text"
                                onChange={(e) =>
                                  setFilterProps(idx, {
                                    value: e.target.value,
                                  })
                                }
                                placeholder="Type in address"
                              />
                            )}
                          </>
                        )}
                        <IconButton
                          placeItems="center"
                          colorScheme="primary"
                          variant="ghost"
                          onClick={() => dropNewFilterArrayItem(idx)}
                          icon={<ImCancelCircle />}
                        />
                      </Flex>
                    </Flex>
                  );
                })}
                <Menu>
                  <MenuButton
                    as={Button}
                    mt={4}
                    colorScheme="secondary"
                    variant="solid"
                  >
                    Add filter row
                  </MenuButton>
                  <MenuList>
                    <MenuGroup title="source"></MenuGroup>
                    <MenuItem
                      onClick={() =>
                        setNewFilterState([
                          ...newFilterState,
                          {
                            type: FILTER_TYPES.ADDRESS,
                            direction: DIRECTIONS.SOURCE,
                            condition: CONDITION.EQUAL,
                            value:
                              subscriptionsCache?.data?.subscriptions[0]
                                ?.address,
                          },
                        ])
                      }
                    >
                      Source
                    </MenuItem>
                    <MenuItem
                      onClick={() =>
                        setNewFilterState([
                          ...newFilterState,
                          {
                            type: FILTER_TYPES.ADDRESS,
                            direction: DIRECTIONS.DESTINATION,
                            condition: CONDITION.EQUAL,
                            value:
                              subscriptionsCache?.data?.subscriptions[0]
                                ?.address,
                          },
                        ])
                      }
                    >
                      Destination
                    </MenuItem>
                  </MenuList>
                </Menu>
              </DrawerBody>
              <DrawerFooter pb={16} placeContent="center">
                <Button
                  colorScheme="suggested"
                  variant="solid"
                  // type="submit"
                  onClick={() => handleFilterSubmit()}
                >
                  Apply selected filters
                </Button>
              </DrawerFooter>
            </DrawerContent>
          </Drawer>
          <Flex h="3rem" w="100%" bgColor="gray.100" alignItems="center">
            <Flex maxW="90%">
              {filterState.map((filter, idx) => {
                if (filter.type === FILTER_TYPES.DISABLED) return "";
                return (
                  <Tag
                    key={`filter-badge-display-${idx}`}
                    mx={1}
                    size="lg"
                    variant="solid"
                    colorScheme="secondary"
                  >
                    {filter?.type === FILTER_TYPES.ADDRESS && (
                      <TagLabel>
                        {filter.condition === CONDITION.NOT_EQUAL && "Not "}
                        {filter.direction === DIRECTIONS.SOURCE
                          ? "From: "
                          : "To: "}
                        {subscriptionsCache?.data?.subscriptions.find(
                          (subscription) =>
                            subscription.address === filter.value
                        )?.label ?? filter.value}
                      </TagLabel>
                    )}

                    <TagCloseButton onClick={() => dropFilterArrayItem(idx)} />
                  </Tag>
                );
              })}
            </Flex>
            <Spacer />
            <IconButton
              mr={4}
              onClick={onOpen}
              colorScheme="primary"
              variant="ghost"
              icon={<FaFilter />}
            />
          </Flex>

          <Flex
            className="ScrollableWrapper"
            w="100%"
            overflowY="hidden"
            h="calc(100% - 3rem)"
          >
            <Flex
              className="Scrollable"
              id="StreamEntry"
              overflowY="scroll"
              direction="column"
              w="100%"
              //onScroll={(e) => handleScroll(e)}
            >
              <Stack direction="row" justifyContent="space-between">
                {!isFetching ? (
                  <Button
                    onClick={() => {
                      remove();
                      setStreamBoundary({
                        start_time: null,
                        end_time: null,
                        include_start: false,
                        include_end: true,
                        next_event_time: null,
                        previous_event_time: null,
                      });
                    }}
                    variant="outline"
                    colorScheme="suggested"
                  >
                    Refresh to newest
                  </Button>
                ) : (
                  <Button
                    isLoading
                    loadingText="Loading"
                    variant="outline"
                    colorScheme="suggested"
                  ></Button>
                )}

                {streamBoundary.next_event_time &&
                streamBoundary.end_time != 0 &&
                !isFetching ? (
                  <Button
                    onClick={() => {
                      updateStreamBoundaryWith({
                        end_time: streamBoundary.next_event_time + 5 * 60,
                        include_start: false,
                        include_end: true,
                      });
                    }}
                    variant="outline"
                    colorScheme="suggested"
                  >
                    Load latest transaction
                  </Button>
                ) : (
                  "" // some strange behaivior without else condition return 0 wich can see on frontend page
                )}
              </Stack>
              {entries
                ?.sort((a, b) => b.timestamp - a.timestamp) // TODO(Andrey) improve that for bi chunks of data sorting can take time
                .map((entry, idx) => (
                  <StreamEntry
                    showOnboardingTooltips={false}
                    key={`entry-list-${idx}`}
                    entry={entry}
                    disableDelete={!canDelete}
                    disableCopy={!canCreate}
                    filterCallback={handleFilterStateCallback}
                    filterConstants={{ DIRECTIONS, CONDITION, FILTER_TYPES }}
                  />
                ))}
              {streamBoundary.previous_event_time && !isFetching ? (
                <Center>
                  <Button
                    onClick={() => {
                      remove();
                      updateStreamBoundaryWith({
                        start_time: streamBoundary.previous_event_time - 5 * 60,
                        include_start: false,
                        include_end: true,
                      });
                    }}
                    variant="outline"
                    colorScheme="suggested"
                  >
                    Go to previous transaction
                  </Button>
                </Center>
              ) : (
                <Center>
                  {!isFetching ? (
                    "Тransactions not found. You can subscribe to more addresses in Subscriptions menu."
                  ) : (
                    <Button
                      isLoading
                      loadingText="Loading"
                      variant="outline"
                      colorScheme="suggested"
                    ></Button>
                  )}
                </Center>
              )}
              {streamBoundary.previous_event_time && isLoading ? (
                <Center>
                  <Spinner
                    //hidden={!isFetchingMore}
                    ref={loadMoreButtonRef}
                    my={8}
                    size="lg"
                    color="primary.500"
                    thickness="4px"
                    speed="1.5s"
                  />
                </Center>
              ) : (
                ""
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
    </Flex>
  );
};

export default EntriesNavigation;
