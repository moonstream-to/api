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
  Spacer,
} from "@chakra-ui/react";
import { useSubscriptions } from "../core/hooks";
import StreamEntry from "./StreamEntry";
import UIContext from "../core/providers/UIProvider/context";
import { FaFilter } from "react-icons/fa";
import useStream from "../core/hooks/useStream";
import { ImCancelCircle } from "react-icons/im";

const pageSize = 25;
const FILTER_TYPES = {
  ADDRESS: 0,
  GAS: 1,
  GAS_PRICE: 2,
  AMMOUNT: 3,
  HASH: 4,
  DISABLED: 99,
};
const DIRECTIONS = { SOURCE: 0, DESTINATION: 1 };
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

  const { fetchMore, isFetchingMore, canFetchMore, EntriesPages, isLoading } =
    useStream({
      pageSize,
      refreshRate: 1500,
      searchQuery: ui.searchTerm,
      enabled: true,
      isContent: false,
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
      newFilterState[0].value === null
    ) {
      setFilterProps(0, {
        value: subscriptionsCache.data.subscriptions[0].address,
      });
    }
  }, [subscriptionsCache, newFilterState, setFilterProps]);

  const entriesPagesData = EntriesPages
    ? EntriesPages.pages.map((page) => {
        return page.data;
      })
    : [""];

  const entries = entriesPagesData.flat();
  const canCreate = false;

  const canDelete = false;

  const dropNewFilterArrayItem = (idx) => {
    const newArray = [...newFilterState];
    delete newArray[idx];
    setNewFilterState(newArray);
  };

  const dropFilterArrayItem = (idx) => {
    const newArray = [...filterState];
    newArray[idx].type = FILTER_TYPES.DISABLED;
    setFilterState(newArray);
  };

  const handleFilterSubmit = () => {
    setFilterState(newFilterState);
    onClose();
  };

  const handleAddressChange = (idx) => (e) => {
    setFilterProps(idx, { value: e.target.value });
  };

  const handleConditionChange = (idx) => (e) => {
    setFilterProps(idx, { condition: parseInt(e.target.value) });
  };

  const handleFilterStateCallback = (props) => {
    const newFilterState = [...filterState];
    newFilterState.push({ ...props });
    setFilterState(newFilterState);
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
                                  subscriptionsCache.data.subscriptions.map(
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
                            value: subscriptionsCache.data.subscriptions[0].id,
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
                            value: null,
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
          <Flex h="3rem" w="100%" bgColor="gray.200" alignItems="center">
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
            // maxH="100%"
            h="calc(100% - 3rem)"
          >
            <Flex
              className="Scrollable"
              id="StreamEntry"
              // flexGrow={1}
              overflowY="scroll"
              direction="column"
              height="100%"
              w="100%"
              onScroll={(e) => handleScroll(e)}
            >
              {entries.map((entry, idx) => (
                <StreamEntry
                  key={`entry-list-${idx}`}
                  entry={entry}
                  disableDelete={!canDelete}
                  disableCopy={!canCreate}
                  filterCallback={handleFilterStateCallback}
                  filterConstants={{ DIRECTIONS, CONDITION, FILTER_TYPES }}
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
    </Flex>
  );
};

export default EntriesNavigation;
