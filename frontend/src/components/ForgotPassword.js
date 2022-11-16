import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { useToast, useForgotPassword } from "../core/hooks";
import { FormControl, InputGroup, Button, Input } from "@chakra-ui/react";
import { MODAL_TYPES } from "../core/providers/OverlayProvider/constants";

const ForgotPassword = ({ toggleModal }) => {
  const toast = useToast();
  const { handleSubmit, errors, register } = useForm();
  const { forgotPassword, isLoading, data } = useForgotPassword();

  useEffect(() => {
    if (!data) return;
    toggleModal({ type: MODAL_TYPES.OFF });
  }, [data, toggleModal, toast]);

  return (
    <form onSubmit={handleSubmit(forgotPassword)}>
      <div
        style={{
          fontSize: "18px",
          fontWeight: 400,
          color: errors.username ? "#EE8686" : "white",
        }}
      >
        {errors.email ? errors.email.message : "Email"}
      </div>
      <FormControl isInvalid={errors.email} my={4}>
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
        Send
      </Button>
    </form>
  );
};

export default ForgotPassword;
