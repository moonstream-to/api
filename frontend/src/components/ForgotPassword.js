import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useToast, useForgotPassword } from "../core/hooks";
import {
  FormControl,
  InputGroup,
  FormErrorMessage,
  Button,
  Input,
  InputRightElement,
} from "@chakra-ui/react";
import CustomIcon from "./CustomIcon";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const ForgotPassword = ({ toggleModal }) => {
  const toast = useToast();
  const { handleSubmit, errors, register } = useForm();
  const { forgotPassword, isLoading, data } = useForgotPassword();

  useEffect(() => {
    if (!data) return;

    toggleModal({ type: MODAL_TYPES.OFF });
  }, [data, toggleModal, toast]);

  return (
    <form onSubmit={handleSubmit(forgotPassword)}>
      <FormControl isInvalid={errors.email} my={4}>
        <InputGroup>
          <Input
            colorScheme="blue"
            variant="filled"
            placeholder="Your email here"
            name="email"
            ref={register({ required: "Email is required!" })}
          />
          <InputRightElement>
            <CustomIcon icon="name" />
          </InputRightElement>
        </InputGroup>
        <FormErrorMessage color="red.400" pl="1">
          {errors.email && errors.email.message}
        </FormErrorMessage>
      </FormControl>
      <Button
        type="submit"
        variant="solid"
        colorScheme="blue"
        width="100%"
        isLoading={isLoading}
      >
        Send
      </Button>
    </form>
  );
};

export default ForgotPassword;
