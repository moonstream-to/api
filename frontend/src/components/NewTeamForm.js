
import { jsx } from "@emotion/react";
import { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import {
  FormControl,
  FormErrorMessage,
  InputGroup,
  HStack,
  Input,
} from "@chakra-ui/react";
import { CloseIcon } from "@chakra-ui/icons";

import IconButton from "./IconButton";

const NewTeamForm = ({ createTeamCallback, toggleSelf }) => {
  const { handleSubmit, errors, register } = useForm();

  const inputRef = useRef();

  useEffect(() => {
    inputRef.current.focus();
  }, [inputRef]);

  return (
    <form onSubmit={handleSubmit(createTeamCallback)}>
      <HStack py={2} width="100%">
        <FormControl isInvalid={errors.teamName}>
          <InputGroup>
            <Input
              border="none"
              width="60%"
              placeholder="Team name"
              name="teamName"
              ref={(e) => {
                register(e, { required: "Name is required" });
                inputRef.current = e;
              }}
            />
          </InputGroup>
          <FormErrorMessage color="unsafe.400" pl="1">
            {errors.teamName && errors.teamName.message}
          </FormErrorMessage>
        </FormControl>
        <IconButton type="submit" />
        <IconButton onClick={() => toggleSelf(false)} icon={<CloseIcon />} />
      </HStack>
    </form>
  );
};
export default NewTeamForm;
