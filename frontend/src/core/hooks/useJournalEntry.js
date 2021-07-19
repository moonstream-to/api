import { useQuery } from "react-query";
import { JournalService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useJournalEntry = (journalId, entryId, journalScope) => {
  const toast = useToast();
  const getEntry = async (query, key) => {
    const endpoint =
      journalScope === "personal"
        ? JournalService.getEntry
        : JournalService.getPublicEntry;
    const data = await endpoint(key, { journalId, entryId });

    const entry = data.data;
    return entry;
  };

  const { data, isLoading, isFetchedAfterMount, refetch, isError, error } =
    useQuery(["journal-entry", { journalId, entryId }], getEntry, {
      ...queryCacheProps,
      onError: (error) => toast(error, "error"),
    });

  return { data, isFetchedAfterMount, isLoading, refetch, isError, error };
};

export default useJournalEntry;
