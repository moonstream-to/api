import React, { useState, useEffect } from "react";
import { useSubscriptions } from "../core/hooks";
import {
  Input,
  Stack,
  Text,
  HStack,
  useRadioGroup,
  FormControl,
  FormErrorMessage,
  ModalBody,
  ModalCloseButton,
  ModalHeader,
  Button,
  ModalFooter,
  Spinner,
  IconButton,
} from "@chakra-ui/react";
import RadioCard from "./RadioCard";
import { useForm } from "react-hook-form";
import { GithubPicker } from "react-color";
import { BiRefresh } from "react-icons/bi";
import { makeColor } from "../core/utils/makeColor";
const NewSubscription = ({ isFreeOption, onClose }) => {
  const [color, setColor] = useState(makeColor());
  const { typesCache, createSubscription } = useSubscriptions();
  const { handleSubmit, errors, register } = useForm({});
  const [radioState, setRadioState] = useState("ethereum_blockchain");
  let { getRootProps, getRadioProps } = useRadioGroup({
    name: "type",
    defaultValue: radioState,
    onChange: setRadioState,
  });

  const group = getRootProps();

  useEffect(() => {
    if (createSubscription.isSuccess) {
      onClose();
    }
  }, [createSubscription.isSuccess, onClose]);

  if (typesCache.isLoading) return <Spinner />;

  const createSubscriptionWrap = (props) => {
    createSubscription.mutate({
      ...props,
      color: color,
      type: isFreeOption ? "free" : radioState,
    });
  };

  const handleChangeColorComplete = (color) => {
    setColor(color.hex);
  };

  return (
    <form onSubmit={handleSubmit(createSubscriptionWrap)}>
      <ModalHeader>Subscribe to a new address</ModalHeader>
      <ModalCloseButton />
      <ModalBody>
        <FormControl isInvalid={errors.label}>
          <Input
            my={2}
            type="text"
            autoComplete="off"
            placeholder="Enter label"
            name="label"
            ref={register({ required: "label is required!" })}
          ></Input>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.label && errors.label.message}
          </FormErrorMessage>
        </FormControl>
        <FormControl isInvalid={errors.address}>
          <Input
            type="text"
            autoComplete="off"
            my={2}
            placeholder="Enter address"
            name="address"
            ref={register({ required: "address is required!" })}
          ></Input>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.address && errors.address.message}
          </FormErrorMessage>
        </FormControl>
        <Stack my={16} direction="column">
          <Text fontWeight="600">
            {isFreeOption
              ? `Free subscription is only availible Ethereum blockchain source`
              : `On which source?`}
          </Text>

          <FormControl isInvalid={errors.subscription_type}>
            <HStack {...group} alignItems="stretch">
              {typesCache.data.map((type) => {
                const radio = getRadioProps({
                  value: type.id,
                  isDisabled:
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
              {errors.subscription_type && errors.subscription_type.message}
            </FormErrorMessage>
          </FormControl>
        </Stack>
        <FormControl isInvalid={errors.color}>
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

          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.color && errors.color.message}
          </FormErrorMessage>
        </FormControl>
      </ModalBody>
      <ModalFooter>
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
      </ModalFooter>
    </form>
  );
};

export default NewSubscription;
