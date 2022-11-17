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
            variant="bw"
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
        fontSize="lg"
        h="46px"
        type="submit"
        width="100%"
        variant="plainOrange"
        isLoading={isLoading}
      >
        Send
      </Button>
    </form>
  );
};

export default ForgotPassword;
