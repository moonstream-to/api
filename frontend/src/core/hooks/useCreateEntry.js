import { useMutation, useQueryCache } from "react-query";
import { EntryService } from "../services";
import { useToast } from ".";

const useCreateEntry = (journalId) => {
  const cache = useQueryCache();
  const toast = useToast();

  const [createEntry, { isLoading, data }] = useMutation(
    EntryService.create(journalId),
    {
      onSuccess: (newEntry) => {
        const EntriesPages = cache.getQueryData([
          "journal-entries",
          { journalId },
        ]);
        EntriesPages[0].data.unshift(newEntry.data);
        EntriesPages.map((page, idx) => {
          if (idx + 1 < EntriesPages.length) {
            const ShiftedEntry = EntriesPages[idx].data.pop();
            EntriesPages[idx + 1].data.unshift(ShiftedEntry);
          }
          return page;
        });
        cache.setQueryData(["journal-entries", { journalId }], EntriesPages);
      },
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  return { createEntry, isLoading, data };
};

export default useCreateEntry;
