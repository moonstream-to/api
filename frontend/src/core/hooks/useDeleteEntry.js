import { useMutation, useQueryCache } from "react-query";
import { EntryService } from "../services";
import { useToast } from ".";

const useDeleteEntry = ({ entryId, journalId }) => {
  const cache = useQueryCache();
  const toast = useToast();

  const [deleteEntry] = useMutation(
    EntryService.deleteEntry(journalId, entryId),
    {
      onSuccess: () => {
        const previousEntriesPages = cache.getQueryData([
          "journal-entries",
          { journalId },
        ]);
        const newEntriesPages = [...previousEntriesPages];
        newEntriesPages.map((page) => {
          page.data = page.data.filter((entry) => entry.id !== entryId);
          return page;
        });

        cache.setQueryData(["journal-entries", { journalId }], newEntriesPages);
      },
      onError: (error) => {
        toast(error, "error");
      },
    }
  );
  return deleteEntry;
};

export default useDeleteEntry;
