import React, { Fragment, useEffect, useState } from "react";
import {
  Text,
  Stack,
  Tooltip,
  useClipboard,
  Heading,
  Image,
  Spacer,
  Spinner,
  chakra,
  SimpleGrid,
  Box,
  Modal,
  ModalContent,
  ModalOverlay,
  IconButton,
  useDisclosure,
} from "@chakra-ui/react";
import { useToast } from "../../core/hooks";
import { useSubscriptions } from "../../core/hooks";
import moment from "moment";
import { AiOutlineMonitor } from "react-icons/ai";
import NewSubscription from "../NewSubscription";

const EthereumWhalewatchCard_ = ({
  entry,
  showOnboardingTooltips,
  className,
}) => {
  const [newSubscriptionWhaleType, setNewSubscriptionWhaleType] = useState();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { subscriptionsCache, subscriptionTypeIcons } = useSubscriptions();
  const [copyString, setCopyString] = useState(false);
  const [icon, setIcon] = useState(null);
  const { onCopy, hasCopied } = useClipboard(copyString, 1);
  const toast = useToast();

  useEffect(() => {
    if (hasCopied && copyString) {
      toast("Copied to clipboard", "success");
      setCopyString(false);
    } else if (copyString) {
      onCopy();
    }
  }, [copyString, onCopy, hasCopied, toast]);

  useEffect(() => {
    if (subscriptionTypeIcons) {
      setIcon(subscriptionTypeIcons.ethereum_whalewatch);
    }
  }, [subscriptionTypeIcons, setIcon]);
  if (subscriptionsCache.isLoading) return <Spinner />;

  const whales = {
    transactionsOut: entry?.event_data?.transactions_out[0] || {},
    transactionsIn: entry?.event_data?.transactions_in[0] || {},
    valueOut: entry?.event_data?.value_out[0] || {},
    valueIn: entry?.event_data?.value_in[0] || {},
  };

  Object.values(whales).forEach((whaleInfo) => {
    whaleInfo.color =
      subscriptionsCache.data.subscriptions.find((obj) => {
        return obj.address === whaleInfo.address;
      })?.color ?? "gray.500";
    whaleInfo.label =
      subscriptionsCache.data.subscriptions.find((obj) => {
        return obj.address === whaleInfo.address;
      })?.label ?? whaleInfo.address;
  });

  const rowLabels = {
    transactionsOut: "transactions sent",
    transactionsIn: "transactions received",
    valueOut: "WEI sent",
    valueIn: "WEI received",
  };

  const subscribeClicked = (whaleType) => {
    setNewSubscriptionWhaleType(whaleType);
    onOpen();
  };
  return (
    <Stack className={className}>
      <Modal
        isOpen={isOpen}
        onClose={onClose}
        size="2xl"
        scrollBehavior="outside"
      >
        <ModalOverlay />

        <ModalContent>
          <NewSubscription
            isFreeOption={false}
            onClose={onClose}
            initialAddress={whales[newSubscriptionWhaleType]?.address}
            initialType="ethereum_blockchain"
          />
        </ModalContent>
      </Modal>
      <Tooltip
        hasArrow
        isOpen={showOnboardingTooltips}
        label="This is an Ethereum whale watch event. It shows top movers on the Ethereum blockchain in the given time period."
        variant="onboarding"
        placement="top"
      >
        <Stack
          className="title"
          direction="row"
          w="100%"
          h="1.6rem"
          minH="1.6rem"
          textAlign="center"
          spacing={0}
          alignItems="center"
          bgColor="gray.300"
        >
          {icon ? <Image boxSize="16px" src={icon} /> : ""}
          <Heading px={1} size="xs" isTruncated>
            Ethereum whale watch
          </Heading>
          <Spacer />
          <Text isTruncated pr={12}>
            {`${moment(entry.event_data.date_range.start_time).format(
              "ll [from] LT"
            )} to ${moment(entry.event_data.date_range.end_time).format(
              moment(entry.event_data.date_range.start_time).format("l") ===
                moment(entry.event_data.date_range.end_time).format("l")
                ? "LT"
                : "lll"
            )}`}
          </Text>
        </Stack>
      </Tooltip>
      <SimpleGrid columns={9} w="100%" minWidth="min-content">
        <Text
          gridColumn="1 / 3"
          h="100%"
          w="100%"
          fontSize="sm"
          py="2px"
          px={2}
          fontWeight="600"
          // w={showFullView ? null : "120px"}
          justifyContent="flex-start"
        >
          Whale
        </Text>
        <Text
          gridColumn="3 / 8"
          h="100%"
          w="100%"
          fontSize="sm"
          py="2px"
          px={2}
          fontWeight="600"
          // w={showFullView ? null : "120px"}
          justifyContent="flex-start"
        >
          Address
        </Text>
        <Text
          gridColumn="8 / 10"
          h="100%"
          w="100%"
          fontSize="sm"
          py="2px"
          px={2}
          fontWeight="600"
          // w={showFullView ? null : "120px"}
          justifyContent="flex-start"
        >
          Value
        </Text>
        {Object.keys(whales).map((whaleType, idx) => {
          return (
            <Fragment key={`whale-whatch-${idx}`}>
              <Box gridColumn="1 / 3">
                <Text
                  h="100%"
                  w="100%"
                  fontSize="sm"
                  py="2px"
                  px={2}
                  justifyContent="flex-start"
                  isTruncated
                >
                  {rowLabels[whaleType]}
                </Text>
              </Box>
              <Stack
                gridColumn="3 / 8"
                mx={0}
                py="2px"
                fontSize="sm"
                bgColor={whales[whaleType].color}
                h="100%"
                direction="row"
              >
                <Box
                  onClick={() => setCopyString(whales[whaleType].address)}
                  isTruncated
                >
                  {whales[whaleType].label}
                </Box>
                <Spacer />
                {whales[whaleType].label === whales[whaleType].address && (
                  <Tooltip
                    label="subscribe to this address"
                    variant="onboarding"
                  >
                    <Box boxSize="min-content">
                      <IconButton
                        onClick={() => subscribeClicked(whaleType)}
                        colorScheme="orange"
                        variant="outline"
                        m={0}
                        boxSize="24px"
                        icon={<AiOutlineMonitor />}
                      />
                    </Box>
                  </Tooltip>
                )}
              </Stack>
              <Box
                gridColumn="8 / 10"
                mx={0}
                py="2px"
                fontSize="sm"
                isTruncated
                w="calc(100%)"
                h="100%"
                textAlign="left"
                pl={2}
              >
                {whales[whaleType].statistic}
              </Box>
            </Fragment>
          );
        })}
      </SimpleGrid>
    </Stack>
  );
};

const EthereumWhalewatchCard = chakra(EthereumWhalewatchCard_, {
  baseStyle: {
    my: 0,
    direction: "column",
    flexBasis: "10px",
    flexGrow: 1,
    borderWidth: "2px",
    borderLeftRadius: "md",
    borderColor: "gray.600",
    spacing: 0,
    h: "auto",
    overflowX: "hidden",
    overflowY: "visible",
  },
});

export default EthereumWhalewatchCard;
