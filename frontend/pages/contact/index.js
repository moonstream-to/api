import React from "react";
import { Box, Center, VStack, Text, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import HubspotForm from "react-hubspot-form";

const Contact = () => (
  <Box>
    <Box px="1.5rem" m="auto" mb={8} minWidth="1000px" minHeight="60vh">
      {/* <Heading my={8} as="h1">
        Contact Us
      </Heading> */}
      <Center>
        <VStack>
          <Text my={10} fontSize={["lg", "xl"]}>
            Thanks for your interest in Moonstream Engine.
            <br />
            Please answer these questions to get started.
          </Text>
        </VStack>
      </Center>
      <HubspotForm
        portalId="8018701"
        formId="b54d192f-59b1-410a-8ac1-a1e8383c423c"
        loading={<Spinner colorScheme="primary" speed="1s" />}
      />
    </Box>
  </Box>
);

Contact.getLayout = getLayout;

export async function getStaticProps() {
  const layoutProps = getLayoutProps();
  // const metaTags = {
  //   title: "Moonstream: privacy policy",
  //   description: "Privacy policy and legal information",
  //   keywords: "moonstream, privacy, policy, legal",
  //   url: "https://www.moonstream.to/privacy-policy",
  // };
  // layoutProps.props.metaTags = {
  //   ...layoutProps.props.metaTags,
  //   ...DEFAULT_METATAGS,
  //   ...metaTags,
  // };
  return { ...layoutProps };
}

export default Contact;
