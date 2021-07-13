
import { jsx } from "@emotion/react";
import { Circle, Text } from "@chakra-ui/react";

const CircleButton = ({ sign, onClick }) => {
  return (
    <Circle
      overflow="initial"
      transition="0.5s"
      _hover={{ bgColor: "primary.100", transform: "scale(1.2)" }}
      boxSize="28px"
      m="0 0.5rem"
      cursor="pointer"
      background="primary.800"
      boxShadow="0 4px 14px 0 rgba(33, 41, 144, 0.3)"
      // box-shadow: 0 4px 14px 0 rgba(33, 41, 144, 0.3);
      onClick={onClick}
    >
      <Text
        transition="1s"
        _hover={{ transform: "scale(1.5)" }}
        color="white.100"
      >
        {sign}
      </Text>
    </Circle>
  );
};

export default CircleButton;
