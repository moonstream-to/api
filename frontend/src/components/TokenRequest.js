import React from "react";
import {
  Box,
  InputGroup,
  InputLeftElement,
  FormControl,
  FormErrorMessage,
  Stack,
  Button,
  Input,
  chakra,
} from "@chakra-ui/react";
import { useEffect, useState, useRef } from "react";
import { Icon } from "../../src/Theme";

import { useForm } from "react-hook-form";
import { useUser, useTokens } from "../core/hooks";

const TokenRequest = ({ setNewToken, onClose }) => {
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
      setNewToken(createToken.data.data);
      onClose();
    }
  }, [createToken.data, setNewToken, onClose]);

  const formStyle = {
    display: "flex",
    flexWrap: "wrap",
    minWidth: "100px",
    flexFlow: "row wrap-reverse",
    aligntContent: "flex-end",
    width: "100%",
  };

  if (!user) return ""; //loading...

  return (
    <Box px={1} py={4}>
      <form onSubmit={handleSubmit(createToken.mutate)} style={formStyle}>
        <Stack direction="column" spacing={4} w="100%">
          <Stack direction="column" spacing={1}>
            <chakra.label for="pwd">API key label:</chakra.label>
            <Input
              w="100%"
              ref={register}
              name="token_note"
              placeholder="My API key label"
              type="search"
            />
          </Stack>
          <Stack direction="column" spacing={1}>
            <chakra.label for="pwd">Password:</chakra.label>
            <FormControl isInvalid={errors.password}>
              <InputGroup minWidth="300px">
                <InputLeftElement onClick={togglePassword}>
                  <Icon icon="password" />
                </InputLeftElement>

                <Input
                  id="pwd"
                  colorScheme="blue"
                  variant="filled"
                  isDisabled={createToken.isLoading}
                  placeholder="This action requires your password to confirm"
                  name="password"
                  type={showPassword}
                  ref={(e) => {
                    register(e, { required: "Password is required!" });
                    PasswordRef.current = e;
                  }}
                />
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1" justifyContent="Center">
                {errors.password && errors.password.message}
              </FormErrorMessage>
            </FormControl>
          </Stack>

          <Input
            type="hidden"
            ref={register}
            name="username"
            defaultValue={user?.username}
          />
          <Stack pt={9} direction="row" justifyContent="flex-end" w="100%">
            <Button
              m={0}
              variant="solid"
              colorScheme="blue"
              type="submit"
              isLoading={createToken.isLoading}
            >
              Submit
            </Button>
            <Button
              variant="solid"
              colorScheme="red"
              type="submit"
              onClick={() => onClose()}
            >
              Cancel
            </Button>
          </Stack>
        </Stack>
      </form>
    </Box>
  );
};
export default TokenRequest;
