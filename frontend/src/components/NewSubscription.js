import React, { useState, useEffect, useCallback } from "react";
import { useSubscriptions } from "../core/hooks";
import {
  Input,
  Stack,
  Text,
  HStack,
  useRadioGroup,
  FormControl,
  FormErrorMessage,
  Button,
  Spinner,
  IconButton,
  ButtonGroup,
  Flex,
} from "@chakra-ui/react";
import RadioCard from "./RadioCard";
// import { useForm } from "react-hook-form";
import { CirclePicker } from "react-color";
import { BiRefresh } from "react-icons/bi";
import { GithubPicker } from "react-color";
import { makeColor } from "../core/utils/makeColor";
import { useForm } from "react-hook-form";
const _NewSubscription = ({
  isFreeOption,
  onClose,
  setIsLoading,
  initialAddress,
  initialType,
  isModal,
}) => {
  const [color, setColor] = useState(makeColor());
  const { handleSubmit, errors, register } = useForm({});
  const { typesCache, createSubscription } = useSubscriptions();

  const [radioState, setRadioState] = useState(
    initialType ?? "ethereum_blockchain"
  );

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
      props.label = "Address";
      if (
        subscriptionAdressFormatRadio.startsWith("tag") &&
        radioState != "ethereum_whalewatch"
      ) {
        props.address = subscriptionAdressFormatRadio;
        props.label = "Tag";
      }

      createSubscription.mutate({
        ...props,
        color: color,
        type: isFreeOption ? "ethereum_blockchain" : radioState,
      });
    },
    [
      createSubscription,
      isFreeOption,
      color,
      radioState,
      subscriptionAdressFormatRadio,
    ]
  );

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

  return (
    <form onSubmit={handleSubmit(createSubscriptionWrapper)}>
      <Stack my={4} direction="column">
        <Stack spacing={1} w="100%">
          <Text fontWeight="600">Source:</Text>
          {/* position must be relative otherwise radio boxes add strange spacing on selection */}
          <Stack
            spacing={1}
            w="100%"
            direction="row"
            flexWrap="wrap"
            position="relative"
          >
            {typesCache.data
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
              })}
          </Stack>
        </Stack>

        <Flex direction="row" w="100%" flexWrap="wrap" pt={4}>
          {/* position must be relative otherwise radio boxes add strange spacing on selection */}
          <HStack flexGrow={0} flexBasis="140px" position="relative">
            {search(radioState, typesCache.data).choices.length > 0 && (
              <Text fontWeight="600">Type:</Text>
            )}
            {search(radioState, typesCache.data).choices.map(
              (addition_selects) => {
                const radio = getRadioPropsSubscription({
                  value: addition_selects,
                  isDisabled: addition_selects.startsWith("tag"),
                });
                return (
                  <RadioCard
                    px="4px"
                    py="2px"
                    key={`subscription_tags_${addition_selects}`}
                    {...radio}
                  >
                    {mapper[addition_selects]}
                  </RadioCard>
                );
              }
            )}
          </HStack>
          {subscriptionAdressFormatRadio.startsWith("input") &&
            radioState != "ethereum_whalewatch" && (
              <Flex flexBasis="240px" flexGrow={1}>
                <FormControl isInvalid={errors?.address}>
                  <Input
                    type="text"
                    autoComplete="off"
                    my={2}
                    placeholder="Address to subscribe to"
                    name="address"
                    ref={register({ required: "address is required!" })}
                  ></Input>
                  <FormErrorMessage color="unsafe.400" pl="1">
                    {errors?.address && errors?.address.message}
                  </FormErrorMessage>
                </FormControl>
              </Flex>
            )}
        </Flex>
        <Input
          type="hidden"
          placeholder="subscription_type"
          name="subscription_type"
          ref={register({ required: "select type" })}
          value={radioState}
          onChange={() => null}
        ></Input>
      </Stack>
      <FormControl isInvalid={errors?.color}>
        {!isModal ? (
          <Flex direction="row" pb={2} flexWrap="wrap" alignItems="baseline">
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
                // colorScheme="primary"
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
        <FormErrorMessage color="unsafe.400" pl="1">
          {errors?.color && errors?.color.message}
        </FormErrorMessage>
      </FormControl>

      <ButtonGroup direction="row" justifyContent="flex-end" w="100%">
        <Button
          type="submit"
          colorScheme="suggested"
          isLoading={createSubscription.isLoading}
        >
          Confirm
        </Button>

        <Button colorScheme="gray" onClick={onClose}>
          Cancel
        </Button>
      </ButtonGroup>
    </form>
  );
};

export default _NewSubscription;
