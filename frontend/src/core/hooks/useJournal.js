import { useQuery } from "react-query";
import { JournalService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useJournal = (journalId, journalScope) => {
  const toast = useToast();

  const getJournal = async (query, key) => {
    const journalEndpoint =
      journalScope === "public"
        ? JournalService.getPublicJournal
        : JournalService.getJournal;
    const data = await journalEndpoint(key, { journalId });

    const entry = data.data;
    return entry;
  };

  const { data, isLoading, refetch } = useQuery("journal", getJournal, {
    ...queryCacheProps,
    onError: (error) => {
      toast(error, "error");
    },
  });

  return {
    data,
    isLoading,
    refetch,
  };
};

export default useJournal;
