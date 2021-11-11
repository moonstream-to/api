import React, { useContext, useEffect } from "react";
import {
  chakra,
  FormLabel,
  Input,
  Stack,
  InputGroup,
  Box,
  Button,
  Table,
  Th,
  Td,
  Tr,
  Thead,
  Tbody,
  Center,
  Checkbox,
  CloseButton,
  InputRightAddon,
  Badge,
  InputLeftAddon,
} from "@chakra-ui/react";
import { CheckCircleIcon } from "@chakra-ui/icons";
import { useStorage, useSubscriptions } from "../core/hooks";
import Downshift from "downshift";
import color from "color";
import OverlayContext from "../core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";
import UIContext from "../core/providers/UIProvider/context";

const NewDashboard = (props) => {
  const ui = useContext(UIContext);
  const overlay = useContext(OverlayContext);
  const [newDashboardForm, setNewDashboardForm] = useStorage(
    sessionStorage,
    "new_dashboard",
    {
      name: "",
      subscriptions: [
        {
          label: "",
          abi: false,
          subscription_id: null,
          isMethods: false,
          isEvents: false,
          generic: {
            transactions: {
              in: false,
              out: false,
            },
            value: {
              in: false,
              out: false,
              balance: false,
            },
          },
        },
      ],
    }
  );

  const subscriptions = useSubscriptions();

  const [pickerItems, setPickerItems] = React.useState(
    subscriptions.subscriptionsCache.data?.subscriptions
  );

  useEffect(() => {
    if (!subscriptions.subscriptionsCache.isLoading) {
      const massaged = subscriptions.subscriptionsCache.data?.subscriptions.map(
        (item) => {
          return { value: item.address, ...item };
        }
      );
      setPickerItems(massaged);
    }
  }, [
    subscriptions.subscriptionsCache.data,
    subscriptions.subscriptionsCache.isLoading,
  ]);

  const filterFn = (item, inputValue) =>
    item.subscription_type_id === "ethereum_blockchain" &&
    (!inputValue ||
      item.address.toUpperCase().includes(inputValue.toUpperCase()) ||
      item.label.toUpperCase().includes(inputValue.toUpperCase()));

  return (
    <>
      <Stack spacing="24px">
        <Box>
          <FormLabel htmlFor="name">Name dashboard</FormLabel>
          <Input
            ref={props?.firstField}
            id="name"
            type="search"
            placeholder="How new board should be named?"
            value={newDashboardForm?.name}
            onChange={(e) =>
              setNewDashboardForm((prevState) => {
                return { ...prevState, name: e.target.value };
              })
            }
          />
        </Box>

        <Box>
          <FormLabel htmlFor="Addresses">Address list</FormLabel>
          <Table
            borderColor="gray.200"
            // borderWidth="1px"
            variant="simple"
            colorScheme="blue"
            // justifyContent="center"
            textAlign="center"
            borderBottomRadius="xl"
            // alignItems="baseline"
            h="auto"
            size="sm"
            mt={0}
          >
            <Thead>
              <Tr>
                <Th textAlign="center">Address</Th>
                <Th textAlign="center" colSpan="3">
                  ABI
                </Th>

                <Th textAlign="center" colSpan="2">
                  Transactions
                </Th>
                <Th textAlign="center" colSpan="3">
                  Value
                </Th>
              </Tr>
              <Tr>
                <Th></Th>
                <Th p={1} textAlign="center">
                  ABI
                </Th>
                <Th p={1} textAlign="center">
                  Methods
                </Th>
                <Th p={1} textAlign="center">
                  Events
                </Th>
                <Th p={1} textAlign="center">
                  In
                </Th>
                <Th p={1} textAlign="center">
                  Out
                </Th>
                <Th p={1} textAlign="center">
                  In
                </Th>
                <Th p={1} textAlign="center">
                  Out
                </Th>
                <Th p={1} textAlign="center">
                  Balance
                </Th>
              </Tr>
            </Thead>
            <Tbody>
              {newDashboardForm?.subscriptions.map((subscibedItem, idx) => {
                return (
                  <Tr key={`form-address-row-${idx}`}>
                    <Td>
                      {!subscriptions.subscriptionsCache.isLoading &&
                        subscriptions.subscriptionsCache.data &&
                        pickerItems && (
                          <>
                            <Downshift
                              onSelect={(selectedItem) => {
                                const newState = { ...newDashboardForm };
                                newState.subscriptions[idx] = {
                                  label: selectedItem.label,
                                  address: selectedItem.address,
                                  subscription_id: selectedItem.id,
                                  abi: selectedItem.abi,
                                  isMethods: false,
                                  isEvents: false,
                                  generic: {
                                    transactions: {
                                      in: false,
                                      out: false,
                                    },
                                    value: {
                                      in: false,
                                      out: false,
                                      balance: false,
                                    },
                                  },
                                };
                                setNewDashboardForm(newState);
                              }}
                              // isOpen={showSuggestions}
                              itemToString={(item) => (item ? item.label : "")}
                              initialSelectedItem={subscibedItem ?? undefined}
                            >
                              {({
                                getInputProps,
                                getItemProps,
                                getLabelProps,
                                getMenuProps,
                                getToggleButtonProps,
                                isOpen,
                                inputValue,
                                highlightedIndex,
                                // selectedItem,
                                getRootProps,
                              }) => {
                                const labelColor =
                                  subscibedItem.color &&
                                  color(`${subscibedItem.color}`);
                                return (
                                  <Box pos="relative">
                                    <Box
                                      // style={comboboxStyles}
                                      {...getRootProps(
                                        {},
                                        { suppressRefError: true }
                                      )}
                                    >
                                      <InputGroup>
                                        <InputLeftAddon
                                          isTruncated
                                          maxW="60px"
                                          fontSize={
                                            ui.isMobileView ? "xs" : "sm"
                                          }
                                          bgColor={
                                            subscibedItem?.color ?? "gray.100"
                                          }
                                        >
                                          <FormLabel
                                            alignContent="center"
                                            my={2}
                                            {...getLabelProps()}
                                            color={
                                              labelColor
                                                ? labelColor?.isDark()
                                                  ? "white"
                                                  : labelColor.darken(0.6).hex()
                                                : "inherit"
                                            }
                                          >{`#${idx}:`}</FormLabel>
                                        </InputLeftAddon>

                                        <Input
                                          placeholder="Subscription to use in dashboard"
                                          isTruncated
                                          fontSize="sm"
                                          // defaultValue={
                                          //   subscibedItem?.label ?? "yoyoy"
                                          // }
                                          {...getInputProps({
                                            defaultValue:
                                              subscibedItem?.label ?? "iha",
                                          })}
                                        ></Input>
                                        <InputRightAddon>
                                          {" "}
                                          <button
                                            {...getToggleButtonProps()}
                                            aria-label={"toggle menu"}
                                          >
                                            &#8595;
                                          </button>
                                        </InputRightAddon>
                                      </InputGroup>
                                    </Box>
                                    {/* <Menu
                                          isOpen={isOpen}

                                          // style={menuStyles}
                                          // position="absolute"
                                          colorScheme="blue"
                                          bgColor="gray.300"
                                          inset="unset"
                                          // spacing={2}

                                          // p={2}
                                        > */}
                                    {isOpen ? (
                                      <Stack
                                        // display="flex"
                                        direction="column"
                                        className="menuListTim"
                                        {...getMenuProps()}
                                        bgColor="gray.300"
                                        borderRadius="md"
                                        boxShadow="lg"
                                        pos="absolute"
                                        left={0}
                                        right={0}
                                        spacing={2}
                                        zIndex={1000}
                                        py={2}
                                      >
                                        {pickerItems &&
                                          pickerItems.filter((item) =>
                                            filterFn(item, inputValue)
                                          ).length === 0 && (
                                            <Button
                                              colorScheme="orange"
                                              variant="outline"
                                              size="sm"
                                              fontSize="sm"
                                              w="100%"
                                              m={0}
                                              isTruncated
                                              onClick={() => {
                                                overlay.toggleModal({
                                                  type: MODAL_TYPES.NEW_SUBSCRIPTON,
                                                  props: {
                                                    initialValue: inputValue,
                                                  },
                                                });
                                              }}
                                            >
                                              Subscribe to: {inputValue}{" "}
                                            </Button>
                                          )}
                                        {pickerItems &&
                                          pickerItems
                                            .filter((item) =>
                                              filterFn(item, inputValue)
                                            )
                                            .map((item, index) => {
                                              const badgeColor = color(
                                                `${item.color}`
                                              );

                                              return (
                                                <Stack
                                                  px={4}
                                                  py={1}
                                                  alignItems="center"
                                                  key={item.value}
                                                  {...getItemProps({
                                                    key: item.value,
                                                    index,
                                                    item,
                                                  })}
                                                  direction="row"
                                                  w="100%"
                                                  bgColor={
                                                    index === highlightedIndex
                                                      ? "orange.900"
                                                      : "inherit"
                                                  }
                                                  color={
                                                    index === highlightedIndex
                                                      ? "gray.100"
                                                      : "inherit"
                                                  }
                                                >
                                                  <chakra.span whiteSpace="nowrap">
                                                    {item.label}
                                                  </chakra.span>
                                                  <Badge
                                                    size="sm"
                                                    placeSelf="self-end"
                                                    colorScheme={
                                                      item.abi
                                                        ? "green"
                                                        : "gray"
                                                    }
                                                  >
                                                    ABI
                                                  </Badge>
                                                  <Badge
                                                    isTruncated
                                                    size="sm"
                                                    placeSelf="self-end"
                                                    bgColor={item.color}
                                                    color={
                                                      badgeColor.isDark()
                                                        ? badgeColor
                                                            .lighten(100)
                                                            .hex()
                                                        : badgeColor
                                                            .darken(0.6)
                                                            .hex()
                                                    }
                                                  >
                                                    {item.address}
                                                  </Badge>
                                                </Stack>
                                              );
                                            })}
                                        {inputValue === "" && (
                                          <Button
                                            colorScheme="orange"
                                            variant="outline"
                                            w="100%"
                                            m={0}
                                            size="sm"
                                            onClick={() =>
                                              overlay.toggleModal({
                                                type: MODAL_TYPES.NEW_SUBSCRIPTON,
                                              })
                                            }
                                          >
                                            New subscription
                                            {inputValue}{" "}
                                          </Button>
                                        )}
                                      </Stack>
                                    ) : null}
                                    {/* </Menu> */}
                                  </Box>
                                );
                              }}
                            </Downshift>
                          </>
                          // <AutoComplete
                          //   openOnFocus
                          //   creatable
                          //   suggestWhenEmpty
                          // >
                          //   <AutoCompleteInput variant="filled" />
                          //   <AutoCompleteList>
                          //     {pickerItems?.map((subscription, oid) => (
                          //       <AutoCompleteItem
                          //         key={`row-${idx}-option-${oid}`}
                          //         value={subscription.address}
                          //         textTransform="capitalize"
                          //         align="center"
                          //       >
                          //         {/* <Avatar
                          //       size="sm"
                          //       // name={person.name}
                          //       // src={person.image}
                          //     /> */}
                          //         <Text ml="4">{subscription.label}</Text>
                          //       </AutoCompleteItem>
                          //     ))}
                          //     {/* <AutoCompleteCreatable>
                          //     {({ value }) => (
                          //       <span>New Subscription: {value}</span>
                          //     )}
                          //   </AutoCompleteCreatable> */}
                          //   </AutoCompleteList>
                          // </AutoComplete>
                        )}
                    </Td>
                    <Td p={1} textAlign="center">
                      {subscibedItem.abi && subscibedItem.address && (
                        <CheckCircleIcon color="green" />
                      )}
                      {!subscibedItem.abi && (
                        <Button
                          colorScheme="orange"
                          size="xs"
                          py={2}
                          disabled={!subscibedItem.address}
                          onClick={() =>
                            overlay.toggleModal({
                              type: MODAL_TYPES.UPLOAD_ABI,
                              props: { id: subscibedItem.id },
                            })
                          }
                        >
                          Upload
                        </Button>
                      )}
                    </Td>

                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.abi}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx] = {
                            ...newState.subscriptions[idx],
                            isMethods: !newState.subscriptions[idx].isMethods,
                          };
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.isMethods}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={
                          !subscibedItem.address || !subscibedItem.abi
                        }
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx] = {
                            ...newState.subscriptions[idx],
                            isEvents: !newState.subscriptions[idx].isEvents,
                          };
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.isEvents}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.address}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx].generic.transactions.in =
                            !newState.subscriptions[idx].generic.transactions
                              .in;
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.generic.transactions.in}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.address}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx].generic.transactions.out =
                            !newState.subscriptions[idx].generic.transactions
                              .out;
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.generic.transactions.out}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.address}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx].generic.value.in =
                            !newState.subscriptions[idx].generic.value.in;
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.generic.value.in}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.address}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx].generic.value.out =
                            !newState.subscriptions[idx].generic.value.out;
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.generic.value.out}
                      ></Checkbox>
                    </Td>
                    <Td p={1} textAlign="center">
                      <Checkbox
                        isDisabled={!subscibedItem.address}
                        onChange={() => {
                          const newState = { ...newDashboardForm };
                          newState.subscriptions[idx].generic.balance =
                            !newState.subscriptions[idx].generic.balance;
                          setNewDashboardForm(newState);
                        }}
                        isChecked={subscibedItem.generic.balance}
                      ></Checkbox>
                    </Td>

                    <Td p={1} textAlign="center">
                      {idx > 0 && (
                        <CloseButton
                          onClick={() => {
                            const hardcopy = [
                              ...newDashboardForm?.subscriptions,
                            ];
                            hardcopy.splice(idx, 1);
                            setNewDashboardForm((prevState) => {
                              return {
                                ...prevState,
                                subscriptions: [...hardcopy],
                              };
                            });
                          }}
                        />
                      )}
                    </Td>
                  </Tr>
                );
              })}
            </Tbody>
          </Table>
          <Center>
            <Button
              w="100px"
              colorScheme="gray"
              variant="solid"
              p={0}
              maxH="1.25rem"
              _active={{ textDecor: "none" }}
              onClick={() => {
                const newState = { ...newDashboardForm };
                newState.subscriptions.push({
                  label: "",
                  abi: false,
                  subscription_id: null,
                  isMethods: false,
                  isEvents: false,
                  generic: {
                    transactions: {
                      in: false,
                      out: false,
                    },
                    value: {
                      in: false,
                      out: false,
                      balance: false,
                    },
                  },
                });
                setNewDashboardForm(newState);
              }}
            >
              +
            </Button>
          </Center>
        </Box>

        {/* <Box>
                <FormLabel htmlFor="desc">ABI</FormLabel>
                <Textarea
                  id="desc"
                  placeholder="ABI Upload element should be here instead"
                />
              </Box> */}
      </Stack>
    </>
  );
};

const ChakraNewDashboard = chakra(NewDashboard);

export default ChakraNewDashboard;
