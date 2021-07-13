import { useMutation, useQueryCache } from "react-query";
import { JournalService } from "../services";

const useCreateJournal = () => {
  const cache = useQueryCache();

  const createJournal = useMutation(JournalService.create, {
    onSuccess: (newJournal) => {
      const previousJournals = cache.getQueryData(["journals-list"]);
      const newJournals = [...previousJournals];
      newJournals.push(newJournal.data);
      newJournals.sort(function (a, b) {
        var aName = a.name.toUpperCase();
        var bName = b.name.toUpperCase();
        return aName < bName ? -1 : aName < bName ? 1 : 0;
      });

      cache.setQueryData(["journals-list"], newJournals);

      return () => cache.setQueryData(["journals-list"], previousJournals);
    },
  });

  return createJournal;
};

export default useCreateJournal;
