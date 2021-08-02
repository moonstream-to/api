import React from "react";
import { Heading, Box, Text, Center, VStack } from "@chakra-ui/react";
const Page404 = () => (
  <Box pt={8} w="100%" h="100%">
    <Center>
      <VStack>
        <Heading>Ooops... 404 </Heading>
        <Text>Page not Found! </Text>
      </VStack>
    </Center>
  </Box>
);

export default Page404;
