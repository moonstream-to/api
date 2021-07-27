import { getLayout } from "../src/layouts/AppLayout";
import React, { useState } from "react";
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
  Modal,
  useDisclosure,
  ModalOverlay,
  ModalContent,
} from "@chakra-ui/react";
import { headingStyle } from "./index";
import NewSubscription from "../src/components/NewSubscription";
import { AiOutlinePlusCircle } from "react-icons/ai";

const Subscriptions = () => {
  const { subscriptionsCache } = useSubscriptions();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isAddingFreeSubscription, setIsAddingFreeSubscription] = useState();

  document.title = `My Subscriptions`;

  const newSubscriptionClicked = (isForFree) => {
    setIsAddingFreeSubscription(isForFree);
    onOpen();
  };
  return (
    <Box w="100%" px="7%" pt={2}>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size="2xl"
        scrollBehavior="outside"
      >
        <ModalOverlay />

        <ModalContent>
          <NewSubscription
            isFreeOption={isAddingFreeSubscription}
            onClose={onClose}
          />
        </ModalContent>
      </Modal>
      {subscriptionsCache.isLoading ? (
        <Center>
          <Spinner
            hidden={false}
            // ref={loadMoreButtonRef}
            my={8}
            size="lg"
            color="primary.500"
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
              bgColor="primary.50"
              borderTopRadius="xl"
              justifyContent="flex-end"
              alignItems="center"
            >
              {subscriptionsCache.data?.is_free_subscription_availible && (
                <Button
                  onClick={() => newSubscriptionClicked(true)}
                  mr={8}
                  colorScheme="suggested"
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
                colorScheme="primary"
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
  );
};

Subscriptions.getLayout = getLayout;
export default Subscriptions;
