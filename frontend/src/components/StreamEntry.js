import React, { useContext } from "react";
import { Flex, Text, IconButton, Tag } from "@chakra-ui/react";
import moment from "moment";
import { ViewIcon } from "@chakra-ui/icons";
import { useRouter } from "../core/hooks";
import UIContext from "../core/providers/UIProvider/context";

const StreamEntry = ({ entry, filterCallback, filterConstants }) => {
  const ui = useContext(UIContext);
  const router = useRouter();

  const handleViewClicked = (entryId) => {
    ui.setEntryId(entryId);
    ui.setEntriesViewMode("entry");
    router.push({
      pathname: `/stream/${entry.id}`,
      query: router.query,
    });
  };
  return (
    <Flex
      px={6}
      m={1}
      mr={2}
      maxH="3rem"
      borderRadius="md"
      borderTop="1px"
      bgColor="gray.100"
      borderColor="white.300"
      boxSizing="border-box"
      transition="0.1s"
      _hover={{ bg: "secondary.200" }}
      flexBasis="100px"
      flexGrow={1}
      h="3rem"
      direction="row"
      justifySelf="center"
      justifyContent="normal"
      alignItems="baseline"
      boxShadow="lg"
    >
      <Flex flexGrow={1} placeSelf="center">
        <Tag
          alignSelf="center"
          colorScheme="secondary"
          variant="subtle"
          onClick={() =>
            filterCallback({
              direction: filterConstants.DIRECTIONS.SOURCE,
              type: filterConstants.FILTER_TYPES.ADDRESS,
              value: entry.from_address,
              conditon: filterConstants.CONDITION.EQUAL,
            })
          }
        >
          {"From:"}
          {`${entry.from_label} - ${entry.from_address}`}
        </Tag>{" "}
        <Tag
          alignSelf="center"
          colorScheme="secondary"
          variant="subtle"
          onClick={() =>
            filterCallback({
              direction: filterConstants.DIRECTIONS.DESTINATION,
              type: filterConstants.FILTER_TYPES.ADDRESS,
              value: entry.to_address,
              conditon: filterConstants.CONDITION.EQUAL,
            })
          }
        >
          {"To:"}
          {`${entry.to_label} - ${entry.to_address}`}
        </Tag>{" "}
        <Tag alignSelf="center" colorScheme="secondary" variant="subtle">
          Gas Price: {entry.gasPrice}
        </Tag>
        <Tag colorScheme="secondary" variant="subtle">
          Gas: {entry.gas}
        </Tag>
        <Tag colorScheme="secondary" variant="subtle">
          Value: {entry.value}
        </Tag>
      </Flex>

      <Text opacity="0.5" fontSize="xs" alignSelf="baseline">
        {moment(entry.created_at).format("DD MMM, YYYY, h:mm:ss")}{" "}
      </Text>
      <IconButton
        p={0}
        variant="ghost"
        boxSize="32px"
        colorScheme="primary"
        icon={<ViewIcon />}
        onClick={() => handleViewClicked(entry.id)}
      />
    </Flex>
  );
};

export default StreamEntry;
