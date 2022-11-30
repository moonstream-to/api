import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Text,
  Stack,
  Box,
  FormControl,
  InputGroup,
  Input,
  InputRightElement,
  Button,
} from "@chakra-ui/react";
import CustomIcon from "./CustomIcon";
import { useLogin } from "../core/hooks";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const SignIn = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const { login, isLoading, data } = useLogin();
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (!data) {
      return;
    }

    toggleModal({ type: MODAL_TYPES.OFF });
  }, [data, toggleModal]);

  return (
    <>
      <form onSubmit={handleSubmit(login)}>
        <Stack width="100%" spacing={3}>
          <div
            style={{
              fontSize: "18px",
              fontWeight: 400,
              color: errors.username ? "#EE8686" : "white",
            }}
          >
            {errors.username ? errors.username.message : "Username"}
          </div>
          <FormControl isInvalid={errors.username}>
            <InputGroup bg="black">
              <Input
                autoComplete="username"
                variant="bw"
                placeholder="Enter your username or email"
                name="username"
                {...register("username", { required: true })}
                ref={register({ required: "Username is required" })}
              />
            </InputGroup>
          </FormControl>
          <div
            style={{
              fontSize: "18px",
              color: errors.password ? "#EE8686" : "white",
            }}
          >
            {errors.password ? errors.password.message : "Password"}
          </div>
          <FormControl isInvalid={errors.password}>
            <InputGroup bg="black">
              <Input
                autoComplete="current-password"
                variant="bw"
                placeholder="Enter your password"
                name="password"
                type={showPassword ? "text" : "password"}
                ref={register({ required: "Password is required" })}
              />
              <InputRightElement
                onClick={() => setShowPassword(!showPassword)}
                style={{ cursor: "pointer" }}
              >
                <CustomIcon icon="password" />
              </InputRightElement>
            </InputGroup>
          </FormControl>
          <Text textAlign="start" fontSize="18px">
            {" "}
            <Box
              cursor="pointer"
              color="#EE8686"
              as="span"
              onClick={() => toggleModal({ type: MODAL_TYPES.FORGOT })}
            >
              Forgot your password?
            </Box>
          </Text>
        </Stack>

        <Button
          mt="30px"
          mb="10px"
          h="46px"
          fontSize="lg"
          variant="plainOrange"
          type="submit"
          width="100%"
          isLoading={isLoading}
        >
          Login
        </Button>
      </form>

      <Text textAlign="center" fontSize="md" color="white">
        Don`t have an account?{" "}
        <Box
          cursor="pointer"
          color="#EE8686"
          as="span"
          onClick={() => toggleModal({ type: MODAL_TYPES.SIGNUP })}
        >
          Register
        </Box>
      </Text>
    </>
  );
};

export default SignIn;
