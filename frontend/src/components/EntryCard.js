
import { jsx } from "@emotion/react";
import { Box } from "@chakra-ui/react";

const EntryCard = (props) => {
  const background = props.isActive ? "secondary.500" : "transparent";
  return (
    <Box
      py={2}
      px={6}
      borderTop="1px"
      borderColor="white.300"
      bg={background}
      transition="0.1s"
      _hover={props.isActive ? null : { bg: "secondary.200" }}
    >
      {props.children}
    </Box>
  );
};

export default EntryCard;
