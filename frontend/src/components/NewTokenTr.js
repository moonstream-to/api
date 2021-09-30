import React, { useEffect, useRef, Fragment } from "react";
import {
  FormControl,
  FormErrorMessage,
  InputGroup,
  Input,
  Td,
  Tr,
} from "@chakra-ui/react";
import { CloseIcon } from "@chakra-ui/icons";
import IconButton from "./IconButton";

const NewTokenTr = ({ isOpen, toggleSelf, errors, register, journalName }) => {
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
          <Td>New Token:</Td>
          <Td>
            <FormControl isInvalid={errors.appName}>
              <InputGroup>
                <Input
                  fontSize="sm"
                  border="none"
                  width="60%"
                  defaultValue={journalName}
                  height="fit-content"
                  placeholder="App name"
                  name="appName"
                  ref={(e) => {
                    register(e, { required: "app name is required" });
                    inputRef.current = e;
                  }}
                />
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1">
                {errors.appName && errors.appName.message}
              </FormErrorMessage>
            </FormControl>
          </Td>
          <Td>
            <FormControl isInvalid={errors.appVersion}>
              <InputGroup>
                <Input
                  fontSize="sm"
                  border="none"
                  width="60%"
                  height="fit-content"
                  placeholder="App Version"
                  name="appVersion"
                  ref={(e) => {
                    register(e, { required: "app name is required" });
                  }}
                />
              </InputGroup>
              <FormErrorMessage color="red.400" pl="1">
                {errors.appVersion && errors.appVersion.message}
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

export default NewTokenTr;
