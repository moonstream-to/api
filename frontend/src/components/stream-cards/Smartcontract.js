import React, { useEffect, useState } from "react";
import {
  Flex,
  Text,
  Textarea,
  Stack,
  Tooltip,
  useClipboard,
  Heading,
  Image,
  useMediaQuery,
  Spacer,
  Spinner,
  chakra,
} from "@chakra-ui/react";
import moment from "moment";
import { useToast } from "../../core/hooks";
import { useSubscriptions } from "../../core/hooks";

const SmartcontractCard_ = ({ entry, showOnboardingTooltips, className }) => {
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
      setIcon(subscriptionTypeIcons.ethereum_);
    }
  }, [subscriptionTypeIcons, setIcon]);

  const [showFullView] = useMediaQuery(["(min-width: 420px)"]);
  if (subscriptionsCache.isLoading) return <Spinner />;

  const transaction = {
    ...entry.event_data,
  };

  const color =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === transaction.address;
    })?.color ?? "gray.500";

  const label =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === transaction.address;
    })?.label ?? transaction.address;

  return (
    <Stack className={className}>
      <Tooltip
        hasArrow
        isOpen={showOnboardingTooltips}
        label="Top of card describes type of event. Ethereum blockchain in this case. It as unique hash shown here"
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
          {icon ? (
            <Image
              boxSize="16px"
              src={
                "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg"
              }
            />
          ) : (
            ""
          )}
          <Heading px={1} size="xs">
            Hash
          </Heading>
          <Spacer />
          <Text
            isTruncated
            onClick={() => setCopyString(transaction.hash)}
            pr={12}
          >
            {transaction.hash}
          </Text>
        </Stack>
      </Tooltip>
      <Stack
        className="CardAddressesRow"
        direction={showFullView ? "row" : "column"}
        w="100%"
        h={showFullView ? "1.6rem" : "3.2rem"}
        minH="1.6rem"
        textAlign="center"
        spacing={0}
        alignItems="center"
      >
        <Text
          bgColor="gray.600"
          h="100%"
          py={1}
          px={2}
          w={showFullView ? null : "120px"}
        >
          address:
        </Text>
        <Tooltip label={transaction.address} aria-label="address:">
          <Text
            bgColor={color}
            isTruncated
            w="calc(100%)"
            h="100%"
            onClick={() => setCopyString(transaction.address)}
          >
            {label}
          </Text>
        </Tooltip>
      </Stack>
      <Flex flexWrap="wrap" w="100%">
        <Flex minH="2rem" minW="fit-content" flexGrow={1}>
          <Text
            h="100%"
            fontSize="sm"
            py="2px"
            px={2}
            whiteSpace="nowrap"
            w={showFullView ? null : "120px"}
            textAlign="justify"
          >
            log index:
          </Text>
          <Tooltip label={transaction.log_index} aria-label="Log index:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(transaction.log_index)}
            >
              {transaction.log_index}
            </Text>
          </Tooltip>
        </Flex>
        <Flex h="2rem" minW="fit-content" flexGrow={1}>
          <Text
            w={showFullView ? null : "120px"}
            h="100%"
            fontSize="sm"
            py="2px"
            px={2}
            textAlign="justify"
          >
            type:
          </Text>
          <Tooltip label={transaction?.label_data?.type} aria-label="type:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(transaction?.label_data?.type)}
            >
              {transaction?.label_data?.type}
            </Text>
          </Tooltip>
        </Flex>
        <Flex h="2rem" minW="fit-content" flexGrow={1}>
          <Text
            w={showFullView ? null : "120px"}
            h="100%"
            fontSize="sm"
            py="2px"
            px={2}
            textAlign="justify"
          >
            name:
          </Text>
          <Tooltip label={transaction?.label_data?.name} aria-label="Name:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(transaction?.label_data?.name)}
            >
              {transaction?.label_data?.name}
            </Text>
          </Tooltip>
        </Flex>

        <Flex h="2rem" minW="fit-content" flexGrow={1}>
          <Text
            minW="fit-content"
            h="100%"
            fontSize="sm"
            py="2px"
            px={2}
            textAlign="justify"
          >
            data:
          </Text>
        </Flex>
        {entry.event_timestamp && (
          <Flex h="auto" minW="fit-content">
            <Text
              px={1}
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              borderColor="gray.700"
            >
              {moment(entry.event_timestamp * 1000).format(
                "DD MMM, YYYY, HH:mm:ss"
              )}{" "}
            </Text>
          </Flex>
        )}
      </Flex>
      <Flex>
        {" "}
        <Tooltip label={transaction.value} aria-label="Value:">
          <Textarea
            mx={0}
            minH="max-content"
            py="4px"
            fontSize="sm"
            w="calc(100%)"
            value={JSON.stringify(transaction["label_data"], null, 4)}
            h="100%"
            onClick={() =>
              setCopyString(JSON.stringify(transaction["label_data"], null, 4))
            }
          ></Textarea>
        </Tooltip>
      </Flex>
    </Stack>
  );
};

const SmartcontractCard = chakra(SmartcontractCard_, {
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

export default SmartcontractCard;
