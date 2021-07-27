import { useInfiniteQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { SubscriptionsService } from "../services";

const useJournalEntries = ({
  refreshRate,
  isContent,
  pageSize,
  searchQuery,
  enabled,
}) => {
  const limit = pageSize ? pageSize : 25;

  const getStream =
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

      const response = await SubscriptionsService.getStream({
        searchTerm,
        isContent,
        limit,
        offset: pageParam,
      });
      const newEntryList = response.data.stream.map((entry) => ({
        ...entry,
      }));
      return {
        data: [...newEntryList],
        pageParams: {
          pageParam: pageParam + 1,
          next_offset: response.data.next_offset,
          total_results: response.data.total_results,
          offset: response.data.offset,
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
  } = useInfiniteQuery(["stream", { searchQuery }], getStream(searchQuery), {
    refetchInterval: refreshRate,
    ...queryCacheProps,
    getNextPageParam: (lastGroup) => {
      return lastGroup.next_offset === null ? false : lastGroup.next_offset;
    },
    onSuccess: (data) => {
    },
    enabled: !!enabled,
  });

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
