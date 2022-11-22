import React, { useEffect } from "react";
import { Box, Center, VStack, Text, Icon, Spinner } from "@chakra-ui/react";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";
import HubspotForm from "react-hubspot-form";
import { useRouter } from "next/router";
import { BiArrowBack } from "react-icons/bi";

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
      <Box
        px="1.5rem"
        py={10}
        m="auto"
        mb={8}
        minHeight="100vh"
        textColor="black"
        bgColor="white"
        position="relative"
        pt="72px"
      >
        <Icon
          as={BiArrowBack}
          w={["30px", "40px", "50px"]}
          h={["30px", "40px", "50px"]}
          onClick={() => {
            router.push("/");
          }}
          position="absolute"
          justifySelf="left"
          alignSelf="left"
        ></Icon>
        <Center>
          <VStack>
            <Text
              my={5}
              px={10}
              fontSize={["md", "lg", "xl"]}
              textAlign="center"
            >
              Thanks for your interest in Moonstream. Our tools are fully
              customized to your project. <br /> Please answer these questions
              to get started:
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
              We&apos;ll reach out directly within 3 business days after you
              submit this form. You won&apos;t be receiving any spam emails from
              us, only the most important technical updates.
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
