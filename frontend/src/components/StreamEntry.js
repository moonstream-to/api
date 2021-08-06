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
} from "@chakra-ui/react";
import moment from "moment";
import { ArrowRightIcon } from "@chakra-ui/icons";
import { useRouter } from "../core/hooks";
import UIContext from "../core/providers/UIProvider/context";
import { useToast, useTxCashe } from "../core/hooks";

const StreamEntry = ({ entry, filterCallback, filterConstants }) => {
  const ui = useContext(UIContext);
  const router = useRouter();
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
  const handleViewClicked = (entryId) => {
    ui.setEntryId(entryId);
    ui.setEntriesViewMode("entry");
    useTxCashe.setCurrentTransaction(entry);
    router.push({
      pathname: `/stream/${entry.hash}`,
      query: router.query,
    });
  };

  const [showFullView] = useMediaQuery(["(min-width: 420px)"]);

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
      _hover={{ bg: "secondary.200" }}
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
            h="fit-content"
            minH="fit-content"
            overflowX="hidden"
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
              bgColor="brand.300"
            >
              <Image
                boxSize="16px"
                src={
                  "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg"
                }
              />
              <Heading size="xs">Ethereum blockhain</Heading>
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
                  bgColor="secondary.500"
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
                    bgColor="secondary.200"
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
                  bgColor="primary.500"
                  h="100%"
                  color="white"
                  py={1}
                  px={2}
                  w={showFullView ? null : "120px"}
                >
                  To:
                </Text>
                <Tooltip label={entry.to_address} aria-label="From:">
                  <Text
                    bgColor="primary.200"
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
            <Stack
              className="ValuesRow"
              direction={showFullView ? "row" : "column"}
              alignItems={showFullView ? "center" : "flex-start"}
              placeContent="space-evenly"
              // h="1rem"
              w="100%"
              // h="1.6rem"
              minH="2rem"
              textAlign="center"
              spacing={0}
              bgColor="primimary.50"
            >
              <Stack
                direction="row"
                fontSize="sm"
                fontWeight="600"
                borderColor="gray.1200"
                borderRightWidth={showFullView ? "1px" : "0px"}
                placeContent="center"
                spacing={0}
                flexBasis="10px"
                flexGrow={1}
                w="100%"
              >
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
              </Stack>
              <Stack
                direction="row"
                fontSize="sm"
                fontWeight="600"
                borderColor="gray.1200"
                borderRightWidth={showFullView ? "1px" : "0px"}
                placeContent="center"
                spacing={0}
                flexBasis="10px"
                flexGrow={1}
                w="100%"
              >
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
              </Stack>
              <Stack
                direction="row"
                fontSize="sm"
                fontWeight="600"
                borderColor="gray.1200"
                borderRightWidth={
                  entry.timestamp ? (showFullView ? "1px" : "0px") : "0px"
                }
                placeContent="center"
                spacing={0}
                flexBasis="10px"
                flexGrow={1}
                w="100%"
              >
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
              </Stack>
              {entry.timestamp && (
                <Stack
                  direction="row"
                  fontSize="sm"
                  fontWeight="600"
                  placeContent="center"
                  spacing={0}
                  flexBasis="10px"
                  flexGrow={1}
                >
                  <Text mx={0} py="2px" fontSize="sm" w="calc(100%)" h="100%">
                    {moment(entry.timestamp * 1000).format(
                      "DD MMM, YYYY, HH:mm:ss"
                    )}{" "}
                  </Text>
                </Stack>
              )}
            </Stack>
          </Stack>
        )}
        <Flex>
          <IconButton
            m={0}
            onClick={() => handleViewClicked(entry)}
            h="full"
            // minH="24px"
            borderLeftRadius={0}
            variant="solid"
            px={0}
            minW="24px"
            colorScheme="suggested"
            icon={<ArrowRightIcon w="24px" />}
          />
        </Flex>
      </Stack>
    </Flex>
  );
};

export default StreamEntry;
