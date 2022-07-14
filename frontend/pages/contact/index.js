import React, { useEffect } from "react";
import { Box, Image, Center, VStack, Text, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import HubspotForm from "react-hubspot-form";
import { useRouter } from "next/router";

const Contact = () => {
  const router = useRouter();
  const formId = "b54d192f-59b1-410a-8ac1-a1e8383c423c";

  useEffect(() => {
    function handler(event) {
      if (
        event.data.type === "hsFormCallback" &&
        event.data.eventName === "onFormSubmitted"
      ) {
        if (event.data.id === formId) {
          router.push("/");
        }
      }
    }

    window.addEventListener("message", handler);
    return () => {
      window.removeEventListener("message", handler);
    };
  });

  return (
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
          formId={formId}
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
};

Contact.getLayout = getLayout;

export async function getStaticProps() {
  const layoutProps = getLayoutProps();
  const metaTags = {
    title: "Moonstream: Contact form",
    description:
      "Form requesting contact information to connect with Moonstream",
    keywords: "moonstream, contact, web3, game economy, get acquainted",
    url: "https://www.moonstream.to/contact",
  };
  layoutProps.props.metaTags = { ...layoutProps.props.metaTags, ...metaTags };
  return { ...layoutProps };
}

export default Contact;
