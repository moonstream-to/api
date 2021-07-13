
import { jsx } from "@emotion/react";
import { useEffect, useRef, Fragment } from "react";
import {
  FormControl,
  FormErrorMessage,
  InputGroup,
  Input,
  Select,
  Td,
  Tr,
} from "@chakra-ui/react";
import { CloseIcon } from "@chakra-ui/icons";

import IconButton from "./IconButton";

const AddUserForm = ({ isOpen, toggleSelf, errors, register }) => {
  const inputRef = useRef(null);
  useEffect(() => {
    if (isOpen) {
      //without timeout input is not catching focus on chrome and firefox..
      //probably because it is hidden within accordion
      setTimeout(() => {
        inputRef.current.focus();
      }, 100);
    }
  }, [inputRef, isOpen]);

  return (
    <Fragment>
      {isOpen && (
        <Tr transition="0.3s" _hover={{ bg: "white.200" }}>
          <Td></Td>
          <Td>
            <FormControl isInvalid={errors.email}>
              <InputGroup>
                <Input
                  fontSize="sm"
                  border="none"
                  width="60%"
                  height="fit-content"
                  placeholder="email"
                  name="email"
                  ref={(e) => {
                    register(e, { required: "email is required" });
                    inputRef.current = e;
                  }}
                />
              </InputGroup>
              <FormErrorMessage color="unsafe.400" pl="1">
                {errors.email && errors.email.message}
              </FormErrorMessage>
            </FormControl>
          </Td>

          <Td>
            <FormControl isInvalid={errors.role}>
              <Select
                _focus={{ outline: "solid 1px", outlineColor: "primary.500" }}
                fontSize="sm"
                border="none"
                placeholder="Select role"
                name="role"
                width="200px"
                height="fit-content"
                bgColor="white.200"
                ref={(e) => {
                  register(e, {
                    required: "Role is required",
                  });
                }}
              >
                <option>member</option>
                {/* <option>admin</option> */}
                <option>owner</option>
              </Select>
              <FormErrorMessage color="unsafe.400" pl="1">
                {errors.role && errors.role.message}
              </FormErrorMessage>
            </FormControl>
          </Td>

          <Td>
            <IconButton type="submit" />
            <IconButton
              onClick={() => toggleSelf(false)}
              icon={<CloseIcon />}
            />
          </Td>
        </Tr>
      )}
    </Fragment>
  );
};

export default AddUserForm;
