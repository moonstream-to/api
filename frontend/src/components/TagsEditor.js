
import { jsx } from "@emotion/react";
import { useCallback, useState, useEffect } from "react";
import { Tag, TagLabel, TagCloseButton, Flex, Input } from "@chakra-ui/react";
import { useRouter, useUpdateTag } from "../core/hooks";
import { useQueryCache } from "react-query";
const TagsEditor = ({ entry }) => {
  const router = useRouter();
  const [canEditTags, setEditTags] = useState(false);
  const cache = useQueryCache();
  const { id: journalId, entryId, appScope } = router.params;

  const [tag, setTag] = useState("");
  const updateTag = useUpdateTag(journalId, entryId);
  const onTagAdd = useCallback(
    (e) => {
      if (e.keyCode !== 13) {
        return;
      }

      if (!entry.tags.includes(e.target.value)) {
        updateTag({ tag: e.target.value, action: "add" });
      }
      setTag("");
    },
    [entry, setTag, updateTag]
  );

  useEffect(() => {
    const userPermissions = cache.getQueryData([
      "journal-permissions-current-user",
      { journalId },
    ]);
    if (userPermissions && appScope !== "public") {
      if (userPermissions.includes("journals.entries.update")) {
        setEditTags(true);
      } else {
        setEditTags(false);
      }
    } else {
      setEditTags(false);
    }
  }, [cache, appScope, journalId]);
  const onTagDelete = useCallback(
    (index) => {
      updateTag({ tag: entry.tags[index], action: "delete" });
    },
    [entry, updateTag]
  );

  return (
    <Flex alignSelf="flex-start">
      <Flex flexWrap="wrap" pl={2} pr={2} spacing={2} alignItems="center">
        {entry?.tags?.map((tag, index) => (
          <Tag
            variant="subtle"
            colorScheme="primary"
            // size="sm"
            key={`${tag}-${index}`}
            zIndex={1}
          >
            <TagLabel>{tag}</TagLabel>
            {canEditTags && (
              <TagCloseButton onClick={() => onTagDelete(index)} />
            )}
          </Tag>
        ))}
        {canEditTags && (
          <Input
            variant="newTag"
            placeholder="+ Add tag"
            onKeyUp={onTagAdd}
            value={tag}
            onChange={(e) => setTag(e.target.value)}
          />
        )}
      </Flex>
    </Flex>
  );
};

export default TagsEditor;
