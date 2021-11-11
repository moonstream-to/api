import React from "react";
import { VStack, Heading } from "@chakra-ui/react";
import { getLayout } from "../../src/layouts/AppLayout";

const Papers = () => {
  return (
    <VStack>
      <Heading py={12}>DASHBOARD PLIX</Heading>
    </VStack>
  );
};

Papers.getLayout = getLayout;

export default Papers;
