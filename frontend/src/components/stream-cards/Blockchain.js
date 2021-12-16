import React, { useContext, useEffect, useState } from "react";
import {
  Flex,
  Text,
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
import UIContext from "../../core/providers/UIProvider/context";
import { useToast } from "../../core/hooks";
import { useSubscriptions } from "../../core/hooks";

const EthereumBlockchainCard_ = ({
  entry,
  showOnboardingTooltips,
  className,
}) => {
  const { subscriptionsCache } = useSubscriptions();
  const ui = useContext(UIContext);
  const [copyString, setCopyString] = useState(false);
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

  const [showFullView] = useMediaQuery(["(min-width: 420px)"]);
  if (subscriptionsCache.isLoading) return <Spinner />;

  const from_color =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === entry.event_data.from;
    })?.color ?? "gray.500";

  const from_label =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === entry.event_data.from;
    })?.label ?? entry.event_data.from;

  const to_color =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === entry.event_data.to;
    })?.color ?? "gray.500";

  const to_label =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === entry.event_data.to;
    })?.label ?? entry.event_data.to;

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
          <Image
            boxSize="16px"
            src={
              "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg"
            }
          />
          <Heading px={1} size="xs">
            Hash
          </Heading>
          <Spacer />
          <Text
            isTruncated
            onClick={() => setCopyString(entry.event_data.hash)}
            pr={12}
          >
            {entry.event_data.hash}
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
        <Stack
          overflow="hidden"
          textOverflow="ellipsis"
          whiteSpace="nowrap"
          direction="row"
          fontSize="sm"
          fontWeight="600"
          minw="min-content"
          w={showFullView ? "calc(50%)" : "calc(100%)"}
          h="100%"
          borderColor="gray.1200"
          borderRightWidth={showFullView ? "1px" : "0px"}
          placeContent="center"
          spacing={0}
        >
          <Tooltip
            hasArrow
            isOpen={showOnboardingTooltips && !ui.isMobileView}
            label="From and to addresses, clicking names will copy address to clipboard!"
            variant="onboarding"
            placement={ui.isMobileView ? "bottom" : "left"}
            maxW="150px"
          >
            <Text
              bgColor="gray.600"
              h="100%"
              fontSize="sm"
              py="2px"
              px={2}
              w={showFullView ? null : "120px"}
            >
              From:
            </Text>
          </Tooltip>
          <Tooltip label={entry.event_data.from} aria-label="From:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              bgColor={from_color}
              isTruncated
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.from)}
            >
              {from_label}
            </Text>
          </Tooltip>
        </Stack>

        <Stack
          overflow="hidden"
          textOverflow="ellipsis"
          whiteSpace="nowrap"
          direction="row"
          fontSize="sm"
          fontWeight="600"
          minw="min-content"
          w={showFullView ? "calc(50%)" : "calc(100%)"}
          h="100%"
          spacing={0}
        >
          <Text
            bgColor="gray.600"
            h="100%"
            py={1}
            px={2}
            w={showFullView ? null : "120px"}
          >
            To:
          </Text>
          <Tooltip label={entry.event_data.to} aria-label="From:">
            <Text
              bgColor={to_color}
              isTruncated
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.to)}
            >
              {to_label}
            </Text>
          </Tooltip>
        </Stack>
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
            Gas Price:
          </Text>
          <Tooltip label={entry.event_data.gasPrice} aria-label="Gas Price:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.gasPrice)}
            >
              {entry.event_data.gasPrice}
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
            Gas:
          </Text>
          <Tooltip label={entry.event_data.gas} aria-label="Gas:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.gas)}
            >
              {entry.event_data.gas}
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
            Value:
          </Text>
          <Tooltip label={entry.event_data.value} aria-label="Value:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.value)}
            >
              {entry.event_data.value}
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
            Nonce:
          </Text>
          <Tooltip label={entry.event_data.value} aria-label="Value:">
            <Text
              mx={0}
              py="2px"
              fontSize="sm"
              w="calc(100%)"
              h="100%"
              onClick={() => setCopyString(entry.event_data.value)}
            >
              {entry.event_data.nonce}
            </Text>
          </Tooltip>
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
    </Stack>
  );
};

const EthereumBlockchainCard = chakra(EthereumBlockchainCard_, {
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

export default EthereumBlockchainCard;
