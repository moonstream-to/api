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
  Spacer,
  Flex,
} from "@chakra-ui/react";
import RadioCard from "./RadioCard";
// import { useForm } from "react-hook-form";
import { CirclePicker } from "react-color";
import { BiRefresh } from "react-icons/bi";
import { makeColor } from "../core/utils/makeColor";
import { useForm } from "react-hook-form";
const _NewSubscription = ({
  isFreeOption,
  onClose,
  setIsLoading,
  initialAddress,
  initialType,
}) => {
  const [color, setColor] = useState(makeColor());
  const { handleSubmit, errors, register } = useForm({});
  const { typesCache, createSubscription } = useSubscriptions();
  // const { handleSubmit, errors, register } = useForm({});
  const [radioState, setRadioState] = useState(
    initialType ?? "ethereum_blockchain"
  );
  let { getRootProps, getRadioProps } = useRadioGroup({
    name: "type",
    defaultValue: radioState,
    onChange: setRadioState,
  });

  const group = getRootProps();

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
      createSubscription.mutate({
        ...props,
        color: color,
        type: isFreeOption ? "ethereum_blockchain" : radioState,
      });
    },
    [createSubscription, isFreeOption, color, radioState]
  );

  if (typesCache.isLoading) return <Spinner />;

  const handleChangeColorComplete = (color) => {
    setColor(color.hex);
  };

  if (!errors) return "";

  return (
    <form onSubmit={handleSubmit(createSubscriptionWrapper)}>
      <FormControl isInvalid={errors?.label}>
        <Input
          my={2}
          type="text"
          autoComplete="off"
          placeholder="Name of subscription (you can change it later)"
          name="label"
          ref={register({ required: "label is required!" })}
        ></Input>
        <FormErrorMessage color="unsafe.400" pl="1">
          {errors?.label && errors?.label.message}
        </FormErrorMessage>
      </FormControl>
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
      <Stack my={4} direction="column">
        {/* <Text fontWeight="600">
          {isFreeOption
            ? `Right now you can subscribe only to ethereum blockchain`
            : `On which source?`}
        </Text> */}

        <FormControl isInvalid={errors?.subscription_type}>
          <HStack {...group} alignItems="stretch">
            {typesCache.data.map((type) => {
              const radio = getRadioProps({
                value: type.id,
                isDisabled:
                  (initialAddress && initialType) ||
                  !type.active ||
                  (isFreeOption && type.id !== "ethereum_blockchain"),
              });
              return (
                <RadioCard key={`subscription_type_${type.id}`} {...radio}>
                  {type.name}
                </RadioCard>
              );
            })}
          </HStack>
          <Input
            type="hidden"
            placeholder="subscription_type"
            name="subscription_type"
            ref={register({ required: "select type" })}
            value={radioState}
            onChange={() => null}
          ></Input>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors?.subscription_type && errors?.subscription_type.message}
          </FormErrorMessage>
        </FormControl>
      </Stack>
      <FormControl isInvalid={errors?.color}>
        <Flex direction="row" pb={2} flexWrap="wrap">
          <Stack pt={2} direction="row" h="min-content">
            <Text fontWeight="600" alignSelf="center">
              Label color
            </Text>{" "}
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
          <Flex p={2}>
            <CirclePicker
              onChangeComplete={handleChangeColorComplete}
              circleSpacing={1}
              circleSize={24}
            />
          </Flex>
        </Flex>

        <FormErrorMessage color="unsafe.400" pl="1">
          {errors?.color && errors?.color.message}
        </FormErrorMessage>
      </FormControl>

      <ButtonGroup direction="row" justifyContent="space-evenly">
        <Button
          type="submit"
          colorScheme="suggested"
          isLoading={createSubscription.isLoading}
        >
          Confirm
        </Button>
        <Spacer />
        <Button colorScheme="gray" onClick={onClose}>
          Cancel
        </Button>
      </ButtonGroup>
    </form>
  );
};

export default _NewSubscription;
