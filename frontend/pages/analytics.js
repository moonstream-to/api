import React, { useEffect } from "react";
import HubspotForm from "react-hubspot-form";
import { getLayout } from "../src/layouts/AppLayout";
import { Spinner, Flex, Heading } from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";

const Analytics = () => {
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Analytics: Page under construction`;
    }
  }, []);

  return (
    <Scrollable>
      <Flex
        h="100%"
        w="100%"
        m={0}
        px="7%"
        direction="column"
        alignItems="center"
      >
        <Heading as="h1" py={4}>
          This section is under construction
        </Heading>
        <Heading as="h2" size="sm" py={2}>
          Message us to tell your needs for this page
        </Heading>
        <HubspotForm
          portalId="8018701"
          formId="39bc0fbe-41c4-430a-b885-46eba66c59c2"
          loading={<Spinner colorScheme="blue" speed="1s" />}
        />
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
