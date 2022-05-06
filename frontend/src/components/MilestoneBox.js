import { React } from "react";
import { chakra, Box, Text } from "@chakra-ui/react";

const _MilestoneBox = ({ headingText }) => {
  return (
    <Box
      minW={["150px", "180px", "300px", "300px", "400px", "500px"]}
      py={5}
      px={3}
    >
      <Text
        fontSize={["md", "2xl", "3xl", "4xl", "4xl", "4xl"]}
        ml={5}
        color="orange.500"
        fontWeight="bold"
        textAlign="center"
      >
        {headingText}
      </Text>
    </Box>
  );
};

const MilestoneBox = chakra(_MilestoneBox);

export default MilestoneBox;
