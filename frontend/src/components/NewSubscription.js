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
} from "@chakra-ui/react";
import RadioCard from "./RadioCard";
import { useForm } from "react-hook-form";

const NewSubscription = ({ isFreeOption, onClose }) => {
  const { typesCache, createSubscription } = useSubscriptions();
  const { handleSubmit, errors, register } = useForm();
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
      type: isFreeOption ? "free" : radioState,
    });
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

          <FormControl isInvalid={errors.type}>
            <HStack {...group} alignItems="stretch">
              {typesCache.data.map((type) => {
                const radio = getRadioProps({
                  value: type.subscription_type,
                  isDisabled:
                    !type.active ||
                    (isFreeOption &&
                      type.subscription_type !== "ethereum_blockchain"),
                });
                if (!type.subscription_plan_id) return "";
                return (
                  <RadioCard key={`subscription-type-${type.id}`} {...radio}>
                    {type.name}
                  </RadioCard>
                );
              })}
            </HStack>
          </FormControl>
        </Stack>
      </ModalBody>
      <ModalFooter>
        <Button
          type="submit"
          colorScheme="suggested"
          isLoading={createSubscription.isLoading}
        >
          Confirm
        </Button>
        <Button colorScheme="gray">Cancel</Button>
      </ModalFooter>
    </form>
  );
};

export default NewSubscription;
