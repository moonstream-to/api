/** @jsxRuntime classic */
/** @jsx jsx */
import { jsx } from "@emotion/react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import {
  Heading,
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
import CustomIcon from "./CustomIcon"
import { useSignUp } from "../core/hooks";
import Modal from "./Modal";
import PasswordInput from "./PasswordInput";

const SignUp = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const { signUp, isLoading, data } = useSignUp();

  useEffect(() => {
    if (!data) {
      return;
    }
    toggleModal("verify");
  }, [data, toggleModal]);

  return (
    <Modal onClose={() => toggleModal(null)}>
      <Heading mt={2} size="md">
        Create an account
      </Heading>
      <Text color="gray.1200" fontSize="md">
        Sign up for free
      </Text>
      <form onSubmit={handleSubmit(signUp)}>
        <Stack width="100%" pt={4} spacing={3}>
          <FormControl isInvalid={errors.username}>
            <InputGroup>
              <Input
                variant="filled"
                colorScheme="primary"
                placeholder="Your username here"
                name="username"
                ref={register({ required: "Username is required!" })}
              />
              <InputRightElement>
                <CustomIcon icon="name" />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="unsafe.400" pl="1">
              {errors.username && errors.username.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.email}>
            <InputGroup>
              <Input
                variant="filled"
                colorScheme="primary"
                placeholder="Your email here"
                name="email"
                ref={register({ required: "Email is required!" })}
              />
              <InputRightElement>
                <CustomIcon icon="name" />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="unsafe.400" pl="1">
              {errors.email && errors.email.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.password}>
            <PasswordInput
              placeholder="Add password"
              name="password"
              ref={register({ required: "Password is required!" })}
            />
            <FormErrorMessage color="unsafe.400" pl="1">
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
        </Stack>
        <Button
          my={8}
          variant="solid"
          colorScheme="primary"
          width="100%"
          type="submit"
          isLoading={isLoading}
        >
          Register
        </Button>
      </form>
      <Box height="1px" width="100%" background="#eaebf8" mb="1.875rem" />
      <Text textAlign="center" fontSize="md" color="gray.1200">
        Already have an account?{" "}
        <Box
          cursor="pointer"
          color="primary.400"
          as="span"
          onClick={() => toggleModal("login")}
        >
          Login
        </Box>
      </Text>
    </Modal>
  );
};

export default SignUp;
