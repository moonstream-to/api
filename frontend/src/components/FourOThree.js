import React from "react";
import { Heading, Box, Text, VStack, Center } from "@chakra-ui/react";
const Page403 = ({ location }) => (
  <Box pt={8} w="100%" h="100%">
    <Center>
      <VStack>
        <Heading>Agghr... Forbidden! </Heading>
        <Text>You have no permission to read</Text>
        <Text> {location.pathname}</Text>
      </VStack>
    </Center>
  </Box>
);
export default Page403;
