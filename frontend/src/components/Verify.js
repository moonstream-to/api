
/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useMutation } from "react-query";
import {
  Heading,
  Text,
  Box,
  FormControl,
  FormErrorMessage,
  Input,
  Button,
} from "@chakra-ui/react";
import Modal from "./Modal";
import { AuthService } from "../core/services";
import { useToast, useUser } from "../core/hooks";

const Verify = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const toast = useToast();
  const [verify, { isLoading, error, data }] = useMutation(async (data) => {
    const verificationResponse = await AuthService.verify(data);
    return verificationResponse.data;
  });
  const { getUser } = useUser();

  useEffect(() => {
    if (!data) {
      return;
    }
    getUser();
    toggleModal(null);
  }, [data, getUser, toggleModal]);

  useEffect(() => {
    if (error?.response?.data?.detail) {
      toast(error.response.data.detail, "error");
    }
  }, [error, toast]);

  return (
    <Modal onClose={() => toggleModal(null)}>
      <Heading mt={2} size="lg">
        Verify account
      </Heading>
      <form onSubmit={handleSubmit(verify)}>
        <FormControl isInvalid={errors.code} my={8}>
          <Input
            placeholder="Your code here"
            name="code"
            ref={register({ required: "code field is required!" })}
          />
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.code && errors.code.message}
          </FormErrorMessage>
        </FormControl>
        <Button
          type="submit"
          verify="primary"
          colorScheme="primary"
          width="100%"
          isLoading={isLoading}
        >
          Verify
        </Button>
      </form>
      <Box height="1px" width="100%" background="#eaebf8" mb="1.875rem" />
      <Text fontSize="sm" color="gray.1200">
        We just sent you a verification code by email.
      </Text>
      <Text fontSize="sm" color="gray.1200">
        Please enter the code here so we can verify that you are who you say you
        are.
      </Text>
    </Modal>
  );
};

export default Verify;
