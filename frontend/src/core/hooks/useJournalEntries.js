import { useInfiniteQuery } from "react-query";
import { useEntriesSearch } from ".";
import { queryCacheProps } from "./hookCommon";

const useJournalEntries = ({
  journalId,
  journalType,
  isContent,
  pageSize,
  searchQuery,
}) => {
  const limit = pageSize ? pageSize : 25;

  const { entriesSearch } = useEntriesSearch({
    journalId,
  });

  const getEntries =
    (searchTerm) =>
    async ({ pageParam = 0 }) => {
      if (!pageParam) {
        pageParam = 0;
      }

      const searchTags = searchTerm.split(" ").filter(function (n) {
        if (n.startsWith("#")) return n;
        else {
          return null;
        }
      });

      const data = await entriesSearch({
        searchTerm,
        journalType,
        isContent,
        limit,
        offset: pageParam,
        searchTags,
      });
      const newEntryList = data.data.results.map((entry) => ({
        ...entry,
        id: entry.entry_url.split("/").pop(),
      }));
      return {
        data: [...newEntryList],
        pageParams: {
          pageParam: pageParam + 1,
          next_offset: data.data.next_offset,
          total_results: data.data.total_results,
          offset: data.data.offset,
        },
      };
    };

  const {
    data: EntriesPages,
    isFetchingMore,
    isLoading,
    canFetchMore,
    fetchMore,
    refetch,
  } = useInfiniteQuery(
    ["journal-entries", { journalId }],
    getEntries(searchQuery),
    {
      refetchInterval: 1000,
      ...queryCacheProps,
      // getNextPageParam: (lastPage) => lastPage.next_offset ?? false,
      getNextPageParam: (lastGroup) => {
        return lastGroup.next_offset === null ? false : lastGroup.next_offset;
      },
      enabled: !!journalId,
    }
  );

  return {
    EntriesPages,
    fetchMore,
    isFetchingMore,
    canFetchMore,
    refetch,
    isLoading,
  };
};

export default useJournalEntries;
