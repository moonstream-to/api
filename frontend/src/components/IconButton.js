
import { jsx } from "@emotion/react";
import { IconButton as IconButtonChakra } from "@chakra-ui/react";
import { CheckIcon } from "@chakra-ui/icons";

const IconButton = (props) => {
  return (
    <IconButtonChakra
      p={0}
      boxSize="24px"
      icon={<CheckIcon boxSize="18px" />}
      bg="none"
      _hover={{ transform: "scale(1.2)" }}
      _focus={{ outline: "none" }}
      _active={{ bg: "none" }}
      {...props}
    />
  );
};
export default IconButton;
