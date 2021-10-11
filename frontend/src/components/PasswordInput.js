import React, { useState } from "react";
import { InputGroup, InputRightElement, Input } from "@chakra-ui/react";
import CustomIcon from "./CustomIcon";

const PasswordInput = ({ placeholder, name }, ref) => {
  const [showPassword, togglePassword] = useState(false);

  return (
    <InputGroup>
      <Input
        variant="filled"
        colorScheme="blue"
        autoComplete="current-password"
        placeholder={placeholder}
        name={name}
        type={showPassword ? "text" : "password"}
        ref={ref}
      />
      <InputRightElement onClick={() => togglePassword(!showPassword)}>
        <CustomIcon icon="password" />
      </InputRightElement>
    </InputGroup>
  );
};

export default React.forwardRef(PasswordInput);
