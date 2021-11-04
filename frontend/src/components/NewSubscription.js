import React, { useState, useEffect, useCallback, useRef } from "react";
import { useSubscriptions } from "../core/hooks";
import {
  Input,
  Stack,
  Text,
  useRadioGroup,
  FormControl,
  FormErrorMessage,
  Button,
  Spinner,
  IconButton,
  ButtonGroup,
  Flex,
  Box,
  InputGroup,
  Image,
  InputLeftAddon,
  InputRightAddon,
  chakra,
  Tooltip,
  VStack,
  FormLabel,
  useToast,
} from "@chakra-ui/react";
// import { useForm } from "react-hook-form";
import { CirclePicker } from "react-color";
import { BiRefresh } from "react-icons/bi";
import { GithubPicker } from "react-color";
import { makeColor } from "../core/utils/makeColor";
import { useForm } from "react-hook-form";
import Web3 from "web3";
import Downshift from "downshift";
import { QuestionIcon } from "@chakra-ui/icons";
const _NewSubscription = ({
  isFreeOption,
  onClose,
  setIsLoading,
  initialAddress,
  initialType,
  isModal,
  initialValue,
}) => {
  const [color, setColor] = useState(makeColor());
  const { handleSubmit, errors, register } = useForm({});
  const [address, setAddress] = useState();
  const [label, setLabel] = useState();
  const [type, setType] = useState();
  const { typesCache, createSubscription } = useSubscriptions();

  const [radioState, setRadioState] = useState(
    initialType ?? "ethereum_blockchain"
  );

  const [pickerItems, setPickerItems] = useState();

  const toast = useToast();

  useEffect(() => {
    if (!typesCache.isLoading) {
      const massaged = typesCache.data?.map((item) => {
        return { value: item.name, ...item };
      });
      setPickerItems(massaged);
    }
  }, [typesCache.data, typesCache.isLoading]);

  const mapper = {
    "tag:erc721": "NFTs",
    "input:address": "Address",
  };

  const [subscriptionAdressFormatRadio, setsubscriptionAdressFormatRadio] =
    useState("input:address");

  let { getRadioProps } = useRadioGroup({
    name: "type",
    defaultValue: radioState,
    onChange: setRadioState,
  });

  let { getRadioProps: getRadioPropsSubscription } = useRadioGroup({
    name: "subscription",
    defaultValue: subscriptionAdressFormatRadio,
    onChange: setsubscriptionAdressFormatRadio,
  });

  useEffect(() => {
    if (initialValue && initialValue !== "") {
      console.log("iv:", initialValue, Web3.utils.isAddress(initialValue));
      if (Web3.utils.isAddress(initialValue)) {
        setAddress(initialValue);
      } else {
        setLabel(initialValue);
      }
    }
  }, [initialValue]);
  useEffect(() => {
    if (setIsLoading) {
      setIsLoading(createSubscription.isLoading);
    }
  }, [createSubscription.isLoading, setIsLoading]);

  useEffect(() => {
    if (createSubscription.isSuccess) {
      onClose();
    }
  }, [createSubscription.isSuccess, onClose]);

  const createSubscriptionWrapper = useCallback(
    (props) => {
      props.label = props.label ?? "Address";
      props.type = type.id;
      if (
        subscriptionAdressFormatRadio.startsWith("tag") &&
        radioState != "ethereum_whalewatch"
      ) {
        props.address = subscriptionAdressFormatRadio;
        props.label = "Tag";
      }
      if (!props.address) {
        props.address = "0x000000000000000000000000000000000000dead";
      }

      if (Web3.utils.isAddress(props.address)) {
        createSubscription.mutate({
          ...props,
          color: color,
        });
      } else {
        if (!toast.isActive("address_toast"))
          toast({
            title: "Is not valid Ethereum Address",
            status: "error",
            position: "bottom",
            id: "address_toast",
            description: "Web3.utils.isAddress returned false",
          });
      }
    },
    [
      toast,
      createSubscription,
      color,
      radioState,
      subscriptionAdressFormatRadio,
      type,
    ]
  );
  const downshiftRef = useRef(null);

  if (typesCache.isLoading) return <Spinner />;

  function search(nameKey, myArray) {
    for (var i = 0; i < myArray.length; i++) {
      if (myArray[i].id === nameKey) {
        return myArray[i];
      }
    }
  }

  const handleChangeColorComplete = (color) => {
    setColor(color.hex);
  };

  if (!errors) return "";

  console.log("selected type", type);
  console.log("pickerItems", pickerItems);

  const filterFn = (item, inputValue) => {
    console.log("filterFN", item.name, inputValue);
    return (
      !inputValue || item.name.toUpperCase().includes(inputValue.toUpperCase())
    );
  };

  return (
    <form onSubmit={handleSubmit(createSubscriptionWrapper)}>
      <Stack mb={0} direction="column">
        <Stack spacing={1} w="100%" pb={2}>
          <Text fontWeight="600">Type:</Text>
          {/* position must be relative otherwise radio boxes add strange spacing on selection */}
          <Stack
            spacing={1}
            w="100%"
            direction="row"
            flexWrap="wrap"
            position="relative"
          >
            {!typesCache.isLoading && typesCache.data && pickerItems && (
              <>
                <Downshift
                  onSelect={(selectedItem) => {
                    setType(selectedItem);
                  }}
                  // isOpen={showSuggestions}
                  itemToString={(item) => (item ? item.name : "")}
                  // initialSelectedItem={pickerItems[1] ?? undefined}
                  ref={downshiftRef}
                  // initialInputValue={}
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
                    selectedItem,
                    getRootProps,
                  }) => {
                    console.log("selected item,", selectedItem?.name);
                    return (
                      <Box pos="relative" w="100%">
                        <Box
                          // style={comboboxStyles}
                          {...getRootProps({}, { suppressRefError: true })}
                        >
                          <InputGroup>
                            <InputLeftAddon
                              isTruncated
                              maxW="60px"
                              fontSize="sm"
                              bgColor={"gray.100"}
                            >
                              <Image h="24px" src={selectedItem?.icon_url} />
                            </InputLeftAddon>

                            <Input
                              placeholder="What do you want to subscribe to"
                              isTruncated
                              fontSize="sm"
                              {...getInputProps()}
                              // defaultValue={selectedItem.name ?? undefined}
                              // value={selectedItem.name}
                            ></Input>
                            <InputRightAddon p={0}>
                              <Button
                                variant="outline"
                                w="100%"
                                m={0}
                                p={0}
                                colorScheme="gray"
                                {...getToggleButtonProps({
                                  // onClick: () =>
                                  //   console.log(
                                  //     "ref: ",
                                  //     downshiftRef.current.clearSelection()
                                  //   ),
                                })}
                                aria-label={"toggle menu"}
                              >
                                &#8595;
                              </Button>
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
                              pickerItems
                                .filter((item) => filterFn(item, inputValue))
                                .map((item, index) => {
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
                                      justifyContent="space-between"
                                    >
                                      <Image
                                        h="24px"
                                        src={item.icon_url}
                                        alignSelf="flex-start"
                                      />
                                      <chakra.span
                                        whiteSpace="nowrap"
                                        alignSelf="center"
                                      >
                                        {item.name}
                                      </chakra.span>
                                      <Tooltip
                                        label={item.description}
                                        colorScheme="blue"
                                        variant="onboarding"
                                      >
                                        <QuestionIcon h="24px" />
                                      </Tooltip>
                                    </Stack>
                                  );
                                })}
                          </Stack>
                        ) : null}
                        {/* </Menu> */}
                      </Box>
                    );
                  }}
                </Downshift>
              </>
            )}
            {/* {typesCache.data
              .sort((a, b) =>
                a?.name > b?.name ? 1 : b?.name > a?.name ? -1 : 0
              )
              .map((type) => {
                const radio = getRadioProps({
                  value: type.id,
                  isDisabled:
                    (initialAddress && initialType) ||
                    !type.active ||
                    (isFreeOption && type.id !== "ethereum_blockchain"),
                });

                return (
                  <RadioCard
                    px="8px"
                    py="4px"
                    mt="2px"
                    w="190px"
                    {...radio}
                    key={`subscription_type_${type.id}`}
                    label={type.description}
                    iconURL={type.icon_url}
                  >
                    {type.name.slice(9, type.name.length)}
                  </RadioCard>
                );
              })} */}
          </Stack>
        </Stack>

        {!type?.id?.includes("whalewatch") && type && (
          <Flex direction="row" w="100%" flexWrap="wrap">
            {/* position must be relative otherwise radio boxes add strange spacing on selection */}
            <VStack w="100%" spacing={0}>
              {subscriptionAdressFormatRadio.startsWith("input") && (
                <Flex w="100%">
                  <FormControl isInvalid={errors?.address}>
                    <InputGroup my={2} fontSize="xs">
                      <InputLeftAddon>
                        <FormLabel
                          fontWeight="600"
                          // alignSelf="flex-start"
                          m={0}
                        >
                          Address:
                        </FormLabel>
                      </InputLeftAddon>
                      <Input
                        type="text"
                        autoComplete="off"
                        placeholder="Address to subscribe to"
                        name="address"
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        ref={register({ required: "address is required!" })}
                      ></Input>
                    </InputGroup>
                    <FormErrorMessage color="red.400" pl="1">
                      {errors?.address && errors?.address.message}
                    </FormErrorMessage>
                  </FormControl>
                </Flex>
              )}
            </VStack>
          </Flex>
        )}
        {!type?.id?.includes("whalewatch") && type && (
          <Flex direction="row" w="100%" flexWrap="wrap">
            {/* position must be relative otherwise radio boxes add strange spacing on selection */}
            <VStack w="100%" spacing={0}>
              <Flex w="100%">
                <FormControl isInvalid={errors?.label}>
                  <InputGroup my={2} fontSize="xs">
                    <InputLeftAddon>
                      <FormLabel
                        fontWeight="600"
                        // alignSelf="flex-start"
                        m={0}
                      >
                        Label:
                      </FormLabel>
                    </InputLeftAddon>
                    <Input
                      type="text"
                      autoComplete="off"
                      placeholder="Name your label"
                      name="label"
                      value={label}
                      onChange={(e) => setLabel(e.target.value)}
                      ref={register({ required: "label is required!" })}
                    ></Input>
                  </InputGroup>
                  <FormErrorMessage color="red.400" pl="1">
                    {errors?.label && errors?.label.message}
                  </FormErrorMessage>
                </FormControl>
              </Flex>
            </VStack>
          </Flex>
        )}

        {type && (
          <FormControl isInvalid={errors?.color}>
            {!isModal ? (
              <Flex
                direction="row"
                pb={2}
                flexWrap="wrap"
                alignItems="baseline"
              >
                <Text fontWeight="600" alignSelf="center">
                  Label color
                </Text>{" "}
                <Stack
                  // pt={2}
                  direction={["row", "row", null]}
                  h="min-content"
                  alignSelf="center"
                >
                  <IconButton
                    size="md"
                    // colorScheme="blue"
                    color={"white.100"}
                    _hover={{ bgColor: { color } }}
                    bgColor={color}
                    variant="outline"
                    onClick={() => setColor(makeColor())}
                    icon={<BiRefresh />}
                  />
                  <Input
                    type="input"
                    placeholder="color"
                    name="color"
                    ref={register({ required: "color is required!" })}
                    value={color}
                    onChange={() => null}
                    w="200px"
                  ></Input>
                </Stack>
                <Flex p={2} flexBasis="120px" flexGrow={1} alignSelf="center">
                  <CirclePicker
                    width="100%"
                    onChangeComplete={handleChangeColorComplete}
                    circleSpacing={1}
                    circleSize={24}
                  />
                </Flex>
              </Flex>
            ) : (
              <>
                <Stack direction="row" pb={2}>
                  <Text fontWeight="600" alignSelf="center">
                    Label color
                  </Text>{" "}
                  <IconButton
                    size="md"
                    color={"white.100"}
                    _hover={{ bgColor: { color } }}
                    bgColor={color}
                    variant="outline"
                    onClick={() => setColor(makeColor())}
                    icon={<BiRefresh />}
                  />
                  <Input
                    type="input"
                    placeholder="color"
                    name="color"
                    ref={register({ required: "color is required!" })}
                    value={color}
                    onChange={() => null}
                    w="200px"
                  ></Input>
                </Stack>

                <GithubPicker onChangeComplete={handleChangeColorComplete} />
              </>
            )}
            <FormErrorMessage color="red.400" pl="1">
              {errors?.color && errors?.color.message}
            </FormErrorMessage>
          </FormControl>
        )}
        <ButtonGroup direction="row" justifyContent="flex-end" w="100%">
          <Button
            type="submit"
            colorScheme="green"
            isLoading={createSubscription.isLoading}
          >
            Confirm
          </Button>

          <Button colorScheme="red" onClick={onClose}>
            Cancel
          </Button>
        </ButtonGroup>
      </Stack>
    </form>
  );
};

export default _NewSubscription;
