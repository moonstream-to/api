import React, { useEffect } from "react";
import HubspotForm from "react-hubspot-form";
import { getLayout } from "../src/layouts/AppLayout";
import { Spinner, Flex, Heading } from "@chakra-ui/react";
import Scrollable from "../src/components/Scrollable";
import mixpanel from "mixpanel-browser";
import MIXPANEL_EVENTS from "../src/core/providers/AnalyticsProvider/constants";
import { useUser } from "../src/core/hooks";

const Analytics = () => {
  useEffect(() => {
    if (typeof window !== "undefined") {
      document.title = `Analytics: Page under construction`;
    }
  }, []);

  const { user } = useUser();

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
          loading={<Spinner colorScheme="primary" speed="1s" />}
          onSubmit={() =>
            mixpanel.track(MIXPANEL_EVENTS.FORM_SUBMITTED, {
              formType: "Hubspot analytics",
              user: user,
            })
          }
        />
      </Flex>
    </Scrollable>
  );
};

Analytics.getLayout = getLayout;
export default Analytics;
