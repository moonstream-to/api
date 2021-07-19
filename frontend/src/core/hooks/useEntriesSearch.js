import { useMutation } from "react-query";
import { JournalService } from "../services";
import { useToast } from ".";

const useEntriesSearch = ({ journalId }) => {
  const toast = useToast();

  const {
    mutateAsync: entriesSearch,
    isLoading,
    error,
    data,
  } = useMutation(
    JournalService.searchEntries({ journalId }),

    {
      onError: (error) => {
        toast(error, "error");
      },
    }
  );

  return {
    entriesSearch,
    data,
    isLoading,
    error,
  };
};

export default useEntriesSearch;
