import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import {
  Text,
  Stack,
  Box,
  FormControl,
  InputGroup,
  Button,
  Input,
  InputRightElement,
} from "@chakra-ui/react";
import CustomIcon from "./CustomIcon";
import { useSignUp } from "../core/hooks";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const SignUp = ({ toggleModal }) => {
  const { handleSubmit, errors, register } = useForm();
  const { signUp, isLoading, isSuccess } = useSignUp();
  const [showPassword, togglePassword] = useState(false);

  useEffect(() => {
    console.log(toggleModal);
    if (isSuccess) {
      toggleModal({ type: MODAL_TYPES.OFF });
    }
  }, [isSuccess, toggleModal]);

  return (
    <>
      <form onSubmit={handleSubmit(signUp)}>
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
            <InputGroup>
              <Input
                borderColor="white"
                bg="#1A1D22"
                color="white"
                _placeholder={{ textColor: "#CDCDCD" }}
                autoComplete="username"
                variant="outline"
                placeholder="Enter your username or email"
                errorBorderColor="#EE8686"
                name="username"
                {...register("username", { required: true })}
                ref={register({ required: "Username is required" })}
                _hover={{
                  backgroundColor: "#1A1D22",
                }}
                _focus={{
                  backgroundColor: "#1A1D22",
                }}
                _autofill={{
                  backgroundColor: "#1A1D22",
                  textFillColor: "white",
                  boxShadow: "0 0 0px 1000px #1A1D22 inset",
                  transition: "background-color 5000s ease-in-out 0s",
                }}
              />
            </InputGroup>
          </FormControl>
          <div
            style={{
              fontSize: "18px",
              fontWeight: 400,
              color: errors.username ? "#EE8686" : "white",
            }}
          >
            {errors.email ? errors.email.message : "Email"}
          </div>
          <FormControl isInvalid={errors.email}>
            <InputGroup>
              <Input
                borderColor="white"
                bg="#1A1D22"
                color="white"
                _placeholder={{ textColor: "#CDCDCD" }}
                variant="outline"
                errorBorderColor="#EE8686"
                _hover={{
                  backgroundColor: "#1A1D22",
                }}
                _focus={{
                  backgroundColor: "#1A1D22",
                }}
                _autofill={{
                  backgroundColor: "#1A1D22",
                  textFillColor: "white",
                  boxShadow: "0 0 0px 1000px #1A1D22 inset",
                  transition: "background-color 5000s ease-in-out 0s",
                }}
                placeholder="Enter your email"
                name="email"
                autoComplete="email"
                ref={register({ required: "Email is required" })}
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
                borderColor="white"
                bg="#1A1D22"
                color="white"
                _placeholder={{ textColor: "#CDCDCD" }}
                autoComplete="current-password"
                variant="outline"
                placeholder="Enter your password"
                errorBorderColor="#EE8686"
                name="password"
                type={showPassword ? "text" : "password"}
                ref={register({ required: "Password is required" })}
                _hover={{
                  backgroundColor: "#1A1D22",
                }}
                _focus={{
                  backgroundColor: "#1A1D22",
                }}
                _autofill={{
                  backgroundColor: "#1A1D22",
                  textFillColor: "white",
                  boxShadow: "0 0 0px 1000px #1A1D22 inset",
                  transition: "background-color 5000s ease-in-out 0s",
                }}
              />
              <InputRightElement onClick={() => togglePassword(!showPassword)}>
                <CustomIcon icon="password" />
              </InputRightElement>
            </InputGroup>
          </FormControl>
        </Stack>
        <Button
          mt="30px"
          mb="10px"
          bg="#F56646"
          fontWeight="700"
          borderRadius="30px"
          padding="10px 30px"
          fontSize="20px"
          height="46px"
          color="#ffffff"
          type="submit"
          width="100%"
          variant="solid"
          isLoading={isLoading}
          _hover={{
            backgroundColor: "#F4532F",
          }}
          _focus={{
            backgroundColor: "#F4532F",
          }}
          _active={{
            backgroundColor: "#F4532F",
          }}
        >
          Register
        </Button>
      </form>
      <Text textAlign="center" fontSize="md" color="white">
        Already have an account?{" "}
        <Box
          cursor="pointer"
          color="#EE8686"
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
