
import { jsx } from "@emotion/react";
import { Tag, TagLabel, Flex, Button } from "@chakra-ui/react";
import { useState } from "react";

const TAGS_DISPLAY_NUM_DEF = 5;
const TagsList = ({ tags }) => {
  const [showAllTags, toggleAllTags] = useState(false);
  const tagButtonText = showAllTags ? "Show less" : "Show all";

  const TagsToShow = () =>
    tags
      .filter((tag, i) => (showAllTags ? true : i < TAGS_DISPLAY_NUM_DEF))
      .map((tag, index) => {
        return (
          <Tag
            variant="subtle"
            colorScheme="primary"
            size="sm"
            key={`${tag}-${index}`}
          >
            <TagLabel>{tag}</TagLabel>
          </Tag>
        );
      });

  return (
    <Flex display="flex" flexWrap="wrap" align="center" spacing={1}>
      <TagsToShow />
      {tags.length > TAGS_DISPLAY_NUM_DEF && (
        <Button
          m={1}
          onClick={() => toggleAllTags(!showAllTags)}
          size="xs"
          variant="link"
          color="primary.600"
          ml={1}
          style={{ transform: "translateY(-1px)" }}
        >
          {tagButtonText}
        </Button>
      )}
    </Flex>
  );
};
export default TagsList;
