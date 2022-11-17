import { getLayout } from "../src/layouts/AppLayout";
import React, { useContext } from "react";
import SubscriptionsList from "../src/components/SubscriptionsList";
import { useSubscriptions } from "../src/core/hooks";
import {
  Box,
  Center,
  Spinner,
  ScaleFade,
  Heading,
  Flex,
  Button,
} from "@chakra-ui/react";
import { AiOutlinePlusCircle } from "react-icons/ai";
import OverlayContext from "../src/core/providers/OverlayProvider/context";
import { MODAL_TYPES } from "../src/core/providers/OverlayProvider/constants";
import Scrollable from "../src/components/Scrollable";
const Subscriptions = () => {
  const { subscriptionsCache } = useSubscriptions();
  const modal = useContext(OverlayContext);

  document.title = `My Subscriptions`;

  // TODO(zomglings): This should be imported from some common location. For now, copied from
  // pages/account/security.js. It was attempting to get imported from "./index", but is not defined
  // there.
  const headingStyle = {
    as: "h2",
    pt: 2,
    mb: 4,
    borderBottom: "solid",
    borderColor: "blue.50",
    borderBottomWidth: "2px",
  };

  const newSubscriptionClicked = () => {
    modal.toggleModal({ type: MODAL_TYPES.NEW_SUBSCRIPTON });
  };
  return (
    <Scrollable>
      <Box w="100%" px="7%" pt={2}>
        {subscriptionsCache.isLoading ? (
          <Center>
            <Spinner
              hidden={false}
              my={8}
              size="lg"
              color="blue.500"
              thickness="4px"
              speed="1.5s"
            />
          </Center>
        ) : (
          <ScaleFade in>
            <Heading {...headingStyle}> My Subscriptions </Heading>
            <Flex
              mt={4}
              overflow="initial"
              maxH="unset"
              height="100%"
              direction="column"
            >
              <Flex
                h="3rem"
                w="100%"
                bgColor="black.300"
                borderColor="white"
                borderTopRadius="xl"
                justifyContent="flex-end"
                alignItems="center"
              >
                {subscriptionsCache.data?.is_free_subscription_availible && (
                  <Button
                    onClick={() => newSubscriptionClicked(true)}
                    mr={8}
                    colorScheme="green"
                    variant="solid"
                    size="sm"
                    rightIcon={<AiOutlinePlusCircle />}
                  >
                    Add for free
                  </Button>
                )}
                <Button
                  onClick={() => newSubscriptionClicked(false)}
                  mr={8}
                  colorScheme="blue"
                  variant="solid"
                  size="sm"
                  rightIcon={<AiOutlinePlusCircle />}
                >
                  Add new
                </Button>
              </Flex>
              <SubscriptionsList data={subscriptionsCache.data} />
            </Flex>
          </ScaleFade>
        )}
      </Box>
    </Scrollable>
  );
};

Subscriptions.getLayout = getLayout;
export default Subscriptions;
