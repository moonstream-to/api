import { useQuery } from "react-query";
import { JournalService } from "../services";
import { queryCacheProps } from "./hookCommon";
import { useToast } from ".";

const useJournalStats = (journalId) => {
  const toast = useToast();

  const getStats = async (query, key) => {
    const response = await JournalService.getJournalStats(key, { journalId })(
      query
    );

    return response.data;
  };

  const { data, isLoading, refetch } = useQuery(
    ["journal-stats", { journalId }],
    getStats,
    {
      ...queryCacheProps,
      onError: (error) => {
        toast(error, "error");
      },
      onSuccess: () => {},
    }
  );

  return {
    data,
    isLoading,
    refetch,
  };
};

export default useJournalStats;
