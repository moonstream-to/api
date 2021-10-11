import { React, useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useChangePassword, useRouter } from "../core/hooks";
import {
  Box,
  FormControl,
  FormErrorMessage,
  InputGroup,
  Stack,
  Center,
  Button,
  Input,
  InputRightElement,
} from "@chakra-ui/react";
import { CustomIcon } from "../components";

const ChangePassword = () => {
  const router = useRouter();
  const { handleSubmit, errors, register, setError } = useForm();
  const { changePassword, data, isLoading } = useChangePassword();
  const [showPassword, setShowPassword] = useState({
    password: "password",
    newPassword: "password",
    confirmPassword: "password",
  });

  const togglePassword = (key) => {
    if (showPassword[key] === "password") {
      setShowPassword({ ...showPassword, [key]: "text" });
    } else {
      setShowPassword({ ...showPassword, [key]: "password" });
    }
  };
  const change = (data) => {
    if (data.newPassword !== data.confirmPassword) {
      return setError("confirmPassword", {
        type: "manual",
        message: "New password and confirm password does not match",
      });
    } else {
      changePassword({
        newPassword: data.newPassword,
        currentPassword: data.currentPassword,
      });
    }
  };

  useEffect(() => {
    if (data) router.push("/");
  }, [data, router]);

  useEffect(() => {
    document.title = `Security`;
  }, []);

  return (
    <Box alignSelf="flex-start" width="100%">
      <Center>
        <form className="form" onSubmit={handleSubmit(change)}>
          <Stack width="100%" pt={4} spacing={3}>
            <FormControl isInvalid={errors.newPassword}>
              <InputGroup>
                <Input
                  placeholder="Current password"
                  autoComplete="current-password"
                  name="currentPassword"
                  type={showPassword.password}
                  ref={register({ required: "Current password is required!" })}
                />
                <InputRightElement onClick={() => togglePassword("password")}>
                  <CustomIcon icon="password" />
                </InputRightElement>
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1">
                {errors.newPassword && errors.newPassword.message}
              </FormErrorMessage>
            </FormControl>
            <FormControl isInvalid={errors.newPassword}>
              <InputGroup>
                <Input
                  autoComplete="new-password"
                  placeholder="New password"
                  name="newPassword"
                  type={showPassword.newPassword}
                  ref={register({ required: "Password is required!" })}
                />
                <InputRightElement
                  onClick={() => togglePassword("newPassword")}
                >
                  <CustomIcon icon="password" />
                </InputRightElement>
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1">
                {errors.newPassword && errors.newPassword.message}
              </FormErrorMessage>
            </FormControl>
            <FormControl isInvalid={errors.confirmPassword}>
              <InputGroup>
                <Input
                  autoComplete="new-password"
                  placeholder="Confirm password"
                  name="confirmPassword"
                  type={showPassword.confirmPassword}
                  ref={register({ required: "Password is required!" })}
                />
                <InputRightElement
                  onClick={() => togglePassword("confirmPassword")}
                >
                  <CustomIcon icon="password" />
                </InputRightElement>
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1">
                {errors.confirmPassword && errors.confirmPassword.message}
              </FormErrorMessage>
            </FormControl>
          </Stack>
          <Stack></Stack>
          <Center>
            <Button
              my={8}
              variant="solid"
              colorScheme="blue"
              type="submit"
              isLoading={isLoading}
            >
              Save
            </Button>
          </Center>
        </form>
      </Center>
    </Box>
  );
};

export default ChangePassword;
