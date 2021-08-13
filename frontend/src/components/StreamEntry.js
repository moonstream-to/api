import React, { useContext, useEffect, useState } from "react";
import {
  Flex,
  Text,
  IconButton,
  Stack,
  Tooltip,
  useClipboard,
  Heading,
  Image,
  useMediaQuery,
  Spacer,
  Spinner,
} from "@chakra-ui/react";
import moment from "moment";
import { ArrowRightIcon } from "@chakra-ui/icons";
import UIContext from "../core/providers/UIProvider/context";
import { useToast } from "../core/hooks";
import { useSubscriptions } from "../core/hooks";

const StreamEntry = ({ entry }) => {
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
      return obj.address === entry.from_address;
    })?.color ?? "gray.500";

  const to_color =
    subscriptionsCache.data.subscriptions.find((obj) => {
      return obj.address === entry.to_address;
    })?.color ?? "gray.500";

  return (
    <Flex
      p={0}
      m={1}
      mr={2}
      borderRadius="md"
      borderTop="1px"
      bgColor="gray.100"
      borderColor="white.300"
      transition="0.1s"
      flexBasis="50px"
      direction="row"
      justifySelf="center"
      justifyContent="normal"
      alignItems="baseline"
      boxShadow="lg"
      minH="fit-content"
    >
      <Stack
        direction="row"
        flexBasis="100px"
        flexGrow={1}
        minW="100px"
        h="100%"
        spacing={0}
      >
        {true && (
          <Stack
            my={0}
            direction="column"
            flexBasis="10px"
            flexGrow={1}
            borderWidth="2px"
            borderLeftRadius="md"
            borderColor="gray.600"
            spacing={0}
            h="auto"
            // h="fit-content"
            // minH="fit-content"
            overflowX="hidden"
            overflowY="visible"
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
                onClick={() => setCopyString(entry.hash)}
                pr={12}
              >
                {entry.hash}
              </Text>
            </Stack>
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
                <Tooltip label={entry.from_address} aria-label="From:">
                  <Text
                    mx={0}
                    py="2px"
                    fontSize="sm"
                    bgColor={from_color}
                    isTruncated
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.from_address)}
                  >
                    {entry.from_label ?? entry.from_address}
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
                <Tooltip label={entry.to_address} aria-label="From:">
                  <Text
                    bgColor={to_color}
                    isTruncated
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.to_address)}
                  >
                    {entry.to_label ?? entry.to_address}
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
                <Tooltip label={entry.gasPrice} aria-label="Gas Price:">
                  <Text
                    mx={0}
                    py="2px"
                    fontSize="sm"
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.gasPrice)}
                  >
                    {entry.gasPrice}
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
                <Tooltip label={entry.gas} aria-label="Gas:">
                  <Text
                    mx={0}
                    py="2px"
                    fontSize="sm"
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.gas)}
                  >
                    {entry.gas}
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
                <Tooltip label={entry.value} aria-label="Value:">
                  <Text
                    mx={0}
                    py="2px"
                    fontSize="sm"
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.value)}
                  >
                    {entry.value}
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
                <Tooltip label={entry.value} aria-label="Value:">
                  <Text
                    mx={0}
                    py="2px"
                    fontSize="sm"
                    w="calc(100%)"
                    h="100%"
                    onClick={() => setCopyString(entry.value)}
                  >
                    {entry.nonce}
                  </Text>
                </Tooltip>
              </Flex>
              {entry.timestamp && (
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
                    {moment(entry.timestamp * 1000).format(
                      "DD MMM, YYYY, HH:mm:ss"
                    )}{" "}
                  </Text>
                </Flex>
              )}
            </Flex>
          </Stack>
        )}
        <Flex>
          <IconButton
            m={0}
            onClick={() => ui.setCurrentTransaction(entry)}
            h="full"
            // minH="24px"
            borderLeftRadius={0}
            variant="solid"
            px={0}
            minW="24px"
            colorScheme="secondary"
            icon={<ArrowRightIcon w="24px" />}
          />
        </Flex>
      </Stack>
    </Flex>
  );
};

export default StreamEntry;
