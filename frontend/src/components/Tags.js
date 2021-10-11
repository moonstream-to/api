import React from "react";
import { Tag, TagLabel, Flex } from "@chakra-ui/react";
const Tags = ({ tags }) => {
  const displayTags = tags?.filter(
    (tag) =>
      tag.startsWith("from") ||
      tag.startsWith("client") ||
      tag.startsWith("network") ||
      tag.startsWith("to") ||
      tag.startsWith("source") ||
      tag.startsWith("node")
  );
  return (
    <Flex alignSelf="flex-start">
      <Flex flexWrap="wrap" pl={2} pr={2} spacing={2} alignItems="center">
        {displayTags?.map((tag, index) => (
          <Tag
            variant="subtle"
            colorScheme="blue"
            key={`${tag}-${index}`}
            zIndex={1}
          >
            <TagLabel>{tag}</TagLabel>
          </Tag>
        ))}
      </Flex>
    </Flex>
  );
};

export default Tags;
