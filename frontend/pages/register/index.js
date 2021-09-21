import React, { useState } from "react";
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
import Icon from "../../src/components/CustomIcon";
import useSignUp from "../../src/core/hooks/useSignUp";
import useUser from "../../src/core/hooks/useSignUp";
import useRouter from "../../src/core/hooks/useSignUp";
import { DEFAULT_METATAGS } from "../../src/core/constants";

export async function getStaticProps() {
  return {
    props: { metaTags: { ...DEFAULT_METATAGS } },
  };
}

const Register = () => {
  const router = useRouter();
  const { handleSubmit, errors, register } = useForm();
  const [showPassword, togglePassword] = useState(false);

  const { user } = useUser();
  const loggedIn = user && user.username;

  //   const { email, code } = router.query;
  const email = router.query?.email;
  const code = router.query?.code;
  const { signUp, isLoading } = useSignUp(code);

  loggedIn && router.push("/stream");

  return (
    <Box minH="900px" w="100%" px={["7%", null, "25%"]} alignSelf="center">
      <Heading mt={2} size="md">
        Create an account
      </Heading>
      <Text color="gray.300" fontSize="md">
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
                <Icon icon="name" />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="red.400" pl="1">
              {errors.username && errors.username.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.email}>
            <InputGroup>
              {!email && (
                <Input
                  variant="filled"
                  colorScheme="blue"
                  placeholder="Your email here"
                  name="email"
                  ref={register({ required: "Email is required!" })}
                />
              )}
              {email && (
                <Input
                  variant="filled"
                  colorScheme="blue"
                  placeholder="Your email here"
                  defaultValue={email}
                  isReadOnly={true}
                  name="email"
                  ref={register({ required: "Email is required!" })}
                />
              )}
              <InputRightElement>
                <Icon icon="name" />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="red.400" pl="1">
              {errors.email && errors.email.message}
            </FormErrorMessage>
          </FormControl>
          <FormControl isInvalid={errors.password}>
            <InputGroup>
              <Input
                variant="filled"
                colorScheme="blue"
                autoComplete="new-password"
                placeholder="Add password"
                name="password"
                type={showPassword ? "text" : "password"}
                ref={register({ required: "Password is required!" })}
              />
              <InputRightElement onClick={() => togglePassword(!showPassword)}>
                <Icon icon="password" />
              </InputRightElement>
            </InputGroup>
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
    </Box>
  );
};
export default Register;
