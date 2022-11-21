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
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
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
              fontWeight: 400,
              color: errors.username ? "#EE8686" : "white",
            }}
          >
            {errors.email ? errors.email.message : "Email"}
          </div>
          <FormControl isInvalid={errors.email}>
            <InputGroup>
              <Input
                variant="bw"
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
        </Stack>
        <Button
          mt="30px"
          mb="10px"
          fontSize="lg"
          h="46px"
          type="submit"
          width="100%"
          variant="plainOrange"
          isLoading={isLoading}
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
