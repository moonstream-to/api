import React from "react";
import {
  Box,
  InputGroup,
  InputLeftElement,
  FormControl,
  FormErrorMessage,
  HStack,
  Button,
  InputRightElement,
  Input,
} from "@chakra-ui/react";
import { CloseIcon } from "@chakra-ui/icons";
import { useEffect, useState, useRef } from "react";
import { Icon } from "../../src/Theme";

import { useForm } from "react-hook-form";
import { useUser, useTokens } from "../core/hooks";

const TokenRequest = ({ newToken, toggle }) => {
  const { user } = useUser();
  const { createToken } = useTokens();
  const { handleSubmit, errors, register } = useForm();
  const [showPassword, setShowPassword] = useState("password");

  const togglePassword = () => {
    if (showPassword === "password") {
      setShowPassword("text");
    } else {
      setShowPassword("password");
    }
  };

  const PasswordRef = useRef();

  useEffect(() => {
    if (PasswordRef.current) {
      PasswordRef.current.focus();
    }
  }, [PasswordRef]);

  useEffect(() => {
    if (createToken.data?.data) {
      newToken(createToken.data.data);
      toggle(null);
    }
  }, [createToken.data, newToken, toggle]);

  const formStyle = {
    display: "flex",
    flexWrap: "wrap",
    minWidth: "100px",
    flexFlow: "row wrap-reverse",
    aligntContent: "flex-end",
  };

  if (!user) return ""; //loading...

  return (
    <Box>
      <form onSubmit={handleSubmit(createToken.mutate)} style={formStyle}>
        <HStack>
          <Button
            variant="solid"
            colorScheme="primary"
            type="submit"
            isLoading={createToken.isLoading}
          >
            Submit
          </Button>

          <FormControl isInvalid={errors.password}>
            <InputGroup minWidth="300px">
              <InputLeftElement onClick={togglePassword}>
                <Icon icon="password" />
              </InputLeftElement>
              <Input
                colorScheme="primary"
                variant="filled"
                isDisabled={createToken.isLoading}
                autoComplete="on"
                placeholder="Your Bugout password"
                name="password"
                type={showPassword}
                ref={(e) => {
                  register(e, { required: "Password is required!" });
                  PasswordRef.current = e;
                }}
              />
              <InputRightElement onClick={() => toggle(null)}>
                <CloseIcon />
              </InputRightElement>
            </InputGroup>
            <FormErrorMessage color="unsafe.400" pl="1" justifyContent="Center">
              {errors.password && errors.password.message}
            </FormErrorMessage>
          </FormControl>
          <Input
            type="hidden"
            ref={register}
            name="username"
            defaultValue={user?.username}
          />
        </HStack>
      </form>
    </Box>
  );
};
export default TokenRequest;
