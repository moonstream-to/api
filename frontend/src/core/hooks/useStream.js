import { useInfiniteQuery } from "react-query";
import { queryCacheProps } from "./hookCommon";
import { SubscriptionsService } from "../services";
import moment from "moment";

const useJournalEntries = ({
  refreshRate,
  isContent,
  pageSize,
  searchQuery,
  enabled,
}) => {
  //const limit = pageSize ? pageSize : 25;

  const getStream =
    (searchTerm) =>
    async ({ pageParam = { start_time: 0, end_time: 0 } }) => {
      console.log("pageParam", pageParam);

      const response = await SubscriptionsService.getStream({
        searchTerm: searchTerm,
        start_time: pageParam.start_time,
        end_time: pageParam.end_time,
      });

      const newEntryList = response.data.stream.map((entry) => ({
        ...entry,
      }));

      console.log("response.data", response.data);
      return {
        data: [...newEntryList],
        pageParams: {
          start_time: response.data.start_time,
          end_time: response.data.end_time,
        },
      };
    };

  const {
    data: EntriesPages,
    isFetchingMore,
    isLoading,
    fetchNextPage,
    fetchPreviousPage,
    hasNextPage,
    canFetchMore,
    fetchMore,
    refetch,
  } = useInfiniteQuery(["stream", { searchQuery }], getStream(searchQuery), {
    refetchInterval: refreshRate,
    ...queryCacheProps,
    getNextPageParam: (lastGroup) => {
      console.log("lastGroup", lastGroup);
      console.log("canFetchMore", canFetchMore);
      console.log("fetchMore", fetchMore);
      console.log("fetchNextPage", fetchNextPage);
      console.log("fetchPreviousPage", fetchPreviousPage);
      console.log("hasNextPage", hasNextPage);

      return 1;
    },
    onSuccess: () => {},
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
