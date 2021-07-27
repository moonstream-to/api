import { useMutation, useQueryClient } from "react-query";
import { EntryService } from "../services";
import { useToast } from ".";

const useUpdateEntry = (journalId, entryId) => {
  const entriesCache = useQueryClient();
  const entryCache = useQueryClient();
  const toast = useToast();

  const handleError = (error, variables, context) => {
    entriesCache.setQueryData(
      ["journal-entries", { journalId }],
      context.prevEntriesPages
    );
    entryCache.setQueryData(
      ["journal-entry", { journalId, entryId }],
      context.prevEntry
    );

    toast(error, "error");
  };

  const { mutate: updateEntry } = useMutation(
    EntryService.update(journalId, entryId),
    {
      onMutate: (newData) => {
        const prevEntriesPages = entriesCache.getQueryData([
          "journal-entries",
          { journalId },
        ]);

        const newEntriesPages = JSON.parse(JSON.stringify(prevEntriesPages));
        const prevEntry = entryCache.getQueryData([
          "journal-entry",
          { journalId, entryId },
        ]);

        const newEntry = { ...prevEntry, ...newData };

        newEntriesPages.map((page) => {
          page.data = page.data.map((entry) => {
            if (entry.id === entryId) {
              return {
                ...entry,
                ...newData,
                // for tags useUpdateTag instead
              };
            }
            return entry;
          });
          return page;
        });

        entriesCache.setQueryData(
          ["journal-entries", { journalId }],
          newEntriesPages
        );
        entryCache.setQueryData(
          ["journal-entry", { journalId, entryId }],
          newEntry
        );

        return { prevEntriesPages, prevEntry };
      },
      onError: (error, variables, context) =>
        handleError(error, variables, context),
    }
  );

  return updateEntry;
};

export default useUpdateEntry;
