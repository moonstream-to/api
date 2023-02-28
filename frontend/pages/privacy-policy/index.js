import React from "react";
import { Box, Heading, Link, Text } from "@chakra-ui/react";
import { DEFAULT_METATAGS } from "../../src/core/constants";
import { getLayout, getLayoutProps } from "../../src/layouts/WideInfoPage";

const PrivacyPolicy = () => (
  <Box mt="72px">
    <Box m="auto" mb={8} maxWidth="1238px" minHeight="60vh">
      <Heading my={8} as="h1">
        Privacy Policy for Moonstream
      </Heading>
      <Text fontSize="md">
        At Moonstream, accessible from https://moonstream.to/, one of our main
        priorities is the privacy of our visitors. This Privacy Policy document
        contains types of information that is collected and recorded by
        Moonstream and how we use it. If you have additional questions or
        require more information about our Privacy Policy, do not hesitate to
        <Link color="primary.600" href="#contact">
          {" "}
          contact us
        </Link>
        . This Privacy Policy applies only to our online activities and is valid
        for visitors to our website with regards to the information that they
        shared and/or collect in Moonstream. This policy is not applicable to
        any information collected offline or via channels other than this
        website. Consent By using our website, you hereby consent to our Privacy
        Policy and agree to its terms. Information we collect The personal
        information that you are asked to provide, and the reasons why you are
        asked to provide it, will be made clear to you at the point we ask you
        to provide your personal information. If you{" "}
        <Link color="primary.600" href="#contact">
          contact us{" "}
        </Link>
        directly, we may receive additional information about you such as your
        name, email address, phone number, the contents of the message and/or
        attachments you may send us, and any other information you may choose to
        provide. When you register for an Account, we may ask for your contact
        information, including items such as name, company name, address, email
        address, and telephone number.
      </Text>
      <Heading mt={4} size="md">
        Consent
      </Heading>
      <Text mt={4} fontSize="md">
        By using our website, you hereby consent to our Privacy Policy and agree
        to its terms.
      </Text>
      <Heading mt={4} size="md">
        Information we collect
      </Heading>
      <Text mt={4} fontSize="md">
        The personal information that you are asked to provide, and the reasons
        why you are asked to provide it, will be made clear to you at the point
        we ask you to provide your personal information. If you{" "}
        <Link color="primary.600" href="#contact">
          contact us{" "}
        </Link>
        directly, we may receive additional information about you such as your
        name, email address, phone number, the contents of the message and/or
        attachments you may send us, and any other information you may choose to
        provide. When you register for an Account, we may ask for your contact
        information, including items such as name, company name, address, email
        address, and telephone number.
      </Text>
      <Heading mt={4} size="md">
        How we use your information
      </Heading>
      <Text mt={4} fontSize="md">
        We use the information we collect in various ways, including to:
        <li>Provide, operate, and maintain our webste</li>
        <li>Improve, personalize, and expand our webste</li>
        <li>Understand and analyze how you use our webste</li>
        <li>Develop new products, services, features, and functionality</li>
        <li>
          Communicate with you directly, including for customer service, to
          provide you with updates and other information relating to the webste,
          and for marketing and promotional purposes
        </li>
        <li>Send you emails</li>
        <li>Find and prevent fraud</li>
        <li>address, email address, and telephone number.</li>
      </Text>
      <Heading mt={4} size="md">
        Log Files
      </Heading>
      <Text mt={4} fontSize="md">
        {`Moonstream follows a standard procedure of using log files. These files
        log visitors when they visit websites. All hosting companies do this and
        a part of hosting services' analytics. The information collected by log
        files include internet protocol (IP) addresses, browser type, Internet
        Service Provider (ISP), date and time stamp, referring/exit pages, and
        possibly the number of clicks. These are not linked to any information
        that is personally identifiable. The purpose of the information is for
        analyzing trends, administering the site, tracking users' movement on
        the website, and gathering demographic information.`}
      </Text>
      <Heading mt={4} size="md">
        Third Party Privacy Policies
      </Heading>
      <Text mt={4} fontSize="md">
        {`Moonstream's Privacy Policy does not apply to other advertisers or
        websites. Thus, we are advising you to consult the respective Privacy
        Policies of these third-party ad servers for more detailed information.
        It may include their practices and instructions about how to opt-out of
        certain options.`}
      </Text>
      <Heading mt={4} size="md">
        Third Party Privacy Policies
      </Heading>
      <Text mt={4} fontSize="md">
        {`Moonstream's Privacy Policy does not apply to other advertisers or
        websites. Thus, we are advising you to consult the respective Privacy
        Policies of these third-party ad servers for more detailed information.
        It may include their practices and instructions about how to opt-out of
        certain options.`}
      </Text>
      <Text mt={4} fontSize="md">
        {`You can choose to disable cookies through your individual browser
        options. To know more detailed information about cookie management with
        specific web browsers, it can be found at the browsers' respective
        websites.`}
      </Text>
      <Heading mt={4} size="md">
        CCPA Privacy Rights (Do Not Sell My Personal Information)
      </Heading>
      <Text mt={4} fontSize="md">
        {`Under the CCPA, among other rights, California consumers have the right
        to: Request that a business that collects a consumer's personal data
        disclose the categories and specific pieces of personal data that a
        business has collected about consumers. Request that a business delete
        any personal data about the consumer that a business has collected.
        Request that a business that sells a consumer's personal data, not sell
        the consumer's personal data. If you make a request, we have one month
        to respond to you. If you would like to exercise any of these rights,
        please `}
        <Link color="primary.600" href="#contact">
          contact us
        </Link>
        .
      </Text>
      <Heading mt={4} size="md">
        GDPR Data Protection Rights
      </Heading>
      <Text mt={4} fontSize="md">
        We would like to make sure you are fully aware of all of your data
        protection rights. Every user is entitled to the following: The right to
        access – You have the right to request copies of your personal data. We
        may charge you a small fee for this service. The right to rectification
        – You have the right to request that we correct any information you
        believe is inaccurate. You also have the right to request that we
        complete the information you believe is incomplete. The right to erasure
        – You have the right to request that we erase your personal data, under
        certain conditions. The right to restrict processing – You have the
        right to request that we restrict the processing of your personal data,
        under certain conditions. The right to object to processing – You have
        the right to object to our processing of your personal data, under
        certain conditions. The right to data portability – You have the right
        to request that we transfer the data that we have collected to another
        organization, or directly to you, under certain conditions. If you make
        a request, we have one month to respond to you. If you would like to
        exercise any of these rights, please{" "}
        <Link color="primary.600" href="#contact">
          contact us
        </Link>
        .
      </Text>
      <Heading mt={4} size="md">
        {`Children's Information`}
      </Heading>
      <Text mt={4} fontSize="md">
        Another part of our priority is adding protection for children while
        using the internet. We encourage parents and guardians to observe,
        participate in, and/or monitor and guide their online activity.
        Moonstream does not knowingly collect any Personal Identifiable
        Information from children under the age of 13. If you think that your
        child provided this kind of information on our website, we strongly
        encourage you to{" "}
        <Link color="primary.600" href="#contact">
          contact us
        </Link>{" "}
        immediately and we will do our best efforts to promptly remove such
        information from our records.
      </Text>
      <a id="contact">
        <Heading mt={4} size="md">
          Contact information
        </Heading>
      </a>
      <Text mt={4} fontSize="md">
        Contact us by reaching out to info@moonstream.to.
      </Text>
    </Box>
  </Box>
);

PrivacyPolicy.getLayout = getLayout;

export async function getStaticProps() {
  const layoutProps = getLayoutProps();
  const metaTags = {
    title: "Moonstream: privacy policy",
    description: "Privacy policy and legal information",
    keywords: "moonstream, privacy, policy, legal",
    url: "https://www.moonstream.to/privacy-policy",
  };
  layoutProps.props.metaTags = {
    ...layoutProps.props.metaTags,
    ...DEFAULT_METATAGS,
    ...metaTags,
  };
  return { ...layoutProps };
}

export default PrivacyPolicy;
