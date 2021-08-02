import React from "react";
import { useRadio, Box, Flex } from "@chakra-ui/react";

const RadioCard = (props) => {
  const { getInputProps, getCheckboxProps } = useRadio(props);

  const input = getInputProps();
  const checkbox = getCheckboxProps();

  return (
    <Flex as="label" h="fill-availible">
      <input {...input} />
      <Box
        justifyContent="left"
        alignContent="center"
        {...checkbox}
        cursor="pointer"
        borderWidth="1px"
        borderRadius="md"
        boxShadow="md"
        _disabled={{
          bg: "gray.300",
          color: "gray.900",
          borderColor: "gray.300",
        }}
        _checked={{
          bg: "secondary.900",
          color: "white",
          borderColor: "secondary.900",
        }}
        _focus={{
          boxShadow: "outline",
        }}
        px={5}
        py={3}
        fontWeight="600"
      >
        {props.children}
      </Box>
    </Flex>
  );
};

// const RadioCard = chakra(RadioCard_);
export default RadioCard;
