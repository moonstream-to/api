
import { jsx } from "@emotion/react";
import { Box, LinkBox } from "@chakra-ui/react";

const JournalLinkBox = (props) => {
  return (
    <LinkBox
      as={Box}
      alignItems="baseline"
      px={2}
      py={1}
      my={1}
      mx={1}
      bg={props.isActive ? "secondary.900" : "none"}
      color={props.isActive ? "white.200" : "white.200"}
      fontWeight={600}
      // transition="0.3s"
      fontSize="md"
      _hover={{
        boxShadow: "md",
        bg: props.isActive ? "secondary.900" : "primary.500",
        color: "white.200",
      }}
      borderRadius="sm"
      boxShadow={props.isActive ? "md" : "none"}
      variant="ghost"
      display="flex"
      flex="row"
      textOverflow="ellipsis"
      overflow="visible"
      {...props.props}
    >
      {props.children}
    </LinkBox>
  );
};

export default JournalLinkBox;
