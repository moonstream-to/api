import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  Text,
  Stack,
  Box,
  FormControl,
  FormErrorMessage,
  InputGroup,
  Button,
  Input,
  InputRightElement,
} from "@chakra-ui/react";
import CustomIcon from "./CustomIcon";
import { useSignUp } from "../core/hooks";
import PasswordInput from "./PasswordInput";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const SignUp = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const { signUp, isLoading, isSuccess } = useSignUp();

  useEffect(() => {
    if (isSuccess) {
      toggleModal({ type: MODAL_TYPES.OFF });
    }
  }, [isSuccess, toggleModal]);

  return (
    <>
      <Text color="gray.1200" fontSize="md">
        Sign up for free
      </Text>
      <form onSubmit={handleSubmit(signUp)}>
        <Stack width="100%" pt={4} spacing={3}>
          <FormControl isInvalid={errors.username}>
            <InputGroup>
              <Input
                variant="filled"
                colorScheme="blue"
                placeholder="Your username here"
                name="username"
                ref={register({ required: "Username is required!" })}
              />
              <InputRightElement>
                <CustomIcon icon="name" />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="red.400" pl="1">
              {errors.username && errors.username.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.email}>
            <InputGroup>
              <Input
                variant="filled"
                colorScheme="blue"
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
          <FormControl isInvalid={errors.password}>
            <PasswordInput
              placeholder="Add password"
              name="password"
              ref={register({ required: "Password is required!" })}
            />
            <FormErrorMessage color="red.400" pl="1">
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
        </Stack>
        <Button
          my={8}
          variant="solid"
          colorScheme="blue"
          width="100%"
          type="submit"
          isLoading={isLoading}
        >
          Register
        </Button>
      </form>
      <Box height="1px" width="100%" background="#eaebf8" mb="1.875rem" />
      <Text textAlign="center" fontSize="md" color="gray.1200" pb={8}>
        Already have an account?{" "}
        <Box
          cursor="pointer"
          color="blue.400"
          as="span"
          onClick={() => toggleModal({ type: MODAL_TYPES.LOGIN })}
        >
          Login
        </Box>
      </Text>
    </>
  );
};

export default SignUp;
