import { useMutation, useQueryCache } from "react-query";
import { JournalService } from "../services";
import { useToast } from ".";

const useDeleteJournal = (id) => {
  const cache = useQueryCache();
  const toast = useToast();

  const [deleteJournal] = useMutation(JournalService.deleteJournal(id), {
    onMutate: () => {
      const previousJournals = [...cache.getQueryData(["journals-list"])];

      const newJournals = previousJournals.filter(
        (journal) => journal.id !== id
      );
      cache.setQueryData(["journals-list"], newJournals);

      return { previousJournals };
    },
    onError: (error, variables, context) => {
      cache.setQueryData(["journals-list"], context.previousJournals);
      toast("Not enough permisions to delete this Journal", "error");
    },
  });

  return { deleteJournal };
};

export default useDeleteJournal;
