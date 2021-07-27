import { useCallback } from "react";
import { useMutation, useQueryCache } from "react-query";
import { TagService } from "../services";
import { useToast } from ".";

const useUpdateTag = (journalId, entryId) => {
  const cache = useQueryCache();
  const entryCache = useQueryCache();
  const toast = useToast();

  const updateCache = (tagUpdate) => {
    const prevEntriesPages = cache.getQueryData([
      "journal-entries",
      { journalId },
    ]);
    const newEntriesPages = JSON.parse(JSON.stringify(prevEntriesPages));
    const prevEntry = entryCache.getQueryData([
      "journal-entry",
      { journalId, entryId },
    ]);
    const newEntry = JSON.parse(JSON.stringify(prevEntry));

    newEntriesPages.map((page) => {
      page.data = page.data.map((entry) => {
        if (entry.id === entryId) {
          var newTags;
          if (tagUpdate.action === "add") {
            newTags = [...entry.tags, tagUpdate.tag];
            entry.tags = newTags;
          } else {
            newTags = entry.tags.filter((item) => item !== tagUpdate.tag);
            entry.tags = newTags;
          }
          newEntry.tags = newTags;
          entryCache.setQueryData(
            ["journal-entry", { journalId, entryId }],
            newEntry
          );
        }

        return entry;
      });
      return page;
    });
    cache.setQueryData(["journal-entries", { journalId }], newEntriesPages);

    return { prevEntriesPages, prevEntry };
  };

  const handleError = (error, variables, context) => {
    if (context) {
      cache.setQueryData(
        ["journal-entries", { journalId }],
        context.prevEntriesPages
      );
      entryCache.setQueryData(
        ["journal-entry", { journalId, entryId }],
        context.prevEntry
      );
    }

    toast(error, "error");
  };
  const [addTag] = useMutation(TagService.createTag(journalId, entryId), {
    onMutate: (data) => {
      let retval = updateCache({ tag: data.tags[0], action: "add" });
      return retval;
    },
    onError: (error, variables, context) =>
      handleError(error, variables, context),
  });

  const [deleteTag] = useMutation(TagService.deleteTag(journalId, entryId), {
    onMutate: (data) => {
      let retval = updateCache(data);
      return retval;
    },
    onError: (error, variables, context) =>
      handleError(error, variables, context),
  });

  const updateTag = useCallback(
    (tagUpdate) => {
      switch (tagUpdate.action) {
        case "add":
          addTag({ tags: [tagUpdate.tag] });
          break;
        case "delete":
          deleteTag({ tag: tagUpdate.tag });
          break;
        default:
          return "";
      }
    },
    [addTag, deleteTag]
  );

  return updateTag;
};
export default useUpdateTag;
