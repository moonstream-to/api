import React, { useContext } from "react";
import { Flex, Heading, Text, IconButton } from "@chakra-ui/react";
import moment from "moment";
import { ViewIcon } from "@chakra-ui/icons";
import { useRouter } from "../core/hooks";
import UIContext from "../core/providers/UIProvider/context";

const EntryList = ({ entry }) => {
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
      borderTop="1px"
      borderColor="white.300"
      transition="0.1s"
      _hover={{ bg: "secondary.200" }}
      width="100%"
      direction="row"
      justifyContent="normal"
      alignItems="baseline"
    >
      <Flex flexGrow={1}>
        <Heading as="h3" fontWeight="500" fontSize="md">
          {entry.title}
        </Heading>
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

export default EntryList;
