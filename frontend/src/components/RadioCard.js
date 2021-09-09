import React from "react";
import { useRadio, Box, Flex, Tooltip, Image } from "@chakra-ui/react";

const RadioCard = (props) => {
  const { getInputProps, getCheckboxProps } = useRadio(props);

  const input = getInputProps();
  const checkbox = getCheckboxProps();

  return (
    <Tooltip
      hidden={props.label ? false : true}
      label={props.label}
      variant="suggestion"
      openDelay={500}
    >
      <Flex as="label" h="fill-availible">
        <input {...input} />
        <Box
          alignContent="center"
          {...checkbox}
          cursor="pointer"
          borderWidth="1px"
          borderRadius="lg"
          boxShadow="md"
          _disabled={{
            bg: "gray.300",
            color: "gray.900",
            borderColor: "gray.300",
          }}
          _checked={{
            // bg: "secondary.900",

            color: "secondary.900",
            borderColor: "secondary.900",
            borderWidth: "4px",
          }}
          justifyContent="center"
          px={props.px}
          mt={props.mt}
          py={props.py}
          w={props.w}
          fontWeight="600"
        >
          {props.iconURL && (
            <Image display="inline-block" w="16px" src={props.iconURL} />
          )}{" "}
          {props.children}
        </Box>
      </Flex>
    </Tooltip>
  );
};

export default RadioCard;
