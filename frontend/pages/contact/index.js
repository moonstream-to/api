import React from "react";
import { Box, Image, Center, VStack, Text, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import HubspotForm from "react-hubspot-form";

const Contact = () => (
  <Box>
    <Box px="1.5rem" m="auto" mb={8} minWidth="1000px" minHeight="100vh">
      <Image></Image>
      <Center>
        <VStack>
          <Text my={5} fontSize={["lg", "xl"]} textAlign="center">
            Thanks for your interest in Moonstream.
            <br />
            Please answer some questions to help us get acquainted with you.
          </Text>
        </VStack>
      </Center>
      <HubspotForm
        portalId="8018701"
        formId="b54d192f-59b1-410a-8ac1-a1e8383c423c"
        loading={<Spinner colorScheme="primary" speed="1s" />}
      />
      <Center>
        <Text my={5} fontSize={["md", "lg"]} textAlign="center" width="60%">
          <i>
            Click the button to submit your answers. We&apos;ll reach out
            directly within 3 days. You will not receive any marketing emails
            from us.
          </i>
        </Text>
      </Center>
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
